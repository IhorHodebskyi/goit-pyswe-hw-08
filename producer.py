import pika
from datetime import datetime
import json
from config import Config
from models import Contact
from faker import Faker
import connect

fake = Faker()

config = Config()

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))

channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
channel.queue_declare(queue=config.queue_name, durable=True)
channel.queue_bind(exchange='direct_logs', queue=config.queue_name, routing_key='web')


def create_fake_contacts(num_contacts):
    contacts = []
    for _ in range(num_contacts):
        name = fake.name()
        email = fake.email()
        contact = Contact(name=name, email=email, message="Fake email message", is_sent=False)
        contact.save()
        contacts.append(contact)
    return contacts


contacts = create_fake_contacts(100)

def criate_tasc(contacts):
    for contact in contacts:
        message = {
            "contact_id": str(contact.id)
        }

        message_json = json.dumps(message)
        channel.basic_publish(
            exchange='direct_logs',
            routing_key='web',
            body=message_json,
            properties=pika.BasicProperties(delivery_mode=2))

        print(f" [x] Sent {contact.name}, {contact.email}")

    connection.close()

if __name__ == '__main__':
    criate_tasc(contacts)