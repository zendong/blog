# 璞奇观察

探索AI、记录创业经历与思考

![LOGO](assets/app/LOGO.svg)

## 本地开发

### 环境要求

- Ruby 3.2+
- Bundler
- Make (可选，用于简化命令)

### 快速开始

```bash
# 使用 Homebrew 安装 Ruby 3.2
brew install ruby@3.2

# 安装依赖并启动本地服务
make install
make local
```

访问 http://localhost:4000/blog/ 查看效果。

### 手动安装

```bash
# 添加 Ruby 到 PATH
echo 'export PATH="/usr/local/opt/ruby@3.2/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 安装 Jekyll 依赖
bundle install

# 启动本地服务
bundle exec jekyll serve --host 0.0.0.0 --port 4000
```

### Makefile 命令

| 命令 | 说明 |
|------|------|
| `make install` | 安装依赖 |
| `make local` | 启动本地服务器 |
| `make build` | 构建站点到 `_site/` |
| `make clean` | 清理生成的文件 |
| `make help` | 显示帮助信息 |

### 构建站点

```bash
bundle exec jekyll build
```

构建后的站点位于 `_site/` 目录。

## 写作

### 创建新文章

在 `_posts/` 目录下创建 Markdown 文件，文件名格式为 `YYYY-MM-DD-title.md`。

Front matter 示例：

```yaml
---
title: "文章标题"
date: 2026-03-23
categories:
  - 技术
tags:
  - tag1
  - tag2
layout: post
---
```

### 文章模板

参考 `_posts/2026-03-21-from-openclaw-skills-to-puqi-app.md`

## 部署

Push 到 `main` 分支后，GitHub Actions 会自动构建并部署到 GitHub Pages。

访问地址：https://zendong.github.io/blog/

## 技术栈

- [Jekyll](https://jekyllrb.com/) - 静态站点生成器
- [GitHub Pages](https://pages.github.com/) - 托管服务
- SCSS - 样式预处理
