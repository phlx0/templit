"""
templit.commands.list
~~~~~~~~~~~~~~~~~~~~~
`templit list` and `templit show` subcommands.
"""

from __future__ import annotations

import argparse

from templit.color import (
    BOLD, CYAN, DIM, GREEN, WHITE,
    RESET,
    divider, fmt_tags, header, info, paint,
)
from templit.registry import get_registry


# ── list ─────────────────────────────────────────────────────────────────────

def cmd_list(args: argparse.Namespace) -> int:
    reg     = get_registry()
    matches = reg.search(query=args.search, tag=args.tag)

    header()
    divider()

    for name, tmpl in matches.items():
        src_label = (
            paint("user", GREEN, BOLD)
            if tmpl.source == "user"
            else paint("builtin", DIM)
        )
        print(f"  {paint(name, WHITE, BOLD):<36}  {paint(tmpl.desc, DIM)}")
        print(f"  {'':<36}  {fmt_tags(tmpl.tags)}  [{src_label}]")
        print()

    divider()
    suffix = ""
    if args.search or args.tag:
        q = args.search or args.tag
        suffix = f"  ·  filter: {paint(q, CYAN)}"
    print(f"  {paint(str(len(matches)), CYAN, BOLD)} template(s) listed{suffix}")
    print()
    return 0


def add_list_parser(sub) -> None:
    p = sub.add_parser("list", aliases=["ls"], help="List available templates")
    p.add_argument("-s", "--search", metavar="QUERY", default="",
                   help="Filter by name / description / tag")
    p.add_argument("-t", "--tag", metavar="TAG", default="",
                   help="Filter by exact tag")
    p.set_defaults(func=cmd_list)


# ── show ─────────────────────────────────────────────────────────────────────

def cmd_show(args: argparse.Namespace) -> int:
    reg  = get_registry()
    tmpl = reg.get(args.template)
    if tmpl is None:
        from templit.color import err
        err(f"Template '{args.template}' not found.")
        return 1

    header()
    divider()
    print(f"  {paint(tmpl.name, CYAN, BOLD)}  —  {tmpl.desc}")
    print(f"  {fmt_tags(tmpl.tags)}")
    divider()
    for fname in tmpl.files:
        print(f"  {paint(fname, WHITE)}")
    print()
    return 0


def add_show_parser(sub) -> None:
    p = sub.add_parser("show", help="Show files contained in a template")
    p.add_argument("template", help="Template name")
    p.set_defaults(func=cmd_show)
