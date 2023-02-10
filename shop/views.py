import os
import stripe
from django.conf import settings
from dotenv import load_dotenv
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from loguru import logger

from shop.serializers import OrderSerializer
from shop.models import Item, Order

load_dotenv()

stripe.api_key = settings.STRIPE_SECRET_KEY
domain_url = str(os.getenv('DOMAIN_URL'))


@api_view(["GET"])
def api_buy_item(request, pk):
    if Item.objects.filter(pk=pk).exists():
        item = Item.objects.get(pk=pk)
    else:
        return Response({"detail": "Товар с данным id не найден"},
                        status=status.HTTP_400_BAD_REQUEST)
    logger.debug(f"item_id: {item}")
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success/",
            cancel_url=domain_url + "cancel/",
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": item.currency,
                    "product_data": {
                        "name": item.name,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": 1,
            }],
            allow_promotion_codes=True,
        )
    except Exception as e:
        return Response(data={"error": str(e)})

    return Response(data={"sessionId": checkout_session["id"]})


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
