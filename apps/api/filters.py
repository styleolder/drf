# -*- coding: utf-8 -*-  
__author__ = 'style'
from goods.models import Goods
import django_filters


class ProFilter(django_filters.FilterSet):
    market_price_min = django_filters.NumberFilter(name='market_price', lookup_expr='gte')
    market_price_max = django_filters.NumberFilter(name='market_price', lookup_expr='lte')

    class Meta:
        model = Goods
        fields = ['market_price_min','market_price_max']