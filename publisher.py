#!/usr/bin/env python
import pika
import os
import sys
import time
import random

rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')

if not rabbitmq_host or not rabbitmq_port:
    print("Error: RABBITMQ_HOST or RABBITMQ_PORT environment variables are not set.")
    sys.exit(1)

# Lists for random message and routing key selection
ROUTING_KEYS = ["modulo0.info", "modulo0.warning", "modulo0.error", "modulo1.info", "modulo1.warning", "modulo1.error"]
MESSAGES = [
    "User logged in successfully.",
    "A minor error was detected in the system.",
    "The database connection failed.",
    "A new session was started.",
    "The disk space is running low."
]

try:
    credentials = pika.PlainCredentials('guest', 'guest') # Replace with your credentials
    parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=int(rabbitmq_port),  # Default RabbitMQ port
        virtual_host='/', # Default virtual host
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    while True:
        routing_key = random.choice(ROUTING_KEYS)
        message = random.choice(MESSAGES)
        channel.basic_publish(
            exchange='topic_logs', routing_key=routing_key, body=message.encode())
        print(f" [x] Sent {routing_key}: {message}")
        
        # Wait for 1 second
        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    sys.exit(1)