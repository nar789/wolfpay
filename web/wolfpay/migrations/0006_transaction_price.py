# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-04 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wolfpay', '0005_transaction_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='price',
            field=models.IntegerField(null=True),
        ),
    ]