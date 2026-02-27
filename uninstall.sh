#!/usr/bin/env bash
# uninstall.sh — remove templit completely
set -uo pipefail

# ── colors ───────────────────────────────────────────────────────────────────
BOLD="\033[1m"; CYAN="\033[36m"; GREEN="\033[32m"
RED="\033[31m"; DIM="\033[2m"; YELLOW="\033[33m"; RESET="\033[0m"

ok()   { echo -e "${GREEN}${BOLD}  ✓ ${RESET}$*"; }
info() { echo -e "${CYAN}${DIM}  · ${RESET}$*"; }
warn() { echo -e "${YELLOW}${BOLD}  ! ${RESET}$*"; }

banner() {
  echo ""
  echo -e "${CYAN}${BOLD}  templit uninstaller${RESET}"
  echo -e "${DIM}  ──────────────────────────────${RESET}"
  echo ""
}

# ── config ───────────────────────────────────────────────────────────────────
INSTALL_DIR="$HOME/.templit"
USER_TMPL="$HOME/.config/templit"
BIN_LINKS=(
  "/usr/local/bin/templit"
  "$HOME/.local/bin/templit"
)

# ── confirm ──────────────────────────────────────────────────────────────────
banner
echo -e "  This will remove:"
echo -e "  ${DIM}• $INSTALL_DIR  (virtualenv + package)${RESET}"
echo -e "  ${DIM}• any templit symlinks on your PATH${RESET}"
echo ""
read -rp "  Continue? [y/N] " confirm
echo ""
if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
  echo "  Aborted."
  echo ""
  exit 0
fi

# ── remove symlinks ──────────────────────────────────────────────────────────
for link in "${BIN_LINKS[@]}"; do
  if [ -L "$link" ]; then
    rm "$link" && ok "Removed symlink $link"
  elif [ -f "$link" ]; then
    rm "$link" && ok "Removed binary $link"
  fi
done

# catch any other templit still on PATH
EXTRA=$(command -v templit 2>/dev/null || true)
if [ -n "$EXTRA" ]; then
  warn "Found another templit at $EXTRA — removing..."
  rm -f "$EXTRA" && ok "Removed $EXTRA"
fi

# ── remove virtualenv ────────────────────────────────────────────────────────
if [ -d "$INSTALL_DIR" ]; then
  info "Removing $INSTALL_DIR ..."
  rm -rf "$INSTALL_DIR"
  ok "Removed $INSTALL_DIR"
else
  warn "$INSTALL_DIR not found — skipping"
fi

# ── user templates (optional) ────────────────────────────────────────────────
if [ -d "$USER_TMPL" ]; then
  echo ""
  read -rp "  Also delete your user templates at $USER_TMPL? [y/N] " del_tmpl
  echo ""
  if [[ "$del_tmpl" =~ ^[Yy]$ ]]; then
    rm -rf "$USER_TMPL"
    ok "Removed $USER_TMPL"
  else
    info "Kept $USER_TMPL"
  fi
fi

# ── verify ───────────────────────────────────────────────────────────────────
if command -v templit &>/dev/null; then
  warn "templit still found at $(command -v templit) — open a new shell session to clear it"
else
  ok "templit is no longer on PATH"
fi

echo ""
echo -e "${GREEN}${BOLD}  Done.${RESET}"
echo ""
