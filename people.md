---
layout: default
title: people
---

{% assign faculty = site.data.people | where: 'position', 'faculty' %}
{% assign staff = site.data.people | where: 'position', 'research_scientist' %}
{% assign postdocs = site.data.people | where: 'position', 'postdoc' %}
{% assign phd = site.data.people | where: 'position', 'phd' %}
{% assign master = site.data.people | where: 'position', 'master' %}
{% assign grad = phd | concat: master %}

{% assign faculty = faculty | where_exp: 'f', 'f.end == nil' %}
{% assign staff = staff | where_exp: 's', 's.end == nil' %}
{% assign postdocs = postdocs | where_exp: 'p', 'p.end == nil' %}
{% assign grad = grad | where_exp: 'g', 'g.end == nil' %}

<div class="people">

{% if faculty != blank %}
<h2>Faculty</h2>
<div class="row">
{% for p in faculty %}
<div class="col">
<a href="{{ p.website }}">
  <img src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
<br/>
<b><a href="{{ p.website }}">{{ p.name }}</a></b>
<br/>
{{ p.title }}
</div>
{% endfor %}
</div>
{% endif %}

{% if staff != blank %}
<h2>Research Scientists</h2>
<div class="row">
{% for p in staff %}
<div class="col">
<a href="{{ p.website }}">
  <img src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
<br/>
<b><a href="{{ p.website }}">{{ p.name }}</a></b>
<br/>
{{ p.title }}
</div>
{% endfor %}
</div>
{% endif %}

{% if postdocs != blank %}
<h2>Postdoctoral Researchers</h2>
<div class="row">
{% for p in postdocs %}
<div class="col">
<a href="{{ p.website }}">
  <img src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
<br/>
<b><a href="{{ p.website }}">{{ p.name }}</a></b>
<br/>
{{ p.title }}
</div>
{% endfor %}
</div>
{% endif %}

{% if grad != blank %}
<h2>Graduate Students</h2>
<div class="row">
{% for p in grad %}
<div class="col">
<a href="{{ p.website }}">
  <img src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
<br/>
<b><a href="{{ p.website }}">{{ p.name }}</a></b>
<br/>
{{ p.title }}
</div>
{% endfor %}
</div>
{% endif %}

</div>
