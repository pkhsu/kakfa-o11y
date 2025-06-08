package com.example;

import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Properties;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

public class JavaProducer {

    private static final Logger logger = LoggerFactory.getLogger(JavaProducer.class);
    private static final String TOPIC_NAME = "tutorial-topic";
    private static final String BOOTSTRAP_SERVERS = "kafka:9092"; // Docker service name

    public static void main(String[] args) throws InterruptedException {
        logger.info("Starting Java Kafka Producer with OpenTelemetry");

        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        // Enable idempotence for safety, good practice
        props.put(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");
        props.put(ProducerConfig.ACKS_CONFIG, "all"); // Ensure messages are acknowledged by all replicas
        props.put(ProducerConfig.DELIVERY_TIMEOUT_MS_CONFIG, 30000); // Timeout for message delivery


        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            int messageCount = 0;
            while (true) {
                String messageId = UUID.randomUUID().toString();
                String message = "Hello from Java Producer! Message ID: " + messageId + ", Count: " + (++messageCount);

                ProducerRecord<String, String> record = new ProducerRecord<>(TOPIC_NAME, messageId, message);

                // Asynchronous send
                producer.send(record, (metadata, exception) -> {
                    if (exception == null) {
                        logger.info("Sent message: ID='{}', Partition={}, Offset={}", messageId, metadata.partition(), metadata.offset());
                    } else {
                        logger.error("Error sending message with ID '{}'", messageId, exception);
                    }
                });
                producer.flush(); // Flush messages to ensure they are sent, especially in a loop
                TimeUnit.SECONDS.sleep(5); // Send a message every 5 seconds
            }
        } catch (Exception e) {
            logger.error("Java Producer encountered an error", e);
        }
    }
}
