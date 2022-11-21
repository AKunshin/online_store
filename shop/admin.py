from django.contrib import admin
from .models import Item, Order
# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency', 'id', 'get_rub_currency']


@admin.register(Order)
class Order(admin.ModelAdmin):
    list_display=['id','get_total_price']