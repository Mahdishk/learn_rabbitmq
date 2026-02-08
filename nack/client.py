import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="nack_exchange", exchange_type="fanout")

while True:
    ch.basic_publish(exchange="nack_exchange", routing_key="home", body="Hello World...!")
    print("message sent...!")
    input("Press enter to send another message...")

