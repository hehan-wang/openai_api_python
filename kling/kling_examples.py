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
    #     api_key=api_key,
    #     prompt="A peaceful mountain lake at sunset",
    #     aspect_ratio="16:9",
    #     save_dir="./examples/basic"
    # )


    api_key = encode_jwt_token('AbatkPmfCEgaPmrakhReMRPkDffDJJkd', 'DP9gr39CpBaLbCdfPLPHyBNCpNaNkedQ')
    print(api_key)  # 打印生成的API_TOKEN

    files = generate_image(
        api_key=api_key,
        prompt="A peaceful mountain lake at sunset",
        aspect_ratio="16:9",
        save_dir="./examples/basic"
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