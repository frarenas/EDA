#!/usr/bin/env python
import pika
import os
import sys
import time

rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')
rabbitmq_user = os.getenv('RABBITMQ_USER')
rabbitmq_pass = os.getenv('RABBITMQ_PASS')

if not rabbitmq_host or not rabbitmq_port or not rabbitmq_user or not rabbitmq_pass:
    print("Error: RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS environment variables are not set.")
    sys.exit(1)

queue_name = sys.argv[1]
if not queue_name:
    sys.stderr.write("Usage: %s [queue_name]...\n" % sys.argv[0])
    sys.exit(1)

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
    channel.basic_qos(prefetch_count=1)

    def callback(ch, method, properties, body):
        print(f" [x] Processing {method.routing_key}: {body.decode()}")
        # Simula un trabajo pesado para la demostración
        time.sleep(2)
        print(" [x] Done")
        # Confirma el mensaje para que RabbitMQ sepa que puede enviar el siguiente
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.queue_declare(queue=queue_name, passive=True)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)

    print(f' [*] Waiting for messages on queue: {queue_name}')
    channel.start_consuming()

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    sys.exit(1)