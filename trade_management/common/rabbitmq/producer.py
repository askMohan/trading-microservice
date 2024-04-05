import pika, json
from django.conf import settings

params = pika.URLParameters('amqp://host.docker.internal:5672')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq_ms', heartbeat=1000, blocked_connection_timeout=1000
        )
)
channel = connection.channel()
# channel.queue_declare(queue=settings.OUTGOING_QUEUE_TO_SEND_ORDERS_TO_TRADE_MANAGER, durable=True)

def publish(queue_name, body, **method):
    properties = pika.BasicProperties(**method)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(body), properties=properties)

