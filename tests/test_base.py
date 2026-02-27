"""Tests for templit.base."""

from __future__ import annotations

import pytest
from pathlib import Path

from templit.base import Template, validate_template_name


# ── validate_template_name ───────────────────────────────────────────────────

@pytest.mark.parametrize("name", [
    "my-template",
    "python-cli",
    "react-app",
    "a",
    "abc123",
    "a1-b2",
])
def test_validate_name_valid(name: str) -> None:
    validate_template_name(name)   # should not raise


@pytest.mark.parametrize("name", [
    "",
    "My-Template",      # uppercase
    "-leading",
    "trailing-",
    "double--hyphen",
    "has space",
    "has/slash",
    "../traversal",
])
def test_validate_name_invalid(name: str) -> None:
    with pytest.raises(ValueError):
        validate_template_name(name)


# ── Template.render_path / render_content ────────────────────────────────────

def test_render_path() -> None:
    tmpl = Template(name="t", desc="", tags=[], files={})
    assert tmpl.render_path("{{project}}/main.py", "myapp") == "myapp/main.py"


def test_render_content() -> None:
    tmpl = Template(name="t", desc="", tags=[], files={})
    result = tmpl.render_content("project = {{project}}", "myapp")
    assert result == "project = myapp"


# ── Template.scaffold ────────────────────────────────────────────────────────

def test_scaffold_writes_files(tmp_path: Path) -> None:
    tmpl = Template(
        name="t",
        desc="test",
        tags=[],
        files={"{{project}}/README.md": "# {{project}}"},
    )
    written = tmpl.scaffold("myapp", tmp_path)
    assert len(written) == 1
    out = tmp_path / "myapp" / "README.md"
    assert out.exists()
    assert out.read_text(encoding="utf-8") == "# myapp"


def test_scaffold_dry_run(tmp_path: Path) -> None:
    tmpl = Template(
        name="t",
        desc="test",
        tags=[],
        files={"README.md": "hello"},
    )
    written = tmpl.scaffold("proj", tmp_path, dry_run=True)
    assert len(written) == 1
    assert not (tmp_path / "README.md").exists()


def test_scaffold_skips_existing_by_default(tmp_path: Path) -> None:
    existing = tmp_path / "README.md"
    existing.write_text("original", encoding="utf-8")
    tmpl = Template(name="t", desc="", tags=[], files={"README.md": "new"})
    written = tmpl.scaffold("proj", tmp_path)
    assert written == []
    assert existing.read_text(encoding="utf-8") == "original"


def test_scaffold_overwrite(tmp_path: Path) -> None:
    existing = tmp_path / "README.md"
    existing.write_text("original", encoding="utf-8")
    tmpl = Template(name="t", desc="", tags=[], files={"README.md": "new"})
    written = tmpl.scaffold("proj", tmp_path, overwrite=True)
    assert len(written) == 1
    assert existing.read_text(encoding="utf-8") == "new"


# ── Template serialization ───────────────────────────────────────────────────

def test_round_trip() -> None:
    tmpl = Template(
        name="my-tmpl",
        desc="A test template",
        tags=["python", "test"],
        files={"main.py": "print('hello')"},
        source="builtin",
    )
    data = tmpl.to_dict()
    restored = Template.from_dict("my-tmpl", data, source="builtin")
    assert restored.name  == tmpl.name
    assert restored.desc  == tmpl.desc
    assert restored.tags  == tmpl.tags
    assert restored.files == tmpl.files
