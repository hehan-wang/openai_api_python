import concurrent.futures
import csv
import json
import os
import re
import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI

os.environ['OPENAI_BASE_URL'] = 'https://key.wenwen-ai.com/v1'
os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW'

client = OpenAI()
INPUT_CSV = './weifeng-test.csv'
OUTPUT_CSV = './weifeng-test-result.csv'
MAX_WORKERS = 100

# 从 content 字段中提取 prompt 和 image_urls
request_body_pattern = re.compile(r"request_body: (\{.*?\})")


def parse_content(content):
    match = request_body_pattern.search(content)
    if not match:
        return None, None
    try:
        body = eval(match.group(1))  # 用 eval 解析 dict 字符串
        prompt = body.get('prompt', '')
        image_urls = body.get('image_urls', [])
        return prompt, image_urls
    except Exception as e:
        print(f"Parse error: {e}")
        return None, None

def get_image_ratio(url):
    try:
        resp = requests.get(url, timeout=10)
        img = Image.open(BytesIO(resp.content))
        width, height = img.size
        return width / height, width, height
    except Exception as e:
        print(f"Image error: {e}, url: {url}")
        return None, None, None

def fetch_and_process(row):
    content = row['content']
    prompt, image_urls = parse_content(content)
    prompt=prompt.strip()+"特别注意手指的生成细节，避免多余手指”，避免手指交叉混乱，没有畸形。图片宽高比例【2:3】"
    # 处理开始 打印日志
    print(f"处理开始: prompt: {prompt}, image_urls: {image_urls}")
    if not prompt or not image_urls:
        return {**row, 'prompt': '', 'image_urls': '', 'api_request': '', 'api_response': '', 'image_ratio': '', 'image_width': '', 'image_height': ''}
    # 构造 content_list
    content_list = []
    if prompt:
        content_list.append({
            "type": "text",
            "text": prompt
        })
    for url in image_urls:
        content_list.append({
            "type": "image_url",
            "image_url": {
                "url": url
            }
        })
    api_request = {
        "model": "gpt-4o-image",
        "messages": [
            {"role": "user", "content": content_list}
        ],
        "n": 1,
        "max_tokens": 2048,
        "temperature": 0.8,
    }
    ratio, width, height, image_url = None, None, None, None
    try:
        completion = client.chat.completions.create(**api_request)
        api_response = completion.model_dump_json()
           # 只取第一个图片 url
        response_data = json.loads(api_response)
        image_url = response_data['choices'][0]['message']['content'].split('(')[1].split(')')[0]
        ratio, width, height = get_image_ratio(image_url) if image_url else (None, None, None)
    except Exception as e:
        api_response = str(e)

    # 处理完打印日志
    print(f"处理完成: {image_url}, ratio: {ratio}, width: {width}, height: {height}")
    return {
        **row,
        'prompt': prompt,
        'image_urls': json.dumps(image_urls, ensure_ascii=False),
        'api_request': json.dumps(api_request, ensure_ascii=False),
        'api_response': api_response,
        'image_ratio': ratio if ratio is not None else '',
        'image_width': width if width is not None else '',
        'image_height': height if height is not None else '',
    }

def main():
    with open(INPUT_CSV, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(fetch_and_process, row) for row in rows]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
    # 写入结果 CSV
    fieldnames = list(results[0].keys()) if results else []
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    # 只处理第一条
    # if rows:
    #     result = fetch_and_process(rows[0])
    #     print(json.dumps(result, ensure_ascii=False, indent=2))
    #     # 写入结果 CSV
    #     fieldnames = list(result.keys())
    #     with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
    #         writer = csv.DictWriter(f, fieldnames=fieldnames)
    #         writer.writeheader()
    #         writer.writerow(result)

if __name__ == '__main__':
    main() 