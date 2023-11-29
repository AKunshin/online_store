from decimal import Decimal

from django.db import models
from django.urls import reverse

from payments.service import exchange_to_rubles, get_total_price
from payments.models import Discount


class Item(models.Model):
    """Модель товара"""

    CURRENCY = (
        ("rub", "RUB"),
        ("usd", "USD"),
    )
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=1, verbose_name="Цена"
    )
    currency = models.CharField(
        max_length=3, choices=CURRENCY, default="rub", verbose_name="Валюта"
    )

    @property
    def get_rub_currency(self) -> Decimal:
        """Свойство, для конвертации стоимости в RUB по курсу ЦБ"""
        if self.currency == "usd":
            self.price_rub = self.price * exchange_to_rubles()
        else:
            self.price_rub = self.price
        return self.price_rub.quantize(Decimal("1.00"))

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-id"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Обратное построение адресов"""
        return reverse("view_item", kwargs={"pk": self.pk})


class Order(models.Model):
    """Модель заказа товара"""

    items = models.ManyToManyField(Item, verbose_name="Товары")
    discounts = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Скидка",
    )

    @property
    def get_total_price(self) -> Decimal:
        """Свойство, для получения общей суммы заказа"""
        if self.discounts:
            self.total_price = get_total_price(self.items.all()) * Decimal(
                (100 - self.discounts.percent_off) / 100
            )
        else:
            self.total_price = get_total_price(self.items.all())
        return self.total_price.quantize(Decimal("1.00"))

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-id"]

    def __str__(self):
        return f"Заказ {self.pk}"

    def get_absolute_url(self):
        return reverse("view_order", kwargs={"pk": self.pk})
