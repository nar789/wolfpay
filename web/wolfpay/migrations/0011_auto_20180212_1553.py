# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-02-12 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wolfpay', '0010_send_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='pid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='wolfpay.Product'),
        ),
    ]