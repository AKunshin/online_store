# Generated by Django 4.1.1 on 2022-11-19 05:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_remove_order_item_order_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
    ]
