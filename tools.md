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
<div class="row">
{% for t in tools %}
<div class="col">
<a href="{{ t.website }}">
  <img src="img/tools/{{ t.logo }}" alt="{{ t.name }}"/>
</a>
<br/>
<b><a href="{{ t.website }}">{{ t.name }}</a></b>
<br/>
{{ t.desc-brief }}
<br/>
<div class="desc">
{{ t.desc-long }}
</div>
<a href="{{ t.github }}" class="btn">View on GitHub</a>
</div>
{% endfor %}
</div>
{% endfor %}
