from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from Model.models import Task


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


