# GitHub Pages 与静态博客 — 实践要点

在为本仓库或其它 GitHub Pages 项目写稿时，代理应默认遵守下列约束；若项目已有文档，以项目为准。

## URL 与路径

- **User/Org 站点**：`https://<user>.github.io/` 根路径；**Project 站点**：`https://<user>.github.io/<repo>/`，子路径下资源必须用**根相对或仓库相对**链接，避免本地能开、线上 404。
- Markdown 内图片：优先 `![alt](./assets/...)` 或与站点配置的 `baseurl` 一致的路径（Jekyll 常用 `{{ site.baseurl }}`）。
- **大小写**：GitHub Pages 构建在 Linux 上运行，文件名与路径**区分大小写**。

## Jekyll（默认引擎）

- 文章常用 `_posts/YYYY-MM-DD-slug.md`；需合法 **YAML front matter**（`layout`、`title`、`date` 等）。
- 以 `_` 开头的目录/文件可能被特殊处理；无关内容不要放在 Jekyll 会吞掉的约定路径里。
- 本地若用不同 Ruby/Jekyll 版本，可能与 Actions 不一致；重要布局应在 CI 或与 README 中版本对齐。

## 纯静态（无 Jekyll）

- 在仓库设置中可关闭 Jekyll（例如根目录放 `.nojekyll`），避免 `node_modules` 等被误处理。
- 构建产物在 `docs/` 或 `gh-pages` 分支时，注意**只提交生成结果**还是**源码 + Action 构建**，与仓库 README 一致。

## 资源与性能

- 图片：**WebP/AVIF** 更省流量；大图需压缩，避免单文件过大导致克隆与加载慢。
- **Git LFS**：若用 LFS 存图，确认 Pages 构建流程能拉到 LFS 对象（部分简易流程不会）。
- **外链图**：依赖第三方可用性；长期存档建议落盘到仓库 `assets/`。

## 安全与合规

- 不在仓库中提交 **API Key**；文生图密钥应走 **GitHub Secrets** 或本机密钥管理，skill 只描述「在本地/CI 中调用」，不把密钥写进 Markdown。
- 用户生成内容：注意版权与引用来源；新闻图须可追溯许可。

## CI / 自动化

- 若用 GitHub Actions 部署：检查触发分支、`permissions: contents: read` / `write`、以及 `GITHUB_TOKEN` 推送 Pages 的配置。
- 构建失败时常见原因：front matter 语法错误、禁止插件、子模块未递归检出。

## SEO 与分享（可选）

- `title`、`description`、规范链接（canonical）若主题支持则补齐；Open Graph 图可用首图或单独 square 图。
