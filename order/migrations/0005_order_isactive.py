# Generated by Django 4.1.3 on 2022-12-06 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_kart_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='isactive',
            field=models.BooleanField(default=False),
        ),
    ]