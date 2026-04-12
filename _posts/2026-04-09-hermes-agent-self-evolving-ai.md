---
title: "Hermes Agent：唯一会自我进化的 AI Agent 深度解析"
date: 2026-04-09
categories:
  - 技术
tags:
  - hermes-agent
  - nous-research
  - ai-agent
  - self-improvement
  - skill-system
layout: post
image_prompt: "A futuristic AI agent visualization: a sleek holographic neural network figure with glowing synaptic connections emanating from its core, the figure stands at the center of an expanding spiral of skill cards and knowledge nodes that are progressively building outward, digital consciousness ascending through layers of increasingly complex patterns, deep indigo and electric cyan color palette, neon-lit futuristic atmosphere with ambient particles, cinematic composition with dramatic depth of field, 16:9 aspect ratio"
image_prompt_file: "assets/prompt/2026-04-09/2026-04-09-hermes-agent-self-evolving-ai.txt"
hero_image_ai_generated: true
---

> "为学日益，为道日损。" — 《道德经》

2026 年 2 月，Nous Research 发布了 Hermes Agent。官方给它的定位是「自我改进型 AI Agent 框架」。用大白话翻译：它不是一个绑定在 IDE 里的代码补全工具，也不是一个单纯的聊天机器人。它是一个部署在你自己服务器上的、具备持续学习能力的 AI 助手。

这句话里有三个关键词：**部署在自己服务器**、**持续学习**、**AI 助手**。三个词组合在一起，意味着你拥有了一个会随着使用而变得越来越懂你、越来越能干的 AI 队友。

![首图](https://blog.zendong.com.cn/assets/images/2026/2026-04-09-hermes-agent-self-evolving-ai.png)

## 一、核心原理：内置学习闭环

传统 Agent 大多是一个「执行器」——你给指令，它干活，干完就结束。下一次遇到同样的任务，它仍然要从零开始理解上下文。Hermes Agent 试图打破这个循环，它的核心理念是：**让 Agent 在工作的过程中形成记忆，从记忆里提取技能，用技能加速下一轮工作**。

这套机制可以拆解为四个环节：

**第一，自动创建技能。** 当 Hermes Agent 完成一个复杂任务后，它会自动生成一个可复用的技能（Skill），保存到本地。这个技能不是简单的脚本，而是一段结构化的经验记录：任务是什么、用了什么工具组合、如何拆解步骤。

**第二，技能在使用中自我改进。** 每当调用一个已有技能，Agent 会观察这次执行的效果。如果效果好，技能的权重会微调；如果效果不理想，Agent 会在下次执行时尝试不同的路径。技能不是一次性生成的，而是随着使用次数增加而优化的。

**第三，记忆持久化。** Hermes Agent 有一套「记忆提醒」机制，会定期提示自己保存重要信息。这不是简单的对话历史记录，而是一个主动整理、主动归档的过程。Agent 会在工作间隙检查：有哪些新学到的东西需要写进去？有哪些过时的信息需要清理？

**第四，跨会话搜索。** 使用 FTS5（SQLite 全文搜索）配合 LLM 总结，实现跨会话的信息召回。你问过一个问题的背景，Agent 会在后续对话中自动联想到那段记忆，而不是等你重新解释。

这四个环节构成一个闭环：执行 → 学习 → 沉淀 → 召回 → 再执行。传统 Agent 每次都是从零开始的单次执行，Hermes Agent 则是一条持续向前的学习轨迹。

## 二、关键特性解析

### 1. 技能生态系统

根据 v0.2.0（2026.3.12）的 release note，Hermes Agent 已经拥有 **70+ bundled and optional skills**。这些技能覆盖了代码开发、数据处理、系统运维等多个领域。

更重要的是，这些技能遵循 **agentskills.io 开放标准**。这意味着技能可以跨 Agent 迁移，不被锁定在某一个框架里。

### 2. 多模型支持

Hermes Agent 不绑定任何模型提供商。它支持：

- Nous Portal
- OpenRouter（200+ 模型）
- z.ai / GLM
- Kimi / Moonshot
- MiniMax
- OpenAI
- Anthropic
- 自定义端点

切换模型只需一条命令 `hermes model`，无需改动代码。这种灵活性在实际生产中很重要——你可以根据任务类型选择性价比最高的模型。

### 3. 多平台消息网关

v0.2.0 带来了完整的消息网关，支持：

- Telegram
- Discord
- Slack
- WhatsApp
- Signal
- Email（IMAP/SMTP）
- Home Assistant

统一的会话管理，支持媒体附件和凭证解析。这意味着你可以在任何惯用的平台上与 Hermes Agent 交互，数据和上下文完全同步。

### 4. ACP 服务器与编辑器集成

通过 Agent Communication Protocol（ACP），Hermes Agent 可以与主流编辑器深度集成：

- VS Code
- Zed
- JetBrains

这让 Agent 能够理解你当前编辑的代码、项目的上下文，提供更精准的协助。

### 5. 内置定时任务

Hermes Agent 包含一个 cron 调度器，可以：

- 发送每日报告
- 执行夜间备份
- 运行每周审计
- 按设定时间自动唤醒并执行任务

这让 Agent 具备了「全天候值班」的能力——你设置好规则，剩下的由 Agent 自动完成。

## 三、与传统 Agent 的对比

这里以 2026 年同样备受关注的 OpenClaw 为参照对象，进行一个结构性对比：

| 维度 | Hermes Agent | OpenClaw |
|------|-------------|----------|
| **核心理念** | 自我进化，技能随使用增长 | 自主执行，全天候运行 |
| **学习机制** | 内置学习闭环，自动创建和改进技能 | 依赖 lossless-claw 做会话持久化 |
| **记忆系统** | Agent 主动管理记忆，定期归档与召回 | 会话层（LFM）+ 笔记层（Hybrid）双层 |
| **技能生态** | 70+ 内置技能，agentskills.io 兼容 | 插件系统，lossless-claw 等 |
| **多模型** | 广泛支持，切换灵活 | 支持多 provider |
| **多平台** | 完整消息网关（6+ 平台） | 专注终端与编辑器集成 |
| **定时任务** | 内置 cron 调度器 | 依赖外部调度或手动触发 |
| **适用场景** | 需要持续学习与适应的复杂助手 | 需要自主执行与自动化的任务 |

两者的设计哲学有本质差异：**OpenClaw 是一个「能干活的助手」**，擅长自动执行和跨平台自动化；**Hermes Agent 是一个「会成长的队友」**，擅长在重复任务中积累经验、优化表现。

打个比方：OpenClaw 像一个从不疲倦的实习生，严格按指令执行；Hermes Agent 像一个会反思的同事，每次完成任务后都会想「下次怎么做得更好」。

## 四、对 AI Agent 发展的启示

### 1. 从「执行」到「学习」是关键跃迁

过去一年，大多数 Agent 框架的优化方向是「让 Agent 能够调用更多工具」「让上下文窗口更大」「让推理更准确」。这些改进都在提升单次执行的能力。但 Hermes Agent 指向了一个不同的方向：**Agent 应该具备跨任务的学习能力，而不仅仅是单次执行的能力**。

这对产品设计有重要启示：如果一个 AI 助手用得越久就越懂你，它的价值是随时间递增的；而一个每次都从零开始的助手，它的价值是恒定的。用户会选择哪个？

### 2. 技能作为记忆的载体

Hermes Agent 选择用「技能」而非「对话记录」作为记忆的载体，这个设计值得思考。对话记录是原始数据，技能是加工后的知识。原始数据量大但检索成本高；技能精炼但有信息压缩损失。Hermes Agent 的做法是：用技能沉淀高频模式，用 FTS5 搜索处理低频信息。这种分层处理在人类学习里也能找到对应——大脑既会形成习惯性反应（类似技能），也会保留可检索的叙事记忆。

### 3. 开放标准是生态健康的前提

Hermes Agent 兼容 agentskills.io 开放标准，意味着技能可以在不同 Agent 框架之间迁移。这对整个生态是健康的——开发者不需要为每个框架重复造轮子，用户也不会被锁定在某一个平台。

### 4. 多平台是 Agent 的「身体」

一个只活在终端里的 Agent，它的「身体」是受限的。Hermes Agent 通过多平台消息网关，让自己可以在用户常用的任何地方存在。这提醒我们：**Agent 的价值不仅取决于它有多聪明，还取决于它能在多少场景里触达用户**。

## 五、局限与待观察

Hermes Agent 并不是完美的。它的学习机制依赖 Agent 自己对任务成功的判断——这意味着如果 Agent 对「什么是好结果」的判断出错，技能也会往错误方向优化。另外，自我进化带来的一个隐患是：**用户可能不清楚 Agent 到底学到了什么、改变了什么**，透明性是一个需要持续关注的点。

此外，70+ 技能的生态虽然丰富，但技能质量参差不齐的风险也随之增加。如何建立技能的评估与筛选机制，是规模化的前提。

## 小结

Hermes Agent 的出现，标志着一个新类别的 AI Agent 的确立：不是「执行者」，而是「学习者」。它不追求单次执行的最优解，而是追求跨任务的持续优化。这条路能不能走通，需要看它在真实场景里的长期表现。但至少，它让「AI Agent 会随着使用而进化」这件事，从概念变成了可体验的现实。

---

## 璞奇启示

**第一，学习闭环比信息量更重要。** Hermes Agent 的核心洞察是：不在于你存了多少知识，而在于你有没有一个机制让知识持续被使用和优化。这对学习类产品同样适用——与其堆砌内容，不如设计一个「学→练→反馈→改进」的闭环，让用户在每个环节都有事可做、有迹可循。

**第二，技能积累是长期价值的锚点。** 如果一个学习工具用得越久就越懂你、越能给出精准的练习，它对用户的粘性是自然增长的。Hermes Agent 通过「技能」来沉淀经验，学习类产品也可以通过「用户画像」和「掌握度模型」来实现类似的积累——让工具本身成为用户学习历程的一部分，而不仅仅是旁观者。

---

## 信息说明

- Hermes Agent 仓库：<https://github.com/NousResearch/hermes-agent>
- Hermes Agent v0.2.0 Release：<https://github.com/NousResearch/hermes-agent/releases/tag/v2026.3.12>
- agentskills.io 开放标准：<https://agentskills.io>
