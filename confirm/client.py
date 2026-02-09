import time

import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(
    exchange="confirm_exchange", exchange_type="direct", durable=True, auto_delete=False
)
ch.queue_declare(
    queue="confirm_queue", durable=True, exclusive=False, auto_delete=False
)
ch.queue_bind(
    exchange="confirm_exchange", queue="confirm_queue", routing_key="confirm_key"
)

ch.confirm_delivery()

for i in range(20):
    try:
        ch.basic_publish(
            exchange="confirm_exchange",
            routing_key="confirm_key",
            body=f"Hello World...! {i}",
            properties=pika.BasicProperties(content_type="text/plain", delivery_mode=2),
            mandatory=True,
        )
        print(f"Message {i} confirmed")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(2)
