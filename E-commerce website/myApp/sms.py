#-*- coding:utf-8 -*-
# import http.client
# import urllib
#
# host  = "106.ihuyi.com"
# sms_send_uri = "/webservice/sms.php?method=Submit"
#
# account  = "C66204495"
# password = "f4bcaf08bcd2d18b8325763abf61935c"
#
# def send_sms(text, mobile):
#     params = urllib.parse.urlencode({'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' })
#     headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#     conn = http.client.HTTPConnection(host, port=80, timeout=30)
#     conn.request("POST", sms_send_uri, params, headers)
#     response = conn.getresponse()
#     response_str = response.read()
#     conn.close()
#     return response_str
#
# if __name__ == '__main__':
#
#     mobile = "15517781603"
#     text = "您的验证码是：121254。请不要把验证码泄露给其他人。"
#
#     print(send_sms(text, mobile))
def send_sms(phone,rand_str):
    url = "http://api.sms.cn/sms/?ac=send"

    headers = {'Content-type': 'application/x-www-form-urlencoded'}

    uid="z112233"

    pwd='fc9523f0960f99b6eea5c6880d6f59f8'

    template='100006'

    mobile=phone

    content="{\"code\":\"%s\"}"%rand_str
    # import time
    # timestamp = time.strftime('%Y%m%d%H%M%S')
    #
    # sig = uid + pwd + timestamp

    # import hashlib
    # md = hashlib.md5()
    # md.update(sig.encode('utf-8'))
    # sig = md.hexdigest()
    form_data = {
        'uid':uid,
        'pwd':pwd,
        'mobile':mobile,
        'content':content,
        'template':template,
        'encode':'GBK'
    }

    from urllib.parse import urlencode

    form_data = urlencode(form_data)


    import  http.client

    connect = http.client.HTTPConnection('api.sms.cn')

    connect.request(method='POST',url=url,body=form_data,headers=headers)

    resp = connect.getresponse()

    print(resp.read().decode('gbk'))

