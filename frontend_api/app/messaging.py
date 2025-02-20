# frontend_api/app/messaging.py

import pika
import json
import threading
import time
from .database import SessionLocal  # Import your session factory
from .models import Book  # Import your Book model

def get_rabbitmq_connection(retries=5, delay=5):
    for attempt in range(1, retries + 1):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
            print(f"Connected to RabbitMQ on attempt {attempt}")
            return connection
        except Exception as e:
            print(f"Connection attempt {attempt} failed: {repr(e)}")
            time.sleep(delay)
    raise Exception("Failed to connect to RabbitMQ after multiple attempts")

def callback(ch, method, properties, body):
    try:
        message = json.loads(body)
        print("Frontend received book update:", message)
        action = message.get("action")
        db = SessionLocal()  # Create a new database session for each message
        try:
            if action == "add":
                book_data = message.get("book")
                if book_data:
                    
                    existing = db.query(Book).filter(Book.id == book_data["id"]).first()
                    if not existing:
                        new_book = Book(
                            id=book_data["id"], 
                            title=book_data["title"],
                            publisher=book_data.get("publisher"),
                            category=book_data.get("category"),
                            is_available=book_data["is_available"]
                        )
                        db.add(new_book)
                        db.commit()
                        print("Book added to Frontend DB:", new_book)
            elif action == "remove":
                book_id = message.get("book_id")
                if book_id:
                    book = db.query(Book).filter(Book.id == book_id).first()
                    if book:
                        db.delete(book)
                        db.commit()
                        print("Book removed from Frontend DB:", book_id)
        finally:
            db.close()
    except Exception as e:
        print("Error processing message:", repr(e))

def start_subscriber():
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        channel.exchange_declare(exchange='book_updates', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='book_updates', queue=queue_name)
        print("Frontend subscriber started. Waiting for book updates...")
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
    except Exception as e:
        print("Error in subscriber:", repr(e))

def start_background_subscriber():
    thread = threading.Thread(target=start_subscriber, daemon=True)
    thread.start()
