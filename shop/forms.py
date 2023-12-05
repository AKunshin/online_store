from django import forms
from django.core.exceptions import ValidationError

from .models import Order
from payments.models import Discount


class OrderForm(forms.ModelForm):
    discounts = forms.CharField(
        max_length=20,
        required=False,
        label="Промокод",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Введите промокод...",
                "default": None,
            },
        ),
    )

    class Meta:
        model = Order
        fields = ("items", "discounts")
        widgets = {
            "items": forms.SelectMultiple(attrs={"class": "form-control"}),
        }

    def clean_discounts(self):
        discounts = self.cleaned_data.get("discounts")

        if not Discount.objects.filter(name=discounts) and discounts != None:
            raise ValidationError("Промокод не найден")
        discounts = Discount.objects.get(name=discounts)

        return discounts
