---
layout: default
title: Blog
---

{% for post in site.posts %}
  <h2><a href="{{ post.url }}">{{ post.title }}</a></h2>
  <p>{{ post.date | date_to_string }} <p> </p> {{ post.excerpt | strip_html }}
    <a href="{{ post.url }}" class="read-more">Read More</a> </p>
{% endfor %}
