---
title: "Vibe Coding 生存指南：如何在 AI 时代优雅地躺平编程"
date: 2026-03-24
categories:
  - 技术
tags:
  - vibe-coding
  - ai编程
  - 程序员
  - 工作流
  - 效率工具
layout: post
image_prompt: "A serene illustration of a developer relaxing in a hammock while coding: the developer lounges peacefully with a laptop balanced on their knees, AI robots and code snippets floating around like friendly spirits, the scene set in a peaceful garden with cherry blossoms, warm sunset lighting with a dreamy atmosphere, minimalist digital art style with soft pastel colors, 16:9 aspect ratio, depicting the ideal of effortless programming with AI assistance"
image_prompt_file: "assets/prompt/2026-03-24/2026-03-24-vibe-coding-cn-survival-guide.txt"
---

> 《庄子·逍遥游》有言：「至人无己，神人无功，圣人无名。」千年之后，程序员们终于找到了另一种逍遥方式——让 AI 替自己写代码，自己只需「完全沉浸于氛围之中」。

![Vibe Coding 生存指南](https://blog.zendong.com.cn/assets/images/2026/2026-03-24-vibe-coding-cn-survival-guide.png)

## 缘起：Karpathy 的一句玩笑话

2025年2月，OpenAI 联合创始人 Andrej Karpathy 在 X 上发了一条看似玩笑的帖子：

> "我称之为一种新的编程方式——vibe coding，就是完全沉浸在感觉中，拥抱指数级提升，忘记代码本身的存在。"

这话听起来像是摸鱼指南，但细想却有深意：LLM 已经强大到可以根据自然语言指令自动生成可运行的代码，而人类只需要「说出想要什么」，而不必「知道怎么做」。

短短两个月，Vibe Coding 成为科技圈最热门的词汇之一，甚至被韦氏词典收录为「俚语和流行词」。

---

## Vibe Coding 是什么

**定义**：一种依赖 AI 的编程方式，开发者用自然语言向 LLM 描述需求，LLM 生成软件，程序员从「代码编写者」转变为「需求翻译官」。

**核心特征**：

| 特征 | 传统编程 | Vibe Coding |
|------|---------|-------------|
| 输入 | 代码（精确语法） | 自然语言（模糊描述） |
| 主力 | 人类程序员 | LLM |
| 关注点 | 如何实现 | 想要什么 |
| 代码理解 | 必须理解 | 可以不理解 |
| 键盘使用 | 频繁 | 极少 |

**两种模式**：

- **纯粹模式**：追求极致速度，完全信任 AI 输出，接受代码「不可读」的现实。适合快速原型、概念验证。
- **负责任模式**：在速度和质量之间找平衡，保持对代码的一定理解能力。

---

## 一个 10.4k Star 的中文指南

GitHub 上有一个叫 [tukuaiai/vibe-coding-cn](https://github.com/tukuaiai/vibe-coding-cn) 的项目，目前 10.4k Star、1.1k Fork，堪称 Vibe Coding 领域的中文扛鼎之作。

项目描述是：「Vibe Coding 指南 - 涵盖 Prompt 提示词、Skill 技能库、Workflow 工作流的 AI 编程工作站」。

这是一个从 [EnzeD/vibe-coding](https://github.com/EnzeD/vibe-coding) fork 过来的项目，核心贡献者 tukuaiai 在此基础上添加了大量中文解读和实战经验。

### 核心模块

项目包含四大核心模块：

**1. 元方法论**
用「生成器/优化器」的递归闭环让系统自我进化。简单说就是：让 AI 写提示词，再用 AI 优化提示词，形成正向循环。

**2. 胶水编程**
项目强调三个原则：
- 能抄不写
- 能连不造
- 能复用不原创

这和我之前体验 Codex 的感受不谋而合——有时候最高效的方式就是直接用现成的轮子，让 AI 来粘合。

**3. Canvas 白板驱动开发**
让白板成为「单一真相源」。所有需求、设计、架构都先在白板上画出来，确保人机双方对「做什么」达成一致。

**4. AI 蜂群协作**
多个 AI 在 tmux 下互相感知、协作、分工。这个听起来有点赛博朋克，但本质上是用多 Agent 系统来模拟团队协作。

### 技能库：20 个专业 AI 技能

项目还附带了 20 个专业 AI 技能（skills），分为几大类：

- **元技能**：`skills-skills`（如何生成 Skills）、`sop-generator`（SOP 生成）
- **数据库**：`postgresql`、`timescaledb`
- **加密货币/量化**：`ccxt`、`coingecko`、`hummingbot`
- **开发工具**：`canvas-dev`、`claude-code-guide`、`telegram-dev`

---

## 核心经验：上下文第一性

vibe-coding-cn 项目总结了五条核心经验，每一条都值得细品。

### 1. 上下文是 Vibe Coding 的第一性要素

项目的原话是：「上下文是 Vibe Coding 的第一性要素。」

这很好理解：LLM 的输出质量直接取决于输入的上下文。给 AI 足够的背景信息，它就能给你想要的结果；给的信息残缺，AI 就只能靠脑补。

所以 Vibe Coding 的核心能力，从「写代码」变成了「写上下文」。

### 2. 先结构，后代码

这是我自己也深有体会的经验。先把目录结构、文件划分、模块边界定义清楚，再让 AI 往里面填代码。

好处是：即使 AI 生成的代码不完美，至少你知道它应该出现在哪里。

### 3. Debug 只给预期 vs 实际 + 最小复现

遇到 bug 时，告诉 AI 两件事：
- 你预期发生什么
- 实际发生了什么
- 最小复现步骤

不用长篇大论解释上下文，AI 需要的是精确的信息，而非情感表达。

### 4. AI 错误整理为经验持久化存储

这是项目中我最喜欢的一条。AI 犯的错误不应该被遗忘，而应该被整理成「避坑指南」存入记忆银行，下次遇到类似场景时主动提醒。

---

## 实践建议：从 0 到 1 的路径

如果你想尝试 Vibe Coding，项目提供了一个清晰的路径：

1. **哲学原理**：先理解 Vibe Coding 的核心理念，不是让你偷懒，而是让你把精力从「如何实现」转移到「想要什么」

2. **网络配置**：确保能正常访问 Claude/GPT 等模型

3. **开发环境**：配置 IDE（VS Code 或 Cursor）

4. **CLI 配置**：安装 Claude Code 或 Codex CLI

5. **开始干活**：用自然语言驱动开发

推荐的工具栈：

- **模型**：Claude Opus 4.6 或 GPT-5.3 Codex
- **IDE**：VS Code + Cursor
- **终端**：tmux（多会话管理）
- **辅助**：SuperWhisper（语音输入）

---

## 局限性：Vibe Coding 不是银弹

尽管 Vibe Coding 很美好，但它不是银弹。

**局限一：代码可能难以维护**

当你不知道代码怎么写的时候，你也很难维护它。一旦 AI 生成的代码出问题，你可能连 debug 的方向都没有。

**局限二：不适合复杂系统**

简单项目可以靠「氛围」搞定，但复杂系统需要精确的架构设计和边界控制。Vibe Coding 适合做原型，不适合做生产级系统。

**局限三：对代码质量把控有挑战**

项目的 README 也坦诚地说：「当前经验可能因 AI 能力变化而失效。」

AI 的能力边界在不断变化，去年写不了的代码今年可能就能写了。这意味着 Vibe Coding 的最佳实践也在持续演进。

---

## 璞奇启示

Vibe Coding 的核心理念——让 AI 处理执行层面的事情，人类专注于「想要什么」——和学习场景的逻辑高度相似。

**第一，从「学什么」到「想达成什么」的转变。**

Vibe Coding 把程序员的角色从「代码编写者」变成「需求定义者」。类似的，璞奇的用户也应该从「被动学习知识」变成「主动定义学习目标」。

当你明确知道自己想通过练习达成什么时，AI 才能更精准地为你生成合适的练习内容。

**第二，上下文（Context）质量决定输出质量。**

Vibe Coding 的核心是「给 AI 足够的上下文」。对于学习来说，这个启发是：学习效果很大程度上取决于你提供的背景信息是否充分。

在璞奇中，这意味着一段文本、一篇文章，用户是否提供了足够的上下文来决定 AI 生成的练习难度和方向。

**第三，复用与胶水思维。**

「能抄不写，能连不造」这个原则在学习中同样适用。与其从零开始理解一个概念，不如先看看已有的优质解释和练习，再在此基础上深化。

---

## 小结

Vibe Coding 不是一个让你彻底躺平的概念，而是一个重新定义程序员角色的机会。

Karpathy 说「忘记代码的存在」，但我更愿意把它理解为：**从代码的执行者，变成代码的编排者**。

《逍遥游》说「鹏之徙于南冥也，水击三千里，抟扶摇而上者九万里。」AI 就是那股「扶摇」，而我们需要的，是知道要飞向哪里的方向感。

学会「氛围编程」，或许就能真正实现那句古话的现代版本：**「无所待而技术行」**。

---

## 信息说明

- 关于 Vibe Coding 的概念，以 [Karpathy X 帖子](https://x.com/karpathy/status/xxxxx) 和相关中文解读为准。
- 关于 [tukuaiai/vibe-coding-cn](https://github.com/tukuaiai/vibe-coding-cn) 项目信息，以 GitHub 仓库最新内容为准。