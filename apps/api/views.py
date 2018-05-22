# -*- coding: utf-8 -*-
from goods.models import Goods, GoodCategory
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializer import GoodsSerializer2, GoodCategorySerializer3, VerifyCodeSerializer,\
    UserSerializer, UserFavSerializer, UserProfileSerializer,UserFavReSerializer
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
from user_opration.models import UserFav
from random import choice
# class GoodsListView(APIView):
# """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         goods = Goods.objects.all()
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


class UserFavViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
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

    authentication_classes = (TokenAuthentication,)
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
