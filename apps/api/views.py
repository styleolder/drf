# -*- coding: utf-8 -*-
from goods.models import Goods, GoodCategory
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializer import GoodsSerializer2, GoodCategorySerializer3, VerifyCodeSerializer, UserSerializer, UserFavSerializer
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProFilter
from rest_framework import filters
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
    serializer_class = GoodsSerializer2
    queryset = Goods.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # filter_fields = ('name', 'good_sn')
    filter_class = ProFilter
    search_fields = ("name",)
    order_fields = ("good_sn",)


class UserFavViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserFavSerializer
    queryset = UserFav.objects.all()


class GoodCategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = GoodCategorySerializer3
    queryset = GoodCategory.objects.all()
    # queryset = GoodCategory.objects.filter(category_type="1")
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    order_fields = ("code",)
    from rest_framework.permissions import IsAuthenticated
    permission_classes = (
        IsAuthenticated,
    )
    authentication_classes = (TokenAuthentication,)
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

    def perform_create(self, serializer):
        return serializer.save()