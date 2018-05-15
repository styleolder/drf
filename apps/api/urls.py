# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from views import GoodsViewSet

router = DefaultRouter()
router.register(r'goods', GoodsViewSet)
# Routers provide an easy way of automatically determining the URL conf.
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls()),
    url(r'^', include(router.urls)),
    ]