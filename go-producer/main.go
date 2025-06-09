package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"
    // "strings" // Not used, can be removed

	"github.com/confluentinc/confluent-kafka-go/v2/kafka"
	// "go.opentelemetry.io/contrib/instrumentation/github.com/confluentinc/confluent-kafka-go/otelkafka/v2" // v2 for kafka client
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc"
    "go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc"
	"go.opentelemetry.io/otel/propagation"
	"go.opentelemetry.io/otel/sdk/metric"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.21.0" // Use appropriate semantic conventions version
    "go.opentelemetry.io/otel/attribute"
    "go.opentelemetry.io/otel/trace"
    otelmetric "go.opentelemetry.io/otel/metric"
)

var (
	otlpEndpoint           = getEnv("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4317")
	serviceName            = getEnv("OTEL_SERVICE_NAME", "go-kafka-producer")
	kafkaBootstrapServers  = getEnv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
	topic                  = "tutorial-topic"
    tracer                 trace.Tracer
    meter                  otelmetric.Meter
    messagesSentCounter    otelmetric.Int64Counter
)

func getEnv(key, fallback string) string {
	if value, ok := os.LookupEnv(key); ok {
		return value
	}
	return fallback
}

// initOtel sets up the OpenTelemetry pipeline.
func initOtel(ctx context.Context) (func(context.Context) error, func(context.Context) error, error) {
	res, err := resource.New(ctx,
		resource.WithAttributes(semconv.ServiceNameKey.String(serviceName)),
		resource.WithSchemaURL(semconv.SchemaURL),
	)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to create resource: %w", err)
	}

	// --- Trace Exporter and Provider ---
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
    tracer = tracerProvider.Tracer("github.com/example/go-producer") // Use actual module name

	// --- Metric Exporter and Provider ---
    metricExporter, err := otlpmetricgrpc.New(ctx, otlpmetricgrpc.WithInsecure(), otlpmetricgrpc.WithEndpoint(otlpEndpoint))
    if err != nil {
        return nil, nil, fmt.Errorf("failed to create OTLP metric exporter: %w", err)
    }
    meterProvider := metric.NewMeterProvider(
        metric.WithResource(res),
        metric.WithReader(metric.NewPeriodicReader(metricExporter, metric.WithInterval(5*time.Second))),
    )
    otel.SetMeterProvider(meterProvider)
    meter = meterProvider.Meter("github.com/example/go-producer") // Use actual module name

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
	ctx := context.Background()

	tracerShutdown, meterShutdown, err := initOtel(ctx)
	if err != nil {
		log.Fatalf("Failed to initialize OpenTelemetry: %v", err)
	}
	defer func() {
		if err := tracerShutdown(ctx); err != nil {
			log.Printf("Error shutting down tracer provider: %v", err)
		}
        if err := meterShutdown(ctx); err != nil {
            log.Printf("Error shutting down meter provider: %v", err)
        }
	}()

	// --- Kafka Producer Setup ---
	p, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": kafkaBootstrapServers,
		"client.id":         serviceName,
		"acks":              "all",
        // Add other producer configs as needed, e.g., idempotence
        "enable.idempotence": "true",
	})
	if err != nil {
		log.Fatalf("Failed to create Kafka producer: %v", err)
	}
	defer p.Close()

	// Note: Kafka instrumentation temporarily disabled due to package compatibility
	// instrumentedProducer := otelkafka.NewProducer(p)


	// Handle graceful shutdown
	sigchan := make(chan os.Signal, 1)
	signal.Notify(sigchan, syscall.SIGINT, syscall.SIGTERM)

	deliveryChan := make(chan kafka.Event)
	messageCount := 0
	run := true

	log.Println("Go Kafka producer started. Sending messages...")

	for run {
		select {
		case <-sigchan:
			log.Println("Shutdown signal received, terminating producer loop...")
			run = false
		default:
			messageCount++
			key := fmt.Sprintf("go-key-%d", messageCount)
			value := fmt.Sprintf("Hello from Go Producer! Message ID: %s, Count: %d", key, messageCount)

            // Create a custom span for the send operation
            spanCtx, span := tracer.Start(ctx, "send_go_kafka_message",
                trace.WithAttributes(
                    semconv.MessagingSystemKey.String("kafka"),
                    semconv.MessagingDestinationNameKey.String(topic),
                    semconv.MessagingMessageIDKey.String(key),
                ),
            )

			msg := &kafka.Message{
				TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
				Key:            []byte(key),
				Value:          []byte(value),
			}
			// Note: Using direct producer (instrumentation disabled)
			err = p.Produce(msg, deliveryChan)
			if err != nil {
				log.Printf("Failed to produce message: %v\n", err)
                messagesSentCounter.Add(spanCtx, 1, otelmetric.WithAttributes(attribute.String("status", "error")))
			} else {
                // Wait for delivery report
                e := <-deliveryChan
                m := e.(*kafka.Message)
                if m.TopicPartition.Error != nil {
                    log.Printf("Delivery failed: %v\n", m.TopicPartition.Error)
                    messagesSentCounter.Add(spanCtx, 1, otelmetric.WithAttributes(attribute.String("status", "error")))
                    span.SetAttributes(attribute.Bool("error", true), attribute.String("error.message", m.TopicPartition.Error.Error()))
                } else {
                    log.Printf("Delivered message to topic %s [%d] at offset %v (key: %s)\n",
                        *m.TopicPartition.Topic, m.TopicPartition.Partition, m.TopicPartition.Offset, string(m.Key))
                    messagesSentCounter.Add(spanCtx, 1, otelmetric.WithAttributes(attribute.String("status", "success")))
                    span.SetAttributes(
                        attribute.Int64("messaging.kafka.partition", int64(m.TopicPartition.Partition)),
                        attribute.Int64("messaging.kafka.offset", int64(m.TopicPartition.Offset)),
                    )
                }
            }
            span.End()
			time.Sleep(5 * time.Second)
		}
	}

	// Flush remaining messages
	log.Println("Flushing producer...")
	remaining := p.Flush(15000) // timeout 15 seconds
	if remaining > 0 {
		log.Printf("%d messages were not delivered\n", remaining)
	} else {
		log.Println("All messages flushed successfully.")
	}
	log.Println("Go producer shut down.")
}
