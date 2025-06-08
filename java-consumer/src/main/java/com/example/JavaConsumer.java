package com.example;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Duration;
import java.util.Collections;
import java.util.Properties;

public class JavaConsumer {

    private static final Logger logger = LoggerFactory.getLogger(JavaConsumer.class);
    private static final String TOPIC_NAME = "tutorial-topic";
    private static final String BOOTSTRAP_SERVERS = "kafka:9092"; // Docker service name
    private static final String GROUP_ID = "java-consumer-group";

    public static void main(String[] args) {
        logger.info("Starting Java Kafka Consumer with OpenTelemetry");

        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, GROUP_ID);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest"); // Start reading from the beginning of the topic
        props.put(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "true"); // Auto commit offsets

        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList(TOPIC_NAME));
            logger.info("Subscribed to topic: {}", TOPIC_NAME);

            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(1000)); // Poll for new messages
                if (records.isEmpty()) {
                    // logger.trace("No records received in this poll interval."); // Too verbose for INFO
                    continue;
                }
                for (ConsumerRecord<String, String> record : records) {
                    logger.info("Received message: Key='{}', Value='{}', Partition={}, Offset={}",
                            record.key(), record.value(), record.partition(), record.offset());
                    // Here you would typically process the message
                }
                // Offsets are auto-committed in this example.
                // For manual commit: consumer.commitAsync(); or consumer.commitSync();
            }
        } catch (Exception e) {
            logger.error("Java Consumer encountered an error", e);
        } finally {
             logger.info("Java Consumer is shutting down.");
        }
    }
}
