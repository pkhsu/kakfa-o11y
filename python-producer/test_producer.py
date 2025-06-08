import pytest
from unittest.mock import patch, MagicMock
import os

import producer as python_producer

@pytest.fixture(autouse=True)
def setup_env_vars(monkeypatch):
    monkeypatch.setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "test-endpoint:4317")
    monkeypatch.setenv("KAFKA_BOOTSTRAP_SERVERS", "test-kafka:9092")
    monkeypatch.setenv("OTEL_SERVICE_NAME", "test-python-producer")

def test_setup_opentelemetry(mocker):
    mock_resource = mocker.patch('producer.Resource')
    mock_tracer_provider = mocker.patch('producer.TracerProvider')
    mock_otlp_span_exporter = mocker.patch('producer.OTLPSpanExporter')
    mock_batch_span_processor = mocker.patch('producer.BatchSpanProcessor')
    mock_trace_set_tracer_provider = mocker.patch('producer.trace.set_tracer_provider')
    mock_meter_provider = mocker.patch('producer.MeterProvider')
    mock_otlp_metric_exporter = mocker.patch('producer.OTLPMetricExporter')
    mock_periodic_exporting_metric_reader = mocker.patch('producer.PeriodicExportingMetricReader')
    mock_metrics_set_meter_provider = mocker.patch('producer.metrics.set_meter_provider')
    mock_kafka_instrumentor = mocker.patch('producer.KafkaInstrumentor')
    mock_logging_instrumentor = mocker.patch('producer.LoggingInstrumentor')

    python_producer.setup_opentelemetry()

    mock_resource.assert_called_once()
    mock_tracer_provider.assert_called_once()
    mock_otlp_span_exporter.assert_called_once_with(endpoint="test-endpoint:4317", insecure=True)
    mock_batch_span_processor.assert_called_once()
    mock_trace_set_tracer_provider.assert_called_once()
    mock_meter_provider.assert_called_once()
    mock_otlp_metric_exporter.assert_called_once_with(endpoint="test-endpoint:4317", insecure=True)
    mock_periodic_exporting_metric_reader.assert_called_once()
    mock_metrics_set_meter_provider.assert_called_once()
    mock_kafka_instrumentor.return_value.instrument.assert_called_once()
    mock_logging_instrumentor.return_value.instrument.assert_called_once()

def test_create_producer_success(mocker):
    mock_kafka_producer = mocker.patch('producer.KafkaProducer')
    p = python_producer.create_producer()
    mock_kafka_producer.assert_called_once_with(
        bootstrap_servers=["test-kafka:9092"],
        client_id="test-python-producer",
        acks='all',
        retries=3
    )
    assert p == mock_kafka_producer.return_value

def test_create_producer_failure(mocker):
    mocker.patch('producer.KafkaProducer', side_effect=Exception("Connection error"))
    mock_time_sleep = mocker.patch('time.sleep')
    with pytest.raises(Exception, match="Connection error"):
        python_producer.create_producer()
    mock_time_sleep.assert_called_once_with(10)
