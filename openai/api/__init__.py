import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("model api init OPENAI_BASE_URL, OPENAI_API_KEY in __init__.py")

# 从环境变量读取，如果没有设置则使用默认值
os.environ['OPENAI_BASE_URL'] = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY', '')
