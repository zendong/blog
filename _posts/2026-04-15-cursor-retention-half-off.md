---
title: "差点退订 Cursor: 别走啊，对折卖"
date: 2026-04-15
categories:
  - 随笔
tags:
  - cursor
  - stripe
  - subscription
  - indie-hacker
  - 璞奇 app
layout: post
hero_image_ai_generated: true
image_prompt: "Editorial blog hero, 16:9, indie developer at laptop in dim office with cyan-purple screen glow, floating glowing 50% coupon ribbon beside them, vector-infused digital painting, warm rim light, dark teal background, no logos or fake UI text"
image_prompt_file: "assets/prompt/2026-04-15/2026-04-15-cursor-retention-half-off.txt"
---

> "祸兮福之所倚，福兮祸之所伏。" — 《道德经》

![题图，开发者工位与半价挽留意象](/assets/images/2026/2026-04-15-cursor-retention-half-off.png)

下面这件小事，算《道德经》里那句的当代注脚，祸福在同一天里换了个边。

月初我订了 Cursor 按月两百美元上下的那一档，心里肉疼。横向比过海外大模型和编码 Agent，还是决定先试一个月，要的是模型入口多、线路少操心，璞奇 App 迭代也别被工具拖住。

白天写代码时我走了科学上网。那天 Models 里高配一度刷不出来，新建 Agent 里只剩 Composer 2、Kimi 2.5 这类偏通用的选项。事写到一半卡住，我火气上来，第一反应是去 Stripe 关掉下月自动续费，再换别家。

我顺着账单链路找到 Stripe 的取消入口，准备关订阅。

![Stripe 取消订阅流程里的操作入口](/assets/images/2026/2026-04-15-cursor-retention-half-off-stripe-cancel.png)

![结账流程里出现的下月半价挽留提示](/assets/images/2026/2026-04-15-cursor-retention-half-off-offer.png)

页面弹了一屏挽留，大意是下个月直接半价，而且随时还能再取消。那种语气，很像收银台边有人拽你袖子说一句，别走啊，对折卖。我盯着看了几秒，觉得至少这一个月里工具对我还算刚需，半价又确实削掉一大块成本，就先留下了。

后来我是靠**已经开着的、还在用高配模型的旧 Agent 会话**接着写，没硬等新对话里列表恢复。到晚上 Models 又正常刷出来了，回头看更像是当时服务端或网络侧的一阵抖动，不像是产品故意锁功能。但这一趟折腾下来，账单上相当于少掏了大约一百美元，算意外捡回来的。

我无意把一次个人经历推广成「你去取消就一定能薅到羊毛」。各家 SaaS 的挽留策略、你账号所在区、支付渠道都不一样，能不能弹出同类 offer 没有通用答案。我更有感触的是另一件事，拉新已经很难，真到「人要走了」那一步，产品上愿意让出利润来换多留一个月，说明续费这条线的压力是实打实的。我作为小团队负责人，自己也天天算现金流和工具账，对这种算计不反感，反而觉得透明。

工具还会换，账还会算。今天这条就记一笔，给以后的自己看当时为什么没退。

> **璞奇启示**
>
> 1. 学习或做项目时，遇到「环境一变就失灵」的阻塞，先区分是配置问题还是服务波动，能复用存量会话或缓存进度时，往往比干等列表恢复更省时间。
> 2. 把关键操作（续费、导出、备份）走通一遍并记下来，和璞奇里用练习巩固流程一样，真遇事时少慌一步，就多一分把精力留在正题上的余地。
