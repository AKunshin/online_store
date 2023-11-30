from rest_framework.serializers import ModelSerializer

from shop.models import Item, Order


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = ("name", "description", "price", "currency")


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "items")
