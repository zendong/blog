source "https://rubygems.org"

gem "jekyll", "~> 4.3"

group :jekyll_plugins do
  # GitHub Pages 官方支持的插件
  gem "jekyll-sass-converter", "~> 2.2.0"  # 使用 sassc 而非 sass-embedded
  gem "jekyll-feed"           # RSS/Atom 订阅
  gem "jekyll-sitemap"        # 网站地图
  gem "jekyll-seo-tag"        # SEO 优化
  gem "jekyll-paginate"       # 文章分页
  gem "jekyll-include-cache"  # 包含缓存，提升构建速度

  # 注意：jekyll-minifier 不被 GitHub Pages 支持
  # 压缩功能通过 GitHub Actions 实现
end
