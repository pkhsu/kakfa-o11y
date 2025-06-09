import os
import time
import logging
import signal # For graceful shutdown

from kafka import KafkaConsumer
from kafka.errors import KafkaError

from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME as ResourceAttributesServiceName

# from opentelemetry.instrumentation.kafka import KafkaInstrumentor
# from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator # For manual context extraction if needed

# --- Configuration ---
OTEL_SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "python-kafka-consumer")
OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")
KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
TOPIC_NAME = "tutorial-topic"
CONSUMER_GROUP_ID = "python-consumer-group"

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- OpenTelemetry Setup ---
def setup_opentelemetry():
    resource = Resource(attributes={
        ResourceAttributesServiceName: OTEL_SERVICE_NAME
    })

    tracer_provider = TracerProvider(resource=resource)
    span_exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    )
    meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
    metrics.set_meter_provider(meter_provider)

    # KafkaInstrumentor().instrument()
    # LoggingInstrumentor().instrument(set_logging_format=True)

    logger.info(f"OpenTelemetry configured for {OTEL_SERVICE_NAME} sending to {OTEL_EXPORTER_OTLP_ENDPOINT}")

setup_opentelemetry()
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Custom metric example
message_received_counter = meter.create_counter(
    "python.consumer.messages_received",
    description="Counts the number of messages received by the Python consumer",
    unit="1"
)
processing_time_histogram = meter.create_histogram(
    "python.consumer.message_processing_duration",
    description="Measures the duration of message processing in the Python consumer",
    unit="ms"
)


# --- Kafka Consumer ---
def create_consumer():
    try:
        consumer = KafkaConsumer(
            TOPIC_NAME,
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
            client_id=OTEL_SERVICE_NAME,
            group_id=CONSUMER_GROUP_ID,
            auto_offset_reset='earliest', # Start from the beginning if no offset committed
            enable_auto_commit=True, # Auto commit offsets
            # For manual context extraction (KafkaInstrumentor usually handles this)
            # value_deserializer=lambda v: v.decode('utf-8')
        )
        logger.info(f"KafkaConsumer connected to {KAFKA_BOOTSTRAP_SERVERS} and subscribed to {TOPIC_NAME}")
        return consumer
    except Exception as e:
        logger.error(f"Failed to connect Kafka consumer: {e}")
        time.sleep(10) # Wait before retrying or exiting
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
            # The KafkaConsumer is an iterator, or you can use poll
            for message in consumer: # This blocks until a message is available or timeout
                if not running: break # Check running flag after waking up

                # KafkaInstrumentor should automatically create a span for message processing
                # and link it to the producer's trace via headers.
                # If manual context extraction/span creation is needed:
                # headers = {k: v.decode('utf-8') for k, v in message.headers}
                # parent_context = TraceContextTextMapPropagator().extract(carrier=headers)
                # with tracer.start_as_current_span("process_python_kafka_message", context=parent_context) as span:

                # With auto-instrumentation, the span is typically named like "destination process"
                # e.g. "tutorial-topic process"

                start_time = time.monotonic()
                try:
                    logger.info(
                        f"Received message: Key='{message.key.decode() if message.key else ''}', "
                        f"Value='{message.value.decode() if message.value else ''}', "
                        f"Partition={message.partition}, Offset={message.offset}"
                    )
                    # Simulate message processing
                    time.sleep(0.05) # 50ms processing time

                    message_received_counter.add(1, {"status": "success"})
                    current_span = trace.get_current_span()
                    current_span.set_attribute("messaging.message_payload_size_bytes", len(message.value))
                    current_span.set_attribute("custom.processing.status", "completed")

                except Exception as e:
                    logger.error(f"Error processing message: {e}", exc_info=True)
                    message_received_counter.add(1, {"status": "error"})
                    current_span = trace.get_current_span()
                    current_span.set_attribute("error", True)
                    current_span.set_attribute("error.message", str(e))
                finally:
                    duration_ms = (time.monotonic() - start_time) * 1000
                    processing_time_histogram.record(duration_ms)


                if not running: break
            if not running: break # Exit outer loop if shutdown signal received
            time.sleep(0.1) # Small sleep if consumer iterator times out or loop finishes an iteration

    except KafkaError as e:
        logger.error(f"Kafka consumer error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred in Python consumer: {e}", exc_info=True)
    finally:
        if consumer:
            logger.info("Closing Python Kafka consumer.")
            consumer.close() # This will also commit offsets if auto-commit is enabled
        logger.info("Python consumer application finished.")
