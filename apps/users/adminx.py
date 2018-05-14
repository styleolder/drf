# -*- coding: utf-8 -*-  
__author__ = 'style'
import xadmin
from users.models import VerifyCode,UserProfile


class UserProfileAdmin(object):
    pass


class VerifyCodeAdmin(object):
    fields = ['code', 'add_time', 'mobile']
    search_fields = ['mobile']
    list_filter = ['code', 'add_time', 'mobile']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)