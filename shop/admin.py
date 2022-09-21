from django.contrib import admin
from .models import Item
# Register your models here.

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency', 'id']

# @admin.register(Order)
# class Order(admin.ModelAdmin):
#     pass