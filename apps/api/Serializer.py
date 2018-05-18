# -*- coding: utf-8 -*-  
__author__ = 'style'
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from goods.models import Goods, GoodCategory
from users.models import VerifyCode, UserProfile

import re
from datetime import datetime, timedelta

# class GoodsSerializer(serializers.Serializer):
# name = serializers.CharField()
# good_sn = serializers.CharField()
# good_front_image = serializers.ImageField()
#
# def create(self, validated_data):
# """
# Create and return a new `Snippet` instance, given the validated data.
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


#自定义用户输入验证
class VerifyCodeSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=11)
    add_time = serializers.DateTimeField(read_only=True)
    code = serializers.CharField(read_only=True)

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


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(allow_blank=False, required=True,
                                     validators=[
                                         UniqueValidator(queryset=UserProfile.objects.all(), message="用户已经存在")])
    code = serializers.CharField(max_length=6, required=True, min_length=6, help_text="验证码", write_only=True)

    def validate_code(self, code):
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]
                        ).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            now = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
            if last_record.add_time > now:
                raise serializers.ValidationError("验证码已经过期，请重新获取")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = UserProfile
        fields = ('username', 'mobile', 'code')
