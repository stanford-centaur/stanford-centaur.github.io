---
layout: default
title: news
---

<div id="news-items">
  {% assign sorted_news_items = site.data.news_items | sort: 'date' | reverse %}
  {% for item in sorted_news_items %}
    <div class="news-item">
      <h2>{{ item.title }}</h2>
      <p>{{ item.date | date_to_string }}</p>
      <p>{{ item.excerpt }}</p>
      {% for link in item.urls %}
        <a href="{{ link.url }}">{{ link.label }}</a><br>
      {% endfor %}
      <br>
    </div>
  {% endfor %}
</div>


