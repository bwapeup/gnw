from yunpian_python_sdk.model import constant as YC
from yunpian_python_sdk.ypclient import YunpianClient
from django.conf import settings

yunpian_apikey = getattr(settings, 'YUNPIAN_APIKEY', '')

def send_sms(mobile, msg):
    #clnt = YunpianClient(yunpian_apikey)
    #param = {YC.MOBILE:mobile_number,YC.TEXT:'【云片网】您的验证码是'+verification_code}
    #r = clnt.sms().single_send(param)
    pass