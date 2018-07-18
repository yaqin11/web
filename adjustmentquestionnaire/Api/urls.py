#系统自带
import os

#第三方
from django.conf.urls import url

#项目自定义
from Api.rest import *
from Api.customer import *
from Api.admin import *
#新建session对象
#session_obj = SessionRest()
#新建user对象
#user_obj = UserRest()

# api_urls = [
#     url(r'session',session_obj.enter),
#     url(r'user',user_obj.enter)
# ]
api = Register()
api.regist(SessionRest('session'))
api.regist(UserRest('user'))
api.regist((RegistCode()))
api.regist(CustomerQuestionnaire('customer_questionnaire'))
api.regist(CustomerQuestion('customer_question'))
api.regist(CustomerQuestionnaireState('customer_questionnaire_state'))
api.regist(AdminQuestionnaire('admin_questionnaire'))


