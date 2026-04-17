---
title: "领取经验：半小时完成小程序深度合成类目申请"
date: 2026-04-17
categories:
  - 技术
tags:
  - wechat-miniprogram
  - miniprogram
  - compliance
  - deep-synthesis
  - volcengine
  - 璞奇 app
layout: post
hero_image_ai_generated: true
image_prompt: "Editorial hero illustration for WeChat mini program deep synthesis service category application experience post, minimal flat vector, soft teal and slate blue on light gray, checklist clock document stack, no text no logos, 16:9"
image_prompt_file: "assets/prompt/2026-04-17/2026-04-17-miniprogram-deep-synthesis-category-tips.txt"
---

> "岁寒，然后知松柏之后凋也。" — 《论语·子罕》

![首图](/assets/images/2026/2026-04-17-miniprogram-deep-synthesis-category-tips.png)

**璞奇**小程序在国内非 iOS 侧上架，带 AI 对话等深度合成能力，就要申请微信「深度合成」相关类目。下面按我们这次实际填表顺序写，分享出来供同路人对照。

## 类目选项

![微信小程序后台类目选项示意](/assets/images/2026/2026-04-17-miniprogram-deep-synthesis-category-tips-01-wechat-options.png)

应用**只依赖第三方已备案大模型**，不做自训、不改模型，对照后台说明选 **2.1** 即可。具体编号以你提审时的界面为准。

## 要准备的资料

1）大模型公司（技术主体）的备案材料。自己上备案站截图很快，但微信还要求材料里能体现**对方公司盖章**。

2）你方与技术主体的**合作协议**，双方盖章。

![平台对深度合成类目的材料要求示意](/assets/images/2026/2026-04-17-miniprogram-deep-synthesis-category-tips-02-material-requirements.png)

去年问过一圈大模型与云厂商，多渠道比下来，**用火山引擎侧出具的备案说明和电子合同，整条链路可以全在线办完**，个人体感是最省时间的。线上推理未必只用豆包，**类目审核要的是材料链完整**，和实际默认调哪条模型可以不是一回事。阿里云等常见路径是客户经理、纸质合同寄送，来回周期长很多。

## 操作步骤

### 1）大模型已备案的凭证

在火山引擎侧下载，入口：[费用-合同管理](https://console.volcengine.com/finance/contract/)（若改版以控制台为准）。

![火山引擎侧下载的备案说明类 PDF 示意](/assets/images/2026/2026-04-17-miniprogram-deep-synthesis-category-tips-03-provider-proof-pdf.png)

**教训**，官网 PDF 里嵌的备案截图往往不够清晰，直接交会被打回「模糊不清」。需要再到 [互联网信息服务算法备案](https://beian.cac.gov.cn/#/home) **单独截一版高清图**，拼进最终上传的长图里，放在火山下载内容**之前**。

![算法备案公示站截图示意](/assets/images/2026/2026-04-17-miniprogram-deep-synthesis-category-tips-04-cac-beian-portal.png)

### 2）合作协议（购买服务合同）

在火山引擎**开通一下大模型服务即可**（按文档要求处于可用状态，不必真跑业务流量）。然后按 [火山方舟-客户应用上架指南-算法备案资质申请流程](https://www.volcengine.com/docs/82379/1326340?lang=zh) 在合同管理里生成、合并、下载带章合同（文档最近更新 2025-09-28，入口以页面为准）。

![火山引擎控制台开通模型示意](/assets/images/2026/2026-04-17-miniprogram-deep-synthesis-category-tips-05-enable-model-service.png)

![火山引擎合同管理下载示意](/assets/images/2026/2026-04-17-miniprogram-deep-synthesis-category-tips-06-contract-download.png)

材料齐了我们走了小程序类目**加急**，**大约半小时**通过。个体有差异，Good Luck。

![类目审核通过后的列表示意](/assets/images/2026/2026-04-17-miniprogram-deep-synthesis-category-tips-07-category-approved.png)

## 吐槽与本地拼图

微信这边材料要**图片**，还常要求**合成一张长图**，对开发者不友好，只能照规则来。

Mac 上把 PDF 导出清晰 PNG 再纵向合并，我用的两行如下（依赖 [MuPDF](https://mupdf.com/) 的 `mutool` 与 [ImageMagick](https://imagemagick.org/) 的 `magick`）。

```bash
mutool convert -O resolution=300,format=png -o out.png 大模型证明文件.pdf
magick out*.png -append long_image.png
```

---

国内上架，这可能还只是第一关，后续如何进展，见招拆招吧。

