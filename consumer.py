import time
import pika
import os
import sys
import json
from config import Config
from models import Contact
import connect

config = Config()

queue_name = config.queue_name


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    def send_email_stub(contact):

        print(f"Sending email to {contact.email}...")
        time.sleep(1)
        print(f"Email sent to {contact.email}.")


    def callback(ch, method, properties, body):
        message = json.loads(body.decode('utf-8'))
        contact_id = message.get("contact_id")
        if contact_id:

            contact = Contact.objects(id=contact_id).first()

            if contact and not contact.is_sent:
                print(f" [x] Received contact {contact.name}, {contact.email}")

                send_email_stub(contact)

                contact.is_sent = True
                contact.save()

                print(f" [x] Done {method.delivery_tag} task")
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print(f" [x] Contact {contact_id} not found or already sent.")


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)