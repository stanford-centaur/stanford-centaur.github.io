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
        r'nocite: \"\[@\*\]\"\n': '',
        r'issued: ([0-9][0-9][0-9][0-9])-([0-9][0-9])':\
                r'issued:\n  - year: \1\n    month: \2',
        r'issued: ([0-9][0-9][0-9][0-9])': \
                r'issued:\n  - year: \1\n    month: 01',
        'month: 0': 'month: ',
        r'\$([0-9]*)\^\{(.*)\}\$': r'\1<sup>\2</sup>',
        r'(title:.*)\[': r'\1',
        r'\]{\.nocase}': '',
        r'(' + "|".join(w for w in special_fields) + ')=(.*),': r'\n  \1: \2',
        r'\s+\n': '\n',
        r"([A-Z]) '([1-2])": r"\1'\2",
        r'H\$_2\$o': 'H<sub>2</sub>o',
        r'\$\\delta\$': 'δ',
        r'award: Best SCP': 'award: SCP Best',
        }

def extract_awards(m):
    """Turn emphasized parts of a note (*...*) into a list of awards."""
    note = re.sub(r'\s+', ' ', m.group(1)).strip()
    if note.startswith('"') and note.endswith('"'):
        note = note[1:-1]
    awards = re.findall(r'\*([^*]+)\*', note)
    if not awards:
        return m.group(0)
    res = ''
    rest = re.sub(r'\*[^*]+\*', '', note).strip(' ,;')
    if rest:
        res += '\n  note: ' + rest
    res += '\n  awards:'
    for a in awards:
        res += '\n    - award: ' + a.strip(' ,;')
    return res

# notes may be wrapped over multiple (indented) lines
markdown_vita = re.sub(r'\n  note: (.*(?:\n    .*)*)', extract_awards, markdown_vita)
markdown_refs = re.sub(r'\n  note: (.*(?:\n    .*)*)', extract_awards, markdown_refs)

for s, r in subst.items():
    markdown_vita = re.sub(s, r, markdown_vita)
    markdown_refs = re.sub(s, r, markdown_refs)
    markdown_refs = markdown_refs.replace('references:', '')

with path_outfile.open('w') as outfile:
    outfile.write(markdown_vita)
with path_outfile.open('a') as outfile:
    outfile.write(markdown_refs)

