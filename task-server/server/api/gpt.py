import os
from zhipuai import ZhipuAI

client = ZhipuAI(api_key=os.getenv('ZHIPU_APIKEY'))

def getAnswer(que, remark='', options=''):
    que += '（注：填空题回答不超8个字，选择题只答选项序号）\n'
    if remark: remark = '【提示】' + remark + '\n'
    if options: options = '【选项】' + options
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {
                "role": "user",
                "content": que + remark + options
            },
        ],
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
