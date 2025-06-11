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
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/metric"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.21.0"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/trace"
	otelmetric "go.opentelemetry.io/otel/metric"
)

var (
	otlpEndpoint          = getEnv("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4317")
	serviceName           = getEnv("OTEL_SERVICE_NAME", "go-kafka-producer")
	kafkaBootstrapServers = getEnv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
	topic                 = "tutorial-topic"
	tracer                trace.Tracer
	meter                 otelmetric.Meter
	messagesSentCounter   otelmetric.Int64Counter
)

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

func initOtel(ctx context.Context) (func(context.Context) error, func(context.Context) error, error) {
	res, err := resource.New(ctx,
		resource.WithAttributes(semconv.ServiceNameKey.String(serviceName)),
		resource.WithSchemaURL(semconv.SchemaURL),
	)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to create resource: %w", err)
	}

	// Trace exporter
	traceExporter, err := otlptracegrpc.New(ctx, otlptracegrpc.WithInsecure(), otlptracegrpc.WithEndpoint(otlpEndpoint))
	if err != nil {
		return nil, nil, fmt.Errorf("failed to create OTLP trace exporter: %w", err)
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
		return nil, nil, fmt.Errorf("failed to create OTLP metric exporter: %w", err)
	}
	meterProvider := metric.NewMeterProvider(
		metric.WithResource(res),
		metric.WithReader(metric.NewPeriodicReader(metricExporter, metric.WithInterval(5*time.Second))),
	)
	otel.SetMeterProvider(meterProvider)
	meter = meterProvider.Meter("github.com/example/go-producer")

	messagesSentCounter, err = meter.Int64Counter(
		"go.producer.messages_sent",
		otelmetric.WithDescription("Counts the number of messages sent by the Go producer"),
		otelmetric.WithUnit("1"),
	)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to create messagesSentCounter: %w", err)
	}

	log.Printf("OpenTelemetry initialized for service: %s, exporting to %s\n", serviceName, otlpEndpoint)
	return tracerProvider.Shutdown, meterProvider.Shutdown, nil
}

func main() {
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	tracerShutdown, meterShutdown, err := initOtel(ctx)
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
			log.Printf("Failed to produce message: %v\n", err)
			messagesSentCounter.Add(spanCtx, 1, otelmetric.WithAttributes(attribute.String("status", "error")))
			span.SetAttributes(attribute.String("error", err.Error()))
		} else {
			log.Printf("Message sent successfully: %s\n", message)
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
