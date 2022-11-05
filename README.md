# Personal website for Greg Pauloski

[![Deploy](https://github.com/gpauloski/gpauloski.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/gpauloski/gpauloski.github.io/actions)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/gpauloski/gpauloski.github.io/main.svg)](https://results.pre-commit.ci/latest/github/gpauloski/gpauloski.github.io/main)

Static files and code for generating my personal website at [gregpauloski.com](https://gregpauloski.com).
The template is based on [ericwallace.com](https://www.ericswallace.com/), but all of the code is written from scratch.

## Build Locally

```bash
$ virtualenv venv
$ . venv/bin/activate
$ pip install -e .
$ python -m builder
```

The output is written to `_site/` by default.
Open `_site/index.html` in your browser to view.

## Updating

To add a new publication:
1. Add the bibtex entry to `static/publications/publications.html`.
2. Add the PDF to `static/publications/`.
3. Create a new JSON file for the publication in `content/publications/` and fill out all of the fields.

To add a new presentation:
1. Add the PDF to `static/slides/` or `static/posters/`.
2. Create a new JSON file for the presentation in `content/presentations/` and fill out all of the fields.
