import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="first_exchange", exchange_type="direct")
ch.exchange_declare(exchange="second_exchange", exchange_type="fanout")
ch.exchange_bind(destination="second_exchange", source="first_exchange")

ch.basic_publish(exchange="first_exchange", routing_key="", body="Hello World...!")

print("message sent...!")
connection.close()
