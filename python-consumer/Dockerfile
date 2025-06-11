FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Auto-install instrumentation packages
RUN opentelemetry-bootstrap -a install

COPY consumer.py .

# Environment variables for Zero-code OpenTelemetry Auto-instrumentation
ENV OTEL_SERVICE_NAME="python-kafka-consumer"
ENV OTEL_SERVICE_VERSION="1.0.0"
ENV OTEL_SERVICE_NAMESPACE="kafka-tutorial"
ENV OTEL_RESOURCE_ATTRIBUTES="deployment.environment=tutorial,component.type=consumer,language=python"

# OTLP Configuration
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"
ENV OTEL_EXPORTER_OTLP_PROTOCOL="grpc"

# Enable automatic instrumentation
ENV OTEL_PYTHON_LOG_CORRELATION="true"
ENV OTEL_PYTHON_LOG_LEVEL="info"

# Auto-instrument Kafka
ENV OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=""

# Kafka Configuration
ENV KAFKA_BOOTSTRAP_SERVERS="kafka:9092"

# Ensure logs are sent out immediately
ENV PYTHONUNBUFFERED=1

# Use auto-instrumentation to start the application
CMD ["opentelemetry-instrument", "python", "consumer.py"]
