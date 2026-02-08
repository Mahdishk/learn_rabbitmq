import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="main_dlx", exchange_type="direct")
ch.basic_publish(exchange="main_dlx", routing_key="home", body="Hello World...!")

print("message sent...!")
connection.close()
