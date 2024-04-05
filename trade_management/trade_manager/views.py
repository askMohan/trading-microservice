import json
from decimal import Decimal

from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from .serializers import TradeSerializer

class TradeViewSet(viewsets.ViewSet):
    def list(self, request):
        Orders = models.Trade.objects.all()
        serializer = TradeSerializer(Orders, many=True)
        return Response(serializer.data)