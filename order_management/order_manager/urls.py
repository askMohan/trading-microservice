from django.urls import path
from .views import OrderViewSet

urlpatterns = [
    path('order', OrderViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('order/<str:pk>', OrderViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
]