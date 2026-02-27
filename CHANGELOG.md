# Changelog

All notable changes to this project will be documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.2.0] - 2026-02-27

### Added
- `templit init` — detects existing project type and suggests missing config files
- `--git` flag on `templit use` to run `git init` automatically after scaffolding
- 6 new templates: `go-basic`, `go-cli`, `rust-basic`, `rust-cli`, `react-app`, `github-pages`
- Built-in templates are now plain JSON files in `templit/templates/` — no Python needed to add one
- `--dry-run` flag on `templit init`
- `-y` / `--yes` flag on `templit init` to skip prompts

### Changed
- Built-in template definitions moved from `sources/builtin.py` to individual `.json` files
- `pyproject.toml` updated to use `setuptools.build_meta` backend (fixes Python 3.14 compatibility)

### Fixed
- `uninstall.sh` no longer aborts early when a symlink is not found

---

## [0.1.0] - 2026-02-27

### Added
- Initial release
- 12 built-in templates for Python, Node.js, Docker, CI, and config files
- `templit list` with `--search` and `--tag` filters
- `templit show` to inspect template contents
- `templit use` to scaffold a project
- `templit add` interactive wizard for custom templates
- `templit import` / `export` / `delete` for managing user templates
- User templates stored in `~/.config/templit/templates/`
- `install.sh` and `uninstall.sh`
