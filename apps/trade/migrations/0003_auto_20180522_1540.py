# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-22 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0002_auto_20180514_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingtrade',
            name='goods_num',
            field=models.IntegerField(),
        ),
    ]
