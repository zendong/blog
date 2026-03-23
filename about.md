---
layout: default
title: 关于
permalink: /about/
---

<div class="about">
  <h1 class="page-title">关于</h1>

  <div class="about-content">
    <p class="about-intro">这里是璞奇的创业记录博客，记录关于 AI、技术探索、产品设计、创业经历等方面的思考与探索。</p>


    <div class="about-links">
      <a href="{{ site.puqi_website }}" target="_blank" rel="noopener" class="about-link primary">
        <img src="{{ "/assets/app/LOGO.png" | relative_url }}" alt="璞奇" class="about-logo">
        <span>璞奇</span>
      </a>
      <a href="https://github.com/orgs/zendong/repositories" target="_blank" rel="noopener" class="about-link">
        <svg class="about-icon" viewBox="0 0 16 16" width="16" height="16"><path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28.15-.68.52-.01.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>
        <span>GitHub</span>
      </a>
    </div>

    <div class="about-footer">
      <p>可以通过 <a href="{{ "/feed.xml" | relative_url }}">RSS</a> 订阅本博客的更新。</p>
    </div>
  </div>
</div>

<style>
.about {
  max-width: 100%;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--color-border);
}

.about-content {
  font-size: 1.0625rem;
  line-height: 1.8;
}

.about-intro {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-xl);
}

.about-links {
  display: flex;
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-xl);
}

.about-link {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-xs) var(--spacing-sm);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  color: var(--color-text);
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--color-primary);
    text-decoration: none;
  }

  &.primary {
    color: var(--color-accent);

    &:hover {
      background-color: rgba(249, 115, 22, 0.1);
    }

    .about-logo {
      border-radius: 4px;
    }
  }

  .about-logo {
    height: 24px;
    width: auto;
    border-radius: 4px;
  }

  .about-icon {
    fill: currentColor;
  }
}

.about-footer {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-size: 0.9375rem;

  a {
    color: var(--color-primary);

    &:hover {
      color: var(--color-primary-dark);
    }
  }
}
</style>
