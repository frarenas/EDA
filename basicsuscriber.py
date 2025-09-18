#!/usr/bin/env python
import pika
import os
import sys

rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_port = os.getenv('RABBITMQ_PORT')

if not rabbitmq_host or not rabbitmq_port:
    print("Error: RABBITMQ_HOST or RABBITMQ_PORT environment variables are not set.")
    sys.exit(1)

try:
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    credentials = pika.PlainCredentials('admin', 'admin00') # Replace with your credentials
    parameters = pika.ConnectionParameters(
        host=rabbitmq_host,
        port=int(rabbitmq_port),  # Default RabbitMQ port
        virtual_host='/', # Default virtual host
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

    result = channel.queue_declare('', exclusive=True)
    queue_name = result.method.queue

    binding_keys = sys.argv[1:]
    if not binding_keys:
        sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
        sys.exit(1)

    for binding_key in binding_keys:
        channel.queue_bind(
            exchange='topic_logs', queue=queue_name, routing_key=binding_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')


    def callback(ch, method, properties, body):
        print(f" [x] {method.routing_key}: {body}")


    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()

except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    sys.exit(1)