from django.contrib import admin
from .models import Item, Order
# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency', 'id']


admin.site.register(Order)

# @admin.register(Order)
# class Order(admin.ModelAdmin):
#     pass