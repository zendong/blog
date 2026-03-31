---
title: "「右边怎么没了？」与顶级模型磨穿十七轮：Flutter 长图分享极限打磨实录"
date: 2026-03-31
categories:
  - 技术
tags:
  - flutter
  - repaintboundary
  - gpu-texture
  - flutter-markdown
  - puqi-app
layout: post
image_prompt: "A cinematic technical illustration of Flutter mobile development debugging: a very tall vertical smartphone canvas with a decorative Markdown text poster preview, split layers showing RepaintBoundary, FittedBox transform, GPU texture grid limits at 8192 pixels, and an isolated render pipeline diagram with PipelineOwner and RenderView, deep teal and amber accent lighting, clean isometric infographic style, no legible text, 16:9 aspect ratio"
image_prompt_file: "assets/prompt/2026-03-31/2026-03-31-flutter-share-right-cut-17-rounds.txt"
---

> "过犹不及。" — 《论语·先进》

「右边怎么没了？」——一个 Flutter 分享页面的截图功能，预览正常但导出图片总是被截断。我和 **顶级模型**从 UI 层一路磨到 Flutter 渲染引擎深处：`FittedBox`、`RepaintBoundary`、`OffsetLayer`、GPU 纹理限制……前后 **17 轮**不像闲聊，更像在把一条链路**打磨到极限**；最终彻底重写截图架构才收住。这篇文章完整记录了每一轮的诊断、修复和失败，希望能帮你在类似问题上少走弯路。

![首图](https://blog.zendong.com.cn/assets/images/2026/2026-03-31-flutter-share-right-cut-17-rounds.png)

## 会话侧记：模型、时间与账单

这次排查主要在 **Claude Opus 4.6** 上完成——属于我当时能拿到的、最适合长代码与渲染细节对撞的 **顶级模型** 之一。从第一轮梳理需求到第十七轮独立管线落地，实际耗时 **两个多小时不止**；中间穿插运行、对照截图、改代码、再跑一轮，墙钟时间只会更长。那种感受不是「问几句就好」，而是把假设一轮轮磨掉，直到剩下一条能站得住的架构。

按平台用量粗算，这一轮多轮对话的 **token 费用预计在 40 美元量级**（输入输出合计后的估算，非精确账单）。不便宜。它提醒我两件事：一是这类「渲染 + 长代码」问题，**别低估对话轮次**；二是如果某一类方案连续几轮都只是在同一套假设上打补丁，**不如早点让 AI 重新设计一条 plan**，用新链路替代老链路——下文第 16 轮到第 17 轮的转折，本质上就是一次「推翻重来」。

---

## 背景

我们的 Flutter 移动端 App「璞奇」有一个文字装饰分享功能（`TextDecorationPage`）：用户输入或粘贴一段文字（支持 Markdown），选择主题样式和字号，生成一张精美的装饰长图，可以保存到相册或分享给好友。

功能看起来简单，但背后涉及的技术栈相当复杂：

- Markdown 渲染（`flutter_markdown`）
- 多种装饰主题（网格、彩纸、水墨、PPT 等自定义 `CustomPainter`）
- 动态字号计算
- 长图模式 / 分页模式切换
- `RepaintBoundary.toImage()` 截图导出
- 全屏预览（Hero 动画）

**核心矛盾**：屏幕上预览看着很完美，但保存/分享出去的图片总是和预览不一样。

---

## 第 1 轮：需求梳理 — 发现问题全景

**我的指令**：「尝试梳理一下 TextDecorationPage 这个分享页面有什么问题」

AI 通读了整个 `text_decoration_page.dart`（当时约 2000+ 行），梳理出 6 个问题：

1. 预览与截图不一致 — 使用不同的构建逻辑
2. 字号硬编码，不随内容长度自适应
3. 分页索引越界（`_currentSplitIndex` 可能超出 `_splitTexts` 范围）
4. 编辑模式仍显示装饰预览
5. 全屏预览使用位图而非实时渲染
6. 保存/分享的状态反馈不够清晰

---

## 第 2 轮：全面修复 — 打基础

**我的指令**：「好好修复一下，需要确保展示与分享图片的一致性，控制一定的宽度+字体大小，然后根据内容多少长度自动控制」

AI 进行了大刀阔斧的改造：

- 实现 `_calculateOptimalFontSize` 动态字号算法
- 统一预览与截图共用 `_buildDecorationCanvas` 构建逻辑
- 添加 `_clampSplitIndex` 防止越界
- 改善保存/分享的状态反馈 toast

修复后运行测试——3 个测试全部通过。但实际运行效果……

---

## 第 3 轮：编辑页面和预览区域的交互问题

**我的反馈**：「上面修改的效果不对：1）"编辑"页面只是为了修改文字内容，这时候不涉及预览；2）在选择了样式、字号后，中间图片展示区域需要时左右充满界面，上下长度可以移动的状态，点击后弹出可以全面预览」

**问题诊断**：编辑模式还在渲染装饰画布；预览区域有 padding 和居中，没有充满屏幕宽度。

**修复**：

- 创建纯文本编辑视图 `_buildEditingView`，只有 `TextField`，不渲染装饰
- 预览区使用 `FittedBox(fit: BoxFit.fitWidth)` 让内容横向充满

---

## 第 4 轮：长图预览一片混乱

**我的反馈（附截图）**：「效果明显不对啊，长图模式下，中间展示没有居中，且乱七八糟」

截图中可以看到：内容偏左、文字和背景错位、印章位置错乱，整个画面一片混乱。

![第4轮：长图预览一片混乱](https://blog.zendong.com.cn/assets/images/2026/2026-03-30-flutter-share-image/round4-preview-messy.png)

**问题诊断**：使用了 `Transform.scale` + `Alignment.topLeft` 来缩放预览，这只影响视觉渲染，不影响布局约束，导致内容的绘制位置和布局位置不一致。

**修复**：将 `Transform.scale` 替换为 `FittedBox(fit: BoxFit.fitWidth, alignment: Alignment.topCenter)`。`FittedBox` 会正确处理布局和绘制的一致性。

---

## 第 5 轮：全屏预览被截断

**我的反馈（附两张截图对比）**：「现在默认展示没问题，但是点击后的预览效果不对了」

主页面预览已经正常（PPT 演示主题，字号 24），但全屏预览时内容右侧被截断、文字溢出，完全无法正常阅读。

| 主页面预览（正常） | 全屏预览（截断） |
|:---:|:---:|
| ![预览正常](https://blog.zendong.com.cn/assets/images/2026/2026-03-30-flutter-share-image/round5-preview-ok.png) | ![全屏截断](https://blog.zendong.com.cn/assets/images/2026/2026-03-30-flutter-share-image/round5-fullscreen-truncated.png) |

**问题诊断**：全屏预览页面仍在使用之前捕获的低分辨率位图，在全屏显示时拉伸模糊且截断。

**修复**：创建 `_FullScreenWidgetPreviewPage`，全屏预览时直接渲染 `_buildDecorationCanvas` widget（而非位图），用 `FittedBox` 缩放到屏幕宽度。

---

## 第 6 轮：全屏预览修好了，但换了主题还是有问题

**我的反馈（附两张截图对比）**：「全屏预览还是有问题，这个不可修复吗？」

切换到 PPT 演示主题后，全屏预览依然右侧截断。

| 主页面预览（正常） | 全屏预览（右侧截断） |
|:---:|:---:|
| ![PPT预览正常](https://blog.zendong.com.cn/assets/images/2026/2026-03-30-flutter-share-image/round6-preview-ok-ppt.png) | ![PPT全屏截断](https://blog.zendong.com.cn/assets/images/2026/2026-03-30-flutter-share-image/round6-fullscreen-truncated-ppt.png) |

**修复**：进一步统一全屏预览的 widget 渲染逻辑，确保所有主题下都使用相同的 `_buildDecorationCanvas` 构建路径。

---

## 第 7 轮：展示一致了，但保存出来的图片还是不一样

**我的反馈**：「展示现在是一致了，但是"保存"出来的图片还是不一样，彻底解决一下保存或者分享得到的图片的效果」

**问题诊断**：保存使用 `_captureWidgetAsImage` 方法，在 `Overlay` 中重新渲染 widget 并截图。但 Overlay 的 `BuildContext` 缺少主 widget 树中的 `Theme`、`MediaQuery`、`Directionality`，导致 `MarkdownBody` 渲染出的样式和布局与预览不同。

**修复**：在 Overlay 中显式注入完整上下文：

```dart
final entry = OverlayEntry(
  builder: (_) => Positioned(
    child: MediaQuery(
      data: currentMediaQuery,      // ← 注入
      child: Directionality(
        textDirection: currentDirection, // ← 注入
        child: Theme(
          data: currentTheme,        // ← 注入
          child: RepaintBoundary(
            child: child,
          ),
        ),
      ),
    ),
  ),
);
```

---

## 第 8 轮：图片底部大量空白

**我的反馈**：「还有图片底部空间问题，文字区域底部有大量的空白，然后才是印章，移除这大量的空白区域」

**问题诊断**：高度计算存在双重 padding。`calculateMarkdownHeight`（在 `text_decoration_layout.dart` 中）内部已加了 `verticalPadding * 2`，而调用方 `_measureContentHeightForFont` 又加了 `canvasTopPadding + canvasBottomPadding + stampSpace`。

**修复**：修改 `calculateMarkdownHeight` 只返回纯文本内容高度，padding 统一由调用方添加。

---

## 第 9 轮：导出图片右侧截断

**我的反馈**：「导出还是跟预览的不一致啊，你再排查清楚原因」

**问题诊断**：虽然注入了 `Theme`/`MediaQuery`/`Directionality`，但 Overlay 中 `Positioned(left: -10000, top: -10000)` 的子 widget 被屏幕宽度约束（如 390px），而非目标宽度 800px。MarkdownBody 在 390px 下布局，导出后文字右侧被切掉。

**修复**：给 `Positioned` 添加显式 `width: size.width, height: size.height`，强制在 800px 宽度下布局。

---

## 第 10 轮：字号越大，截断越多

**我的反馈**：「还是不对啊，导出的图片会右侧被截断，跟预览还是不一样」

**我的进一步反馈**：「还是不对，字号越大，导出的图片中文字截掉的越多！！这个问题为什么这么难解决，分析一下」

**问题诊断**：AI 进行了深入分析，发现问题出在 Overlay 方案的根本缺陷——在 Overlay 中"重新渲染"和在主 widget 树中渲染，即使注入了相同的 Theme/MediaQuery，MarkdownBody 的布局仍然可能存在细微差异。

**修复方案大转向**：放弃 Overlay 重新渲染方案。改为直接从预览中已渲染好的 `RepaintBoundary` 截图。在预览区添加 `_previewBoundaryKey`：

```
FittedBox          ← 视觉缩放到屏幕宽度
  └── RepaintBoundary(key: _previewBoundaryKey)  ← 截图点
       └── SizedBox(width: 800)
            └── _buildDecorationCanvas
```

`pixelRatio` 动态计算为 `_contentWidth / previewWidth * 3.0`，确保输出高清。

---

## 第 11 轮：还是老样子

**我的反馈**：「啊啊啊！还是老样子，继续深挖」

**问题诊断**：深入调查 `flutter_markdown` 源码，发现 `MarkdownStyleSheet.fromTheme(Theme.of(context))` 内部会自动调用 `MediaQuery.textScalerOf(context)` 获取系统辅助功能的文字缩放比例。如果用户设备开启了"大字号"辅助功能，`textScaler` 会被二次应用于已经指定了 `fontSize` 的样式——相当于字号被放大了两次！

大字号 → 文字宽度超过 800px 容器 → 右侧溢出被裁剪。字号越大，溢出越多——完美解释了"字号越大截断越多"的现象。

**修复**：

```dart
return MarkdownStyleSheet.fromTheme(Theme.of(context)).copyWith(
  textScaler: TextScaler.noScaling,  // ← 关键修复
  p: textStyle.copyWith(height: 1.8),
  // ...
);
```

---

## 第 12 轮：悲剧，还是不对

**我的反馈**：「悲剧啊，还是不对！！！」

AI 添加了更多调试日志，尝试进一步排查。

---

## 第 13 轮：截图对比 + 日志定位

**我的反馈（附两张截图）**：「还是不行，两张图看一下，第一张是界面看到的，第二张是在导出到相册看到的。还是没有定位到根因」

截图对比非常直观——预览中文字完整排版正常，但导出到相册后右侧大约 1/3 的文字被切掉：

| 界面预览（正常，字号 40） | 导出到相册（右侧截断） |
|:---:|:---:|
| ![预览正常](https://blog.zendong.com.cn/assets/images/2026/2026-03-30-flutter-share-image/round12-preview-ok.png) | ![导出截断](https://blog.zendong.com.cn/assets/images/2026/2026-03-30-flutter-share-image/round12-export-truncated.png) |

可以清楚地看到，导出图片中标题 "一、先了解基" 后面的字消失了，列表项的右半部分全部被切掉。

---

## 第 14 轮：关键日志信息

**我的反馈（附 toast 截图）**：「弹出的信息」

截图显示保存成功的 toast，透露了关键的尺寸信息：

![toast 显示保存尺寸](https://blog.zendong.com.cn/assets/images/2026/2026-03-30-flutter-share-image/round13-toast-size.png)

`图片已保存到相册 [800×5744 → 2400.0×17232.6px]` — 逻辑尺寸 800px、pixelRatio=3.0、输出 2400×17232。看起来尺寸是对的，但图片确实是截断的。

---

## 第 15 轮：GPU 纹理限制浮出水面

**我的反馈（附截图 + 控制台日志）**：

![导出图片右侧被切掉](https://blog.zendong.com.cn/assets/images/2026/2026-03-30-flutter-share-image/round14-export-right-cut.png)

```
flutter: 📸 RepaintBoundary size: 800.0x6278.859240722656
flutter: 📸 Captured image: 1043x8192
保存到相册的依然是截断的
```

**问题诊断**：这条日志是破案的关键！

- `RepaintBoundary` 逻辑尺寸：800.0 × 6278.8
- 期望输出（pixelRatio=3.0）：2400 × 18836
- **实际输出：1043 × 8192**

高度被限制在 **8192**——这是 iOS Metal 渲染引擎的 **GPU 纹理最大尺寸**！Flutter 的 `toImage()` 在超出 GPU 限制时**静默降低 pixelRatio**，导致：

- 宽度从 2400 缩小到 1043
- 高度从 18836 截断到 8192
- 宽高比完全失真

**修复**：实现分段渲染 + 拼接方案：

- 定义 `_maxTextureSize = 4096`（保守值）
- 将长图分成多段，每段的像素尺寸控制在 GPU 限制内
- 在 Overlay 中逐段渲染 canvas 的不同区域
- 用 `PictureRecorder + Canvas` 拼接成完整长图

---

## 第 16 轮：分段渲染拼接，尺寸对了但内容还是截断

**我的反馈（附日志）**：

```
flutter: 📸 boundary: 800.0x6293.2, target: 2400x18880
flutter: 📸 tiled: ratio=3.0, segs=5, out=2400x18880
flutter: 📸 composited: 2400x18880
我已经崩溃了，导出的图片还是右侧被截掉了
```

**问题诊断**：虽然最终图片尺寸正确（2400×18880），但内容右侧仍被截断。分段使用的 Overlay 重新渲染 `_buildDecorationCanvas`，又回到了"渲染环境不一致"的老问题。

**修复尝试**：放弃 Overlay 重新渲染，改用 `OffsetLayer.toImage(rect, pixelRatio:)` 直接从预览的 `RepaintBoundary` 的渲染层分段截取子区域。

但这也没用——

**我的反馈（附日志）**：

```
flutter: 📸 boundary: 800.0x5459.2, target: 2400x16378
flutter: 📸 tiled: ratio=3.0, segs=4, out=2400x16378
flutter: 📸 composited: 2400x16378
目前的实现似乎找不到解决方案了，你最后再查一次，如果还是不行，整个分享功能重新设计一下了
```

**问题诊断**：`OffsetLayer.toImage()` 内部也使用 `Scene.toImage()`，同样受 GPU 纹理限制。而且更根本的问题是——`RepaintBoundary` 位于 `FittedBox` 内部，虽然逻辑尺寸报告 800px，但实际渲染区域被 `FittedBox` 的 `TransformLayer` 影响。

**所有基于"从屏幕 widget 树截图"的方案都走进了死胡同。**

到这里，继续在同一套「on-screen 截图」假设上堆补丁，性价比已经很低。更划算的做法，是让 AI **丢掉旧 plan，换一条架构级路线**：不是再找一个更巧妙的截屏位置，而是承认「截图必须脱离当前树」。

---

## 第 17 轮：独立渲染管线 — 终极方案

这是最后一轮，也是彻底解决问题的一轮。

**核心思路**：完全脱离当前 widget 树，在**独立的渲染管线**中渲染和截图。

参考 Flutter 社区知名截图包 `screenshot` 的 `captureFromLongWidget` 实现原理，创建独立的渲染环境：

```
┌─────────────────────────────────┐
│   独立渲染管线（脱离 widget 树）    │
│                                 │
│  PipelineOwner                  │
│    └── RenderView               │
│         └── RenderPositionedBox │
│              └── RepaintBoundary│
│                   └── Widget    │ ← 和预览完全相同的 build 逻辑
│                                 │
│  BuildOwner                     │
│    └── RenderObjectToWidgetElement │
│                                 │
│  InheritedTheme.captureAll()    │ ← 保持主题一致性
│  MediaQuery(textScaler: noScaling) │ ← 禁用系统字号缩放
└─────────────────────────────────┘
```

实现三个方法：

### 1. `_measureWidgetSize` — 测量自然尺寸

```dart
Size _measureWidgetSize(Widget widget, BoxConstraints constraints) {
  final measureRoot = _MeasurementRenderBox(constraints);
  // ... 独立 PipelineOwner + BuildOwner ...
  measureRoot.scheduleInitialLayout();
  pipelineOwner.flushLayout();
  return measureRoot.size;
}
```

在 800px 宽度约束下预布局 widget，获取其自然高度（如 5459px），完全不受屏幕的影响。

### 2. 动态 pixelRatio 计算

```dart
const double idealRatio = 3.0;
final maxByWidth = _maxTextureSize / measuredSize.width;   // 4096/800 = 5.12
final maxByHeight = _maxTextureSize / measuredSize.height; // 4096/5459 = 0.75
final safeRatio = min(idealRatio, min(maxByWidth, maxByHeight)); // 0.75
```

确保最终像素尺寸的宽和高都不超过 4096px。如果内容很长，会自动降低 pixelRatio。

### 3. `_renderWidgetToImage` — 独立管线渲染截图

```dart
final renderView = RenderView(
  view: view,
  configuration: ViewConfiguration(
    logicalConstraints: BoxConstraints(
      maxWidth: measuredSize.width,
      maxHeight: measuredSize.height,
    ),
    devicePixelRatio: safeRatio,
  ),
);
// ... layout → compositing → paint → toImage ...
```

在完全独立的 `RenderView` 中，以 800px 实际宽度布局和绘制，然后 `toImage`。没有 `FittedBox`，没有 `Transform`，没有 `Overlay`，没有屏幕约束。

**结果**：终于完美解决。

---

## 问题总结：为什么这么难？

回顾整个过程，这个问题之所以如此顽固，是因为它涉及了 Flutter 渲染引擎中多个隐蔽层面的交互：

| 层面 | 具体问题 | 发现于第几轮 |
|------|---------|-----------|
| Widget 构建 | 预览和截图使用不同的 build 逻辑 | 第 2 轮 |
| 布局约束 | FittedBox/Transform 影响子 widget 的实际渲染区域 | 第 4 轮 |
| BuildContext | Overlay 缺少 Theme/MediaQuery/Directionality | 第 7 轮 |
| 布局约束（再次） | Overlay 中 Positioned 受屏幕宽度约束 | 第 9 轮 |
| 文字缩放 | `MarkdownStyleSheet.fromTheme()` 隐式继承 `textScaler` | 第 11 轮 |
| GPU 硬件限制 | `toImage()` 在超出纹理限制时静默降低 pixelRatio | 第 15 轮 |
| 渲染管线 | 所有 on-screen 截图方案都受 widget 树环境影响 | 第 16 轮 |

其中最阴险的是 **GPU 纹理限制**：Flutter 的 `toImage()` 在超出限制时**不抛异常、不打 warning**，而是静默缩小，让你以为截图成功了——直到打开图片才发现内容被截断了。

---

## 经验教训

### 1. 截图永远不要依赖 on-screen widget 树

on-screen 渲染受太多因素影响：FittedBox 缩放、系统字号设置、屏幕宽度约束、GPU 纹理限制……任何一个都可能导致截图和预览不一致。

**正确做法**：使用独立渲染管线（`RenderView` + `PipelineOwner` + `BuildOwner`），让 widget 在指定的逻辑尺寸下完整布局和绘制。

### 2. 始终考虑 GPU 纹理限制

iOS Metal 的纹理限制通常是 4096 或 8192 像素。对于长图（高度可能上万像素），必须：

- 动态计算安全的 `pixelRatio`
- 或者实现分段渲染 + 拼接

### 3. `MarkdownStyleSheet.fromTheme()` 的隐藏坑

它会自动从 `MediaQuery` 获取 `textScaler`。如果你已经通过 `fontSize` 精确控制了字号，务必设置 `textScaler: TextScaler.noScaling`。

### 4. 添加诊断日志至关重要

如果不是添加了 `debugPrint('📸 RepaintBoundary size: ... Captured image: ...')` 这样的日志，我们可能永远发现不了 GPU 纹理限制的问题。关键指标：

- RepaintBoundary 的逻辑尺寸
- toImage 的实际输出尺寸
- 二者的比例是否等于预期的 pixelRatio

### 5. AI 辅助调试的价值与局限

这次调试过程中，AI 能快速定位代码层面的问题（如 BuildContext 缺失、double padding 等），但对于**渲染管线级别**的隐蔽问题（GPU 纹理限制、FittedBox 内部 Transform 行为等），需要**用户提供实际运行截图和日志**才能逐步逼近真相。

17 轮交互，每一轮都缩小了问题范围。虽然中间多次走入死胡同，但正是这些"失败"帮助我们排除了错误假设，最终找到了正确答案。

**另外一点**：当同一类架构（例如 Overlay 截图、on-screen `RepaintBoundary`）连续多轮仍无法自洽时，不必死磕微调——让模型 **输出新的总体方案**（本例即独立渲染管线），往往比在同一链路上再堆十个小修小补更省总成本。

---

## 最终代码架构

```
_captureFullImage()
  │
  ├── 构建 canvasWidget（与预览完全相同的 build 逻辑）
  │
  ├── InheritedTheme.captureAll() — 捕获主题上下文
  │
  ├── MediaQuery(textScaler: TextScaler.noScaling) — 禁用系统缩放
  │
  ├── _measureWidgetSize() — 独立管线测量自然高度
  │     └── _MeasurementRenderBox + PipelineOwner
  │
  ├── 动态计算 safeRatio = min(3.0, 4096/width, 4096/height)
  │
  └── _renderWidgetToImage() — 独立管线渲染截图
        ├── RenderView(ViewConfiguration: 指定逻辑尺寸 + pixelRatio)
        ├── PipelineOwner + BuildOwner
        ├── layout → compositing → paint
        └── RepaintBoundary.toImage(pixelRatio: safeRatio)
```

从第 1 轮到第 17 轮，这个文件从约 2000 行修改到 3280+ 行，经历了至少 6 种截图架构方案，最终才找到了正确的解法。

有时候，解决一个看似简单的 bug，需要的不是更巧妙的 hack，而是对底层架构的重新理解。

---

## 璞奇启示

**第一，练习与导出要同源。** 学习场景里若「练到的」和「考到的 / 导出的」不是同一套规则，用户会觉得「明明会了却挂科」。Flutter 里预览与导出要共用同一构建与同一渲染假设；璞奇里则对应：同一知识点上的练习与测评，应在同一套解释与难度标尺下生成。

**第二，卡住时换路径，比硬扛更划算。** 当一条实现路径反复踩坑，继续微调往往边际收益很低；明确换一套方案（新 plan），用更干净的前提重做，常常更快。对应到学习产品：与其在同一题型上堆提示，不如换一类表征或脚手架，帮用户换脑子。

---

## 信息说明

- 文中 **Claude Opus 4.6** 模型信息与公开介绍见 [Anthropic：Claude Opus 4.6](https://www.anthropic.com/research/claude-opus-4-6)（具体 API 名称与计费以官方文档为准）。
- **约 40 美元 token 费用** 为本次多轮会话的粗略估算，非平台精确账单；实际扣费以各服务商出账为准。
- Flutter 截图包 **`screenshot`** 社区实现思路可参考其包文档与源码（搜索 pub.dev `screenshot`）。
- 题图与正文截图位于本站 `assets/images/2026/` 下；正文配图目录为 `2026-03-30-flutter-share-image/`（素材日期与排查过程一致）。

---
