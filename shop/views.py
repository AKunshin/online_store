from rest_framework.viewsets import ModelViewSet

from shop.serializers import ItemSerializer, OrderSerializer
from shop.models import Item, Order


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
