
# Create your models here.
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.core.mail import send_mail
from django.urls import reverse
from django.template.loader import get_template

class User(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=120, null=False)
    email = models.EmailField(unique=True, max_length=255, null=False)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    cash = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True, db_index=True)
    staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.username

    @property
    def is_staff(self):
        return self.staff

    def buy_stocks(self, quantity, price):
        purchase_amount = Decimal(quantity) * price
        if self.cash >= purchase_amount:
            self.cash -= Decimal(quantity) * price
            self.save()
            return True
        return False

    def sell_stocks(self, quantity, price):
        self.cash += Decimal(quantity) * price
        self.save()