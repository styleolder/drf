# -*- coding: utf-8 -*-  
__author__ = 'style'
from rest_framework import serializers
from goods.models import Goods, GoodCategory
from users.models import VerifyCode, UserProfile
import re
from datetime import datetime,timedelta

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


class GoodCategorySerializer2(serializers.ModelSerializer):
     sub_name = GoodCategorySerializer(many=True)
     class Meta:
        model = GoodCategory
        fields = "__all__"


class GoodCategorySerializer3(serializers.ModelSerializer):
     sub_name = GoodCategorySerializer(many=True)
     class Meta:
        model = GoodCategory
        fields = "__all__"

class GoodsSerializer2(serializers.ModelSerializer):
     category = GoodCategorySerializer()
     class Meta:
        model = Goods
        fields = "__all__"


class VerifyCodeSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=11)
    REG_MOBILE = "^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$"

    def validate_mobile(self, mobile):

        if UserProfile.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("手机用户已经存在")

        if not re.match(self.REG_MOBILE, mobile):
            raise serializers.ValidationError("手机号码错误")

        now = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)

        if VerifyCode.objects.filter(add_time__gt=now, mobile=mobile).count():
            raise serializers.ValidationError("时间间隔60s")
        return mobile

    class Meta:
        model = VerifyCode
        fields = "__all__"
