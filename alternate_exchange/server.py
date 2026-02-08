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

ch.queue_declare(queue="altq")
ch.queue_bind(exchange="alternate", queue="altq")

ch.queue_declare(queue="mainq")
ch.queue_bind(exchange="main", queue="mainq", routing_key="home")


def alt_callback(ch, method, properties, body):
    print(f"Alternate exchange: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main_callback(ch, method, properties, body):
    print(f"Main exchange: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue="altq", on_message_callback=alt_callback)
ch.basic_consume(queue="mainq", on_message_callback=main_callback)

print("Starting server...!")
ch.start_consuming()