from django.conf.urls import url
from myApp import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^bopintroduce/$', views.bopintroduce),
    url(r'^bouintroduce/$', views.bouintroduce),
    url(r'^login/$', views.login),
url(r'^main/$', views.main),
url(r'^detail/$', views.detail),
]