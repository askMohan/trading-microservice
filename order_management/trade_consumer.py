import django
import os, pika, json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "order_management.settings")
django.setup()

from django.conf import settings

from order_manager import dal as order_manager_dal

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host='rabbitmq_ms', heartbeat=1000, blocked_connection_timeout=1000
        )
)

channel = connection.channel()

channel.queue_declare(queue=settings.INCOMING_QUEUE_TO_RECEIVE_TRADES_UPDATE, durable=True)

def callback(ch, method, properties, body):
    data = json.loads(body)
    if properties.content_type == 'trade_update':
        order_manager_dal.update_state_and_traded_quantity(data['id'], data['traded_quantity'], data['average_traded_price'])

channel.basic_consume(queue=settings.INCOMING_QUEUE_TO_RECEIVE_TRADES_UPDATE, on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()

