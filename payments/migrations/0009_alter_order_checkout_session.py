# Generated by Django 4.1.7 on 2023-02-25 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0008_alter_order_checkout_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='checkout_session',
            field=models.CharField(default='test', max_length=200, null=True),
        ),
    ]
