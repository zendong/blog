---
layout: default
title: 标签云
permalink: /tags/
---

<div class="tags-page">
  <h1 class="page-title">标签云</h1>

  {% assign all_tags = site.posts | map: 'tags' | join: ',' | split: ',' | uniq | sort %}

  <!-- 标签统计 -->
  <div class="tags-stats">
    <span class="stat-item">共 {{ all_tags.size }} 个标签</span>
    <span class="stat-item">{{ site.posts.size }} 篇文章</span>
  </div>

  <!-- 标签云 -->
  <div class="tags-cloud">
    {% for tag in all_tags %}
    {% assign tag_posts = site.posts | where_exp: "post", "post.tags contains tag" %}
    {% assign count = tag_posts.size %}
    {% if count > 0 %}
    <a href="#{{ tag }}" class="tag-item size-{{ count }}" data-count="{{ count }}">
      {{ tag }}
      <span class="tag-count">{{ count }}</span>
    </a>
    {% endif %}
    {% endfor %}
  </div>

  <!-- 按标签分类的文章列表 -->
  <div class="tags-detail">
    {% for tag in all_tags %}
    {% assign tag_posts = site.posts | where_exp: "post", "post.tags contains tag" %}
    {% if tag_posts.size > 0 %}
    <section class="tag-section" id="{{ tag }}">
      <h2 class="tag-title">
        {{ tag }}
        <span class="tag-post-count">{{ tag_posts.size }} 篇</span>
      </h2>
      <div class="tag-posts">
        {% for post in tag_posts %}
        <article class="tag-post-item">
          <time class="post-date" datetime="{{ post.date | date_to_xmlschema }}">
            {{ post.date | date: "%Y.%m.%d" }}
          </time>
          <a href="{{ post.url | relative_url }}" class="post-title">{{ post.title }}</a>
          {% if post.categories.size > 0 %}
          <span class="post-category">{{ post.categories[0] }}</span>
          {% endif %}
        </article>
        {% endfor %}
      </div>
    </section>
    {% endif %}
    {% endfor %}
  </div>
</div>

<style>
.tags-page {
  max-width: 100%;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--color-border);
}

.tags-stats {
  display: flex;
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.stat-item {
  background-color: var(--color-bg-elevated);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  border: 1px solid var(--color-border);
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-3xl);
  padding: var(--spacing-xl);
  background-color: var(--color-bg-elevated);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--color-border);
}

.tag-item {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-xs);
  padding: var(--spacing-sm) var(--spacing-md);
  background-color: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  color: var(--color-text);
  font-size: 0.9375rem;
  transition: all 0.2s ease;

  &:hover {
    background-color: var(--color-primary);
    color: white;
    border-color: var(--color-primary);
    text-decoration: none;
  }

  .tag-count {
    font-size: 0.75rem;
    background-color: var(--color-bg-code);
    color: var(--color-text-muted);
    padding: 0.125rem 0.375rem;
    border-radius: 10px;
  }

  &:hover .tag-count {
    background-color: rgba(255, 255, 255, 0.2);
    color: white;
  }
}

/* 根据文章数量调整标签大小 */
.tag-item.size-1 { font-size: 0.875rem; }
.tag-item.size-2 { font-size: 1rem; }
.tag-item.size-3,
.tag-item.size-4 { font-size: 1.125rem; font-weight: 500; }
.tag-item.size-5,
.tag-item.size-6,
.tag-item.size-7,
.tag-item.size-8,
.tag-item.size-9,
.tag-item.size-10 { font-size: 1.25rem; font-weight: 600; }

.tags-detail {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2xl);
}

.tag-section {
  scroll-margin-top: 80px;
}

.tag-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);

  .tag-post-count {
    font-size: 0.875rem;
    color: var(--color-text-muted);
    font-weight: 400;
  }
}

.tag-posts {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.tag-post-item {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--color-border-light);

  &:last-child {
    border-bottom: none;
  }
}

.tag-post-item .post-date {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  color: var(--color-text-muted);
  min-width: 90px;
}

.tag-post-item .post-title {
  flex: 1;
  color: var(--color-text);
  font-weight: 500;

  &:hover {
    color: var(--color-primary);
  }
}

.tag-post-item .post-category {
  background-color: var(--color-bg-code);
  color: var(--color-primary);
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

@media (max-width: 640px) {
  .tags-cloud {
    padding: var(--spacing-md);
  }

  .tag-post-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
    padding: var(--spacing-md) 0;
  }

  .tag-post-item .post-date {
    min-width: auto;
  }
}
</style>
