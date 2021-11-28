from django.urls import path
from app_01 import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'crawler/', views.crawler, name='crawler'),
    path(r'search-form/', views.search_form, name='search_form'),
    path(r'search/', views.search, name='search'),
    path(r'search-post/', views.search_post, name='search_post'),
]
