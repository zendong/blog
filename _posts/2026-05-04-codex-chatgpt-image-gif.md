---
title: "codex+gpt-image2,实现一键生成小璞GIF"
date: 2026-05-04
categories:
  - 技术
tags:
  - codex
  - chatgpt-image
  - gif
  - pracmo
  - puki
layout: post
hero_image_ai_generated: true
image_prompt: "Create a clean abstract 16:9 editorial poster background for a Chinese experience-sharing blog post about a new workflow for making transparent mascot GIFs. Minimal light background, one cute pangolin-like mascot silhouette, a short frame strip, translucent layer cards, chroma-key green accent, product-engineering workflow mood, spacious layout with large empty area on the left for Chinese title typography, crisp premium editorial style, no readable text, no logos, no watermarks."
image_prompt_file: "assets/prompt/2026-05-04/2026-05-04-codex-chatgpt-image-gif.txt"
---

> "Animation is not the art of drawings that move but the art of movements that are drawn." — Norman McLaren，见 Alanna Thain《In the Blink of an Eye: Norman McLaren Between Dance and Animation》

![首图](/assets/images/2026/2026-05-04-codex-chatgpt-image-gif.png)

这两天我在折腾一件挺小，但很有意思的事。

给璞奇的吉祥物小璞做 GIF。

不是那种随便贴两张图一闪一闪的 GIF，而是一个能在聊天里直接用的小表情。比如「溜了」，小璞一缩，滚成一个穿山甲球，露出一只眼睛，然后滚出画面。再比如「服了，晕倒」，它先一脸无语，然后眼冒星星，晃两下，啪叽倒下。

听起来像美术活。

但这次真正让我觉得有意思的，不是哪一个工具多神，而是我终于跑通了一套新方案。用 Codex 串流程，用 GPT-Image 2 出关键帧，再用脚本抠绿、切帧、预览、校验，最后合成透明 GIF。

也就是说，目标不再是「生成一张好看的图」。

目标是「给一个动作，尽量一键生成一套可交付的小璞 GIF 资产」。

最后效果大概是这样。

![小璞溜了 GIF](/assets/images/2026/2026-05-04-codex-chatgpt-image-gif-liule.gif)

![小璞服了晕倒 GIF](/assets/images/2026/2026-05-04-codex-chatgpt-image-gif-yundao.gif)

它很适合拿来讲一个正在发生的变化，AI 不只是给你生成一张图，它正在进入「把图变成一套可复用资产」的阶段。

## 第一件事，不要直接要 GIF

我一开始也会下意识说，帮我生成一个 GIF。

但真正跑起来以后会发现，这个说法太粗了。

GIF 的难点不在「最后那个 .gif 文件」，而在每一帧是否顺序正确、角色是否一致、动作是否连续。尤其是吉祥物这种东西，不能第一帧是穿山甲，第二帧突然像小恐龙，第三帧又变成一个泛化的萌宠。

所以更稳的做法，是先让图片模型生成一张横向 sprite sheet。

比如「溜了」这个动作，我让它一次画出从站立、蜷缩、滚成球、滚动、出画的连续关键帧。

![小璞溜了源 sprite sheet](/assets/images/2026/2026-05-04-codex-chatgpt-image-gif-sprite-source.jpg)

这样做有两个好处。

一是角色风格更统一。模型在同一张图里画连续动作，比你分 8 次单独生成图片更不容易跑偏。

二是后处理更可控。你可以把这张图切成一个个姿态，再重新排成 480x480 的透明帧。

这一步很像做动画分镜。

先有关键姿势，再有播放节奏。

## 第二件事，透明背景要靠后处理

据codex自己交代，它内置的image-gen没有支持透明背景选项，它也没让我为难，它自己主动给出了方案，就是生成的图片用绿色背景，然后自己写了python代码，一把移除掉绿色背景从而实现透明背景效果。

我甚至不知道它怎么做的，它反正是做到了。

实际处理时还有一个小技巧，别死盯 `#00ff00`。模型生成出来的绿色背景，经常不是每个像素都精确等于 `#00ff00`，边缘还有抗锯齿。所以 `pracmo-image` 默认会用 `--auto-key border` 从边缘自动取背景色，再配合透明阈值和 `despill` 去掉绿色残边。

最后得到的单帧大概是这样。

![透明 PNG 单帧](/assets/images/2026/2026-05-04-codex-chatgpt-image-gif-transparent-frame.png)

这张图看起来像有底色，是因为网页预览会给透明图垫背景。真正的文件是 RGBA。流程里还会抽查四角 alpha，确认四角都是 0，避免以为透明，实际还是一张带底色的图。

## 第三件事，先看帧，再合成

这次踩的一个坑，很典型。

「服了，晕倒」那个 GIF，前面几帧都很好。小璞从无语、闭眼、晕圈，到身体往后仰，都挺顺。

结果到了摔倒后，方向突然变了。

前一帧还是头朝右往后倒，下一帧躺下后头尾方向突然反过来。单独看每张图都可爱，但连起来就像瞬移。

这就是 GIF 和单图最大的区别。

单图只看美不美。

GIF 要看时间。

所以后来我给流程里加了一条硬规则，合成 GIF 前必须先生成帧预览，按顺序肉眼检查。动作方向、头尾朝向、身体重心、角色大小都要连续。

![小璞服了晕倒帧预览](/assets/images/2026/2026-05-04-codex-chatgpt-image-gif-yundao-frames.jpg)

如果发现方向不对，先修帧。可以重排，可以镜像，可以补中间帧，也可以重生成。总之不要拿「单张好看但动画不顺」的素材硬合成。

「溜了」这个 GIF 也踩过类似的坑。

滚成球的时候，我一开始按 6 等分去裁 sprite sheet，结果球刚好贴到面板边缘，被切掉了一块。后面一旋转，球就不圆了。

修法也很工程，先把整张 sprite sheet 抠成透明，再根据 alpha 通道找连通主体，按 x 坐标排序，裁出每个姿态。

![小璞溜了帧预览](/assets/images/2026/2026-05-04-codex-chatgpt-image-gif-liule-frames.jpg)

这个小经验很值钱。

有些问题不是提示词能完全解决的。你得让模型做它擅长的部分，画出足够好的姿态。再让脚本做它擅长的部分，裁切、抠图、排序、校验。

## 第四件事，透明 GIF 还有一个暗坑

这里再提一个小技术点。

我这里依赖了开源的 `slack-gif-creator` skill 来合成 GIF。它里面的 `GIFBuilder` 很方便，能控制尺寸、帧率、颜色数，也能导出适合 Slack emoji 的 128x128 版本。

但有个问题，GIFBuilder 默认会把 RGBA 帧转成 RGB。

这一下，透明就没了。

所以我的实际流程是两步。

先用 GIFBuilder 生成一个预览版，确认帧率、尺寸、文件大小都在合理范围。

再用 PIL 重新保存最终交付版，把透明像素写成 GIF 的透明索引。保存后还要再读回来检查，看看 `transparency` 是否存在，四角转成 RGBA 后 alpha 是否为 0。

听起来有点绕，但实际很像前端里处理兼容性。不是你写了透明，它就一定透明。你得看最终格式怎么存。

## 最后把流程写成 skill

整个过程里，Codex 最有价值的地方，不是「它会写一句提示词」。

真正有价值的是，它能把一个模糊需求拆成一套工程动作。

比如我说，生成一个小璞「溜了」的 GIF。

`pracmo-image` 会先读小璞三视图和身份规则，知道颈部玉石不能画成吊坠，手背黄色鳞片不能画成手环。生成时优先走 Codex 内置 `image_gen`，需要透明时先产出 chroma-key 源图，再调用脚本转成透明 PNG。

它也会建任务目录，把 `*-source.png`、透明帧、帧预览、最终 GIF 都放在同一个目录里。源图要保留，方便回溯和重做。透明 PNG 要验证 RGBA 和四角 alpha。GIF 合成前必须先看帧预览，确认动作方向、头尾朝向、角色大小没有突然跳变。

如果是「滚成球」这种动作，流程还会优先生成横向 sprite sheet。后面不是简单按等宽硬裁，而是基于透明图的 alpha 通道做主体提取，再按 x 坐标排序。这样可以避开球体被切掉一块的问题。

最后一步才交给开源的 `slack-gif-creator` 合成 GIF。它可以先做 Slack 尺寸和帧率预览，但透明 GIF 交付版还要额外用 PIL 写透明索引，并读回来确认 `transparency` 存在。

这次最后我把这些规则写进了 `pracmo-image` skill。它还谈不上完全无人值守，但已经初步接近「一句话生成小璞 GIF」：给一个动作或情绪，Codex 负责把流程跑完。

过去我们说 AI 生成图片，重点通常在「出图」。但现在我越来越觉得，真正有用的是「出资产」。图只是中间结果，资产要有命名、有目录、有源文件、有后处理、有校验、有复用规则。这样它才不是一次性的烟花，而是能放进产品里的零件。

## 如果你也想试

可以按这个顺序来。

前提也先说清楚：需要能科学上网，也需要可用的 ChatGPT 会员。这个流程里，最关键的生图能力来自 ChatGPT Image 2。

1. 先确定角色参考图，把不可变的形象规则写清楚。
2. 用 GPT-Image 2 生成源图。需要透明时，先生成纯色 chroma-key 背景。
3. 保留 `*-source.png`，再用脚本转成 RGBA 透明 PNG。
4. 校验透明图，至少确认文件是 RGBA，四角 alpha 为 0。
5. 如果是 GIF，先生成同规格透明帧和帧预览，肉眼检查连贯性。
6. 再合成透明 GIF，同时导出一个小尺寸 emoji 版。
7. 把踩坑经验写回提示词模板或 skill，下一次继续复用。

这套流程现在还有手工环节，但每一步都能看见哪里在失真。等规则稳定后，再把它交给 `pracmo-image` 串起来，就能慢慢走向一键生成。

小璞从一张三视图，变成一个能「溜了」也能「晕倒」的小动画。

这件事本身很小。但小东西动起来的时候，你会突然意识到，产品里的很多细节，其实都可以这样一点点被做出来。

> **璞奇启示**
>
> 1. 学习产品里的角色、图标和动效，不一定要一次追求全自动。先把「关键帧、透明化、校验、复用规则」拆开，AI 反而更容易稳定参与。
> 2. 做练习也是一样，先看每一步是否连贯，再追求最终结果。一个答案、一个动作、一段 GIF，本质都需要可检查的中间过程。
