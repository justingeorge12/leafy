# Generated by Django 5.0.2 on 2024-02-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('join_date', models.DateField()),
                ('phone', models.PositiveIntegerField()),
                ('is_verified', models.BooleanField(default=False)),
                ('is_blocked', models.BooleanField(default=False)),
                ('otp_secret', models.CharField(max_length=100)),
                ('otp_fld', models.CharField()),
                ('referral_link', models.CharField(max_length=255, unique=True)),
            ],
        ),
    ]
