# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-18 23:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_verifycode_code_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('0', '\u7537'), ('1', '\u5973')], default='0', max_length=10, verbose_name='\u6027\u522b'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u6635\u79f0'),
        ),
    ]
