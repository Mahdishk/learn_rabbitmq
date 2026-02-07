import uuid

import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

reply_queue = ch.queue_declare(queue="request-queue")


def on_reply_message_received(ch, method, properties, body):
    print(f"Received: {properties.correlation_id}")
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,
        body=f"Reply to {properties.correlation_id}",
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue="request-queue", on_message_callback=on_reply_message_received)

print("Starting server...!")
ch.start_consuming()
