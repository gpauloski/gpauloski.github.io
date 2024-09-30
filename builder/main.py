from __future__ import annotations

import argparse
import datetime
import os
import shutil
import sys
import webbrowser
from collections.abc import Sequence

import builder
from builder.config import Config
from builder.presentations import load_presentations
from builder.publications import load_publications
from builder.render import build_templates
from builder.theses import load_theses


def configure_build_dir(build_dir: str, *, seed_dir: str | None = None) -> str:
    print(f"creating build dir at {build_dir}...")

    if os.path.isdir(build_dir):
        print(f"build dir already exists, clearing {build_dir}...")
        shutil.rmtree(build_dir)

    if seed_dir is not None:
        print(f"populating build dir from seed dir {seed_dir}...")
        shutil.copytree(seed_dir, build_dir)
    else:
        os.makedirs(build_dir, exist_ok=True)

    print("build dir initialized.")

    return build_dir


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="Jinja-based static webpage builder",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="python -m builder",
    )

    # https://stackoverflow.com/a/8521644/812183
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"builder {builder.__version__}",
    )

    parser.add_argument(
        "--config",
        default="./config/config.toml",
        help="config file",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="open the page in browser after build",
    )

    args = parser.parse_args(argv)

    config = Config.from_file(args.config)

    publications = load_publications(
        config.publications.publications_dir,
        os.path.join(config.build.static_dir, config.publications.bibtex),
    )
    presentations = load_presentations(config.presentations.presentations_dir)
    theses = load_theses(config.theses.theses_dir)

    pub_categories = {
        "systems": "Distributed Systems",
        "ml": "Scalable Deep Learning",
        "science": "AI for Science",
    }

    build_dir = configure_build_dir(
        config.build.build_dir,
        seed_dir=config.build.static_dir,
    )
    build_templates(
        build_dir,
        templates=config.build.templates_dir,
        # Keyword arguments that get passed to jinja templates
        selected_publications=[p for p in publications if p.selected],
        all_publications=publications,
        pub_categories=pub_categories,
        presentations=presentations,
        theses=theses,
        current_year=datetime.date.today().year,
        config=config,
    )

    if args.open:
        url = os.path.join(build_dir, "index.html")
        webbrowser.open(url, new=0, autoraise=True)

    return 0
