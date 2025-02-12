# Generated by Django 5.0.2 on 2024-02-14 17:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category_management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('image1', models.ImageField(upload_to='images/')),
                ('image2', models.ImageField(upload_to='images/')),
                ('image3', models.ImageField(upload_to='images/')),
                ('image4', models.ImageField(upload_to='images/')),
                ('is_listed', models.BooleanField(default=True)),
                ('og_price', models.IntegerField(null=0)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category_management.category')),
            ],
        ),
    ]
