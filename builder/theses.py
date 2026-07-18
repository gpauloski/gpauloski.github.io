from __future__ import annotations

import calendar
import glob
import json
import os
import pathlib
from typing import NamedTuple

from bibtexparser.bibdatabase import BibDatabase

from builder.publications import get_bibtex_writer
from builder.publications import load_bibtex


class Thesis(NamedTuple):
    tag: str
    title: str
    abstract: str
    committee: str
    location: str
    university: str
    year: int
    month: int
    date_str: str
    pdf: str | None = None
    slides: str | None = None
    poster: str | None = None
    bibtex_id: str | None = None
    bibtex: str = ""


def parse_thesis_json(thesis_file: str) -> Thesis:
    with open(thesis_file) as f:
        attrs = json.load(f)

        return Thesis(
            tag=pathlib.Path(thesis_file).stem,
            title=attrs["title"],
            abstract=attrs["abstract"],
            committee=attrs["committee"],
            location=attrs["location"],
            university=attrs.get("university", ""),
            pdf=attrs["pdf"] if "pdf" in attrs else None,
            poster=attrs["poster"] if "poster" in attrs else None,
            slides=attrs["slides"] if "slides" in attrs else None,
            bibtex_id=attrs["bibtex"] if "bibtex" in attrs else None,
            year=attrs["year"],
            month=attrs["month"],
            date_str=f"{calendar.month_abbr[attrs['month']]} {attrs['year']}",
        )


def load_theses(theses_dir: str, bib_file: str | None = None) -> list[Thesis]:
    theses_files = glob.glob("*.json", root_dir=theses_dir)

    theses = [
        parse_thesis_json(os.path.join(theses_dir, f)) for f in theses_files
    ]

    if bib_file is not None:
        bibs = load_bibtex(bib_file).entries_dict
        bib_writer = get_bibtex_writer()
        for i, thesis in enumerate(theses):
            if thesis.bibtex_id is not None and thesis.bibtex_id in bibs:
                temp_database = BibDatabase()
                temp_database.entries = [bibs[thesis.bibtex_id]]
                bib_str = bib_writer.write(temp_database)
                theses[i] = thesis._replace(bibtex=bib_str)

    theses.sort(key=lambda p: (p.year, p.month), reverse=True)

    return theses
