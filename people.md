---
layout: default
title: people
---

# People

<div class="people">

<h2>Faculty</h2>

<div class="row">
{% for p in site.data.people.faculty %}
<div class="col" style="text-align:center;">
<a href="{{ p.website }}">
  <img src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
<br/>
<b>{{ p.name }}</b>
<br/>
{{ p.title }}
</div>
{% endfor %}
</div>

<h2>Research Scientists</h2>

<div class="row">
{% for p in site.data.people.staff %}
<div class="col" style="text-align:center;">
<a href="{{ p.website }}">
  <img src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
<br/>
<b>{{ p.name }}</b>
<br/>
{{ p.title }}
</div>
{% endfor %}
</div>

<h2>Postdoctoral Researchers</h2>

<div class="row">
{% for p in site.data.people.postdocs %}
<div class="col" style="text-align:center;">
<a href="{{ p.website }}">
  <img src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
<br/>
<b>{{ p.name }}</b>
<br/>
{{ p.title }}
</div>
{% endfor %}
</div>

<h2>Graduate Students</h2>

<div class="row">
{% for p in site.data.people.students %}
<div class="col" style="text-align:center;">
<a href="{{ p.website }}">
  <img src="img/people/{{ p.img }}" alt="{{ p.name }}"/>
</a>
<br/>
<b>{{ p.name }}</b>
<br/>
{{ p.title }}
</div>
{% endfor %}
</div>

</div>
