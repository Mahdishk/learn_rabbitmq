import uuid

import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

reply_queue = ch.queue_declare(queue="", exclusive=True)


def on_reply_message_received(ch, method, properties, body):
    print(f"reply received: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(
    queue=reply_queue.method.queue,
    on_message_callback=on_reply_message_received
)

ch.queue_declare("request-queue")
core_id = str(uuid.uuid4())
print(f"Sending request: {core_id}")

ch.basic_publish(
    exchange="",
    routing_key="request-queue",
    body="Can I request a reply?",
    properties=pika.BasicProperties(
        reply_to=reply_queue.method.queue, correlation_id=core_id
    ),
)

print("Starting client...!")
ch.start_consuming()
