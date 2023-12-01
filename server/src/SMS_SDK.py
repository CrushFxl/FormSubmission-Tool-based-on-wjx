from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525.client import Client as Client
from alibabacloud_dysmsapi20170525 import models as models
import configparser
import os

# 从密钥文件中读取AccessKey口令
path = os.path.dirname(__file__) + f"\\AccessKey.ini"
conf = configparser.ConfigParser()
conf.read(path, encoding='utf-8-sig')
access_key_id = conf["AccessKey"]["access_key_id"]
access_key_secret = conf["AccessKey"]["access_key_secret"]
config = open_api_models.Config(
    access_key_id=access_key_id,
    access_key_secret=access_key_secret
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
