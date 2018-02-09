# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-04 04:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('wolfpay', '0004_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
