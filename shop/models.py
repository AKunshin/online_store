from django.db import models
from django.db.models import Sum
from django.urls import reverse
from decimal import Decimal
from payments.service import exchange_to_rubles


class Item(models.Model):
    """Модель товара"""
    CURRENCY = (
                ("rub", 'RUB'),
                ("usd", 'USD'),
                )
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10,
                                decimal_places=2,
                                default=1,
                                verbose_name="Цена")
    currency = models.CharField(max_length=3,
                                choices=CURRENCY,
                                default="rub",
                                verbose_name="Валюта")

    @property
    def get_usd_currency(self):
    # Свойство, для конвертации стоимости в USD по курсу ЦБ    
        if self.currency == "usd":
            self.price_usd = self.price
            return self.price_usd
        else:
            self.price_usd = self.price / Decimal(exchange_to_rubles())
            return self.price_usd

    def get_absolute_url(self):
        """Обратное построение адресов"""
        return reverse("view_item", kwargs={"pk": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Order(models.Model):
    """Модель заказа товара"""
    item = models.ManyToManyField(Item,
                                  verbose_name="Товары",
                                  related_name="orders")


    @property
    def get_total_price(self):
        # Свойство, для получения общей суммы заказа
        self.total_price = self.item.aggregate(Sum('price'))[
            'price__sum']        
        return self.total_price

    def __str__(self):
        return f"Заказ {self.pk}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
