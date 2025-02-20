# admin_api/app/messaging.py

import pika
import json

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    return connection

def publish_book_update(message: dict):
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.exchange_declare(exchange='book_updates', exchange_type='fanout')
    channel.basic_publish(
        exchange='book_updates',
        routing_key='',
        body=json.dumps(message)
    )
    connection.close()
