---
title: "和 AI 聊完就忘？我们用 Agent Skill，把对话接进璞奇的练习与笔记"
date: 2026-04-05
categories:
  - 创业
tags:
  - pracmo
  - agent-skill
  - 璞奇APP
  - openclaw
  - claude-code
layout: post
image_prompt: "Conceptual hero: flowing chat bubbles from an AI agent converging into a glowing bridge with subtle API motifs, leading to a mobile flashcard practice deck and an open notebook, soft teal and warm coral on dark background, modern product illustration, cinematic soft lighting, 16:9, no readable text"
image_prompt_file: "assets/prompt/2026-04-05/2026-04-05-pracmo-create-agent-skill.txt"
hero_image_ai_generated: true
---

> "逝者如斯夫，不舍昼夜。" — 《论语·子罕》

![首图](https://blog.zendong.com.cn/assets/images/2026/2026-04-05-pracmo-create-agent-skill.png)

很多人已经习惯在对话里和 AI 一起读材料、做总结、想方案。可对话一停，内容常常就散了：想练要另起炉灶，想记又要换 App。**璞奇（Pracmo）**先把「练」和「沉淀」做成底座；**pracmo-create** 则是在上面接两根线——把两类「创建」能力接到 Agent 对话里：助手不只会陪聊，还能在合适的时候，**真的在璞奇里帮你生成一份流炼，或写进一条笔记**。下面三件事说清楚：卡在哪、Skill 为啥关键、怎么上手。

## 聊完就走，问题出在哪

产品能力再强，如果**进系统的入口**只有网页和 App，在 Agent 时代就会断层：用户和 AI 已经在一句话、一段上下文里把事情说清楚了，却还要再「翻译」成点击、表单和菜单。

**pracmo-create** 面向的不是「再堆一个功能」，而是**让璞奇的创建能力，能被 Agent 稳定地用起来**：说过的话，有机会变成你真正用得上的练习和笔记。

## 「练一下」和「记一下」，同一套思路

目前这条能力覆盖两件事：

- **练一下**：把当前对话里的材料，整理成可以分享的**流炼**练习。
- **记一下**：把你想沉淀的内容写进**笔记本**；需要时还可以新建笔记本。

两件事看起来不同，设计上是同一套节奏：**先想清楚要创建什么，征得你同意，再落库、再给你结果**。这样既尊重意图，也避免 Agent 自作主张乱创建。

可以概括成三句话：

1. **统一身份**：用 API Key 把「谁在创建」说清楚，Agent 环境里有钥匙就能干活，不必再走一遍传统登录链路讲故事。
2. **先草案，后创建**：无论是出题还是记笔记，都先让你看到「准备做成什么样」，再动手——这是把对话里的模糊意图，变成可交付结果的安全阀。
3. **编排放在 Skill，能力放在产品**：产品侧专注把「练习」「笔记本」「笔记」做好；Skill 专注问对人、排对序、在对的时机调用。后面要扩展更多「创建型」能力，也沿这条线长。

## 为什么 Agent Skill 是「总闸门」

**对话是自然语言的入口**：用户说的是意图，不是字段名。Skill 负责把「练一下」「记到工作笔记本」这种话，变成可执行、可校验的步骤。

**Skill 是意图与产品之间的协议层**：后端提供「能创建什么」；Skill 规定「在什么前提下、按什么顺序、和用户怎么确认」。没有这一层，Agent 要么只能给建议，要么容易乱调用。

**Skill 让「上下文」变成「资产」**：同一段对话，可以被收敛成**一道可练的练习**或**一条可检索的笔记**，而不是散落在聊天记录里。

我们并不是在「给璞奇加两个按钮」，而是在补一条**从对话到璞奇资产**的通路。Skill 越清晰，这条通路越稳；通路越稳，璞奇作为「练习与沉淀」的底座，才越能在 Agent 工作流里站住脚。

## 怎么接进「流炼」：安装与体验

如果你在用 **OpenClaw**、**Claude Code** 等 Agent 环境，可以把当前对话里感兴趣的内容收成**流炼练习草案**，确认后再创建，并拿到分享链接；到手机端打开，整条路径可以很顺。

在官方仓库 [zendong/skills](https://github.com/zendong/skills) 中，**流炼创建**当前对应的 Skill 名为 **`pracmo-create`**（以仓库内 `SKILL.md` 为准）。大致步骤：

1. 在 [API Key 页面](https://www.zendong.com.cn/app/api-key) 登录并获取 API Key。
2. 在运行 Agent 的环境中设置环境变量 **`PRACMO_APIKEY`**（值为你的 Key；请勿把密钥贴进公开聊天）。

然后把下面这段交给 Agent，让它自己装技能、读文档（会拉到 `SKILL.md` 和依赖说明）：

```text
参考如下命令 npx skills add https://github.com/zendong/skills --skill pracmo-create 下载 pracmo-create skill 内容到你的 skill 目录，然后读取此 skill 的 SKILL.md，说明你新增的能力以及依赖
```

下面以 **OpenClaw** 为例，走一遍「装完就能玩」的路径。

![在 OpenClaw 里安装并配置 pracmo-create](https://blog.zendong.com.cn/assets/images/2026/2026-04-05-pracmo-create-agent-skill-openclaw-install.png)

告诉它 **API Key 上哪领**（见上文链接），它会自己去查环境变量怎么设，基本不用你手抄一长串。

装好之后，就可以进入「偷懒但有用」模式：让 Agent 把当前对话收成**笔记**，再顺手来一份**流炼**，当作读完笔记的小考。

![一次生成笔记与流炼练习](https://blog.zendong.com.cn/assets/images/2026/2026-04-05-pracmo-create-agent-skill-note-and-flow.png)

手机端打开璞奇，笔记这边已经就位：

![手机端查看笔记](https://blog.zendong.com.cn/assets/images/2026/2026-04-05-pracmo-create-agent-skill-mobile-note.png)

同一套内容，流炼也在列表里，点进去就能开练：

![手机端查看流炼练习](https://blog.zendong.com.cn/assets/images/2026/2026-04-05-pracmo-create-agent-skill-mobile-flow.png)

分享链接丢进浏览器，**免装、点开即练**（具体是否免登录以题型与线上规则为准）：

![网页端直接开练](https://blog.zendong.com.cn/assets/images/2026/2026-04-05-pracmo-create-agent-skill-web-play.png)

璞奇里，**流炼**把主题变成可反复练、可追踪的练习流；**笔记与错题**让学完有痕迹；**云端同步**让进度跟着人走。更完整的产品介绍可见前文《从「看过」到「掌握」：璞奇，把任意主题装进 AI 随身练习室》。**「记一下」**等与笔记相关的 Agent 创建能力，与 **pracmo-create** 的产品编排一致，具体以官方仓库与后续发布的 `SKILL.md` 为准。

## 璞奇启示

学习类产品里，用户缺的不一定是「更多内容」，而是**把当下语境里的理解，变成可重复、可检索的练习与笔记**。

**第一，协议层比单点功能更重要。**  
自然语言入口要落地，需要清晰的 Skill：何时触发、如何确认、调用哪条后端能力。璞奇把「练」与「沉淀」做成可被 Agent 调用的能力，练习与笔记才跟得上对话节奏。

**第二，先草案后创建，是信任与质量的折中。**  
对用户可见的确认步骤，既是安全阀，也是把模糊意图变成可交付结果的过程——这与璞奇用多种练习形式帮助用户掌握知识的思路一致：掌握来自可执行的下一步，而不是一次性灌输。

## 小结

**pracmo-create** 想说明白一件事：**让璞奇的「创建」能力，跟得上用户和 Agent 的对话节奏**。而 **Agent Skill** 的价值也很直接：**没有 Skill 把自然语言接进来，产品能力再强，也难进 Agent 这条信息输入的主干道**。

我们正在做的，就是把璞奇往这条主干道上多推一步——让你说过的话，有机会变成你真正用得上的练习和笔记。

---

## 信息说明

- API Key：<https://www.zendong.com.cn/app/api-key>
- Web 应用：<https://www.zendong.com.cn/app/>
- Skill 仓库：<https://github.com/zendong/skills>（Skill 名称、接口字段与行为以仓库内 `SKILL.md` 及线上开放平台为准）
