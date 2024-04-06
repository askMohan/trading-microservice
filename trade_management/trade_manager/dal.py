from . import models

from django.db.models import Count, F, Sum, Q

def create_trade(**kwargs):
    models.Trade.objects.create(**kwargs)

def get_average_traded_price_and_traded_quantity(order_id):
    return models.Trade.objects.filter(Q(bid_order_id=order_id) | Q(ask_order_id=order_id)).annotate(
        total_traded_value=F('quantity') * F('price')
    ).aggregate(average_traded_price=Sum('total_traded_value') / Sum('quantity'), traded_quantity=Sum('quantity'))
