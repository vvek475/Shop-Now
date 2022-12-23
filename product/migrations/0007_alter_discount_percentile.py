# Generated by Django 4.1.3 on 2022-12-01 11:43

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_discount_expireson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='percentile',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
