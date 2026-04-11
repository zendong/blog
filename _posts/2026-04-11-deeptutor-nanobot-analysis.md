# DeepTutor 16k Stars！港大开源的 AI 导师系统，还有纳米机器人框架？

> 📅 2026年4月11日
> 🏷️ AI导师 · Agent框架 · 开源项目 · TutorBot

---

最近香港大学数据科学实验室（HKUDS）接连放出了两个重磅开源项目，一个三个月狂揽近 16k Stars 的 AI 导师系统 DeepTutor，一个号称"99% 更少代码"的纳米机器人框架 nanobot。巧的是，DeepTutor 旗下最核心的功能 TutorBot，正是用 nanobot 作为底层引擎驱动的。

这两个项目放在一起，形成了一套从底层 Agent 框架到上层应用场景的完整技术栈，值得单独拎出来好好拆解一番。

![首图](2026-04-11-deeptutor-nanobot-cover.png)

---

## 一、DeepTutor：三个月 16k Stars 的爆发式增长

先说 DeepTutor。

根据 GitHub 数据，`HKUDS/DeepTutor` 目前拥有约 **15,959 Stars**、**2,098 Forks**，项目采用 Apache-2.0 开源协议。从 2025 年 12 月 29 日正式发布，到 2026 年 2 月 6 日突破 10k Stars，仅用了 **39 天**。这个速度即便放在 AI 开源项目里也算现象级的。

DeepTutor 对自己的定位是：**Agent-Native Personalized Tutoring**——原生 Agent 化的个性化导师系统。这句话里有两层意思：

1. **不是普通的聊天机器人**，而是一个真正具有持久记忆、主动干预能力的 AI 导师；
2. **个性化**，每个导师 Bot 可以有不同的"灵魂"（Soul）、记忆和工作空间。

### 核心功能一览

| 功能模块 | 说明 |
|:---|:---|
| **TutorBot** | 持久化的自主 AI 导师，每个 Bot 有独立记忆、人格和工具集 |
| **Co-Writer** | 内嵌 AI 协作的 Markdown 编辑器，选中文字即可重写/扩展/缩写 |
| **Guided Learning** | 将文档转化为可视化、分步骤的学习旅程 |
| **Knowledge Hub** | PDF/Markdown/TXT 上传，构建 RAG 知识库 |
| **Persistent Memory** | 跨会话持久化的学习者画像与进度追踪 |
| **Deep Solve** | 多 Agent 协作的问题解决，带精确溯源 |
| **Math Animator** | 用 Manim 将数学概念转化为动态动画 |

值得特别关注的是，2026 年 4 月 4 日 DeepTutor 刚发布了 **v1.0.0**，这是一个从零开始的重写版本，据说代码量达到了 **~20 万行**，带来了 TutorBot、Agent-Native CLI、Python SDK 等一系列新特性。

### 快速上手

```bash
# 方式一：一条命令启动引导安装（推荐）
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
conda create -n deeptutor python=3.11 && conda activate deeptutor
python scripts/start_tour.py

# 方式二：Docker 一键部署
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env  # 填入你的 API Key
docker compose -f docker-compose.ghcr.yml up -d
```

服务启动后访问 `http://localhost:3782` 即可。

---

## 二、nanobot：DeepTutor TutorBot 的核心引擎

如果说 DeepTutor 是一座精心建造的房子，那么 nanobot 就是那块打好的地基。

nanobot 的 GitHub 仓库是 `HKUDS/nanobot`，采用 MIT 协议。它的自我介绍非常直白——**Ultra-Lightweight Personal AI Agent**，即超轻量级个人 AI Agent，并在 README 里非常自信地写了一句：

> ⚡️ Delivers core agent functionality with **99% fewer lines of code**.

99% 更少代码——这个说法来自 DeepTutor 团队对自己的要求，也确实反映了 nanobot 在架构上的极致追求。nanobot v0.1.5 于 2026 年 4 月 5 日发布，包含了更稳定的长时任务、**Dream 二阶段记忆**、生产级沙箱隔离和编程 Agent SDK。

### nanobot 的核心特性

| 特性 | 说明 |
|:---|:---|
| **超轻量** | 核心 Agent 代码量极小，适合稳定运行长时间任务 |
| **多渠道接入** | Telegram、Discord、WhatsApp、WeChat、飞书、钉钉、Slack、Email、QQ 等 |
| **MCP 支持** | 可接入 Model Context Protocol 生态，连接外部工具服务器 |
| **Python SDK** | 可以作为库直接调用，无需 CLI |
| **OpenAI-Compatible API** | `nanobot serve` 即可暴露 `/v1/chat/completions` 接口 |
| **Dream 记忆系统** | 二阶段记忆整合，定期压缩历史信息，保留关键知识 |
| **Heartbeat 主动唤醒** | 定期检查任务文件，主动向用户推送提醒 |
| **Skill 加载** | 支持给 Agent 安装新技能，类似 LangChain Tool 概念但更轻量 |
| **沙箱安全** | 可选 bubblewrap 隔离，保护系统不被恶意指令影响 |

### 快速体验

```bash
# 安装（推荐 uv，快速稳定）
uv tool install nanobot-ai

# 初始化
nanobot onboard

# 开始对话
nanobot agent
```

如果要在特定渠道（比如 Telegram）运行，只需要额外配置一个 bot token：

```json
// ~/.nanobot/config.json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  },
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxx"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  }
}
```

```bash
nanobot gateway  # 启动网关，对接配置好的渠道
```

### 支持的 LLM 提供商（部分）

| 提供商 | Binding | 备注 |
|:---|:---|:---|
| OpenAI | `openai` | 直连 |
| Anthropic | `anthropic` | Claude 直连 |
| DeepSeek | `deepseek` | 性价比高 |
| Groq | `groq` | 免费额度 |
| DashScope | `dashscope` | 通义千问 |
| MiniMax | `minimax` | 国内 |
| Ollama | `ollama` | 本地模型 |
| vLLM | `vllm` | 自托管 |
| Azure OpenAI | `azure_openai` | 企业版 |
| 30+ 更多 | — | 详见官方 README |

---

## 三、技术架构与创新点解析

### 3.1 nanobot 的架构设计

nanobot 的项目结构非常有条理，核心逻辑集中在 `agent/` 目录：

```
nanobot/
├── agent/           # 🧠 核心 Agent 逻辑
│   ├── loop.py     #    Agent 循环（LLM ↔ 工具执行）
│   ├── context.py  #    Prompt 构建
│   ├── memory.py   #    持久化记忆
│   ├── skills.py   #    Skill 加载器
│   ├── subagent.py #    后台任务执行
│   └── tools/      #    内置工具（含 spawn）
├── skills/         # 🎯 打包的 Skills（github, weather, tmux...）
├── channels/       # 📱 聊天渠道集成（支持插件化）
├── bus/            # 🚌 消息路由
├── cron/           # ⏰ 定时任务
├── heartbeat/      # 💓 主动唤醒
├── providers/      # 🤖 LLM 提供商
├── session/        # 💬 会话管理
├── config/         # ⚙️ 配置
└── cli/            # 🖥️ 命令行入口
```

**Agent Loop** 是核心循环——接收消息 → 构建 Context → 调用 LLM → 执行工具 → 写回记忆 → 返回结果。工具包括：文件读写、Shell 执行、Web 搜索、MCP 工具、以及最关键的 `spawn`（可以派生子 Agent）。

**Dream 记忆系统**是 nanobot 的一大亮点。传统的 Agent 记忆通常是"所有历史全部塞进 Context"，这在长对话中会严重消耗 token。Dream 系统采用了两阶段策略：

1. **第一阶段**：在每次交互中实时写入 `memory/history.jsonl`（追加式摘要历史）
2. **第二阶段**：定期调用 Dream 进程，将历史信息整合进 `SOUL.md`、`USER.md`、`memory/MEMORY.md` 等结构化文件，实现长期知识的压缩存储

这和人类记忆"工作记忆 → 睡眠期间整合为长期记忆"的过程非常类似，名字起得很有味道。

### 3.2 DeepTutor TutorBot 的 Agent 架构

TutorBot 是 DeepTutor 中最能体现 Agent 原生思维的功能。它的架构大致如下：

```
TutorBot
├── Soul Template       # 人格定义（SOUL.md）
├── Memory              # 独立记忆空间
├── Session            # 独立会话管理
├── Tools              # 完整工具集（RAG、搜索、代码执行...）
├── Heartbeat          # 主动提醒系统
├── Multi-Channel      # 跨平台接入
└── ⬇️ 底层引擎：nanobot
```

每个 TutorBot 是一个完全独立的 Agent 实例，拥有：

- **独立的 Soul 文件**：定义导师的性格、语气、教学哲学。内置 Socratic（苏格拉底式追问）、Encouraging（鼓励型）等模板，也可以完全自定义
- **独立的工具集**：可以访问 DeepTutor 全部工具，包括 RAG 检索、代码执行、Web 搜索、学术论文搜索、深度推理等
- **主动 Heartbeat**：定期检查学习进度、推送复习提醒，即使你不主动打开 App
- **跨渠道存在**：同时运行在 Telegram、Discord、飞书、微信等多个平台

创建自己的 TutorBot 只需要一行命令：

```bash
# CLI 方式
deeptutor bot create math-tutor --persona "苏格拉底式数学导师，擅长追问式引导"

# Web 界面方式更直观：直接点击创建，填写人设描述
```

### 3.3 DeepTutor 的统一工作空间

DeepTutor 的另一个架构亮点是**五模式统一上下文**：

| 模式 | 典型场景 |
|:---|:---|
| **Chat** | 日常问答，灵活组合 RAG/搜索/代码工具 |
| **Deep Solve** | 复杂问题，多 Agent 协作规划→调查→解决→验证 |
| **Quiz Generation** | 基于知识库自动生成评测题目 |
| **Deep Research** | 主题研究，多 Agent 并行 RAG+搜索+论文，最后汇总报告 |
| **Math Animator** | 将数学概念用 Manim 动画化 |

这五个模式**共享同一个上下文线程**——你可以先 Chat 快速提问，发现问题复杂后升级到 Deep Solve，做完后生成 Quiz 自测，最后开启 Deep Research 深入研究。所有对话历史、RAG 引用、知识库上下文全程不丢失。

---

## 四、与璞奇 App 的结合可能性

璞奇 App 专注于**生成练习**，而练习的本质是一种**信息采集和娱乐交互**的过程——它不一定需要有对错之分，可以仅仅是客观或非客观的信息采集，带有游戏化性质的互动体验。

从这个角度看，DeepTutor 体系（特别是 TutorBot + nanobot）给璞奇提供了一条很有意思的技术路线参考：

### 4.1 TutorBot 作为"练习导师"

DeepTutor 的 TutorBot 天然就是"导师"角色。将璞奇的练习能力嫁接到 TutorBot 上，可以实现：

```
用户 → TutorBot（苏格拉底式追问）
     → 触发练习生成（璞奇内核）
     → 练习题推送（多渠道：Telegram/飞书/微信）
     → 用户作答 → 即时反馈 + 记忆更新
```

每个学生的练习记录、错题分布、知识点掌握情况，都可以作为 TutorBot 记忆的一部分，驱动后续更精准的练习推荐。

### 4.2 nanobot 作为底层 Agent 引擎

nanobot 的架构足够轻量级，对资源要求低，适合嵌入璞奇的后端体系。它提供了开箱即用的：

- **多渠道消息接入**（Telegram/飞书/微信等），璞奇的练习推送可以复用这套基础设施
- **Skill 机制**，璞奇的练习生成能力可以封装为一个 nanobot Skill，其他 Agent 可以直接调用
- **Python SDK**，直接 import 进璞奇的服务端代码，不需要单独起进程
- **OpenAI-Compatible API**，如果璞奇未来想做 Agent-to-Agent 的互操作，门槛极低

### 4.3 互补的哲学

璞奇"练习不一定有对错"的理念，实际上和 DeepTutor 强调的**个性化学习**高度契合。DeepTutor 的 Knowledge Hub + Persistent Memory 可以完整记录一个学习者在璞奇的所有练习轨迹；TutorBot 可以根据这些轨迹，主动生成适合该学习者当前状态的练习。

两者结合的想象空间很大：一个学生可能早上在 DeepTutor 的 Guided Learning 里学习"光的折射"，下午 TutorBot 通过飞书推送了一道璞奇生成的折射相关练习题——而且这道题是根据这个学生过去三天在光学知识点上的薄弱环节量身定制的。

---

## 五、值得关注的近期动态

### DeepTutor Roadmap

| 状态 | 里程碑 |
|:---:|:---|
| 🔜 | **登录认证系统** — 公网部署的多用户支持 |
| 🔜 | **主题与外观定制** — 多样化 UI 皮肤 |
| 🔜 | **LightRAG 集成** — 高级知识库引擎 |
| 🔜 | **文档站点** — 完整使用文档和 API 参考 |

### nanobot Roadmap

| 状态 | 里程碑 |
|:---:|:---|
| 🔜 | **多模态** — 支持图像、语音、视频理解 |
| 🔜 | **长期记忆** — 永久记住关键上下文 |
| 🔜 | **更强推理** — 多步规划和反思能力 |
| 🔜 | **更多集成** — 日历等工具接入 |

---

## 六、总结

DeepTutor 和 nanobot 的组合，展示了一条从底层轻量 Agent 框架到上层个性化学习应用的完整技术路径：

- **nanobot** 是地基——极简代码量、多渠道接入、模块化工具、MCP 支持、生产级的安全和稳定性
- **DeepTutor** 是上层建筑——基于 nanobot 构建了 TutorBot、Co-Writer、Guided Learning 等一系列学习场景
- 两者都是 **HKUDS 团队**的作品，Apache-2.0 / MIT 双协议，开源姿态非常友好

对璞奇 App 而言，这套技术栈提供了**多渠道练习推送能力**、**个性化导师 Agent 引擎**和**可插拔的练习 Skill** 三条现成路径。如果未来璞奇要走出"做题 → 对答案"的传统框架，向"AI 导师 + 练习 + 记忆"一体化的方向发展，DeepTutor/nanobot 体系是非常值得研究和借鉴的范式。

---

## 参考链接

| 资源 | 地址 |
|:---|:---|
| DeepTutor GitHub | https://github.com/HKUDS/DeepTutor |
| nanobot GitHub | https://github.com/HKUDS/nanobot |
| DeepTutor v1.0.0 Release | https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0 |
| nanobot v0.1.5 Release | https://github.com/HKUDS/nanobot/releases/tag/v0.1.5 |
| HKUDS 生态（LightRAG/AutoAgent） | https://github.com/HKUDS |

---

*本文相关数据截至 2026 年 4 月，GitHub Stars 数量可能有实时变动，请以实际仓库数据为准。*
