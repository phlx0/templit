"""
templit.commands.manage
~~~~~~~~~~~~~~~~~~~~~~~
Commands for managing user templates:
  templit add      — interactive wizard
  templit import   — import a JSON file
  templit delete   — remove a user template
  templit export   — serialise a template to JSON
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from templit.base import Template, validate_template_name
from templit.color import DIM, CYAN, WHITE, BOLD, divider, err, info, ok, paint, warn
from templit.config import USER_TMPL, ensure_dirs
from templit.registry import get_registry, reset_registry


# ── add ──────────────────────────────────────────────────────────────────────

def cmd_add(args: argparse.Namespace) -> int:  # noqa: ARG001
    """Interactive wizard for creating a new user template."""
    ensure_dirs()
    print()
    print(paint("  Add a custom template", BOLD, CYAN))
    divider()

    name = input(paint("  Name (slug, e.g. my-config): ", WHITE)).strip()
    try:
        validate_template_name(name)
    except ValueError as exc:
        err(str(exc))
        return 1

    target = USER_TMPL / f"{name}.json"
    if target.exists():
        warn(f"Template '{name}' already exists — it will be overwritten.")

    desc     = input(paint("  Short description: ", WHITE)).strip()
    tags_raw = input(paint("  Tags (comma-separated, e.g. python,config): ", WHITE)).strip()
    tags     = [t.strip() for t in tags_raw.split(",") if t.strip()]

    print(paint("\n  Define the files for this template.", DIM))
    print(paint("  Use {{project}} as a placeholder for the project name.", DIM))
    print(paint("  Enter one file per block; blank filename = done.\n", DIM))

    files: dict[str, str] = {}
    while True:
        fname = input(paint("  File path (or ENTER to finish): ", WHITE)).strip()
        if not fname:
            break
        print(paint(f"  Paste content for '{fname}' (end block with a line containing only ---):", DIM))
        lines = []
        while True:
            line = input()
            if line == "---":
                break
            lines.append(line)
        files[fname] = "\n".join(lines) + "\n"
        ok(f"Added {fname}")

    if not files:
        err("No files defined. Template not saved.")
        return 1

    tmpl = Template(name=name, desc=desc, tags=tags, files=files, source="user")
    target.write_text(json.dumps(tmpl.to_dict(), indent=2), encoding="utf-8")
    reset_registry()    # force reload so the new template is visible immediately
    ok(f"Template '{name}' saved to {target}")
    print()
    return 0


def add_add_parser(sub) -> None:
    p = sub.add_parser("add", help="Add a custom template interactively")
    p.set_defaults(func=cmd_add)


# ── import ───────────────────────────────────────────────────────────────────

def cmd_import(args: argparse.Namespace) -> int:
    ensure_dirs()
    src = Path(args.file)
    if not src.exists():
        err(f"File not found: {args.file}")
        return 1

    # Validate stem as a template name
    try:
        validate_template_name(src.stem)
    except ValueError as exc:
        err(f"Invalid template filename: {exc}")
        return 1

    try:
        data = json.loads(src.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        err(f"Invalid JSON in template file: {exc}")
        return 1

    if "files" not in data or not isinstance(data["files"], dict):
        err("Template file is missing a 'files' dict.")
        return 1

    dest = USER_TMPL / f"{src.stem}.json"
    shutil.copy2(src, dest)
    reset_registry()
    ok(f"Imported '{src.stem}' → {dest}")
    return 0


def add_import_parser(sub) -> None:
    p = sub.add_parser("import", help="Import a JSON template file")
    p.add_argument("file", help="Path to .json template")
    p.set_defaults(func=cmd_import)


# ── delete ───────────────────────────────────────────────────────────────────

def cmd_delete(args: argparse.Namespace) -> int:
    target = USER_TMPL / f"{args.template}.json"
    if not target.exists():
        err(f"No user template named '{args.template}'.")
        return 1
    target.unlink()
    reset_registry()
    ok(f"Deleted user template '{args.template}'.")
    return 0


def add_delete_parser(sub) -> None:
    p = sub.add_parser("delete", aliases=["rm"], help="Delete a user template")
    p.add_argument("template", help="Template name")
    p.set_defaults(func=cmd_delete)


# ── export ───────────────────────────────────────────────────────────────────

def cmd_export(args: argparse.Namespace) -> int:
    reg  = get_registry()
    tmpl = reg.get(args.template)
    if tmpl is None:
        err(f"Template '{args.template}' not found.")
        return 1
    out = Path(args.output)
    out.write_text(json.dumps(tmpl.to_dict(), indent=2), encoding="utf-8")
    ok(f"Exported '{args.template}' → {out}")
    return 0


def add_export_parser(sub) -> None:
    p = sub.add_parser("export", help="Export a template to a JSON file")
    p.add_argument("template", help="Template name")
    p.add_argument("output",   help="Destination .json path")
    p.set_defaults(func=cmd_export)
