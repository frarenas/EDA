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
ROUTING_KEYS = ["login.info", "login.warning", "login.error"]
MESSAGES = [
    "11111111111",
    "22222222222",
    "33333333333.",
    "444444444444",
    "555555555555"
]

try:
    credentials = pika.PlainCredentials('admin', 'admin00') # Replace with your credentials
    parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=int(rabbitmq_port),  # Default RabbitMQ port
        virtual_host='/', # Default virtual host
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    while True:
        routing_key = random.choice(ROUTING_KEYS)
        message = random.choice(MESSAGES)

        send_with_headers = random.choice([True, False])

        if send_with_headers:
            # Define the headers
            headers = {
                "app-id": "login",
                "service": "user-authentication",
                "timestamp": int(time.time())
            }
            # Create a BasicProperties object with the headers
            properties = pika.BasicProperties(headers=headers)
            print(" [x] Sent WITH headers")
        else:
            # Create a BasicProperties object without headers
            properties = pika.BasicProperties()
            print(" [x] Sent WITHOUT headers")

        channel.basic_publish(
            exchange='city-pass.exchange',
            routing_key=routing_key,
            body=message.encode(),
            properties=properties
        )
        print(f" [x] Sent {routing_key}: {message}")
    
        
        # Wait for 1 second
        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    sys.exit(1)