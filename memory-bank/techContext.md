# Technical Context

## Technologies Used

### Core Infrastructure
- **Apache Kafka 3.6.1**: Core messaging platform with comprehensive JMX metrics exposure
- **Apache Zookeeper**: Kafka cluster coordination and metadata management
- **Docker & Docker Compose**: Containerized environment orchestration
- **Confluent Kafka Distribution**: Enhanced Kafka images with additional tooling

### Observability Stack (Grafana LGTM)
- **OpenTelemetry Collector**: Centralized telemetry collection and processing
- **Prometheus**: Metrics storage and time-series database
- **Loki**: Log aggregation and querying
- **Tempo**: Distributed tracing storage and analysis
- **Grafana**: Unified observability visualization and dashboards

### Application Languages & Frameworks

#### Java Applications
- **Java 11**: Runtime environment
- **Maven 3.x**: Build and dependency management
- **Kafka Clients 3.6.1**: Native Kafka client library
- **OpenTelemetry Java Agent**: Auto-instrumentation for zero-code observability
- **SLF4J + Logback**: Logging framework with structured output
- **JUnit 5 + Mockito**: Testing framework

#### Python Applications
- **Python 3.x**: Runtime environment
- **kafka-python**: Kafka client library
- **OpenTelemetry Python SDK**: Manual instrumentation with full control
- **pytest + pytest-mock**: Testing framework
- **Structured logging**: JSON-formatted logs with trace correlation

#### Go Applications
- **Go 1.21+**: Runtime environment
- **confluent-kafka-go/v2**: High-performance Kafka client (CGO-based)
- **OpenTelemetry Go SDK**: Manual instrumentation with metrics/traces/logs
- **Built-in testing**: Go standard testing package

### Monitoring & Metrics
- **JMX Exporter**: Kafka and ZooKeeper metrics exposure
- **Prometheus Exporters**: Infrastructure and application metrics
- **OpenTelemetry Instrumentation**: Multi-language application observability
- **Health Check Endpoints**: Service availability monitoring

### Development & Tutorial Tools
- **Streamlit**: Interactive tutorial web application
- **Shell Scripts**: Environment automation and startup
- **Docker Health Checks**: Service dependency management

## Development Setup

### Prerequisites
- Docker Engine with Docker Compose v2 support
- Git for repository management
- Modern web browser for Grafana and Streamlit access

### Local Development Environment
```bash
# Quick start
./start.sh

# Manual startup
docker compose up --build -d

# Service-specific development
docker compose up kafka zookeeper  # Core services only
docker compose up grafana prometheus loki tempo  # Monitoring stack
```

### Port Allocation
```
3000  - Grafana Dashboard
3100  - Loki (Log ingestion)
3200  - Tempo (Trace ingestion)
4317  - OTel Collector GRPC
4318  - OTel Collector HTTP
8080  - Kafka JMX Exporter
8081  - ZooKeeper JMX Exporter
8501  - Streamlit Tutorial App
8889  - OTel Collector Prometheus Metrics
9090  - Prometheus
9092  - Kafka (internal)
29092 - Kafka (external)
```

## Technical Constraints

### Language-Specific Limitations

#### Java
- **Auto-instrumentation dependency**: Relies on OpenTelemetry Java agent for zero-code instrumentation
- **JVM overhead**: Additional memory usage from OTel agent and instrumentation
- **Build complexity**: Maven shade plugin required for fat JAR creation

#### Python
- **Manual instrumentation**: Requires explicit OTel SDK integration in application code
- **Dependency management**: Complex dependency tree with OTel exporters
- **Performance impact**: Python GIL limitations with high-throughput scenarios

#### Go
- **CGO dependency**: confluent-kafka-go requires CGO for librdkafka
- **Manual instrumentation**: No auto-instrumentation available, requires explicit SDK usage
- **Module complexity**: Complex dependency resolution for OTel packages

### Infrastructure Constraints
- **Single-broker setup**: Simplified Kafka cluster not suitable for production patterns
- **Local development only**: No production deployment configurations
- **Resource intensive**: Full stack requires significant local compute resources
- **Persistence**: Data persists in Docker volumes but not across complete teardowns

## Dependencies

### External Dependencies
```yaml
Kafka Dependencies:
  - confluentinc/cp-kafka:latest
  - confluentinc/cp-zookeeper:latest

Observability Stack:
  - grafana/grafana:latest
  - prom/prometheus:latest
  - grafana/loki:latest
  - grafana/tempo:latest
  - otel/opentelemetry-collector-contrib:latest
  - bitnami/jmx-exporter:latest

Application Base Images:
  - openjdk:11-jre-slim (Java apps)
  - python:3.11-slim (Python apps)
  - golang:1.21-alpine (Go apps build)
  - alpine:latest (Go apps runtime)
  - python:3.11-slim (Streamlit app)
```

### Key Version Dependencies
- **OpenTelemetry**: 1.32.0 across all language SDKs
- **Kafka Clients**: 3.6.1 for Java, latest compatible versions for Python/Go
- **Docker Compose**: v2 syntax required for health check dependencies

## Tool Usage Patterns

### OpenTelemetry Configuration
- **Centralized collection**: All telemetry flows through OTel Collector
- **OTLP export**: Applications use OTLP gRPC for efficient data transmission
- **Resource attribution**: Consistent service identification across all components
- **Batch processing**: Optimized for throughput with batch exporters

### Monitoring Data Flow
```
Applications → OTel Collector → Storage Backends → Grafana
     ↓              ↓                ↓             ↓
  OTLP gRPC    Processing &     Prometheus      Visualization
  Logs/Traces    Routing        Loki/Tempo       & Alerting
  Metrics
```

### Development Workflow
1. **Environment Start**: `./start.sh` launches complete stack
2. **Application Development**: Modify applications with live reload
3. **Monitoring Validation**: Verify metrics/traces in Grafana
4. **Testing**: Run language-specific test suites
5. **Cleanup**: `docker compose down` for environment teardown 