# Generated by Django 4.1.3 on 2022-11-30 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_product_count_alter_product_guarantee_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='refurbished',
        ),
        migrations.CreateModel(
            name='Refurbished',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=1)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product')),
            ],
        ),
    ]