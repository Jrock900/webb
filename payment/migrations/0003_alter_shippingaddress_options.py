# Generated by Django 5.0.3 on 2024-06-12 00:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_shippingadress_shippingaddress'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shippingaddress',
            options={'verbose_name_plural': 'Shipping Address'},
        ),
    ]
