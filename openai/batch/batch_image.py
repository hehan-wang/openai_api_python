import os
import json
from datetime import datetime
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
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW'
os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-6353'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8516'
# os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW-8520'


client = OpenAI()
times = 1
workers = 1

def run_once(idx):
    try:
        # res = client.images.generate(
        #     model="gpt-4o-image",
        #     # model="gpt-image-1",
        #     # model="kling-image",.
        #     prompt="Generate a blu e sky with white clouds and the word \"Hello\" in skywriting.",
        #     n=1,
        #     size="1024x1536",
        #     # high, medium and low
        #     quality='low',
        #     # output_format="png",
        #     # response_format="url"
        # )

        prompt = """
        全景镜头，背景是在一个公园里面，后方是片民房，此时阳光明媚。图中人物顾清寒（男）搂着图中女子张云（女），表情含笑，图中女子张云（女）穿着一件淡蓝色长裙，坐在一张躺椅上。画风是「古风」。宽高比例 「9:16」，分辨率为1125*2000。超清画质，超高细节，五官清晰，眼神明亮，身体比例正常，四肢细节展示正常，画面质量和谐。
        """
        res = client.images.edit(
            # model="gpt-image-1",
            model="gpt-4o-image",
            image=open("../api/test.png", "rb"),  # No list here, just the file object
            #  image=[
            #     open("1.jpg", "rb"),
            #     open("2.jpg", "rb"),
            # ],
            size="1024x1536",
            prompt=prompt,
            # response_format="url",
        )
        # print(res.model_dump_json())
        return (idx, res.model_dump_json())
    except Exception as e:
        return (idx, str(e))

def main():
    # 创建输出文件名，包含时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"image_generation_results_{timestamp}.json"
    
    results = []
    with ThreadPoolExecutor(max_workers=workers) as executor:  # 你可以调整 max_workers
        futures = [executor.submit(run_once, i) for i in range(times)]
        for future in as_completed(futures):
            idx, content = future.result()
            print(f"--------------{idx}------------------")
            print(content)
            results.append({"index": idx, "result": content})

    # 将结果写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # 输出统计结果
    print(f"运行结束，总次数：{len(results)}")
    print(f"结果已保存到文件：{output_file}")

if __name__ == "__main__":
    main()
