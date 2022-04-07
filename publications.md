---
layout: default
title: publications
---

{% assign years = site.data.publications.references
  | map: "issued"
  | map: "year"
  | where_exp: 'y', 'y > 2015'
  | uniq | sort | reverse %}

{% assign books = site.data.publications.references
  | where_exp: 'r', "r.type == 'book'" %}
{% assign book_chapters = site.data.publications.references
  | where_exp: 'r', "r.type == 'chapter'" %}
{% assign articles = site.data.publications.references
  | where_exp: 'r', "r.type == 'article-journal'" %}
{% assign papers = site.data.publications.references
  | where_exp: 'r', "r.type == 'paper-conference'" %}
{% assign reports = site.data.publications.references
  | where_exp: 'r', "r.type == 'report'" %}
{% assign theses = site.data.publications.references
  | where_exp: 'r', "r.type == 'thesis'" %}

{% for year in years %}

# {{ year }}

{% assign ybooks = books
  | where_exp: 'r', 'r.issued[0].year == year' %}
{% assign ychapters = book_chapters
  | where_exp: 'r', 'r.issued[0].year == year' %}
{% if ybooks.size > 0 or ychapters.size > 0 %}
## Books and Book Chapters
{% assign months = ybooks
  | map: "issued"
  | map: "month"
  | uniq | sort | reverse %}
{% for month in months %}
{% assign mbooks = ybooks
  | where_exp: 'r', 'r.issued[0].month == month' %}
{% for item in mbooks %}
{% capture title %}{% assign t = item.title | split: ' ' %}{% for word in t %}{{ word | capitalize }} {% endfor %}{% endcapture %}
{% if item.url %}[{{ title }}]({{ item.url }}){% else %}{{ title }} {% endif %}. Edited by {% for editor in item.editor %}{% if item.editor.size > 1 %}{% if forloop.last == true %} and {% elsif forloop.first == false %}, {% endif %}{% endif %}{{ editor.given }} {{ editor.family }}{% endfor %}. {% if item.collection-title %}{{ item.collection-title }},{% endif %}{% if item.volume %} vol. {{ item.volume }},{% endif %} {{ item.publisher }}. ({{ item.issued[0].year}})
{% endfor %}
{% endfor %}
{% assign months = ychapters
  | map: "issued"
  | map: "month"
  | uniq | sort | reverse %}
{% for month in months %}
{% assign mbooks = ychapters
  | where_exp: 'r', 'r.issued[0].month == month' %}
{% for item in mbooks %}
{% capture title %}{% assign t = item.title | split: ' ' %}{% for word in t %}{{ word | capitalize }} {% endfor %}{% endcapture %}
{% if item.url %}[{{ title }}]({{ item.url }}){% else %}{{ title }} {% endif %}. {% for author in item.author %}{% if item.author.size > 1 %}{% if forloop.last == true %} and {% elsif forloop.first == false %}, {% endif %}{% endif %}{{ author.given }} {{ author.family }}{% endfor %}. {% if item.container-title %} In {{ item.container-title }},{% endif %}{% if item.volume %} vol. {{ item.volume }},{% endif %} {% if item.collection-title %}{{ item.collection-title }},{% endif %} {% if item.editor %}({% for editor in item.editor %}{% if item.editor.size > 1 %}{% if forloop.last == true %} and {% elsif forloop.first == false %}, {% endif %}{% endif %}{{ editor.given }} {{ editor.family }}{% endfor %}, eds.),{% endif %}{% if item.page %} pp. {{ item.page }},{% endif %} {{ item.publisher }}. ({{ item.issued[0].year}})
{% endfor %}
{% endfor %}
{% endif %}

{% assign yarticles = articles
  | where_exp: 'r', 'r.issued[0].year == year' %}
{% if yarticles.size > 0 %}
## Journal Articles
{% assign months = yarticles
  | map: "issued"
  | map: "month"
  | uniq | sort | reverse %}
{% for month in months %}
{% assign marticles = yarticles
  | where_exp: 'r', 'r.issued[0].month == month' %}
{% for item in marticles %}
{% capture title %}{% assign t = item.title | split: ' ' %}{% for word in t %}{{ word | capitalize }} {% endfor %}{% endcapture %}
{% if item.url %}[{{ title }}]({{ item.url }}){% else %}{{ title }} {% endif %}. {% for author in item.author %}{% if item.author.size > 1 %}{% if forloop.last == true %} and {% elsif forloop.first == false %}, {% endif %}{% endif %}{{ author.given }} {{ author.family }}{% endfor %}. {% if item.container-title %} In {{ item.container-title }},{% endif %}{% if item.volume %} vol. {{ item.volume }},{% endif %} {% if item.collection-title %}{{ item.collection-title }},{% endif %} {% if item.page %} pp. {{ item.page }},{% endif %} {{ item.publisher }}. ({{ item.issued[0].year}})
{% endfor %}
{% endfor %}
{% endif %}

{% assign ypapers = papers
  | where_exp: 'r', 'r.issued[0].year == year' %}
{% if ypapers.size > 0 %}
## Conference Papers
{% assign months = ypapers
  | map: "issued"
  | map: "month"
  | uniq | sort | reverse %}
{% for month in months %}
{% assign mpapers = ypapers
  | where_exp: 'r', 'r.issued[0].month == month' %}
{% for item in mpapers %}
{% if item.url %}[{{ item.title }}]({{ item.url }}){% else %}{{ item.title }} {% endif %}. {% for author in item.author %}{% if item.author.size > 1 %}{% if forloop.last == true %} and {% elsif forloop.first == false %}, {% endif %}{% endif %}{{ author.given }} {{ author.family }}{% endfor %}. {% if item.container-title %} In {{ item.container-title }},{% endif %}{% if item.volume %} vol. {{ item.volume }},{% endif %} {% if item.collection-title %}{{ item.collection-title }},{% endif %} {% if item.page %} pp. {{ item.page }},{% endif %} {{ item.publisher }}. ({{ item.issued[0].year}})
{% if item.award %}<br/><span class="awards"><strong>{{ item.award }}</strong></span>{% endif %}
{% endfor %}
{% endfor %}
{% endif %}

{% assign yreports = reports
  | where_exp: 'r', 'r.issued[0].year == year' %}
{% if yreports.size > 0 %}
## Reports
{% assign months = yreports
  | map: "issued"
  | map: "month"
  | uniq | sort | reverse %}
{% for month in months %}
{% assign mreports = yreports
  | where_exp: 'r', 'r.issued[0].month == month' %}
{% for item in mreports %}
{% capture title %}{% assign t = item.title | split: ' ' %}{% for word in t %}{{ word | capitalize }} {% endfor %}{% endcapture %}
{% if item.url %}[{{ title }}]({{ item.url }}){% else %}{{ title }} {% endif %}. {% for author in item.author %}{% if item.author.size > 1 %}{% if forloop.last == true %} and {% elsif forloop.first == false %}, {% endif %}{% endif %}{{ author.given }} {{ author.family }}{% endfor %}. ({{ item.issued[0].year}})
{% endfor %}
{% endfor %}
{% endif %}

{% assign ytheses = theses
  | where_exp: 'r', 'r.issued[0].year == year' %}
{% if ytheses.size > 0 %}
## Theses
{% assign months = ytheses
  | map: "issued"
  | map: "month"
  | uniq | sort | reverse %}
{% for month in months %}
{% assign mtheses = ytheses
  | where_exp: 'r', 'r.issued[0].month == month' %}
{% for item in mtheses %}
{% capture title %}{% assign t = item.title | split: ' ' %}{% for word in t %}{{ word | capitalize }} {% endfor %}{% endcapture %}
{% if item.url %}[{{ title }}]({{ item.url }}){% else %}{{ title }} {% endif %}. {% for author in item.author %}{% if item.author.size > 1 %}{% if forloop.last == true %} and {% elsif forloop.first == false %}, {% endif %}{% endif %}{{ author.given }} {{ author.family }}{% endfor %}. {% if item.genre %} {{ item.genre }},{% endif %} {{ item.publisher }}. ({{ item.issued[0].year}})
{% endfor %}
{% endfor %}
{% endif %}

{% endfor %}
