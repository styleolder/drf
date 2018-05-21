# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from views import GoodsViewSet, GoodCategoryViewSet, VerifyCodeViewSet, UserViewSet, UserFavViewSet

router = DefaultRouter()
router.register(r'goods', GoodsViewSet)
router.register(r'goodscategort', GoodCategoryViewSet)
router.register(r'verifycode', VerifyCodeViewSet)
router.register(r'UserViewSet', UserViewSet)
router.register(r'UserFav', UserFavViewSet)


# Routers provide an easy way of automatically determining the URL conf.
urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include_docs_urls()),
    url(r'^', include(router.urls)),
    ]