"""
templit.cli
~~~~~~~~~~~
Argument parser and main() entry-point.
Each subcommand is registered by its own module; this file only wires them.
"""

from __future__ import annotations

import argparse
import logging
import sys
import textwrap

from templit import __version__
from templit.color import BOLD, paint
from templit.config import ensure_dirs

from templit.commands.list   import add_list_parser, add_show_parser
from templit.commands.use    import add_use_parser
from templit.commands.init   import add_init_parser
from templit.commands.manage import (
    add_add_parser,
    add_import_parser,
    add_delete_parser,
    add_export_parser,
)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="templit",
        description=paint("templit — fast project template scaffolding", BOLD),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              templit list
              templit list --search api
              templit list --tag python
              templit show python-fastapi
              templit use  python-fastapi myapp
              templit use  python-fastapi myapp --git
              templit use  python-cli mytool --dest ~/projects
              templit init
              templit init --yes
              templit add
              templit import ./my-template.json
              templit export python-cli ./backup.json
              templit delete my-template
        """),
    )
    p.add_argument("-V", "--version", action="version",
                   version=f"templit {__version__}")
    p.add_argument(
        "--log-level",
        default="WARNING",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set logging verbosity (default: WARNING)",
    )

    sub = p.add_subparsers(dest="cmd", metavar="<command>")
    sub.required = False

    add_list_parser(sub)
    add_show_parser(sub)
    add_use_parser(sub)
    add_init_parser(sub)
    add_add_parser(sub)
    add_import_parser(sub)
    add_delete_parser(sub)
    add_export_parser(sub)

    return p


def main(argv: list[str] | None = None) -> int:
    ensure_dirs()
    parser = build_parser()
    args   = parser.parse_args(argv)

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(name)s: %(message)s",
    )

    if not args.cmd:
        parser.print_help()
        print()
        return 0

    try:
        return args.func(args)
    except KeyboardInterrupt:
        print()
        return 130
    except Exception as exc:
        from templit.color import err
        err(f"Unexpected error: {exc}")
        logging.debug("Traceback:", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
