from django.db import models


class Item(models.Model):
    """Модель товара"""
    CURRENCY = (
        ("rub", 'RUB'),
        ("usd", 'USD'),
    )
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Цена")
    currency = models.CharField(
        max_length=3, choices=CURRENCY, default="rub", verbose_name="Валюта"
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Товар"
        verbose_name_plural="Товары"


# class Order(models.Model):
#     item = models.ForeignKey()

