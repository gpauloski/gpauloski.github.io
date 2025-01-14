from __future__ import annotations

import calendar
import glob
import json
import os
import pathlib
from typing import NamedTuple


class Thesis(NamedTuple):
    tag: str
    title: str
    abstract: str
    committee: str
    location: str
    year: int
    month: int
    date_str: str
    pdf: str | None = None
    slides: str | None = None
    poster: str | None = None


def parse_thesis_json(thesis_file: str) -> Thesis:
    with open(thesis_file) as f:
        attrs = json.load(f)

        return Thesis(
            tag=pathlib.Path(thesis_file).stem,
            title=attrs["title"],
            abstract=attrs["abstract"],
            committee=attrs["committee"],
            location=attrs["location"],
            pdf=attrs["pdf"] if "pdf" in attrs else None,
            poster=attrs["poster"] if "poster" in attrs else None,
            slides=attrs["slides"] if "slides" in attrs else None,
            year=attrs["year"],
            month=attrs["month"],
            date_str=f"{calendar.month_abbr[attrs['month']]} {attrs['year']}",
        )


def load_theses(theses_dir: str) -> list[Thesis]:
    theses_files = glob.glob("*.json", root_dir=theses_dir)

    theses = [
        parse_thesis_json(os.path.join(theses_dir, f)) for f in theses_files
    ]

    theses.sort(key=lambda p: (p.year, p.month), reverse=True)

    return theses
