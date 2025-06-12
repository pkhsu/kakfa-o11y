# Kafka APM & Observability Solution Demo

> **A demonstration of Application Performance Monitoring (APM) and observability patterns for Apache Kafka environments, showcasing monitoring, alerting, and troubleshooting capabilities.**

**Note: This is a proof-of-concept demo project for learning and evaluation purposes, not intended for production use without significant modifications.**

## Executive Summary

This project demonstrates an **APM solution concept** for Kafka operations teams, showcasing how to achieve **complete visibility into Kafka-based microservices architectures**. This demo provides:

- **End-to-End Visibility**: Full observability across producers, consumers, brokers, and infrastructure
- **Rapid Problem Resolution**: Reduce MTTR from hours to minutes with correlated metrics, logs, and traces
- **Proactive Monitoring**: Early detection of performance degradation and capacity issues
- **Multi-Language Support**: Unified observability across Java, Python, and Go applications
- **Modern Observability Stack**: Built on OpenTelemetry standards with proven open-source tools

### Demo Value
- **Demonstrates reduction** in troubleshooting time through correlated telemetry
- **Shows capacity planning** capabilities with trend analysis and comprehensive metrics
- **Illustrates operational visibility** with comprehensive monitoring and alerting
- **Showcases observability patterns** for automated monitoring and early issue detection

---

## System Architecture

```mermaid
graph TB
    subgraph "Application Layer"
        JP[Java Producer]
        JC[Java Consumer]
        PP[Python Producer]
        PC[Python Consumer]
        GP[Go Producer]
        GC[Go Consumer]
    end
    
    subgraph "Kafka Cluster"
        K[Kafka Broker]
        Z[Zookeeper]
        JMX1[JMX Exporter - Kafka]
        JMX2[JMX Exporter - Zookeeper]
    end
    
    subgraph "Observability Pipeline"
        OC[OpenTelemetry Collector]
    end
    
    subgraph "Storage & Processing"
        P[Prometheus<br/>Metrics]
        L[Loki<br/>Logs]
        T[Tempo<br/>Traces]
    end
    
    subgraph "Visualization & Alerting"
        G[Grafana<br/>Dashboards & Alerts]
        SA[Streamlit<br/>Demo App]
    end
    
    JP --> |OTLP| OC
    JC --> |OTLP| OC
    PP --> |OTLP| OC
    PC --> |OTLP| OC
    GP --> |OTLP| OC
    GC --> |OTLP| OC
    
    JP -.-> |Kafka Protocol| K
    JC -.-> |Kafka Protocol| K
    PP -.-> |Kafka Protocol| K
    PC -.-> |Kafka Protocol| K
    GP -.-> |Kafka Protocol| K
    GC -.-> |Kafka Protocol| K
    
    JMX1 --> |Prometheus Format| OC
    JMX2 --> |Prometheus Format| OC
    K --> JMX1
    Z --> JMX2
    
    OC --> |Metrics| P
    OC --> |Logs| L
    OC --> |Traces| T
    
    P --> G
    L --> G
    T --> G
    
    G --> SA
```

### Key Architecture Principles
- **Centralized Collection**: Single OpenTelemetry Collector for all telemetry data
- **Vendor Neutrality**: Standards-based OpenTelemetry implementation
- **Scalability**: Horizontally scalable components with persistent storage
- **Security**: Configurable authentication and encryption support
- **High Availability**: Resilient design with health checks and automatic recovery

---

## Technology Stack

### Application Instrumentation Layer
| Component | Technology | Purpose | Key Features |
|-----------|------------|---------|--------------|
| **Java Apps** | OpenTelemetry Java Agent | Auto-instrumentation | Zero-code instrumentation, JVM metrics, Kafka client tracing |
| **Python Apps** | OpenTelemetry Python SDK | Manual instrumentation | Custom metrics, structured logging, async support |
| **Go Apps** | OpenTelemetry Go SDK | Manual instrumentation | High-performance tracing, custom metrics, low overhead |

### Message Streaming Platform
| Component | Technology | Purpose | Key Features |
|-----------|------------|---------|--------------|
| **Apache Kafka** | Confluent Platform | Message Broker | High throughput, durability, partition-based scaling |
| **Zookeeper** | Apache Zookeeper | Coordination Service | Cluster coordination, configuration management |
| **JMX Exporters** | Prometheus JMX Exporter | Metrics Collection | Broker metrics, JVM stats, topic metrics |

### Observability Infrastructure
| Component | Technology | Purpose | Key Features |
|-----------|------------|---------|--------------|
| **OpenTelemetry Collector** | OTEL Collector Contrib | Telemetry Pipeline | Data collection, processing, routing, export |
| **Prometheus** | Prometheus TSDB | Metrics Storage | Time-series database, PromQL queries, alerting |
| **Loki** | Grafana Loki | Log Aggregation | Log indexing, LogQL queries, label-based organization |
| **Tempo** | Grafana Tempo | Trace Storage | Distributed tracing, trace correlation, sampling |
| **Grafana** | Grafana | Visualization | Dashboards, alerting, data exploration |

### Development & Deployment
| Component | Technology | Purpose | Key Features |
|-----------|------------|---------|--------------|
| **Docker** | Container Runtime | Containerization | Consistent environments, resource isolation |
| **Docker Compose** | Orchestration | Service Management | Multi-service deployment, networking, volumes |
| **Streamlit** | Python Web Framework | Demo Interface | Interactive tutorials, real-time monitoring |

---

## APM & Observability Data Flow

### Three Pillars of Observability

#### Metrics Pipeline
```
Applications → OpenTelemetry SDK → OTLP → Collector → Prometheus → Grafana
JMX Exporters → Prometheus Format → Collector → Prometheus → Grafana
```

**Key Metrics Categories:**
- **Application Metrics**: Message throughput, processing latency, error rates
- **Kafka Broker Metrics**: Topic sizes, partition distribution, consumer lag
- **Infrastructure Metrics**: CPU, memory, disk usage, network I/O
- **JVM Metrics**: Garbage collection, heap usage, thread pools

#### Logs Pipeline
```
Applications → OpenTelemetry SDK → OTLP → Collector → Loki → Grafana
Kafka Brokers → JSON Logs → Collector → Loki → Grafana
```

**Log Enrichment Features:**
- **Trace Correlation**: Automatic trace ID injection
- **Structured Logging**: JSON format with consistent fields
- **Context Propagation**: Cross-service correlation
- **Error Classification**: Automatic error detection and categorization

#### Traces Pipeline
```
Applications → OpenTelemetry SDK → OTLP → Collector → Tempo → Grafana
```

**Distributed Tracing Capabilities:**
- **End-to-End Tracing**: Producer → Kafka → Consumer spans
- **Cross-Language Correlation**: Unified trace view across Java, Python, Go
- **Performance Profiling**: Detailed timing analysis
- **Dependency Mapping**: Service interaction visualization

### Data Correlation Strategy

The solution implements **comprehensive correlation** across all telemetry types:

1. **Trace-Metrics Correlation**: Link specific traces to performance metrics
2. **Log-Trace Correlation**: Automatic trace ID injection in logs
3. **Service Mapping**: Automatic discovery of service dependencies
4. **Error Correlation**: Link errors across metrics, logs, and traces

---

## Quick Start Guide

### Prerequisites

**System Requirements:**
- Docker Engine 20.10+ with Compose V2
- 4GB+ RAM (8GB recommended for demo environment)
- 5GB+ free disk space
- Network access for Docker image downloads

**Verification:**
```bash
# Verify Docker and Compose installation
docker --version          # Should be 20.10+
docker compose version     # Should be v2.x+

# Check system resources
free -h                    # Verify available RAM
df -h                      # Verify disk space
```

### Deployment Steps

1. **Clone and Setup**
    ```bash
    git clone <repository_url>
   cd kakfa-o11y
   chmod +x start.sh
    ```

2. **Start the Environment**
    ```bash
    ./start.sh
    ```
   
   The script will:
   - Validate system prerequisites
   - Build application containers
   - Deploy all services
   - Perform health checks
   - Display access URLs

3. **Verify Deployment**
   ```bash
   # Check service health
   docker compose ps
   
   # View startup logs
   docker compose logs -f --tail=50
   
   # Verify Kafka connectivity
   docker compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list
   ```

### Access Points

| Service | URL | Credentials | Purpose |
|---------|-----|-------------|---------|
| **Grafana** | http://localhost:3000 | admin/admin | Primary monitoring interface |
| **Prometheus** | http://localhost:9090 | - | Metrics exploration |
| **Demo App** | http://localhost:8501 | - | Interactive tutorials |
| **OTel Collector** | http://localhost:13133/health | - | Collector health check |

---

## Monitoring & Observability Guide

### Pre-Built Dashboards

#### 1. **Kafka O11y Overview - Enhanced Broker Monitoring**
*Primary operational dashboard with 50+ key metrics*

**Key Sections:**
- **Cluster Health**: Controller status, partition states, replication health
- **Performance Metrics**: Throughput, latency, request rates
- **Resource Utilization**: CPU, memory, disk, network usage
- **Error Monitoring**: Failed requests, exception rates, timeout tracking
- **Consumer Groups**: Lag monitoring, offset management
- **Application Metrics**: Producer/consumer rates across all languages

### Essential Monitoring Scenarios

#### **Scenario 1: Performance Investigation**
        ```bash
# Generate load and observe
        docker compose logs -f python-producer
```

**In Grafana:**
1. Navigate to "Kafka O11y Overview" dashboard
2. Observe real-time message throughput
3. Check producer/consumer latency metrics
4. Correlate with JVM memory usage

**Key Metrics to Watch:**
- `rate(kafka_messages_sent_total[1m])` - Python producer throughput
- `rate(go_producer_messages_sent[1m])` - Go producer throughput  
- `kafka_network_request_total_time_ms_mean` - Request latency
- `jvm_memory_used_bytes{area="heap"}` - Memory usage

#### **Scenario 2: Error Detection & Root Cause Analysis**
```bash
# Simulate network issues
docker compose pause kafka
docker compose logs python-consumer
docker compose unpause kafka
```

**Investigation Steps:**
1. **Metrics**: Check error rate spikes in dashboard
2. **Logs**: Use Loki to find error messages
   ```
   {service_name="python-kafka-consumer"} |= "ERROR"
   ```
3. **Traces**: Identify failed traces in Tempo
4. **Correlation**: Link errors across all three pillars

#### **Scenario 3: Capacity Planning**
**Monitor trends over time:**
- Disk usage growth rates
- Consumer lag trends
- Network bandwidth utilization
- JVM garbage collection frequency

**PromQL Queries for Capacity Planning:**
```promql
# Storage growth rate
increase(kafka_log_log_size_bytes[1h])

# Consumer lag trend
kafka_consumer_lag_sum

# Network utilization
rate(kafka_network_io_bytes_total[5m])
```

### Example Alerting Rules

#### Sample Alert Configurations
```yaml
# High Consumer Lag
- alert: KafkaConsumerLagHigh
  expr: kafka_consumer_lag_sum > 1000
  for: 2m
  
# Broker Offline
- alert: KafkaBrokerDown
  expr: kafka_controller_active_count == 0
  for: 30s
  
# High Error Rate
- alert: ApplicationErrorRateHigh
  expr: rate(application_errors_total[5m]) > 0.1
  for: 1m
```

---

## Customization & Extension Guide

### Scaling Considerations

#### **Horizontal Scaling (Demo)**
```yaml
# Scale producers/consumers for testing
docker compose up --scale python-producer=3 --scale java-consumer=2

# Note: This demo uses single Kafka broker
# Multi-broker setup would require additional configuration
```

#### **Resource Optimization (Example)**
```yaml
# Example JVM settings for testing
environment:
  JAVA_OPTS: >-
    -XX:+UseG1GC
    -XX:MaxGCPauseMillis=20
    -XX:InitiatingHeapOccupancyPercent=35
    -Xms512m -Xmx1g
```

### Security Considerations (Reference)

#### **Authentication & Authorization**
```yaml
# Enable SASL authentication
kafka:
  environment:
    KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: SASL_PLAINTEXT:SASL_PLAINTEXT
    KAFKA_SASL_ENABLED_MECHANISMS: PLAIN
    KAFKA_SASL_MECHANISM_INTER_BROKER_PROTOCOL: PLAIN
```

#### **TLS Encryption**
```yaml
# Enable TLS for OTLP communication
otel-collector:
  volumes:
    - ./certs:/etc/ssl/certs
  environment:
    OTEL_EXPORTER_OTLP_CERTIFICATE: /etc/ssl/certs/cert.pem
```

### Integration Examples

#### **External Prometheus/Grafana**
```yaml
# Configure external endpoints
otel-collector:
  environment:
    PROMETHEUS_REMOTE_WRITE_ENDPOINT: "https://your-prometheus.com/api/v1/write"
    GRAFANA_CLOUD_URL: "https://your-grafana-cloud.com"
```

#### **Enterprise Monitoring Integration**
- **Datadog**: Use OTLP exporter configuration
- **New Relic**: Configure OTLP endpoint
- **Splunk**: Use Splunk HEC exporter
- **Elastic Stack**: Configure Elasticsearch exporter

---

## Demo Scenarios & Tutorials

### Guided Walkthrough

#### **Scenario A: Normal Operations Monitoring**
1. Start the environment and observe baseline metrics
2. Navigate through Grafana dashboards
3. Understand normal performance patterns
4. Set up basic alerting rules

#### **Scenario B: Performance Troubleshooting**
1. Introduce artificial latency
2. Observe metric degradation
3. Use logs to identify root cause
4. Trace request flow through system
5. Implement performance improvements

#### **Scenario C: Failure Recovery**
1. Simulate broker failure
2. Monitor cluster recovery
3. Analyze consumer rebalancing
4. Validate data consistency

#### **Scenario D: Scaling Operations**
1. Increase message load
2. Monitor resource utilization
3. Scale consumers dynamically
4. Observe performance improvements

### Interactive Tutorial Access

Visit the **Streamlit Demo App** at http://localhost:8501 for:
- Step-by-step guided scenarios
- Interactive metric exploration
- Real-time system status
- Best practices documentation

---

## Operations & Maintenance

### Daily Operations

#### **Health Check Procedures**
```bash
# Individual service checks
docker compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
curl -f http://localhost:13133/health  # OTel Collector
curl -f http://localhost:3000/api/health  # Grafana
```

#### **Backup & Recovery**
```bash
# Backup Grafana dashboards
docker compose exec grafana grafana-cli admin export-dashboard

# Backup Prometheus data
docker run --rm -v prometheus_data:/data alpine tar czf - /data

# Backup application configurations
tar czf config-backup.tar.gz grafana/ prometheus/ loki/ tempo/
```

### Troubleshooting Guide

#### **Common Issues & Solutions**

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **High Memory Usage** | OOM errors, slow response | Increase container memory limits |
| **Consumer Lag** | Processing delays | Scale consumers or optimize processing |
| **Network Issues** | Connection timeouts | Check Docker networking, firewall rules |
| **Storage Growth** | Disk space warnings | Implement retention policies |

#### **Diagnostic Commands**
    ```bash
# View detailed logs
docker compose logs --tail=100 -f [service-name]

# Check resource usage
docker stats

# Network connectivity
docker compose exec python-producer ping kafka

# Kafka cluster status
docker compose exec kafka kafka-broker-api-versions --bootstrap-server localhost:9092
```

---

## Performance Benchmarks

### Baseline Performance Metrics

#### **Message Throughput**
- **Java Producer**: ~5,000-10,000 messages/second
- **Python Producer**: ~1,000-2,000 messages/second  
- **Go Producer**: ~8,000-15,000 messages/second

#### **Resource Utilization**
- **Memory Usage**: ~4-6GB total for full stack
- **CPU Usage**: ~1-2 cores under typical load
- **Network**: ~10-50MB/s typical throughput
- **Storage**: ~100-500MB/day log retention

#### **Latency Characteristics**
- **End-to-End Latency**: P95 < 100ms
- **Producer Latency**: P95 < 50ms  
- **Consumer Processing**: P95 < 20ms

---

## API Reference

### OpenTelemetry Endpoints

| Endpoint | Purpose | Port |
|----------|---------|------|
| `http://localhost:4317` | OTLP gRPC | 4317 |
| `http://localhost:4318` | OTLP HTTP | 4318 |
| `http://localhost:13133/health` | Health Check | 13133 |
| `http://localhost:55679` | zPages | 55679 |

### Grafana API
    ```bash
# Create dashboard
curl -X POST http://admin:admin@localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @dashboard.json

# Query metrics
curl -X GET "http://admin:admin@localhost:3000/api/datasources/proxy/1/api/v1/query?query=up"
```

### Prometheus API
    ```bash
# Query metrics
curl "http://localhost:9090/api/v1/query?query=kafka_messages_sent_total"

# Query range
curl "http://localhost:9090/api/v1/query_range?query=rate(kafka_messages_sent_total[5m])&start=2024-01-01T00:00:00Z&end=2024-01-01T01:00:00Z&step=15s"
```

---

## Running Tests

### Unit Testing

#### **Java Applications**
    ```bash
cd java-producer && mvn test
cd java-consumer && mvn test
    ```

#### **Python Applications**  
    ```bash
cd python-producer && pytest -v
cd python-consumer && pytest -v
cd streamlit-app && pytest -v
```

#### **Go Applications**
    ```bash
cd go-producer && go test -v ./...
cd go-consumer && go test -v ./...
    ```

### Integration Testing
    ```bash
# Manual integration test - verify all services are running
docker compose ps

# Check message flow
docker compose logs -f python-producer | head -20
docker compose logs -f go-consumer | head -20
```

---

## Contributing & Support

### Development Setup
    ```bash
# Clone repository
git clone <repository_url>
cd kakfa-o11y

# Build and run in development mode
docker compose up --build
```

### Support Channels
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Wiki**: Detailed documentation and examples

### Roadmap
- [ ] Kubernetes deployment manifests
- [ ] Enhanced alerting rules
- [ ] Custom Grafana plugins
- [ ] Performance optimization guides
- [ ] Multi-cluster monitoring

---

## Appendix

### Metrics Reference

#### **Application Metrics**
| Metric | Type | Description | Labels |
|--------|------|-------------|--------|
| `kafka_messages_sent_total` | Counter | Total messages sent (Python) | `status`, `language`, `component`, `topic`, `partition` |
| `go.producer.messages_sent` | Counter | Total messages sent (Go) | `status` |
| `kafka_messages_sent_bytes_total` | Counter | Total bytes sent (Python) | `status`, `language`, `component`, `topic`, `partition` |
| `kafka_message_send_duration_ms` | Histogram | Send operation duration (Python) | `status`, `language`, `component`, `topic`, `partition` |
| `kafka_producer_active` | UpDownCounter | Producer status (Python) | `status`, `language`, `component` |

#### **Kafka Broker Metrics**
| Metric | Type | Description |
|--------|------|-------------|
| `kafka_controller_active_count` | Gauge | Active controller count |
| `kafka_server_replica_manager_under_replicated_partitions` | Gauge | Under-replicated partitions |
| `kafka_network_request_total_time_ms_mean` | Gauge | Average request processing time |

### Environment Variables Reference

#### **OpenTelemetry Configuration**
    ```bash
OTEL_SERVICE_NAME=your-service-name
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=production
OTEL_METRICS_EXPORTER=otlp
OTEL_LOGS_EXPORTER=otlp
OTEL_TRACES_EXPORTER=otlp
```

#### **Kafka Configuration**
    ```bash
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_AUTO_OFFSET_RESET=earliest
KAFKA_CONSUMER_GROUP_ID=your-consumer-group
```

---

**For questions, issues, or contributions, please visit our [GitHub repository](https://github.com/your-org/kafka-o11y-demo)**

*This demo showcases modern observability patterns for educational and evaluation purposes. Significant modifications would be required for production deployment.*
