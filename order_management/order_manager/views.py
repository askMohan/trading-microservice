import json
from decimal import Decimal

from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import ORDER_STATUS
from .models import Order
from .serializers import OrderSerializer
from common.rabbitmq import producer


class OrderViewSet(viewsets.ViewSet):
    def list(self, request):
        Orders = Order.objects.all()
        serializer = OrderSerializer(Orders, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        producer.publish(
            settings.OUTGOING_QUEUE_TO_SEND_ORDERS_TO_TRADE_MANAGER,
            serializer.data,
            content_type='order_created'
        )
        response = {"id": serializer.data['id']}
        return Response(response, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(id=pk)
            serializer = OrderSerializer(order)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            if order.status == 1 or order.status == 2:
                order = Order.objects.get(id=pk)
                data = request.data
                curr_price = order.price
                order.price=data['updated_price']
                order.save()
            else:
                return Response(status=status.HTTP_417_EXPECTATION_FAILED)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        producer.publish(
            settings.OUTGOING_QUEUE_TO_SEND_ORDERS_TO_TRADE_MANAGER,
            {
                "id":order.id,
                "curr_price":float(curr_price),
                "new_price":float(order.price),
                "side": order.side
            },
            content_type='order_updated'
        )
        return Response({"success": True}, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            order = Order.objects.get(id=pk)
            print(order.status == 3)
            if order.status == 1 or order.status == 2:
                order.status = ORDER_STATUS.CANCELLED.value
                order.save()
            else:
                return Response(status=status.HTTP_417_EXPECTATION_FAILED)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        producer.publish(
            settings.OUTGOING_QUEUE_TO_SEND_ORDERS_TO_TRADE_MANAGER,
            {
                "id":order.id,
                "curr_price":float(order.price),
                "side": order.side
            },
            content_type='order_deleted'
        )
        return Response({"success": True}, status=status.HTTP_200_OK)