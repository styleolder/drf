# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from goods.models import Goods
# Create your models here.
from drf import settings


@python_2_unicode_compatible
class ShoppingTrade(models.Model):
    """
        购物车
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户", help_text="用户")
    goods = models.ForeignKey(Goods, verbose_name="商品", help_text="商品")
    goods_num = models.IntegerField(default=0, verbose_name="购买数量", help_text="购买数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", help_text="添加时间")

    class Meta:
        verbose_name = "购物车"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name
        # return "%s(%d)".format(self.goods.name, self.goods_num)


@python_2_unicode_compatible
class OrderInfo(models.Model):
    """
        订单信息
    """
    ORDER_STATUS = (
        ("success", "支付成功"),
        ("cancel", "取消支付"),
        ("wait", "等待支付")
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order_sn = models.CharField(max_length=100, verbose_name="订单编号", null=True, blank=True)
    trade_no = models.CharField(max_length=100, null=True, blank=True, verbose_name="第三方订单编号")
    pay_status = models.CharField(default="wait", max_length=10, choices=ORDER_STATUS, verbose_name="订单状态")
    pay_time = models.DateTimeField(null=True, blank=True, verbose_name="支付时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    address = models.CharField(max_length=200, verbose_name="地址")
    signer_name = models.CharField(max_length=50, verbose_name="收件人姓名")
    signer_mobile = models.CharField(max_length=11, verbose_name="收件人电话")
    bbs = models.CharField(max_length=50, verbose_name="订单留言", null=True, blank=True)

    class Meta:
        verbose_name = "订单信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn


@python_2_unicode_compatible
class OrderGoods(models.Model):
    """
        订单详情
    """
    order_sn = models.ForeignKey(OrderInfo)
    goods = models.ForeignKey(Goods)
    goods_num = models.IntegerField(default=0, verbose_name="商品数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "订单详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_sn.order_sn

