from django.test import TestCase

# Create your tests here.
def test(a,b,c ,*args,**kwargs):
    print(a)
    print(b)
    print(c)
    print(args)
    print(kwargs)
test(1,2,3,4,5,6,age=10,name = 100)
