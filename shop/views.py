import os
import stripe
from django.conf import settings
from dotenv import load_dotenv
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from shop.serializers import ItemSerializer, OrderSerializer
from shop.models import Item, Order

load_dotenv()

stripe.api_key = settings.STRIPE_SECRET_KEY
domain_url = str(os.getenv('DOMAIN_URL'))


class ItemViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(methods=["get"],detail=False)
    def buy(self, request):
        item_id = request.GET.get("id")
        item = Item.objects.get(pk=item_id)
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
            return Response({"error": str(e)})

        return Response({"sessionId": checkout_session["id"]})



class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
