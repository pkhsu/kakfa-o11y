# Build stage
FROM golang:1.23 AS builder

WORKDIR /app

# Install librdkafka dependencies
RUN apt-get update && apt-get install -y \
    librdkafka-dev \
    pkg-config \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy go mod files
COPY go.mod go.sum ./
RUN go mod download

# Copy source
COPY . .

# Build
RUN CGO_ENABLED=1 go build -o /go-producer main.go

# Runtime stage
FROM ubuntu:latest

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    librdkafka1 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy binary
COPY --from=builder /go-producer /go-producer

ENV OTEL_SERVICE_NAME="go-kafka-producer"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="otel-collector:4317"
ENV KAFKA_BOOTSTRAP_SERVERS="kafka:9092"

# Set the entrypoint
ENTRYPOINT ["/go-producer"]
