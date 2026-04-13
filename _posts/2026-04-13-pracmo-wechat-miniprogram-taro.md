---
title: "从 Web 到微信：璞奇小程序的技术选型与踩坑实录"
date: 2026-04-13
categories:
  - 技术
tags:
  - pracmo
  - wechat-miniprogram
  - taro
  - react
  - monorepo
  - 璞奇 app
layout: post
hero_image_ai_generated: true
image_prompt: "Abstract technical illustration, web browser and WeChat mini program connected by data flow, monorepo packages and one API, flat vector, soft blue-green on light gray, 16:9, no text"
image_prompt_file: "assets/prompt/2026-04-13/2026-04-13-pracmo-wechat-miniprogram-taro.txt"
---

> "操千曲而后晓声，观千剑而后识器。" — 《文心雕龙·知音》

![首图](/assets/images/2026/2026-04-13-pracmo-wechat-miniprogram-taro.png)

做教育类产品，如果只盯浏览器和 App，会漏掉一大块日常流量。**微信小程序**离用户最近，搜一搜、聊天里顺手打开、用完即走，都是 Web 很难单独吃下的场景。把同一套流炼能力迁到小程序，本质是在**扩大用户覆盖**，让「想练的人」不必先装 App 或找电脑。

这篇记录璞奇仓库里，围绕 `pracmo-website` 的工程协作方式，为**微信小程序**选型 Taro、接入 `@pracmo/shared`、与既有 API 对齐的过程，以及中间踩过的依赖与工具坑。不是教程抄书，是一边做一边记。

## 我们在做什么

璞奇（Pracmo）长期以 Web（`pracmo-website`）和多端 App 为主阵地。要在微信里完成同一套「流炼」体验，需要一条能长期维护的小程序链路。目标可以压成三句，**和现有后端契约对齐**，**和现有 monorepo 协作方式对齐**，**能复用的就复用**，而不是再起一个只给小程序用的孤岛仓库。

## 来龙去脉：为什么是现在、为什么这样拆

业务上，小程序是触达与转化的重要场景，登录、列表、练习播放要和 Web 一致，避免同一账号两套逻辑。工程上，仓库已经是 **monorepo**，Web、共享包、后端并列。把小程序放进同一 workspace，可以让 API 契约、类型、常量与 `@pracmo/shared` 同源，减少「Web 改了字段、小程序下周才同步」的撕裂。

技术选型上，团队熟悉 React 与 TypeScript，**Taro** 能用接近 Web 的方式组织页面，再编译成微信小程序，比从零维护一套原生小程序栈，更贴合现有前端习惯。

## Taro 项目说明（`pracmo-miniapp`）

### Taro 在本仓库里的角色

**Taro** 是京东开源的多端统一开发框架，用 React 或 Vue 写业务，再编译到各端目标。当前选型是 **Taro 4 + React + Webpack5**，构建目标为 **微信小程序（`weapp`）**，与 `pracmo-website` 共用后端与 `@pracmo/shared` 契约，不维护第二套协议。

### 目录与产物（简表）

| 路径或配置 | 说明 |
|------------|------|
| `config/index.ts` | Taro 配置，`sourceRoot: 'src'`，`outputRoot: 'dist'`，`framework: 'react'`，`compiler: 'webpack5'`，插件 `@tarojs/plugin-platform-weapp`。 |
| `src/` | 页面、组件、HTTP 与微信登录适配、`AuthContext` 等。`app.config.ts` 声明路由。 |
| `dist/` | `taro build --type weapp` 产出，微信开发者工具里 `miniprogramRoot` 指向这里（以工程配置为准）。 |
| `project.config.json` | 开发者工具工程配置。本地可用 `project.private.config.json` 覆盖 AppID，勿把敏感信息提交 Git。 |

### 与 monorepo 的衔接

根目录 `package.json` 使用 **npm workspaces**，把 `pracmo-miniapp` 和 `packages/*`、`pracmo-website` 放在同一工作区。构建顺序是先编译 `@pracmo/shared`，再编小程序。根目录脚本示例是 `npm run build:miniapp`（内部是 `build:shared` 加上子包的 `build:weapp`）。日常开发可用 `npm run dev:miniapp`，等价于在 `pracmo-miniapp` 里跑 **`taro build --type weapp --watch`**，保存后增量编译，配合开发者工具刷新。

### 运行时和构建期约定

小程序里没有 Node 式的 `process`，业务代码里**不要**直接写 `process.env`。环境相关变量用 Taro 的 **`defineConstants`** 在构建期注入，例如 API 基地址、调试登录开关，否则真机会遇到 `ReferenceError: process is not defined`。微信能力（登录 `code`、存储、路由）收在小程序适配层，领域与 HTTP 契约尽量来自 `@pracmo/shared`，与 Web 对齐。

### 依赖与打包（workspace 特有问题）

在 npm workspaces 下，`react` 可能被解析到不同物理路径，Webpack 分 chunk 后容易出现**多份 React**，表现成 Hooks 异常，例如 `useState` 读到 null。做法是在 `mini.webpackChain` 里给 **`react`、`scheduler`、`react-reconciler`** 以及 **`react/jsx-runtime`** 配 **`resolve.alias`**，统一到当前包解析出的一份目录。根 **`package.json` 的 `overrides`** 把 `react`、`react-dom` 固定到与 Taro 4 匹配的 **React 18.x**，并和 **lockfile** 对齐，避免子目录单独 `npm install` 又把版本扯歪。

## 架构方案（四层）

1. **客户端**，Taro + React，独立目录 `pracmo-miniapp`，目标是微信小程序，路由由 Taro 约定式配置管理。  
2. **共享层**，`@pracmo/shared` 放 contracts、API 封装和平台无关逻辑，编译成 JS 后，由小程序侧注入 Taro 网络层、存储、微信登录。  
3. **后端**，沿用与 Web 相同的 HTTP API，只做微信 `code` 登录和会话存储等宿主相关差异。  
4. **工程约束**，workspaces + 根目录 overrides，避免多份互不兼容的 `react`。

整体是「共享契约、多端适配、单后端」，小程序是新交付渠道，不是新业务孤岛。

## 实施里容易忽略的点

登录与会话方面，首屏常要**恢复登录态**（本地 token 再拉账号信息），要配超时和失败提示，避免长时间白屏。微信登录依赖**真实 AppID** 和**合法域名**配置，能编译通过不等于能登录。与 Web 的边界是，UI 可以不同，接口语义、错误码和数据模型要和 `pracmo-website` 依赖的后端一致，否则客服和运营会被两端不一致拖垮。

## 踩坑记录（现象、原因、对策）

**1）开发者工具里游客模式与 `webapi_getwxaasyncsecinfo:fail`**  
现象是 `SystemError`、安全相关接口失败。原因多是**游客 AppID** 或工具侧模拟，和业务里有没有调某个接口不一定对应。对策是换成公众平台登记的小程序 AppID，工具里尽量不用灰度基础库瞎试，网络代理和 VPN 先关掉对照，必要时真机预览。

**2）React 大版本与 Taro 不一致，白屏、Minified React error #31**  
Taro 4 的 React 插件链路面向 **React 18**。workspace 里若出现 **React 19**，会和 `react-reconciler` 不匹配。对策是子包锁 **18.x**，根目录 overrides，并修正 **package-lock** 里嵌套的 `react`，不要只在 `package.json` 里改数字。

**3）`Cannot read property 'useState' of null`**  
本质是 **`ReactCurrentDispatcher` 为空**，常见原因是产物里多路径解析出多份 `react`。对策是前面的 **webpack alias**，重装依赖后**整包重编**，不要用旧的 `dist` 糊弄。

**4）lock 与磁盘 `node_modules` 不一致**  
子目录执行 **`npm install react@…`** 可能把版本写回，或 lock 里嵌套条目没更新。对策是以**根目录** `npm install` 为准，必要时手修 lock 再装，团队约定子 workspace 不要随便单升 `react`。

## 小结

小程序不是副本工程，而是 monorepo 里的一条渠道。Taro 负责「用 React 写、产出微信小程」，`@pracmo/shared` 负责「与 Web 同源契约」，AppID、基础库、React 单实例、lockfile 决定能不能稳定跑。报错要分层，工具 SDK 的 `getwxaasyncsecinfo` 和业务 JS 不是一类问题，白屏先看 AppService 里**第一条业务栈**，再对依赖和产物。

从 `pracmo-website` 代表的前后端协作方式出发，选 **Taro + 共享包 + 既有 API** 可以长期多人协作。真正费时间的往往是依赖图、打包解析和微信工具环境对齐，把版本锁定、Webpack alias、私有 AppID 和统一构建入口写进规范，后面迭代会省很多来回。

> **璞奇启示**
>
> 1. 学习类产品要**扩大用户覆盖**，微信小程是高频入口之一，与 Web、App 并行能减少「想练却卡在安装」的流失。  
> 2. 同一套练习逻辑，用共享契约加各端适配，比各端各写协议更利于把「练会」闭环做稳，也方便用 AI 辅助生成与批改练习时保持一致性。
