from django.db import models


class Discount(models.Model):
    """Модель скидки"""
    DURATION = (
        ("once", "ONCE"),
        ("forever", "FOREVER"),
        ("repeating", "REPEATING"),
    )
    name = models.CharField(max_length=20, unique=True,
                            verbose_name="Название купона")
    percent_off = models.IntegerField(
        verbose_name="Процент скидки")
    duration = models.CharField(
        max_length=20,
        choices=DURATION,
        default="once",
        verbose_name="Срок действия")

    def __str__(self) -> str:
        return f"{self.percent_off}%"

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"
