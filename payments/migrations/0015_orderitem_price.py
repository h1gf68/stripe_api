# Generated by Django 4.1.7 on 2023-02-25 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0014_remove_orderitem_price_alter_order_checkout_session'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
