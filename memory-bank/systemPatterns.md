# System Patterns

## System Architecture

### Overall Design
The system follows a microservices observability pattern with centralized telemetry collection. It demonstrates event-driven architecture monitoring across multiple programming languages with unified observability standards.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Producers     │    │     Kafka       │    │   Consumers     │
│                 │    │   Cluster       │    │                 │
│ ┌─────────────┐ │    │                 │    │ ┌─────────────┐ │
│ │Java Producer│ │    │ ┌─────────────┐ │    │ │Java Consumer│ │
│ └─────────────┘ │───▶│ │   Broker    │ │───▶│ └─────────────┘ │
│ ┌─────────────┐ │    │ │             │ │    │ ┌─────────────┐ │
│ │Python Prod. │ │    │ │ ZooKeeper   │ │    │ │Python Cons. │ │
│ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
│ ┌─────────────┐ │    │                 │    │ ┌─────────────┐ │
│ │Go Producer  │ │    │                 │    │ │Go Consumer  │ │
│ └─────────────┘ │    │                 │    │ └─────────────┘ │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                        │                        │
          │                        │                        │
          └────────────────────────▼────────────────────────┘
                               ┌─────────────────┐
                               │ OTel Collector  │
                               │                 │
                               │ ┌─────────────┐ │
                               │ │   Metrics   │ │
                               │ │   Logs      │ │
                               │ │   Traces    │ │
                               │ └─────────────┘ │
                               └─────────────────┘
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌─────────────────┐            ┌─────────────────┐            ┌─────────────────┐
│   Prometheus    │            │      Loki       │            │     Tempo       │
│   (Metrics)     │            │     (Logs)      │            │   (Traces)      │
└─────────────────┘            └─────────────────┘            └─────────────────┘
        │                               │                               │
        └───────────────────────────────┼───────────────────────────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │    Grafana      │
                               │  (Dashboards)   │
                               └─────────────────┘
```

## Key Technical Decisions

### 1. OpenTelemetry-First Approach
**Decision**: Use OpenTelemetry as the primary instrumentation standard across all languages
**Rationale**: Vendor-neutral, standardized approach that works consistently across Java, Python, and Go
**Implementation**: Each application uses language-specific OTel SDKs with OTLP export to central collector

### 2. Centralized Telemetry Collection
**Decision**: Single OpenTelemetry Collector handles all telemetry processing
**Rationale**: Simplifies configuration, enables consistent processing, and provides single point for telemetry routing
**Implementation**: Collector receives OTLP data and routes to appropriate backends (Prometheus, Loki, Tempo)

### 3. JMX-Based Kafka Monitoring
**Decision**: Use dedicated JMX exporters for Kafka and ZooKeeper metrics
**Rationale**: Provides comprehensive broker-level metrics not available through client instrumentation
**Implementation**: Separate containers running JMX exporters with detailed metric configurations

### 4. Language-Specific Instrumentation Patterns
**Decision**: Demonstrate different OTel integration approaches per language
- **Java**: Auto-instrumentation via Java agent
- **Python**: Manual SDK instrumentation with enhanced control
- **Go**: Manual SDK instrumentation with comprehensive metric creation
**Rationale**: Shows real-world patterns teams would use in each language ecosystem

## Design Patterns

### 1. Unified Metric Naming
Pattern for consistent metric naming across languages:
```
kafka_messages_sent_total{language="python", status="success"}
kafka_messages_received_total{language="go", status="error"}
```

### 2. Trace Correlation
Consistent span naming and attribute patterns:
```
Span: "kafka_message_send"
Attributes:
  - messaging.system: "kafka"
  - messaging.destination: "tutorial-topic"
  - messaging.operation: "send"
  - language: "python"
  - component.type: "producer"
```

### 3. Resource Attribution
Standardized resource attributes for service identification:
```
Resource Attributes:
  - service.name: "java-kafka-producer"
  - service.version: "1.0.0"
  - service.namespace: "kafka-tutorial"
  - deployment.environment: "tutorial"
  - component.type: "producer"
  - language: "java"
```

## Component Relationships

### Data Flow Architecture
1. **Applications** → **OTel Collector** (OTLP gRPC/HTTP)
2. **JMX Exporters** → **OTel Collector** (Prometheus scraping)
3. **OTel Collector** → **Backends** (Prometheus, Loki, Tempo)
4. **Grafana** → **Backends** (Query and visualization)

### Service Dependencies
- **Kafka** depends on **ZooKeeper**
- **Applications** depend on **Kafka** (health checks)
- **OTel Collector** depends on all backends
- **JMX Exporters** depend on **Kafka/ZooKeeper**

## Critical Implementation Paths

### 1. Message Tracing Flow
Producer → Kafka → Consumer with full trace correlation:
1. Producer creates span with trace context
2. Trace context propagated in Kafka message headers
3. Consumer extracts context and continues trace
4. Full trace visible in Tempo with proper parent-child relationships

### 2. Error Handling and Monitoring
Comprehensive error tracking across all components:
- Application-level error metrics and logs
- Kafka broker error rates from JMX metrics
- Infrastructure errors from Docker stats
- Correlated error analysis in Grafana dashboards

### 3. Performance Monitoring
Multi-layered performance observation:
- Application metrics (message rates, processing times)
- Kafka broker performance (request latency, throughput)
- JVM metrics (GC, memory) for Java applications
- Infrastructure metrics (CPU, memory, network) 