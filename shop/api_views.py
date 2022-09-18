from rest_framework import viewsets
from shop.serializers import ItemSerializer
from shop.models import Item


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer