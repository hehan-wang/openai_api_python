#!/usr/bin/env python3
"""
Kling AI Image Generator - Simple Examples
"""

import os
from kling_image_generator import generate_image, batch_generate, KlingImageGenerator, encode_jwt_token


def basic_example():
    """Basic image generation"""
    # api_key = os.getenv('KLING_API_KEY')

    print("=== Basic Example ===")
    # files = generate_image(
    #     api_key='sk-RC2GoclGIAs7309WB76bAd7e0e24407d8a9cA7C837Ab3b38',
    #     base_url='https://api.bltcy.ai/kling',
    #     prompt="图片中有两个角色，第一个是虚拟角色（这个角色要求参考输入图片中人物的性别，以及形象特征生成）"
    #            "。第二个是主控角色，是一名年轻女性（不需要参考输入图片），穿着一件淡黄色短裙。场景：在公园。绿树成荫，"
    #            "鲜花盛开，阳光洒在小径上。虚拟角色搂着主控角色，表情为满脸宠溺。主控角色站在虚拟角色前面，背对着镜头。"
    #            "生成画风参考输入图片中的画风。超清画质，超高细节，五官清晰，眼神明亮，身体比例正常，四肢细节展示正常，"
    #            "画面质量和谐，图片宽高比例【2:3】。",
    #     aspect_ratio="16:9",
    #     save_dir="./examples/basic",
    #     model='kling-v1.5',
    #     image='https://hobby-suanfa.hobby666.com/chat_video_generation/image_super_resolution/2025-06-14/afb40bbe7f9a45ceb89ea8f3228939ff/1125x2000_e28f6cdfe3674f93a03528378267d59f.jpg'
    # )


    api_key = encode_jwt_token('AbatkPmfCEgaPmrakhReMRPkDffDJJkd', 'DP9gr39CpBaLbCdfPLPHyBNCpNaNkedQ')
    print(api_key)  # 打印生成的API_TOKEN

    files = generate_image(
        api_key=api_key,
        prompt="图片中有两个角色，第一个是虚拟角色（这个角色要求参考输入图片中人物的性别，以及形象特征生成）"
               "。第二个是主控角色，是一名年轻女性（不需要参考输入图片），穿着一件淡黄色短裙。场景：在公园。绿树成荫，"
               "鲜花盛开，阳光洒在小径上。虚拟角色搂着主控角色，表情为满脸宠溺。主控角色站在虚拟角色前面，背对着镜头。"
               "生成画风参考输入图片中的画风。超清画质，超高细节，五官清晰，眼神明亮，身体比例正常，四肢细节展示正常，"
               "画面质量和谐，图片宽高比例【2:3】。",
        aspect_ratio="16:9",
        save_dir="./examples/basic",
        model='kling-v1.5',
        image='https://hobby-suanfa.hobby666.com/chat_video_generation/image_super_resolution/2025-06-14/afb40bbe7f9a45ceb89ea8f3228939ff/1125x2000_e28f6cdfe3674f93a03528378267d59f.jpg'
    )
    print(f"Generated: {files}")


def batch_example():
    """Batch generation example"""
    api_key = os.getenv('KLING_API_KEY')
    if not api_key:
        print("Please set KLING_API_KEY environment variable")
        return
    
    print("\n=== Batch Example ===")
    prompts = [
        "A futuristic city skyline",
        "A magical forest with glowing trees",
        "A vintage car on a country road"
    ]
    
    results = batch_generate(
        api_key=api_key,
        prompts=prompts,
        aspect_ratio="1:1",
        save_dir="./examples/batch"
    )
    
    for i, files in enumerate(results):
        print(f"Prompt {i+1}: {len(files)} images generated")


def advanced_example():
    """Advanced usage with custom parameters"""
    api_key = os.getenv('KLING_API_KEY')
    if not api_key:
        print("Please set KLING_API_KEY environment variable")
        return
    
    print("\n=== Advanced Example ===")
    generator = KlingImageGenerator(api_key)
    
    # Different aspect ratios
    configs = [
        {"aspect_ratio": "1:1", "prompt": "Square portrait of a cat"},
        {"aspect_ratio": "16:9", "prompt": "Wide landscape with mountains"},
        {"aspect_ratio": "9:16", "prompt": "Tall portrait of a building"}
    ]
    
    for config in configs:
        try:
            files = generator.generate(
                prompt=config["prompt"],
                aspect_ratio=config["aspect_ratio"],
                save_dir=f"./examples/{config['aspect_ratio'].replace(':', 'x')}"
            )
            print(f"{config['aspect_ratio']}: {len(files)} files")
        except Exception as e:
            print(f"Failed {config['aspect_ratio']}: {e}")


if __name__ == "__main__":
    basic_example()
    # batch_example()
    # advanced_example()