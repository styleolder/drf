# -*- coding: utf-8 -*-  
__author__ = 'style'
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from goods.models import Goods, GoodCategory, GoodsImage
from users.models import VerifyCode, UserProfile
from user_opration.models import UserFav, UserAddress
from trade.models import ShoppingTrade, OrderInfo
from rest_framework.validators import UniqueTogetherValidator

import re
from datetime import datetime, timedelta
from time import strftime
import random
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
        # 增加联合验证，保证一个用户收藏同种商品只有一次
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
        # 增加联合验证，保证一个用户收藏同种商品只有一次


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

    # 取值验证
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

    # 整体的值验证，所有的值已dict的形式存储在attrs中
    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    # 设置关联的model与需要操作的字段
    class Meta:
        model = UserProfile
        fields = ('username', 'mobile', 'code', 'password')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("username", "mobile", "birthday", "gender", "email")


class ShoppingTradeSerializer(serializers.Serializer):
    """
        自定义Serializer
    """
    # 自动填充请求数据的用户，会被数据保存到self.context['request']中
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    goods_num = serializers.IntegerField(min_value=1, required=True, error_messages={
        "min_value": "商品数据大于1",
        "required": "此商品已经存在"
    })
    goods = serializers.PrimaryKeyRelatedField(queryset=Goods.objects.all(), required=True)

    # 自定serializer的create方法
    def create(self, validated_data):
        # 获取当前用户从serializers.HiddenField(
        #serializers.CurrentUserDefault()
        #)中得到
        user = self.context['request'].user
        #validated_data 是上面定义的model form的dict
        goods_num = validated_data['goods_num']
        #goods由于是外键的原因，其实goods是一个对象
        goods = validated_data['goods']
        #保存购物车有2中可能，1.没有此种商品，自动创建对象 2.有此种商品，
        existed = ShoppingTrade.objects.filter(user=user, goods=goods)
        if existed:
            existed = existed[0]
            existed.goods_num += goods_num
            existed.save()
        else:
            existed = ShoppingTrade.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        instance.goods_num = validated_data["goods_num"]
        instance.save()
        return instance


class ShoppingTradeReSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer2(many=False)

    class Meta:
        model = ShoppingTrade
        fields = "__all__"


class OrderInfoReSerializer(serializers.ModelSerializer):
    #todo
    goods = ShoppingTradeReSerializer(many=False)

    class Meta:
        model = OrderInfo
        fields = "__all__"


class OrderInfoSerializer(serializers.ModelSerializer):
    #自动填充user
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    # order_sn总长度为:时间戳12位，随机数字2位，用户ID取后4位 总计18位
    order_sn = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True)
    pay_status = serializers.CharField(read_only=True)

    def generate_order_sn(self):
        user_id = self.context["request"].user.id
        if len(str(user_id)) > 4:
            user_id = str(user_id)[:-4]
        else:
            user_id = str(user_id).zfill(4)

        order_sn = "{time_str}{user}{random_str}".format(time_str=strftime("%Y%m%d%H%M%S"), user=user_id,
                                                         random_str=random.randint(10, 99))
        return order_sn

    def validate(self, attrs):
        attrs["order_sn"] = self.generate_order_sn()
        if attrs["address"] == "" and attrs["signer_name"] == "" and attrs["signer_mobile"] == "":
            default_address = UserAddress.objects.filter(user=self.context["request"].user, is_default=True)
            if default_address.count() == 1:
                attrs["address"] = default_address[0].address
                attrs["signer_name"] = default_address[0].signer_name
                attrs["signer_mobile"] = default_address[0].signer_mobile
            else:
                raise serializers.ValidationError("请先填写默认的收货信息 or 输入完整的收货信息")
        elif attrs["address"] == "" or attrs["signer_name"] == "" or attrs["signer_mobile"] == "":
            raise serializers.ValidationError("请检查收货信息的完整性")
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"


class UserAddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = UserAddress
        fields = "__all__"