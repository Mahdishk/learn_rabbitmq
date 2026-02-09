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

print("Waiting for messages...!")


def callback(ch, method, properties, body):
    print(f"Received: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue="confirm_queue", on_message_callback=callback)

print("Starting server...!")
ch.start_consuming()
