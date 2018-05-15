# -*- coding: utf-8 -*-
from goods.models import Goods
from rest_framework.views import APIView
from rest_framework.response import Response
from .Serializer import GoodsSerializer


class GoodsListView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()
        serializer = GoodsSerializer(goods, many=True)
        return Response(serializer.data)