#! /bin/python

import pathlib
import re
import subprocess

parent_dir = pathlib.Path(__file__).parent.parent.resolve()
path_refs_bib = parent_dir.joinpath("_refs", "refs.bib")
path_vita_bib = parent_dir.joinpath("_refs", "vita.bib")
path_outfile = parent_dir.joinpath("_data", "publications.yml")

pandoc_args_vita = [
        'pandoc',
        path_vita_bib.as_posix(),
        '-s',
        '-f', 'biblatex',
        '-t', 'markdown'
        ]
pandoc_args_refs = [
        'pandoc',
        path_refs_bib.as_posix(),
        '-s',
        '-f', 'biblatex',
        '-t', 'markdown'
        ]

markdown_vita = subprocess.check_output(pandoc_args_vita).decode('utf8')
markdown_refs = subprocess.check_output(pandoc_args_refs).decode('utf8')

special_fields = ['pdf', 'bibtex', 'artifact']

subst = {
        '---\n': '',
        '\n---': '',
        'nocite: \"\[@\*\]\"\n': '',
        r'issued: ([0-9][0-9][0-9][0-9])-([0-9][0-9])':\
                r'issued:\n  - year: \1\n    month: \2',
        r'issued: ([0-9][0-9][0-9][0-9])': \
                r'issued:\n  - year: \1\n    month: 01',
        'month: 0': 'month: ',
        r'\$([0-9]*)\^\{(.*)\}\$': r'\1<sup>\2</sup>',
        r'(title:.*)\[': r'\1',
        r'\]{\.nocase}': '',
        r'(' + "|".join(w for w in special_fields) + ')=(.*),': r'\n  \1: \2',
        r'\*(Best.*?ward.*?)\*': r'\n  award: \1',
        r'\*(Distinguished.*?ward.*?)\*': r'\n  award: \1',
        r'\*(Nominated.*?ward.*?)\*': r'\n  award: \1',
        r'\*(Highlighted Paper)\*': r'\n  award: \1',
        r'.*note: "([\s\S]*?)"': r'\1',
        r'\s+\n': '\n',
        r"([A-Z]) '([1-2])": r"\1'\2",
        r'H\$_2\$o': 'H<sub>2</sub>o',
        r'Best SCP': 'SCP Best',
        }

for s, r in subst.items():
    markdown_vita = re.sub(s, r, markdown_vita)
    markdown_refs = re.sub(s, r, markdown_refs)
    markdown_refs = markdown_refs.replace('references:', '')

with path_outfile.open('w') as outfile:
    outfile.write(markdown_vita)
with path_outfile.open('a') as outfile:
    outfile.write(markdown_refs)

