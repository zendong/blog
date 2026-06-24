---
title: "LLM Tool Call乱吐JSON的有限终极解法"
date: 2026-06-22
categories:
  - 技术
tags:
  - llm
  - tool-call
  - json-schema
  - json-repair
  - pracmo
layout: post
hero_image_ai_generated: true
image_prompt: 'Create a horizontal WeChat article cover illustration for a Pracmo technical blog article about LLM tool calls returning malformed JSON and a four-layer defense: prompt-level schema hints, strict schema properties, JSON repair, and LLM fallback. Include Puki, the Pracmo pangolin learning companion, based on the Puki three-view reference: cream white face and belly, deep royal blue body, teal scarf with gold trim, round jade ornament, layered teal/yellow/coral/red/blue pangolin scales. Visual objects: broken JSON cards, four clean gates labeled Prompt, Strict, Repair, Fallback, a small DingTalk alert card, pangolin scale path motifs. Fresh bright product editorial style, warm cream, sky blue, mint, aqua green, warm yellow, small coral accents, horizontal 16:9. No logo, no watermark, no long text.'
image_prompt_file: "assets/prompt/2026-06-22/2026-06-22-tool-call-json-safety.txt"
---

> LLM 的 tool call 偶尔吐出坏 JSON 时，工程系统到底该信它，修它，还是报警？

![Tool Call 四层兜底流程](/assets/images/2026/2026-06-22-tool-call-json-safety.png)

这两天修了一个很典型的 LLM 工程问题：AI 在对话里调用内部工具，准备帮用户生成练习或甲程，但 `tool_call.function.arguments` 偶尔不是我们期待的那个干净 JSON。

有时是字符串里夹了没转义好的引号，比如用户需求里出现 `"招式-经络"`；有时模型给参数外面多包了一层 `raw`；还有时结构看起来差不多，但某个字段的类型、枚举、必填约束没有完全对上。

如果这一步失败，用户看到的是“怎么刚才还聊得好好的，突然创建失败了”。工程上看，就是把不确定的自然语言输出，直接接进了确定的业务入口。

在界面上看到的效果是这样：
![Tool Call 参数解析失败截图](/assets/images/2026/2026-06-22-tool-call-json-safety-screenshot-error.png)

之前也遇到过几次，都只是针对性的修补一下。这次发生在我跟新用户当面介绍的时候，那尴尬啊，无处躲藏。

于是痛下决心，决定根治这大模型不听使唤的顽疾。

前后累计建了四道门。作为 API 调用方，影响 LLM 输出的手段不多，后端也加上了告警，这套解法对于我们来说算是终极解决方案了。

## 第一扇门：先在 Schema 说明里劝一劝

最前面先做的是最朴素的办法：加强 tool schema 里的说明。

比如在 `userRequest` 这类容易混入自然语言的字段里，明确提示模型不要生成未转义的 `"`，尽量避免让用户输入里的引号把 JSON 字符串冲开。

![Tool Schema 字段说明截图](/assets/images/2026/2026-06-22-tool-call-json-safety-screenshot-schema.png)

这一步有用，但效果不大。

原因也很简单：提示词说明其实还是“劝”。模型大多数时候会听，但只要用户内容复杂一点、字段很长一点，或者中间有中文引号、英文引号、转义符混在一起，它还是可能把字符串边界搞乱。

所以第一道门只能降低概率，不能当成边界。

## 第二扇门：用 Schema 属性真正收口

第二步才是把约束写进结构本身。

每个参数声明 `type`，必填字段放进 `required`，枚举字段显式写 `enum`，每个 object 层级都设置 `additionalProperties: false`。对 OpenAI 及兼容厂商，还打开 `strict: true`。

这一步的目标不是“让模型更听话”这么抽象，而是让模型少走岔路。

一个工具如果只说“传一个对象过来”，模型就会自由发挥；如果 schema 明确到对象层级、字段类型和枚举空间，它就更像在填表。表格越清楚，后端越少做猜谜游戏。

OpenAI 的 [Structured Outputs 文档](https://platform.openai.com/docs/guides/structured-outputs)也把 function calling 和结构化输出放在同一类约束思路里：能用 schema 收紧，就不要只靠提示词维持秩序。

这里还有一个现实限制：不是所有兼容厂商都完整支持 `strict` 或完全按 OpenAI 的方式解释 schema 属性。支持的厂商尽量打开，不支持的厂商就退化成更强的结构提示和后续兜底。

## 第三扇门：json-repair 做急救

Schema 能减少问题，但挡不住所有问题。

真实世界里，坏 JSON 常常只差一口气：多一个逗号，少一个转义，字符串边界被用户输入冲开了。为了不让这种小伤直接变成创建失败，我们在解析前引入 `json-repair`。

它负责处理常见 JSON 损坏，比如：

```text
原始 tool arguments
  -> 直接 JSON parse
  -> 失败后进入 json repair
  -> repair 后再 parse
```

这里要克制。`json-repair` 不是业务语义修复器，它只修格式，不猜“用户到底想创建几个练习”。所以它适合放在结构解析前，不能替代后面的字段校验。

我们还保留了 `raw` 这类兼容逻辑：如果模型把真实参数包进 `{"raw": {...}}`，解析层会尽量把它剥出来，再交给具体工具做正常校验。

## 第四扇门：让 LLM 救一下 LLM

如果 repair 后仍然失败，就进入最后兜底：用 lowcost 模型再解析一次。

这个兜底不是让模型“继续创作”，而是给它一个非常明确的清洗任务：

1. 这是原始工具调用内容。
2. 这是解析错误。
3. 这是目标 JSON 示例。
4. 只返回符合 schema 的 JSON。

它像一个便宜的格式整理员，只在前三道门都失败时上场。成功了，用户流程还能继续；失败了，也不再静默吞掉问题。

更重要的是，这个能力被做成每类内部 tool 必须实现的兜底方法。创建练习有自己的恢复方式，创建甲程也有自己的恢复方式。通用层负责“何时触发兜底”，具体 tool 负责“怎样把坏输入提炼成自己的合法参数”。

每一类新定义的 tool 给出预期的 JSON 示例，整合如下的处理逻辑，拼接后的提示词对接 LLM 时，配上 `response_format` 参数为 `{"type": "json_object"}`，这样有要求、有示例、有格式约束，进一步提升救回来的可能性。

![LLM 兜底提示词与 JSON 示例截图](/assets/images/2026/2026-06-22-tool-call-json-safety-screenshot-fallback.png)

这也避免了一个常见坏味道：在公共解析层越堆越多业务特判，最后变成一锅谁也不敢动的兼容逻辑。

## 告警要比用户先看见

最后补的是钉钉告警。

只要 AI 生成练习或甲程时再次发生转换错误，就把转换报错、原始 tool call、repair 结果、LLM 兜底是否触发、兜底是否成功都发出来。

如果触发了 LLM 兜底，也发告警，不管它最后有没有救回来。

原因很简单：兜底是为了用户体验，不是为了掩盖系统问题。只要这条路径开始变热，就说明 schema、prompt 或模型适配里还有东西需要继续收紧。

## 最后的形态

现在这条链路大概是这样：

```text
schema 提示词限制
  -> strict/schema 属性约束
  -> 本地 JSON 解析
  -> json-repair
  -> raw 兼容
  -> tool 自己的 lowcost LLM 兜底
  -> 钉钉告警
```

它不是一次性相信模型，而是把信任拆成几层。

第一层先劝模型别犯错。第二层用厂商支持的 schema 能力收口。第三层修复低级格式错。第四层让便宜模型做受限提取。最后用告警确保所有异常都有回声。

这类问题的有趣之处在于，表面看是 JSON 转换异常，根上其实是“概率输出如何进入确定系统”。解决它也不是一句“加强 prompt”就够了，而是要把不确定性关进一条有护栏、有急救、有报警的通道里。

> **璞奇启示**
>
> 1. AI 产品里，最危险的不是模型偶尔犯错，而是工程系统假装它永远不会犯错。练习和甲程是用户的学习资产，创建链路就不能只靠「模型应该会按格式返回」。
> 2. 更好的做法是前面强约束，中间可修复，后面可兜底，异常可追踪。不要和模型讲道理，给它铺轨道。
