import os


from zhipuai import ZhipuAI
client = ZhipuAI(api_key=os.getenv('ZHIPU_APIKEY'))


def getAnswer(que, remark='', options=''):
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {
                "role": "user",
                "content": ""
            },

        ],
    )
    return response

resp = getAnswer(notice)


print(resp.choices[0], '\n', 'tag:', resp.choices[0].message.content)
