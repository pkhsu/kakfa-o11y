package main

import (
	"context"
	"os"
	"strings"
	"testing"
    // "github.com/confluentinc/confluent-kafka-go/v2/kafka" // Not strictly needed for these tests
    // We need to mock parts of OTel and potentially Kafka client if we were to test deeper.
    // For now, focus on what can be tested without heavy mocking of Cgo components.
)

// Test getEnv function
func TestGetEnv(t *testing.T) {
    t.Run("should return fallback if env var not set", func(t *testing.T) {
        key := "NON_EXISTENT_ENV_VAR_FOR_TEST"
        fallback := "default_value"
        if val := getEnv(key, fallback); val != fallback {
            t.Errorf("getEnv(%s, %s) = %s; want %s", key, fallback, val, fallback)
        }
    })

    t.Run("should return env var value if set", func(t *testing.T) {
        key := "EXISTENT_ENV_VAR_FOR_TEST"
        expectedValue := "actual_value"
        fallback := "default_value"

        os.Setenv(key, expectedValue)
        defer os.Unsetenv(key) // Cleanup

        if val := getEnv(key, fallback); val != expectedValue {
            t.Errorf("getEnv(%s, %s) = %s; want %s", key, fallback, val, expectedValue)
        }
    })
}

// Test OTel initialization (basic check, not deep mocking of all OTel components)
// This test is more of an integration test snippet as it tries to set up real OTel components.
// A pure unit test would mock otlptracegrpc.New, resource.New etc.
func TestInitOtel_Producer(t *testing.T) {
    // Set minimal environment variables required by initOtel
    os.Setenv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317") // Dummy endpoint
    os.Setenv("OTEL_SERVICE_NAME", "test-go-producer-otel")
    defer os.Unsetenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    defer os.Unsetenv("OTEL_SERVICE_NAME")

    ctx := context.Background()
    tracerShutdown, meterShutdown, err := initOtel(ctx)

    if err != nil {
        // Allow specific error if endpoint is not actually available,
        // as this test runs without a real OTel collector.
        // We are primarily checking that the function attempts to initialize.
        if !strings.Contains(err.Error(), "connection refused") && !strings.Contains(err.Error(), "context deadline exceeded") {
             t.Fatalf("initOtel() failed unexpectedly: %v", err)
        }
         t.Logf("initOtel() failed as expected without a collector: %v", err)
    } else {
         t.Log("initOtel() succeeded (unexpected without a collector, but implies setup logic ran)")
    }


    // Check if tracer and meter were assigned (even if providers failed to connect)
    // Note: In the actual code, tracer and meter are global. This isn't ideal for testing.
    // For this test, we can't directly assert on the global `tracer` and `meter`
    // without refactoring initOtel or the global variables.
    // This test primarily ensures initOtel runs without panic and returns.

    if tracerShutdown == nil {
        t.Error("initOtel() tracerShutdown function is nil")
    }
    if meterShutdown == nil {
         t.Error("initOtel() meterShutdown function is nil")
    }

    // Attempt to call shutdown functions to ensure they don't panic
    if tracerShutdown != nil {
         if err := tracerShutdown(ctx); err != nil {
             if !strings.Contains(err.Error(), "context deadline exceeded"){ // Expected if exporter never connected
                 t.Logf("tracerShutdown failed (tolerable in test if due to no collector): %v", err)
             }
         }
    }
    if meterShutdown != nil {
         if err := meterShutdown(ctx); err != nil {
              if !strings.Contains(err.Error(), "context deadline exceeded"){
                 t.Logf("meterShutdown failed (tolerable in test if due to no collector): %v", err)
              }
         }
    }
}

// Testing the main Kafka producing loop is complex for a unit test due to:
// - Infinite loop
// - Direct usage of kafka.NewProducer and its methods (CGO)
// - time.Sleep
// - os.Signal handling
// Such a test would be an integration test.

// Placeholder for a test that might be possible with significant refactoring
// or by testing smaller, extracted helper functions.
func TestMessageCreationLogic(t *testing.T) {
     // If message creation had complex logic, it could be extracted and tested.
     // e.g., key := fmt.Sprintf("go-key-%d", messageCount)
     // value := fmt.Sprintf("Hello from Go Producer! Message ID: %s, Count: %d", key, messageCount)
     // This is simple enough not to warrant its own test unless it grew.
     t.Skip("Skipping direct test of message creation as it's simple and embedded in main loop.")
}
