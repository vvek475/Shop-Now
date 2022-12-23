# Generated by Django 4.1.3 on 2022-11-30 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('price', models.IntegerField(default=1)),
                ('guarantee', models.IntegerField(blank=True, default=0, null=True)),
                ('refurbished', models.BooleanField(default=False)),
                ('seller', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('expireson', models.DateField(auto_now_add=True)),
                ('products', models.ManyToManyField(to='product.product')),
            ],
        ),
    ]
