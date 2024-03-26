# Generated by Django 5.0.2 on 2024-03-21 14:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfr_login', '0004_alter_customer_otp_fld'),
        ('manage_order', '0006_alter_ordered_items_status_cancelledorder'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderReturns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(auto_now_add=True, null=True)),
                ('pickup_date', models.DateField(blank=True, null=True)),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='manage_order.ordered_items')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bfr_login.customer')),
            ],
        ),
    ]
