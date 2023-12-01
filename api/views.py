from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from payments.service import create_payment_intent
from shop.models import Item, Order

from .serializers import ItemSerializer


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemDetailView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "shop/item_detail.html"

    def get(self, request, pk):
        try:
            item = get_object_or_404(Item, pk=pk)
            serializer = ItemSerializer(item)
            return Response({"serializer": serializer,"item": item})
        except Http404:
            return Response(
                {"detail": "Товар с данным id не найден"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        serializer = ItemSerializer(item, data=request.data)
        if not serializer.is_valid():
            return Response({"serializer": serializer, "item": item})
        serializer.save()
        return redirect("home")



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
