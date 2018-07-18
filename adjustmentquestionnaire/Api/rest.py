import json
import random
from datetime import datetime

from  django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login,logout,authenticate
from django.conf.urls import url
from django.contrib.auth.models import User

from myApp.models import *
from Api.utils import method_not_allowed,json_response,params_error,not_authenticated
from Api.decorators import *
#定义初始类
class Rest(object):
    def __init__(self,name=None):
        self.name = name or self.__class__.__name__.lower()
    #定义一个方法，用于绑定到url中
    @csrf_exempt
    def enter(self,request,*arg,**kwargs):
       #取出客户端请求方法
       method = request.method
       #根据请求方法执行相应的处理函数
       if method == 'GET':
           #获取资源
           return self.get(request,*arg,**kwargs)
       elif method == 'POST':
           # 更新资源
           return self.post(request, *arg, **kwargs)
       elif method == 'PUT':
           # 添加资源
           return self.put(request, *arg, **kwargs)
       elif method == 'DELETE':
           #删除资源
           return self.delete(request, *arg, **kwargs)
       else:
           #不支持其他方法
        return HttpResponse('{"msg":"不支持该方法！"}')
    def get(self,request,*args,**kwargs):
        return  method_not_allowed()
    def post(self,request,*args,**kwargs):
        return  method_not_allowed()
    def put(self,request,*args,**kwargs):
        return  method_not_allowed()
    def delete(self,request,*args,**kwargs):
        return  method_not_allowed()

#路由注册
class Register(object):
    def __init__(self):
        self.resources = []
    def regist(self,resource):
        self.resources.append(resource)

    @property
    def urls(self):
        urlpatterns = [
            url(r'^{name}$'.format(name=resource.name),resource.enter)
            for resource in self.resources
        ]
        return urlpatterns

class SessionRest(Rest):
    #保存登录状态
    def put(self,request,*args,**kwargs):
            data = request.PUT
            username = data.get('username','')
            password = data.get("password",'')
            #查询数据库用户表
            user = authenticate(username=username,password=password)
            if user:
                #保存登陆状态
                login(request,user)
                return json_response(
                    {
                        "msg":"登录成功"
                    }
                )
            else:
                return params_error({
                    "msg":"用户名或者密码错误"
                })
        #删除登录状态
    def delete(self,request,*args,**kwargs):
        logout(request)
        return json_response({
            "msg":"退出登录"
        })
    #return json_response({"msg":"session put"})
    # def delete(self,request,*args,**kwargs):
    #         return json_response({"msg":"session delete"})

class UserRest(Rest):
    #查看用户/客户的具体信息
    def get(self,request,*args,**kwargs):
        #判断是否登录
        user = request.user
        if user.is_authenticated:
            #获取信息
            data = dict()
            if hasattr(user,'customer'):
                customer = user.customer
                data['name'] = customer.name
                data['qq'] = customer.email
                data['user'] = user.id
                data['category'] = 'customer'
            elif hasattr(user,'userinfo'):
                userinfo = user.userinfo
                data['name']= userinfo.name
                data['qq'] = userinfo.qq
                data['user'] = user.id
                data['category'] = 'userinfo'
            else:
                return json_response({
                })
        else:
            return not_authenticated()
        #return  json_response({"msg":"user get"})
        return json_response(data)

    #修改用户或者客户的信息
    def post(self,request,*args,**kwargs):
        #判断用户是否登陆（Django自带）
        data = request.POST
        user = request.user
        if user.is_authenticated:
            #是否拥有一个属性
            if hasattr(user,'customer'):
                customer = request.user.customer
                customer.name = data.get('name','')
                customer.email = data.get('email','')
                customer.save()

            elif hasattr(user,'userinfo'):
                userinfo = request.user.userinfo
                userinfo.name = data.get('name','')
                userinfo.qq = data.get('qq','')
                userinfo.save()

            else:
                return json_response({
                    "msg":"恭喜，更新成功！"
                })
        else:
            return not_authenticated()
        return json_response(
            {"msg":"更新成功"}
        )
        # print("post数据是：")
        # print(request.POST)
        # print('http 请求体是：')
        # print(request.body)
        # data = json.loads(request.body.decode())
        # print(data)
        #print(request.body.decode())
        #return  json_response({"msg":"user post"})

    #创建一个用户或者客户
    def put(self,request,*args,**kwargs):
        # print('请求的数据类型是：')
        # print(request.content_type)
        # print('http 请求体是：')
        # data = json.loads(request.body.decode())
        # print(data)
        data=request.PUT
        # print(data)
        username = data.get('username','')
        password = data.get('password','')
        ensure_password = data.get('ensure_password','')
        regist_code = data.get('regist_code',0)
        session_regist_code = request.session.get('regist_code',1)
        error = dict()
        if not username:
            error['username'] = "必须提供用户名"
        else:
            if User.objects.filter(username=username).count()>0:
                error['username'] = '用户名已存在'
        if len(password)<6:
            error['password'] = '密码不可少于六位'
        if password != ensure_password:
            error['ensure_password'] = '两次输入的密码不匹配'
        if regist_code != session_regist_code:
            error['regist_code'] = '验证码不匹配'
        if error:
            return  params_error(error)
        user = User()
        user.username = username
        user.set_password(password)
        user.save()

        #category = data.get('category','userinfo')
        category = data.get('category', 'customer')
        if category == 'userinfo':
            #创建普通用户
            user_obj = UserInfo()
            user_obj.name = ""
            user_obj.qq = ""
        else:
            #创建客户
            user_obj = Customer()
            user_obj.name = ""
            user_obj.email=""
        user_obj.user = user
        user_obj.save()
        #print(request.PUT) #{'username': 'user1', 'password': '123456'}
        return  json_response({"注册的id：":user.id})
        # return  json_response({"msg":"user put"})
# def Klass(object):
#         def __new__(cls, *args, **kwargs):
#             pass
#         def __init__(self):
#             pass
# obj = Klass()
# A = type('A',(object,),{})
# import random
class RegistCode(Rest):
    #select * from django_session;
    #import base64
    # base64.b64decode('NTRkNjMzMWQxNGVmMDlkZjliZDg4NWIzZDU3MzZlZGQ4NTRhMmE2ZDp7InJlZ2lzdF9jb2RlIjo3MTcxOX0=')
    def get(self,request,*args,**kwargs):
        #获取6位随机数字
        regist_code = random.randint(100000,1000000)
        request.session['regist_code'] = regist_code
        #返回随机数
        return json_response({
            "registe_code":regist_code
        })