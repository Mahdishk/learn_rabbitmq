import pika
from pika.exchange_type import ExchangeType

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="he", exchange_type=ExchangeType.headers)
ch.queue_declare(queue="hq-any")

bind_args = {"x-match": "any", "name": "mahdi", "age": "25"}
ch.queue_bind(exchange="he", queue="hq-any", arguments=bind_args)

print("Waiting for messages...!")


def callback(ch, method, properties, body):
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue="hq-any", on_message_callback=callback)
ch.start_consuming()
