---
title: "一个二维码，怎么把用户送到正确的应用商店"
date: 2026-07-01
categories:
  - 技术
  - 产品
tags:
  - pracmo
  - download-router
  - qr-code
  - nginx
  - app-store
layout: post
hero_image_ai_generated: true
image_prompt: "Horizontal product-editorial illustration for a Pracmo unified app download URL article: Puki the pangolin holds a QR-code-like card, one abstract URL route passes through a gateway into a web page and branches to generic mobile download cards for iOS, HarmonyOS / Huawei, Android stores, Tencent App Store fallback and APK fallback, fresh cream, sky blue, mint, aqua green, warm yellow and coral colors, no text, no logos, no watermark."
image_prompt_file: "assets/prompt/2026-07-01/2026-07-01-one-url-app-download-router.txt"
---

> 线下物料只能印一个二维码时，怎么让 iPhone、华为、小米、OPPO、vivo 和普通 Android 用户都少走弯路？

![首图](/assets/images/2026/2026-07-01-one-url-app-download-router.png)

故事是这样的。

璞奇 App 上架以后，我们遇到一个很现实的问题。

官网可以放很多按钮。App Store 一个按钮，华为一个按钮，小米一个按钮，应用宝一个按钮，APK 再来一个按钮。

但线下物料不行。

展架、传单、海报、朋友圈截图，很多时候只能放一个二维码。你不可能在一张小卡片上塞六七个码，再让用户自己判断该扫哪一个。

用户也不会有这个耐心。

所以这个需求非常朴素，一个二维码，一个 URL，用户扫码后自动去适合自己的下载入口。

我们最后选的统一入口是这个。

[https://zendong.com.cn/dl](https://zendong.com.cn/dl)

这篇顺手把实现分享出来。它不是一个特别复杂的系统，但里面有几个取舍挺有意思，尤其是移动端下载这件事，一旦碰到国内安卓生态，就会马上从「做个链接」变成「做一条兼容路线」。

## 需求从哪来

这个需求不是拍脑袋做的。

它来自三个场景。

一个是官网。用户点下载 App，我们不希望他先看一堆平台按钮，再自己判断手机型号。

一个是线下。物料一旦印出去，二维码最好几年都不要变。今天华为链接换了，明天 APK 换了，不能每次都重新印。

还有一个是增长投放。我们需要在 URL 后面加 `source`、`campaign`、`entry` 这样的参数，知道用户从哪来，但又不能让参数把下载链路搞复杂。

所以，核心目标其实是三句话。

入口稳定。

自动适配。

失败可退。

我觉得第三句最容易被低估。很多下载页的问题，不是不能自动跳，而是一旦自动跳失败，用户就掉进了一个黑洞。微信打不开应用市场，厂商 scheme 被拦截，桌面浏览器识别不了设备，最后页面空白或者卡住。

这就很伤。

我们的原则是，能自动就自动，不能自动就让用户自己选。不要假装环境永远理想。

## 一个 URL 怎么落到页面上

这条链路分两层。

第一层在 nginx，负责保证 `https://zendong.com.cn/dl` 这个裸域名路径能直接回到 Web SPA。

第二层在 Web 页面，负责根据 User-Agent 识别设备，再跳到对应应用商店或兜底入口。

画出来大概是这样。

![统一下载入口架构图](/assets/images/2026/2026-07-01-one-url-app-download-router-architecture.png)

nginx 这里有一个关键点。

我们的裸域名 `zendong.com.cn` 大多数路径会跳到 `www.zendong.com.cn`。但 `/dl` 是二维码固定入口，所以它不能跟着普通裸域名规则走。

生产配置里对 `/dl` 做了特例。

```nginx
location = /dl {
    expires off;
    add_header Cache-Control "no-store";
    try_files /index.html =404;
}

location = /dl/ {
    return 301 https://zendong.com.cn/dl$is_args$args;
}

location ^~ /assets/ {
    expires 7d;
    add_header Cache-Control "public, max-age=604800";
    add_header Access-Control-Allow-Origin "*";
    try_files $uri =404;
}
```

这里有两个小细节。

`/dl` 直接返回 `index.html`，不跳 `www`。

`/assets/` 也要在裸域名下能访问，因为 Vite 构建出来的 `index.html` 会继续加载静态资源。只让 `/dl` 返回页面、不管 assets，会变成首页壳子能回来，JS 和 CSS 全部 404。

这块其实很像接线。

二维码接到裸域名，裸域名接到 SPA，SPA 再接到真正的下载目标。任何一段接错，用户扫出来就不是你想要的那条路。

## Web 页面怎么判断设备

Web 端的配置集中在一个文件里。

`apps/web/src/config/downloadTargets.ts`

这个文件是下载目标的单一来源。App Store、华为 AppGallery、荣耀、小米、OPPO、vivo、应用宝、官方 APK，都在这里维护。

页面路由挂在 React Router 里。

`/dl` 对应 `DownloadRouterPage`。

页面进来后，会读 `navigator.userAgent`，做两类判断。

一类是设备。

| 识别结果 | 当前规则 |
| --- | --- |
| iOS | iPhone、iPad、iPod |
| 华为 / 鸿蒙 | huawei、harmonyos |
| 荣耀 | honor |
| 小米 | miui、xiaomi、redmi、mibrowser |
| OPPO | oppo、coloros、oneplus |
| vivo | vivo、iqoo |
| 普通 Android | android |
| 未知 | 以上都不匹配 |

另一类是浏览器环境。

微信、QQ、微博这些内置浏览器会单独识别出来。识别出来以后，页面不会直接禁止自动跳转，但会提示用户，如果打不开应用市场，可以点右上角用系统浏览器打开，或者走手动下载。

这块需要注意一下，厂商识别必须排在通用 Android 前面。

不然所有安卓设备都会先命中 `android`，后面的华为、小米、OPPO、vivo 就没有机会了。

## 自动跳转和兜底

真正跳转的代码很短。

```ts
if (detection.target?.enabled && detection.target.url) {
  window.location.href = detection.target.url;
}
```

但目标选择有优先级。

| 设备 | 自动目标优先级 |
| --- | --- |
| iOS | App Store |
| 华为 / 鸿蒙 | 华为 AppGallery -> 应用宝 -> APK |
| 荣耀 | 荣耀应用市场 -> 华为 AppGallery -> 应用宝 -> APK |
| 小米 | 小米应用商店 -> 应用宝 -> APK |
| OPPO | OPPO 商店 -> 应用宝 -> APK |
| vivo | vivo 商店 -> 应用宝 -> APK |
| 普通 Android | 应用宝 -> APK |
| 未知设备 | 不自动跳转，直接手动选择 |

这张表就是整个下载页的核心。

每个厂商优先去自己的市场。厂商市场不可用时，落到应用宝。应用宝再不行，Android 还有官方 APK。

应用宝在这里承担的是通用网页兜底角色。更准确一点说，我们用的是腾讯应用宝提供的「微下载」链接。

![应用宝微下载配置](/assets/images/2026/2026-07-01-one-url-app-download-router-yingyongbao-micro-download.png)

它不只是一个普通下载页。

在应用宝后台，微下载链接可以继续绑定 iOS 下载地址、Android 首页 scheme、鸿蒙首页 scheme、Applink 协议头等配置。这样用户落到 `https://a.app.qq.com/o/simple.jsp?pkgname=cn.com.zendong.wancai` 后，应用宝还能根据访问环境再做一次处理。

这对微信生态尤其有用。

微信、QQ、浏览器、厂商系统，各自对 scheme、App Link、下载包的拦截策略都不完全一样。我们自己的 `/dl` 页面先做第一层设备识别，应用宝微下载再做第二层场景适配。访问环境再复杂，至少还能先落到一个能打开的网页。

对 iOS、鸿蒙这类环境，最终怎么提示或跳转，要以应用宝微下载页面自己的处理为准。我们不会把它当唯一入口，但它很适合站在第二层兜底位。

再往后，就是 APK。

APK 是安卓最后一道门。用户如果在某些环境里打不开商店，至少还能下载官方安装包。这个选择不如应用市场顺滑，但比让用户卡死强。

这里其实还有一个取舍，我们到底是自己做 `/dl`，还是直接把二维码交给应用宝微下载这类现成服务。

如果只是快速上线，现成服务当然省事。它已经适配了很多微信、QQ、浏览器里的跳转细节，也能配置 iOS、鸿蒙、Applink、scheme 这些东西。

但我们最后还是把第一跳留在了自己手里。

| 方案 | 好处 | 问题 | 适合场景 |
| --- | --- | --- | --- |
| 直接使用现成服务 | 上线最快，微信生态适配成熟，后台可配置多端链接 | 主入口、页面体验、参数处理、兜底策略都受平台限制 | 只需要一个通用下载页 |
| 自主实现 `/dl` | 域名、页面、设备识别、手动选择、APK 兜底、投放参数都可控 | 要自己维护 UA 规则、商店链接、nginx 配置和测试 | 需要长期品牌入口和多渠道投放 |
| 当前混合方案 | 自研入口先分流，应用宝微下载做二级兜底 | 复杂度比单一方案高一点 | 既要品牌可控，又要微信生态兜底 |

自研的优势，不是我们比应用宝更懂所有手机环境。

恰恰相反，应用宝在微信生态里的适配能力，我们应该直接用。

真正重要的是，二维码和 URL 属于我们自己。以后应用市场链接换了，APK 地址换了，甚至兜底服务换了，用户手里的二维码都不用动。我们还可以在第一跳保留来源参数，失败时展示自己的手动选择页，把「自动失败」变成「用户还能继续选」。

所以这不是完全自研和完全外包的二选一。

我们的做法是，第一跳自己掌握，复杂生态交给成熟服务兜底。

页面还设置了一个 1500ms 的定时器。

如果自动跳转成功，用户通常已经离开了这个页面。

如果跳转被拦截、scheme 没打开、设备没识别出来，1.5 秒后手动选择列表会显示出来。

这个体验我觉得挺重要。

自动化不是把用户交给黑盒，而是在黑盒不工作时，把方向盘还给用户。

## 二维码怎么传播

统一 URL 的另一个好处，是二维码终于可以稳定了。

我们现在官网 App 下载区和线下物料都可以使用同一个二维码。

![璞奇 App 统一下载二维码](/assets/images/2026/2026-07-01-one-url-app-download-router-qr.png)

这个二维码背后指向的就是 `https://zendong.com.cn/dl`。

后面如果某个应用市场链接换了，我们改 `DOWNLOAD_LINKS`，重新构建发布 Web 就行。二维码不用换，物料不用重新印。

如果要做投放，也可以在 URL 后加参数。

```text
https://zendong.com.cn/dl?source=booth&campaign=offline
```

nginx 会保留 query，把它带到 Web 页面。页面会展示 `source`、`campaign`、`entry` 等上下文，方便确认入口来源。

不过这块还没有做完。

目前这些 query 只到达 `/dl` 页面，没有继续传到应用商店，也没有落到后端统计。它解决的是「传播入口统一」和「页面上能看到来源」，还不是完整归因系统。

## 现在还不够好的地方

坦率的讲，这个实现还挺实用，但也没有完全自动化。

第一个问题，是 User-Agent 识别永远只能是经验规则。

有些手机浏览器会改 UA，有些内置浏览器会藏掉信息。我们可以覆盖主流厂商，但没法保证每个奇怪环境都识别准确。

第二个问题，是跳转成功与否很难精确判断。

`window.location.href` 发出去以后，浏览器可能打开应用市场，也可能弹窗，也可能被拦截。Web 页面很难拿到一个可靠的成功回执。所以我们只能用 1.5 秒后展示手动列表的方式兜底。

第三个问题，是应用商店归因还没接起来。

现在 `source=booth` 这样的参数只在页面层可见。用户真正跳到 App Store、华为、小米、应用宝之后，后续安装和激活还没有形成完整追踪。这块以后如果要认真做投放，需要接下载页埋点、短链记录、应用首启回传，甚至不同应用市场自己的归因能力。

第四个问题，是厂商链接还要持续维护。

国内安卓生态就是这样。链接、scheme、审核状态、包名、市场页面，都可能变化。统一入口不是一劳永逸，它只是把变化收进一个配置文件里，让变化不要污染二维码和物料。

这已经是一个比较好的边界。

用户只记一个入口。

我们维护一张路由表。

## 小结

最后看，这套方案的关键不是把所有跳转都自己做掉，而是把入口握在自己手里。

用户只看到一个二维码。我们在背后维护一张路由表，能识别就直达，识别不了就让用户选，市场打不开就走应用宝，Android 还有 APK。

对跨端 App 来说，这样的统一下载入口应该尽早做。等物料印完、链接散出去，再回头收口，会麻烦很多。
