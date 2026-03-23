#!/usr/bin/env python3
"""
MiniMax Token Plan Monitor and Image Generator

This script monitors MiniMax Token Plan remaining quota and automatically
generates images using the image-01 model when resources are available.
"""

import os
import sys
import time
import json
import logging
import argparse
import requests
import anthropic
from datetime import datetime
from pathlib import Path

# Configuration
TOKEN_PLAN_URL = "https://www.minimaxi.com/v1/api/openplatform/coding_plan/remains"
IMAGE_API_URL = "https://api.minimaxi.com/v1/image_generation"

# Logging setup
def setup_logging(output_dir: Path):
    """Setup logging to file and console."""
    log_file = output_dir / "generation.log"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)


def get_api_key() -> str:
    """Get API key from environment variable."""
    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("MINIMAX_API_KEY environment variable is not set")
    return api_key


def query_token_plan(api_key: str) -> dict:
    """
    Query MiniMax Token Plan remaining quota.

    Returns:
        dict: Response containing model_remains array
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    logging.info("Querying Token Plan...")
    response = requests.get(TOKEN_PLAN_URL, headers=headers, timeout=30)
    response.raise_for_status()

    data = response.json()
    base_resp = data.get("base_resp", {})
    logging.info(f"Token Plan API status: {base_resp.get('status_msg', 'unknown')}")
    return data


def check_token_quota(data: dict, model_name: str = "MiniMax-M2.7") -> bool:
    """
    Check if token quota meets the threshold for image generation.

    Token Plan resets every 5 hours.
    Trigger condition: remaining quota >= 30%

    Args:
        data: Token Plan API response
        model_name: Model to check (default: MiniMax-M2.7)

    Returns:
        bool: True if quota is sufficient
    """
    from datetime import datetime

    model_remains = data.get("model_remains", [])

    # Find the specified model
    model_data = None
    for item in model_remains:
        if item.get("model_name") == model_name:
            model_data = item
            break

    if not model_data:
        logging.error(f"Model {model_name} not found in response")
        return False

    total = model_data.get("current_interval_total_count", 0)
    remaining = model_data.get("current_interval_usage_count", 0)

    # Calculate remaining percentage: 1 - (used/total)
    remaining_pct = (remaining / total) * 100 if total > 0 else 0

    # Time information
    start_time_ms = model_data.get("start_time", 0)
    end_time_ms = model_data.get("end_time", 0)
    now_ms = datetime.now().timestamp() * 1000

    start_time = datetime.fromtimestamp(start_time_ms / 1000)
    end_time = datetime.fromtimestamp(end_time_ms / 1000)
    now = datetime.fromtimestamp(now_ms / 1000)

    elapsed_hours = (now_ms - start_time_ms) / 1000 / 3600
    remaining_hours = (end_time_ms - now_ms) / 1000 / 3600

    logging.info(f"===== Token Plan Status =====")
    logging.info(f"Model: {model_name}")
    logging.info(f"Time Period: {start_time.strftime('%Y-%m-%d %H:%M')} ~ {end_time.strftime('%Y-%m-%d %H:%M')}")
    logging.info(f"Current Time: {now.strftime('%Y-%m-%d %H:%M')}")
    logging.info(f"Total Quota: {total}")
    logging.info(f"Used: {total - remaining} ({100 - remaining_pct:.1f}%)")
    logging.info(f"Remaining: {remaining} ({remaining_pct:.1f}%)")
    logging.info(f"Elapsed: {elapsed_hours:.2f} hours")
    logging.info(f"Remaining Time: {remaining_hours:.2f} hours")
    logging.info(f"==============================")

    threshold = 30
    return remaining_pct >= threshold


def enhance_prompt(api_key: str, prompt: str) -> str:
    """
    Enhance a simple description into a detailed image generation prompt
    using MiniMax text model.

    Args:
        api_key: MiniMax API key
        prompt: Simple description text

    Returns:
        str: Enhanced prompt
    """
    system_prompt = """你是一个专业的AI图像生成提示词工程师。你的任务是将用户提供的简单描述转化为详细、专业的图像生成提示词。

请注意：
1. 详细描述光线、构图、色彩、风格等要素
2. 添加专业摄影或绘画术语
3. 描述画面的氛围和情绪
4. 不要添加任何解释或说明，只输出增强后的提示词
5. 保持提示词简洁但富有细节

示例：
输入：一只猫
输出：A majestic orange tabby cat sitting on a windowsill, soft golden hour sunlight streaming from the right side, warm bokeh background with blurred autumn leaves, shallow depth of field, professional photography, cozy atmosphere, shot with Canon EOS R5, 85mm lens, f/1.8"""

    logging.info(f"Enhancing prompt: {prompt[:50]}...")

    client = anthropic.Anthropic(api_key=api_key, base_url="https://api.minimaxi.com/anthropic")
    message = client.messages.create(
        model="MiniMax-M2.7",
        max_tokens=1000,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    )

    enhanced = prompt
    for block in message.content:
        if block.type == "text":
            enhanced = block.text
            break

    logging.info(f"Enhanced prompt: {enhanced}")
    return enhanced


def generate_image(api_key: str, prompt: str, model: str = "image-01") -> list:
    """
    Generate images using MiniMax image-01 API.

    Args:
        api_key: MiniMax API key
        prompt: Image generation prompt
        model: Model to use (image-01 or image-01-live)

    Returns:
        list: List of image URLs
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": "16:9",
        "response_format": "url",
        "n": 1,
        "prompt_optimizer": True
    }

    logging.info(f"Generating image with model {model}...")
    response = requests.post(IMAGE_API_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    data = response.json()
    logging.info(f"Image generation response: {data}")

    # Handle response format: { "data": { "image_urls": ["..."] } }
    image_urls = []
    if "data" in data:
        image_urls = data["data"].get("image_urls", [])

    if not image_urls:
        raise ValueError(f"No image URLs in response: {data}")

    logging.info(f"Generated {len(image_urls)} image(s)")
    return image_urls


def download_image(image_url: str, output_path: Path) -> bool:
    """
    Download image from URL to local path.

    Args:
        image_url: URL of the image
        output_path: Local path to save the image

    Returns:
        bool: True if successful
    """
    logging.info(f"Downloading image to {output_path}...")
    response = requests.get(image_url, timeout=60)
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        f.write(response.content)

    logging.info(f"Image saved: {output_path}")
    return True


def read_prompts_file(file_path: str) -> list:
    """
    Read prompts from a text file.
    Lines starting with '#' are treated as comments and ignored.

    Args:
        file_path: Path to the prompts file

    Returns:
        list: List of prompt strings
    """
    prompts = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                prompts.append(line)

    logging.info(f"Loaded {len(prompts)} prompts from {file_path}")
    return prompts


def sanitize_filename(text: str, max_length: int = 20) -> str:
    """
    Sanitize text for use in filename.

    Args:
        text: Input text
        max_length: Maximum length

    Returns:
        str: Sanitized filename safe string
    """
    # Remove/replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        text = text.replace(char, '_')

    # Truncate and add underscore
    text = text[:max_length].strip()
    if text and not text.endswith('_'):
        text += '_'

    return text


def create_output_directory(base_output: str) -> Path:
    """
    Create output directory with optional timestamp.

    Args:
        base_output: Base output directory path

    Returns:
        Path: Created output directory path
    """
    output_dir = Path(base_output)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="MiniMax Image Generator"
    )
    parser.add_argument(
        "--prompts",
        required=True,
        help="Path to the prompts file (required)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force execution, skip Token Plan quota check"
    )
    parser.add_argument(
        "--output",
        default="./generated_images/",
        help="Output directory (default: ./generated_images/)"
    )
    parser.add_argument(
        "--model",
        default="image-01",
        choices=["image-01", "image-01-live"],
        help="Image model to use (default: image-01)"
    )
    parser.add_argument(
        "--check-model",
        default="MiniMax-M2.7",
        help="Model to check for token quota (default: MiniMax-M2.7)"
    )
    parser.add_argument(
        "--enhance",
        action="store_true",
        help="Enable prompt enhancement using LLM (disabled by default)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key()

    # Create output directory and setup logging
    output_dir = create_output_directory(args.output)
    logger = setup_logging(output_dir)

    logging.info("=" * 50)
    logging.info("MiniMax Image Generator Started")
    logging.info(f"Prompts file: {args.prompts}")
    logging.info(f"Output directory: {output_dir}")
    logging.info(f"Force mode: {args.force}")
    logging.info(f"Enhance prompt: {args.enhance}")
    logging.info(f"Check model: {args.check_model}")
    logging.info(f"Image model: {args.model}")
    logging.info("=" * 50)

    # Check token quota unless forced
    if not args.force:
        try:
            token_data = query_token_plan(api_key)
            logging.info(f"Token data: {token_data}")
            if not check_token_quota(token_data, "MiniMax-M*"):
                logging.warning("Token quota below threshold. Use --force to skip this check.")
                sys.exit(0)
        except Exception as e:
            logging.error(f"Failed to query Token Plan: {e}")
            sys.exit(1)

    # Read prompts
    try:
        prompts = read_prompts_file(args.prompts)
        if not prompts:
            logging.warning("No prompts found in file.")
            sys.exit(0)
    except Exception as e:
        logging.error(f"Failed to read prompts file: {e}")
        sys.exit(1)

    # Process each prompt
    success_count = 0
    fail_count = 0

    for i, original_prompt in enumerate(prompts, 1):
        try:
            logging.info(f"\n--- Processing prompt {i}/{len(prompts)} ---")

            # Use prompt directly or enhance based on flag
            final_prompt = original_prompt
            if args.enhance:
                final_prompt = enhance_prompt(api_key, original_prompt)
                time.sleep(1)  # Rate limiting

            # Generate image(s)
            image_urls = generate_image(api_key, final_prompt, args.model)
            time.sleep(1)  # Rate limiting

            # Save images
            for j, image_url in enumerate(image_urls):
                suffix = f"_{j+1}" if len(image_urls) > 1 else ""
                filename = f"{i:03d}{suffix}_{sanitize_filename(original_prompt)}.png"
                output_path = output_dir / filename
                download_image(image_url, output_path)
                logging.info(f"Success: {filename}")

            success_count += 1

        except Exception as e:
            logging.error(f"Failed to process prompt '{original_prompt[:50]}...': {e}")
            fail_count += 1
            continue

    # Summary
    logging.info("\n" + "=" * 50)
    logging.info("Generation Complete")
    logging.info(f"Success: {success_count}, Failed: {fail_count}")
    logging.info(f"Output directory: {output_dir}")
    logging.info("=" * 50)


if __name__ == "__main__":
    main()
