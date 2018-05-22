# -*- coding: utf-8 -*-  
__author__ = 'style'
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from goods.models import Goods, GoodCategory, GoodsImage
from users.models import VerifyCode, UserProfile
from user_opration.models import UserFav
from rest_framework.validators import UniqueTogetherValidator

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
# """
# return Goods.objects.create(**validated_data)
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


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image", "index", "add_time")


class GoodsSerializer2(serializers.ModelSerializer):
    category = GoodCategorySerializer()
    goodsimage = GoodsImageSerializer(many=True)

    class Meta:
        model = Goods
        fields = "__all__"


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        fields = ("user", "goods", "id")
        #增加联合验证，保证一个用户收藏同种商品只有一次
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="已经收藏"
            )
        ]


class UserFavReSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer2()

    class Meta:
        model = UserFav
        fields = ("goods", "id")
        #增加联合验证，保证一个用户收藏同种商品只有一次
# 自定义用户输入验证


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
    username = serializers.CharField(allow_blank=False, required=True, label="用户名",
                                     validators=[
                                         UniqueValidator(queryset=UserProfile.objects.all(), message="用户已经存在")])
    code = serializers.CharField(max_length=6, required=True, min_length=6, help_text="验证码", write_only=True,
                                 label="手机短信验证码")
    password = serializers.CharField(
        style={
            'input_type': 'password'
        },
        min_length=6,
        max_length=12,
        label="密码",
        write_only=True,
    )

    # 保存model的时候进行值的更新
    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    #取值验证
    def validate_code(self, code):
        reg_num = "[0-9]{6}"
        if not re.match(reg_num, code):
            raise serializers.ValidationError("验证码格式错误")
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if verify_records:
            last_record = verify_records[0]
            now = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")
            if last_record.add_time > now:
                raise serializers.ValidationError("验证码已经过期，请重新获取")
        else:
            raise serializers.ValidationError("验证码错误")

    #整体的值验证，所有的值已dict的形式存储在attrs中
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    #设置关联的model与需要操作的字段
    class Meta:
        model = UserProfile
        fields = ('username', 'mobile', 'code', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("username","mobile","birthday","gender","email")