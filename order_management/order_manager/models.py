from django.db import models

from .constants import ORDER_SIDES, ORDER_STATUS


class Order(models.Model):
    # user_id = models.IntegerField(null=False)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2, null=False, blank=False)
    side = models.IntegerField(choices=ORDER_SIDES.choices(), null=False)
    status = models.IntegerField(choices=ORDER_STATUS.choices(),default=1, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
