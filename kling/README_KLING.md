# Kling AI Image Generator

简洁的Kling AI图片生成Python客户端。

## 安装

```bash
pip install requests
```

## 快速开始

```python
from kling_image_generator import generate_image

# 简单生成
files = generate_image(
    api_key="your_api_key",
    prompt="A beautiful sunset over mountains",
    aspect_ratio="16:9"
)
```

## 使用方法

### 1. 基础生成
```python
from kling_image_generator import KlingImageGenerator

generator = KlingImageGenerator("your_api_key")
files = generator.generate(
    prompt="Your image description",
    aspect_ratio="16:9",  # 1:1, 16:9, 9:16
    save_dir="./images"
)
```

### 2. 批量生成
```python
from kling_image_generator import batch_generate

results = batch_generate(
    api_key="your_api_key",
    prompts=["prompt1", "prompt2", "prompt3"],
    aspect_ratio="1:1"
)
```

### 3. 环境变量
```bash
export KLING_API_KEY="your_api_key"
```

## 示例

运行示例代码：
```bash
python kling_examples.py
```

## API参数

- `prompt`: 图片描述文本
- `aspect_ratio`: 比例 ("1:1", "16:9", "9:16")
- `model`: 模型名称 (默认: "kling-v1")
- `image_count`: 生成数量 (默认: 1)
- `save_dir`: 保存目录 (默认: "./images")

## 文件结构

```
kling/
├── kling_image_generator.py  # 主要客户端
├── kling_examples.py         # 使用示例
└── README_KLING.md          # 说明文档
```