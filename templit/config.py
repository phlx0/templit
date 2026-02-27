"""
templit.config
~~~~~~~~~~~~~~
All paths and persistent config live here.
Nothing else should import Path("/home/...") directly.
"""

import json
from pathlib import Path

from templit import __version__

CONFIG_DIR  = Path.home() / ".config" / "templit"
USER_TMPL   = CONFIG_DIR / "templates"
CONFIG_FILE = CONFIG_DIR / "config.json"


def ensure_dirs() -> None:
    """Create config directories if they do not exist yet."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    USER_TMPL.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(
            json.dumps({"version": __version__}, indent=2),
            encoding="utf-8",
        )


def load_config() -> dict:
    ensure_dirs()
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


def save_config(data: dict) -> None:
    ensure_dirs()
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")
