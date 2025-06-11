import os
import time
import logging
import uuid
import json
from datetime import datetime

from kafka import KafkaProducer
from kafka.errors import KafkaError

from opentelemetry import trace, metrics, _logs
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Status, StatusCode

# Auto instrumentation packages removed for manual instrumentation # For log correlation

# --- Configuration ---
OTEL_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "python-kafka-producer")
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC_NAME = "tutorial-topic"
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- OpenTelemetry Setup ---
def setup_opentelemetry():
    # Enhanced resource attributes
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: OTEL_SERVICE_NAME,
        ResourceAttributes.SERVICE_VERSION: SERVICE_VERSION,
        ResourceAttributes.SERVICE_NAMESPACE: "kafka-tutorial",
        ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "tutorial",
        "component.type": "producer",
        "language": "python",
        "kafka.topic": TOPIC_NAME,
        "messaging.system": "kafka",
    })

    # Tracer Provider
    tracer_provider = TracerProvider(resource=resource)
    span_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Meter Provider
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True),
        export_interval_millis=5000
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # Logger Provider for OTLP log export
    logger_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    _logs.set_logger_provider(logger_provider)
    
    # Attach OTEL handler to root logger
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)

    logger.info(f"OpenTelemetry configured for {OTEL_SERVICE_NAME} v{SERVICE_VERSION} sending to {OTEL_EXPORTER_OTLP_ENDPOINT}")

setup_opentelemetry()
tracer = trace.get_tracer(__name__, SERVICE_VERSION)
meter = metrics.get_meter(__name__, SERVICE_VERSION)

# Unified metric naming with consistent labels
messages_sent_counter = meter.create_counter(
    "kafka_messages_sent_total",
    description="Total number of messages sent to Kafka",
    unit="1"
)

messages_sent_bytes = meter.create_counter(
    "kafka_messages_sent_bytes_total", 
    description="Total bytes of messages sent to Kafka",
    unit="By"
)

message_send_duration = meter.create_histogram(
    "kafka_message_send_duration_ms",
    description="Time taken to send a message to Kafka",
    unit="ms"
)

kafka_producer_active = meter.create_up_down_counter(
    "kafka_producer_active",
    description="Whether the producer is active (1) or not (0)",
    unit="1"
)

# --- Kafka Producer ---
def create_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
            client_id=f"{OTEL_SERVICE_NAME}-{uuid.uuid4().hex[:8]}",
            acks='all',
            retries=3,
            max_in_flight_requests_per_connection=1,  # For ordering
            batch_size=16384,
            linger_ms=10,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        logger.info(f"KafkaProducer connected to {KAFKA_BOOTSTRAP_SERVERS}")
        kafka_producer_active.add(1, {"status": "active", "language": "python", "component": "producer"})
        return producer
    except Exception as e:
        logger.error(f"Failed to connect Kafka producer: {e}")
        kafka_producer_active.add(0, {"status": "failed", "language": "python", "component": "producer"})
        time.sleep(10)
        raise

# --- Main Application ---
if __name__ == "__main__":
    producer = None
    try:
        producer = create_producer()
        message_count = 0
        
        while True:
            message_count += 1
            message_id = str(uuid.uuid4())
            
            # Create message payload with metadata
            message_payload = {
                "id": message_id,
                "count": message_count,
                "timestamp": datetime.utcnow().isoformat(),
                "producer": "python",
                "version": SERVICE_VERSION,
                "content": f"Hello from Python Producer! Message #{message_count}"
            }

            # Create a span for the send operation with enhanced attributes
            with tracer.start_as_current_span("kafka_message_send") as span:
                start_time = time.time()
                
                # Set comprehensive span attributes
                span.set_attributes({
                    SpanAttributes.MESSAGING_SYSTEM: "kafka",
                    SpanAttributes.MESSAGING_DESTINATION: TOPIC_NAME,
                    SpanAttributes.MESSAGING_DESTINATION_KIND: "topic",
                    SpanAttributes.MESSAGING_MESSAGE_ID: message_id,
                    SpanAttributes.MESSAGING_KAFKA_MESSAGE_KEY: message_id,
                    "messaging.kafka.client_id": producer.config['client_id'],
                    "messaging.operation": "send",
                    "component.type": "producer",
                    "language": "python",
                    "message.count": message_count,
                    "message.size_bytes": len(json.dumps(message_payload).encode('utf-8')),
                })

                try:
                    future = producer.send(
                        TOPIC_NAME, 
                        key=message_id, 
                        value=message_payload
                    )
                    
                    record_metadata = future.get(timeout=10)
                    duration_ms = (time.time() - start_time) * 1000
                    
                    # Enhanced logging with structured data
                    logger.info(
                        f"Message sent successfully - ID: {message_id}, "
                        f"Count: {message_count}, Partition: {record_metadata.partition}, "
                        f"Offset: {record_metadata.offset}, Duration: {duration_ms:.2f}ms"
                    )
                    
                    # Record metrics with consistent labels
                    base_labels = {
                        "status": "success",
                        "language": "python", 
                        "component": "producer",
                        "topic": TOPIC_NAME,
                        "partition": str(record_metadata.partition)
                    }
                    
                    messages_sent_counter.add(1, base_labels)
                    messages_sent_bytes.add(
                        len(json.dumps(message_payload).encode('utf-8')), 
                        base_labels
                    )
                    message_send_duration.record(duration_ms, base_labels)
                    
                    # Update span with success attributes
                    span.set_attributes({
                        "messaging.kafka.partition": record_metadata.partition,
                        "messaging.kafka.offset": record_metadata.offset,
                        "messaging.kafka.timestamp": record_metadata.timestamp,
                        "duration_ms": duration_ms,
                    })
                    span.set_status(Status(StatusCode.OK))
                    
                except KafkaError as e:
                    duration_ms = (time.time() - start_time) * 1000
                    logger.error(f"Error sending message ID {message_id}: {e}")
                    
                    # Record error metrics
                    error_labels = {
                        "status": "error",
                        "language": "python",
                        "component": "producer", 
                        "topic": TOPIC_NAME,
                        "error_type": type(e).__name__
                    }
                    
                    messages_sent_counter.add(1, error_labels)
                    message_send_duration.record(duration_ms, error_labels)
                    
                    # Update span with error attributes
                    span.set_attributes({
                        "error": True,
                        "error.type": type(e).__name__,
                        "error.message": str(e),
                        "duration_ms": duration_ms,
                    })
                    span.set_status(Status(StatusCode.ERROR, str(e)))

                producer.flush()
                time.sleep(5)

    except Exception as e:
        logger.error(f"An unexpected error occurred in Python producer: {e}", exc_info=True)
        kafka_producer_active.add(-1, {"status": "error", "language": "python", "component": "producer"})
    finally:
        if producer:
            logger.info("Closing Python Kafka producer.")
            producer.close()
            kafka_producer_active.add(-1, {"status": "shutdown", "language": "python", "component": "producer"})
        logger.info("Python producer application finished.")
