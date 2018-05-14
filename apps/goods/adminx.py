# -*- coding: utf-8 -*-  
__author__ = 'style'
import xadmin
from xadmin import views
from goods.models import GoodCategory, Goods, GoodsCategoryBrand, GoodsImage, Banner

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GoodCategoryAdmin(object):
    fields = ['name', 'code', 'desc', 'category_type', 'parent_category', 'add_time', 'is_table']
    search_fields = ['name', 'code']
    list_filter = ['add_time']

    list_display = (
        'name',
        'code',
        'category_type',
        'parent_category',
        'add_time'
    )


class GoodsCategoryBrandAdmin(object):
    fields = ['name', 'desc', 'images', 'add_time']
    search_fields = ['name']
    list_filter = ['name', 'desc', 'images', 'add_time']


class GoodsAdmin(object):
    fields = ['name', 'good_sn', 'add_time']
    search_fields = ['name']
    list_filter = [
        "category",
        "name",
        "good_sn",
        "desc",
        "brand",
        "add_time",
        "click_num",
        "sold_num",
        "fav_num",
        "goods_num",
        "market_price",
        "shop_price",
        "good_desc",
        "ship_free",
        "good_front_image",
        "is_new",
        "is_hot"
    ]


class GoodsImageAdmin(object):
    fields = ['goods', 'image', 'add_time', 'index']
    search_fields = ['goods']
    list_filter = ['goods', 'image', 'add_time', 'index']


class BannerAdmin(object):
    fields = ['goods', 'image', 'index', 'add_time']
    list_filter = ['goods']
    search_fields = ['goods', 'image', 'index', 'add_time']


class GlobalSettings(object):
    site_title = u"styleShop"
    site_footer = u"styleShop"
    menu_style = "accordion"


xadmin.site.register(GoodCategory, GoodCategoryAdmin)
xadmin.site.register(GoodsCategoryBrand, GoodsCategoryBrandAdmin)
xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(GoodsImage, GoodsImageAdmin)


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)