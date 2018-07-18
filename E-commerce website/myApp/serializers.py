from rest_framework import serializers
from myApp.models import MainDescription,Product,Slideshow
from django.contrib.auth.models import User

class SlidershowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slideshow
        fields = ('trackid','name','img','sort')
#系列化MainDescription模型对象
class MainDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainDescription
        fields = ('categoryId','categoryName','sort','img','product1','product2','product3')
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields =('id','name','productId','longName','storeNums','specifics','sort','marketPrice','price','categoryId',
                 'childId','img','keywords','brandId','brandName','safeDay','safeUnit','safeUnitDesc','isDelete'
                 )