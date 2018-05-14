# -*- coding: utf-8 -*-  
__author__ = 'style'
import xadmin
from user_opration.models import UserFav, UserAddress


class UserFavAdmin(object):
    fields = ['user', 'add_time', 'goods']
    search_fields = ['user']
    list_filter = ['user', 'add_time', 'goods']


class UserAddressAdmin(object):
    fields = ['user', 'address', 'signer_name', 'signer_mobile', 'is_default', 'add_time']
    search_fields = ['user', 'signer_mobile']
    list_filter = ['user', 'address', 'signer_name', 'signer_mobile', 'is_default', 'add_time']


xadmin.site.register(UserFav, UserFavAdmin)
xadmin.site.register(UserAddress, UserAddressAdmin)