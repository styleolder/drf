# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-23 22:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0013_auto_20180523_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordergoods',
            name='order_sn',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goods', to='trade.OrderInfo'),
        ),
    ]