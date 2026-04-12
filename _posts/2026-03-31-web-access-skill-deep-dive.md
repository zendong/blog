---
title: "web-access：给 AI Agent 装上完整联网能力的 Skill"
date: 2026-03-31
categories:
  - 技术
tags:
  - agent
  - skill
  - claude-code
  - openclaw
  - cdp
  - browser-automation
  - web-access
layout: post
image_prompt: "A futuristic AI agent visualization: a digital spider or lobster claw made of glowing cyan data streams reaching out to touch the surface of the internet represented as a vast glowing network grid, with multiple browser windows floating around connected by light beams, data packets flowing between the claw and web pages, neural network patterns in the background, deep blue and purple color scheme with bright cyan accents, cyberpunk aesthetic, 16:9 aspect ratio, concept art depicting AI web access capabilities"
image_prompt_file: "assets/prompt/2026-03-31/2026-03-31-web-access-skill-deep-dive.txt"
hero_image_ai_generated: true
---

> "The only true wisdom is in knowing you know nothing." — Socrates

Socrates的这句话道出了 AI Agent 在联网场景下的困境：AI 知道很多，但当它需要获取**最新、最准确**的信息时，它实际上"什么都不知道"。传统 Agent 的联网能力要么依赖搜索引擎的二手信息，要么根本无法访问需要登录态的网页。

[web-access](https://github.com/eze-is/web-access) 这个 Skill（GitHub Stars 2800+），试图解决这个问题——让 Claude Code 拥有完整、可靠、可控的联网与浏览器操控能力。

![web-access 概念图](https://blog.zendong.com.cn/assets/images/2026/2026-03-31-web-access-skill-deep-dive.png)

## 1. 项目背景与核心定位

### 1.1 为什么需要 web-access

Claude Code 本身具备 `WebSearch` 和 `WebFetch` 能力，但这两个工具都有明显局限：

- **WebSearch**：适合发现信息来源，但无法获取需要登录态的内容
- **WebFetch**：适合拉取公开页面，但无法处理动态渲染页面，也无法操作网页界面

更关键的是，这两个工具之间**没有调度策略**——Agent 不知道何时该用搜索，何时该用抓取，何时又必须动用浏览器。

web-access 的核心定位是：**给 AI Agent 装上一套完整的联网工具箱，包括智能调度、浏览器自动化和站点经验积累**。

### 1.2 项目信息

| 项目 | 信息 |
|------|------|
| GitHub | [eze-is/web-access](https://github.com/eze-is/web-access) |
| 作者 | 一泽 Eze |
| 版本 | 2.4.1 |
| 许可证 | MIT |
| 创建时间 | 2026-03-18 |
| Stars | 2800+ |

---

## 2. 技术原理：三层架构

web-access 的设计基于一个核心洞察：**联网任务需要分层的抽象，而不是一个万能工具**。

```
┌─────────────────────────────────────────────────────────┐
│                    web-access 三层架构                      │
├─────────────────────────────────────────────────────────┤
│  第一层：工具调度层    │ 根据场景自主选择最优联网工具              │
│                       │ WebSearch / WebFetch / curl /     │
│                       │ Jina / CDP，按需组合               │
├─────────────────────────────────────────────────────────┤
│  第二层：CDP 浏览器层  │ 直连用户 Chrome，携带登录态            │
│                       │ 支持动态页面、交互操作、视频截帧          │
├─────────────────────────────────────────────────────────┤
│  第三层：站点经验层    │ 按域名存储操作经验（URL 模式、平台特征、   │
│                       │ 已知陷阱），跨 session 复用          │
└─────────────────────────────────────────────────────────┘
```

### 2.1 第一层：工具调度层

这是 web-access 的"大脑"，负责根据任务性质选择最合适的联网工具。

| 场景 | 推荐工具 | 原因 |
|------|---------|------|
| 搜索摘要或关键词，发现信息来源 | **WebSearch** | 适合信息发现 |
| URL 已知，需提取特定信息 | **WebFetch** | 拉取网页内容，由小模型提取 |
| URL 已知，需原始 HTML（meta、JSON-LD） | **curl** | 获取原始源码 |
| 非公开内容，或静态层无效的平台（小红书、微信公众号） | **浏览器 CDP** | 直接跳过静态层 |
| 需要登录态或自由导航 | **浏览器 CDP** | 携带用户登录态 |

工具选择的哲学是：**一手信息优于二手信息**。搜索引擎是定位工具，不是证明工具——找到来源后，直接访问读取原文。

**Jina 加速层**：第三方服务，可将网页转为 Markdown，大幅节省 token。适合文章、博客、文档、PDF 等以正文为核心的页面。

### 2.2 第二层：CDP 浏览器层

这是 web-access 的"手"，通过 Chrome DevTools Protocol 直接操控用户的 Chrome 浏览器。

核心能力：
- **直连用户日常 Chrome**：天然携带登录态，无需启动独立浏览器
- **后台 tab 操作**：不影响用户已有标签页
- **完整浏览器能力**：支持动态页面渲染、交互操作、视频截帧

CDP Proxy 通过 WebSocket 直连 Chrome，提供 HTTP API 接口。启动后持续运行，所有操作通过 curl 调用。

### 2.3 第三层：站点经验层

这是 web-access 的"记忆"，按域名存储已验证的操作经验。

经验内容包括：
- **平台特征**：架构、反爬行为、登录需求、内容加载方式
- **有效模式**：已验证的 URL 模式、操作策略、选择器
- **已知陷阱**：什么会失败以及为什么

经验文件示例：
```markdown
---
domain: xiaohongshu.com
aliases: [小红书]
updated: 2026-03-25
---
## 平台特征
需要登录态，xsec_token 机制，创作者平台有状态校验

## 有效模式
直接 CDP 访问主站，跳过静态层

## 已知陷阱
手动构造 URL 可能缺失隐式参数，触发反爬
```

---

## 3. CDP 浏览器控制详解

### 3.1 架构原理

CDP（Chrome DevTools Protocol）是 Chrome 内置的调试协议，web-access 通过 CDP Proxy 封装为 HTTP API：

```
Agent (curl) → CDP Proxy (Node.js WebSocket) → Chrome (CDP)
```

用户只需在 Chrome 中开启远程调试（`chrome://inspect/#remote-debugging` 勾选 Allow），无需其他配置。

### 3.2 核心 API

| API | 功能 |
|-----|------|
| `GET /new?url=URL` | 创建新后台 tab |
| `POST /eval?target=ID` | 执行 JavaScript，读取/写入 DOM |
| `POST /click?target=ID` | JS 层点击（`el.click()`） |
| `POST /clickAt?target=ID` | 真实鼠标事件（绕过部分反自动化检测） |
| `POST /setFiles?target=ID` | 文件上传（绕过文件对话框） |
| `GET /screenshot?target=ID` | 截图（捕获视频当前帧） |
| `GET /scroll?target=ID` | 滚动触发懒加载 |
| `GET /close?target=ID` | 关闭 tab |

### 3.3 三种点击方式

web-access 提供了三种点击策略，适用于不同场景：

| 方式 | 实现 | 适用场景 |
|------|------|---------|
| `/click` | JS `el.click()` | 大多数场景，速度快 |
| `/clickAt` | CDP `Input.dispatchMouseEvent` | 需要真实鼠标事件（触发文件对话框、绕过反自动化） |
| `/setFiles` | `DOM.setFileInputFiles` | 文件上传，直接设置路径 |

### 3.4 页面内导航

两种方式打开页面内链接：

- **`/click`**：在当前 tab 内点击，串行处理，适合需要连续操作的场景
- **`/new` + 完整 URL**：在新 tab 中打开，适合需要并行访问多页面的场景

**重要设计**：站点自己生成的链接天然携带完整上下文（包含 token 等隐式参数），而手动构造的 URL 可能缺失这些参数。web-access 强调提取 URL 时应保留完整地址。

### 3.5 程序化 vs GUI 交互

浏览器内操作有两种方式：

- **程序化方式**（构造 URL 直接导航、eval 操作 DOM）：速度快、精确，但更容易触发反爬
- **GUI 交互**（点击按钮、填写输入框）：为人设计，网站不会限制，确定性最高

当程序化方式受阻时，GUI 交互是可靠的兜底。

---

## 4. 与传统方案的对比

### 4.1 方案横向对比

| 方案 | 工具选择 | 登录态支持 | 动态页面 | 交互能力 | 站点经验 |
|------|---------|----------|---------|---------|---------|
| 原生 WebSearch/WebFetch | 单一工具 | ❌ | ❌ | ❌ | ❌ |
| Selenium/Playwright | 手动控制 | 需要启动独立浏览器 | ✅ | ✅ | ❌ |
| RPA 工具 | 录制+回放 | 需要配置 | ✅ | ✅ | 有限 |
| **web-access** | **智能调度** | **✅ 直连用户 Chrome** | **✅** | **✅** | **✅** |

### 4.2 核心优势

**1. 智能调度而非一刀切**
不是把所有任务都推向浏览器，而是根据场景选择最优工具。轻量查询用 WebSearch，需要登录态或交互时再升级到 CDP。

**2. 用户 Chrome 天然携带登录态**
不需要维护独立的浏览器实例或登录状态，用户日常使用的 Chrome 就是最完整的浏览器环境。

**3. 站点经验跨 session 复用**
每次成功操作的经验都被记录，下次遇到同类站点可以直接调用，而不需要从零开始摸索。

**4. 并行分治提升效率**
多目标调研时，分发给子 Agent 并行执行，共享一个 Chrome 实例，tab 级隔离，兼顾速度与安全。

### 4.3 适用边界

web-access 不是银弹，以下场景可能不适合：

- **完全禁用 JavaScript 的环境**：静态 HTML 抓取更高效
- **需要严格隔离的自动化测试**：应该用独立的浏览器实例
- **高频短时请求**：CDP 开销相对较大，不适合极高频调用

---

## 5. 应用场景

### 5.1 信息核实与调研

**场景**：用户要求核实"某公司最新公告"或"某政策文件"

web-access 的处理流程：
1. WebSearch 定位信息来源
2. 直接访问官方页面（CDP 携带登录态）
3. 读取原文，提取关键信息
4. 对照用户提供的声明，判断一致性

一手来源优于二手报道——这是信息核实的核心原则。

### 5.2 社交媒体操作

**场景**：用户要求"去小红书搜索某关键词账号"或"在创作者平台发布内容"

对于小红书、微信公众号等反爬严格的平台：
- 静态抓取无效 → 直接 CDP 访问
- 需要登录态 → 直连用户 Chrome，自动携带
- 平台有特殊机制（如 xsec_token）→ 站点经验已记录

### 5.3 视频内容分析

**场景**：用户要求"分析某视频的内容"

web-access 通过截图捕获视频当前帧，配合 `/eval` 操作 `<video>` 元素（获取时长、seek 到任意时间点），可对视频内容进行离散采样分析。

### 5.4 多目标并行调研

**场景**：用户要求"同时调研这 5 个产品的官网，给我对比摘要"

web-access 支持子 Agent 分治策略：
- 主 Agent 分析任务，分发给多个子 Agent
- 每个子 Agent 创建独立 tab，并行抓取
- 主 Agent 只接收摘要，节省上下文 token

### 5.5 表单填写与文件上传

**场景**：用户要求"帮我在某平台上传图片并提交表单"

通过 `/setFiles` 直接设置文件路径，绕过文件对话框；通过 `/click` 或 `/clickAt` 提交表单，全程无需用户介入。

---

## 6. 设计哲学

web-access 的设计哲学浓缩在一句话中：

> **Skill = 哲学 + 技术事实，不是操作手册。讲清 tradeoff 让 AI 自己选，不替它推理。**

这意味着：
- **目标驱动而非步骤驱动**：告诉 AI 要什么，而不是一步步教它怎么做
- **工具自主选择**：提供场景和工具特点，AI 根据实际情况判断
- **经验可累积**：成功的策略被记录，失败的陷阱被标注

浏览哲学的核心是**"像人一样思考"**——带着目标进入，边看边判断，遇到阻碍就解决，不在错误的方式上反复重试。

---

## 璞奇启示

web-access 对学习类产品的启示在于**"工具分层与智能调度"**。

**第一，工具需要分层，不是一个万能按钮**

web-access 的三层架构揭示了一个重要道理：不同任务需要不同工具，强行用单一工具处理所有任务要么低效，要么脆弱。

学习类产品同样如此——不同的知识点、不同的学习阶段，需要不同的练习形式。刷题适合巩固记忆，但不适合建立理解；案例分析适合深度理解，但不适合快速自测。璞奇如果能根据用户的薄弱点自动选择最合适的练习形式，效果会比"一种形式打天下"好得多。

**第二，学习经验需要跨 session 积累**

web-access 按域名存储站点经验，让 AI 每次访问都能站在上次成功的基础上。

璞奇的用户学习数据同样需要"跨 session 积累"——用户上次做错的题，下次应该自动避坑；用户在某类知识点上反复出错，说明需要更多同类练习。这种经验驱动的自适应，比简单的"推荐相似题目"更有价值。

**第三，一手信息优先**

web-access 强调一手来源优于二手报道，直接访问原文比搜索引擎更可靠。

学习场景中，"直接理解概念"比"看别人的解读"更有效。当用户遇到难点时，璞奇应该引导用户回到原始概念（官方文档、原始论文）去理解，而不是在二手解释中打转。

---

## 信息说明

- web-access GitHub 仓库：https://github.com/eze-is/web-access
- CDP Proxy 基于 Node.js 22+ 和 Chrome 远程调试
- 项目创建时间：2026-03-18
- 文章内容基于 v2.4.1 版本
