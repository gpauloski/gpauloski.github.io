# Publications

Each file in this directory is JSON with the following fields.
The files will be automatically parsed to generate the static page.

```json
{
    "title": "Paper Title",
    "authors": [
        "Author 1",
        "Author 2"
    ],
    "venue": "FunConf 2022",
    "award": null,
    "tldr": "Two sentence TLDR.",
    "paper": "publications/*.pdf",
    "bibtex": "bibtex entry name",
    "code": null,
    "website": null,
    "poster": null,
    "slides": null,
    "publication" : null,
    "preprint": null,
    "year": 2020,
    "month": 11,
    "selected": false
}
```

If the publication received an award, set `award` to an object with the award
name and an optional link to the award announcement.

```json
"award": {
    "name": "eScience Best Paper",
    "url": "https://www.escience-conference.org/2024/"
}
```
