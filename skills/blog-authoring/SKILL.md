---
name: blog-authoring
description: >-
  一站式博客文章创作助手：根据用户提供的核心话题，自动生成带 Jekyll front matter 的 Markdown 文章、
  AI 配图及提示词、社交标签。专注于记录创业经历、技术探索与产品思考。
  优先使用 Cursor GenerateImage 工具生成图片（如果在 Cursor 环境中），否则使用 MiniMax API。
  适用于 GitHub Pages / Jekyll 博客 workflow。
---

# 博客文章创作助手

## 何时启用

当用户想要：
- 撰写一篇关于创业经历、产品设计、技术探索的文章
- 为文章生成配图和提示词
- 创建符合 Jekyll 格式的 Markdown 文件
- 自动保存图片到博客仓库的指定目录

## 工作流程

### 阶段 1：理解需求与规划

1. **确认话题**：用 1-2 句话复述用户意图，确认无敏感/侵权内容
2. **确定风格**：
   - 技术文章：轻松有节奏，可适当引经据经典（诗词、成语）
   - 结构：标题 → 导语（钩子）→ 2-4 个小节 → 小结/开放问题
3. **时效性检查**：若涉及时事/版本发布，先联网检索核对事实
4. **事实核查（必须执行）**：涉及外部信息的内容（如 GitHub 仓库地址、产品链接、数据等），必须联网验证正确性后才可写入文章。如果找不到准确信息，宁可删除该内容也不要填写错误信息

### 阶段 2：生成文章内容

#### 2.1 编写 Jekyll Front Matter

参考格式：

```yaml
---
title: "文章标题"
date: YYYY-MM-DD
categories:
  - 创业  # 或：技术、随笔、行业观察
tags:
  - tag1
  - tag2
  - tag3
  - tag4
layout: post
image_prompt: "英文提示词内容"
image_prompt_file: "assets/prompt/YYYY-MM-DD/YYYY-MM-DD-{slug}.txt"
---
```

**标签选择原则**：
- 2-5 个标签，小写连字符格式
- 包含技术关键词（如 `agent`, `skill`）
- 包含场景关键词（如 `ios`, `web`, `product-design`）
- 可适当加入产品名（如 `璞奇app`）

#### 2.2 撰写正文

- **文风**：平实、直接，避免矫情或过度修饰的词汇。技术文保留步骤与结论。
- **导语**：引用名言或提出钩子问题。
  - 引用必须注明出处（人名或作品名称）
  - 优先使用中文名言，除非其他语言更切合文章表达
  - 引用格式：`> "引文内容" — 出处`
- **避免词汇**：
  - 不要用"辗转反侧"、"捶胸顿足"、"呕心沥血"等夸张表达
  - 不要用"里程碑式"、"颠覆性"、"划时代"等过度修饰
  - 问题就是问题，不需要强调其"严重性"或"艰巨性"
- **配图**：文章中仅包含首图（导语下方），使用绝对 URL 格式：
  ```markdown
  ![首图](https://blog.zendong.com.cn/assets/images/YYYY/YYYY-MM-DD-{slug}.png)
  ```

**名言引用流程**（去重保障机制）：

**核心原则**：选择最契合文章的引用，quotes.yml 仅用于追踪和去重，不限制引用来源。

1. **选择最契合的引用**：
   - 根据文章主题、情感基调和思想内核，选择**最贴切**的引用
   - 不限于数据库中的来源，可以是任何经典、名人语录、网络金句等
   - 优先选择相对冷门但契合度高的引用，避免烂大街的"名人名言"
   - 每篇文章**仅使用一个引用**作为导语

2. **去重检查**：
   在确定引用后，查询 `_data/quotes.yml`：
   - 如果该引用（或高度相似的引用）在 `last_used` 距今**不足30天**，则**换一篇引用**
   - 如果30天内有相同来源的引用，优先换用其他来源
   - 核心是避免读者在不同文章中看到重复的引用

3. **记录已用引用**（必须立即执行）：
   确定最终引用后，**立即**更新 `_data/quotes.yml`：
   - 如果是数据库中已存在的引用（by id）：更新 `used_count + 1`，`last_used` 改为今天
   - 如果是**新引用**（数据库中不存在）：在对应类别下新增一条记录，设置 `used_count: 1`，`last_used: 今天`

4. **插入文章**：
   使用格式 `> "引文内容" — 出处`

**名言引用建议来源**：
- 中国古典：《论语》《道德经》《庄子》《孟子》《礼记》等
- 西方哲学：苏格拉底、柏拉图、亚里士多德、尼采、康德等
- 科学思想：爱因斯坦、费曼、香农等
- 现代文学：卡夫卡、村上春树、余华、王小波等
- 技术/商业：圣西门、德鲁克、彼得·蒂尔等

#### 2.3 璞奇 APP 启示（必选）

每篇文章必须包含一个**「璞奇启示」**小节，将文章主题与璞奇 APP 的产品理念关联：

**璞奇 APP 定位**：一款通过 AI 为用户学习内容提效的工具，AI 为用户感兴趣的内容生成相关的练习内容，用丰富的练习方式来帮助用户掌握知识，达成目标。

**写作要点**：
- 从文章主题中提取 1-2 个可迁移到学习场景的洞察
- 思考：这个技术/趋势/方法如何帮助用户更好地学习？
- 举例：
  - 技术文章 → AI 如何辅助理解复杂概念
  - 创业故事 → 学习路径设计的启发
  - 产品思考 → 练习形式创新

**示例结构**：
```markdown
## 璞奇启示

词元对学习类产品的启示...

**第一，[洞察1]**
[具体阐述]

**第二，[洞察2]**
[具体阐述]
```

### 阶段 3：生成配图提示词

#### 3.1 提炼视觉主题

从文章中提取 **1个** 适合视觉化的核心场景/隐喻作为首图：

**首图（1张）**：
- 位于导语下方
- 呼应文章主题核心场景/事件
- 编写英文提示词

**提示词结构**：
```
主体描述 + 光线/色彩 + 风格/氛围 + 构图/视角
```

**示例**：
```
A futuristic vision of humanity's transition to interstellar civilization:
a massive orbital solar array surrounding a glowing star like a partial Dyson sphere,
with sleek spacecraft and AI satellites swarming around it,
Earth visible in the distant background, cosmic dust and nebula atmosphere,
cinematic photorealistic rendering with dramatic lighting, 16:9 aspect ratio,
epic sci-fi concept art depicting the Kardashev Type II civilization milestone
```

#### 3.2 保存提示词文件

创建目录和文件：
- 目录：`assets/prompt/YYYY-MM-DD/`
- 文件：`YYYY-MM-DD-{slug}.txt`

文件内容格式（单个提示词）：
```
# 文章标题：{title}
# 生成日期：{date}
# 图片用途：文章首图

{英文提示词}
```

### 阶段 4：生成图片

**重要**：图片生成是必须步骤，不可跳过。如果图片生成失败（包括 API Key 缺失、环境问题等），需要记录错误但**不要中断流程**，继续完成文章其余部分，并在最终交付时告知用户图片未生成。

#### 4.1 检测当前环境

判断是否在 Cursor 环境中：
- 如果能调用 `GenerateImage` 工具 → 使用 Cursor 生成（优先）
- 否则 → 使用 MiniMax API（需要 venv 虚拟环境）

#### 4.2 生成图片

**第一步：生成首图**
- 文件名：`YYYY-MM-DD-{slug}.png`（**必须与文章文件名匹配，不带 -hero 后缀**）
- 生成后保存到 `assets/images/YYYY/`

**第二步：压缩图片**
```bash
cd tools/image-generator-minimax
venv/bin/python compress_image.py ../../assets/images/YYYY/YYYY-MM-DD-{slug}.png
```

#### 4.3 MiniMax API 使用方式

```bash
# 激活虚拟环境
source venv/bin/activate  # macOS/Linux

cd tools/image-generator-minimax

# 生成首图
python minimax_image_generator.py \
  --prompts ../../assets/prompt/YYYY-MM-DD/{slug}.txt \
  --output ../../assets/images/YYYY \
  --force

# 压缩
python compress_image.py ../../assets/images/YYYY/YYYY-MM-DD-{slug}.png

# 退出虚拟环境
deactivate
```

#### 4.4 图片嵌入流程

**直接使用 URL 格式**，无需 base64 转换：

```markdown
![首图](https://blog.zendong.com.cn/assets/images/YYYY/YYYY-MM-DD-{slug}.png)
```

**重要**：图片标签 `![首图](...)` 必须写入文章正文中（导语下方），而不仅仅是 front matter 中声明。两者缺一不可。

#### 4.5 命名约定

- 文章文件：`YYYY-MM-DD-{slug}.md`
- 首图：`YYYY-MM-DD-{slug}.png`（持久化保存到 `assets/images/YYYY/`）
- 提示词文件：`YYYY-MM-DD-{slug}.txt`

### 阶段 5：自审文章内容

在完善元信息之前，必须对文章进行自审，确保内容完整、逻辑正确、信息准确。

**自审清单**：

1. **逻辑完整性**：
   - 文章结构是否清晰（导语 → 正文 → 璞奇启示 → 小结）
   - 段落之间是否有合理的过渡
   - 结论是否与前文呼应

2. **内容一致性**：
   - 如果列出 N 个要点/原因/启示，实际段落数量是否匹配
   - 小标题的数量是否与内容对应
   - 表格行数是否与描述一致

3. **信息准确性**：
   - 引用名言是否标注了正确出处
   - **外部链接（GitHub地址、产品链接等）必须联网验证正确性**
   - 数据、日期、版本号是否准确
   - **如果无法确认事实，该信息必须删除，不可猜测填写**

4. **格式规范性**：
   - Front matter 是否完整（title/date/categories/tags/layout/image_prompt/image_prompt_file）
   - YAML 语法是否正确（注意中文引号可能导致解析错误）
   - **图片 URL 必须使用绝对地址 `https://blog.zendong.com.cn/...`，禁止使用 `{{ "..." | relative_url }}` filter**
   - 无多余空格或格式问题

5. **璞奇启示检查**：
   - 是否包含「璞奇启示」小节
   - 是否关联到璞奇 APP 的产品理念
   - 洞察是否从文章主题自然迁移

**自审执行方式**：
- 通读全文，检查上述要点
- 如发现问题，直接修改文章内容
- 自审通过后，再进入阶段 6

### 阶段 6：完善文章元信息

文章末尾不需要额外添加配图清单（已在 front matter 中声明），只需添加信息说明：

```markdown
---

## 信息说明

- [如有引用外部信息，列出来源链接]
```

## 完整交付物

### 1. Markdown 文章文件

路径：`_posts/YYYY-MM-DD-{slug}.md`

内容结构：
```markdown
---
title: "..."
date: YYYY-MM-DD
categories:
  - ...
tags:
  - ...
layout: post
image_prompt: "..."
image_prompt_file: "assets/prompt/YYYY-MM-DD/YYYY-MM-DD-{slug}.txt"
---

> 导语引用或钩子

![首图](https://blog.zendong.com.cn/assets/images/YYYY/YYYY-MM-DD-{slug}.png)

## 正文...

## 璞奇启示

...

---

## 信息说明
...
```

### 2. 提示词文件

路径：`assets/prompt/YYYY-MM-DD/YYYY-MM-DD-{slug}.txt`

### 3. 图片文件（持久化保存）

- 首图：`assets/images/YYYY/YYYY-MM-DD-{slug}.png`

## 质量检查清单

- [ ] Front matter 格式正确，包含 title/date/categories/tags/layout/image_prompt/image_prompt_file
- [ ] 文章图片使用**绝对 URL**（`https://blog.zendong.com.cn/...`），**禁止使用 `{{ "..." | relative_url }}`**
- [ ] 文章图片使用 URL 格式（非 base64）
- [ ] 包含「璞奇启示」小节，关联璞奇 APP 产品理念
- [ ] 提示词文件已保存到 `assets/prompt/` 目录
- [ ] 图片文件已保存到 `assets/images/` 目录
- [ ] 图片已成功生成（Cursor GenerateImage 优先，或 MiniMax API）
- [ ] 文章自审通过（逻辑完整、内容一致、信息准确）
- [ ] **外部链接（GitHub地址、产品链接等）已联网验证正确性**
- [ ] 涉及时事的内容已标注信息截止时间
- [ ] **无法确认的事实信息已删除，不可猜测填写**

### 阶段 7：构建与交付

#### 7.1 运行构建验证

在博客根目录执行 `make build` 确保没有异常：

```bash
make build
```

**成功标准**：
- 构建命令返回码为 0
- 无 Error 级别日志输出

**失败处理**：
- 如果构建失败，检查 `_posts/` 目录下的 Markdown 文件格式是否正确
- 常见的 front matter 格式错误（如引号不匹配、缺少冒号）
- 修复后重新运行 `make build` 直至通过
- **如果构建失败，不执行 Git 提交，直接退出本阶段**

#### 7.2 Git 提交与推送

**前置条件**：构建必须成功（返回码为 0）。如果构建失败，**跳过本步骤，直接报告错误**。

构建成功后，执行 Git 提交流程：

**步骤 1：查看变更状态**
```bash
git status
```

**步骤 2：添加文件**
```bash
git add _posts/YYYY-MM-DD-{slug}.md \
       assets/images/YYYY/YYYY-MM-DD-{slug}.png \
       assets/prompt/YYYY-MM-DD/YYYY-MM-DD-{slug}.txt
```

**步骤 3：创建提交**
```bash
git commit -m "$(cat <<'EOF'
Add: 新文章标题

- 新增 Markdown 文章
- 添加配图和提示词文件

Co-Authored-By AI
EOF
)"
```

**步骤 4：推送到远程**
```bash
git push origin main
```

**错误处理**：如果 Git 操作（add/commit/push）任何一步出错，**不要重试，不要 partial commit**，直接报告错误并退出。

#### 7.3 交付确认

推送成功后，向用户确认：
- 文章已成功创建并推送到 GitHub
- 包含文章、配图（如已生成）、提示词文件
- GitHub Actions 将自动构建并部署到 GitHub Pages

**如果图片未生成**：明确告知用户需要在 `tools/image-generator-minimax` 配置 `MINIMAX_API_KEY` 环境变量后手动运行生成脚本。

## 示例参考

参考文章：`@_posts/2026-03-23-tesla-terafab-interstellar-civilization.md`

该示例展示了：
- 完整的 Jekyll front matter（含 image_prompt 和 image_prompt_file）
- 引用经典作为导语
- 技术文章的结构化写作
- 「创业视角」小节的写作方式（可作为「璞奇启示」的参考）
- 文末信息说明
