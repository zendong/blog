---
title: "Piebald-AI/claude-code-system-prompts：解密 Claude Code 的系统提示词工程"
date: 2026-03-31
categories:
  - 技术
tags:
  - claude-code
  - agent
  - system-prompt
  - agent-teams
  - prompt-engineering
layout: post
image_prompt: "A technical blueprint or schematic diagram showing the internal architecture of an AI coding agent, with interconnected modules labeled like System Prompts, Tools, Sub-Agents, Memory, and System Reminders, floating in a futuristic control room with holographic displays, blue and cyan color scheme, engineering diagram aesthetic, 16:9 aspect ratio"
image_prompt_file: "assets/prompt/2026-03-31/2026-03-31-claude-code-system-prompts-deep-dive.txt"
hero_image_ai_generated: true
---

> "The best code is no code at all. The second best code is the code you can clearly understand." — Jeff Atwood

代码的可理解性来自清晰的架构，而 AI Agent 的"可理解性"——即它为什么以特定方式行为——来自透明的系统提示词工程。Piebald-AI 维护的 [claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts) 仓库（Stars 2000+）完整开源了 Claude Code 的所有系统提示词，让社区第一次得以窥探这个顶级 Agent产品的内部构造。

## 1. 仓库结构：提示词的模块化组织

Claude Code 的系统提示词并非一个巨大的单体文件，而是被精心拆分为**多个关注点分离的模块**：

```
claude-code-system-prompts/
├── system-prompts/           # 核心系统提示词
│   ├── system-prompt-*.md    # 主系统提示词片段
│   └── tool-description-*.md  # 工具描述
├── agent-prompt-*.md         # 子 Agent 提示词
│   ├── agent-prompt-agent-creation-architect.md
│   ├── agent-prompt-agent-hook.md
│   └── agent-prompt-auto-mode-rule-reviewer.md
├── system-reminder-*.md      # 系统提醒
└── utility-prompt-*.md       # 工具提示词
```

### 1.1 System Prompts（核心系统提示词）

主系统提示词被拆分为多个专项文件，每个文件处理一个独立维度：

- **`system-prompt-tone-and-style-code-references.md`** — 定义代码引用风格：*"When referencing specific functions or pieces of code include the pattern `file_path:line_number`"*
- **`system-prompt-agent-memory-instructions.md`** — Agent 记忆系统指令，Claude Code 如何持久化上下文知识
- 等等

这种拆分带来一个关键优势：**热修复特定行为而不影响全局**。如果需要调整 Claude 的代码引用风格，不需要改动整个系统提示词，只需修改那一个文件。

### 1.2 Tool Descriptions（工具描述）

Claude Code 内置 18 个工具，每个工具都有独立的描述文件。这些描述定义了：

1. **工具能力边界** — 工具能做什么、不能做什么
2. **使用约束** — 什么情况下应该/不应该使用
3. **输出格式预期** — Claude 应该期望什么样的返回结构

例如 `tool-description-bash-alternative-write-files.md` 处理的是"哪些场景下 Bash 应该被 Write 文件替代"这一边界问题。

### 1.3 Agent Prompts（子 Agent 提示词）

Claude Code 内部使用多个专业子 Agent（Plan/Explore/Task），每个都有独立提示词：

- **`agent-prompt-agent-creation-architect.md`** — Agent 创建架构师
- **`agent-prompt-agent-hook.md`** — Agent 钩子逻辑
- **`agent-prompt-auto-mode-rule-reviewer.md`** — 自动模式规则审查

这种设计允许 Claude Code 在不同场景下召唤不同的"专家人格"，而不是用同一个提示词处理所有任务。

### 1.4 System Reminders（系统提醒）

System Reminders 是动态注入的上下文片段，用于在运行时提醒 Claude 某些即时性信息（例如 `/btw` 命令的副作用处理）。

## 2. 关键工程洞察

### 2.1 "薄推理内核 + 厚工程控制面"

Claude Code 背后的核心设计哲学可以总结为：

> **好的 agent 系统 = 很薄的推理内核 + 很厚的工程控制面**

Anthropic 并没有依赖一个"更强大的模型"来解决问题，而是通过**精心设计的提示词层次**来约束和引导模型行为。系统提示词不是给模型"更多知识"，而是给模型"更多边界"——告诉它什么时候该用工具、什么时候该停下来等待用户确认、什么时候应该拒绝执行。

### 2.2 上下文隔离与信任边界

从 Piebald 的仓库可以观察到，Claude Code 的提示词设计中大量使用了**上下文隔离模式**：

- 每个子 Agent 有独立的提示词，意味着它只能看到自己"该知道"的信息
- 工具描述明确标注了权限边界
- System Reminders 是按需注入的，不是全量加载

这种设计直接解决了多 Agent 系统中的**信息泄露风险**——如果每个 Agent 都能访问完整上下文，那么它们之间的隔离就毫无意义。

### 2.3 "先串行规划，再并行执行"

从 Agent Teams 的架构可以看出，Claude Code 并不假设"启动多个实例就能自动协作"。真正的协作需要**显式协议**：

1. **Lead Agent**（主会话）先完成整体 SPEC 和接口定义（串行阶段）
2. 基于清晰的接口定义，**Teammates** 才开始独立工作（并行阶段）
3. 最终由 **Lead Agent** 负责集成和仲裁

这与 Piebald 仓库中"agent-creation-architect"的设计思路一脉相承——先规划，再执行。

## 3. Agent Teams：2026 年 2 月发布的多智能体协作系统

### 3.1 核心组件

Agent Teams 是 Claude Code 在 2026 年 2 月推出的实验性功能，代表了 AI 辅助编程从单点智能向**群体智能**的关键演进：

```
┌─────────────────────────────────────────────────────┐
│                    Lead Agent                        │
│  (主会话: 任务拆解、委派、进度追踪、最终集成)         │
├─────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ Teammate │  │ Teammate │  │ Teammate │          │
│  │ (前端)   │  │ (后端)   │  │ (测试)   │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│         ↕           ↕           ↕                  │
│  ┌─────────────────────────────────────────────┐  │
│  │          Shared: Task List + Mailbox          │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### 3.2 核心能力

| 能力 | 说明 |
|------|------|
| **并行工作** | 多个 Claude 实例同时处理不同任务 |
| **任务列表管理** | pending/in-progress/completed 状态追踪 |
| **Mailbox 系统** | 队友间直接通信，无需都通过 Lead 中转 |
| **文件所有权** | 按目录/模块划分修改权限 |

### 3.3 四层工程决策

Agent Teams 引入了一套**显式协作协议**，包含四个关键层次：

1. **上下文隔离边界** — 明确谁该看到什么信息，关键信息必须通过共享文件或 Mailbox 显式传递
2. **调度策略** — 手动定义第一层任务拆分，而非让 Lead 自动拆分
3. **失败处理** — 建立断路器机制（终止/纠偏/重对齐三种回退策略）
4. **合并仲裁** — 明确谁负责合并、冲突解决规则和验收命令

### 3.4 启用方式

```bash
# 方式一：配置文件
# ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}

# 方式二：环境变量
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### 3.5 何时使用 Agent Teams

Agent Teams 适合的场景：
- 项目太大，单个 AI 顾此失彼
- 需要同时进行代码审查、写测试、写文档
- 需要从多个角度同时排查问题

**不适合**的场景：
- 简单的一次性任务（反而增加协调开销）
- 需要强上下文一致性的工作（多 Agent 信息传递有延迟）
- 成本敏感的项目（每个队友是完整的 Claude Code 实例，消耗翻倍）

## 4. 总结

Piebald-AI 的 claude-code-system-prompts 仓库为我们提供了一扇窗口，让我们得以理解 Claude Code 这个世界级 Agent 产品背后的**提示词工程哲学**：

1. **模块化** — 将系统提示词拆分为关注点分离的独立文件，实现独立热修复
2. **层次化** — 通过 System Prompt → Agent Prompts → Tool Descriptions → System Reminders 的层次结构，渐进式构建 Agent 行为
3. **显式协作** — Agent Teams 展示的"先规划再并行"工程方法论，而非简单启动多个实例期望自动协作

开源社区能够完整看到这些提示词，本身就是一件值得尊敬的事——它让 AI Agent 的行为不再是黑箱，让用户能够真正理解和掌控自己的工具。

---

*参考资料：*
- *[Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts)*
- *[Claude Code Agent Teams 完全指南](https://blog.csdn.net/u010634066/article/details/157903022)*
- *[Agent模式与框架——Claude Agent Teams 架构解读](https://blog.csdn.net/qq_54655817/article/details/157900747)*
