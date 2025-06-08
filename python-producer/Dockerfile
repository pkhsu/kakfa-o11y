FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if any (e.g., for some gRPC components if not pre-installed)
# RUN apt-get update && apt-get install -y <any-dependencies> && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY producer.py .

# Environment variables for OpenTelemetry (can also be set in docker-compose.yml)
ENV OTEL_SERVICE_NAME="python-kafka-producer"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317" # OTLP gRPC endpoint for Python
# Note: Python OTLP exporter by default uses gRPC. If HTTP is needed, use OTLPSpanExporterHttp, etc.
# ENV OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf" # If OTLP HTTP is preferred
ENV KAFKA_BOOTSTRAP_SERVERS="kafka:9092"

# Ensure logs are sent with trace context by LoggingInstrumentor
ENV PYTHONUNBUFFERED=1 # Ensures logs are sent out immediately

CMD ["python", "producer.py"]
