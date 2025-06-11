package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
	"go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc"
	"go.opentelemetry.io/otel/exporters/otlp/otlplog/otlploggrpc"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/metric"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	sdklog "go.opentelemetry.io/otel/sdk/log"
	semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/trace"
	otelmetric "go.opentelemetry.io/otel/metric"
	otellog "go.opentelemetry.io/otel/log"
)

var (
	otlpEndpoint          = getEnv("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4317")
	serviceName           = getEnv("OTEL_SERVICE_NAME", "go-kafka-producer")
	kafkaBootstrapServers = getEnv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
	topic                 = "tutorial-topic"
	tracer                trace.Tracer
	meter                 otelmetric.Meter
	logger                otellog.Logger
	messagesSentCounter   otelmetric.Int64Counter
)

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

func initOtel(ctx context.Context) (func(context.Context) error, func(context.Context) error, func(context.Context) error, error) {
	res, err := resource.New(ctx,
		resource.WithAttributes(semconv.ServiceNameKey.String(serviceName)),
		resource.WithSchemaURL(semconv.SchemaURL),
	)
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to create resource: %w", err)
	}

	// Trace exporter
	traceExporter, err := otlptracegrpc.New(ctx, otlptracegrpc.WithInsecure(), otlptracegrpc.WithEndpoint(otlpEndpoint))
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to create OTLP trace exporter: %w", err)
	}
	bsp := sdktrace.NewBatchSpanProcessor(traceExporter)
	tracerProvider := sdktrace.NewTracerProvider(
		sdktrace.WithSampler(sdktrace.AlwaysSample()),
		sdktrace.WithResource(res),
		sdktrace.WithSpanProcessor(bsp),
	)
	otel.SetTracerProvider(tracerProvider)
	otel.SetTextMapPropagator(propagation.NewCompositeTextMapPropagator(propagation.TraceContext{}, propagation.Baggage{}))
	tracer = tracerProvider.Tracer("github.com/example/go-producer")

	// Metric exporter
	metricExporter, err := otlpmetricgrpc.New(ctx, otlpmetricgrpc.WithInsecure(), otlpmetricgrpc.WithEndpoint(otlpEndpoint))
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to create OTLP metric exporter: %w", err)
	}
	meterProvider := metric.NewMeterProvider(
		metric.WithResource(res),
		metric.WithReader(metric.NewPeriodicReader(metricExporter, metric.WithInterval(5*time.Second))),
	)
	otel.SetMeterProvider(meterProvider)
	meter = meterProvider.Meter("github.com/example/go-producer")

	// Log exporter
	logExporter, err := otlploggrpc.New(ctx, otlploggrpc.WithInsecure(), otlploggrpc.WithEndpoint(otlpEndpoint))
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to create OTLP log exporter: %w", err)
	}
	loggerProvider := sdklog.NewLoggerProvider(
		sdklog.WithResource(res),
		sdklog.WithProcessor(sdklog.NewBatchProcessor(logExporter)),
	)
	// Note: OpenTelemetry Go doesn't have global logger provider like traces/metrics
	// We'll use the loggerProvider directly
	logger = loggerProvider.Logger("github.com/example/go-producer")

	messagesSentCounter, err = meter.Int64Counter(
		"go.producer.messages_sent",
		otelmetric.WithDescription("Counts the number of messages sent by the Go producer"),
		otelmetric.WithUnit("1"),
	)
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to create messagesSentCounter: %w", err)
	}

	log.Printf("OpenTelemetry initialized for service: %s, exporting to %s\n", serviceName, otlpEndpoint)
	return tracerProvider.Shutdown, meterProvider.Shutdown, loggerProvider.Shutdown, nil
}

func healthCheck() error {
	// Simple health check - test Kafka connectivity
	p, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": kafkaBootstrapServers,
	})
	if err != nil {
		return fmt.Errorf("failed to create Kafka producer: %w", err)
	}
	defer p.Close()

	// Test basic connection by getting cluster metadata
	metadata, err := p.GetMetadata(nil, false, 5000)
	if err != nil {
		return fmt.Errorf("failed to get Kafka metadata: %w", err)
	}
	
	if len(metadata.Brokers) == 0 {
		return fmt.Errorf("no Kafka brokers available")
	}
	
	return nil
}

func main() {
	// Handle health check argument
	if len(os.Args) > 1 && os.Args[1] == "--health-check" {
		err := healthCheck()
		if err != nil {
			log.Printf("Health check failed: %v", err)
			os.Exit(1)
		}
		log.Println("Health check passed")
		os.Exit(0)
	}

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	tracerShutdown, meterShutdown, loggerShutdown, err := initOtel(ctx)
	if err != nil {
		log.Fatalf("Failed to initialize OpenTelemetry: %v", err)
	}
	defer func() {
		if err := tracerShutdown(context.Background()); err != nil {
			log.Printf("Error shutting down tracer provider: %v", err)
		}
		if err := meterShutdown(context.Background()); err != nil {
			log.Printf("Error shutting down meter provider: %v", err)
		}
		if err := loggerShutdown(context.Background()); err != nil {
			log.Printf("Error shutting down logger provider: %v", err)
		}
	}()

	// Kafka Producer Setup
	p, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": kafkaBootstrapServers,
	})
	if err != nil {
		log.Fatalf("Failed to create Kafka producer: %v", err)
	}
	defer p.Close()

	log.Printf("Go Kafka producer started. Sending messages to topic %s...\n", topic)

	for i := 0; ; i++ {
		// Create span for message sending
		spanCtx, span := tracer.Start(ctx, "kafka_message_send")
		
		message := fmt.Sprintf("Hello from Go Producer! Message #%d", i)
		
		err := p.Produce(&kafka.Message{
			TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
			Value:          []byte(message),
		}, nil)

		if err != nil {
			// Standard log for container logs
			log.Printf("[ERROR] [go-producer] Failed to produce message to topic=%s: %v", topic, err)
			// OpenTelemetry structured log
			var record otellog.Record
			record.SetTimestamp(time.Now())
			record.SetObservedTimestamp(time.Now())
			record.SetSeverity(otellog.SeverityError)
			record.SetSeverityText("ERROR")
			record.SetBody(otellog.StringValue(fmt.Sprintf("Failed to produce message to topic=%s: %v", topic, err)))
			record.AddAttributes(
				otellog.String("service.name", "go-producer"),
				otellog.String("kafka.topic", topic),
				otellog.String("operation", "kafka_produce"),
				otellog.String("status", "error"),
				otellog.String("error", err.Error()),
				otellog.String("component", "kafka"),
				otellog.String("language", "go"),
			)
			logger.Emit(spanCtx, record)
			messagesSentCounter.Add(spanCtx, 1, otelmetric.WithAttributes(attribute.String("status", "error")))
			span.SetAttributes(attribute.String("error", err.Error()))
		} else {
			// Standard log for container logs
			log.Printf("[INFO] [go-producer] Message sent successfully to topic=%s: %s", topic, message)
			// OpenTelemetry structured log
			var record otellog.Record
			record.SetTimestamp(time.Now())
			record.SetObservedTimestamp(time.Now())
			record.SetSeverity(otellog.SeverityInfo)
			record.SetSeverityText("INFO")
			record.SetBody(otellog.StringValue(fmt.Sprintf("Message sent successfully to topic=%s: %s", topic, message)))
			record.AddAttributes(
				otellog.String("service.name", "go-producer"),
				otellog.String("kafka.topic", topic),
				otellog.String("message.content", message),
				otellog.String("operation", "kafka_produce"),
				otellog.String("status", "success"),
				otellog.String("component", "kafka"),
				otellog.String("language", "go"),
			)
			logger.Emit(spanCtx, record)
			messagesSentCounter.Add(spanCtx, 1, otelmetric.WithAttributes(attribute.String("status", "success")))
			span.SetAttributes(
				attribute.String("kafka.topic", topic),
				attribute.String("message.content", message),
				attribute.String("producer.language", "go"),
			)
		}
		
		span.End()
		p.Flush(1000)
		time.Sleep(5 * time.Second)
	}
}
