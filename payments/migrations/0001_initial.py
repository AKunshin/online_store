# Generated by Django 4.1.1 on 2022-11-25 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Название купона')),
                ('percent_off', models.IntegerField(max_length=3, verbose_name='Процент скидки')),
                ('duration', models.CharField(choices=[('once', 'ONCE'), ('forever', 'FOREVER'), ('repeating', 'REPEATING')], default='once', max_length=20, verbose_name='Срок действия')),
            ],
        ),
    ]
