---
layout: default
title: tools
---

<div class="row">
{% for t in site.data.tools %}
<div class="col" style="text-align:center;">
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
