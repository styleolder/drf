# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from datetime import datetime
from django.db import models
from goods.models import Goods
from django.contrib.auth import get_user_model
# Create your models here.
from drf import settings
#User = get_user_model()


@python_2_unicode_compatible
class UserFav(models.Model):
    """
        用户收藏
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    goods = models.ForeignKey(Goods, related_name="goods", help_text="商品ID")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name
        #增加联合验证，保证一个用户收藏同种商品只有一次
        # unique_together = ("user", "goods")

    def __str__(self):
        return self.user.username


@python_2_unicode_compatible
class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    address = models.CharField(max_length=200, verbose_name="地址")
    signer_name = models.CharField(max_length=50, verbose_name="收件人姓名")
    signer_mobile = models.CharField(max_length=11, verbose_name="收件人电话")
    is_default = models.BooleanField(default=False, verbose_name="设置为默认收货地址")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "收货地址"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user
