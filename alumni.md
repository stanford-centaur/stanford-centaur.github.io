---
layout: default
title: alumni
---

{% assign faculty = site.data.people | where: 'position', 'faculty' %}
{% assign staff = site.data.people | where: 'position', 'research_scientist' %}
{% assign postdocs = site.data.people | where: 'position', 'postdoc' %}
{% assign phd = site.data.people | where: 'position', 'phd' %}
{% assign master = site.data.people | where: 'position', 'master' %}

{% assign faculty = faculty | where_exp: 'p', 'p.end != nil' %}
{% assign staff = staff | where_exp: 'p', 'p.end != nil' %}
{% assign postdocs = postdocs | where_exp: 'p', 'p.end != nil' %}
{% assign phd = phd | where_exp: 'p', 'p.end != nil' %}
{% assign master = master | where_exp: 'p', 'p.end != nil' %}

<div class="alumni">
{% if faculty != empty %}
<h2>Former Faculty</h2>
{% assign years = faculty | map: 'end' | uniq | sort | reverse %}
{% for year in years %}
{% assign f = faculty | where: 'end', year %}
{% for p in f %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
<img style="vertical-align:middle" src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
</a>
{% else %}
<img style="vertical-align:middle" src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% endif %}
&nbsp;<b>{% if p.website %}<a href="{{ p. website}}">{{ p.name }}</a>{% else %}{{ p.name }}{% endif %}</b> ({{ p.start }}&ndash;{{ p.end}}){% if p.now %}, {{ p. now }}{% endif %}
</div>
{% endfor %}
{% endfor %}
{% endif %}

{% if staff != empty %}
<h2>Former Research Scientists</h2>
{% assign years = staff | map: 'end' | uniq | sort | reverse %}
{% for year in years %}
{% assign st = staff | where: 'end', year %}
{% for p in st %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
  <img style="vertical-align:middle" src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
</a>
{% else %}
  <img style="vertical-align:middle" src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% endif %}
&nbsp;<b>{% if p.website %}<a href="{{ p. website}}">{{ p.name }}</a>{% else %}{{ p.name }}{% endif %}</b> ({{ p.start }}&ndash;{{ p.end}}){% if p.now %}, {{ p. now }}{% endif %}
</div>
{% endfor %}
{% endfor %}
{% endif %}

{% if postdocs != empty %}
<h2>Former Postdoctoral Researchers</h2>
{% assign years = postdocs | map: 'end' | uniq | sort | reverse %}
{% for year in years %}
{% assign pd = postdocs | where: 'end', year %}
{% for p in pd %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
{% endif %}
<img style="vertical-align:middle" src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% if p.website %}
</a>
{% endif %}
&nbsp;<b>{% if p.website %}<a href="{{ p.website }}">{{ p.name }}</a>{% else %}{{ p.name }}{% endif %}</b> ({{ p.start }}&ndash;{{ p.end}}){% if p.now %}, {{ p. now }}{% endif %}
</div>
{% endfor %}
{% endfor %}
{% endif %}

{% if phd != empty %}
<h2>Former Ph.D. Students</h2>
{% assign years = phd | map: 'end' | uniq | sort | reverse %}
{% for year in years %}
{% assign g = phd | where: 'end', year %}
{% for p in g %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
  <img style="vertical-align:middle" src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
</a>
{% else %}
  <img style="vertical-align:middle" src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% endif %}
&nbsp;<b>{% if p.website %}<a href="{{ p. website}}">{{ p.name }}</a>{% else %}{{ p.name }}{% endif %}</b> ({{ p.start }}&ndash;{{ p.end}}){% if p.now %}, {{ p. now }}{% endif %}
</div>
{% endfor %}
{% endfor %}
{% endif %}

{% if master != empty %}
<h2>Former Masters Students</h2>
{% assign years = master | map: 'end' | uniq | sort | reverse %}
{% for year in years %}
{% assign g = master | where: 'end', year %}
{% for p in g %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
  <img style="vertical-align:middle" src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
</a>
{% else %}
  <img style="vertical-align:middle" src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% endif %}
&nbsp;<b>{% if p.website %}<a href="{{ p. website}}">{{ p.name }}</a>{% else %}{{ p.name }}{% endif %}</b> ({{ p.start }}&ndash;{{ p.end}}){% if p.now %}, {{ p. now }}{% endif %}
</div>
{% endfor %}
{% endfor %}
{% endif %}
</div>
