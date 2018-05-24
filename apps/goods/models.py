# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from DjangoUeditor.models import UEditorField
from datetime import datetime
# Create your models here.


@python_2_unicode_compatible
class GoodCategory(models.Model):
    """
        商品分类
    """
    CATEGORY_CHOICES = (
        ('1', u"一级分类"),
        ('2', u"二级分类"),
        ('3', u"三级分类")
    )
    name = models.CharField(default="", max_length=50, verbose_name="商品类名")
    code = models.CharField(default="", max_length=100, verbose_name="类名编码")
    desc = models.TextField(default="", verbose_name="类别描述")
    category_type = models.CharField(max_length=10, choices=CATEGORY_CHOICES, verbose_name="分类级别")
    parent_category = models.ForeignKey('self', blank=True, null=True, related_name="sub_name", verbose_name="分类")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_table = models.BooleanField(default=False, verbose_name="是否为导航栏")

    class Meta:
        verbose_name = "商品分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class GoodsCategoryBrand(models.Model):
    """
        推荐商品
    """
    name = models.CharField(default="", max_length=50, verbose_name="品牌名称")
    desc = models.TextField(default="", verbose_name="品牌描述")
    images = models.ImageField(max_length=1000, upload_to="brand/images/", verbose_name="图片")
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = "品牌"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Goods(models.Model):
    """
        商品信息
    """
    category = models.ForeignKey(GoodCategory, verbose_name="商品类别")
    name = models.CharField(default="", max_length=50, verbose_name="商品名称")
    good_sn = models.CharField(default="", max_length=100, verbose_name="商品编码")
    desc = models.TextField(default="", verbose_name="商品描述")
    brand = models.ForeignKey(GoodsCategoryBrand, default=None, blank=True, null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    click_num = models.IntegerField(default=0, verbose_name="商品点击数")
    sold_num = models.IntegerField(default=0, verbose_name="商品售卖数")
    fav_num = models.IntegerField(default=0, verbose_name="商品关注数")
    goods_num = models.IntegerField(default=0, verbose_name="商品库存数")
    market_price = models.FloatField(default=0.0, verbose_name="市场价格")
    shop_price = models.FloatField(default=0.0, verbose_name="商品价格")
    good_desc = UEditorField('内容', height=300, width=800,max_length=1024000000000,
                           default=u'', blank=True, imagePath="images/",
                           toolbars='besttome', filePath='files/')
    ship_free = models.BooleanField(default=True, verbose_name="是否承担运费")
    good_front_image = models.ImageField(upload_to="", verbose_name="封面图片")
    is_new = models.BooleanField(default=False, verbose_name="是否为新品")
    is_hot = models.BooleanField(default=False, verbose_name="是否为热卖商品")

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class GoodsImage(models.Model):
    """
        商品轮播图
    """
    goods = models.ForeignKey(Goods, related_name="goodsimage")
    image = models.ImageField(upload_to="", verbose_name="轮播图", blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    index = models.IntegerField(default=100, verbose_name="轮播图权重")

    class Meta:
        verbose_name = "商品轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


@python_2_unicode_compatible
class Banner(models.Model):
    """
        首页轮播图
    """
    goods = models.ForeignKey(Goods)
    image = models.ImageField(upload_to="", verbose_name="轮播图", blank=True)
    index = models.IntegerField(default=100, verbose_name="轮播图权重")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    desc = models.CharField(default="", blank=True, null=True, max_length=50, verbose_name="描述信息")

    class Meta:
        verbose_name = "首页轮播图"
        verbose_name_plural = verbose_name
        ordering = ["index", "-add_time"]

    def __str__(self):
        return self.goods.name
