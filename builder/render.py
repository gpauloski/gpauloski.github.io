from __future__ import annotations

import os
from typing import Any

import jinja2


def build_templates(
    build: str,
    *,
    templates: str,
    **kwargs: Any,
) -> None:
    if not os.path.isdir(build):
        raise OSError(f"{build} is not a directory")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates),
        autoescape=jinja2.select_autoescape(),
    )

    print("rendering index...")
    index = render_index(env, **kwargs)
    index_file = os.path.join(build, "index.html")
    with open(index_file, "w") as f:
        f.write(index)
    print(f"wrote index to {index_file}.")


def render_index(env: jinja2.Environment, **kwargs: Any) -> str:
    template = env.get_template("index.html")

    return template.render(**kwargs)
