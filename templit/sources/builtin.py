"""
templit.sources.builtin
~~~~~~~~~~~~~~~~~~~~~~~
Loads built-in templates from the JSON files in templit/templates/.
To add a new built-in, just drop a .json file in that folder — no Python needed.
"""

from __future__ import annotations

import json
from pathlib import Path

from templit.base import Template, TemplateSource

# The templates/ folder sits next to this sources/ package
BUILTIN_TMPL_DIR = Path(__file__).parent.parent / "templates"


class BuiltinSource(TemplateSource):
    """Loads every *.json file from the bundled templates/ directory."""

    @property
    def label(self) -> str:
        return "builtin"

    def load(self) -> dict[str, Template]:
        templates: dict[str, Template] = {}
        for path in sorted(BUILTIN_TMPL_DIR.glob("*.json")):
            try:
                data = json.loads(path.read_text())
                name = path.stem
                templates[name] = Template.from_dict(name, data, source="builtin")
            except Exception as exc:
                from templit.color import warn
                warn(f"Could not load built-in '{path.name}': {exc}")
        return templates
