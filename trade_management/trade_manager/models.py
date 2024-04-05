from django.db import models

# Create your models here.

from django.db import models


class Trade(models.Model):
    bid_order_id = models.IntegerField()
    ask_order_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
