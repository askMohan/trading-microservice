from . import models

def create_trade(**kwargs):
    models.Trade.objects.create(**kwargs)