---
title: "AI流水线（1）：从灵感到博客的完整自动化"
date: 2026-03-28
categories:
  - 技术
tags:
  - claude
  - cursor
  - ai
  - github-pages
  - jekyll
  - 博客
  - 自动化
  - skill
  - agent
layout: post
image_prompt: "A futuristic AI-powered content creation pipeline visualization: a holographic workflow diagram showing AI agents transforming raw ideas into polished blog posts, floating digital screens displaying markdown text flowing through stages of content generation, robotic arms arranging UI components, neural network patterns in the background, dark tech aesthetic with cyan and purple neon accents, cinematic photorealistic style, 16:9 aspect ratio, depicting the seamless automation of creative content production"
image_prompt_file: "assets/prompt/2026-03-28/2026-03-28-ai-blog-pipeline.txt"
hero_image_ai_generated: true
---

> "君子生非异也，善假于物也。" — 《荀子·劝学》

人的创造力从来不是孤立的，每一次工具的跃迁都会带来内容生产的革命。从甲骨文到印刷术，从活字印刷到数字时代，内容承载的媒介在变，但人类对效率的追求从未改变。今天，AI 正在开启新一轮的工具革命，而我正在用 AI 流水线把「灵感」变成「博客」这件事，做到极致。

![首图](https://blog.zendong.com.cn/assets/images/2026/2026-03-28-ai-blog-pipeline.png)

---

## 为什么是 GitHub Pages + Jekyll

做技术的人，十有八九都知道 GitHub Pages。它是 GitHub 提供的一个静态网站托管服务，可以直接从仓库渲染出网站来。Jekyll 则是 GitHub Pages 默认支持的静态站点生成器，能够把 Markdown 文件转成漂亮的网站。

这套方案的优点很直接：

**低成本**：GitHub Pages 本身就是免费的，不用买服务器、不用备案、不用维护数据库。一个仓库，一套主题，就能跑起来。

**版本可控**：所有文章都在 Git 仓库里，改了什么、什么时候改、一目了然。想回退任何一个版本，一行命令搞定。

**专注写作**：Markdown 格式足够简洁，标题、正文、代码块、图片链接，足够覆盖99%的写作场景。不用操心排版，Jekyll 会处理。

**CI/CD 原生**：GitHub Actions 可以自动监听仓库变化，一推送就自动构建、部署。这才是这套方案最核心的价值——内容生产和发布流程可以完全自动化。

这周花时间走通了这套流程，核心目的不是搭博客，而是验证一件事：**从一句话或一个链接，AI 能不能自动生成一篇合格的博客文章**？

答案是：能。

---

## AI 博客流水线的完整设计

### 2.1 基本环境准备

要让 AI 独立完成博客生产，需要准备好以下几个工具：

**编辑器**：Claude Desktop 或者 Cursor。这两个工具都支持 MCP（Model Context Protocol），可以调用外部工具。我用的是 Claude Code，配合联网搜索、图片理解、图片生成等 MCP 工具。

**图片生成**：MiniMax API 或者直接用 Cursor 内置的图片生成功能。我的方案里，AI 可以根据文章主题自动生成配图，并自动压缩到合适的文件大小。

**代码托管与部署**：GitHub + GitHub Pages + Jekyll + GitHub Actions。GitHub 负责代码托管，GitHub Actions 负责自动构建和部署，Jekyll 负责把 Markdown 转成网站。

**Skill**：这是核心。一个 Skill 就是一个提示词模板，定义清楚了博客编写的基本要求——文章的格式、调性、结构、引用风格、必备模块（如「璞奇启示」）等。

### 2.2 Skill 的核心设计

Skill 是这个流水线的灵魂。它的核心职责是：

1. **格式规范**：定义 YAML front matter 的格式、标签的选择策略、图片的命名规则等。
2. **结构模板**：定义文章的通用结构——导语引用 → 正文 → 璞奇启示 → 信息说明。
3. **内容质量标准**：明确什么样的文章算「合格」——有信息增量、有独特视角、有实际价值。
4. **金句机制**：要求每一期都引用名言或金句，作为文章的情感锚点。

Skill 的编写本身也是一个迭代过程。初期定义粗一些，在实践中不断打磨细节。比如一开始没要求「璞奇启示」，后来发现这个模块既能保持内容调性统一，又能为璞奇 APP 引流，才加进去的。

### 2.3 工作流程：手动阶段

在接入 OpenClaw 之前，我先把手动流程走通了：

**第一步**：提供一个话题，可以是 URL、新闻链接、或者一段话描述。AI 负责理解话题、搜索补充信息、确认核心观点。

**第二步**：触发 Skill 处理流程。AI 根据 Skill 定义生成文章（Markdown 格式）、生成配图的英文提示词、调用 MiniMax API 生成图片、压缩图片。

**第三步**：AI 自动 commit 提交到 GitHub，触发 GitHub Actions 流水线，自动构建并部署到 GitHub Pages。

整个过程从「给话题」到「网页上看到文章」，中间不需要人工干预。

### 2.4 工作流程：OpenClaw 阶段

手动流程跑通之后，我把它封装成了一个 AI Agent，接入到 OpenClaw（海外版小龙虾）。OpenClaw 本质上是一个 AI Agent 平台，支持通过对话的方式调用各种工具和技能。

接入之后，体验提升了一个层次：

**设置触发规则**：告诉 OpenClaw 如何触发手动创建博客的流程。比如用特定关键字或者固定句式，就能激活 Skill。

**日常创作**：平时刷新闻、读文章的时候，看到有意思的内容，随手跟 OpenClaw 聊一下这个话题——让它了解这个话题的内涵，或者解答我对某个概念的疑问。聊完之后，用触发字激活博客创建流程，AI 会自动完成剩余的工作。

**即时发布**：等 AI 返回正确结果时，文章已经直接发布到网上了。打开博客地址就能看到效果。

这种「对话即创作」的体验很舒服。以前有灵感的时候要专门停下来，打开编辑器，构思框架，然后写。现在只需要随手聊几句，AI 就会帮你把灵感「消化」并「固化」成一篇完整的博客。

实际效果如图所示：跟 OpenClaw 聊一个话题，触发博客创建流程后，AI 自动完成写作、配图、压缩、发布全流程，直接在博客端看到效果。

![对话示意：跟 OpenClaw 聊话题](https://blog.zendong.com.cn/assets/images/2026/2026-03-28-ai-blog-pipeline-chat.png)

![博客端即时看到效果](https://blog.zendong.com.cn/assets/images/2026/2026-03-28-ai-blog-pipeline-result.png)

今天不知不觉就发了四篇，灵感没有丢失，都持久化成了博客：

![一天四篇博客](https://blog.zendong.com.cn/assets/images/2026/2026-03-28-ai-blog-pipeline-posts.png)

---

## 流水线的核心组件

### 3.1 图片的标准化处理

图片是博客文章的重要组成部分，但处理不好会成为性能瓶颈。我的图片处理流程有三个原则：

**统一存储**：所有图片放在 `assets/images/YYYY/` 目录下，按年份归档。文件名采用 `YYYY-MM-DD-{slug}.png` 格式，确保唯一性和可追溯性。

**自动压缩**：图片生成之后会自动调用压缩脚本，将文件大小控制在 512KB 以下。压缩不是简单的质量降低，而是根据图片类型（PNG/JPEG）选择最优的压缩策略。比如截图类图片保持 PNG 格式降低质量参数，而照片类图片可以转成 JPEG 并优化。

**绝对 URL**：文章中引用的图片使用绝对 URL 格式（`https://blog.zendong.com.cn/assets/images/...`），避免相对路径在不同部署环境下可能出现的问题。

### 3.2 GitHub Actions 自动构建

GitHub Actions 是这个流水线的自动化引擎。核心逻辑很简单：当仓库的 `_posts/` 目录下有新的或修改过的 Markdown 文件时，触发构建流程。

构建流程会：
1. 安装 Jekyll 依赖
2. 执行 `jekyll build` 生成静态文件
3. 将 `_site/` 目录部署到 GitHub Pages

整个过程不需要人工干预，只需要一个 `.github/workflows/jekyll.yml` 配置文件。

### 3.3 Skill 的迭代

Skill 不是一次性设计好的，而是在实践中不断迭代的。初期可能只定义了基本结构，在使用过程中发现新需求（比如金句、璞奇启示、图片规范），就不断加进去。

这个迭代过程本身就是一种学习——你在定义 Skill 的同时，也在定义你想要的写作标准和生活方式。

---

## 内容矩阵的扩展想象

这套流水线跑通之后，我开始思考更远的东西。

如果一个 AI Agent 可以帮你写博客，是不是可以扩展到更多内容形式？知乎回答、公众号文章、技术文档、产品介绍、短视频脚本……核心都是「理解信息 → 加工处理 → 生成内容」，只是在格式和渠道上有差异。

**多语言版本**也是一个方向。我的博客面向的是中文读者，但如果有一天需要面向全球，一个支持多语言的 Skill 体系可以快速生成英文版、日文版等不同语言的文章。

**内容矩阵**的概念就是从这儿来的。不是每一个内容渠道都要从头生产，而是让 AI 帮你把一个核心观点「翻译」成适合不同渠道的形态。博客是深度文章，知乎是问答，Twitter/X 是短观点，公众号是软文……本质上是一次创作，多次分发。

这套逻辑能不能跑通，取决于 Skill 定义得够不够细、AI 模型的理解能力够不够强、内容渠道的适配成本够不够低。至少在博客这个场景上，已经验证了可行性。

---

## 璞奇启示

这套 AI 博客流水线对璞奇 APP 的产品设计有直接的启示。

**第一，工具的价值在于降低「从想法到行动」的摩擦。**

璞奇 APP 的核心定位是「AI 为用户学习内容提效」——通过 AI 生成练习题、帮助用户掌握知识。但比练习更重要的是，用户愿意开始学习。

这套博客流水线解决的是「我不想写，因为太麻烦」的问题。类似地，璞奇 APP 要解决的可能是「我不想学，因为启动太难」的问题。如果 AI 能把学习的启动门槛降到最低——用户只需要提供一个话题，AI 帮他生成学习路径和练习内容——这就是工具对行为改变最直接的价值。

**第二，流程自动化是工具的终极形态。**

从手动写博客到 AI 自动生成博客，本质上是一个「流程自动化」的过程。用户只给出目标（一篇博客），AI 负责中间的所有步骤。

璞奇 APP 也可以朝这个方向演进：用户只给出学习目标（比如「我想了解量子计算」），AI 自动生成学习路径、设计练习、追踪进度、提供反馈。用户的学习过程被 AI 「流线化」了，不需要操心「该学什么、该练什么、该掌握到什么程度」这些中间问题。

工具的终极形态是「用户只需要告诉我想做什么，工具帮我做完」。

---

## 小结

AI 博客流水线这件事，本质上是用 AI 工具重新定义「内容创作」这个行为。

以前写博客是：灵感 → 构思 → 写作 → 发布，每个环节都需要人工介入。现在是：灵感 → 触发 AI → 自动完成写作、配图、压缩、发布。人的角色从「执行者」变成了「监督者」。

这种转变不只发生在博客创作上。所有重复性的内容生产工作，都值得用 AI 重新做一遍。

博客地址：https://blog.zendong.com.cn。相关 Skill 和博客源码都是开放状态，可以从博客首页找到 GitHub 仓库链接。

> "工欲善其事，必先利其器。" — 《论语·卫灵公》

---

## 信息说明

- GitHub Pages 官方文档：https://pages.github.com/
- Jekyll 官方文档：https://jekyllrb.com/
- GitHub Actions 官方文档：https://docs.github.com/en/actions
- OpenClaw（小龙虾）官网：https://openclaw.ai/
