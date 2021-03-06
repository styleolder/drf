# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-23 12:01
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0006_auto_20180523_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='pay_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u652f\u4ed8\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='shoppingtrade',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, help_text='\u6dfb\u52a0\u65f6\u95f4', verbose_name='\u6dfb\u52a0\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='shoppingtrade',
            name='goods',
            field=models.ForeignKey(help_text='\u5546\u54c1', on_delete=django.db.models.deletion.CASCADE, to='goods.Goods', verbose_name='\u5546\u54c1'),
        ),
        migrations.AlterField(
            model_name='shoppingtrade',
            name='goods_num',
            field=models.IntegerField(default=0, help_text='\u8d2d\u4e70\u6570\u91cf', verbose_name='\u8d2d\u4e70\u6570\u91cf'),
        ),
        migrations.AlterField(
            model_name='shoppingtrade',
            name='user',
            field=models.ForeignKey(help_text='\u7528\u6237', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237'),
        ),
    ]
