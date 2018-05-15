# -*- coding: utf-8 -*-  
__author__ = 'style'
from rest_framework import serializers


class GoodsSerializer(serializers.Serializer):
    name = serializers.CharField()
    good_sn = serializers.CharField()