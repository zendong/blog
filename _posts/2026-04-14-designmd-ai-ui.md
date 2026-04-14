---
title: "复制一个 DESIGN.md，AI 就能画出像素级一致的 UI"
date: 2026-04-14
categories:
  - AI
  - 设计
tags:
  - ai-design
  - design-md
  - google-stitch
  - vibe-coding
  - voltagent
layout: post
card_image: /assets/images/2026/2026-04-14-designmd-brands.png
---

> "复制一个 DESIGN.md，告诉 AI'做个长这样的页面'，就能得到像素级一致的 UI。"

![66+ 品牌设计风格对比](/assets/images/2026/2026-04-14-designmd-brands.png)

我第一次看到这个说法的时候是怀疑的。不就是一段 Markdown 文本吗？颜色值、字体大小、圆角参数——AI 真的能照着这个原样复刻出一个网站来？

结果我去试了一下 Airbnb 的 DESIGN.md。

没有截图，没有 Figma，没有参考图。就一段纯文本。结果……我得到了一个长得跟 Airbnb 几乎一模一样的页面。

左侧是原始 Airbnb 网站，右侧是 AI 照着 DESIGN.md 生成的页面：

![原始 Airbnb 网站](/assets/images/2026/2026-04-14-designmd-airbnb-original.png)

![AI 生成的 Airbnb 风格页面](/assets/images/2026/2026-04-14-designmd-airbnb-generated.png)

这篇文章就来聊聊 DESIGN.md 是什么，以及怎么用它。

## DESIGN.md 从哪来

这个概念是 Google 提出来的。

Google 有一个叫 Stitch 的项目（内部代号 Nemo），目标是"Design with AI"。它的核心想法很简单：与其让 AI 自由发挥画 UI，不如给它一份文字版的设计规范，让它照着这份规范来生成。

这份规范就是 DESIGN.md。

> DESIGN.md is a plain-text design system document that AI agents read to generate consistent UI.

翻译过来就是：一个纯文本的设计系统文档，AI agent 读取它来生成一致的 UI。

关键在这几个字：**纯文本**。不是 Figma 文件，不是 JSON，不是 XML，就是一个 Markdown 文件，放到项目根目录里，任何 AI 编码工具都能读。

## awesome-design-md：66 个品牌的设计规范

光有 Google 的概念还不够，得有人真的去写这些 DESIGN.md 文件。

VoltAgent 团队干了这件事。他们创建了 awesome-design-md 项目，收录了 66 个品牌的 DESIGN.md 文件。

数据是这样的：

- 2026 年 4 月 1 日创建
- 不到两周，48k Stars
- 6k Forks
- 31 次提交

平均每天 3400 个 Star。这个增长速度相当离谱。

覆盖的品牌类型包括：

- AI/LLM 平台：Claude、Minimax、Mistral AI、xAI 等
- 开发者工具：Cursor、Vercel、Raycast、Expo 等
- 金融科技：Stripe、Coinbase、Binance、Revolut 等
- 电商零售：Airbnb、Nike、Shopify、Meta Store 等
- 汽车：Tesla、BMW、Ferrari、Lamborghini 等
- 还有 Apple、NVIDIA、Spotify、SpaceX 等等

你想做什么风格，基本都能找到对应的 DESIGN.md。

![品牌风格对比](/assets/images/2026/2026-04-14-designmd-brands.png)

## DESIGN.md 里到底写了什么

光有概念不够，得看看实际的 DESIGN.md 长什么样。

我以 evertrain 项目里的 DESIGN.md 为例，它目前的 Airbnb 风格版本是这样组织的：

### 1. Visual Theme & Atmosphere

第一部分是描述设计理念和氛围。

```markdown
Airbnb's website is a warm, photography-forward marketplace that
feels like flipping through a travel magazine where every page
invites you to book. The design operates on a foundation of
pure white (#ffffff) with the iconic Rausch Red (#ff385c) serving
as the singular brand accent.
```

这一段是写给 AI 看的"感受描述"，让它理解这个品牌的整体调性。后面的章节则是更具体的参数规范。

### 2. Color Palette & Roles

颜色系统。每个颜色都有语义名称、hex 值和功能说明。

```markdown
### Primary Brand
- **Rausch Red** (#ff385c): primary CTA, brand accent
- **Deep Rausch** (#e00b41): pressed/dark variant

### Text Scale
- **Near Black** (#222222): primary text — warm, not cold
- **Secondary Gray** (#6a6a6a): descriptions
```

AI 读到这里就知道，#ff385c 是品牌红，主要用于 CTA 按钮；#222222 是主文本色，不是纯黑。

### 3. Typography Rules

字体规范。包括字体家族选择和完整的层级表。

```markdown
| Role | Font | Size | Weight | Line Height |
| Section Heading | Airbnb Cereal VF | 28px | 700 | 1.43 |
| Card Heading | Airbnb Cereal VF | 22px | 600 | 1.18 |
| Button | Airbnb Cereal VF | 16px | 500 | 1.25 |
```

层级表是 AI 生成一致 UI 的关键。不同品牌的同类文本必须用相同的字重、字号、行高。

### 4. Component Stylings

组件样式规范。按组件类型分：按钮、卡片、输入框、导航等。

```markdown
### Buttons
**Primary Dark**
- Background: #222222
- Text: #ffffff
- Padding: 0px 24px
- Radius: 8px

### Cards & Containers
- Background: #ffffff
- Radius: 20px
- Shadow: rgba(0,0,0,0.02)... (三层阴影)
```

每个组件都有具体的参数，而不是模糊的"大气"或"精致"。

### 5. Layout Principles

布局规范。间距系统、网格、留白哲学。

```markdown
### Spacing System
- Base unit: 8px
- Scale: 2px, 4px, 8px, 16px, 24px, 32px, 48px, 64px

### Border Radius Scale
- Standard (8px): Buttons, tabs
- Card (20px): Feature cards
- Large (32px): Hero containers
```

### 6. Depth & Elevation

阴影系统。Airbnb 用的是三层阴影叠加：

```markdown
| Level | Treatment |
| Card | rgba(0,0,0,0.02) 0px 0px 0px 1px,
       rgba(0,0,0,0.04) 0px 2px 6px,
       rgba(0,0,0,0.1) 0px 4px 8px |
| Hover | rgba(0,0,0,0.08) 0px 4px 12px |
```

第一层是极淡的边框环，第二层是柔和的环境阴影，第三层是主要提升感。组合起来就有一种"自然的光线感"。

### 7. Do's and Don'ts

设计护栏。这个章节告诉 AI 什么该做什么不该做。

```markdown
### Do
- Use #222222 for text — never pure #000000
- Apply Rausch Red only for primary CTAs

### Don't
- Don't use pure black (#000000) for text
- Don't apply Rausch Red to backgrounds
```

这类规则能防止 AI 在某些地方用错颜色或者过度使用品牌色。

### 8. Responsive Behavior

响应式行为规范。断点、触摸目标、折叠策略。

### 9. Agent Prompt Guide

最后是给 AI 看的快速参考。

```markdown
### Quick Color Reference
- Background: Pure White (#ffffff)
- Text: Near Black (#222222)
- Brand accent: Rausch Red (#ff385c)
```

以及一些可以直接用的组件提示词模板。

## 怎么用

步骤很简单：

```
1. 从 awesome-design-md 选一个喜欢的 DESIGN.md
2. 复制到项目根目录
3. 告诉 AI："参考这个 DESIGN.md 做页面"
4. 验证结果
```

以 Airbnb 风格为例：

```bash
# 复制 Airbnb 的 DESIGN.md
cp awesome-design-md/airbnb/DESIGN.md ./

# 告诉 AI
"用 DESIGN.md 的风格，做一个落地页"
```

剩下的就是 AI 的工作了。

## 如果我想建自己的 DESIGN.md 呢

这个是我觉得最有意思的部分。

DESIGN.md 的格式是固定的 9 个章节，但是具体写什么需要你对自己产品的设计系统有清晰的认识。

换句话说，如果你本来就没有设计系统，DESIGN.md 也救不了你。

但如果你有设计系统，把它们写成 DESIGN.md 的格式，就能让 AI 照着这个规范来生成内容。

**怎么把这个过程自动化？**

我想到的方向是：能不能建一个 skill，让 AI 自动分析一个品牌的网站，然后生成对应的 DESIGN.md？

大概的思路是这样：

1. **输入**：一个网站 URL
2. **第一步**：抓取页面，提取颜色值（从 CSS、SVG、图片）
3. **第二步**：分析字体（从 font-family、heading 层级）
4. **第三步**：识别组件样式（按钮、卡片、输入框的圆角/阴影）
5. **第四步**：总结布局特点（间距系统、网格结构）
6. **输出**：一个符合 Stitch 规范的 DESIGN.md 文件

技术上是可行的。现在有很多工具可以分析网站的设计元素：Chrome DevTools Protocol、Playwright、Cloudflare Workers 的网页抓取 API 等等。

难点在于：**解析的准确性**。AI 生成的 DESIGN.md 如果颜色值差几个 hex，或者把 8px 圆角识别成 12px，后面照着这个生成出来的 UI 就会走样。

不过话说回来，就算不能做到 100% 准确，能有个 80% 的初稿也远比从零开始强。后续再手工微调几个关键参数，比完全从头写要省很多力气。

## 局限性

说完了好用的部分，也得聊聊局限。

**DESIGN.md 能解决的是视觉一致性，不是设计本身。**

它能保证：
- 颜色对
- 字体对
- 组件样式对

它不能保证：
- 这个设计好不好看
- 用户体验流程是否合理
- 内容策略是否正确

还有一个风险：**如果大家都用同样的 DESIGN.md，最后出来的 UI 会不会趋同？**

66 个品牌看着挺多，但毕竟是有限的。大家都用 Stripe 的风格做金融产品，最后可能满屏都是紫色渐变。

多样化是设计的生命。DESIGN.md 是工具，用得好不好还是看人。

**还有一个坑得说一下。**

awesome-design-md 这个项目确实火了，但是火了就变味了。现在你去他们的 GitHub 主页，会发现链接全指向 getdesign.md 和 VoltAgent 的官网。而 getdesign.md 是什么？是一个付费服务。

更骚的操作是这样的：你想复刻一个完整的网站？付钱。DESIGN.md 文件本身免费，但是**生成可用的复刻网站**变成了付费项目。

说白了就是用 DESIGN.md 的概念引流到自己的付费服务。GitHub 上 48k Stars，全是免费流量。

这种感觉就像什么呢？你兴冲冲打开一个"免费食谱大全"的网站，结果发现"查看完整食谱"要付费订阅。GitHub Stars 是有了，但护城河已经挖好了。

不过话说回来，这个模式也没什么问题。开源项目要活下去，总得有个变现方式。只是别天真的以为"48k Stars = 全免费"就行。

## 璞奇启示

> **璞奇启示**
>
> 1. 璞奇的练习卡片、笔记页面也可以用 DESIGN.md 思路来规范视觉。定义一套"璞奇 DESIGN.md"：主色调、卡片样式、间距系统，AI 生成的练习内容自动保持一致。
> 2. DESIGN.md 把"不确定的 AI 输出"封装进"确定的规范框架"。璞奇也可以用类似的思路：用 Markdown 定义练习模板的结构和格式，让 AI 生成的内容有规可循。
> 3. 建一个"分析网站 → 输出 DESIGN.md"的 skill，在技术上是可行的，难点在于解析准确性。如果能解决这个，设计师的效率会大幅提升。

---

**相关链接：**

- awesome-design-md：https://github.com/VoltAgent/awesome-design-md
- Google Stitch：https://stitch.withgoogle.com/
- VoltAgent：https://github.com/VoltAgent/voltagent
