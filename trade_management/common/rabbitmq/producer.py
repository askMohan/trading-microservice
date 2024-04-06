import pika, json
from django.conf import settings

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq_ms', heartbeat=1000, blocked_connection_timeout=1000
        )
)
channel = connection.channel()

def publish(queue_name, body, **method):
    print("=================================")
    print(body)
    print("=========================================")
    properties = pika.BasicProperties(**method)
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(body), properties=properties)

