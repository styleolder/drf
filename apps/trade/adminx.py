# -*- coding: utf-8 -*-  
__author__ = 'style'
import xadmin
from trade.models import ShoppingTrade, OrderInfo, OrderGoods


class ShoppingTradeAdmin(object):
    fields = ['user', 'goods', 'goods_num', 'add_time']
    search_fields = ['goods', 'goods_num', 'add_time']
    list_filter = ['user', 'goods', 'goods_num', 'add_time']


class OrderInfoAdmin(object):
    fields = [
        'user',
        'order_sn',
        'trade_no',
        'pay_status',
        'pay_time',
        'add_time',
        'address',
        'signer_name',
        'signer_mobile',
        'bbs'
    ]
    search_fields = ['order_sn']
    list_filter = [
        'user',
        'order_sn',
        'trade_no',
        'pay_status',
        'pay_time',
        'add_time',
        'address',
        'signer_name',
        'signer_mobile',
        'bbs'
    ]


class OrderGoodsAdmin(object):
    fields = ['good_sn', 'goods', 'goods_num', 'add_time']
    search_fields = ['add_time', 'good_sn', 'goods']
    list_filter = ['good_sn', 'goods', 'goods_num', 'add_time']

xadmin.site.register(ShoppingTrade, ShoppingTradeAdmin)
xadmin.site.register(OrderInfo, OrderInfoAdmin)
xadmin.site.register(OrderGoods, OrderGoodsAdmin)
