# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-23 12:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0007_auto_20180523_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='trade_no',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='\u7b2c\u4e09\u65b9\u8ba2\u5355\u7f16\u53f7'),
        ),
    ]
