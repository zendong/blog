---
title: "CLI-Anything 深度解读：让所有软件成为 AI Agent 的原生工具"
date: 2026-03-29
categories:
  - 技术
tags:
  - agent
  - ai-agent
  - cli
  - claude-code
  - openclaw
  - mcp
  - hku
  - harness-engineering
layout: post
image_prompt: "A futuristic visualization of software transformation: a complex professional software application interface (like Blender or GIMP) being wrapped by glowing golden CLI command lines emanating from a central transformer device, with small AI robot agents interacting through command terminals, data streams flowing outward, dark background with circuit board patterns, golden and cyan light rays, cinematic lighting, 16:9 aspect ratio, concept art showing the bridge between human GUI and AI agent CLI"
image_prompt_file: "assets/prompt/2026-03-29/2026-03-29-cli-anything-deep-dive.txt"
hero_image_ai_generated: true
---

> "合于利而动，不合于利而止。" — 《孙子兵法》

AI Agent 很会推理，却并不擅长稳定地使用真实世界的软件。当它需要操控 GIMP 做图像处理、控制 Blender 渲染 3D 模型、操作 LibreOffice 批量转换文档时，现状令人尴尬：要么靠截图点击的 GUI 自动化（脆弱得像纸牌屋），要么重新实现一个阉割版 API（费时费力还不完整）。

香港大学数据科学实验室（HKUDS）开源的 [CLI-Anything](https://github.com/hkuds/cli-anything) 项目，给出了一个简洁却充满智慧的答案：**把一切软件都变成 CLI 接口**。

上线数周，GitHub stars 突破 **17,000+**，成为今年 AI Agent 领域最炙手可热的项目之一。

![CLI-Anything 让软件变成 Agent-Native 的概念图](https://blog.zendong.com.cn/assets/images/2026/2026-03-29-cli-anything-deep-dive.png)

## 核心问题：Agent 与软件之间的鸿沟

要理解 CLI-Anything 的价值，先要看清当前 AI Agent 操控软件时的三条路，以及它们各自的缺陷。

**第一条路：GUI 自动化**。看屏幕、找按钮、移动鼠标、点击、读反馈。这类方案能跑 demo，但分辨率变了可能失效，主题换了可能识别错，软件升级按钮位置就变了。流程稍微复杂一点，稳定性就快速下降——像让 AI 戴着手套操作精密仪器，事倍功半。

**第二条路：API 集成**。很多桌面软件根本没有完整 API，有 API 也往往只覆盖核心场景的 20%。很多历史项目、开源软件、创意工具，本来就不是为 Agent 设计的。软件真实能力很强，但 Agent 只能碰到边缘功能。

**第三条路：手写工具接入**。每个软件单独开发一层 Agent 集成，先研究软件能力，再设计接口，再开发，再测试。成本极高，无法规模化。

## 解决思路：CLI 作为通用接口

CLI-Anything 的核心洞察只有一句话：**CLI（命令行界面）才是人类和 AI Agent 的通用接口**。

这并非空想。Claude Code 每天通过 CLI 执行数以千计的真实工作流，已经验证了这条路是可行的。CLI 的优势在于：

- **结构化且可组合**：文本命令天然匹配 LLM 的输入格式，可自由串联成复杂工作流
- **轻量且通用**：几乎零开销，跨平台运行，不依赖额外环境
- **自描述**：一个 `--help` 就能让 Agent 自动发现所有功能
- **Agent 友好**：结构化 JSON 输出，Agent 无需任何额外解析
- **确定且可靠**：输出稳定一致，Agent 行为可预测

CLI-Anything 的项目口号精准地点出了这个趋势：**"Today's Software Serves Humans 👨‍💻. Tomorrow's Users will be Agents 🤖"**。

## 技术架构：七阶段全自动流水线

CLI-Anything 的技术核心是一套七阶段 SOP（标准操作流程），由 AI Agent 自动执行，全程无需人工介入。

```
/cli-anything <software-path-or-repo>
         │
         ▼
┌─────────────────────────┐
│ 1. Analyze（代码分析）    │ 扫描源代码，映射 GUI 动作到 API
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 2. Design（接口设计）     │ 定义 CLI 命令结构和参数
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 3. Implement（实现）     │ 生成完整的 Python CLI 包
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 4. Test（测试）          │ 端到端测试 + 单元测试
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 5. Document（文档）       │ 自动生成 --help 和使用文档
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 6. Register（注册）     │ 发布到 Agent 插件市场
└─────────────────────────┘
         │
         ▼
┌─────────────────────────┐
│ 7. Verify（验证）        │ 真实软件验证，确保可用
└─────────────────────────┘
```

用户只需要一行命令，CLI-Anything 就能为任意有源码的软件生成一套完整的、生产级可用的 CLI 接口。

### 六种后端集成范式

生成的 CLI 并不只有一种形态。根据目标软件的特点，CLI-Anything 支持六种后端集成方式：

| 集成范式 | 代表软件 | 实现方式 |
|---------|---------|---------|
| 子进程调用 | GIMP、Blender、Audacity | 调用真实软件的 CLI/脚本接口 |
| 无头模式 | LibreOffice | `libreoffice --headless` |
| REST API | ComfyUI、AdGuard Home | HTTP 请求调用 |
| OAuth2/API Key | Zoom、AnyGen、Novita | 认证 + REST 调用 |
| MCP 协议 | Browser（DOMShell） | MCP 协议通信 |
| 本地推理引擎 | Ollama | REST API (localhost) |

这意味着 CLI-Anything 的适用范围是"任何有代码库或可编程接口的软件"，远不止桌面 GUI 应用。

## 为什么爆火

CLI-Anything 的爆发不是偶然，而是踩中了几个关键节点的必然。

**解决了真实痛点**。开发者社区对 GUI 自动化的脆弱性早有怨气，对手写集成的高成本也心知肚明。CLI-Anything 出现时说出了大家一直在想但没说出口的话。

**Claude Code 的示范效应**。Claude Code 的 CLI 做得极为出色——有状态、自描述、好用还强大。Agent 拿起来就能干活。但绝大多数专业软件（GIMP、Blender、LibreOffice、OBS）都没有这样的 CLI。CLI-Anything 填补了这个空白。

**零修改原软件**。不需要软件本身支持任何新协议，不需要找厂商合作，不需要fork 源码。CLI-Anything 是纯粹的外挂层，这种侵入性极低的设计让它极具推广价值。

**100% 测试通过率**。截至 2026 年 3 月，项目累计通过 1,858 项测试（含 1,355 项单元测试、484 项端到端测试），通过率 100%。这种质量背书在开源项目中极为罕见。

**插件市场直连**。支持 Claude Code、OpenClaw、nanobot、Cursor 等主流 Agent 工具，安装只需两行命令，降低了使用门槛。

## 对 AI Agent 生态的意义

CLI-Anything 的出现，在三个层面对 AI Agent 生态产生了深远影响。

### 1. 填补了 MCP 覆盖不到的空白

MCP（Model Context Protocol）是 Agent 工具接入的主流协议，但它需要软件本身支持 MCP。而 CLI-Anything 是一种更底层的抽象——只要软件有可调用的入口（哪怕只是命令行参数），就能生成 Agent 可用的接口。它不是 MCP 的替代品，而是 MCP 之外的另一种选择。

### 2. 催生了 "Harness Engineering" 新范式

2025 年中，Andrej Karpathy 提出 Context Engineering 比 Prompt Engineering 更重要。2026 年初，CLI-Anything 项目让一个新的工程概念浮出水面——**Harness Engineering**。

如果说 Prompt Engineering 是"该怎么问"，Context Engineering 是"该让模型看到什么"，那么 Harness Engineering 就是"整个环境该如何设计"——Agent 外部的约束、反馈与运维系统。

CLI-Anything 生成的不只是 CLI，而是一整套 "Harness"（测试架）。它包含测试用例、验证脚本、使用文档、集成代码，共同构成一个经过实战验证的 Agent-Software 接口层。

### 3. 重新定义了"软件 Agent-Native"

CLI-Anything 提出了一个清晰的愿景：**未来的软件不只需要为人类设计 GUI，还需要为 Agent 设计 CLI**。这不是要取代 GUI，而是在原有基础上增加一层专为机器交互设计的抽象层。通过这一层抽象，软件的功能被转化为原子化的命令，输入输出被标准化为结构化数据。

## 璞奇启示

CLI-Anything 对学习类产品有重要启示。

**第一，学习内容需要"原子化"**。CLI-Anything 将复杂的专业软件功能拆解为可组合的原子命令。同理，AI 学习类产品也需要将知识拆解为可练习的最小单元——不是让用户"看完一篇文章"，而是让他完成一个具体的、可验证的练习动作。璞奇的练习题设计正是这种思路的体现。

**第二，输出格式决定 AI 能否理解**。CLI-Anything 强制所有命令输出 JSON 结构化数据，因为这是 AI 最容易处理的格式。学习类产品也需要为 AI 设计"结构化的输出格式"——不是让 AI 输出自然语言描述，而是输出带类型、带格式、带验证的练习结果，这样 AI 才能准确评估学习效果并给出反馈。

**第三，"零修改"的兼容性思维**。CLI-Anything 不需要软件本身做任何修改，就能让 Agent 控制它。学习类产品也可以借鉴这种思维：不需要用户改变原有的学习习惯，不需要用户安装特殊软件，直接在他们已有的内容上叠加 AI 能力层。

---

## 信息说明

- CLI-Anything GitHub 仓库：[https://github.com/hkuds/cli-anything](https://github.com/hkuds/cli-anything)
- HKUDS 实验室：[https://github.com/hkuds](https://github.com/hkuds)
- MCP 协议由 Anthropic 于 2024 年 11 月推出，CLI-Anything 与之形成互补而非替代关系
- 项目数据截至 2026 年 3 月
