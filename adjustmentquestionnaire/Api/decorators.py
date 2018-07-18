from Api.utils import *

#登录用户是客户,只能在类中使用
def  customer_required(func):
    def _wrapper(self,request,*args,**kwargs):
        user = request.user
        if not user.is_authenticated:
            return not_authenticated()
        #如果不是客户则禁止登录
        if not hasattr(user,'customer'):
            return permission_denied()
        return func(self,request,*args,**kwargs)
    return _wrapper

#登录用户是普通用户,只能在类中使用
def userinfo_required(func):
    def _wrapper(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return not_authenticated()
    # 如果不是普通用户则禁止登录
        if not hasattr(user, 'userinfo'):
            return permission_denied()
        return func(self, request, *args, **kwargs)
    return _wrapper

#登录用户是管理员,只能在类中使用
def superuser_required(func):
    def _wrapper(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return not_authenticated()
        return func(self, request, *args, **kwargs)
    return _wrapper