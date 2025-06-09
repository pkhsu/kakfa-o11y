# Stage 1: Build the application
FROM maven:3.9-eclipse-temurin-11 AS builder
WORKDIR /app
COPY pom.xml .
COPY src ./src
RUN mvn clean package

# Stage 2: Create the runtime image
FROM eclipse-temurin:11-jre
WORKDIR /app

# Download OpenTelemetry Java Agent
ARG OTEL_AGENT_VERSION=1.32.0
RUN apt-get update && apt-get install -y curl && \
    curl -L -o opentelemetry-javaagent.jar \
       https://github.com/open-telemetry/opentelemetry-java-instrumentation/releases/download/v${OTEL_AGENT_VERSION}/opentelemetry-javaagent.jar && \
    apt-get remove -y curl && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/target/java-producer-1.0-SNAPSHOT.jar /app/java-producer.jar

ENV OTEL_SERVICE_NAME="java-kafka-producer"
# OTLP gRPC endpoint
ENV OTEL_EXPORTER_OTLP_ENDPOINT="http://otel-collector:4317"
ENV OTEL_METRICS_EXPORTER="otlp"
# Send logs via OTLP
ENV OTEL_LOGS_EXPORTER="otlp"
ENV OTEL_TRACES_EXPORTER="otlp"
# Enable Kafka client instrumentation (usually on by default with the agent)
ENV OTEL_INSTRUMENTATION_KAFKA_ENABLED="true"
# Propagate trace context
ENV OTEL_PROPAGATORS="tracecontext,baggage"

# For Logback appender to find the SDK
ENV OTEL_SDK_DISABLED="false"

ENTRYPOINT ["java", \
           "-javaagent:/app/opentelemetry-javaagent.jar", \
           "-jar", "/app/java-producer.jar"]
