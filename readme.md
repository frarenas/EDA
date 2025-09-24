# RabbitMQ Queue System Example

This project demonstrates a basic message queue system using RabbitMQ and Python. It includes a message consumer with built-in retry logic and a Dead Letter Queue (DLQ) for handling messages that fail to be processed after multiple attempts.

## Prerequisites:
* Docker Compose: Used to run the RabbitMQ service.

* .env file: A file in the base directory with the following variables:
```
RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=
RABBITMQ_PASS=
```

## Usage

### Getting Started

**Start the services:** This command will start the RabbitMQ container in the background.
```
docker compose up -d
```

**Stop the services:**
```
docker compose down
```

