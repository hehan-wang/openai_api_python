import requests
import time
import os
from typing import Optional, List
import time
import jwt


def encode_jwt_token(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,  # 有效时间，此处示例代表当前时间+1800s(30min)
        "nbf": int(time.time()) - 5  # 开始生效的时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token


class KlingImageGenerator:
    def __init__(self, api_key: str, base_url: str = 'https://api-beijing.klingai.com'):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

    def generate(self, prompt: str, **kwargs) -> List[str]:
        """Generate images and return local file paths"""
        # Set defaults
        model = kwargs.get('model', 'kling-v1')
        aspect_ratio = kwargs.get('aspect_ratio', '1:1')
        image_count = kwargs.get('image_count', 1)
        save_dir = kwargs.get('save_dir', './images')

        # Create save directory
        os.makedirs(save_dir, exist_ok=True)

        # Start generation
        result = self._start_generation(prompt, model, aspect_ratio, image_count)
        task_id = result['data']['task_id']

        # Wait for completion
        final_result = self._wait_completion(task_id)

        # Download images
        images = final_result['data']['task_result']['images']
        return self._download_images(images, task_id, save_dir)

    def _start_generation(self, prompt: str, model: str, aspect_ratio: str, image_count: int):
        """Start image generation task"""
        url = f"{self.base_url}/v1/images/generations"
        payload = {
            "prompt": prompt,
            "model": model,
            "aspect_ratio": aspect_ratio,
            "image_count": image_count
        }

        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def _wait_completion(self, task_id: str, max_wait: int = 300, interval: int = 5):
        """Wait for task completion"""
        url = f"{self.base_url}/v1/images/generations/{task_id}"
        start_time = time.time()

        while time.time() - start_time < max_wait:
            response = requests.get(url, headers=self.headers, timeout=30)
            response.raise_for_status()
            result = response.json()

            status = result['data']['task_status']
            if status in ['succeed', 'SUCCEED']:
                return result
            elif status == 'failed':
                raise Exception(f"Generation failed: {result}")

            time.sleep(interval)

        raise Exception(f"Task timeout after {max_wait} seconds")

    def _download_images(self, images: List, task_id: str, save_dir: str) -> List[str]:
        """Download images and return file paths"""
        downloaded_files = []

        for i, image_info in enumerate(images):
            image_url = image_info['url']
            filename = f"kling_{task_id}_{i + 1}.png"
            file_path = os.path.join(save_dir, filename)

            # Download image
            response = requests.get(image_url, timeout=60)
            response.raise_for_status()

            with open(file_path, 'wb') as f:
                f.write(response.content)

            downloaded_files.append(file_path)

        return downloaded_files


# Simple usage functions
def generate_image(api_key: str, prompt: str, base_url: str = "https://api-beijing.klingai.com", **kwargs) -> List[str]:
    """Simple function to generate images"""
    generator = KlingImageGenerator(api_key, base_url=base_url)
    return generator.generate(prompt, **kwargs)


def batch_generate(api_key: str, prompts: List[str], base_url: str = "https://api-beijing.klingai.com", **kwargs) -> List[List[str]]:
    """Generate multiple images in batch"""
    generator = KlingImageGenerator(api_key, base_url=base_url)
    results = []

    for prompt in prompts:
        try:
            files = generator.generate(prompt, **kwargs)
            results.append(files)
        except Exception as e:
            print(f"Failed for prompt '{prompt}': {e}")
            results.append([])

    return results


if __name__ == "__main__":
    # Example usage
    api_key = os.getenv('KLING_API_KEY', 'your_api_key_here')

    files = generate_image(
        api_key=api_key,
        prompt="A beautiful sunset over mountains",
        aspect_ratio="16:9",
        save_dir="./examples"
    )

    print(f"Generated files: {files}")
