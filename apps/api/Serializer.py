# -*- coding: utf-8 -*-  
__author__ = 'style'
from rest_framework import serializers
from goods.models import Goods, GoodCategory


# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField()
#     good_sn = serializers.CharField()
#     good_front_image = serializers.ImageField()
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Goods.objects.create(**validated_data)


class GoodCategorySerializer(serializers.ModelSerializer):
     class Meta:
        model = GoodCategory
        fields = "__all__"


class GoodsSerializer2(serializers.ModelSerializer):
     category = GoodCategorySerializer()
     class Meta:
        model = Goods
        fields = "__all__"
