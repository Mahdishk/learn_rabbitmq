import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="topic_logs", exchange_type="topic")

messages = {
    "error.warning.important": "this is an important message",
    "error.critical.important": "this is super important message",
    "info.debug.notimportant": "this is not an important message",
}

for k, v in messages.items():
    ch.basic_publish(exchange="topic_logs", routing_key=k, body=v)

print("Sent...!")
connection.close()
