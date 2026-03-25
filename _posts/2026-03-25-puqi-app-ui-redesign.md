---
title: "璞奇 APP 交互改版：从聊天工具到内容工作台"
date: 2026-03-25
categories:
  - 产品
tags:
  - 璞奇app
  - ui设计
  - 产品设计
  - 交互设计
  - 人工智能
layout: post
image_prompt: "A futuristic mobile app interface transformation concept: left side showing a cluttered traditional chat interface with multiple toolbars and buttons, right side showing a clean minimalist conversational interface with floating action buttons and glassmorphism design, abstract representation of AI conversation flow as glowing particles connecting user and AI, soft blue and green gradient background suggesting clarity and focus, minimalist futuristic aesthetic, clean lines and smooth curves, no text characters, digital illustration style depicting UI/UX evolution"
image_prompt_file: "assets/prompt/2026-03-25/2026-03-25-puqi-app-ui-redesign.txt"
---

> "为学日益，为道日损。" — 《道德经》

UI 改版的过程，本质上是一个不断做减法的过程。这次璞奇的改版，终于让我下定决心：把「聊天工具」彻底升级为「内容工作台」。

![首图](https://blog.zendong.com.cn/assets/images/2026/2026-03-25-puqi-app-ui-redesign.png)

**新旧版 UI 对比**：

![新版 UI 设计](https://blog.zendong.com.cn/assets/images/2026/2026-03-25-puqi-app-ui-redesign-new.png)

## 改版背景：理工思维的局限

璞奇最早的版本，是我用「理工思维」设计的。功能堆叠、界面繁复，每次迭代都在做加法——加功能、加按钮、加选项。加到后来，连我自己都觉得「不忍直视」。

问题的根源不在于功能多少，而在于呈现方式。用户打开 APP，看到的是一座功能超市，而不是一个聚焦的学习场景。

![旧版 UI 界面](https://blog.zendong.com.cn/assets/images/2026/2026-03-25-puqi-app-ui-redesign-old.png)

上图是经过多次优化后的旧版界面。可以看到：顶部搜索框、多个功能入口、横向滚动的卡片、内容分区……信息密度不可谓不高，但对于一个学习场景来说，用户的注意力被严重分散了。

## 新版设计：以对话为核心

这次改版，我参考了蚂蚁「阿福」的设计理念，核心逻辑只有一条：**把功能嵌入对话，让对话本身成为工作台**。

**「对话即界面」**——这是新版的底层设计哲学。

### 简化原则

新版遵循三个简化原则：

**第一，能藏起来的就从主界面移走。**

之前的版本恨不得把所有功能都摆在首页。新版只保留最核心的对话入口，所有工具通过对话中的快捷按钮来触发。用户不需要的功能，就不该出现在他的视野里。

**第二，用多变的格式提升效率。**

当纯文字对话效率低下时，用富媒体格式来提升信息传递效率。练习卡片、选项胶囊、进度展示——这些格式不再是「功能入口」，而是「对话内容」的一部分。

**第三，让 AI 引导交互。**

旧版是「用户找功能」，新版是「AI 推功能」。对话开场由 AI 主导，根据用户目标推荐合适的练习模式，而不是让用户在茫茫功能海中自己摸索。

### 界面变化

对比新旧两版，最明显的变化是：

| 维度 | 旧版 | 新版 |
| --- | --- | --- |
| 入口呈现 | 多入口卡片流 | 单对话流 |
| 功能触发 | 用户主动点击 | AI 引导推荐 |
| 视觉层次 | 平铺展开 | 沉浸聚焦 |
| 交互核心 | 工具按钮 | 对话输入框 |

## 技术实现：GenUI 的应用

这次改版的技术核心是 GenUI——用 AI 生成界面。

具体来说，当用户在对话中表达需求时，AI 不仅返回文字内容，还会动态生成对应的交互组件。比如用户说「我想做成语练习」，AI 会生成一个包含「流炼练习」卡片的回复，用户直接点击卡片即可进入练习。

这种设计的好处是：
- **界面即内容**：不再有「界面层」和「内容层」的割裂
- **动态适配**：同一个对话流可以承载完全不同的交互形态
- **减法开发**：不需要为每个功能单独设计界面，开发成本大幅降低

## 后续规划：技能中心

框架搭好了，后续的扩展就有了基础。

下一步的计划是在服务端持续叠加 SKILL（技能）体系。简单说，就是让 AI 不仅能生成练习，还能调用各种外部工具来完成更复杂的任务。

比如：
- 一个 SKILL 负责「出题」
- 一个 SKILL 负责「批改」
- 一个 SKILL 负责「知识图谱构建」
- 一个 SKILL 负责「学习路径规划」

这些 SKILL 通过对话串联起来，形成一个完整的学习工作流。用户不需要关心背后调用了多少工具，只需要在对话中表达目标，AI 协调各种技能来完成。

这才是「内容工作台」的真正含义：**工具围绕对话组织，能力围绕目标聚合**。

## 璞奇启示

这次 UI 改版对学习类产品有重要启示。

**第一，学习场景需要极简界面。**

学习本身就是一件需要专注的事。界面越复杂，认知负担越重，学习效率越低。璞奇新版的设计理念是：把「学习」这件事本身作为界面，而不是在学习内容之上再叠一层工具。

**第二，AI 引导比功能堆叠更有价值。**

旧版的设计逻辑是「给你一堆功能，你自己选」。新版是「告诉我你要什么，我帮你安排」。后者更符合学习者的心智——他们需要的是目标达成路径，而不是功能清单。

**第三，格式即内容。**

在对话中嵌入富媒体格式，不是为了「好看」，而是为了「高效」。一个练习卡片比一段文字描述更直观，一个进度图比百分比数字更易懂。好的格式设计，能让学习效率事半功倍。

