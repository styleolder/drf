# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


@python_2_unicode_compatible
class UserProfile(AbstractUser):
    USER_CHOICES = (
        ("0", u"男"),
        ("1", u"女")
    )
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="昵称")
    birthday = models.DateField(max_length=10, null=True, blank=True, verbose_name="生日")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机")
    gender = models.CharField(max_length=10, choices=USER_CHOICES, verbose_name="性别")
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name="邮箱")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class VerifyCode(models.Model):
    """
        手机验证码
    """
    code = models.CharField(max_length=6, verbose_name="验证码")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机")

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.mobile

