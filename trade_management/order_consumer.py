import django
import os, pika, json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "trade_management.settings")
django.setup()

from django.conf import settings

from trade_manager.orderbook.order_book import OrderBook

params = pika.URLParameters('amqp://guest:guest@host.docker.internal:5672/')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue=settings.INCOMING_QUEUE_TO_RECEIVE_ORDERS_TO_TRADE_MANAGER)

order_book = OrderBook()

def callback(ch, method, properties, body):
    print('Received in main')
    print(body)
    print(type(body))
    data = body

    if properties.content_type == 'order_created':
        order_book.create_order(body)

    elif properties.content_type == 'order_updated':
        data = json.loads(body)
        order_book.update_order(
            data['id'], data['curr_price'], data['new_price'], data['side']
        )

    elif properties.content_type == 'order_deleted':
        data = json.loads(body)
        order_book.delete_order(data['id'], data['curr_price'], data['side'])


channel.basic_consume(queue=settings.INCOMING_QUEUE_TO_RECEIVE_ORDERS_TO_TRADE_MANAGER, on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()

