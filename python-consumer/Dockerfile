FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY consumer.py .

ENV OTEL_SERVICE_NAME="python-kafka-consumer"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"
ENV KAFKA_BOOTSTRAP_SERVERS="kafka:9092"
ENV PYTHONUNBUFFERED=1

CMD ["python", "consumer.py"]
