# -*- coding: utf-8 -*-
from goods.models import Goods
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializer import GoodsSerializer2
from rest_framework import status
from rest_framework import mixins, generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProFilter


# class GoodsListView(APIView):
#     """
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


class GoodsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = GoodsSerializer2
    queryset = Goods.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # filter_fields = ('name', 'good_sn')
    filter_class = ProFilter

    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     market_price = self.request.query_params.get("market_price", 0)
    #     if market_price:
    #         queryset = queryset.filter(market_price__gt=market_price)
    #     return queryset