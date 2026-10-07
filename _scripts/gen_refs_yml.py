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
        }

def get_venue(entry):
    """Get venue abbreviation from container title, e.g., (FM'24) or CAV 2026."""
    m = re.search(r'\n  container-title: (.*(?:\n    .*)*)', entry)
    if not m:
        return None
    title = re.sub(r'\s+', ' ', m.group(1))
    m = re.search(r"\(([A-Z]+) ?'[0-9][0-9]\)", title) \
            or re.search(r'\b([A-Z]{2,}) [0-9]{4}\b', title)
    return m.group(1) if m else None

def extract_awards(entry):
    """
    Turn emphasized parts of a note (*...*), optionally linked
    ([*...*](url)), into a list of awards. Awards without venue are
    prefixed with the venue abbreviation.
    """
    # notes may be wrapped over multiple (indented) lines
    m = re.search(r'\n  note: (.*(?:\n    .*)*)', entry)
    if not m:
        return entry
    note = re.sub(r'\s+', ' ', m.group(1)).strip()
    if note.startswith('"') and note.endswith('"'):
        note = note[1:-1]
    pattern = r'\[\*([^*]+)\*\]\(([^)]+)\)|\*([^*]+)\*'
    awards = re.findall(pattern, note)
    if not awards:
        return entry
    venue = get_venue(entry)
    res = ''
    rest = re.sub(pattern, '', note).strip(' ,;')
    if rest:
        res += '\n  note: ' + rest
    res += '\n  awards:'
    for linked, url, plain in awards:
        award = (linked or plain).strip(' ,;')
        award = award.replace('Best SCP', 'SCP Best')
        if venue and not re.match(r'(Nominated|[A-Z]{2,}) ', award):
            award = f'{venue} {award}'
        res += '\n    - award: ' + award
        if url:
            res += '\n      url: ' + url
    return entry[:m.start()] + res + entry[m.end():]

markdown_vita = ''.join(
        extract_awards(e) for e in re.split(r'(?=\n- )', markdown_vita))
markdown_refs = ''.join(
        extract_awards(e) for e in re.split(r'(?=\n- )', markdown_refs))

for s, r in subst.items():
    markdown_vita = re.sub(s, r, markdown_vita)
    markdown_refs = re.sub(s, r, markdown_refs)
    markdown_refs = markdown_refs.replace('references:', '')

with path_outfile.open('w') as outfile:
    outfile.write(markdown_vita)
with path_outfile.open('a') as outfile:
    outfile.write(markdown_refs)

