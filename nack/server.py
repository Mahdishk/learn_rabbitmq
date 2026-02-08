import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="nack_exchange", exchange_type="fanout")
ch.queue_declare(queue="nack_queue")
ch.queue_bind(exchange="nack_exchange", queue="nack_queue")

print("Waiting for messages...!")


def callback(ch, method, properties, body):
    if method.delivery_tag % 5 == 0:
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False, multiple=True)
    print(f"received {method.delivery_tag}")


ch.basic_consume(queue="nack_queue", on_message_callback=callback)
print("Starting server...!")
ch.start_consuming()
