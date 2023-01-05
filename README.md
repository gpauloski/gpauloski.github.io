# Personal website for Greg Pauloski

[![Deploy](https://github.com/gpauloski/gpauloski.github.io/actions/workflows/deploy.yml/badge.svg)](https://github.com/gpauloski/gpauloski.github.io/actions)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/gpauloski/gpauloski.github.io/main.svg)](https://results.pre-commit.ci/latest/github/gpauloski/gpauloski.github.io/main)

Static files and code for generating my personal website at [gregpauloski.com](https://gregpauloski.com).
The page design is based on [ericwallace.com](https://www.ericswallace.com/), and the static site compilation is done in Python using Jinja.

## Structure

| Directory    | Description |
| ------------ | ----------- |
| `builder/`   | Python packages that compiles the static site with Jinja.     |
| `content/`   | Data files for generating various sections of the site.       |
| `static/`    | Static files to include in the site (CSS, files, images).     |
| `templates/` | HTML Jinja templates compiled to produce final rendered site. |

## Build Locally

```bash
$ virtualenv venv
$ . venv/bin/activate
$ pip install -e .
$ python -m builder --open
```

The output is written to `_site/` by default, and `_site/index.html` can be opened in your browser to view.
The `--open` flag will automatically open the page after the build completes.

The filepaths default to the existing ones in the repo but can be overridden via arguments.
See `python -m builder --help` for more details.

## Updating

To add a new publication:
1. Add the bibtex entry to `static/publications/publications.html`.
2. Add the PDF to `static/publications/`.
3. Create a new JSON file for the publication in `content/publications/` and fill out all of the fields.

To add a new presentation:
1. Add the PDF to `static/slides/` or `static/posters/`.
2. Create a new JSON file for the presentation in `content/presentations/` and fill out all of the fields.

# Deploying

The website is built and deployed from HEAD weekly and on each push to `main`.

# Fixing BibTex

The `builder` package also includes a CLI utility for formatting BibTex files.
The formatter will do many things: sort by entry IDs, sort keys within entries, clean up indents, use uniform formatting, fix casing in titles, and more.

The `builder` package must first be installed in your Python environment if not already.
```bash
$ virtualenv venv
$ . venv/bin/activate
$ pip install .
```

To format:
```bash
$ python -m builder.publications --input INPUT_BIB_FILE --output OUTPUT_BIB_FILE
```
Use `python -m builder.publications --help` for additional options.
