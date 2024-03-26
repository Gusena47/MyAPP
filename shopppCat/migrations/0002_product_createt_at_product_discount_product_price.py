# Generated by Django 5.0 on 2023-12-29 20:28

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopppCat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='createt_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='discount',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]