from statistics import mode
from tabnanny import verbose
from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=150, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Цена")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Товар"
        verbose_name_plural="Товары"