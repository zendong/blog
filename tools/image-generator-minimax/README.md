# MiniMax Token Image Generator

MiniMax Token Plan 监控与图片生成自动化脚本。通过监控 Token Plan 剩余量，在资源充裕时自动调用 MiniMax image-01 模型生成图片。

## 功能特性

- **Token Plan 监控**：自动查询 MiniMax Token Plan 剩余用量
- **智能触发**：剩余 1 小时用量 ≥ 30% 时触发生成
- **Prompt 增强**：调用 MiniMax LLM 将简单描述转化为高质量图像 prompt
- **批量生成**：支持从文本文件读取多条描述
- **自动保存**：生成图片自动保存到带时间戳的目录

## 项目结构

```
tools/minimax-token-image-generator/
├── minimax_image_generator.py   # 主脚本
├── prompts_example.txt           # 示例需求文件
└── README.md                    # 使用说明
```

## 环境要求

- Python 3.x
- `requests` 库
- `anthropic` 库

## 安装依赖

```bash
pip install requests anthropic
```

## 配置

设置 MiniMax API Key：

```bash
export MINIMAX_API_KEY="your-api-key"
```

API Key 获取地址：https://platform.minimaxi.com

## 使用方法

### 准备需求文件

创建文本文件，每行一个图片描述：

```
一只穿着宇航服的橘猫
日落时分的海边小镇水彩风格
未来城市的霓虹灯夜景赛博朋克风格
```

### 运行脚本

**自动模式（检查 Token 剩余量）**：

```bash
python minimax_image_generator.py --prompts prompts.txt
```

**强制执行模式（跳过 Token 检查）**：

```bash
python minimax_image_generator.py --prompts prompts.txt --force
```

**自定义输出目录**：

```bash
python minimax_image_generator.py --prompts prompts.txt --output ./my_images/
```

**指定图片模型**：

```bash
python minimax_image_generator.py --prompts prompts.txt --model image-01-live
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `--prompts` | 需求文件路径（必填） |
| `--force` | 强制执行，跳过 Token 剩余量检查 |
| `--output` | 输出目录（默认 `./generated_images/`） |
| `--model` | 图片模型，可选 `image-01` 或 `image-01-live`（默认 `image-01`） |

## 输出文件

脚本运行后，会在输出目录中生成：

```
generated_images/
└── 20260320_143052/           # 时间戳目录
    ├── 001_一只穿着宇航.png    # 图片文件
    ├── 002_日落时分的海边.png
    ├── 003_未来城市的霓虹.png
    └── generation.log         # 生成日志
```

## Token Plan 说明

- Token Plan 每 5 小时清空一次
- 触发条件：剩余 1 小时内用量 ≥ 30%
- 使用 `--force` 参数可跳过检查强制执行

## API 说明

- 国内版 API Host：`api.minimaxi.com`
- 认证方式：`MINIMAX_API_KEY` 环境变量
- 使用 `Bearer` 认证

## 注意事项

1. 确保 API Key 有足够的权限
2. 脚本会自动添加延迟以避免 API 限流
3. 图片生成可能需要几秒钟时间，请耐心等待
4. 建议先使用 `--force` 模式测试脚本是否正常工作
