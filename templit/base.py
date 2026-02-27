"""
templit.base
~~~~~~~~~~~~
Abstract base class for template sources and the Template dataclass.

A *TemplateSource* is anything that can yield a mapping of
  name -> Template
Examples: built-in registry, user JSON directory, remote URL, etc.
"""

from __future__ import annotations

import abc
import logging
import re
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

# Slug validation: lowercase letters, digits, hyphens; no leading/trailing hyphens.
_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_template_name(name: str) -> None:
    """Raise ValueError if *name* is not a valid template slug."""
    if not name:
        raise ValueError("Template name must not be empty.")
    if not _NAME_RE.match(name):
        raise ValueError(
            f"Invalid template name {name!r}. "
            "Use lowercase letters, digits, and hyphens only (e.g. my-config)."
        )


# ── Template ─────────────────────────────────────────────────────────────────

@dataclass
class Template:
    """A single scaffolding template."""

    name: str
    desc: str
    tags: list[str]
    files: dict[str, str]       # relative-path -> raw content
    source: str = "builtin"     # human-readable provenance label

    # ── rendering ────────────────────────────────────────────────────────────

    def render_path(self, rel: str, project: str) -> str:
        return rel.replace("{{project}}", project)

    def render_content(self, content: str, project: str) -> str:
        return content.replace("{{project}}", project)

    def scaffold(
        self,
        project: str,
        dest: Path,
        dry_run: bool = False,
        *,
        overwrite: bool = False,
    ) -> list[Path]:
        """
        Write all template files into *dest*.

        Returns the list of paths that were (or would be) written.
        Emits no console output — callers are responsible for user-facing messages.
        """
        written: list[Path] = []
        for rel, content in self.files.items():
            target = dest / self.render_path(rel, project)
            if dry_run:
                logger.debug("[dry-run] would write %s", target)
                written.append(target)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists() and not overwrite:
                logger.debug("skipping existing file: %s", target)
            else:
                target.write_text(self.render_content(content, project), encoding="utf-8")
                logger.debug("wrote %s", target)
                written.append(target)
        return written

    # ── serialization ────────────────────────────────────────────────────────

    def to_dict(self) -> dict:
        return {
            "desc": self.desc,
            "tags": self.tags,
            "files": self.files,
        }

    @classmethod
    def from_dict(cls, name: str, data: dict, source: str = "user") -> "Template":
        return cls(
            name=name,
            desc=data.get("desc", ""),
            tags=list(data.get("tags", [])),
            files=dict(data.get("files", {})),
            source=source,
        )


# ── Abstract source ──────────────────────────────────────────────────────────

class TemplateSource(abc.ABC):
    """
    Abstract provider of named templates.

    Subclass this to add new template origins (built-ins, disk, remote, …).
    """

    @abc.abstractmethod
    def load(self) -> dict[str, Template]:
        """Return a mapping of template-name -> Template."""
        ...

    # Optional human-readable label shown in `templit list`
    @property
    def label(self) -> str:
        return self.__class__.__name__
