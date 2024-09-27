from __future__ import annotations

import dataclasses
import pathlib
import tomllib
from typing import Any


@dataclasses.dataclass
class Config:
    build: BuildConfig
    overview: OverviewConfig
    research: ResearchConfig
    projects: ProjectsConfig
    publications: PublicationsConfig
    presentations: PresentationsConfig
    theses: ThesesConfig

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Config:
        return Config(
            build=BuildConfig(**data["build"]),
            overview=OverviewConfig(**data["overview"]),
            research=ResearchConfig(**data["research"]),
            projects=ProjectsConfig(**data["projects"]),
            publications=PublicationsConfig(**data["publications"]),
            presentations=PresentationsConfig(**data["presentations"]),
            theses=ThesesConfig(**data["theses"]),
        )

    @classmethod
    def from_file(cls, filepath: str | pathlib.Path) -> Config:
        with open(filepath, "rb") as f:
            return Config.from_dict(tomllib.load(f))


@dataclasses.dataclass
class BuildConfig:
    """build config.

    Attributes:
        build_dir: Output of build directory.
        templates: Templates directory.
        static: Static content directory.
    """

    build_dir: str
    templates_dir: str
    static_dir: str


@dataclasses.dataclass
class OverviewConfig:
    """Overview config.

    Attributes:
        name: Name of website owner.
        titles: List of titles/professions.
        headshot: Path to headshot image.
        contacts: Mapping of contact type to link.
        analytics: Google analyics ID.
        source: Link to source code of website.
        text: Overview/intro paragraph (HTML supported).
    """

    name: str
    titles: list[str]
    headshot: str
    contacts: list[dict[str, str]]
    analytics: str
    source: str
    text: str


@dataclasses.dataclass
class ResearchConfig:
    """Research config.

    Attributes:
        sections: List of mappings where each mapping contains the name
            and text key corresponding to a research section.
    """

    sections: list[dict[str, str]]


@dataclasses.dataclass
class ProjectsConfig:
    """Projects config.

    Attributes:
        github: Link to GitHub page where projects can be found.
        links: List of mappings where each mapping contains the name and link
            key corresponding to a project.
    """

    github: str
    links: list[dict[str, str]]


@dataclasses.dataclass
class PublicationsConfig:
    """Publications config.

    Attributes:
        bibtex: Relative link to bibtex file (this will be relative to the
            static files directory.
        publications_dir: Directory containing JSON files of publication
            metadata.
    """

    bibtex: str
    publications_dir: str


@dataclasses.dataclass
class PresentationsConfig:
    """Presentations config.

    Attributes:
        presentations_dir: Directory containing JSON files of presentation
            metadata.
    """

    presentations_dir: str


@dataclasses.dataclass
class ThesesConfig:
    """Theses config.

    Attributes:
        theses_dir: Directory containing JSON files of theses metadata.
    """

    theses_dir: str
