"""
templit.commands.init
~~~~~~~~~~~~~~~~~~~~~
`templit init` — detect what's in the current folder and offer to
add relevant config/boilerplate files.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Callable

from templit.color import BOLD, CYAN, DIM, GREEN, WHITE, divider, ok, info, warn, paint
from templit.registry import get_registry


# ── detectors ────────────────────────────────────────────────────────────────
# Each detector is a (label, condition_fn, template_suggestions) triple.
# condition_fn returns True if it recognises the project type.

def _has(*filenames: str) -> bool:
    """Return True if any of *filenames* exist in the current directory."""
    return any(Path(f).exists() for f in filenames)


def _has_ext(*exts: str) -> bool:
    """Return True if any file with one of *exts* exists (non-recursive)."""
    return any(
        f.is_file() and f.suffix in exts
        for f in Path(".").iterdir()
    )


DETECTORS: list[tuple[str, Callable[[], bool], list[str]]] = [
    # (label, condition_fn, [template suggestions])
    (
        "Python project",
        lambda: _has("pyproject.toml", "setup.py", "setup.cfg") or _has_ext(".py"),
        ["gitignore-python", "makefile-python", "python-pytest", "pre-commit",
         "github-actions-python", "editorconfig", "dockerfile-python"],
    ),
    (
        "Node.js project",
        lambda: _has("package.json"),
        ["editorconfig"],
    ),
    (
        "Go project",
        lambda: _has("go.mod") or _has_ext(".go"),
        ["editorconfig"],
    ),
    (
        "Rust project",
        lambda: _has("Cargo.toml") or _has_ext(".rs"),
        ["editorconfig"],
    ),
    (
        "Docker",
        lambda: _has("Dockerfile", "docker-compose.yml", "docker-compose.yaml"),
        [],
    ),
    (
        "Git repo",
        lambda: _has(".git"),
        ["pre-commit", "editorconfig"],
    ),
]


# ── command ──────────────────────────────────────────────────────────────────

def cmd_init(args: argparse.Namespace) -> int:
    reg = get_registry()
    cwd = Path(".").resolve()

    print()
    print(paint("  templit init", BOLD, CYAN))
    print(paint(f"  {cwd}", DIM))
    divider()

    # ── detect project types ─────────────────────────────────────────────────
    detected = [
        (label, suggestions)
        for label, condition, suggestions in DETECTORS
        if condition()
    ]

    if not detected:
        warn("Could not detect a known project type in this directory.")
        print()
        return 0

    print(paint("  Detected:", DIM))
    for label, _ in detected:
        print(f"  {paint('✓', GREEN, BOLD)}  {label}")
    print()

    # ── collect relevant template suggestions ────────────────────────────────
    seen: set[str] = set()
    suggestions: list[str] = []
    for _, tmpl_names in detected:
        for name in tmpl_names:
            if name not in seen and reg.get(name) is not None:
                seen.add(name)
                suggestions.append(name)

    def _already_present(name: str) -> bool:
        """Return True if all files in template already exist in cwd."""
        tmpl = reg.get(name)
        return bool(tmpl and all((cwd / f).exists() for f in tmpl.files))

    suggestions = [s for s in suggestions if not _already_present(s)]

    if not suggestions:
        ok("Everything looks good — no missing config files detected.")
        print()
        return 0

    print(paint("  Suggested additions:", DIM))
    for i, name in enumerate(suggestions, 1):
        tmpl = reg.get(name)
        print(
            f"  {paint(str(i), CYAN, BOLD)}.  {paint(name, WHITE, BOLD)}"
            f"  {paint('— ' + tmpl.desc, DIM)}"
        )
    print()

    if args.yes:
        chosen = suggestions
    else:
        raw = input(
            paint("  Which to add? (numbers e.g. 1 3 5, 'a' for all, ENTER to skip): ", WHITE)
        ).strip()

        if not raw:
            info("Nothing added.")
            print()
            return 0

        if raw.lower() == "a":
            chosen = suggestions
        else:
            chosen = []
            for part in raw.split():
                try:
                    idx = int(part) - 1
                    if 0 <= idx < len(suggestions):
                        chosen.append(suggestions[idx])
                    else:
                        warn(f"Index out of range: {part!r}")
                except ValueError:
                    warn(f"Skipping invalid input: {part!r}")

    if not chosen:
        info("Nothing selected.")
        print()
        return 0

    # ── scaffold chosen templates ─────────────────────────────────────────────
    print()
    project_name = cwd.name
    for name in chosen:
        tmpl = reg.get(name)
        info(f"Adding '{name}'...")
        written = tmpl.scaffold(project_name, cwd, dry_run=args.dry_run)
        for path in written:
            if args.dry_run:
                info(f"[dry] {path}")
            else:
                ok(str(path))

    if args.dry_run:
        print()
        info("Dry run — nothing written.")
    else:
        print()
        ok("Done.")
    print()
    return 0


def add_init_parser(sub) -> None:
    p = sub.add_parser(
        "init",
        help="Detect project type and add relevant config files",
    )
    p.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Add all suggestions without prompting",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without writing files",
    )
    p.set_defaults(func=cmd_init)
