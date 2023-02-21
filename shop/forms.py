from django import forms
from django.core.exceptions import ValidationError

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["items", "discounts"]

        widgets = {
            "items": forms.SelectMultiple(attrs={"class": "form-control"}),
            "discounts": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Введите промокод...",
            }),
        }

    def clean_discounts(self):
        data = self.cleaned_data["discounts"]
        if not Order.objects.filter(discounts=data):
            raise ValidationError("Промокод не найден")
        
        return data
    
