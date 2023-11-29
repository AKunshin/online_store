from rest_framework.viewsets import ModelViewSet
from payments.serializers import ItemSerializer

from shop.models import Item

class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer