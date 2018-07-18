import json
import qrcode
from tempfile import TemporaryFile
import base64

from django.http.response import HttpResponse


def method_not_allowed():
    return HttpResponse('{"msg":"方法不支持"}',status=405,content_type="application/json")
#参数错误
def params_error(errors):
    return HttpResponse(json.dumps(errors), status=422, content_type="application/json")
def not_authenticated():
    return HttpResponse('{"msg":"未登录"}', status=401, content_type="application/json")
def permission_denied():
    return HttpResponse('{"msg":"没有权限"}', status=402, content_type="application/json")
def json_response(data):
    return HttpResponse(json.dumps(data), status=200, content_type="application/json")

def create_qrcode(data):
    img = qrcode.make(data)
    tmp = TemporaryFile()
    img.save(tmp)
    tmp.seek(0)
    return base64.b64encode(tmp.read()).decode()
