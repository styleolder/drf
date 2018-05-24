# -*- coding: utf-8 -*-
from goods.models import Goods, GoodCategory
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from .Serializer import GoodsSerializer2, GoodCategorySerializer3, \
    VerifyCodeSerializer, UserSerializer, \
    UserFavSerializer, UserProfileSerializer, \
    UserFavReSerializer, \
    ShoppingTradeSerializer, \
    ShoppingTradeReSerializer, OrderInfoSerializer,\
    UserAddressSerializer, OrderInfoReSerializer,\
    BannerSerializer, IndexGoodCategorySerializer

from rest_framework import status
from rest_framework import mixins, generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProFilter
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# 添加token认证
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from users.models import UserProfile, VerifyCode
from user_opration.models import UserFav, UserAddress
from trade.models import ShoppingTrade, OrderInfo, OrderGoods
from goods.models import Banner

from random import choice
# class GoodsListView(APIView):
# """
# List all snippets, or create a new snippet.
# """
# def get(self, request, format=None):
# goods = Goods.objects.all()
#         serializer = GoodsSerializer2(goods, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = GoodsSerializer2(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class GoodsListView(mixins.ListModelMixin, mixins.RetrieveModelMixin,generics.GenericAPIView):
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer2
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


class GoodsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        获取商品详细信息
    """
    serializer_class = GoodsSerializer2
    queryset = Goods.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'good_sn')
    filter_class = ProFilter
    search_fields = ("name",)
    order_fields = ("good_sn",)


class UserFavViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
        用户收藏信息接口
    """
    serializer_class = UserFavSerializer
    queryset = UserFav.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly,
    )
    #设置单条检索的索引
    lookup_field = "goods_id"

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavReSerializer
        elif self.action == "create":
            return UserFavSerializer
        return UserFavSerializer

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


class GoodCategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        商品分类
    """
    serializer_class = GoodCategorySerializer3
    queryset = GoodCategory.objects.all()
    # queryset = GoodCategory.objects.filter(category_type="1")
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    order_fields = ("code",)

    # authentication_classes = (TokenAuthentication,)
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    permission_classes = (
        IsAuthenticated,
    )
    # from rest_framework.authtoken.models import Token
    # from users.models import UserProfile
    # for user in UserProfile.objects.all():
    #     Token.objects.create(user=user)
    #     print user.username, Token.key
    #     print "======================="
    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     market_price = self.request.query_params.get("market_price", 0)
    #     if market_price:
    #         queryset = queryset.filter(market_price__gt=market_price)
    #     return queryset


class VerifyCodeViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
        手机验证码
    """
    serializer_class = VerifyCodeSerializer
    queryset = VerifyCode.objects.all()
    # queryset = GoodCategory.objects.filter(category_type="1")
    # filter_backends = (DjangoFilterBackend,  filters.SearchFilter,filters.OrderingFilter)
    # order_fields = ("-add_time",)
    # search_fields = ("mobile",)
    authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)

    #自定义create方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile"]
        print mobile
        code_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        code = []
        for i in range(6):
            code.append(choice(code_list))
        code = "".join(code)
        print code
        verifycode = VerifyCode(code=code, mobile=mobile)
        verifycode.save()
        return Response(
            {
                "mobile": mobile,
                "code": code
            }, status=status.HTTP_201_CREATED)


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
        用户短信注册
    """
    serializer_class = UserSerializer
    queryset = UserProfile.objects.all()
    # authentication_classes = (TokenAuthentication,)
    # queryset = GoodCategory.objects.filter(category_type="1")
    # filter_backends = (DjangoFilterBackend,  filters.SearchFilter,filters.OrderingFilter)
    # order_fields = ("-add_time",)
    # search_fields = ("mobile",)
    # authentication_classes = (TokenAuthentication, BasicAuthentication, SessionAuthentication)
    # 自定义用户返回信息，返回数据里添加token
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        payload = jwt_payload_handler(user)
        serializer.data["token"] = jwt_encode_handler(payload)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()


class UserProfileViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
        用户个人信息
    """
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, SessionAuthentication,)

    #动态加载Serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserProfileSerializer
        elif self.action == "create":
            return UserSerializer
        return UserProfileSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    #默认ID返回，只会返回当前登录用户的信息
    def get_object(self):
        return self.request.user


class ShoppingTradeViewSet(viewsets.ModelViewSet):
    """
        购物车
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly
    )
    lookup_field = "goods_id"
    #首先会验证queryset，然后才会重写
    queryset = ShoppingTrade.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ShoppingTradeReSerializer
        return ShoppingTradeSerializer

    #重写queryset
    def get_queryset(self):
        return ShoppingTrade.objects.filter(user=self.request.user)


class OrderInfoSerializerViewSet(viewsets.ModelViewSet):
    """
        订单信息
    """
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly
    )
    #首先会验证queryset，然后才会重写
    queryset = OrderInfo.objects.all()
    #动态获取serializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderInfoReSerializer
        return OrderInfoSerializer
    #重写queryset

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)
    #可以从ViewSet中补充字段，但是一般都是在Serializer中自动填充的
    # def generate_order_sn(self):
    #     #以下为自己实现的时间戳，只精确到秒
    #     # from random import choice
    #     # import time
    #     # base_str = "zxcvbnmlkjhgfdsaqwertyuiopQWERTYUIOPASDFGHJKLZXCVBNM1234567890"
    #     # result = [int(time.time()), self.request.user.id]
    #     # for i in range(num):
    #     #     result.append(choice(base_str))
    #     # order_sn = "".join(result)
    #     # return order_sn
    #     from time import strftime
    #     import random
    #     #order_sn总长度为:时间戳12位，随机数字2位，用户ID取后4位 总计18位
    #     user_id = self.request.user.id
    #     if len(str(user_id) > 4):
    #         user_id = str(user_id)[:-4]
    #     else:
    #         user_id = str(user_id).zfill(4)
    #     order_sn = "{time_str}{user}{random_str}".format(time_str=strftime("%Y%m%d%H%M%S"), user=user_id,
    #                                                      random_str=random.randint(10, 99))
    #     return order_sn
    #
    # def perform_create(self, serializer):
    #     serializer.validated_data["order_sn"] = self.generate_order_sn()
    #     return serializer.save()

    def perform_create(self, serializer):
        shop_carts = ShoppingTrade.objects.filter(user=self.request.user)
        if shop_carts:
            order = serializer.save()
            for shop_cart in shop_carts:
                ordergood = OrderGoods()
                ordergood.goods = shop_cart.goods
                ordergood.goods_num = shop_cart.goods_num
                ordergood.order_sn = order
                ordergood.save()

                shop_cart.delete()
            return order
        else:
            raise serializers.ValidationError("没有需要购买的商品")


class UserAddressViewSet(viewsets.ModelViewSet):
    """
        订单信息
    """
    serializer_class = UserAddressSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (
        IsAuthenticated,
        IsOwnerOrReadOnly
    )

    #首先会验证queryset，然后才会重写
    queryset = UserAddress.objects.all()

    #重写queryset
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        address_default = UserAddress.objects.filter(user=self.request.user, is_default=True)
        user_address = UserAddress.objects.filter(user=self.request.user)
        if serializer.validated_data['is_default']:
            if user_address.count() >= 5:
                raise serializers.ValidationError("添加地址最多为5个")
            elif address_default.count() >= 1:
                    address_default.update(is_default=False)

        return serializer.save()


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        首页轮播图
    """
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()


class IndexGoodCategoryViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    """
        分类商品显示
    """
    serializer_class = IndexGoodCategorySerializer
    queryset = GoodCategory.objects.all()