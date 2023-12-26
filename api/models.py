from openai import OpenAI

# 获取所有models
client = OpenAI()
res = client.models.list()
print(res.data)
