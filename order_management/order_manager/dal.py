from . import models
from . import constants

def update_state_and_traded_quantity(id, traded_quantity, average_traded_price):
    try:
        order = models.Order.objects.get(id=id)
        order.traded_quantity = traded_quantity
        order.average_traded_price = average_traded_price
        if order.traded_quantity == order.quantity:
            order.status = constants.ORDER_STATUS.SUCCESSFULL.value
        else:
            order.status = constants.ORDER_STATUS.PARTIALLY_FILLED.value
        order.save()
    except models.Order.DoesNotExist:
        return