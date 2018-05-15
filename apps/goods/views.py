from django.shortcuts import render
from goods.models import Goods
from django.views.generic.base import View

import json
# Create your views here.

class GoodsList(View):
    def get(self,request):
        json_list = []
        goods = Goods.objects.all()
        for good in goods:
            json_dist = {}
            json_dist['name'] = good.name
            json_dist['good_sn'] = good.good_sn
            json_list.append(json_dist)
        from django.http import HttpResponse
        return HttpResponse(json.dumps(json_list),content_type="application/json")