# Generated by Django 5.0.2 on 2024-02-22 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bfr_login', '0003_remove_customer_referral_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='otp_fld',
            field=models.CharField(max_length=4),
        ),
    ]
