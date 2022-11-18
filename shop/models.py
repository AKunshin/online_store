from django.db import models
from django.db.models import Sum
from django.urls import reverse


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
    total_price = models.DecimalField(max_digits=10,
                                      decimal_places=2, null=True,
                                      default=1,
                                      verbose_name="Итоговая сумма")

    def save(self, *args, **kwargs):
        """Переопределение поля для общей стоимости заказа"""
        super().save(*args, **kwargs)
        self.total_price = self.item.all().aggregate(Sum('price'))[
            'price__sum']
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ {self.pk}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
