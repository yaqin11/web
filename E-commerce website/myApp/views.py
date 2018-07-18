from django.shortcuts import render,HttpResponse,redirect
from myApp.models import Slideshow,MainDescription,Product,CategorieGroup,ChildGroup,User,Address,Cart,Order
from myApp.serializers import MainDescriptionSerializer,SlidershowSerializer,ProductSerializer
from myApp.permissions import IsOwnerOrReadOnly
#from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from myApp.sms import send_sms
from django.http import JsonResponse
import uuid
# Create your views here.

#首页
def home(request):
    #获取轮播图数据
    slideList = Slideshow.objects.all()
    #获取5大模块数据
    mainList = MainDescription.objects.all()
    for item in mainList:
        products = Product.objects.filter(categoryId=item.categoryId)
        item.product1 = products.get(productId=item.product1)
        item.product2 = products.get(productId=item.product2)
        item.product3 = products.get(productId=item.product3)
    return render(request,"home/home.html",{"slideList":slideList,"mainList":mainList})

def market(request,gid,cid,sid):
    #左侧分组信息
    leftCategorieList = CategorieGroup.objects.all()
    # 获取分组商品的信息
    products = Product.objects.filter(categoryId=gid)
    #获取子类数据
    if cid != "0":
        products = products.filter(childId=cid)
    #获取子组信息
    childs = ChildGroup.objects.filter(categorie__categorieId=gid)
    #排序
    if sid == "1":
        pass
    elif sid == "2":
        products = products.order_by("price")
    elif sid == "3":
        products = products.order_by("-price")
    return render(request,"market/market.html", {"leftCategorieList":leftCategorieList, "products":products,"childs":childs,"gid":gid,"cid":cid})
def profiles(request,id):
   product = Product.objects.get(pk=id)
   return render(request, "market/profiles.html", {"product":product})
#购物车
def cart(request):
    #判断是否登录
    tokenValue = request.COOKIES.get("token")
    if not tokenValue:
        #说明没登录
        return redirect("/login/")
    try:
        user = User.objects.get(tokenValue=tokenValue)
    except User.DoesNotExist as e:
        return redirect("/login/")
    carts = Cart.objects.filter(user__tokenValue=tokenValue)
    return render(request,"cart/cart.html",{"carts":carts})

def qOrder(request):
    tokenValue = request.COOKIES.get("token")
    #找到当前可用的订单
    order = Order.orders2.filter(user__tokenValue=tokenValue).get(flag=0)
    order.flag =1
    order.save()
    # 属于该订单的购物车选中数据的isOrder置为False
    carts = Cart.objects.filter(user__tokenValue=tokenValue).filter(order=order).filter(isCheck=True)
    for cart in carts:
        cart.isOrder = False
        cart.save()
    # 将没有被选中的数据添加到新的订单中
    newOrder = Order.create(str(uuid.uuid4()),User.objects.get(tokenValue=tokenValue),Address.objects.get(pk=1),0)
    newOrder.save()
    oldCarts = Cart.objects.filter(user__tokenValue=tokenValue)
    for cart in oldCarts:
        cart.order = newOrder
        cart.save()
    return JsonResponse({"error":0})
def changecart2(request):
    cartid = request.POST.get("cartid")
    cart = Cart.objects.get(pk=cartid)
    cart.isCheck = not cart.isCheck
    cart.save()
    return JsonResponse({"error":0,"flag":cart.isCheck})



#购物车改变
def changecart(request,flag):
    num =1
    if flag == "1":
        num = -1
    #判断是否没有登录
    tokenValue = request.COOKIES.get("token")
    if not tokenValue:
        #说明没有登录
        return JsonResponse({"error":1})
    try:
        user = User.objects.get(tokenValue=tokenValue)
    except User.DoesNotExist as e:
        return JsonResponse({"error:2"})
    gid  = request.POST.get("gid")
    cid = request.POST.get("cid")
    pid = request.POST.get("pid")

    product = Product.objects.filter(categoryId=gid,childId=cid).get(productId=pid)

    try:
        cart = Cart.objects.filter(user__tokenValue=tokenValue).filter(product__categoryId=gid).filter(product__childId=cid).get(product__productId=pid)
        if flag =="2":
            if product.storeNums == "0":
                return JsonResponse({"error":0,"num":cart.num})
            # 以买过该商品，得到了该购物车数据
        cart.num = cart.num + num
        product.storeNums = str(int(product.storeNums)- num)
        product.save()
        if cart.num == 0:
            cart.delete()
        else:
            cart.save()
    except Cart.DoesNotExist as e:
        if flag == "1":
            return JsonResponse({"error":0,"num":0})
        # 找一个可用的订单  isDelete为False，flag为0，在当前用户中的所有订单中最多只能有一个订单为0
        try:
            order = Order.orders2.filter(user__tokenValue=tokenValue).get(flag=0)
        except Order.DoesNotExist as e:
            #没有可用订单
             orderId = str(uuid.uuid4())
             address = Address.objects.get(pk=1)
             order = Order.create(orderId,user,address,0)
             order.save()
        # 没有购买过该商品，需要创建该条购物车数据
        cart = Cart.create(user,product,order,1)
        cart.save()
        product.storeNums = str(int(product.storeNums)-num)
        product.save()
    #告诉客户端添加成功
    return JsonResponse({"error":0,"num":cart.num})




def mine(request):
    phone = request.session.get("phoneNum",default = "未登录")
    return render(request,"mine/mine.html",{"phone":phone})

from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect("/mine/")

def login(request):
    if request.method == "GET":
        if request.is_ajax():
            import random
            #生产验证码
            strNum = '1234567890'
            # 随机选取4个值作为验证码
            rand_str=''
            for i in range(0,6):
                rand_str += strNum[random.randrange(0,len(strNum))]
            # msg = "您的验证码是：%s。请不要把验证码泄露给其他人。"%rand_str
            phone = request.GET.get("phoneNum")
            send_sms(phone,rand_str)
            # 存入session
            request.session["code"] = rand_str
            print(rand_str)
            return JsonResponse({"data":"ok"})
        else:
            return render(request,"mine/login.html")
    else:
            phone = request.POST.get("username")
            passwd = request.POST.get("passwd")
            code = request.session.get("code")

            if passwd == code:
                # 验证码验证成功
                # 判断用户是否存在
                uuidStr = str(uuid.uuid4())
                try:
                    user = User.objects.get(pk=phone)
                    user.tokenValue = uuidStr
                    user.save()
                except User.DoesNotExist as e:
                    # 注册
                    user = User.create(phone, None, uuidStr, "sunck good")
                    user.save()
                request.session["phoneNum"] = phone
                reponse = redirect("/mine/")
                #将tokenValue写入cookie
                reponse.set_cookie("token",uuidStr)
                return reponse
            else:
                # 验证码验证失败
                return redirect(" /login/")
def address_inf(request):
    # phoneNum = request.session.get("phoneNum")
    # now_user=User.objects.filter(phoneNum=phoneNum).first()
    address1 = Address.objects.all()
    return render(request,"mine/address.html",{"address1": address1 })
def add_address(request):
    if request.method == "POST":
        phoneNum = request.session.get("phoneNum")
        now_user = User.objects.filter(phoneNum=phoneNum).first()
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        phoneNum = request.POST.get('phoneNum')
        postCode = request.POST.get('postCode')
        address = request.POST.get('address')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        street = request.POST.get('street')
        detailAddress = request.POST.get('detailAddress')
        address = Address.create(name=name,sex=sex,phoneNum=phoneNum,postCode=postCode,address=address, province=province, city=city, county=county, street=street, detailAddress=detailAddress, user=now_user)
        address.save()
        return redirect("/add/")
    else:
         return render(request,'mine/addaddress.html')
def modify_address(request,gid):
    if request.method == "POST":
        phoneNum = request.session.get("phoneNum")
        now_user = User.objects.filter(phoneNum=phoneNum).first()
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        phoneNum = request.POST.get('phoneNum')
        postCode = request.POST.get('postCode')
        address = request.POST.get('address')
        province = request.POST.get('province')
        city = request.POST.get('city')
        county = request.POST.get('county')
        street = request.POST.get('street')
        detailAddress = request.POST.get('detailAddress')
        address = Address.create(name=name,sex=sex,phoneNum=phoneNum,postCode=postCode,address=address, province=province, city=city, county=county, street=street, detailAddress=detailAddress, user=now_user)
        address.save()
    address1 = Address.objects.get(pk=gid)
    return render(request,'mine/modifyaddress.html',{"ad":address1,"gid":gid})

#接口分析
#轮播图接口
#GET www.sunck.wang/slideshows
#GET www.sunck.wang/maindescriptions
#GET www.sunck.wang/products?category_id=&product1_id=
#&product2_id=&product3_id=
# class SlidershowViewSet(viewsets.ModelViewSet):
#     queryset = Slideshow.objects.all()
#     serializer_class = SlidershowSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
# class MainDescriptionViewSet(viewsets.ModelViewSet):
#     queryset = MainDescription.objects.all()
#     serializer_class = MainDescriptionSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
# def products(request):
#     category_id = request.GET.get("category_id")
#     product1_id = request.GET.get("product1_id")
#     product2_id = request.GET.get("product2_id")
#     product3_id = request.GET.get("product3_id")
#     return    HttpResponse(category_id)
    #p1=Product.objects.get(category_id=category_id)

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.filter(categoryId="103598")
#     serializer_class = ProductSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)







