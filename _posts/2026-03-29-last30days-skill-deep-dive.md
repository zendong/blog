---
title: "last30days-skill：一键追遍全网30天热点，AI研究助手的瑞士军刀"
date: 2026-03-29
categories:
  - 技术
tags:
  - agent
  - skill
  - ai-agent
  - claude-code
  - research
  - 社交媒体
  - 趋势分析
layout: post
image_prompt: "A futuristic command center interface showing multiple social media platforms converging into a central holographic display: Reddit, X (Twitter), YouTube, TikTok, Hacker News streams flowing into a glowing research synthesis sphere, data visualization graphs and trend lines surrounding it, cyberpunk aesthetic with deep blue and purple neon lighting, sleek dark interface with floating panels, dramatic overhead lighting, 16:9 aspect ratio, cinematic sci-fi interface design"
image_prompt_file: "assets/prompt/2026-03-29/2026-03-29-last30days-skill-deep-dive.txt"
hero_image_ai_generated: true
---

> "独学而无友，则孤陋而寡闻。" — 《礼记·学记》

在 AI 时代，我们面临的信息焦虑比以往任何时候都更严重。每天有无数讨论在 Reddit、X、Hacker News、YouTube、TikTok 上产生又消失，如果只靠个人浏览，根本无法跟上技术迭代的速度。

GitHub 上的一个新项目 [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) 正在解决这个痛点：它让 AI 代理成为一个全能的研究助手，只需一个指令，就能自动抓取指定话题在过去 30 天内全网的热门讨论，合成一份带来源、带评分、带可复用 Prompt 的情报简报。

上线两个月，已斩获 **13,760+ stars**，日均增长 2000+，是今年 AI 开发者工具领域最耀眼的项目之一。

![last30days-skill 多平台研究界面想象图](https://blog.zendong.com.cn/assets/images/2026/2026-03-29-last30days-skill-deep-dive.png)

## 核心原理：多源聚合 + 智能评分

last30days-skill 的架构设计非常清晰，核心是一个 Python 编排脚本（`last30days.py`），负责协调多个数据源：

| 数据源 | 认证方式 | 数据类型 |
|--------|----------|----------|
| Reddit | OpenAI API Key | 帖子标题、评分、评论、热度 |
| X (Twitter) | xAI API Key | 推文内容、转发数、互动量 |
| YouTube | OpenAI API Key | 视频标题、观看量、**字幕摘录** |
| TikTok | ScrapeCreators API | 视频描述、播放量、话题标签 |
| Instagram | ScrapeCreators API | Reels 标题、观看量 |
| Hacker News | Algolia API（免费） | 标题、分数、评论 |
| Polymarket | Gamma API（免费） | 预测市场、赔率、成交量 |
| Bluesky | BSKY_APP_PASSWORD | 帖子内容、互动数据 |
| 通用 Web | WebSearch | 博客、新闻、教程 |

数据聚合后，系统会进行四维评分：

1. **相关性权重**（关键词匹配）
2. **时效性权重**（30天内，越近越高）
3. **参与度权重**（点赞、评论、分享）
4. **跨平台信号**（同一内容多平台出现，权重倍增）

评分后的数据通过去重算法（基于文本相似度）过滤重复内容，最终输出结构化报告。

## 核心功能一览

### 1. 智能意图解析

输入研究请求后，skill 会先解析用户意图：

- **PROMPTING** 模式：用户想要获取可直接使用的 Prompt 示例
- **RECOMMENDATIONS** 模式：用户想要特定工具/产品的推荐列表
- **NEWS** 模式：用户想要了解最新动态
- **COMPARISON** 模式：用户想对比两个事物（如 "Cursor vs Windsurf"）

这种分类决定了后续的信息抓取策略和输出格式。

### 2. 对比模式（Comparison Mode）

这是 v2.9.5 的重磅功能。输入 `/last30days cursor vs windsurf`，系统会：

1. 并行执行两次独立研究（Cursor 研究 + Windsurf 研究）
2. 再执行一次组合研究
3. 输出三份报告 + 一个并排对比表格
4. 给出数据驱动的结论

### 3. 自动保存研究库

每次研究结果都会自动保存到 `~/Documents/Last30Days/` 目录下，按话题命名归档。长期使用下来，你就拥有了一个的个人研究资料库。

### 4. 置信度与来源透明

每个数据点都标注了来源平台和置信度评分，读者可以追溯原始链接，告别"AI 瞎编"的问题。

## 实战案例：研究 "AI Video Generation Tools 2026"

假设你想了解最近一个月 AI 视频生成领域的最新进展，只需输入：

```
/last30days AI video generation tools
```

系统会：

1. 在 Reddit 各子版块搜索 AI video 相关讨论
2. 抓取 X 上相关账号的推文
3. 获取 YouTube 上的教程和演示视频（含字幕摘录）
4. 搜索 TikTok 上的热门 AI 视频话题
5. 查阅 Polymarket 上的相关预测市场（如 "Runway vs Pika 谁能赢"）
6. 补充 Web 端的博客文章和新闻报道

最终输出类似这样的报告：

```
## 研究报告：AI Video Generation Tools
来源：Reddit, X, YouTube, TikTok, HN, Polymarket, Web

### 关键发现
- **Runway Gen-3** 在 Reddit 获得 4.2k upvotes，成为最多讨论的模型
- **Pika 2.0** 在 X 上被 23 位 KOL 同步推荐
- Polymarket 上 "Pika wins 2026" 的赔率达到 1.7（隐含概率 58%）
- YouTube 头部教程平均获取 50k+ 播放量

### 社区情绪
正面 72% | 中立 18% | 负面 10%

### 可用 Prompt 示例
[3-5 个可直接复制到 Runway/Pika 使用的 Prompt]
```

整个过程耗时约 3-5 分钟，相当于一个人花两小时浏览全网的结果。

## 技术架构亮点

### 模块化设计

`scripts/lib/` 下的每个模块职责单一：

- `env.py` — 环境变量与认证
- `dates.py` — 日期范围计算
- `cache.py` — 24 小时 TTL 缓存
- `http.py` — 重试逻辑的 HTTP 客户端
- `models.py` — 模型自动选择（OpenAI/xAI）
- `normalize.py` — 统一数据结构
- `score.py` — 多维评分算法
- `dedupe.py` — 文本相似度去重

这种设计让项目易于测试和维护，也是它能快速迭代的重要原因。

### 零存储依赖

所有输出默认写入 `~/.local/share/last30days/out/`，不需要数据库，不需要 Docker，一个 Python 脚本跑起来就能用。

### 跨 Agent 兼容

项目不仅支持 Claude Code，还提供了 Gemini 扩展（`gemini-extension.json`），以及通用的 CLI 接口，其他 Agent 框架也可以方便地集成。

## 适用场景

last30days-skill 特别适合以下场景：

| 场景 | 价值 |
|------|------|
| **技术选型** | 在选择新框架/工具前，快速了解社区反馈 |
| **竞品分析** | 对比多个产品的口碑和功能差异 |
| **行业观察** | 追踪某个新兴领域的最新动态 |
| **内容创作** | 获取最新的梗、案例、Prompt 灵感 |
| **投资研究** | 结 Polmarlet 的预测市场获取市场情绪 |

## 璞奇启示

last30days-skill 的设计逻辑为学习类产品带来了重要启示。

**第一，信息时效性决定学习效率。**

传统的学习路径是"先系统学习，再应用"，但 AI 时代知识半衰期极短。这提示我们：学习类产品应该加入"30天热点"模块，让用户在学习理论知识的同时，保持对领域动态的敏感度。

**第二，多源交叉验证提升信息质量。**

单一来源的信息容易被算法放大或扭曲，而 last30days-skill 通过跨平台聚合和评分机制，过滤噪音，放大真实信号。学习类产品可以借鉴：不是给用户更多信息，而是帮用户找到**经过验证的高质量信息**。

**第三，主动推送优于被动搜索。**

当用户需要"研究"时，工具已经主动整理好了简报。这种"主动服务"模式，比让用户在海量信息中自己摸索，效率提升何止十倍。

---

## 信息说明

- GitHub 仓库：[https://github.com/mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)
- 项目文档：[https://github.com/mvanhorn/last30days-skill/blob/main/README.md](https://github.com/mvanhorn/last30days-skill/blob/main/README.md)
- ClawHub 地址：[https://clawhub.ai/skills/last30days-official](https://clawhub.ai/skills/last30days-official)
- 安装命令：`/plugin marketplace add mvanhorn/last30days-skill`
- 数据统计截至 2026-03-29
