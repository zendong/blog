---
title: "璞奇 Chrome 插件上架手记，标准入口和本地安装都要有"
date: 2026-06-11
categories:
  - 技术
  - 产品
tags:
  - pracmo
  - chrome-extension
  - chrome-web-store
  - product
layout: post
hero_image_ai_generated: true
image_prompt: "Horizontal product-editorial illustration for a Pracmo Chrome extension article: Puki the pangolin learning companion with a review checklist and puzzle-piece backpack, a simplified browser window, zip package, web learning cards flowing into a practice path, fresh cream, sky blue, mint, warm yellow and coral colors, no text or watermark."
image_prompt_file: "assets/prompt/2026-06-11/2026-06-11-pracmo-chrome-extension-store-submit.txt"
---

> 一个学习工具，如果只待在 App 里，就会错过很多真正发生学习的地方。

![首图](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit.png)

这两天在推进璞奇 Chrome 插件版的上架。

事情不算大，但我觉得值得记一笔。

璞奇的定位一直是全场景的兴趣练习助手。用户在哪里看到内容，最好就能在哪里把内容收进来，后面再生成练习、复盘、追问。App 端已经覆盖了一部分场景，但网页端有个天然优势，很多内容本来就发生在浏览器里。

比如得到、极客时间、各种公开网页、文档页、长文章。

你在电脑上读到一段内容，觉得值得练一下，这时候让用户复制、传到手机、再打开 App，其实已经多绕了好几圈。Chrome 插件这个形态的价值就在这里，它可以贴着网页工作，把「看到内容」和「整理成练习」之间那段距离缩短。

![网页学习内容示例](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-01-web-learning.png)

![璞奇 Chrome 插件面板](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-02-extension-panel.png)

坦率的讲，这不是一个多华丽的产品动作。

它更像是把入口补齐。

## 先把官方入口走起来

Chrome 插件要走标准渠道，绕不开 Chrome Web Store。

国内访问 Google 服务确实不算顺手，但官方入口还是要维护起来。一个工具如果要长期给用户使用，最好不要只有一种安装方式。官方商店是标准入口，本地 zip 是备用入口，两条路都在，用户选择会更稳。

这次先把基础信息、隐私说明、截图和发布配置录进去。

![Chrome Web Store 提交入口](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-03-store-submit.png)

![插件信息录入](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-04-store-info.png)

![隐私相关信息](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-05-privacy.png)

提交时弹了一个提示。

![Chrome Web Store 审核提示](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-06-review-warning.png)

我看了一下，核心原因大概率是权限范围。

璞奇插件在 `manifest.json` 里申请了比较宽的 host permissions，也就是接近全站可访问的能力。Chrome 官方文档里对 [host permissions](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions) 的解释很直接，它允许扩展和匹配 URL 的页面交互。Chrome Web Store 的 [review process](https://developer.chrome.com/docs/webstore/review-process) 也明确提到，申请 broad host permissions 或敏感执行权限的扩展，审核时间可能更长。

这个事儿挺典型。

从功能角度看，璞奇插件想覆盖网页学习内容，权限范围宽一点有现实理由。你不知道用户下一次会在哪个网页学习，也不知道材料来自哪个站。可从平台审核角度看，权限宽就天然要多问几句，因为它确实可能接触到更多页面内容。

我非常理解这个逻辑。

所以这次没有为了快速通过而把能力先拆残。先保留现有配置，接受深入审核，看官方反馈再决定下一步怎么收窄或解释。产品早期很多时候就是这样，不是每一步都优雅，但每一步都要把约束看清楚。

## 本地 zip 也要保留

另一条路是本地安装。

这条路不如商店安装优雅，但很实用。尤其在商店审核还没结束，或者用户所在网络访问不稳定时，本地 zip 至少能让真正想试的人先跑起来。

当前包地址放这里。

[https://download.zendong.com.cn/artifacts/pracmo-chrome-extension-current.zip](https://download.zendong.com.cn/artifacts/pracmo-chrome-extension-current.zip)

我刚核过，这个链接现在返回的是 zip 文件。

安装方式也和 Chrome 官方教程一致。Chrome 开发者文档在 [Hello World extension](https://developer.chrome.com/docs/extensions/get-started/tutorial/hello-world) 里写得很清楚，进入 `chrome://extensions`，打开 Developer mode，然后点 Load unpacked，选择扩展目录。

放到璞奇插件这里，大致就是四步。

第一步，下载 zip 包并解压。

![解压插件 zip 包](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-07-unzip.png)

第二步，在 Chrome 地址栏输入 `chrome://extensions`，打开开发者模式。

![打开 Chrome 扩展开发者模式](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-08-developer-mode.png)

第三步，点击「加载未打包的扩展程序」。

![加载未打包扩展](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-09-load-unpacked.png)

第四步，选择刚才解压出来的 `pracmo-chrome-extension-current` 目录。

![选择扩展目录](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-10-select-folder.png)

导入成功后，扩展列表里就能看到璞奇。

![插件导入成功](/assets/images/2026/2026-06-11-pracmo-chrome-extension-store-submit-11-loaded.png)

这条路径适合早期用户，也适合内部测试。

说真的，折腾半天还要手工加载扩展，看起来有点土。但很多产品的早期版本就是这样，先有一条能跑通的管道，再慢慢把它修成顺滑的路。

## 我更关心的是入口密度

这件事让我又想起一个老问题。

学习产品到底应该在哪出现？

如果只站在 App 视角，答案很容易变成，用户应该打开 App，然后开始学习。可真实世界不是这样。很多时候，学习是顺手发生的。看到一篇文章，听到一节课，刷到一个概念，正在查一个问题，突然觉得这个东西我应该练一练。

入口越贴近这个瞬间，产品越像一个助手。

Chrome 插件不是为了替代 App，而是补上桌面网页这个入口。网页里产生材料，插件负责收拢，App 继续承接练习和复盘。中间不需要把用户来回折腾。

这也是我为什么愿意把官方商店和本地 zip 都先弄起来。

一个是标准入口，一个是可用入口。

标准入口让产品更像一个长期工具，可用入口让早期反馈不要卡在审核和网络环境里。两者都不完美，但合在一起，至少把路铺出来了。

后面如果 Chrome Web Store 审核给出更明确意见，再回头调整权限说明、收窄匹配范围，或者做成更强的用户触发式授权。现在先把这一步记录下来。

小步推进，也算推进。

> **璞奇启示**
>
> 1. 学习材料经常不是在学习 App 里出生的，而是在网页、课程、文档和搜索过程中冒出来的。好的练习工具应该靠近材料出现的地方。
> 2. 产品入口有时要分成「标准入口」和「可用入口」。前者负责长期信任，后者负责早期反馈，两条线一起跑，才不容易卡死在单点上。
