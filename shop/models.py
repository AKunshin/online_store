from decimal import Decimal
from django.db import models
from django.urls import reverse
from payments.service import exchange_to_rubles, get_total_price


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
    def get_rub_currency(self):
    # Свойство, для конвертации стоимости в RUB по курсу ЦБ    
        if self.currency == "USD":
            self.price_rub = self.price * round(exchange_to_rubles(), 2)
            return self.price_rub
        else:
            self.price_rub = self.price
            return self.price_rub

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
    items = models.ManyToManyField(Item,
                                  verbose_name="Товары")

    def get_absolute_url(self):
        return reverse("view_order", kwargs={"pk": self.pk})

    @property
    def get_total_price(self):
        # Свойство, для получения общей суммы заказа
        self.total_price = get_total_price(self.items.all())
        return self.total_price


    def __str__(self):
        return f"Заказ {self.pk}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-id']
