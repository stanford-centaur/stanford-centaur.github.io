---
layout: default
title: people
---

{% assign faculty = site.data.people | where: 'position', 'faculty' %}
{% assign staff = site.data.people | where: 'position', 'research_scientist' %}
{% assign postdocs = site.data.people | where: 'position', 'postdoc' %}
{% assign visiting = site.data.people | where: 'position', 'visiting' %}
{% assign phd = site.data.people | where: 'position', 'phd' %}
{% assign rotating = site.data.people | where: 'position', 'rotating' %}
{% assign master = site.data.people | where: 'position', 'master' %}
{% assign bachelor = site.data.people | where: 'position', 'bachelor' %}
{% assign grad = phd | concat: master | concat: bachelor %}

{% assign faculty = faculty | where_exp: 'f', 'f.end == nil' %}
{% assign staff = staff | where_exp: 's', 's.end == nil' %}
{% assign postdocs = postdocs | where_exp: 'p', 'p.end == nil' %}
{% assign visiting = visiting | where_exp: 'p', 'p.end == nil' %}
{% assign grad = grad | where_exp: 'g', 'g.end == nil' %}
{% assign rotating = rotating | where_exp: 'r', 'r.end == nil' %}

<div class="people">

{% if faculty.size != 0 %}
<h2>Faculty</h2>
{% include rows.html items=faculty card="person_card.html" %}
{% endif %}

{% if staff.size != 0 %}
<h2>Research Scientists</h2>
{% include rows.html items=staff card="person_card.html" %}
{% endif %}

{% if postdocs.size != 0 %}
<h2>Postdoctoral Researchers</h2>
{% include rows.html items=postdocs card="person_card.html" %}
{% endif %}

{% if visiting.size != 0 %}
<h2>Visiting Researchers</h2>
{% include rows.html items=visiting card="person_card.html" %}
{% endif %}

{% if grad.size != 0 %}
<h2>Graduate Students</h2>
{% include rows.html items=grad card="person_card.html" %}
{% endif %}


{% if rotating.size != 0 %}
<h2>Rotating Graduate Students</h2>
{% include rows.html items=rotating card="person_card.html" %}
{% endif %}

</div>
