from django.db import models


class Discount(models.Model):
    """Модель скидки"""

    DURATION = (
        ("once", "ONCE"),
        ("forever", "FOREVER"),
        ("repeating", "REPEATING"),
    )
    name = models.CharField(max_length=20, unique=True, verbose_name="Название купона")
    percent_off = models.IntegerField(verbose_name="Процент скидки")
    duration = models.CharField(
        max_length=20, choices=DURATION, default="once", verbose_name="Срок действия"
    )

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self) -> str:
        return self.name
