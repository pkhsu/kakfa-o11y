# Stage 1: Build the Go application
FROM golang:1.23-bullseye AS builder

WORKDIR /app

# Install build dependencies for confluent-kafka-go (librdkafka)
RUN apt-get update && apt-get install -y librdkafka-dev && rm -rf /var/lib/apt/lists/*

COPY go.mod go.sum ./
# Download dependencies first to leverage Docker cache
RUN go mod download

COPY . .
RUN CGO_ENABLED=1 go build -o /go-producer main.go


# Stage 2: Create the runtime image
FROM debian:bullseye-slim

WORKDIR /app

# Install runtime dependencies for confluent-kafka-go (librdkafka)
RUN apt-get update && apt-get install -y librdkafka1 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /go-producer /go-producer

ENV OTEL_SERVICE_NAME="go-kafka-producer"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="otel-collector:4317"
ENV KAFKA_BOOTSTRAP_SERVERS="kafka:9092"

# Set the entrypoint
ENTRYPOINT ["/go-producer"]
