from datetime import datetime

from marshmallow import fields,INCLUDE, Schema, post_load
from .order import Order

class OrderInputSchema(Schema):
    side = fields.Integer(required=True)
    id = fields.Integer(required=True)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)

    class Meta:
        unknown = INCLUDE

    @post_load
    def make_order(self, data, **kwargs):
        order_data = {
            'id': data['id'],
            'side': data['side'],
            'price': data['price'],
            'quantity': data['quantity']
        }
        return Order(**order_data)

