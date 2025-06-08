#!/bin/bash

# Simple script to start the Kafka O11y Tutorial environment

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker could not be found. Please install Docker."
    exit 1
fi

# Check if Docker Compose is installed (v2 syntax)
if ! docker compose version &> /dev/null
then
    echo "Docker Compose (v2 syntax: 'docker compose') could not be found. Please ensure you have a recent version of Docker Desktop or Docker Engine with Compose plugin."
    exit 1
fi

echo "Starting Kafka O11y Tutorial environment with Docker Compose..."
echo "This might take a few minutes for the first time as images are downloaded and built."

# Bring up all services in detached mode
docker compose up --build -d

if [ $? -eq 0 ]; then
    echo ""
    echo "Environment started successfully!"
    echo "----------------------------------"
    echo "Access the services at these URLs (from your host machine):"
    echo "- Streamlit Tutorial: http://localhost:8501"
    echo "- Grafana:            http://localhost:3000 (admin/admin)"
    echo "- Kafka (external):   localhost:29092 (for tools like kcat/kafkacat if needed)"
    echo ""
    echo "To see logs for all services: docker compose logs -f"
    echo "To see logs for a specific service: docker compose logs -f <service_name> (e.g., java-producer)"
    echo "To stop the environment: docker compose down"
else
    echo ""
    echo "There was an error starting the environment with Docker Compose."
    echo "Please check the output above for more details."
    exit 1
fi

exit 0
