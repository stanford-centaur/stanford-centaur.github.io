---
layout: default
title: tools
---
{% assign categories = site.data.tools.tools
  | map: 'category' | uniq | sort %}

{% for category in categories %}
{% assign cat = site.data.tools.categories | where_exp: 'c', 'c.id == category' %}
# {{ cat[0].name }}
{% assign tools = site.data.tools.tools | where_exp: 't', 't.category == category' %}
{% include rows.html items=tools card="tool_card.html" %}
{% endfor %}
