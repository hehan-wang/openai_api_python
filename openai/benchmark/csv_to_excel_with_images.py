import csv
import re
import requests
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from io import BytesIO
import os

csv_path = './weifeng-test-result.csv'
excel_path = './weifeng-test-result.xlsx'

# 提取api_response中的图片url（markdown图片语法）
def extract_img_url(api_response):
    match = re.search(r'!\[.*?\]\((https?://[^\)]+)\)', api_response)
    if match:
        return match.group(1)
    return None

# 读取csv
with open(csv_path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# 新增一列
new_field = '图片预览'

wb = Workbook()
ws = wb.active
ws.append(fieldnames + [new_field])

for i, row in enumerate(rows, start=2):
    api_response = row.get('api_response', '')
    img_url = extract_img_url(api_response)
    ws.append([row[f] for f in fieldnames] + [img_url if img_url else ''])
    if img_url:
        try:
            resp = requests.get(img_url, timeout=10)
            img = XLImage(BytesIO(resp.content))
            img.width = 100
            img.height = 100
            ws.add_image(img, f'{chr(65+len(fieldnames))}{i}')
        except Exception as e:
            ws.cell(row=i, column=len(fieldnames)+1, value='图片加载失败')

wb.save(excel_path) 