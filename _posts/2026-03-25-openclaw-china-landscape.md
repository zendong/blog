---
title: "2026国内OpenClaw类产品统计：10+产品全景对比"
date: 2026-03-25
categories:
  - 技术
tags:
  - openclaw
  - ai-agent
  - 人工智能
  - 产品分析
  - 大模型
layout: post
image_prompt: "A futuristic tech landscape visualization: multiple glowing digital interfaces representing different AI agent products floating in a cosmic void, each interface displaying Chinese characters and tech symbols, connected by flowing data streams and neural network patterns, color palette of deep blue purple with bright cyan and magenta accents, abstract isometric cityscape of digital products, clean minimalist aesthetic with holographic elements, no text characters visible, digital art style depicting the AI agent ecosystem diversity in China 2026"
image_prompt_file: "assets/prompt/2026-03-25/2026-03-25-openclaw-china-landscape.txt"
---

> "独学而无友，则孤陋而寡闻。" — 《礼记·学记》

2026年3月，OpenClaw以32万Stars超越Linux，成为GitHub史上增长最快的开源项目。这股「养虾」热潮也迅速蔓延至国内各大云厂商和AI公司。本文盘点国内各类OpenClaw类产品的能力、模型支持、渠道集成等维度，供选型参考。

![首图](https://blog.zendong.com.cn/assets/images/2026/2026-03-25-openclaw-china-landscape.png)

## 一、市场概况

截至2026年3月25日，国内已知的OpenClaw类产品**超过20款**，主要分为三大阵营：

| 阵营 | 数量 | 代表产品 |
| --- | --- | --- |
| 大厂商业版 | ~10款 | KimiClaw、AutoClaw、MaxClaw、ArkClaw、QClaw、DuClaw、CoPaw、WorkBuddy、Linclaw、Molili |
| 开源社区版 | ~5款 | ZeroClaw、NanoClaw、CowAgent、三省六部制/edict、AionUi |
| 工具生态版 | ~5款 | Cherry Studio、DuMate等 |

---

## 二、大厂商业版横向对比

### 2.1 产品速查表

| 产品 | 厂商 | 部署方式 | 国内渠道 | 模型支持 | 开源 | 定价 |
| --- | --- | --- | --- | --- | --- | --- |
| **KimiClaw** | 月之暗面 | 云端SaaS | 飞书深度 | Kimi K2.5（主力）、DeepSeek | 否 | 199元/月（含额度） |
| **AutoClaw（澳龙）** | 智谱AI | 本地桌面 | 飞书一键接入 | GLM-5、Pony-Alpha-2（专属）、DeepSeek、Kimi、MiniMax | 否 | 免费额度+积分包 |
| **MaxClaw** | MiniMax | 云端SaaS+移动端 | 飞书/钉钉 | MiniMax全系模型 | 否 | 39元/月+Coding Plan |
| **ArkClaw** | 字节跳动火山引擎 | 云端托管 | 飞书深度 | 豆包、Claude、文心ERNIE | 部分 | 需coding plan |
| **QClaw** | 腾讯电脑管家 | macOS/Win客户端 | 微信直联 | 混元、ChatGPT | 否 | 内测中 |
| **DuClaw** | 百度智能云 | 云端+手机 | 百度系 | 文心ERNIE | 否 | 预发布 |
| **CoPaw** | 阿里云 | 本地+云端双模式 | 钉钉、飞书、QQ、Discord、iMessage | 通义千问、DeepSeek、Ollama | 是（Apache 2.0） | 免费开源 |
| **WorkBuddy** | 腾讯 | 桌面应用 | 企业微信、微信、QQ、飞书、钉钉 | 混元、CodeBuddy | 否 | 企业级 |
| **Linclaw** | 七牛云 | DMG/EXE/pip | 9大渠道全覆盖 | 七牛云MaaS（DeepSeek/Kimi/GLM/MiniMax） | MIT | 按量付费 |
| **Molili** | 当贝 | 本地一键安装 | 微信、钉钉、飞书、Siri | DeepSeek、MiniMax、通义千问、Kimi、智谱GLM | 否 | 订阅制 |
| **DuMate（搭子）** | 百度 | 手机端 | 百度系 | 文心ERNIE | 否 | 3月17日上线 |

### 2.2 核心能力对比

| 产品 | 技能/Skills | 浏览器自动化 | 本地文件访问 | 记忆持久化 | 定时任务 |
| --- | --- | --- | --- | --- | --- |
| KimiClaw | 5000+技能库 | 支持 | 云端存储 | 40GB云存储 | 支持 |
| AutoClaw | 50+预置 | AutoGLM Browser-Use | 本地执行 | 飞书同步 | 支持 |
| MaxClaw | 专家团预设 | 支持 | 有限 | 云端 | 支持 |
| ArkClaw | 预置20项技能 | 支持 | 云端沙箱 | 支持 | 支持 |
| CoPaw | 可扩展 | 支持 | 本地/云端 | 长期记忆 | 支持 |
| Molili | 8000+技能 | 支持 | 精细化权限 | 支持 | 支持 |
| QClaw | 20+技能包 | 支持 | 本地 | 支持 | 支持 |

---

## 三、开源社区版横向对比

| 产品 | GitHub Stars | 语言/架构 | 部署方式 | 国内渠道 | 开源协议 | GitHub仓库 |
| --- | --- | --- | --- | --- | --- | --- |
| **CowAgent** | 42.2k ⭐ | Python/pip | 本地部署 | 微信/飞书/钉钉/企业微信 | MIT | [zhayujie/cowagent](https://github.com/zhayujie/cowagent) |
| **Cherry Studio** | 41.5k | DMG/EXE/Linux | 桌面安装 | 多渠道接入 | Apache 2.0 | [CherryHQ/cherry-studio](https://github.com/CherryHQ/cherry-studio) |
| **ZeroClaw** | 27.3k | Rust单二进制 | 单文件 | Provider自配 | MIT | [zeroclaw-labs/zeroclaw](https://github.com/zeroclaw-labs/zeroclaw) |
| **NanoClaw** | 23.3k | Docker | 容器化 | Provider自配 | MIT | [qwibitai/nanoclaw](https://github.com/qwibitai/nanoclaw) |
| **三省六部制/edict** | 9.7k | Python | 多Agent编排 | 多渠道 | MIT | [cft0808/edict](https://github.com/cft0808/edict) |
| **CoPaw** | — | Python | 本地+云端 | 钉钉/飞书/QQ等 | Apache 2.0 | [modelscope/AgentScope](https://github.com/modelscope/AgentScope) |
| **AionUi** | 18.9k | 桌面安装包 | AI工具统一管理 | 多渠道 | MIT | [iOfficeAI/aionui](https://github.com/iOfficeAI/aionui) |

### 开源版特点分析

**CowAgent（42.2k Stars）**——GitHub Stars最高
- 支持微信、飞书、钉钉、企业微信四大渠道
- 内置LinkAI知识库
- 适合企业微信自部署场景

**Cherry Studio（41.5k Stars）**——模型支持最广
- 支持300+模型接入
- 知识库RAG问答
- 多模型对话客户端

**ZeroClaw（27.3k Stars）**——最轻量
- Rust单二进制，16MB内存
- 适合嵌入式/IoT场景

---

## 四、兼容OpenClaw生态情况

### 4.1 技能兼容度分类

| 兼容等级 | 产品 | 说明 |
| --- | --- | --- |
| **完全兼容** | CoPaw、ZeroClaw、NanoClaw、CowAgent | 直接使用OpenClaw的Skills生态 |
| **部分兼容** | AutoClaw、ArkClaw、MaxClaw、Linclaw | 预置Skills或转换层 |
| **不兼容** | KimiClaw、DuClaw、DuMate | 自主生态体系 |

### 4.2 模型调用能力对比

| 产品 | Claude | GPT-5 | DeepSeek | Kimi K2.5 | 国产模型 |
| --- | --- | --- | --- | --- | --- |
| OpenClaw（原版） | ✅ | ✅ | ✅ | ✅ | ✅ |
| KimiClaw | ❌ | ❌ | ✅ | ✅⭐ | ❌ |
| AutoClaw | ✅ | ❌ | ✅ | ✅ | ✅ GLM |
| MaxClaw | ✅ | ❌ | ✅ | ❌ | ✅ MiniMax |
| ArkClaw | ✅ | ✅ | ✅ | ❌ | ✅ 豆包/ERNIE |
| CoPaw | ✅ | ✅ | ✅ | ✅ | ✅ 通义千问 |
| Linclaw | ✅ | ✅ | ✅ | ✅ | ✅ 全覆盖 |

---

## 五、垂直场景推荐

| 场景 | 推荐产品 | 理由 |
| --- | --- | --- |
| **飞书重度用户** | ArkClaw、KimiClaw | 原生飞书集成，体验最佳 |
| **微信用户** | QClaw、WorkBuddy | 微信直联，零配置 |
| **企业安全合规** | WorkBuddy、ArkClaw | 闭源部署，权限可控 |
| **技术开发者** | CoPaw、ZeroClaw | 开源可定制，Apache 2.0 |
| **隐私敏感** | AutoClaw（本地）、ZeroClaw | 本地执行，数据不离手 |
| **预算有限** | Molili（成本低）、Linclaw | 订阅制/按量付费 |
| **多模型切换** | Cherry Studio、Linclaw | 300+/全模型覆盖 |
| **嵌入式/IoT** | ZeroClaw | Rust单二进制，16MB |

---

## 六、市场格局分析

### 6.1 四大路线

```
┌─────────────────────────────────────────────────────────┐
│                    国内OpenClaw类产品格局                    │
├─────────────────────────────────────────────────────────┤
│  云端SaaS    │ KimiClaw、MaxClaw、ArkClaw    │ 门槛低   │
│  本地部署    │ AutoClaw、Molili、CoPaw        │ 隐私好   │
│  桌面客户端  │ QClaw、WorkBuddy、Linclaw      │ 体验佳   │
│  开源轻量    │ ZeroClaw、NanoClaw、CowAgent   │ 可定制   │
└─────────────────────────────────────────────────────────┘
```

### 6.2 差异化要点

1. **渠道整合能力**——Linclaw（9大渠道）vs 原版OpenClaw（不支持微信/钉钉）
2. **模型专属优化**——Pony-Alpha-2（AutoClaw）、Kimi K2.5（KimiClaw）
3. **成本控制**——Molili（实测比原版低50%）、Linclaw（按量付费）
4. **部署门槛**——AutoClaw（一键安装1分钟）vs CoPaw（三行命令）

---

## 七、信息说明

- 数据截止时间：2026年3月25日
- GitHub Stars数据为2026年3月中旬统计
- 产品信息和定价以各厂商官方公告为准
- 后续将持续更新产品动态
