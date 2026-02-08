import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="alternate", exchange_type="fanout")
ch.exchange_declare(
    exchange="main",
    exchange_type="direct",
    arguments={"alternate-exchange": "alternate"},
)

ch.basic_publish(exchange="main", routing_key="error", body="Hello World...!")

print("message sent...!")
connection.close()