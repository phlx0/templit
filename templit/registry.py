"""
templit.registry
~~~~~~~~~~~~~~~~
Merges multiple TemplateSource instances into one flat namespace.
Sources registered later override earlier ones (user > builtin).
"""

from __future__ import annotations

import logging

from templit.base import Template, TemplateSource

logger = logging.getLogger(__name__)


class Registry:
    """
    Central template store.

    Usage::

        reg = Registry()
        reg.register(BuiltinSource())
        reg.register(UserDiskSource())   # overrides builtins with same name

        tmpl = reg.get("python-fastapi")
        all  = reg.all()
    """

    def __init__(self) -> None:
        self._sources: list[TemplateSource] = []
        self._cache: dict[str, Template] | None = None

    # ── registration ─────────────────────────────────────────────────────────

    def register(self, source: TemplateSource) -> "Registry":
        """Append a source; later sources win on name collision."""
        self._sources.append(source)
        self._cache = None      # invalidate on every structural change
        return self

    def invalidate(self) -> None:
        """Explicitly drop the cached template map (e.g. after writing a new file)."""
        self._cache = None

    # ── lookup ───────────────────────────────────────────────────────────────

    def _build(self) -> dict[str, Template]:
        merged: dict[str, Template] = {}
        for src in self._sources:
            try:
                merged.update(src.load())
            except Exception as exc:
                logger.warning("Source %r failed to load: %s", src.label, exc)
        return merged

    def all(self) -> dict[str, Template]:
        if self._cache is None:
            self._cache = self._build()
        return self._cache

    def get(self, name: str) -> Template | None:
        return self.all().get(name)

    def search(self, query: str = "", tag: str = "") -> dict[str, Template]:
        q = query.lower()
        results: dict[str, Template] = {}
        for name, tmpl in self.all().items():
            if tag and tag not in tmpl.tags:
                continue
            if q and (
                q not in name.lower()
                and q not in tmpl.desc.lower()
                and not any(q in t for t in tmpl.tags)
            ):
                continue
            results[name] = tmpl
        return results


# ── application registry factory ─────────────────────────────────────────────
# Prefer dependency-injection over a module-level mutable singleton;
# use get_registry() only at CLI entry-points, not deep in library code.

_registry: Registry | None = None


def get_registry() -> Registry:
    """Return the application-wide Registry, building it on first call."""
    global _registry
    if _registry is None:
        from templit.sources.builtin import BuiltinSource
        from templit.sources.disk    import UserDiskSource
        _registry = (
            Registry()
            .register(BuiltinSource())
            .register(UserDiskSource())     # user templates override builtins
        )
    return _registry


def reset_registry() -> None:
    """Reset the singleton (primarily useful in tests)."""
    global _registry
    _registry = None
