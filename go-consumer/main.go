package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
    // "strings" // Not used
	"syscall"
	"time"

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
	// "go.opentelemetry.io/contrib/instrumentation/github.com/confluentinc/confluent-kafka-go/otelkafka/v2"
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
	serviceName           = getEnv("OTEL_SERVICE_NAME", "go-kafka-consumer")
	kafkaBootstrapServers = getEnv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
	topic                 = "tutorial-topic"
	groupID               = "go-consumer-group"
    tracer                trace.Tracer
    meter                 otelmetric.Meter
    messagesReceivedCounter otelmetric.Int64Counter
    processingTimeHistogram otelmetric.Float64Histogram
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
    tracer = tracerProvider.Tracer("github.com/example/go-consumer") // Use actual module name


    metricExporter, err := otlpmetricgrpc.New(ctx, otlpmetricgrpc.WithInsecure(), otlpmetricgrpc.WithEndpoint(otlpEndpoint))
    if err != nil {
        return nil, nil, fmt.Errorf("failed to create OTLP metric exporter: %w", err)
    }
    meterProvider := metric.NewMeterProvider(
        metric.WithResource(res),
        metric.WithReader(metric.NewPeriodicReader(metricExporter, metric.WithInterval(5*time.Second))),
    )
    otel.SetMeterProvider(meterProvider)
    meter = meterProvider.Meter("github.com/example/go-consumer") // Use actual module name

    messagesReceivedCounter, err = meter.Int64Counter(
        "go.consumer.messages_received",
        otelmetric.WithDescription("Counts the number of messages received by the Go consumer"),
        otelmetric.WithUnit("1"),
    )
    if err != nil {
        return nil, nil, fmt.Errorf("failed to create messagesReceivedCounter: %w", err)
    }
    processingTimeHistogram, err = meter.Float64Histogram(
        "go.consumer.message_processing_duration",
        otelmetric.WithDescription("Measures the duration of message processing in the Go consumer"),
        otelmetric.WithUnit("ms"),
    )
    if err != nil {
        return nil, nil, fmt.Errorf("failed to create processingTimeHistogram: %w", err)
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
		if err := tracerShutdown(context.Background()); err != nil { // Use new context for shutdown
			log.Printf("Error shutting down tracer provider: %v", err)
		}
        if err := meterShutdown(context.Background()); err != nil {
            log.Printf("Error shutting down meter provider: %v", err)
        }
	}()

	// --- Kafka Consumer Setup ---
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": kafkaBootstrapServers,
		"group.id":          groupID,
		"auto.offset.reset": "earliest",
        "enable.auto.commit": "true", // Auto commit, can be false for manual
	})
	if err != nil {
		log.Fatalf("Failed to create Kafka consumer: %v", err)
	}
	defer c.Close() // Ensure consumer is closed on exit

	// Note: Kafka instrumentation temporarily disabled due to package compatibility
	// instrumentedConsumer := otelkafka.NewConsumer(c)

	err = c.Subscribe(topic, nil)
	if err != nil {
		log.Fatalf("Failed to subscribe to topic %s: %v", topic, err)
	}

	log.Printf("Go Kafka consumer started. Group ID: %s. Waiting for messages on topic %s...\n", groupID, topic)

	sigchan := make(chan os.Signal, 1)
	signal.Notify(sigchan, syscall.SIGINT, syscall.SIGTERM)
	run := true

	for run {
		select {
		case sig := <-sigchan:
			log.Printf("Caught signal %v: terminating\n", sig)
			run = false
		default:
            // Note: Using direct Kafka consumer (instrumentation disabled)
			msg, err := c.ReadMessage(100*time.Millisecond) // Poll with timeout

			if err != nil {
				// Errors other than timeout
				if kerr, ok := err.(kafka.Error); ok && kerr.Code() != kafka.ErrTimedOut {
					log.Printf("Consumer error: %v (%v)\n", err, msg)
                    messagesReceivedCounter.Add(ctx, 1, otelmetric.WithAttributes(attribute.String("status", "error")))
				}
				continue // Continue polling on timeout or other non-fatal errors
			}

            processCtx, processSpan := tracer.Start(ctx, "process_go_kafka_message")
            startTime := time.Now()

			log.Printf("Received message on %s [%d] at offset %v: key=%s, value=%s\n",
				*msg.TopicPartition.Topic, msg.TopicPartition.Partition, msg.TopicPartition.Offset,
				string(msg.Key), string(msg.Value))

            // Simulate processing
            time.Sleep(50 * time.Millisecond)

            messagesReceivedCounter.Add(processCtx, 1, otelmetric.WithAttributes(attribute.String("status", "success")))
            processSpan.SetAttributes(
                attribute.Int("messaging.kafka.partition", int(msg.TopicPartition.Partition)),
                attribute.Int("messaging.kafka.offset", int(msg.TopicPartition.Offset)),
                attribute.String("custom.processing.status", "completed"),
            )
            processingDurationMs := float64(time.Since(startTime).Microseconds()) / 1000.0
            processingTimeHistogram.Record(processCtx, processingDurationMs)
            processSpan.End()
		}
	}
	log.Println("Closing consumer...")
}
