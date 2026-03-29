---
title: "lossless-claw：让 AI 拥有永不丢失的记忆"
date: 2026-03-29
categories:
  - 技术
tags:
  - openclaw
  - lossless-claw
  - context-management
  - agent
  - LCM
layout: post
image_prompt: "A conceptual visualization of an AI agent with an eternal memory: a digital lobster claw made of light and data streams, holding a glowing crystal orb that contains preserved conversation history, data flows streaming into the orb from multiple directions forming a DAG structure, a vast neural network background with glowing synapses, deep blue and purple color palette, cyberpunk aesthetic with holographic elements, 16:9 aspect ratio, futuristic tech illustration"
image_prompt_file: "assets/prompt/2026-03-29/2026-03-29-lossless-claw-deep-dive.txt"
---

> "信息是熵。" — 克劳德·香农

香农告诉我们，信息即不确定性。而上下文丢失，就是 AI Agent 最大的信息熵增。lossless-claw 试图做的，就是用有向无环图对抗这种熵增，让 AI 的每一次对话都成为可追溯、可逆、可持续积累的记忆。

![lossless-claw 概念图](https://blog.zendong.com.cn/assets/images/2026/2026-03-29-lossless-claw-deep-dive.png)

## 1. 来历：为什么会有这个插件

OpenClaw（绰号"大龙虾"）是 2026 年最受关注的开源 AI Agent 框架，GitHub 星标已突破 28 万。但它有一个天然的缺陷——**上下文窗口有限**。

默认模式下，OpenClaw 和大多数 Agent 一样：当上下文快要满时，会不断截断旧消息。这就像一个人每次只能记住最近 10 分钟的对话，之前的细节全部丢失。研究者称之为 AI 的"失忆症"。

2026 年 3 月，OpenClaw 迎来了一个大版本更新（v3.x），引入了 **Context Engine 插件接口**。这是一个关键的设计变化——它将上下文管理逻辑从核心框架中解耦出来，通过插槽式注册表和配置驱动解析，让开发者可以接入不同的上下文管理策略。

Martian Engineering 团队（就是开发 lossless-claw 的那群人）抓住了这个机会。他们认为：与其在核心框架里修修补补，不如重新设计一套无损的上下文管理机制。于是 **lossless-claw** 诞生了。

---

## 2. 原理：基于 DAG 的无损上下文管理

lossless-claw 的全称是 **LCM (Lossless Context Management) plugin for OpenClaw**，中文可以叫"无损上下文管理插件"。它的核心技术基于 **有向无环图（DAG）**。

### 2.1 滑动窗口的困境

传统 Agent 的上下文管理方式通常是"滑动窗口"——当上下文快满时，丢弃最早的消息，保留最新的。这导致两个问题：

1. **信息丢失**：早期的重要细节无法回溯
2. **语义断层**：被截断的对话可能让 AI 误解后续上下文

### 2.2 DAG 的解决思路

lossless-claw 采用了完全不同的策略。它不再简单丢弃旧消息，而是：

1. **持久化存储**：所有历史消息都被永久存储，而不是截断后丢弃
2. **增量摘要**：当消息量增长时，系统会自动生成摘要节点，压缩历史信息
3. **DAG 结构**：用有向无环图组织消息节点，保留消息间的依赖关系和推理路径
4. **智能检索**：Agent 可以随时回溯到任意历史节点，获取完整细节

你可以把 DAG 想象成一棵不断生长的树——新的对话是树枝，旧的对话不会消失，而是变成年轮。AI 可以在任何时候调取"年轮"中的信息。

### 2.3 核心特性

- **无损**：完整保留每条原始消息，不丢失任何细节
- **可逆**：摘要过程可逆，可以从摘要还原原始信息
- **增量**：不需要每次都重新压缩，只处理增量部分
- **高保真**：保留原始语义和推理路径，AI 不会误解上下文

---

## 3. 核心机制：它是如何工作的

### 3.1 消息存储层

当用户与 OpenClaw 对话时，每条消息都会经过以下处理：

1. **消息捕获**：所有用户消息和 AI 回复都被捕获
2. **节点创建**：每条消息作为一个节点存入 DAG
3. **边建立**：消息间的引用关系、父子关系被记录为图的边
4. **摘要触发**：当节点数量达到阈值时，触发摘要生成

### 3.2 摘要生成策略

这是 lossless-claw 最核心的创新。它不是简单地将 100 条消息压缩成 10 条，而是：

1. **活跃上下文优先**：确保当前对话的核心内容始终在上下文窗口内
2. **语义保留**：摘要时保留关键推理链和重要事实
3. **引用可达**：从摘要节点可以追溯到原始消息节点

### 3.3 上下文窗口管理

对于模型来说，lossless-claw 提供了一个"虚拟上下文窗口"：

- 窗口内是当前最活跃的对话 + 必要的摘要
- 窗口外的信息存在 DAG 中，随时可以调取
- Agent 可以在任何时候发送"回溯请求"，获取历史细节

---

## 4. 安装部署

### 4.1 环境要求

- OpenClaw 版本 >= 3.0（支持 Context Engine 插件接口）
- Node.js >= 18
- 足够的存储空间用于持久化消息

### 4.2 安装步骤

**第一步：安装插件**

```bash
openclaw plugins install @martian-engineering/lossless-claw
```

**第二步：配置 openclaw.json**

在你的 OpenClaw 配置文件 `openclaw.json` 中，找到 `contextEngine` 字段，将其修改为：

```json
{
  "contextEngine": "lossless-claw"
}
```

**第三步：重启服务**

```bash
openclaw gateway restart
```

### 4.3 验证安装

安装完成后，可以运行以下命令验证：

```bash
openclaw plugins list
```

确认 lossless-claw 处于 active 状态即可。

---

## 5. 对 OpenClaw 生态的意义

### 5.1 解决长期记忆问题

这是最直接的价值。OpenClaw 本身是一个强大的 Agent 框架，但缺乏长期记忆能力。lossless-claw 补上了这最后一块短板，让 Agent 可以在多轮对话中持续学习和积累。

### 5.2 插件生态的示范

Context Engine 插件接口的引入，让 OpenClaw 从一个封闭的框架变成了可扩展的平台。lossless-claw 是第一个重量级的实现，证明了插件系统的可行性。可以预见，未来会有更多插件涌现——不同的记忆策略、不同的压缩算法、不同的检索机制。

### 5.3 企业级应用的基础

对于需要在复杂任务中保持上下文的场景（如代码审查、长期项目跟进、多步骤数据分析），无损上下文管理是刚需。lossless-claw 让 OpenClaw 从"玩具"变成"生产力工具"成为可能。

### 5.4 推动 AI Agent 记忆研究

从更宏观的角度看，lossless-claw 代表了一种新的研究方向——**如何在有限的上下文窗口内实现近乎无损的记忆**。它结合了传统信息检索和现代大模型压缩技术，为其他 Agent 框架提供了可借鉴的思路。

---

## 6. 局限与展望

当然，lossless-claw 也不是银弹：

- **存储成本**：所有消息永久存储，长期使用后存储量可观
- **摘要质量**：摘要生成依赖底层 LLM 的能力，摘要质量参差不齐可能影响效果
- **性能开销**：DAG 管理和检索比简单滑动窗口更耗时

这些问题随着技术演进会逐步改善。Martian Engineering 团队也在持续迭代，GitHub 上已有 166+ commits 的活跃维护记录。

---

## 璞奇启示

lossless-claw 对学习类产品的启示在于**"渐进式知识巩固"**机制。

**第一，信息的持久化存储是学习的基础。**

lossless-claw 的核心洞察是：信息不应该被简单地丢弃，而应该被结构化地保留。这对应到学习场景，就是"笔记"的价值——碎片化的知识点需要被持久化存储，才能在需要时被调取。璞奇的练习系统本质上也是一种"知识持久化"——将用户学习的内容转化为可检验的练习记忆。

**第二，摘要（压缩）能力决定了知识的可用性。**

lossless-claw 的摘要不是简单裁剪，而是保留了关键的推理链。学习同样如此——单纯的死记硬背效果有限，只有将知识压缩为可迁移的"心智模型"，才能在新的场景中灵活运用。璞奇的 AI 练习生成，正是试图帮助用户建立这种压缩后的知识结构。

---

## 小结

香农的熵理论告诉我们：信息不会凭空消失，只会转移。lossless-claw 正是这句话的践行者——它不丢弃信息，而是用 DAG 重新组织信息，让 AI 在有限的窗口内看到近乎无损的上下文。

对于 OpenClaw 生态而言，lossless-claw 不只是一个插件，更是一种范式转变的信号：AI Agent 的记忆问题，终于有了靠谱的解决方案。

> 君子生非异也，善假于物也。— 《荀子·劝学》

好的工具，让 AI 善假于物，也让人善假于 AI。

---

## 信息说明

- 关于 lossless-claw 的详细信息，以 [GitHub 仓库](https://github.com/martian-engineering/lossless-claw) 的最新文档为准
- 关于 OpenClaw Context Engine 插件接口，以 [OpenClaw 官方文档](https://github.com/nickar) 为准
