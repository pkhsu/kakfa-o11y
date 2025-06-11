import os
import time
import logging
import signal
import json
from datetime import datetime

from kafka import KafkaConsumer
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
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator

# --- Configuration ---
OTEL_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "python-kafka-consumer")
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC_NAME = "tutorial-topic"
CONSUMER_GROUP_ID = "python-consumer-group"
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "1.0.0")

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# --- Helper Functions ---
def safe_deserialize_message(message_bytes):
    """Safely deserialize message value, handling both JSON and plain text"""
    try:
        decoded = message_bytes.decode('utf-8')
        # Try to parse as JSON first
        return json.loads(decoded)
    except json.JSONDecodeError:
        # If not valid JSON, return as plain text wrapped in a dict
        return {
            "content": decoded,
            "type": "plain_text",
            "source": "unknown"
        }
    except Exception as e:
        logger.warning(f"Failed to deserialize message: {e}")
        return {
            "content": str(message_bytes),
            "type": "raw_bytes", 
            "error": str(e)
        }

# --- OpenTelemetry Setup ---
def setup_opentelemetry():
    # Enhanced resource attributes
    resource = Resource.create({
        ResourceAttributes.SERVICE_NAME: OTEL_SERVICE_NAME,
        ResourceAttributes.SERVICE_VERSION: SERVICE_VERSION,
        ResourceAttributes.SERVICE_NAMESPACE: "kafka-tutorial",
        ResourceAttributes.DEPLOYMENT_ENVIRONMENT: "tutorial",
        "component.type": "consumer",
        "language": "python",
        "kafka.topic": TOPIC_NAME,
        "kafka.consumer_group": CONSUMER_GROUP_ID,
        "messaging.system": "kafka",
    })

    tracer_provider = TracerProvider(resource=resource)
    span_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

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
messages_received_counter = meter.create_counter(
    "kafka_messages_received_total",
    description="Total number of messages received from Kafka",
    unit="1"
)

messages_received_bytes = meter.create_counter(
    "kafka_messages_received_bytes_total",
    description="Total bytes of messages received from Kafka", 
    unit="By"
)

message_processing_duration = meter.create_histogram(
    "kafka_message_processing_duration_ms",
    description="Time taken to process a message from Kafka",
    unit="ms"
)

consumer_lag = meter.create_up_down_counter(
    "kafka_consumer_lag",
    description="Current consumer lag (estimated)",
    unit="1"
)

kafka_consumer_active = meter.create_up_down_counter(
    "kafka_consumer_active",
    description="Whether the consumer is active (1) or not (0)",
    unit="1"
)

# --- Kafka Consumer ---
def create_consumer():
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
            client_id=f"{OTEL_SERVICE_NAME}",
            group_id=CONSUMER_GROUP_ID,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            auto_commit_interval_ms=1000,
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000,
            fetch_min_bytes=1,
            fetch_max_wait_ms=500,
            max_poll_records=100,
            value_deserializer=lambda v: safe_deserialize_message(v) if v else None,
            key_deserializer=lambda k: k.decode('utf-8') if k else None
        )
        logger.info(f"KafkaConsumer connected to {KAFKA_BOOTSTRAP_SERVERS} and subscribed to {TOPIC_NAME}")
        kafka_consumer_active.add(1, {"status": "active", "language": "python", "component": "consumer"})
        return consumer
    except Exception as e:
        logger.error(f"Failed to connect Kafka consumer: {e}")
        kafka_consumer_active.add(0, {"status": "failed", "language": "python", "component": "consumer"})
        time.sleep(10)
        raise

# --- Graceful Shutdown ---
running = True
def signal_handler(signum, frame):
    global running
    logger.info(f"Signal {signum} received, shutting down...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

# --- Main Application ---
if __name__ == "__main__":
    consumer = None
    try:
        consumer = create_consumer()
        logger.info("Python Kafka consumer started. Waiting for messages...")
        
        while running:
            # Poll for messages with timeout
            messages = consumer.poll(timeout_ms=1000)
            
            if not messages:
                continue
                
            for topic_partition, records in messages.items():
                for message in records:
                    if not running:
                        break
                        
                    start_time = time.time()
                    
                    # Extract trace context from headers if available
                    headers = dict(message.headers) if message.headers else {}
                    string_headers = {k: v.decode('utf-8') if isinstance(v, bytes) else str(v) 
                                    for k, v in headers.items()}
                    
                    # Create span for message processing with parent context
                    propagator = TraceContextTextMapPropagator()
                    parent_context = propagator.extract(carrier=string_headers)
                    
                    with tracer.start_as_current_span(
                        "kafka_message_process", 
                        context=parent_context
                    ) as span:
                        try:
                            # Set comprehensive span attributes
                            span.set_attributes({
                                SpanAttributes.MESSAGING_SYSTEM: "kafka",
                                SpanAttributes.MESSAGING_DESTINATION: TOPIC_NAME,
                                SpanAttributes.MESSAGING_DESTINATION_KIND: "topic",
                                SpanAttributes.MESSAGING_OPERATION: "process",
                                SpanAttributes.MESSAGING_KAFKA_CONSUMER_GROUP: CONSUMER_GROUP_ID,
                                SpanAttributes.MESSAGING_KAFKA_MESSAGE_KEY: message.key,
                                "messaging.kafka.partition": message.partition,
                                "messaging.kafka.offset": message.offset,
                                "component.type": "consumer",
                                "language": "python",
                                "message.size_bytes": len(message.value) if message.value else 0,
                                "message.timestamp": message.timestamp,
                            })
                            
                            # Process message payload
                            payload = message.value
                            # Handle different message formats
                            if isinstance(payload, dict):
                                if 'id' in payload:
                                    # JSON message from Python producer
                                    message_id = payload.get('id', 'unknown')
                                    content = payload.get('content', str(payload))
                                elif 'content' in payload and payload.get('type') == 'plain_text':
                                    # Plain text message (e.g., from Java producer)
                                    message_id = 'plain-text-msg'
                                    content = payload['content']
                                else:
                                    message_id = 'unknown'
                                    content = str(payload)
                            else:
                                message_id = 'raw-msg'
                                content = str(payload)
                            
                            logger.info(
                                f"Processing message - ID: {message_id}, "
                                f"Key: {message.key}, Partition: {message.partition}, "
                                f"Offset: {message.offset}, Size: {len(str(payload))} bytes, "
                                f"Content: {content[:100]}..."  # Show first 100 chars
                            )
                            
                            # Simulate message processing
                            time.sleep(0.05)  # 50ms processing time
                            
                            processing_duration = (time.time() - start_time) * 1000
                            
                            # Record successful processing metrics
                            base_labels = {
                                "status": "success",
                                "language": "python",
                                "component": "consumer", 
                                "topic": TOPIC_NAME,
                                "partition": str(message.partition),
                                "consumer_group": CONSUMER_GROUP_ID
                            }
                            
                            messages_received_counter.add(1, base_labels)
                            messages_received_bytes.add(
                                len(str(payload)) if payload else 0,
                                base_labels
                            )
                            message_processing_duration.record(processing_duration, base_labels)
                            
                            # Update span with success attributes
                            span.set_attributes({
                                "processing.duration_ms": processing_duration,
                                "processing.status": "completed",
                                "message.id": message_id,
                            })
                            span.set_status(Status(StatusCode.OK))
                            
                        except Exception as e:
                            processing_duration = (time.time() - start_time) * 1000
                            logger.error(f"Error processing message: {e}", exc_info=True)
                            
                            # Record error metrics
                            error_labels = {
                                "status": "error",
                                "language": "python",
                                "component": "consumer",
                                "topic": TOPIC_NAME,
                                "partition": str(message.partition),
                                "consumer_group": CONSUMER_GROUP_ID,
                                "error_type": type(e).__name__
                            }
                            
                            messages_received_counter.add(1, error_labels)
                            message_processing_duration.record(processing_duration, error_labels)
                            
                            # Update span with error attributes  
                            span.set_attributes({
                                "error": True,
                                "error.type": type(e).__name__,
                                "error.message": str(e),
                                "processing.duration_ms": processing_duration,
                            })
                            span.set_status(Status(StatusCode.ERROR, str(e)))
                            
                if not running:
                    break
                    
            if not running:
                break
                
    except KafkaError as e:
        logger.error(f"Kafka consumer error: {e}")
        kafka_consumer_active.add(-1, {"status": "error", "language": "python", "component": "consumer"})
    except Exception as e:
        logger.error(f"An unexpected error occurred in Python consumer: {e}", exc_info=True)
        kafka_consumer_active.add(-1, {"status": "error", "language": "python", "component": "consumer"})
    finally:
        if consumer:
            logger.info("Closing Python Kafka consumer.")
            consumer.close()
            kafka_consumer_active.add(-1, {"status": "shutdown", "language": "python", "component": "consumer"})
        logger.info("Python consumer application finished.")
