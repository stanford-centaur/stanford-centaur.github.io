---
layout: default
title: alumni
---

{% assign faculty = site.data.people.faculty | where: 'active', false %}
{% assign staff = site.data.people.staff | where: 'active', false %}
{% assign postdocs = site.data.people.postdocs | where: 'active', false %}
{% assign grad = site.data.people.grad | where: 'active', false %}

# Alumni

<div class="alumni">
{% if faculty != empty %}
<h2>Former Faculty</h2>
{% endif %}

{% if staff != empty %}
<h2>Former Research Scientists</h2>
{% endif %}

{% if postdocs != empty %}
<h2>Former Postdoctoral Researchers</h2>
{% for p in postdocs %}
<div class="col">
<a href="{{ p.website }}">
  <img style="vertical-align:middle" src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
&nbsp;<b><a href="{{ p. website}}">{{ p.name }}</a></b>{% if p.now %}, {{ p. now }}{% endif %}
</div>
{% endfor %}
{% endif %}

{% if grad != empty %}
<h2>Former Graduate Students</h2>
{% for p in grad %}
<div class="col">
<a href="{{ p.website }}">
  <img style="vertical-align:middle" src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
&nbsp;<b><a href="{{ p. website}}">{{ p.name }}</a></b>{% if p.now %}, {{ p. now }}{% endif %}
</div>
{% endfor %}
{% endif %}
</div>
