from datetime import datetime
from decimal import Decimal

import requests
import pytz

import stripe
from bs4 import BeautifulSoup

from django.http import JsonResponse
from django.conf import settings
from django.db.models import Sum


domain_url = settings.DOMAIN_URL
stripe.api_key = settings.STRIPE_SECRET_KEY

customer = stripe.Customer.create()
products = stripe.Product.list()
prices = stripe.Price.list()


def get_current_date() -> str:
    """Получение текущей даты, перевод в строку"""
    timezone = pytz.timezone("Europe/Moscow")
    now_with_tz = timezone.localize(datetime.now())
    current_date = now_with_tz.strftime("%d.%m.%Y")
    return current_date


def exchange_to_rubles() -> Decimal:
    """Перевод долларов в рубли по курсу ЦБ РФ"""
    current_date = get_current_date()
    url = "http://www.cbr.ru/scripts/XML_daily.asp?"
    params = {"date_req": current_date}
    request = requests.get(url, params)
    soup = BeautifulSoup(request.content, "xml")
    dollar_exchange_rate = soup.find(ID="R01235").Value.string
    dollar_exchange_rate = Decimal(dollar_exchange_rate.replace(",", ".")).quantize(
        Decimal("1.00")
    )
    return dollar_exchange_rate


def get_total_price(items) -> Decimal:
    """Функция, для получения общей суммы заказа"""
    total_price_rub = 0
    total_price_usd = 0
    if items.filter(currency="rub"):
        total_price_rub = items.filter(currency="rub").aggregate(Sum("price"))[
            "price__sum"
        ]
    if items.filter(currency="usd"):
        total_price_usd = (
            items.filter(currency="usd").aggregate(Sum("price"))["price__sum"]
            * exchange_to_rubles()
        )
    total_price = total_price_rub + total_price_usd
    total_price = Decimal(total_price).quantize(Decimal("1.00"))
    return total_price


def create_stripe_checkout(item):
    """Создание сессии stripe"""
    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=domain_url + "success/",
            cancel_url=domain_url + "cancel/",
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": item.currency,
                        "product_data": {
                            "name": item.name,
                        },
                        "unit_amount": int(item.price * 100),
                    },
                    "quantity": 1,
                }
            ],
            tax_id_collection={"enabled": True},
            allow_promotion_codes=True,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)})

    return JsonResponse({"sessionId": checkout_session["id"]})


def create_payment_intent(order):
    """Создание stripe payment intent"""
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(order.get_total_price * 100),
            currency="rub",
            automatic_payment_methods={
                "enabled": True,
            },
            customer=customer["id"],
            metadata={"order_id": order.id},
        )
        return JsonResponse({"clientSecret": intent["client_secret"]})
    except Exception as e:
        return JsonResponse({"error": str(e)})
