import os
from zhipuai import ZhipuAI


client = ZhipuAI(api_key=os.getenv('ZHIPU_APIKEY'))

tips = ('根据以下【文本】，提取json结构信息，json包含字段：title（活动标题）、'
        'short（活动概要）、stime（开始报名时间）、atime（活动开始时间）、'
        'location（活动地点）、score（活动分数奖励，若无法确认则填0.0）、'
        'limit（报名人数，若无则填写999）'
        '上述所有字段值用字符串表示，其中日期格式为"yyyy-mm-dd hh:mm"。用代码块输出json。\n【文本】')

def getInfo(text):
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {
                "role": "user",
                "content": tips + text
            },

        ],
    )
    return response.choices[0].message.content
