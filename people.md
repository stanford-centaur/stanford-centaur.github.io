---
layout: default
title: people
---

{% assign faculty = site.data.people | where: 'position', 'faculty' %}
{% assign staff = site.data.people | where: 'position', 'research_scientist' %}
{% assign postdocs = site.data.people | where: 'position', 'postdoc' %}
{% assign visiting = site.data.people | where: 'position', 'visiting' %}
{% assign phd = site.data.people | where: 'position', 'phd' %}
{% assign master = site.data.people | where: 'position', 'master' %}
{% assign bachelor = site.data.people | where: 'position', 'bachelor' %}
{% assign grad = phd | concat: master | concat: bachelor %}

{% assign faculty = faculty | where_exp: 'f', 'f.end == nil' %}
{% assign staff = staff | where_exp: 's', 's.end == nil' %}
{% assign postdocs = postdocs | where_exp: 'p', 'p.end == nil' %}
{% assign visiting = visiting | where_exp: 'p', 'p.end == nil' %}
{% assign grad = grad | where_exp: 'g', 'g.end == nil' %}

<div class="people">

{% if faculty != blank %}
<h2>Faculty</h2>
<div class="row">
{% for p in faculty %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
</a>
{% else %}
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% endif %}
<br/>
<b>{% if p.website %}<a href="{{ p.website }}">{{ p.name }}</a>{% else %}{{ p.name }}{% endif %}</b>
<br/>
{% if p.title %}{{ p.title }}{% endif %}
</div>
{% endfor %}
</div>
{% endif %}

{% if staff != blank %}
<h2>Research Scientists</h2>
<div class="row">
{% for p in staff %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
</a>
{% else %}
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% endif %}
<br/>
<b>{% if p.website %}<a href="{{ p.website }}">{{ p.name }}</a>{% else %}p.name{% endif %}</b>
<br/>
{% if p.title %}{{ p.title }}{% else %}Research Scientist{% endif %}
</div>
{% endfor %}
</div>
{% endif %}

{% if postdocs != blank %}
<h2>Postdoctoral Researchers</h2>
<div class="row">
{% for p in postdocs %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
</a>
{% else %}
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% endif %}
<br/>
<b>{% if p.website %}<a href="{{ p.website }}">{{ p.name }}</a>{% else %}{{ p.name }}{% endif %}</b>
<br/>
Postdoctoral Researcher
</div>
{% endfor %}
</div>
{% endif %}

{% if visiting != blank %}
<h2>Visiting Researchers</h2>
<div class="row">
{% for p in visiting %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
</a>
{% else %}
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% endif %}
<br/>
<b>{% if p.website %}<a href="{{ p.website }}">{{ p.name }}</a>{% else %}{{ p.name }}{% endif %}</b>
<br/>
Visiting Researcher
</div>
{% endfor %}
</div>
{% endif %}

{% if grad != blank %}
<h2>Graduate Students</h2>
<div class="row">
{% for p in grad %}
<div class="col">
{% if p.website %}
<a href="{{ p.website }}">
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
</a>
{% else %}
  <img src="img/people/{% if p.img %}{{ p.img }}{% else %}default.png{% endif %}" alt="{{ p.name }}"/>
{% endif %}
<br/>
<b>{% if p.website %}<a href="{{ p.website }}">{{ p.name }}</a>{% else %}{{ p.name }}{% endif %}</b>
<br/>
{% if p.position == 'phd' %}Ph.D.{% elsif p.position == 'master' %}Masters{% elsif p.position == 'bachelor' %}Bachelors{% endif %} Student
</div>
{% endfor %}
</div>
{% endif %}

</div>
