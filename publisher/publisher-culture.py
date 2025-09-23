#!/usr/bin/env python
import pika
import os
import sys
import time
import random

rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')

if not rabbitmq_host or not rabbitmq_port or not rabbitmq_user or not rabbitmq_pass:
    print("Error: RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS environment variables are not set.")
    sys.exit(1)

class Message:
    def __init__(self, topic, payload):
        self.topic = topic
        self.payload = payload

MESSAGES = [
    Message("culture.mobility.roads", '{description: "Tránsito restringido", location: "Colonia 2500"}'),
    Message("culture.mobility.buses", '{description: "Cambio de recorrido línea 146", location: "Gral Paz 1400"}'),
    Message("culture.waste.collection", '{description: "recolección por evento", location: "Estadio Huracan"}')
]

try:
    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
    parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=int(rabbitmq_port),
        virtual_host='/',
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    while True:
        message = random.choice(MESSAGES)

        send_with_headers = random.choice([True, False])

        headers = {
            "module": "culture",
            "channel": "eda",
            "schema": "v1",
            "topic": message.topic,
            "timestamp": int(time.time())
        }

        properties = pika.BasicProperties(headers=headers)

        channel.basic_publish(
            exchange='city-pass.exchange',
            routing_key=message.topic,
            body=message.payload.encode(),
            properties=properties
        )
        print(f" [x] Sent {message.topic}: {message.payload}")
    
        # Wait for 1 second
        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    sys.exit(1)