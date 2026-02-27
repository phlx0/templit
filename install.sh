#!/usr/bin/env bash
# install.sh — install templit and add it to PATH
set -euo pipefail

# ── colors ───────────────────────────────────────────────────────────────────
BOLD="\033[1m"; CYAN="\033[36m"; GREEN="\033[32m"
RED="\033[31m"; DIM="\033[2m"; RESET="\033[0m"

ok()   { echo -e "${GREEN}${BOLD}  ✓ ${RESET}$*"; }
err()  { echo -e "${RED}${BOLD}  ✗ ${RESET}$*" >&2; exit 1; }
info() { echo -e "${CYAN}${DIM}  · ${RESET}$*"; }
banner() {
  echo ""
  echo -e "${CYAN}${BOLD}  templit installer${RESET}"
  echo -e "${DIM}  ──────────────────────────────${RESET}"
  echo ""
}

# ── config ───────────────────────────────────────────────────────────────────
INSTALL_DIR="$HOME/.templit"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── checks ───────────────────────────────────────────────────────────────────
banner
info "Checking requirements..."

command -v python3 &>/dev/null || err "python3 not found. Please install Python 3.9+."

PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)

[[ "$PY_MAJOR" -ge 3 && "$PY_MINOR" -ge 9 ]] \
  || err "Python 3.9+ required (found $PY_VERSION)."
ok "Python $PY_VERSION"

# ── virtualenv ───────────────────────────────────────────────────────────────
info "Creating virtualenv at $INSTALL_DIR ..."
python3 -m venv "$INSTALL_DIR"
ok "Virtualenv ready"

# ── install package ──────────────────────────────────────────────────────────
info "Installing templit..."
"$INSTALL_DIR/bin/pip" install --quiet --upgrade pip
"$INSTALL_DIR/bin/pip" install --quiet -e "$SCRIPT_DIR"
ok "Package installed"

# ── add to PATH ──────────────────────────────────────────────────────────────
# add_to_path <dir>
#   Appends the venv bin dir to the user's shell rc so `templit` is
#   available in every new shell session — nothing else from the venv leaks.
add_to_path() {
  local bin_dir="$1"
  local shell_rc

  if echo "$SHELL" | grep -q "zsh"; then
    shell_rc="$HOME/.zshrc"
  else
    shell_rc="$HOME/.bashrc"
  fi

  if ! grep -qF "$bin_dir" "$shell_rc" 2>/dev/null; then
    echo ""                                 >> "$shell_rc"
    echo "# templit"                        >> "$shell_rc"
    echo "export PATH=\"$bin_dir:\$PATH\"" >> "$shell_rc"
    ok "Added to PATH in $shell_rc"
  else
    ok "Already in $shell_rc — skipping"
  fi
}

info "Adding templit to PATH..."
add_to_path "$INSTALL_DIR/bin"

# also export for the current session so it works right away
export PATH="$INSTALL_DIR/bin:$PATH"

# ── done ─────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}  All done!${RESET} Run: ${BOLD}templit list${RESET}"
echo -e "  ${DIM}(or open a new terminal if the command isn't found yet)${RESET}"
echo ""
