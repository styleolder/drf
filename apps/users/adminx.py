# -*- coding: utf-8 -*-  
__author__ = 'style'
import xadmin
from users.models import VerifyCode,UserProfile


class UserProfileAdmin(object):
    pass


class VerifyCodeAdmin(object):
    fields = ['code', 'add_time', 'mobile', 'code_type']
    search_fields = ['mobile']
    list_filter = ['code', 'add_time', 'mobile', 'code_type']


xadmin.site.register(VerifyCode, VerifyCodeAdmin)