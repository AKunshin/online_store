import requests
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from decimal import Decimal
from django.db.models import Sum


def get_current_date() -> str:
    """Получение текущей даты, перевод в строку"""
    timezone = pytz.timezone("Europe/Moscow")
    now_with_tz = timezone.localize(datetime.now())
    current_date = now_with_tz.strftime("%d.%m.%Y")
    return current_date


def exchange_to_rubles() -> Decimal:
    """Перевод долларов в рубли по курсу ЦБ РФ"""
    current_date = get_current_date()
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    params = {'date_req': current_date}
    request = requests.get(url, params)
    soup = BeautifulSoup(request.content, 'xml')
    dollar_exchange_rate = soup.find(ID='R01235').Value.string
    dollar_exchange_rate = Decimal(
        dollar_exchange_rate.replace(',', '.')).quantize(Decimal("1.00")
        )
    return dollar_exchange_rate


def get_total_price(items) -> Decimal:
    """Функция, для получения общей суммы заказа"""
    total_price_rub = 0
    total_price_usd = 0
    if items.filter(currency="rub"):
        total_price_rub = items.filter(currency="rub").aggregate(Sum('price'))['price__sum']
    if items.filter(currency="usd"):
        total_price_usd = items.filter(currency="usd").aggregate(Sum('price'))['price__sum'] * exchange_to_rubles()
    total_price = total_price_rub + total_price_usd
    total_price = Decimal(total_price).quantize(Decimal("1.00"))
    return total_price
