import os
import time
import logging
import uuid

from kafka import KafkaProducer
from kafka.errors import KafkaError

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME as ResourceAttributesServiceName

# from opentelemetry.instrumentation.kafka import KafkaInstrumentor # Auto instrumentation
# from opentelemetry.instrumentation.logging import LoggingInstrumentor # For log correlation

# --- Configuration ---
OTEL_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "python-kafka-producer")
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317") # gRPC endpoint by default for OTLPExporter
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC_NAME = "tutorial-topic"

# --- Logging Setup ---
# Basic logging config
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- OpenTelemetry Setup ---
def setup_opentelemetry():
    resource = Resource(attributes={
        ResourceAttributesServiceName: OTEL_SERVICE_NAME
    })

    # Tracer Provider
    tracer_provider = TracerProvider(resource=resource)
    span_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    # Meter Provider
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # Auto-instrumentation (disabled for now)
    # KafkaInstrumentor().instrument() # Instrument kafka-python
    # LoggingInstrumentor().instrument(set_logging_format=True) # Instrument logging

    logger.info(f"OpenTelemetry configured for {OTEL_SERVICE_NAME} sending to {OTEL_EXPORTER_OTLP_ENDPOINT}")

setup_opentelemetry()
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Custom metric example
message_counter = meter.create_counter(
    "python.producer.messages_sent",
    description="Counts the number of messages sent by the Python producer",
    unit="1"
)

# --- Kafka Producer ---
def create_producer():
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
            client_id=OTEL_SERVICE_NAME,
            acks='all', # For reliability
            retries=3, # Retry up to 3 times
            # value_serializer=lambda v: json.dumps(v).encode('utf-8') # If sending JSON
        )
        logger.info(f"KafkaProducer connected to {KAFKA_BOOTSTRAP_SERVERS}")
        return producer
    except Exception as e:
        logger.error(f"Failed to connect Kafka producer: {e}")
        # Consider a retry mechanism or exit if critical
        time.sleep(10) # Wait before retrying or exiting
        raise

# --- Main Application ---
if __name__ == "__main__":
    producer = None
    try:
        producer = create_producer()
        message_count = 0
        while True:
            message_id = str(uuid.uuid4())
            message_value = f"Hello from Python Producer! Message ID: {message_id}, Count: {message_count}"

            # Create a span for the send operation
            with tracer.start_as_current_span("send_python_kafka_message") as span:
                span.set_attribute("messaging.system", "kafka")
                span.set_attribute("messaging.destination", TOPIC_NAME)
                span.set_attribute("messaging.message_id", message_id)

                future = producer.send(TOPIC_NAME, key=message_id.encode('utf-8'), value=message_value.encode('utf-8'))

                try:
                    record_metadata = future.get(timeout=10)
                    logger.info(
                        f"Sent message: ID='{message_id}', "
                        f"Partition={record_metadata.partition}, Offset={record_metadata.offset}"
                    )
                    message_counter.add(1, {"status": "success"})
                    span.set_attribute("messaging.kafka.partition", record_metadata.partition)
                    span.set_attribute("messaging.kafka.offset", record_metadata.offset)
                except KafkaError as e:
                    logger.error(f"Error sending message ID {message_id}: {e}")
                    message_counter.add(1, {"status": "error"})
                    span.set_attribute("error", True)
                    span.set_attribute("error.message", str(e))

                producer.flush() # Ensure all buffered messages are sent
                message_count += 1
                time.sleep(5) # Send a message every 5 seconds

    except KafkaError as e:
        logger.error(f"Kafka producer error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred in Python producer: {e}", exc_info=True)
    finally:
        if producer:
            logger.info("Closing Python Kafka producer.")
            producer.close()
        logger.info("Python producer application finished.")
