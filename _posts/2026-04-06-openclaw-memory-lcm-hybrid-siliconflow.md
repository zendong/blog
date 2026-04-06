---
title: "「会话 ≠ 笔记」OpenClaw 记忆手记：LCM × Hybrid（暂不用 QMD）"
date: 2026-04-06
categories:
  - 技术
tags:
  - openclaw
  - lossless-claw
  - memory-search
  - siliconflow
  - 配置
layout: post
image_prompt: "Playful Pixar-style 3D: a friendly cyber-lobster with reading glasses and a tiny professor hat juggles two glowing spheres—one holds a miniature conversation DAG, the other floating markdown pages with magnifying glasses and light beams; coral-orange and electric-teal, warm rim light, whimsical tech hero, 16:9, no legible text"
image_prompt_file: "assets/prompt/2026-04-06/2026-04-06-openclaw-memory-lcm-hybrid-siliconflow.txt"
---

> "教学相长。" — 《礼记·学记》

把 OpenClaw 的「会话层」和「笔记层」一次配稳：用 **lossless-claw（LCM）** 承接长对话与 DAG 溯源；笔记层检索有两种常见路径——**默认**使用 **内置（builtin）SQLite 索引 + memory-search + Hybrid（向量 + BM25）**；也可将全局 **`memory.backend` 设为 `qmd`**，改用 **QMD 本地侧车**（BM25 + 向量 + 重排，经 `qmd query --json` 召回），Markdown 仍是唯一事实来源。本文给出可照抄的配置结构、每一步的原因、**硅基流动（SiliconFlow）** OpenAI 兼容 Embeddings 的对接方式（主要用于 **builtin** 侧），以及 **QMD 的原理、前置条件与 `memory.qmd.*` 配置**。实践素材来自 **本机实操环境** 的部署与验证。

![首图](https://blog.zendong.com.cn/assets/images/2026/2026-04-06-openclaw-memory-lcm-hybrid-siliconflow.png)

## 名词解释

下文用词若不加说明，含义如下（**「笔记」不是「会话」**）：

| 名词                | 指什么                                                                                                                                                                                                |
| ------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **会话 / 会话历史** | 你与 Agent **聊天过程**中的消息流；由 **lossless-claw（LCM）** 写入 **`~/.openclaw/lcm.db`**，用 `lcm_grep` 等工具搜的是这层。                                                                        |
| **笔记 / 笔记文件** | 工作区里 **落盘的 Markdown**，主要是 **`MEMORY.md`**、**`memory/`** 等；由 **`memory_search`** 在 **内置索引**里检索，**不是**会话记录的别名。                                                        |
| **笔记层**          | 文内对「笔记文件 + 其索引与检索」的统称，与 **会话层（LCM）** 并列。                                                                                                                                  |
| **memory-search**   | OpenClaw **内置**能力，在配置里对应 **`agents.defaults.memorySearch`**；Agent 侧工具一般为 **`memory_search`**。                                                                                      |
| **builtin 后端**    | **`memory.backend` 未写或为默认语义时**：OpenClaw 用 **`MemoryIndexManager`** 在工作区 Markdown 上建本地 SQLite 索引（向量表 + 可选 FTS5 关键词），由 **`memorySearch`** 控制嵌入提供方与 Hybrid 等。 |
| **QMD 后端**        | **`memory.backend: "qmd"`** 时：检索改由 **QMD CLI** 侧车执行（`qmd update` / `qmd embed` / `qmd query`），OpenClaw **透传配置**并在失败时 **自动回退 builtin**；与 LCM 仍无关。                      |
| **Hybrid**          | **builtin** 下：**向量相似度 + BM25（FTS5）** 混合排序（可配权重）。**QMD** 下：混合与重排在 QMD 内完成，OpenClaw 侧用 **`memory.qmd.*`** 调参。                                                      |
| **sqlite-vec**      | SQLite 的向量扩展，用于在 **记忆索引库**里加速向量检索；OpenClaw **默认尝试使用自带扩展**，一般 **无需** 自装 npm 包、**无需** 配置 `extensionPath`。                                                 |
| **记忆索引库**      | 存放 chunk、向量、FTS 等的 **SQLite 文件**，路径由 **`store.path`** 决定（见第四节）。与 **`lcm.db`** 是 **两个库**。                                                                                 |

---

## 一、两套系统各自解决什么问题

| 组件                        | 数据落点                                                                                        | 典型能力                                                                      | 何时起作用                                                     |
| --------------------------- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------------------------------------- |
| **lossless-claw**           | `~/.openclaw/lcm.db`                                                                            | 对话原文持久化、摘要 DAG、`lcm_grep` / `lcm_describe` / `lcm_expand_query` 等 | **每一轮**都会参与上下文组装；**搜索类工具**在模型调用时才执行 |
| **memory-search（Hybrid）** | 内置索引（默认 SQLite，见官方 [Memory 配置](https://docs.openclaw.ai/reference/memory-config)） | 对 `MEMORY.md`、`memory/**/*.md` 做 **向量相似度 + BM25 关键词** 合并排序     | 模型调用 **`memory_search`** 时                                |

**为什么要同时开 Hybrid，而不是关掉 BM25 只取向量？**

- **笔记层**里常有 **精确串**：commit id、报错原文、环境变量名、配置键。官方 [Memory Search](https://docs.openclaw.ai/concepts/memory-search) 说明：向量擅长「意思相近」，BM25 擅长「 token 级别命中」；Hybrid 是二者加权合并，更适合真实笔记。
- **LCM 的「关键字」**（如 `lcm_grep`）搜的是 **会话库**，与 **笔记文件索引** 不是同一张表；不能互相替代。

**笔记检索在配置里分两层**：

1. **全局后端**：根级 **`memory.backend`** —— **`builtin`（默认）** 或 **`qmd`**（见第四节「QMD 后端」）。
2. **builtin 时的嵌入与查询细节**：**`agents.defaults.memorySearch`**（启用、provider、Hybrid、store 等）。

Agent 侧工具名仍为 **`memory_search`** / **`memory_get`** 等；**`memory.citations`**（`auto` / `on` / `off`）对两种后端均生效。下文 **硅基流动 Embeddings** 主要针对 **builtin**；若长期只用 QMD 且从不回退，仍建议保留可用的 **`memorySearch`**，以便 QMD 异常时回退仍有向量索引。

**Workspace 常驻文件（与 LCM / memory 的关系）**：`SOUL.md`、`USER.md`、`AGENTS.md`、`HEARTBEAT.md` 等多作为 **系统侧常驻注入**；**`MEMORY.md`** 与 **`memory/`** 由 **`memory_search`** 检索（见上文「笔记」定义）。**LCM 不替代笔记文件的维护与索引**：会话在 **`lcm.db`**，笔记在工作区磁盘 + **记忆索引库**。

| 文件              | 常见作用                                  |
| ----------------- | ----------------------------------------- |
| `SOUL.md`         | 人格与行为准则                            |
| `USER.md`         | 用户偏好与上下文                          |
| `MEMORY.md`       | 长期事实与决策（由 `memory_search` 检索） |
| `AGENTS.md`       | 多 Agent 路由规则                         |
| `HEARTBEAT.md`    | 周期性任务清单                            |
| `BOOTSTRAP.md` 等 | 依你工作区约定                            |

---

## 一点五、方案对比与最终选型（builtin + lossless-claw）

下表便于与官方 [Memory](https://docs.openclaw.ai/concepts/memory) 对照，**不涉及**实验性 [Research · memory](https://docs.openclaw.ai/experiments/research/memory) 里的未来布局。

| 维度                   | **lossless-claw（LCM）**                                        | **笔记层：builtin `memorySearch`**                                          | **笔记层：可选 QMD（`memory.backend: "qmd"`）**                                 |
| ---------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **解决什么问题**       | 长对话持久化、摘要 DAG、会话内 **关键词/回溯**（`lcm_grep` 等） | 工作区 Markdown 的 **语义 +（FTS 可用时）关键词** 混合检索                  | 侧车内 **BM25 + 向量 + 重排**；Markdown 仍为事实来源                            |
| **配置主入口**         | `plugins.slots.contextEngine` + `plugins.entries`               | `agents.defaults.memorySearch`（+ 默认 `memory.backend` 为 builtin）        | 根级 `memory`：`backend: "qmd"` + `memory.qmd.*`                                |
| **嵌入（向量）**       | 不适用                                                          | **远程**（OpenAI 兼容 / Gemini 等）或 **本地** GGUF，由 `memorySearch` 配置 | **QMD 本地**管线（GGUF 等）；**OpenClaw 不会**把 `memorySearch.remote` 传给 QMD |
| **远程 Embedding API** | 不适用                                                          | **一等公民**：`memorySearch.remote` + provider                              | 若需 **纯远程向量**，应优先 **builtin**，而非 QMD                               |
| **失败/降级**          | 以 LCM 文档为准                                                 | FTS 缺失时见 **第八节**；QMD 失败时若开启 QMD 会 **回退 builtin**           | 子进程失败 → **回退 builtin**                                                   |
| **依赖与运维**         | 插件 + `lcm.db`                                                 | Node + 嵌入 API Key（远程时）+ 可选 sqlite-vec                              | 另需 **Bun、QMD CLI、可加载扩展的 SQLite**、首次 HF 模型下载等                  |

**本文最终选型结论（落地配置）**

- **会话层**：**lossless-claw**（长对话与 DAG 工具链）。
- **笔记层**：**memory 使用 builtin 后端**（不显式写 `memory.backend: "qmd"`，或等价于保持默认），配合 **`agents.defaults.memorySearch`**（含 **远程 Embeddings**，例如硅基流动 OpenAI 兼容端点）与 **Hybrid**（在 FTS 可用时）。
- **不采用 QMD 作为主路径** 时的理由：希望 **向量走远程 API**、减少本机 GGUF 与侧车运维；与官方说明一致——**远程 Embedding 以 builtin `memorySearch` 配置为准**。

若日后需要 QMD 的检索流水线，可再启用 `memory.backend: "qmd"`，并保留可用的 `memorySearch` 以便 **自动回退**。

---

## 二、前置条件

- **OpenClaw**：建议 **2026.3.7+**（支持 Context Engine 插件槽位）；本机实操环境为 **2026.3.24**。
- **Node.js**：**≥ 22**（本机实操环境为 v23.11.1）。**SQLite**：随 Node 自带的 `node:sqlite` 即可满足 OpenClaw 与 LCM 的常规读写，**无需**单独安装系统级 SQLite 命令行工具（除非你打算用手动 `sqlite3` 排查库文件）。
- **硅基流动账号**（**builtin + 远程 Embeddings** 时）：在 [控制台](https://cloud.siliconflow.cn/) 创建 API Key；Embeddings 文档见 [创建嵌入请求](https://docs.siliconflow.cn/cn/api-reference/embeddings/create-embeddings)。

---

## 三、安装并启用 lossless-claw

在项目或本机执行：

```bash
openclaw plugins install @martian-engineering/lossless-claw
openclaw gateway restart
```

安装器一般会写入插件槽位，并可能写入根级 **`allow`**（插件白名单）等字段；若需手写，核心是让 **`plugins.slots.contextEngine` 指向 `lossless-claw`**，并在 **`plugins.entries`**（注意与根目录误写的 `entries` 区分）里展开参数。

**推荐起步参数（与 [lossless-claw 配置说明](https://github.com/Martian-Engineering/lossless-claw/blob/main/docs/configuration.md) 一致）：**

| 配置项                | 建议值 | 原因                                                           |
| --------------------- | ------ | -------------------------------------------------------------- |
| `freshTailCount`      | `32`   | 最近若干条消息不压缩，保证工具调用多的场景下「当前回合」仍可读 |
| `contextThreshold`    | `0.75` | 占用上下文窗口比例达阈值再触发压缩，平衡摘要次数与溢出风险     |
| `incrementalMaxDepth` | `-1`   | 长会话需要更深的自动冷凝时，避免 DAG 只停在浅层                |

**SQLite 路径**：默认 **`~/.openclaw/lcm.db`**。

### 3.1 LCM 数据库表（速查）

可用 DBeaver、**`sqlite3 ~/.openclaw/lcm.db`** 等查看。核心表与用途如下（便于排查「数据写没写进去」）。

| 表名               | 用途                                         |
| ------------------ | -------------------------------------------- |
| `conversations`    | 会话维度：session、标题、时间等              |
| `messages`         | 原始消息，按 `conversation_id` 与序号组织    |
| `summaries`        | 摘要节点（DAG 核心），含 leaf / condensed 等 |
| `summary_messages` | 摘要与原始消息的多对多映射                   |
| `summary_parents`  | 摘要节点父子关系，构成 DAG                   |
| `message_parts`    | 消息细粒度拆分（text、reasoning、tool 等）   |
| `context_items`    | 当前上下文窗口内活跃项，决定送入模型的内容   |

辅助表包括 **`large_files`**（大文件外置）、**`conversation_bootstrap_state`**（引导与断点恢复）等。

**设计要点**：`summary_parents` + `depth` 体现 DAG 分层；`context_items` 支撑「当前窗口」与还原；`conversation_bootstrap_state` 支撑重启后增量恢复。

### 3.2 LCM 工具链与召回场景

lossless-claw 对外常见 **四个工具**（名称以你安装版本为准）：主 Agent 可直接用 **`lcm_grep`**、**`lcm_describe`**、**`lcm_expand_query`**；**`lcm_expand`** 多由子 Agent 在深度召回流程中调用。

| 工具               | 角色                                                  |
| ------------------ | ----------------------------------------------------- |
| `lcm_grep`         | 关键词 / 正则，在消息与摘要中 **定位**                |
| `lcm_describe`     | 查看某摘要节点的 **完整摘要内容**                     |
| `lcm_expand_query` | 摘要不足时 **沿 DAG 回溯** 原始消息（可拉起子 Agent） |
| `lcm_expand`       | 深度召回链路 **内部** 使用                            |

**典型链路**：`lcm_grep` → 命中摘要 id → `lcm_describe` → 若仍不足或出现需展开标记 → `lcm_expand_query`（内部再调 `lcm_expand`）。

**召回场景对照**

| 场景                                | 大致链路                                                    |
| ----------------------------------- | ----------------------------------------------------------- |
| 日常多轮对话                        | Workspace 常驻文案 + LCM 组装的 `context_items` → 模型      |
| 问「以前笔记里写过什么」            | `memory_search`（Hybrid）→ 模型                             |
| 长对话变长触发压缩                  | 达 `contextThreshold` → DAG 摘要更新 → `context_items` 变化 |
| 问「以前对话里某句原话 / 某次错误」 | `lcm_grep` → `lcm_describe` → 必要时 `lcm_expand_query`     |

---

## 四、配置 memory-search（builtin）与可选 QMD 后端

以下片段需合并进你的 **`openclaw.json`**（路径以你本机为准，常见为 **`~/.openclaw/openclaw.json`**）。格式可用 JSON5 风格注释，若你的环境仅支持严格 JSON，请删除注释。

### 4.1 builtin 与 QMD：原理对照

| 维度         | **builtin（默认）**                                                                 | **QMD（`memory.backend: "qmd"`）**                                                                                              |
| ------------ | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **事实来源** | 工作区 Markdown（`MEMORY.md`、`memory/**/*.md` 等）                                 | 相同；仍是磁盘上的 Markdown                                                                                                     |
| **索引位置** | OpenClaw 管理的 SQLite（如 `~/.openclaw/memory/{agentId}.sqlite`）                  | QMD 在 **`~/.openclaw/agents/<agentId>/qmd/`** 下自包含配置、缓存与 SQLite（通过设置 **`XDG_CONFIG_HOME` / `XDG_CACHE_HOME`**） |
| **检索实现** | 进程内 **`MemoryIndexManager`**：向量（sqlite-vec 若可用）+ 可选 FTS5 + Hybrid 合并 | **子进程**：`qmd update` / `qmd embed` 建索引，`qmd query --json` 查；侧车内 **BM25 + 向量 + 重排**                             |
| **失败时**   | 无外层回退                                                                          | **自动回退 builtin**（日志告警后继续可用）                                                                                      |
| **嵌入 API** | 由 **`agents.defaults.memorySearch`**（OpenAI / Gemini / 本地等）提供               | 由 QMD 本地管线（Bun + **node-llama-cpp** 等）与下载的模型负责；**不等同于**你在 `memorySearch` 里配的硅基端点                  |

**何时考虑 QMD**：需要 **更强本地混合检索 / 重排**，且能接受 **额外磁盘与首次模型下载**；**小机器或只要简单语义召回** 时 **builtin + sqlite-vec + 远程嵌入** 往往足够。

**`memory.citations`**（`auto` / `on` / `off`）两种后端都适用；snippet 在 `auto`/`on` 下可带 **`Source: <path#line>`** 页脚（详见 [Memory](https://docs.openclaw.ai/concepts/memory)）。

### 4.2 Hybrid 显式开启（builtin；与默认一致，便于审阅）

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        enabled: true,
        query: {
          hybrid: {
            enabled: true,
            vectorWeight: 0.7,
            textWeight: 0.3,
            candidateMultiplier: 4,
          },
        },
      },
    },
  },
}
```

**原因简述**：`enabled: true` 为官方默认行为；写进配置是为了 **代码审阅与文档化**。权重和倍率可按笔记规模微调，详见 [memory-config](https://docs.openclaw.ai/reference/memory-config)。**仅对 builtin 后端有意义**；若 **`memory.backend` 为 `qmd`**，笔记检索以 QMD 为主，本节仍建议保留以便 **回退**。

### 4.3 对接硅基流动：OpenAI 兼容端点 + 远程 Key

硅基流动提供 **`POST /v1/embeddings`**，Base URL 为 **`https://api.siliconflow.cn/v1`**（见官方 OpenAPI 中的 `servers`）。OpenClaw 侧使用 **`provider: "openai"`** 并通过 **`memorySearch.remote`** 指向该 Base URL，即可走 **OpenAI 兼容 Embeddings**。

**模型选择（需在硅基控制台确认当前上架）：**

- 采用 Qwen/Qwen3-Embedding-4B，理论上够用，价格便宜。

完整示例（请将 API Key 换为环境变量注入或私密存储，**勿提交到公开仓库**）：

```json5
{
  agents: {
    defaults: {
      memorySearch: {
        enabled: true,
        provider: "openai",
        model: "Qwen/Qwen3-Embedding-4B",
        remote: {
          baseUrl: "https://api.siliconflow.cn/v1",
          apiKey: "sk-xxxxxxxx",
        },
        query: {
          hybrid: {
            enabled: true,
          },
        },
      },
    },
  },
}
```

**原因说明：**

- **`provider: "openai"`**：使用 OpenClaw 内置的 OpenAI 风格 Embedding 客户端；**不是**指你必须使用 OpenAI 官方，而是 **协议兼容**。
- **`remote.baseUrl` + `remote.apiKey`**：官方 [memory-config](https://docs.openclaw.ai/reference/memory-config) 说明，自定义 OpenAI 兼容端点在此填写；硅基流动使用 Bearer Token，与 OpenAI 一致。
- **更换模型或维度**后，通常需要 **重建索引**（见 **4.4 节**）。

**安全建议**：生产环境用 **环境变量或系统密钥管理** 注入 `apiKey`，避免明文写在仓库里的 `openclaw.json`。

### 4.4 记忆索引库路径与 sqlite-vec（builtin；默认不必配）

**默认建议**：**不要** 在配置里写 **`store.vector.extensionPath`**，也 **不必** 单独 `npm install sqlite-vec`。OpenClaw 会 **优先使用自带的** sqlite-vec（若可用），在 SQLite 里用 `vec0` 做向量检索；若扩展 **加载失败**，会 **自动回退** 到进程内余弦相似度（仍可用，数据量极大时可能更慢）。详见 [memory-config](https://docs.openclaw.ai/reference/memory-config) 中的 **`store.vector`**。

**记忆索引库（默认磁盘位置）**：**builtin** 下索引 SQLite 的路径由 **`agents.defaults.memorySearch.store.path`** 控制，官方默认约为：

`~/.openclaw/memory/{agentId}.sqlite`

其中 **`{agentId}`** 随你的 Agent 标识变化（常见如 `main`），实际文件请以 **`openclaw memory status`** 或当前版本文档为准。这与 **LCM 的 `~/.openclaw/lcm.db`** 是 **两个不同文件**。**QMD** 另有独立库与目录（见 **4.2 节**）。

**可选**：只有当你需要 **自定义索引文件位置** 时，再设置 **`store.path`**；一般不必动。

---

## 五、与 LCM 配套的「会话与兜底压缩」

LCM **不负责** Session 何时被销毁；若空闲过早重置，对话键会变，体验像「失忆」。

```json5
{
  session: {
    reset: {
      mode: "idle",
      idleMinutes: 10080,
    },
  },
}
```

- **`mode: "idle"`**：空闲超时后再重置。
- **`idleMinutes: 10080`**：约 **7 天**，可按需改为 `1440`（1 天）、`43200`（30 天）等。

避免 **内置 compaction** 与 LCM 抢活：将默认压缩改为 **safeguard**（仅在「危险/兜底」场景介入，具体语义以你当前 OpenClaw 版本文档为准）：

```json5
{
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard",
      },
    },
  },
}
```

---

## 六、合并后的配置骨架（单文件参考）

将下列结构与你现有的 `plugins`、`models` 等 **合并**，不要覆盖未提及的键。**若使用 QMD**，在根级增加 **`memory`** 块（见 **4.2 节** 示例），并与下方 **`memorySearch`** 并存以便回退。

```json5
{
  plugins: {
    slots: {
      contextEngine: "lossless-claw",
    },
    entries: {
      "lossless-claw": {
        enabled: true,
        config: {
          freshTailCount: 32,
          contextThreshold: 0.75,
          incrementalMaxDepth: -1,
        },
      },
    },
  },
  session: {
    reset: {
      mode: "idle",
      idleMinutes: 10080,
    },
  },
  agents: {
    defaults: {
      compaction: {
        mode: "safeguard",
      },
      memorySearch: {
        enabled: true,
        provider: "openai",
        model: "Qwen/Qwen3-Embedding-4B",
        remote: {
          baseUrl: "https://api.siliconflow.cn/v1",
          apiKey: "sk-xxxxxxxx",
        },
        query: {
          hybrid: {
            enabled: true,
            vectorWeight: 0.7,
            textWeight: 0.3,
          },
        },
      },
    },
  },
}
```

若安装器还写入了 **`allow`** 等插件白名单字段，请保留安装器生成的那一段。

---

## 七、改完配置后必做的验证与索引

1. **重启 Gateway**

```bash
openclaw gateway restart
```

2. **查看记忆索引状态**

```bash
openclaw memory status
```

若索引为空或更换了 embedding 模型，执行强制重建（官方 [Memory Search 故障排除](https://docs.openclaw.ai/concepts/memory-search)）：

```bash
openclaw memory index --force
```

3. **插件列表确认**

```bash
openclaw plugins list
```

确认 **lossless-claw** 为启用状态。

---

## 八、Node 内置 SQLite 与全文索引（FTS5）：现象与 OpenClaw 官方解法

部分 Node 发行版自带的 **`node:sqlite`** 在 **编译选项** 中 **未包含 FTS5**（`PRAGMA compile_options` 里看不到 `ENABLE_FTS5`），运行时会报 **`no such module: fts5`**。这与「系统 `sqlite3` 命令行是否支持 FTS5」**不是同一套二进制**，因此会出现：**命令行 `sqlite3` 正常，但 builtin 记忆索引里 FTS 仍不可用**。

此处「全局」指 **跨笔记文件的全文检索**（FTS5 虚拟表），不是单文件内 grep。

### 8.1 官方文档给出的处理方式（builtin 记忆检索）

依据官方 [Memory](https://docs.openclaw.ai/concepts/memory) 文档中 **Hybrid search** 与合并策略的说明：

1. **FTS5 无法创建时**：**不硬失败**，改为 **仅向量检索（vector-only）**——仍可对 `MEMORY.md`、`memory/**/*.md` 做 **语义相似度** 搜索；**BM25 关键词这一路** 不再参与（Hybrid 退化为事实上的向量主导）。
2. **嵌入不可用或返回零向量**：文档说明仍会尽量跑 **BM25** 关键词侧（与上条互为补充场景）。
3. **sqlite-vec（向量加速）**：与 FTS5 **无关**。若 `sqlite-vec` 扩展 **缺失或加载失败**，OpenClaw **记录错误** 并 **回退到进程内余弦相似度**（仍可搜，大数据量时可能更慢）。可选配置 **`store.vector.extensionPath`** 指向本机 `vec0` 动态库（见 [Memory · sqlite-vec](https://docs.openclaw.ai/concepts/memory)））。

### 8.2 若仍希望「BM25 + 向量」完整混合、且不想改 Node 的 SQLite

- **可选后端**：在配置中启用 **`memory.backend: "qmd"`**，由 **QMD 侧车** 在 **独立进程 + 自带 SQLite/工具链** 中做混合检索（OpenClaw 文档要求本机有可加载扩展的 SQLite 等）；失败时 **自动回退 builtin**（见 [Memory · QMD](https://docs.openclaw.ai/concepts/memory)）。

### 8.3 LCM（lossless-claw）与 FTS5（另一套库）

若 Gateway 日志中出现 **`FTS5 unavailable`** 类提示，可能涉及 **两套库**：

- **LCM（`~/.openclaw/lcm.db`）**：若 Node 内嵌 SQLite **无 FTS5**，**`lcm_grep`** 的全文检索可能退化为 **LIKE**（以 [lossless-claw FTS5 说明](https://github.com/Martian-Engineering/lossless-claw/blob/main/docs/fts5.md) 为准）。
- **builtin memory-search（`~/.openclaw/memory/{agentId}.sqlite`）**：**`openclaw memory status`** 里 **FTS: unavailable** 表示 **builtin 索引** 无法建 **FTS5 虚拟表**；处理方式见 **8.1**。

二者 **不是同一张表、同一进程里的同一扩展**，互不替代。

### 8.4 仍需要完整 FTS5 时（进阶）

**先检测当前 Node 是否支持 FTS5**：

```bash
node -e "
try {
  const { DatabaseSync } = require('node:sqlite');
  const db = new DatabaseSync(':memory:');
  db.exec('CREATE VIRTUAL TABLE test USING fts5(text)');
  console.log('✅ 当前 Node 的 SQLite 支持 FTS5');
} catch (e) {
  console.log('❌ 当前 Node 不支持 FTS5');
  console.log(e.message);
}
"
```

- **builtin / LCM 笔记与会话数据量不大、可接受无 FTS 的降级行为**：可继续用官方降级路径（**8.1**），或接受 LCM 侧 **LIKE**。
- **必须从 Node 层启用 FTS5**：需 **自行编译带 `SQLITE_ENABLE_FTS5` 的 Node**，或按 [lossless-claw：FTS5 说明](https://github.com/Martian-Engineering/lossless-claw/blob/main/docs/fts5.md) 与当前 Node 版本对齐分支（维护成本较高）。

实验性路线图（**非当前默认产品路径**）见 [Research · memory](https://docs.openclaw.ai/experiments/research/memory)（例如工作区内派生索引、FTS5 + 可选嵌入等设想）。

---

## 九、不建议默认开启的一项

**`memorySearch.experimental.sessionMemory`** 会把 **会话 transcript** 也纳入 `memory_search` 的索引，与 LCM 在「对话回忆」上 **功能重叠**，并增加 embedding 与存储成本。以 LCM 为主时，建议 **保持默认关闭**，除非你明确要让 **`memory_search` 统一搜「笔记 + 历史会话」**。

---

## 小结

**本文落地选型**：**lossless-claw（会话层）+ memory builtin（笔记层）+ `memorySearch`（远程嵌入与 Hybrid；FTS 缺失时见第八节）**，**不以 QMD 为主路径**。

在此前提下完成 **Session/compaction 配套** 后，预期效果是：**会话内容**在 LCM 中可持久化、可压缩与按需深度召回；**长期笔记**以 Markdown 为事实来源，**builtin** 下以 **向量为主**、在 **FTS5 可用时** 叠加 **BM25**；若日后启用 **QMD**，侧车失败时仍 **回退 builtin**。OpenClaw **内置 compaction** 与 LCM **不抢主流程**（`safeguard` 兜底）。具体仍以你本机 OpenClaw 版本与 [Memory](https://docs.openclaw.ai/concepts/memory) 为准。

---

## 璞奇启示

**第一，分层与分工。** 学习也是如此：「课堂对话」与「课后笔记」若混成一条流水，既难检索也难沉淀。工具链里把 **会话层（LCM）** 与 **知识层（MEMORY.md + hybrid 检索）** 分开，等价于把 **过程** 与 **结论** 放在不同抽屉，取用时才清晰。

**第二，语义与关键词互补。** 练习与复习既需要 **理解迁移**（像向量），也需要 **精确召回**（像 BM25）。Hybrid 在笔记场景的价值，对应到学习产品就是：**既抓大意，也抓易错点与术语**。

---

## 信息说明

- OpenClaw Memory（含 **QMD 后端**、向量检索、Hybrid、FTS5 降级、sqlite-vec）：<https://docs.openclaw.ai/concepts/memory>
- OpenClaw 实验性记忆研究（派生索引、SuCo 等，**非默认产品路径**）：<https://docs.openclaw.ai/experiments/research/memory>
- OpenClaw Memory 配置参考：<https://docs.openclaw.ai/reference/memory-config>（含 `store.vector` / sqlite-vec）
- OpenClaw `openclaw memory` CLI：<https://docs.openclaw.ai/cli/memory>
- OpenClaw Memory Search 概念：<https://docs.openclaw.ai/concepts/memory-search>
- lossless-claw 仓库：<https://github.com/Martian-Engineering/lossless-claw>（配置见 <https://github.com/Martian-Engineering/lossless-claw/blob/main/docs/configuration.md>）
- lossless-claw FTS5：<https://github.com/Martian-Engineering/lossless-claw/blob/main/docs/fts5.md>
- 硅基流动 Embeddings API：<https://docs.siliconflow.cn/cn/api-reference/embeddings/create-embeddings>
