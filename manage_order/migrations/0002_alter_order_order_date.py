# Generated by Django 5.0.2 on 2024-03-08 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
