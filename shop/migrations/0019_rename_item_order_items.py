# Generated by Django 4.1.1 on 2022-11-20 16:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_alter_order_item'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='item',
            new_name='items',
        ),
    ]
