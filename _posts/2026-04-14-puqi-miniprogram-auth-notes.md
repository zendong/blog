---
title: "璞奇微信小程序登录侧手记，手机号与 unionId"
date: 2026-04-14
categories:
  - 技术
tags:
  - wechat-miniprogram
  - miniprogram
  - puqi
  - auth
  - 璞奇 app
layout: post
hero_image_ai_generated: true
image_prompt: "Editorial hero illustration for WeChat mini program login and phone verification tradeoffs, minimal flat vector, soft blue and green on light gray, phone frame key branching path lock shield, no text no logos, 16:9"
image_prompt_file: "assets/prompt/2026-04-14/2026-04-14-puqi-miniprogram-auth-notes.txt"
---

> "合于利而动，不合于利而止。" — 《孙子兵法》

![首图](/assets/images/2026/2026-04-14-puqi-miniprogram-auth-notes.png)

最近在补**璞奇**的微信小程序版本，登录这条链路和 App 端还不完全一样，顺手记两条决策和踩坑，给以后自己查。

## 手机号从哪里来

小程序里要不要用微信提供的「一键拿手机号」，和 App 里「用户自己填号再走短信验证」是两条路。我们要手机号，一是合规场景里该留的联系方式得留，二是尽量**少绑第三方**，核心账号字段握在自己短信链路里，心里踏实一点。

App 这边早就定型了，微信登录后发现没绑手机，就进自研页面，输入号码、收验证码、写库，全程我们自己的接口。

小程序多一个选项，开放平台里有**手机号快速验证**一类能力，用户点一次授权，后端拿密文再解密。听起来省事，但和「完全自研采集」对起来，表里每一项都要算账。

| 项 | 微信授权手机号 | 用户手动输入手机号 |
| --- | --- | --- |
| 费用 | 按官方规则，成功调用计费（常见为约 0.03 元/次，以微信后台与文档为准） | 仅短信成本，无按次授权费 |
| 主体要求 | 需企业认证等条件，以平台为准 | 个人或企业均可走通自研链路 |
| 用户步骤 | 一步授权 | 输入、验证码、确认，约三步 |
| 可靠性 | 依赖微信接口与解密链路 | 短信与校验逻辑自控 |
| 安全性 | 微信侧背书 | 自研验证码流程可控 |
| 开发量 | 解密、异常与重试要铺全 | 与 App 对齐则后端可复用 |
| 是否等于「微信绑定手机号」 | 是授权读号 | 否，用户可填任意可达号码 |
| 是否受微信产品策略影响 | 是 | 否 |

几轮对齐之后，小程序侧还是改成了**和 App 同一套自研采集**。这样后端入库、校验、换绑规则不用维护两套语义，运维和客服也少一种「为什么小程序和 App 不一致」的解释成本。计费那一列不是不能用授权，而是对我们当前体量与目标来说，**对齐比单次省几步点击更划算**。

下面是当时梳理的登录流程截图，留给以后改需求时对图说话。

![小程序登录流程](/assets/images/2026/2026-04-14-puqi-miniprogram-auth-notes-flow.png)

## unionId 可能第一次拿不到

另一条坑是 **unionId**（同一微信开放平台下，同一用户在不同应用里的统一标识）。实践里**第一次**进小程序，有时 `jscode2session` 就是不带 unionId，不是你自己写错了字段名那么简单。

我们这边补了两步，都是「有可能才行」的前置条件，真机仍以微信返回为准。

1. 在**微信开放平台**把小程序和同一开发者体系下的应用绑定好，否则谈不上 unionId 这条线。
2. 若仍拿不到 unionId，再走一轮用户资料授权（例如通过 `wx.getUserProfile` 拉昵称头像），授权后再用 `code` 去换 `session`，有的环境下 unionId 会跟着回来。接口形态会随微信版本调整，集成时以**当时**官方文档与调试器为准。

初版能稳定走完登录，页面上大概是下面这样。

![初版登录页面](/assets/images/2026/2026-04-14-puqi-miniprogram-auth-notes-login.png)

---

小程序和 App 并行维护，最怕的是「看起来都能登录，字段含义却悄悄分叉」。能复用的逻辑尽量保证统一，以提高鲁棒性，降低理解成本。

