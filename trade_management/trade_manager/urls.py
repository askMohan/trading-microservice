from django.urls import path
from .views import TradeViewSet

urlpatterns = [
    path('trade', TradeViewSet.as_view({
        'get': 'list',
    }))
]