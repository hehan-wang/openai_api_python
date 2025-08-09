import os
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

# 设置环境变量


# os.environ['OPENAI_BASE_URL'] = 'https://api.xoneai.xyz/v1'
# os.environ['OPENAI_API_KEY'] = 'sk-Vrbdsv2eN53f408465E141EeDd5946BdB47d71D1Aa7c5d16'

# os.environ['OPENAI_BASE_URL'] = 'https://x.api96.com/v1'
# os.environ['OPENAI_API_KEY'] = 'sk-1b34KUU0uPjxxVa0wtIeLOxz7S5XvUQJpGcDNA5NGNwjD5au'

# os.environ['OPENAI_BASE_URL'] = 'https://nekoapi.com/v1'
# os.environ['OPENAI_API_KEY'] = 'sk-WtCTWppdPy8PeTFT0dC58dD704Bb4eCeB0FcE125Ba6c7eA9'

# os.environ['OPENAI_BASE_URL'] = 'http://139.99.124.141:4000/v1'
# os.environ['OPENAI_API_KEY'] = 'sk-KwULYKiaCPtmdU3KA63c0d39A58f491695B47d5f9b8f2c41'

os.environ['OPENAI_BASE_URL'] = 'https://key.wenwen-ai.com/v1'
os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW'

# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8532'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8538'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8526'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8549'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8535'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8514'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8502'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8524'


client = OpenAI()
# 请求内容
# messages = [
#     {"role": "system", "content": "（你的角色设定文本）"},
#     {"role": "assistant", "content": "你好"},
#     {"role": "user", "content": "你好！很高兴与你交流。请问有什么我可以帮助你的吗？"},
#     {"role": "assistant", "content": "你好！我想了解一下"},
#     {"role": "assistant", "content": "关于节假日推广活动的方案。"},
#     {"role": "user", "content": "好的，请问您具体是想推广哪类产品？以及您的目标客户群体是哪些呢？"},
#     {"role": "assistant", "content": "我想推广健康零食。"},
#     {"role": "assistant", "content": "目标客户是注重健康和品质的消费者。"},
#     {"role": "user", "content": "请问您对推广渠道或方式有特定的偏好吗？"}
# ]

# model='gpt-4o-image'
# messages = [
#     {"role": "user", "content": "画个猪"}
# ]

# messages = [
#     {"role": "user", "content": "hi"}
# ]

messages = [
    {"role": "user", "content": "日本旅游推荐"}
]

# messages=[
#     {"role": "user", "content": "输出5000字关于美国发展的文章"}
# ]


# # model='gpt-4o-image'
# model='gpt-4o-mini'
# model='claude-3-7-sonnet-20250219'
# model='gpt-4o'
# model='gpt-4o-mini-2024-07-18'
# model='gemini-2.5-flash'
# model='claude-sonnet-4-20250514'
# model='claude-sonnet-4-20250514-thinking'
# model='gpt-4o-2024-08-06'
# model='gpt-4.1'
# model='gpt-4o-2024-11-20'
# model='gpt-4o-mini-2024-07-18'
model='deepseek-r1-32b'
times = 1
workers = 1

def run_once(idx):
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True
        )
        full_content = ""
        for chunk in completion:
            if hasattr(chunk, 'choices') and chunk.choices:
                delta = chunk.choices[0].delta
                if hasattr(delta, 'content') and delta.content:
                    full_content += delta.content
                elif isinstance(delta, dict) and 'content' in delta:
                    full_content += delta['content']
        return (idx, full_content)
    except Exception as e:
        return (idx, str(e))

def main():
    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:  # 你可以调整 max_workers
        futures = [executor.submit(run_once, i) for i in range(times)]
        for future in as_completed(futures):
            idx, content = future.result()
            print(f"--------------{idx}------------------")
            print(content)
            results.append(content)

    # 输出统计结果
    print("运行结束，总次数：" + str(len(results)))

if __name__ == "__main__":
    main()
