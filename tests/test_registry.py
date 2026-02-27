"""Tests for templit.registry."""

from __future__ import annotations

from templit.base import Template, TemplateSource
from templit.registry import Registry


class _StaticSource(TemplateSource):
    """Test source with a fixed set of templates."""

    def __init__(self, templates: dict[str, Template]) -> None:
        self._templates = templates

    def load(self) -> dict[str, Template]:
        return self._templates


def _tmpl(name: str, tags: list[str] | None = None) -> Template:
    return Template(name=name, desc=f"desc-{name}", tags=tags or [], files={})


# ── registration & lookup ────────────────────────────────────────────────────

def test_register_and_get() -> None:
    reg = Registry()
    reg.register(_StaticSource({"foo": _tmpl("foo")}))
    assert reg.get("foo") is not None
    assert reg.get("bar") is None


def test_later_source_overrides_earlier() -> None:
    a = _tmpl("x")
    b = _tmpl("x")
    reg = Registry()
    reg.register(_StaticSource({"x": a}))
    reg.register(_StaticSource({"x": b}))
    assert reg.get("x") is b


def test_invalidate_clears_cache() -> None:
    source_data: dict[str, Template] = {"t": _tmpl("t")}
    reg = Registry()
    reg.register(_StaticSource(source_data))
    _ = reg.all()                          # populate cache
    source_data["new"] = _tmpl("new")
    assert reg.get("new") is None          # cache still stale
    reg.invalidate()
    assert reg.get("new") is not None


# ── search ───────────────────────────────────────────────────────────────────

def test_search_by_query() -> None:
    reg = Registry()
    reg.register(_StaticSource({
        "python-cli": _tmpl("python-cli", tags=["python"]),
        "go-basic":   _tmpl("go-basic",   tags=["go"]),
    }))
    results = reg.search(query="python")
    assert "python-cli" in results
    assert "go-basic"   not in results


def test_search_by_tag() -> None:
    reg = Registry()
    reg.register(_StaticSource({
        "a": _tmpl("a", tags=["python"]),
        "b": _tmpl("b", tags=["go"]),
    }))
    results = reg.search(tag="python")
    assert "a" in results
    assert "b" not in results


def test_search_empty_returns_all() -> None:
    reg = Registry()
    reg.register(_StaticSource({"x": _tmpl("x"), "y": _tmpl("y")}))
    assert len(reg.search()) == 2


# ── error resilience ─────────────────────────────────────────────────────────

def test_failing_source_does_not_crash_registry() -> None:
    class _BadSource(TemplateSource):
        def load(self):
            raise RuntimeError("boom")

    reg = Registry()
    reg.register(_BadSource())
    reg.register(_StaticSource({"ok": _tmpl("ok")}))
    assert reg.get("ok") is not None
