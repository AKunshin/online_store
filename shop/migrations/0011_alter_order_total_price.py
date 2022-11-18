# Generated by Django 4.1.1 on 2022-09-23 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_item_price_alter_order_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10, verbose_name='Итоговая сумма'),
        ),
    ]
