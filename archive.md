---
layout: default
title: 文章归档
permalink: /archive/
---

<div class="archive">
  <h1 class="page-title">文章归档</h1>

  {% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}

  {% for year in posts_by_year %}
  <section class="year-section">
    <h2 class="year-title">{{ year.name }}</h2>
    <div class="year-posts">
      {% for post in year.items %}
      <article class="archive-post">
        <time class="post-date" datetime="{{ post.date | date_to_xmlschema }}">
          {{ post.date | date: "%m月%d日" }}
        </time>
        <a href="{{ post.url | relative_url }}" class="post-link">{{ post.title }}</a>
        {% if post.categories.size > 0 %}
        <span class="post-category">{{ post.categories[0] }}</span>
        {% endif %}
      </article>
      {% endfor %}
    </div>
  </section>
  {% endfor %}
</div>

<style>
.archive {
  max-width: 100%;
}

.page-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--color-border);
}

.year-section {
  margin-bottom: var(--spacing-2xl);
}

.year-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: var(--spacing-md);
}

.year-posts {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.archive-post {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  padding: var(--spacing-sm) 0;
  border-bottom: 1px solid var(--color-border-light);
}

.archive-post .post-date {
  font-family: var(--font-mono);
  font-size: 0.875rem;
  color: var(--color-text-muted);
  min-width: 80px;
}

.archive-post .post-link {
  flex: 1;
  color: var(--color-text);
  font-weight: 500;

  &:hover {
    color: var(--color-primary);
  }
}

.archive-post .post-category {
  background-color: var(--color-bg-code);
  color: var(--color-primary);
  padding: 0.125rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

@media (max-width: 640px) {
  .archive-post {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-xs);
    padding: var(--spacing-md) 0;
  }

  .archive-post .post-date {
    min-width: auto;
  }
}
</style>
