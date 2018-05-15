# -*- coding: utf-8 -*-
from goods.models import Goods
from django.views.generic.base import View

import json
# Create your views here.

class GoodsList(View):
    def get(self,request):
        goods = Goods.objects.all()
        from django.http import HttpResponse
        from django.core import serializers
        json_data = serializers.serialize("json", goods)
        return HttpResponse(json_data,content_type="application/json")