#!/usr/bin/env python3
"""
图片压缩脚本 - 将图片压缩到指定大小
用法: python compress_image.py <图片路径> [--max-size KB]
"""

import os
import sys
from PIL import Image


def compress_image(image_path, max_size_kb=512):
    """压缩图片到指定大小（KB）"""
    if not os.path.exists(image_path):
        print(f"Error: File not found: {image_path}")
        return False

    max_size_bytes = max_size_kb * 1024
    file_size = os.path.getsize(image_path)

    if file_size <= max_size_bytes:
        print(f"Image already {file_size / 1024:.1f}KB < {max_size_kb}KB, skipping compression")
        return True

    img = Image.open(image_path)
    original_format = img.format

    # PNG 转为 JPEG 更容易压缩
    if img.mode in ('RGBA', 'LA', 'P'):
        # 保持 PNG 但降低质量
        quality = 85
        while True:
            img.save(image_path, 'PNG', optimize=True)
            if os.path.getsize(image_path) <= max_size_bytes or quality <= 50:
                break
            quality -= 5
    else:
        # JPEG 直接压缩
        quality = 85
        while True:
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
            if os.path.getsize(image_path) <= max_size_bytes or quality <= 30:
                break
            quality -= 5

    new_size = os.path.getsize(image_path)
    print(f"Compressed: {file_size / 1024:.1f}KB -> {new_size / 1024:.1f}KB (saved {100 * (1 - new_size / file_size):.1f}%)")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python compress_image.py <image_path> [--max-size KB]")
        sys.exit(1)

    image_path = sys.argv[1]
    max_size = 512  # 默认 512KB

    if len(sys.argv) > 3 and sys.argv[2] == '--max-size':
        max_size = int(sys.argv[3])

    success = compress_image(image_path, max_size)
    sys.exit(0 if success else 1)
