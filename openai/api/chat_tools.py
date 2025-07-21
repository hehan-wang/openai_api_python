import os
from openai import OpenAI
from dotenv import load_dotenv

from openai.types.chat import completion_create_params

# 加载环境变量
load_dotenv()

# 从环境变量读取API配置
os.environ['OPENAI_BASE_URL'] = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-3.5-turbo-1106",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    response_format=completion_create_params.ResponseFormat(type="json_object")
)

print(completion.choices[0].message.model_dump_json())
