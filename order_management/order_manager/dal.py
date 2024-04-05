from . import models

def update_state_and_traded_quantity(id, state, traded_quantity):
    try:
        order = models.Order.objects.get(id=id)
        order.state = state
        order.traded_quantity = traded_quantity
        order.save()
    except models.Order.DoesNotExist:
        return