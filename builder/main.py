from __future__ import annotations

import argparse
import datetime
import os
import shutil
import sys
import webbrowser
from collections.abc import Sequence

import builder
from builder.presentations import load_presentations
from builder.publications import load_publications
from builder.render import build_templates


def configure_build_dir(build_dir: str, *, seed_dir: str | None = None) -> str:
    print(f'creating build dir at {build_dir}...')

    if os.path.isdir(build_dir):
        print(f'build dir already exists, clearing {build_dir}...')
        shutil.rmtree(build_dir)

    if seed_dir is not None:
        print(f'populating build dir from seed dir {seed_dir}...')
        shutil.copytree(seed_dir, build_dir)
    else:
        os.makedirs(build_dir, exist_ok=True)

    print('build dir initialized.')

    return build_dir


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv[1:]

    parser = argparse.ArgumentParser(
        description='Jinja-based static webpage builder',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog='python -m builder',
    )

    # https://stackoverflow.com/a/8521644/812183
    parser.add_argument(
        '-V',
        '--version',
        action='version',
        version=f'builder {builder.__version__}',
    )

    parser.add_argument(
        '--build',
        default='./_site',
        help='output directory',
    )
    parser.add_argument(
        '--content',
        default='./content',
        help='content directory',
    )
    parser.add_argument(
        '--static',
        default='./static',
        help='seed directory (static content for site)',
    )
    parser.add_argument(
        '--templates',
        default='./templates',
        help='templates directory',
    )
    parser.add_argument(
        '--open',
        action='store_true',
        help='open the page in browser after build',
    )

    args = parser.parse_args(argv)

    bib_dir = os.path.join(args.static, 'publications')
    bib_files = [
        os.path.join(bib_dir, f)
        for f in os.listdir(bib_dir)
        if f.endswith('.bib')
    ]
    if len(bib_files) == 0:
        raise OSError(f'No files ending with .bib in {bib_dir} were found.')
    elif len(bib_files) > 1:
        raise OSError(f'Found multiple files ending with .bib in {bib_dir}.')
    (bib_file,) = bib_files

    publications = load_publications(
        os.path.join(args.content, 'publications'),
        bib_file,
    )
    presentations = load_presentations(
        os.path.join(args.content, 'presentations'),
    )

    build_dir = configure_build_dir(args.build, seed_dir=args.static)
    build_templates(
        build_dir,
        templates=args.templates,
        publications=publications,
        presentations=presentations,
        current_year=datetime.date.today().year,
    )

    if args.open:
        url = os.path.join(build_dir, 'index.html')
        webbrowser.open(url, new=0, autoraise=True)

    return 0
