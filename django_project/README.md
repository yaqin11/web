Django项目最基础的架构
=================
###1.创建django项目
django-admin startproject django_project
###2.创建数据库表结构
python manage.py migrate
###3.启动django服务
###python3 manage.py runserver
###4.创建 MySQL 数据库( ORM 无法操作到数据库级别，只能操作到数据表)语法：
create database 数据库名称 default charset=utf8; # 防止编码问题，指定为 utf8
###5.定义模型
django-admin.py startapp Model 
###6.数据库表迁移
    #让Django知道模型有一些改变
    python manage.py makemigrations Model
    # 创建表结构
    python manage.py migrate Model
    或者：
    #让Django知道模型有一些改变
    python manage.py makemigrations app01
    # 创建表结构
    python manage.py migrate app01

Django项目部署
=================
--web服务器--：nginx
--wsgi服务器--：uwsgi
uWSGI+nginx
nginx具备优秀的静态内容处理能力，它将动态内容转发给uWSGI服务器，这样可以达到很好的客户端响应。
将uwsgi和Django连接：
uwsgi --http :8000 --chdir /root/venv/django_project/ --module django_wsgi
nginx配置:
找到nginx的安装目录,打开conf/nginx.conf文件，修改server配置
server {
        listen       80;
        server_name  localhost;
        access_log /home/django_project/logs/django_project.log;
        error_log /home/django_project/logs/error.log;
        location / {            
            # include  uwsgi_params;
            include /etc/nginx/uwsgi_params;
            uwsgi_pass  127.0.0.1:8000;              //必须和uwsgi中的设置一致
            index  index.html index.htm;
            client_max_body_size 35m;
        }
        access_log off;
   }