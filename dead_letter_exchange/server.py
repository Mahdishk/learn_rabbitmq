import pika

credentials = pika.PlainCredentials("mahdi", "123456")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", credentials=credentials)
)
ch = connection.channel()

ch.exchange_declare(exchange="main_dlx", exchange_type="direct")
ch.exchange_declare(exchange="dlx", exchange_type="fanout")

ch.queue_declare(
    queue="main_dlx_q",
    arguments={
        "x-dead-letter-exchange": "dlx",
        "x-message-ttl": 5000,
        "x-max-length": 10,
    },
)
ch.queue_bind(exchange="main_dlx", queue="main_dlx_q", routing_key="home")

ch.queue_declare(queue="dlxq")
ch.queue_bind(exchange="dlx", queue="dlxq")


def dlx_callback(ch, method, properties, body):
    print(f"DLX exchange: {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


ch.basic_consume(queue="dlxq", on_message_callback=dlx_callback)

print("Starting server...!")
ch.start_consuming()
