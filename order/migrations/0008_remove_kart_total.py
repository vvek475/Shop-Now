# Generated by Django 4.1.3 on 2022-12-08 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_remove_order_mobile_order_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kart',
            name='total',
        ),
    ]
