import pika
from pika.exchange_type import ExchangeType

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="he", exchange_type=ExchangeType.headers)
message = "Hello world...!"
ch.basic_publish(
    exchange="he",
    routing_key="",
    body=message,
    properties=pika.BasicProperties(headers={"name": "mahdi"}),
)

print("Sent...!")
connection.close()
