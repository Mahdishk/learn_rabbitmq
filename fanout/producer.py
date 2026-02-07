import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="logs", exchange_type="fanout")
ch.basic_publish(exchange="logs", routing_key="", body="FANOUT...!")

print("message sent...!")
connection.close()
