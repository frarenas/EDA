import pika
import os
import sys
import threading
from flask import Flask, render_template, Response, request
import json
import time

# Flask App Initialization
app = Flask(__name__, template_folder='templates')

# Queue for messages received from RabbitMQ
message_queues = {}
lock = threading.Lock()

# RabbitMQ Connection and Consumer
def rabbitmq_consumer(queue_name):
    try:
        rabbitmq_host = os.getenv('RABBITMQ_HOST')
        rabbitmq_port = os.getenv('RABBITMQ_PORT')

        if not rabbitmq_host or not rabbitmq_port:
            print("Error: RABBITMQ_HOST or RABBITMQ_PORT environment variables are not set.")
            sys.exit(1)

        credentials = pika.PlainCredentials('admin', 'admin00')
        parameters = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=int(rabbitmq_port),
            virtual_host='/',
            credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        def callback(ch, method, properties, body):
            print(f" [x] Received {body.decode()}")
            with lock:
                if queue_name not in message_queues:
                    message_queues[queue_name] = []
                message_queues[queue_name].append(body.decode())
            ch.basic_ack(delivery_tag=method.delivery_tag)

        channel.queue_declare(queue=queue_name, passive=True)
        channel.basic_consume(queue=queue_name, on_message_callback=callback)

        print(f' [*] Waiting for messages on queue: {queue_name}')
        channel.start_consuming()

    except Exception as e:
        print(f"An error occurred in RabbitMQ consumer: {e}", file=sys.stderr)
        sys.exit(1)

# Server-Sent Events Endpoint
@app.route('/stream/<queue_name>')
def stream(queue_name):
    # Start the RabbitMQ consumer in a separate thread if it's not already running
    if queue_name not in message_queues:
        with lock:
            if queue_name not in message_queues:
                message_queues[queue_name] = []
                consumer_thread = threading.Thread(target=rabbitmq_consumer, args=(queue_name,))
                consumer_thread.daemon = True
                consumer_thread.start()
    
    def event_stream():
        while True:
            with lock:
                if message_queues[queue_name]:
                    message = message_queues[queue_name].pop(0)
                    yield f"data: {message}\n\n"
            time.sleep(0.1)

    return Response(event_stream(), mimetype="text/event-stream")

# Webpage Routes
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
