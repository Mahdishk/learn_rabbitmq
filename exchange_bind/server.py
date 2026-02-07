import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="second_exchange", exchange_type="fanout")
ch.queue_declare(queue="Mahdi")

ch.queue_bind(exchange="second_exchange", queue="Mahdi")

print("Waiting for messages...!")


def callback(ch, method, properties, body):
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue="Mahdi", on_message_callback=callback)

print("Starting server...!")
ch.start_consuming()
