---
layout: default
title: blog
---

{% assign combined_posts = site.posts | concat: site.data.external_blog_posts %}
{% assign sorted_posts = combined_posts | sort: 'date' | reverse %}

{% for post in sorted_posts %}
  <h2><a href="{{ post.url }}" {% if post.external %}target="_blank"{% endif %}>{{ post.title }}</a></h2>
  <p>by {{ post.author }}, {{ post.date | date_to_string }} <p> </p> {{ post.excerpt | strip_html }}
  <a href="{{ post.url }}" class="read-more" {% if post.external %}target="_blank"{% endif %}>Read More</a> </p>
{% endfor %}
