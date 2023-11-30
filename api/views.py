from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from payments.service import create_payment_intent
from shop.models import Item, Order

from .serializers import ItemSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


@api_view(["GET"])
def api_buy_item(request, pk):
    try:
        item = get_object_or_404(Item, pk=pk)
        return Response(item)
    except Http404:
        return Response(
            {"detail": "Товар с данным id не найден"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def api_create_payment_intent(request, pk):
    try:
        order = get_object_or_404(Order, pk=pk)
        response = create_payment_intent(order)
        return response
    except Http404:
        return Response(
            {"detail": "Заказ с данным id не найден"},
            status=status.HTTP_400_BAD_REQUEST,
        )
