---
title: "安卓上线改造手记，一轮应用商店反馈带来的改造"
date: 2026-06-13
categories:
  - 技术
  - 产品
tags:
  - pracmo
  - android
  - app-store
  - compliance
layout: post
hero_image_ai_generated: true
image_prompt: "Horizontal product-editorial illustration for a Pracmo Android release article: Puki the pangolin learning companion pushing a cart of app-store review checklist cards toward an upload gate, with privacy document cards, SDK puzzle pieces, push blocks, payment card, generic test devices, and a build package, fresh cream, sky blue, mint, aqua green, warm yellow and coral colors, no text or watermark."
image_prompt_file: "assets/prompt/2026-06-13/2026-06-13-pracmo-android-store-adaptation.txt"
---

> 一次 Android 上架，最后会变成多少张清单？

![首图](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation.png)

流水账记录一下为了适配安卓上线，做了哪些改造，有一部分是来自国内各个安卓应用商店的反馈。

## 隐私条款改成静态 HTML

![隐私政策静态页面](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-01-privacy-html.png)

原来页面的实现是从后端接口来获取后动态加载页面，目的是为了调整隐私条款时可以避免发布，包括多版本管理，但是有一些应用商店无法解析给出的接口。

基于此，改成静态网页。

访问方式也从 `https://www.zendong.com.cn/privacy` 改成 `https://www.zendong.com.cn/privacy.html`。为了向前兼容，老的 URL 还是对应到老逻辑，慢慢把对外提供的链接都调整成后者。

## 隐私条款信息不全，ANDROID ID

![ANDROID ID 反馈](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-02-android-id.png)

目前的采集是嵌入了友盟+的 SDK，需要补上关于「ANDROID ID 的收集说明，包含目的、方式、范围」，同步修改 Web 端的隐私政策 HTML 文件。

```
为保障应用基础运行、统计去重、异常排查、设备兼容性分析及服务安全风控，我们可能在 Android 设备上收集 ANDROID ID。具体说明如下：

- **收集目的**：用于识别同一设备上的重复统计请求、分析设备兼容性与崩溃异常、提升服务稳定性，并辅助识别异常访问或滥用行为；
- **收集方式**：由应用集成的系统能力或第三方统计 SDK 在应用运行过程中自动读取，并通过加密通道传输；我们不会要求您手动提供该信息；
- **收集范围**：仅限 ANDROID ID 及与设备运行环境相关的必要基础信息，不包含您的姓名、手机号、通讯录、短信、照片、精确位置等敏感个人信息；该信息不会用于广告投放、用户画像或与您的账号身份进行直接关联。
```

## 隐私条款信息不全，SDK 信息要补齐

![SDK 信息补齐反馈](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-03-sdk-list.png)

由于要支持多个厂商的 push、IAP，嵌入了对应的官方 SDK，都需要进行补充说明。OPPO 很友好地列出了所有需要列出的 SDK，非常好，直接拿来用即可。

## 隐私保护，未同意前禁止读取剪贴板

![剪贴板读取反馈](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-04-clipboard.png)

检测认为「未同意前 Flutter 读取剪贴板」。

定位结果比较明确，不是业务主动读剪贴板，而是协议弹窗里的 `Markdown(..., selectable: true)` 会启用 Flutter 文本选择能力。在 Android 上，文本选择和编辑菜单可能触发剪贴板读取，被合规平台记录成「未同意前 Flutter 读取剪贴板」。

修复方向是，隐私协议、用户条款这类同意前可打开的协议弹窗全部禁止文本选择。

## 首次必须在登录页面出现前独立弹框展示隐私政策

OPPO 驳回中有如下这一条。

![首次启动隐私弹窗反馈](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-05-first-launch-privacy.png)

参考了一下安卓平台上的其他应用首次登录时的表现，理解要求如下。

平台的硬性要求大概是这样。

1. 首次启动必须弹出独立的、不可跳过的弹窗，不能默认勾选同意。
2. 弹窗里必须清晰展示《用户协议》和《隐私政策》的可点击链接，点了能直接打开。
3. 弹窗必须有「同意」和「不同意 / 退出 App」两个按钮，点击「不同意」必须直接关闭 App。
4. 弹窗文字必须明确告知用户，「点击同意即表示您已阅读并同意上述协议」。

改造后首次登录时增加了如下的确认界面。

![首次启动隐私确认界面](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-06-first-launch-dialog.png)

## 重新安全评估

由于 App 改过名，需要重新为「璞奇」App 进行安全评估。

之前有过一些经验，快速提交一版，但是很快被驳回。

![安全评估驳回反馈](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-07-security-assessment.png)

电话联系了审核单位，对方告知是涉及到深度合成内容，需要前置许可中选择「人工智能技术/算法」，并且地方网信办前置登记通过的信息，或者备案完成的截图。

一轮交互，最终完成了新的 App 创建与安全评估。

## 资质相关

![资质相关反馈](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-08-qualification-list.png)

按照提示来补齐所有这些文件。

![资质文件清单](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-09-qualification-files.png)

## 小米、VIVO 等平台直接无法登录

目前还没有接大规模的真机验证的平台，针对安卓平台的复杂异构环境还不太了解。只是用家里的华为手机测了基本功能，结果安装到朋友的小米手机，直接就无法打开，出现了整体白屏的现象。

在小米、VIVO 的测试平台也出现了这样的反馈。

![小米平台测试反馈](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-10-mi-platform.png)

![VIVO 平台测试反馈](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-11-vivo-platform.png)

幸好 VIVO 的测试平台提供了 log 文件，让 Codex 排查后评估可能的链路是「启动 FlutterEngine -> GeneratedPluginRegistrant 注册插件 -> 某个原生插件静态初始化 NPE -> 插件注册整体失败 -> shared_preferences channel 不可用 -> App 初始化失败 -> 错误页本地化未初始化 -> 白屏/灰屏」。

在这个链路上，有可能是依赖了不完整的 `china_push` 库导致。这个库引入的目标是自动对接到各个安卓厂商内置的 push 库，但是当时配置不完整。

经评估，`china_push` 直接移除掉。push 库，与 IAP 一样，都是一定跟着安卓厂商走的，就变成针对不同厂商时独立出包、针对性管理。

要单独对接国内各个厂商的不同逻辑，又是一通工作量。领着 Agent，各个击破。

补充，后发现 IAP 这个其实并没有要求对接每一个安卓厂商，后面就除了 iOS 和 Google Play，其他都统一到微信支付，这大大简化了逻辑。

## 对话发送兼容性问题

在有些平台上出现这样的兼容性问题。

![输入法显示换行按钮](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-12-keyboard-newline.png)

预期的应该是「发送」按钮。

根本原因，Flutter 对 `maxLines` 和 `textInputAction` 的处理规则。

Flutter 内部有一个隐式规则。

1. 当 `maxLines == 1`，也就是单行输入时，你设置的 `textInputAction` 会被尊重。比如设置为 `TextInputAction.send`，键盘就会显示「发送」按钮。
2. 当 `maxLines > 1` 或 `maxLines: null`，也就是多行或自适应时，Flutter 会强制将 `textInputAction` 覆盖为 `TextInputAction.newline`，此时键盘只会显示「换行」按钮。

但这个规则的生效时机和边界处理，在不同 Flutter 版本、不同 Android 定制系统上存在差异。

1. 部分机型和系统上，Flutter 能正常识别你强制设置的 `textInputAction: TextInputAction.send`，覆盖默认的换行行为。
2. 另一部分机型和系统上，输入法会无视你设置的 `textInputAction`，直接根据多行模式的判断，强制显示「换行」。

为了避免这种细粒度的兼容问题，干脆恢复了输入区域的「发送」图示，这样应该万无一失了吧。

![恢复发送图示](/assets/images/2026/2026-06-13-pracmo-android-store-adaptation-13-send-icon.png)

经过一轮密集的改造，先产出了一版，并且针对国内各厂商采用统一版本，内置各个厂商的 push SDK，自动挑选匹配的，再统一走微信支付。

逐步提交给到各个平台，等待下一波反馈。

> **璞奇启示**
>
> 1. 学习产品不只是把题做好，还要把入口、合规、兼容和支付这些基础链路做稳。用户看见的是一次打开 App，背后其实是一整套平台要求和设备环境。
> 2. 复杂系统的学习也可以这样拆，先把反馈逐条展开，再把每一条变成可验证的小任务。练习不是只练知识点，也是在练这种拆问题的能力。
