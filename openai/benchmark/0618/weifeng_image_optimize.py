import concurrent.futures
import requests
from io import BytesIO
from PIL import Image
from openai import OpenAI
import openpyxl
from openpyxl import Workbook
import os
import json

# 配置OpenAI
os.environ['OPENAI_BASE_URL'] = 'https://key.wenwen-ai.com/v1'
os.environ['OPENAI_API_KEY'] = 'sk-GYYKJ77h2qJ9YfQV46WAHALlqtz1N17Ma3HpyOw1VHKkb0zW'
client = OpenAI()

INPUT_TXT = './input.txt'
OUTPUT_XLSX = './output.xlsx'
MAX_WORKERS = 20

PROMPT_SUFFIX = "图片中有两个角色，第一个是虚拟角色（这个角色要求参考输入图片中人物的性别，以及形象特征生成）。第二个是主控角色，是一名年轻女性（不需要参考输入图片），穿着一件淡黄色短裙。场景：在公园。绿树成荫，鲜花盛开，阳光洒在小径上。虚拟角色搂着主控角色，表情为满脸宠溺。主控角色站在虚拟角色前面，背对着镜头。生成画风参考输入图片中的画风。超清画质，超高细节，五官清晰，眼神明亮，身体比例正常，四肢细节展示正常，画面质量和谐，图片宽高比例【2:3】。"

# 获取图片宽高和比例
def get_image_info(url):
    try:
        resp = requests.get(url, timeout=10)
        img = Image.open(BytesIO(resp.content))
        width, height = img.size
        ratio = width / height
        return width, height, ratio, ''
    except Exception as e:
        return None, None, None, f"Image error: {e}"

# 调用openai api
def call_openai_api(image_url):
    prompt = PROMPT_SUFFIX
    content_list = [
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": image_url}}
    ]
    api_request = {
        "model": "gpt-4o-image",
        "messages": [
            {"role": "user", "content": content_list}
        ],
        "n": 1,
        "max_tokens": 2048,
        "temperature": 0.8,
    }
    try:
        completion = client.chat.completions.create(**api_request)
        api_response = completion.model_dump_json()
        return json.dumps(api_request, ensure_ascii=False), api_response, ''
    except Exception as e:
        return json.dumps(api_request, ensure_ascii=False), '', f"OpenAI error: {e}"

# 处理单个图片url
def process_url(url):
    log = {
        'url': url,
        'width': '',
        'height': '',
        'ratio': '',
        'api_request': '',
        'api_response': '',
        'error': ''
    }
    width, height, ratio, img_err = get_image_info(url)
    log['width'] = width if width else ''
    log['height'] = height if height else ''
    log['ratio'] = ratio if ratio else ''
    if img_err:
        log['error'] = img_err
        return log
    api_request, api_response, api_err = call_openai_api(url)
    log['api_request'] = api_request
    log['api_response'] = api_response
    if api_err:
        log['error'] = api_err
    return log

def main():
    # 读取所有url
    with open(INPUT_TXT, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_url, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            print(f"处理完成: {result}")
            results.append(result)
    # 写入excel
    wb = Workbook()
    ws = wb.active
    headers = ['url', 'width', 'height', 'ratio', 'api_request', 'api_response', 'error']
    ws.append(headers)
    for row in results:
        ws.append([row.get(h, '') for h in headers])
    wb.save(OUTPUT_XLSX)
    print(f"全部完成，结果已写入 {OUTPUT_XLSX}")

if __name__ == '__main__':
    main() 