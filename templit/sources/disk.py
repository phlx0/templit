"""
templit.sources.disk
~~~~~~~~~~~~~~~~~~~~
Loads user-defined templates from ~/.config/templit/templates/*.json.
"""

from __future__ import annotations

import json

from templit.base import Template, TemplateSource
from templit.config import USER_TMPL, ensure_dirs


class UserDiskSource(TemplateSource):
    """
    Reads every *.json file in the user template directory.
    The stem of the filename becomes the template name.
    """

    @property
    def label(self) -> str:
        return "user"

    def load(self) -> dict[str, Template]:
        ensure_dirs()
        templates: dict[str, Template] = {}
        for path in sorted(USER_TMPL.glob("*.json")):
            try:
                data = json.loads(path.read_text())
                name = path.stem
                templates[name] = Template.from_dict(name, data, source="user")
            except Exception as exc:
                from templit.color import warn
                warn(f"Could not load user template '{path.name}': {exc}")
        return templates
