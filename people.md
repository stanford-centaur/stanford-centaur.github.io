---
layout: default
title: people
---

{% assign faculty = site.data.people.faculty | where: 'active', true %}
{% assign staff = site.data.people.staff | where: 'active', true %}
{% assign postdocs = site.data.people.postdocs | where: 'active', true %}
{% assign grad = site.data.people.grad | where: 'active', true %}

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
