---
title: "DeepTutor 与 nanobot，港大 HKUDS 的学习 Agent 技术栈"
date: 2026-04-11
categories:
  - 技术
tags:
  - ai-agent
  - deeptutor
  - nanobot
  - hku
  - openclaw
  - 璞奇app
layout: post
image_prompt: "Bright cartoon flat vector illustration, AI education theme, friendly small robot tutors helping students at desks in a modern classroom, warm orange yellow and light blue palette, stylized faceless characters, clean minimalist, positive mood, no text, 16:9"
image_prompt_file: "assets/prompt/2026-04-11/2026-04-11-deeptutor-nanobot-analysis.txt"
hero_image_ai_generated: true
---

> "教育不是灌满一桶水，而是点燃一把火。" — 威廉·巴特勒·叶芝（William Butler Yeats）

![首图](/assets/images/2026/2026-04-11-deeptutor-nanobot-analysis.png)

香港大学数据智能实验室（[HKUDS](https://github.com/HKUDS)）在 2025 年底到 2026 年春接连开源了两个很能打的项目，个性化学习助手 [DeepTutor](https://github.com/HKUDS/DeepTutor) 与超轻量个人智能体 [nanobot](https://github.com/HKUDS/nanobot)。官方 README 写得很直白，TutorBot 这一层**由 nanobot 驱动**。一条从「底层运行时」到「学习场景产品」的链路人就搭好了，值得按工程视角拆开看。

下文数据与版本说明以 **2026 年 4 月中旬** 查阅 [GitHub 仓库](https://github.com/HKUDS/DeepTutor)与 [Release 页](https://github.com/HKUDS/DeepTutor/releases)为准，星标数会随时间变动。

## DeepTutor 在解决什么问题

定位是 **Agent-Native Personalized Tutoring**，即把智能体当成一等公民来做个性化助学，而不是在聊天窗口上贴一层「答疑」。核心卖点在官方 [Key Features](https://github.com/HKUDS/DeepTutor#-key-features) 里写得很集中，概括起来是这几块：

- **统一聊天工作区**，多种模式（日常对话、深度解题、测验生成、深度研究、数学动画等）共用同一条上下文，避免换功能就丢线程。
- **个人 TutorBot**，每个机器人有独立工作区、记忆与技能，可提醒、可成长；底层写明 **Powered by nanobot**。
- **协作式 Markdown 编辑（Co-Writer）**、**引导式学习（Guided Learning）**、**知识中心与持久记忆** 等，把材料与对话绑在同一套学习闭环里。
- **面向智能体的 CLI**，方便脚本和别的 Agent 调用（仓库里也有 `SKILL.md` 一类约定）。

协议为 **Apache-2.0**。仓库新闻里提到 2026 年 2 月曾在约 **39 天**内达到 **10k** 星标量级，属于社区热度很高的那一档；具体数字以当时页面为准。

### 版本线（简述）

2026 年 4 月初的 [v1.0.0-beta.1](https://github.com/HKUDS/DeepTutor/releases/tag/v1.0.0-beta.1) 起了一次**自底向上的架构重写**，说明里提到约 **20 万行**量级的新代码、双层插件模型（Tools + Capabilities）、TutorBot、CLI 与 SDK 等。之后仍有连续小版本（如 **v1.0.1**、**v1.0.2**）做检索整合、前端资源泄漏修复、可视化与测验去重等，说明项目仍在快速迭代。**默认本地 Web 入口**在文档里常见为 `http://localhost:3782`，以当前仓库说明为准。

### 上手方式（保留官方路径）

交互式安装仍推荐 `python scripts/start_tour.py`；容器路线可用仓库提供的 `docker-compose` 变体。细节以 README 为准，此处不复制易过期的每一步参数。

## nanobot 是什么，和 OpenClaw 什么关系

[nanobot](https://github.com/HKUDS/nanobot) 自述是受 [OpenClaw](https://github.com/openclaw/openclaw) 启发的**超轻量个人智能体**，**MIT** 协议。README 里有一句常被引用的话，大意是用**少得多的代码行数**交付核心智能体能力（仓库里还提供了自行统计核心行数的脚本名，便于核对，而不是口头吹牛）。

它和「纳米机器人」无关，名字容易误读，心里要先翻译成**轻量运行时**。特性上包括多聊天渠道、MCP、心跳与定时任务、沙箱、Python SDK、兼容 OpenAI 的 HTTP 接口等；**2026 年 4 月 5 日**发布的 **v0.1.5** 在发行说明里强调了长任务稳定性、**Dream** 两阶段记忆、沙箱与编程 Agent SDK 等，适合作为 TutorBot 这种**长期在线、多通道**场景的底座。

## 两者如何拼在一起

用盖房子类比，nanobot 更像**地基与管线**（会话、记忆、渠道、工具与技能加载），DeepTutor 在上层叠**学习产品与工作流**（统一工作区、知识库、引导学习与测验等）。官方在 TutorBot 一条里直接链到 nanobot，等于把集成关系写死在产品叙事里，而不是事后附会。

若你关心实现细节，可以在 nanobot 仓库里顺着 `agent/`、记忆与渠道相关目录读；DeepTutor 侧则关注 TutorBot 与工作区、CLI、SDK 的边界。对做教育类产品的人来说，这条链路的启发是，**先有一个可靠的智能体运行时，再把「助学」做成可组合能力**，而不是反过来。

## 近期路线（来自公开 Roadmap 摘要）

两边都在补**多用户与工程化**（例如登录、主题、文档站、知识库引擎升级等），nanobot 一侧也在推进多模态、更强规划与更多第三方集成。具体排期以各自 **Issues / Discussions** 为准，这里只提示「仍在高速演进」，集成前锁版本、读发行说明。

---

对做练习类、伴学类应用的人来说，这套栈的意义在于，**个性化**不必只等于「多记几个用户字段」，而是可以有**独立记忆、渠道触达、可插拔技能**的一条完整路径；璞奇若往「练与学」一体化走，值得对照自己的边界做技术选型，而不是照搬某一版插件接口。

> **璞奇启示**
>
> 1. 练习与伴学若要**持续**，需要可审计的记忆与触达通道，轻量智能体运行时 + 清晰技能边界，比单页聊天更易演进。
> 2. 生成题目时，可把「提取旧知识、间隔复习」设计成与 TutorBot 提醒同频的闭环，而不只做单次出题。
> 3. 对接开源栈前先**锁版本、读 Release**，重写期与高频发版期接口变动大，避免生产环境 silent break。
