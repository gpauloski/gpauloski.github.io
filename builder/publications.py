from __future__ import annotations

import glob
import json
import os
from typing import NamedTuple

import bibtexparser
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bwriter import BibTexWriter


class Publication(NamedTuple):
    title: str
    authors: str
    venue: str
    tldr: str
    paper: str
    bibtex_id: str
    bibtex: str
    year: int
    month: int
    code: str | None = None
    website: str | None = None
    poster: str | None = None
    slides: str | None = None


def parse_publication_json(pub_file: str) -> Publication:
    with open(pub_file) as f:
        attrs = json.load(f)

        if isinstance(attrs['authors'], list):
            authors = ', '.join(attrs['authors'])
        elif isinstance(attrs['authors'], str):
            authors = attrs['authors']
        else:
            raise ValueError(f'Unable to parse authors field of {pub_file}.')

        return Publication(
            title=attrs['title'],
            authors=authors,
            venue=attrs['venue'],
            tldr=attrs['tldr'],
            paper=attrs['paper'],
            bibtex_id=attrs['bibtex'],
            bibtex='',
            code=attrs['code'] if 'code' in attrs else None,
            website=attrs['website'] if 'website' in attrs else None,
            poster=attrs['poster'] if 'poster' in attrs else None,
            slides=attrs['slides'] if 'slides' in attrs else None,
            year=attrs['year'],
            month=attrs['month'],
        )


def load_publications(pub_dir: str, bib_file: str) -> list[Publication]:
    with open(bib_file) as bf:
        bibs = bibtexparser.load(bf).entries_dict

    bib_writer = BibTexWriter()
    bib_writer.indent = '  '

    pubs: list[Publication] = []
    for pub_file in glob.glob('*.json', root_dir=pub_dir):
        pub = parse_publication_json(os.path.join(pub_dir, pub_file))

        bib = bibs[pub.bibtex_id]

        temp_database = BibDatabase()
        temp_database.entries = [bib]
        bib_str = bib_writer.write(temp_database)

        pubs.append(pub._replace(bibtex=bib_str))

    pubs.sort(key=lambda x: (x.year, x.month), reverse=True)

    return pubs