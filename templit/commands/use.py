"""
templit.commands.use
~~~~~~~~~~~~~~~~~~~~
`templit use <template> <project>` — scaffold files into a directory.
"""

from __future__ import annotations

import argparse
import logging
import subprocess
from pathlib import Path

from templit.color import err, info, ok, warn
from templit.registry import get_registry

logger = logging.getLogger(__name__)


def cmd_use(args: argparse.Namespace) -> int:
    reg  = get_registry()
    tmpl = reg.get(args.template)
    if tmpl is None:
        err(f"Template '{args.template}' not found. Run `templit list` to browse.")
        return 1

    dest = Path(args.dest) / args.project
    if not args.dry_run:
        dest.mkdir(parents=True, exist_ok=True)

    print()
    info(f"Scaffolding '{args.template}' → {dest}/")
    print()

    written = tmpl.scaffold(
        args.project,
        dest,
        dry_run=args.dry_run,
        overwrite=getattr(args, "overwrite", False),
    )

    for path in written:
        if args.dry_run:
            info(f"[dry] {path}")
        else:
            ok(str(path))

    # Report files that were skipped (exist and no --overwrite)
    all_paths = [
        dest / tmpl.render_path(rel, args.project)
        for rel in tmpl.files
    ]
    skipped = [p for p in all_paths if p not in written and not args.dry_run and p.exists()]
    for path in skipped:
        warn(f"Skip (exists): {path}")

    if not args.dry_run:
        if args.git:
            _git_init(dest)
        print()
        ok(f"Done! Your project is at {dest}")
    print()
    return 0


def _git_init(dest: Path) -> None:
    """Run `git init` inside *dest* if git is available."""
    try:
        result = subprocess.run(
            ["git", "init", str(dest)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            ok("git init")
        else:
            warn(f"git init failed: {result.stderr.strip()}")
    except FileNotFoundError:
        warn("git not found — skipping git init")


def add_use_parser(sub) -> None:
    p = sub.add_parser("use", help="Scaffold a template into a directory")
    p.add_argument("template", help="Template name (see `templit list`)")
    p.add_argument("project",  help="Project / output name")
    p.add_argument("--dest", metavar="DIR", default=".",
                   help="Parent directory to scaffold into (default: .)")
    p.add_argument("--dry-run", action="store_true",
                   help="Print what would be written without touching disk")
    p.add_argument("--git", action="store_true",
                   help="Run git init after scaffolding")
    p.add_argument("--overwrite", action="store_true",
                   help="Overwrite existing files instead of skipping them")
    p.set_defaults(func=cmd_use)
