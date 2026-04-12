---
title: "我是如何从零搭建这个博客的"
date: 2026-03-23
categories:
  - 技术
tags:
  - github-pages
  - jekyll
  - github-actions
  - 博客搭建
  - 自动化部署
layout: post
image_prompt: "A clean minimalist workspace with a laptop displaying code and a glowing GitHub logo, floating documentation files and git branches around it, soft blue and orange accent colors, modern flat design illustration, 16:9 aspect ratio, digital art style showing developer workflow and version control concepts"
image_prompt_file: "assets/prompt/2026-03-23/how-i-built-this-blog.txt"
hero_image_ai_generated: true
---

> 工欲善其事，必先利其器。——《论语·卫灵公》

![博客搭建过程图]({{ "/assets/images/2026/2026-03-23-how-i-built-this-blog.png" | relative_url }})

## 一、为什么选择 GitHub Pages

做技术博客的选择很多：WordPress、Medium、知乎、CSDN。选择 GitHub Pages 有几个实际的原因：

**数据在自己手里。** 平台会倒闭、改算法、封号。GitHub 只要微软不倒就会在。

**写作体验纯粹。** Markdown + Git，完全掌控内容和版本。

**访问稳定。** GitHub Pages 依托全球 CDN，速度和稳定性有保障。

**成本为零。** 免费额度完全够用。

最终方案是 **GitHub Pages + Jekyll**。

---

## 二、技术方案：Jekyll + GitHub Actions

### 2.1 Jekyll

Jekyll 是 GitHub Pages 默认支持的静态网站生成器，原生支持 Markdown，内置模板引擎，生态成熟。

项目结构：

```
blog/
├── _posts/          # 文章
├── _layouts/        # 模板
├── _includes/       # 组件
├── _sass/           # 样式
├── assets/          # 静态资源
├── _config.yml      # 配置
└── Makefile         # 构建脚本
```

### 2.2 GitHub Actions 自动化部署

每次 `git push` 自动触发构建和部署：

```yaml
name: Deploy GitHub Pages
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
    permissions:
      contents: read
      pages: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true
      - run: |
          bundle install
          bundle exec jekyll build --baseurl "${{ github.event.repository.name }}"
      - uses: actions/upload-pages-artifact@v3
      - uses: actions/deploy-pages@v4
```

---

## 三、本地验证

`Makefile` 简化了本地构建：

```makefile
build:
	bundle exec jekyll build

serve:
	bundle exec jekyll serve --watch

clean:
	rm -rf _site
```

执行 `make build`，Jekyll 在本地生成 `_site` 目录。确认无误后再 push。

---

## 四、遇到的问题

技术方案确定后，实际动手时还是遇到了一些具体问题。

### 4.1 Sass 编译

**现象**：本地 CSS 正常，GitHub Pages 构建后 CSS 变成原始 Sass 代码。

**原因**：GitHub Pages 的 Jekyll 3.10.0 内置 Sass 转换器不支持 `@use` 语法。

**解决**：改用 `@import`。

```scss
// 错误
@use "variables";

// 正确
@import "variables";
```

### 4.2 Actions 部署权限

**现象**：deploy-pages action 报错 `Unable to get ACTIONS_ID_TOKEN_REQUEST_URL`。

**原因**：action 需要 `id-token: write` 权限，workflow 中未声明。

**解决**：添加 permissions 块。

### 4.3 CNAME 文件

**现象**：自定义域名 `blog.zendong.com.cn` 无法生效。

**原因**：`_site` 是构建产物，不会自动包含 CNAME 文件。

**解决**：在 workflow 中手动复制。

```yaml
- name: 复制 CNAME
  run: cp CNAME _site/CNAME
```

### 4.4 循环符号链接

**现象**：Actions 报错 `Too many levels of symbolic links`。

**原因**：存在一个指向自身的符号链接。

**解决**：删除该链接。

---

## 五、样式统一

细节上的调整：

**分类标签**：首页和详情页的 category 标签样式统一为纯色背景。

**关于页面**：官网按钮改为简洁的 logo + 文字格式，与 footer 一致。

**GitHub 链接**：统一指向组织仓库页面。

---

## 六、展望

博客搭建是起点，内容是核心。接下来会持续更新：

- **AI 与学习**：AI 重塑教育，璞奇 APP 产品思考
- **技术探索**：智能体工作流、Cursor 技巧、Claude Code 实践
- **创业记录**：产品从 0 到 1，踩坑复盘

博客本身也在迭代：RSS 订阅、SEO 优化、相关文章推荐……

---

## 璞奇启示

搭建博客是一次最小可行产品的实践。

**快速验证优于完美设计。** 先让博客跑起来，再迭代优化。GitHub Pages 提供了零成本的托管方案，降低了试错门槛。

**自动化减少心智负担。** 写完文章只需要 `git push`，剩下的交给 Actions。可以专注在写作本身。

**复盘是进步的方式。** 踩过的坑、解决的方案，都是成长的养分。记录下来，既是给自己的复盘，也是给他人的参考。

---

## 信息说明

- Jekyll 官方文档：https://jekyllrb.com/
- GitHub Pages 文档：https://docs.github.com/en/pages
- GitHub Actions 文档：https://docs.github.com/en/actions
