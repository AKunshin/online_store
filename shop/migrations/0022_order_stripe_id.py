# Generated by Django 4.1.1 on 2023-12-01 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0021_order_discounts'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
