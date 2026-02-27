"""
templit.color
~~~~~~~~~~~~~
ANSI color helpers. Import only what you need.

Terminal width is resolved lazily so it reflects the current window size
rather than the size at import time.
"""

import shutil
import sys

# ── codes ────────────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RED    = "\033[31m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
CYAN   = "\033[36m"
WHITE  = "\033[97m"


def _cols() -> int:
    """Return the current terminal width (resolved lazily)."""
    return shutil.get_terminal_size((80, 24)).columns


# ── primitives ───────────────────────────────────────────────────────────────

def paint(text: str, *codes: str) -> str:
    """Wrap *text* in ANSI *codes* and reset."""
    return "".join(codes) + text + RESET


def ok(msg: str)   -> None: print(paint("  ✓ ", GREEN, BOLD) + msg)
def err(msg: str)  -> None: print(paint("  ✗ ", RED,   BOLD) + msg, file=sys.stderr)
def info(msg: str) -> None: print(paint("  · ", CYAN,  DIM)  + msg)
def warn(msg: str) -> None: print(paint("  ! ", YELLOW, BOLD) + msg)


def divider(ch: str = "─") -> None:
    print(paint(ch * _cols(), DIM))


def header() -> None:
    from templit import __version__
    banner = " templit "
    cols   = _cols()
    pad    = (cols - len(banner)) // 2
    print()
    print(" " * pad + paint(banner, BOLD, CYAN))
    print(paint(f"  template scaffolding v{__version__}".center(cols), DIM))
    print()


def fmt_tags(tags: list[str]) -> str:
    return "  ".join(paint(f"#{t}", DIM, CYAN) for t in tags)
