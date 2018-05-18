# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-16 17:39
from __future__ import unicode_literals

import DjangoUeditor.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='brand',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='goods.GoodsCategoryBrand'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='good_desc',
            field=DjangoUeditor.models.UEditorField(blank=True, default='', max_length=1024000000000L, verbose_name='\u5185\u5bb9'),
        ),
    ]