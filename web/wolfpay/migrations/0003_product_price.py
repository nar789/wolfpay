# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-31 02:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wolfpay', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]