# -*- coding: utf-8 -*-  
__author__ = 'style'
import xadmin
from users.models import UserProfile, VerifyCode


class UserProfileAdmin(object):
    search_fields = ['name', 'mobile']


class VerifyCodeAdmin(object):
    fields = ['code', 'add_time', 'mobile']
    search_fields = ['mobile']
    list_filter = ['code', 'add_time', 'mobile']

xadmin.site.register(VerifyCode, VerifyCodeAdmin)