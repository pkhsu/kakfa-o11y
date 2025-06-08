# Kafka Observability (O11y) Tutorial with Multi-Language Examples

This project provides a hands-on tutorial for understanding and implementing observability in Apache Kafka based systems. It features producers and consumers in Java, Python, and Go, all integrated with OpenTelemetry for collecting metrics, logs, and traces. The collected telemetry data is visualized using a Grafana stack (Prometheus, Loki, Tempo).

## Features

*   **Apache Kafka**: Core messaging system.
*   **Multi-Language Examples**:
    *   Java Producer & Consumer
    *   Python Producer & Consumer
    *   Go Producer & Consumer
*   **OpenTelemetry Integration**:
    *   Metrics: Collected from applications and Kafka clients.
    *   Logs: Enriched with trace context and sent to Loki.
    *   Traces: Distributed tracing across producers and consumers.
*   **Grafana Stack**:
    *   **Grafana**: For visualization and dashboards.
    *   **Prometheus**: For metrics storage and querying.
    *   **Loki**: For log aggregation and querying.
    *   **Tempo**: For distributed trace storage and visualization.
*   **OpenTelemetry Collector**: Centralized agent for collecting and processing telemetry data.
*   **Docker Compose**: Entire environment orchestrated with Docker Compose for easy setup.
*   **Streamlit Tutorial App**: A web-based guide to navigate the tutorial (content currently minimal).
*   **`start.sh` script**: For easy environment startup.
*   **Pre-configured Grafana Dashboard**: An overview dashboard (`Kafka O11y Tutorial Overview`) is automatically provisioned in Grafana.

## Project Structure

```
.
|-- docker-compose.yml         # Main Docker Compose configuration
|-- grafana/                   # Grafana configs and datasources
|-- loki/                      # Loki config
|-- prometheus/                # Prometheus config
|-- tempo/                     # Tempo config
|-- otel-collector-config.yaml # OpenTelemetry Collector config
|-- java-producer/             # Java Kafka Producer app & Dockerfile
|-- java-consumer/             # Java Kafka Consumer app & Dockerfile
|-- python-producer/           # Python Kafka Producer app & Dockerfile
|-- python-consumer/           # Python Kafka Consumer app & Dockerfile
|-- go-producer/               # Go Kafka Producer app & Dockerfile
|-- go-consumer/               # Go Kafka Consumer app & Dockerfile
|-- streamlit-app/             # Streamlit tutorial application & Dockerfile
|-- start.sh                   # Script to start/stop the environment
`-- README.md                  # This file
```

## Prerequisites

*   **Docker**: Ensure Docker engine is installed and running.
*   **Docker Compose (v2 syntax)**: Ensure you have `docker compose` command available (usually included with Docker Desktop or as a plugin for Docker Engine).

## Getting Started

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd kafka-o11y-tutorial
    ```
    *(Replace `<repository_url>` with the actual URL of this project)*

2.  **Start the Environment**:
    Run the `start.sh` script from the project root:
    ```bash
    ./start.sh
    ```
    This script will:
    *   Check for Docker and Docker Compose.
    *   Build the Docker images for the applications (if not already built or if Dockerfiles changed).
    *   Start all services in detached mode (`docker compose up --build -d`).
    *   Provide you with URLs for accessing the Streamlit tutorial and Grafana.

    The first time you run this, it might take a few minutes to download base Docker images and build the application images.

## Using the Tutorial

Once the environment is running:

1.  **Access the Streamlit Tutorial App**:
    *   Open your web browser and go to: `http://localhost:8501`
    *   *(Note: The content of the Streamlit app is currently minimal and will be expanded in future updates. This README provides more comprehensive guidance for now.)*

2.  **Observe Producer & Consumer Logs**:
    The producer applications (Java, Python, Go) will automatically start sending messages to a Kafka topic named `tutorial-topic`. The corresponding consumer applications will listen to this topic. You can view their logs to see this in action:
    *   To view logs for all services: `docker compose logs -f`
    *   To view logs for a specific service (e.g., `java-producer`):
        ```bash
        docker compose logs -f java-producer
        docker compose logs -f java-consumer
        docker compose logs -f python-producer
        # ...and so on for other services
        ```
    *   Look for log messages indicating messages being sent and received, and potentially OpenTelemetry context information.

3.  **Explore Telemetry Data in Grafana**:
    *   Access Grafana: `http://localhost:3000`
    *   Default credentials: `admin` / `admin` (you may be prompted to change the password on first login).

    **0. Check the Pre-configured 'Kafka O11y Tutorial Overview' Dashboard**:
    *   In Grafana's left sidebar, navigate to "Dashboards".
    *   Look for and open the dashboard titled "Kafka O11y Tutorial Overview".
    *   This dashboard provides a quick glance at message rates for producers/consumers and other relevant metrics from the system.

    **b. Metrics (Prometheus Data Source)**:
    *   In Grafana, go to "Explore" or create/edit a Dashboard panel.
    *   Select the "Prometheus" data source.
    *   Example PromQL queries:
        *   `rate(otelcol_process_uptime[5m])` (OTel Collector's own uptime)
        *   `rate(python_producer_messages_sent_total[1m])` (Custom metric from Python producer)
        *   `rate(go_producer_messages_sent_total[1m])` (Custom metric from Go producer)
        *   `jvm_memory_used_bytes{area="heap", service_name="java-kafka-producer"}` (JVM metrics from Java apps via OTel agent)
        *   Explore other metrics related to Kafka clients (e.g., `kafka_producer_`, `kafka_consumer_`) which might be available depending on the instrumentation level.

    **c. Logs (Loki Data Source)**:
    *   In Grafana, go to "Explore".
    *   Select the "Loki" data source.
    *   Example LogQL queries:
        *   To see logs for a specific application: `{service_name="java-kafka-producer"}`
        *   To see logs from the OTel Collector: `{job="otel-collector"}` or `{instance=~"otel-collector.*"}` (actual labels might vary slightly based on collector config)
        *   Filter by trace ID: `{service_name="python-kafka-consumer"} | json | line_format "{{.message}}" | trace_id="<some_trace_id>"` (assuming logs are JSON formatted and contain trace_id)
    *   You should find logs enriched with `service_name`, `trace_id`, `span_id`, etc.

    **d. Traces (Tempo Data Source)**:
    *   In Grafana, go to "Explore".
    *   Select the "Tempo" data source.
    *   You can search for traces using a Trace ID (if you have one from a log).
    *   Alternatively, use the "Search" tab in the Tempo query editor:
        *   **Service Name**: e.g., `java-kafka-producer`, `python-kafka-consumer`, `go-producer`.
        *   **Span Name**: e.g., `send_java_kafka_message`, `tutorial-topic process` (from Kafka instrumentation), `send_python_kafka_message`.
    *   Select a trace to view its flame graph and span details. You should be able to see the end-to-end flow of messages, from the producer, through Kafka, to the consumer, even across different programming languages.

## Stopping the Environment

*   To stop all running services:
    ```bash
    docker compose down
    ```
*   This will stop and remove the containers. Data stored in Docker volumes (Grafana dashboards, Prometheus metrics, etc.) will persist unless the volumes are manually removed.

## Further Development & Refinements

*   **Populate Streamlit App Content Files**: The Streamlit application (`streamlit-app/app.py`) is structured to load content from markdown files in the `streamlit-app/content/` directory. These files currently contain placeholders and need to be populated with detailed tutorial text.
*   **Go Application Tracer/Meter Naming**: The tracer/meter names in the Go applications (`go-producer/main.go`, `go-consumer/main.go`) use a placeholder module path (`github.com/example/...`). This should be updated to the actual module path for better consistency if the project is forked or formally structured.
*   **Advanced Kafka Observability**: Explore adding JMX Exporter for deeper Kafka broker metrics if not already covered by OpenTelemetry's Kafka metrics.
*   **More Custom Grafana Dashboards**: While an overview dashboard is now provided, additional, more detailed dashboards could be created for specific components or use cases.

## Contributing

Contributions are welcome! Please feel free to fork the repository, make improvements, and submit pull requests.
