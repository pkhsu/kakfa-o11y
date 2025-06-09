# Stage 1: Build the Go application
FROM golang:1.23-bullseye AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y librdkafka-dev && rm -rf /var/lib/apt/lists/*

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=1 go build -o /go-consumer main.go


# Stage 2: Create the runtime image
FROM debian:bullseye-slim

WORKDIR /app

RUN apt-get update && apt-get install -y librdkafka1 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /go-consumer /go-consumer

ENV OTEL_SERVICE_NAME="go-kafka-consumer"
ENV OTEL_EXPORTER_OTLP_ENDPOINT="otel-collector:4317"
ENV KAFKA_BOOTSTRAP_SERVERS="kafka:9092"

ENTRYPOINT ["/go-consumer"]
