import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from decimal import Decimal
from django.db.models import Sum


def get_current_date():
    """Получение текущей даты, перевод в строки"""
    dt = datetime.now()
    d = str(dt.day)
    m = str(dt.month)
    y = str(dt.year)

    # Если число или месяц от 1-9, то добавляем 0,
    # для правильного формата dd/mm/yyyy
    if len(d) == 1:
        d = '0' + d
    if len(m) == 1:
        m = '0' + m

    current_date = f'{d}/{m}/{y}'

    return current_date


def exchange_to_rubles():
    """Перевод долларов в рубли по курсу ЦБ РФ"""
    current_date = get_current_date()
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    params = {'date_req': current_date}
    request = requests.get(url, params)
    soup = BeautifulSoup(request.content, 'xml')
    dollar_exchange_rate = soup.find(ID='R01235').Value.string
    dollar_exchange_rate = Decimal(dollar_exchange_rate.replace(',', '.'))
    return dollar_exchange_rate


def get_total_price(items):
    # Функция, для получения общей суммы заказа
    total_price_rub = 0
    total_price_usd = 0
    if items.filter(currency="rub"):
        total_price_rub = items.filter(currency="rub").aggregate(Sum('price'))['price__sum']
    if items.filter(currency="usd"):
        total_price_usd = items.filter(currency="usd").aggregate(Sum('price'))['price__sum'] * exchange_to_rubles()
    total_price = total_price_rub + total_price_usd
    return total_price