from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525.client import Client as Client
from alibabacloud_dysmsapi20170525 import models as models
from server.settings import Ali_ACCESS_KEY_ID, Ali_ACCESS_KEY_SECRET

# 从settings.py读取AccessKey口令
config = open_api_models.Config(
    access_key_id=Ali_ACCESS_KEY_ID,
    access_key_secret=Ali_ACCESS_KEY_SECRET
)
config.endpoint = 'dysmsapi.aliyuncs.com'
client = Client(config)


def send_sm(phone_num, code):
    """
    内部信任的接口，用于发送短信验证码。
    :param phone_num: 发送的目标手机号
    :param code: 短信中包含的验证码
    :return: API调用结果及
    """
    req = models.SendSmsRequest()
    req.phone_numbers = phone_num;
    req.sign_name = "WeActive";
    req.template_code = "SMS_463965798";
    req.template_param = '{"code":"' + str(code) + '"}';
    response = client.send_sms(req)
    result = response.body.code
    return result
