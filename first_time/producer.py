import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.queue_declare(queue="one")
ch.basic_publish(
    exchange="",
    routing_key="one",
    body="Hello World...!",
    properties=pika.BasicProperties(headers={"name": "mahdi"}),
)
print("message sent...!")

connection.close()
