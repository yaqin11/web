from django.conf.urls import url,include
from myApp import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'maindescriptions',views.MainDescriptionViewSet)
# router.register(r'products',views.ProductViewSet)
#router.register(r'slideshows',views.SlidershowViewSet)
urlpatterns = [
    url(r'^home/$', views.home),
    url(r'market/(\w+)/(\w+)/(\w+)/$', views.market),
url(r'^cart/$', views.cart),
    # 修改购物车  增加、减少
    url(r'^changecart/(\d+)/$', views.changecart),
# 修改购物车  是否选中
url(r'^changecart2/$', views.changecart2),
# 下订单
url(r'^qOrder/$', views.qOrder),

url(r'^mine/$', views.mine),
#登陆界面
    url(r'login/$', views.login),
    url(r'quit/$', views.quit),
url(r'^profiles/(\d+)/$', views.profiles),
    url(r'address_inf/$', views.address_inf),
    url(r'add/$', views.add_address),
url(r'modify/(\d+)/$', views.modify_address),
# url(r'^products/$', views.products),
# url(r'^', include(router.urls)),

]