import pytest
from unittest.mock import patch, MagicMock
import os

import consumer as python_consumer

@pytest.fixture(autouse=True)
def setup_env_vars(monkeypatch):
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "test-endpoint:4317")
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "test-kafka:9092")
    monkeypatch.setenv("OTEL_SERVICE_NAME", "test-python-consumer")
    monkeypatch.setenv("CONSUMER_GROUP_ID", "test-group") # Added for consumer

def test_setup_opentelemetry_consumer(mocker):
    mock_resource = mocker.patch('consumer.Resource')
    mock_tracer_provider = mocker.patch('consumer.TracerProvider')
    # Add other necessary mocks for OTel SDK components similar to producer test
    mock_otlp_span_exporter = mocker.patch('consumer.OTLPSpanExporter')
    mock_batch_span_processor = mocker.patch('consumer.BatchSpanProcessor')
    mock_trace_set_tracer_provider = mocker.patch('consumer.trace.set_tracer_provider')
    mock_meter_provider = mocker.patch('consumer.MeterProvider')
    mock_otlp_metric_exporter = mocker.patch('consumer.OTLPMetricExporter')
    mock_periodic_exporting_metric_reader = mocker.patch('consumer.PeriodicExportingMetricReader')
    mock_metrics_set_meter_provider = mocker.patch('consumer.metrics.set_meter_provider')
    mock_kafka_instrumentor = mocker.patch('consumer.KafkaInstrumentor')
    mock_logging_instrumentor = mocker.patch('consumer.LoggingInstrumentor')

    python_consumer.setup_opentelemetry()

    mock_resource.assert_called_once()
    mock_tracer_provider.assert_called_once()
    mock_otlp_span_exporter.assert_called_once()
    # ... assert other calls ...
    mock_kafka_instrumentor.return_value.instrument.assert_called_once()
    mock_logging_instrumentor.return_value.instrument.assert_called_once()

def test_create_consumer_success(mocker):
    mock_kafka_consumer = mocker.patch('consumer.KafkaConsumer')
    c = python_consumer.create_consumer()
    mock_kafka_consumer.assert_called_once_with(
        python_consumer.TOPIC_NAME,
        bootstrap_servers=["test-kafka:9092"],
        client_id="test-python-consumer",
        group_id="test-group",
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )
    assert c == mock_kafka_consumer.return_value

def test_create_consumer_failure(mocker):
    mocker.patch('consumer.KafkaConsumer', side_effect=Exception("Connection error"))
    mock_time_sleep = mocker.patch('time.sleep')
    with pytest.raises(Exception, match="Connection error"):
        python_consumer.create_consumer()
    mock_time_sleep.assert_called_once_with(10)
