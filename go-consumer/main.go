package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"os/signal"
	"syscall"
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
	serviceName           = getEnv("OTEL_SERVICE_NAME", "go-kafka-consumer")
	kafkaBootstrapServers = getEnv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
	topic                 = "tutorial-topic"
	groupID               = "go-consumer-group"
	tracer                trace.Tracer
	meter                 otelmetric.Meter
	logger                otellog.Logger
	messagesReceivedCounter otelmetric.Int64Counter
	processingTimeHistogram otelmetric.Float64Histogram
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
	tracer = tracerProvider.Tracer("github.com/example/go-consumer")

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
	meter = meterProvider.Meter("github.com/example/go-consumer")

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
	logger = loggerProvider.Logger("github.com/example/go-consumer")

	messagesReceivedCounter, err = meter.Int64Counter(
		"go.consumer.messages_received",
		otelmetric.WithDescription("Counts the number of messages received by the Go consumer"),
		otelmetric.WithUnit("1"),
	)
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to create messagesReceivedCounter: %w", err)
	}
	processingTimeHistogram, err = meter.Float64Histogram(
		"go.consumer.message_processing_duration",
		otelmetric.WithDescription("Measures the duration of message processing in the Go consumer"),
		otelmetric.WithUnit("ms"),
	)
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to create processingTimeHistogram: %w", err)
	}

	log.Printf("OpenTelemetry initialized for service: %s, exporting to %s\n", serviceName, otlpEndpoint)
	return tracerProvider.Shutdown, meterProvider.Shutdown, loggerProvider.Shutdown, nil
}

func healthCheck() error {
	// Simple health check - test Kafka connectivity
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": kafkaBootstrapServers,
		"group.id":          "health-check-group",
		"auto.offset.reset": "earliest",
	})
	if err != nil {
		return fmt.Errorf("failed to create Kafka consumer: %w", err)
	}
	defer c.Close()

	// Test basic connection by getting cluster metadata
	metadata, err := c.GetMetadata(nil, false, 5000)
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

	// Kafka Consumer Setup
	c, err := kafka.NewConsumer(&kafka.ConfigMap{
		"bootstrap.servers": kafkaBootstrapServers,
		"group.id":          groupID,
		"auto.offset.reset": "earliest",
		"enable.auto.commit": "true",
	})
	if err != nil {
		log.Fatalf("Failed to create Kafka consumer: %v", err)
	}
	defer c.Close()

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
			msg, err := c.ReadMessage(100 * time.Millisecond)

			if err != nil {
				if kerr, ok := err.(kafka.Error); ok && kerr.Code() != kafka.ErrTimedOut {
					// Standard log for container logs
					log.Printf("[ERROR] [go-consumer] Consumer error on topic=%s: %v", topic, err)
					// OpenTelemetry structured log
					var record otellog.Record
					record.SetTimestamp(time.Now())
					record.SetObservedTimestamp(time.Now())
					record.SetSeverity(otellog.SeverityError)
					record.SetSeverityText("ERROR")
					record.SetBody(otellog.StringValue(fmt.Sprintf("Consumer error on topic=%s: %v", topic, err)))
					record.AddAttributes(
						otellog.String("service.name", "go-consumer"),
						otellog.String("kafka.topic", topic),
						otellog.String("operation", "kafka_consume"),
						otellog.String("status", "error"),
						otellog.String("error", err.Error()),
						otellog.String("component", "kafka"),
						otellog.String("language", "go"),
					)
					logger.Emit(ctx, record)
					messagesReceivedCounter.Add(ctx, 1, otelmetric.WithAttributes(attribute.String("status", "error")))
				}
				continue
			}

			// Create span for message processing
			processCtx, processSpan := tracer.Start(ctx, "process_go_kafka_message")
			startTime := time.Now()

			// Standard log for container logs
			log.Printf("[INFO] [go-consumer] Received message on topic=%s partition=%d offset=%v key=%s value=%s",
				*msg.TopicPartition.Topic, msg.TopicPartition.Partition, msg.TopicPartition.Offset,
				string(msg.Key), string(msg.Value))
			
			// OpenTelemetry structured log
			var record otellog.Record
			record.SetTimestamp(time.Now())
			record.SetObservedTimestamp(time.Now())
			record.SetSeverity(otellog.SeverityInfo)
			record.SetSeverityText("INFO")
			record.SetBody(otellog.StringValue(fmt.Sprintf("Received message on topic=%s partition=%d offset=%v key=%s value=%s", *msg.TopicPartition.Topic, msg.TopicPartition.Partition, msg.TopicPartition.Offset, string(msg.Key), string(msg.Value))))
			record.AddAttributes(
				otellog.String("service.name", "go-consumer"),
				otellog.String("kafka.topic", *msg.TopicPartition.Topic),
				otellog.Int64("kafka.partition", int64(msg.TopicPartition.Partition)),
				otellog.Int64("kafka.offset", int64(msg.TopicPartition.Offset)),
				otellog.String("kafka.key", string(msg.Key)),
				otellog.String("kafka.value", string(msg.Value)),
				otellog.String("operation", "kafka_consume"),
				otellog.String("status", "success"),
				otellog.String("component", "kafka"),
				otellog.String("language", "go"),
			)
			logger.Emit(processCtx, record)

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
