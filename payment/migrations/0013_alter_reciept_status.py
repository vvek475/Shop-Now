# Generated by Django 4.1.3 on 2022-12-23 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0012_rename_isdelieved_reciept_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reciept',
            name='status',
            field=models.CharField(choices=[('0', 'Order Placed'), ('1', 'Out For Delievery'), ('2', 'Delivered'), ('3', 'Refunded')], default='0', max_length=225),
        ),
    ]
