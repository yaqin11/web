from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from Model.models import Task
from django.urls import reverse


@csrf_exempt
def index(request):
    # return HttpResponse('index!!')
    context = {}
    context['title'] = 'My Django'
    return render(request, 'index.html', context)


@csrf_exempt
def crawler(request):
    tasks = Task.objects.filter(deleted=0).order_by('-id')
    task_name_1 = request.GET.get("task_name_1")
    task_name_2 = request.POST.get("task_name_2")
    return HttpResponse('crawler task filter is success!!')


@csrf_exempt
def search_form(request):
    return render(request, 'app_01/search_form.html')


@csrf_exempt
def search(request):
    request.encoding = 'utf-8'
    if 'content' in request.GET and request.GET['content']:
        message = '搜索的内容为：' + request.GET['content']
        return HttpResponse(message)
    else:
        # message = '您没有提交内容！！'
        return redirect(reverse('app01:search_form'))  # 重定向


# 接收POST请求数据
@csrf_exempt
def search_post(request):
    post_data = {}
    if request.POST:
        post_data['post_key'] = request.POST['q']
    return render(request, 'app_01/post.html', post_data)
