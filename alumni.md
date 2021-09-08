---
layout: default
title: alumni
---

{% assign faculty = site.data.people | where: 'position', 'faculty' %}
{% assign staff = site.data.people | where: 'position', 'research_scientist' %}
{% assign postdocs = site.data.people | where: 'position', 'postdoc' %}
{% assign phd = site.data.people | where: 'position', 'phd' %}
{% assign master = site.data.people | where: 'position', 'master' %}
{% assign grad = phd | concat: master %}

{% assign faculty = faculty | where_exp: 'f', 'f.end != nil' %}
{% assign staff = staff | where_exp: 's', 's.end != nil' %}
{% assign postdocs = postdocs | where_exp: 'p', 'p.end != nil' %}
{% assign grad = grad | where_exp: 'g', 'g.end != nil' %}

<div class="alumni">
{% if faculty != empty %}
<h2>Former Faculty</h2>
{% assign years = faculty | map: 'end' | uniq | sort | reverse %}
{% for year in years %}
{% assign f = faculty | where: 'end', year %}
{% for p in f %}
<div class="col">
<a href="{{ p.website }}">
  <img style="vertical-align:middle" src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
&nbsp;<b><a href="{{ p. website}}">{{ p.name }}</a></b> ({{ p.start }}&ndash;{{ p.end}}){% if p.now %}, {{ p. now }}{% endif %}
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
<a href="{{ p.website }}">
  <img style="vertical-align:middle" src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
&nbsp;<b><a href="{{ p. website}}">{{ p.name }}</a></b> ({{ p.start }}&ndash;{{ p.end}}){% if p.now %}, {{ p. now }}{% endif %}
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
<a href="{{ p.website }}">
  <img style="vertical-align:middle" src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
&nbsp;<b><a href="{{ p. website}}">{{ p.name }}</a></b> ({{ p.start }}&ndash;{{ p.end}}){% if p.now %}, {{ p. now }}{% endif %}
</div>
{% endfor %}
{% endfor %}
{% endif %}

{% if grad != empty %}
<h2>Former Graduate Students</h2>
{% assign years = grad | map: 'end' | uniq | sort | reverse %}
{% for year in years %}
{% assign g = grad | where: 'end', year %}
{% for p in g %}
<div class="col">
<a href="{{ p.website }}">
  <img style="vertical-align:middle" src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
&nbsp;<b><a href="{{ p. website}}">{{ p.name }}</a></b> ({{ p.start }}&ndash;{{ p.end}}){% if p.now %}, {{ p. now }}{% endif %}
</div>
{% endfor %}
{% endfor %}
{% endif %}
</div>
