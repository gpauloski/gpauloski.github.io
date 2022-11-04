from __future__ import annotations

import glob
import json
import os
from typing import NamedTuple


class Presentation(NamedTuple):
    title: str
    location: str
    year: int
    month: int
    slides: str | None = None
    poster: str | None = None


def parse_presentation_json(pres_file: str) -> Presentation:
    with open(pres_file) as f:
        attrs = json.load(f)

        return Presentation(
            title=attrs['title'],
            location=attrs['location'],
            poster=attrs['poster'] if 'poster' in attrs else None,
            slides=attrs['slides'] if 'slides' in attrs else None,
            year=attrs['year'],
            month=attrs['month'],
        )


def load_presentations(pres_dir: str) -> list[Presentation]:
    pres_files = glob.glob('*.json', root_dir=pres_dir)

    press = [
        parse_presentation_json(os.path.join(pres_dir, f)) for f in pres_files
    ]

    press.sort(key=lambda p: (p.year, p.month), reverse=True)

    return press
