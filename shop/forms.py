from django import forms
from django.core.exceptions import ValidationError

from loguru import logger

from .models import Order
from payments.models import Discount


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("items", "discounts")
        widgets = {
            "items": forms.SelectMultiple(attrs={"class": "form-control"}),
            "discounts": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите промокод...",
                    "default": None,
                    "required": False,
                },
            ),
        }

    def clean_discounts(self):
        data = self.cleaned_data["discounts"]

        logger.debug(f"{data=}")

        if not Discount.objects.filter(name=data) and data != None:
            raise ValidationError("Промокод не найден")
        return data
