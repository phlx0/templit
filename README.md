<div align="center">

# ⚡ templit

**Stop writing boilerplate. Start building.**

[![Python](https://img.shields.io/badge/python-3.9+-blue?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-orange?style=flat-square)](pyproject.toml)

*A minimal CLI that scaffolds real project structures in seconds —  
no config files, no templating languages, no nonsense.*

```bash
templit use python-fastapi myapp --git
```

</div>

---

## Why templit?

Every new project starts the same way. You create the same files, copy the same configs, set up the same folder structure — before writing a single line of actual code.

Templit skips all of that.

```
$ templit use react-app my-dashboard --git

  · Scaffolding 'react-app' → my-dashboard/
  
  ✓ my-dashboard/package.json
  ✓ my-dashboard/vite.config.ts
  ✓ my-dashboard/tsconfig.json
  ✓ my-dashboard/index.html
  ✓ my-dashboard/src/main.tsx
  ✓ my-dashboard/src/App.tsx
  ✓ my-dashboard/README.md
  ✓ git init

  ✓ Done! Your project is at my-dashboard/
```

---

## Installation

```bash
git clone https://github.com/yourname/templit.git
cd templit
chmod +x install.sh && ./install.sh
```

Templit installs into an isolated virtualenv at `~/.templit` and adds itself to your `$PATH` automatically. Open a new terminal and you're ready.

**Requires Python 3.9+** — no other dependencies.

```bash
# to uninstall cleanly
./uninstall.sh
```

---

## Commands

### `templit list` — browse templates

```bash
templit list                     # show everything
templit list --search api        # search by name, description, or tag
templit list --tag python        # filter by tag
templit show python-fastapi      # inspect files inside a template
```

### `templit use` — scaffold a new project

```bash
templit use python-fastapi myapp
templit use python-fastapi myapp --git          # also run git init
templit use python-cli mytool --dest ~/projects # custom destination
templit use react-app mysite --dry-run          # preview before writing
```

### `templit init` — improve an existing project

Drop this into any folder. Templit detects what's already there and suggests the config files you're missing — `.gitignore`, `Makefile`, CI workflows, `Dockerfile`, and more. Skips anything you already have.

```bash
cd my-existing-project
templit init            # pick what to add interactively
templit init --yes      # add everything suggested
templit init --dry-run  # preview first
```

### `templit add` / `import` / `export` — manage your own templates

```bash
templit add                         # interactive wizard
templit import ./my-template.json   # import from a file
templit export python-cli out.json  # export any template
templit delete my-template          # remove a user template
```

Your custom templates live in `~/.config/templit/templates/` and override any built-in with the same name.

---

## Built-in templates

| Name | Description | Tags |
|---|---|---|
| `python-basic` | Minimal Python project (src layout) | python |
| `python-cli` | Python CLI with argparse + logging | python, cli |
| `python-fastapi` | FastAPI REST API with Pydantic v2 | python, web, api |
| `python-pytest` | pytest scaffold with conftest | python, testing |
| `node-basic` | Minimal Node.js ESM project | node, javascript |
| `node-express` | Express.js REST API skeleton | node, javascript, api |
| `go-basic` | Minimal Go module | go |
| `go-cli` | Go CLI app with cobra | go, cli |
| `rust-basic` | Minimal Rust binary crate | rust |
| `rust-cli` | Rust CLI app with clap | rust, cli |
| `react-app` | React + Vite + TypeScript | react, typescript, web |
| `github-pages` | Static site with auto-deploy workflow | web, github |
| `dockerfile-python` | Production Dockerfile for Python | docker, devops |
| `github-actions-python` | CI workflow — lint + test | ci, github, python |
| `makefile-python` | Makefile for Python projects | python, devops |
| `editorconfig` | `.editorconfig` for consistent style | config |
| `gitignore-python` | Comprehensive Python `.gitignore` | git, python |
| `pre-commit` | pre-commit hooks (ruff, mypy) | python, git |

---

## Custom templates

Templates are plain JSON — no templating language to learn. Use `{{project}}` anywhere in file paths or content as a placeholder for your project name.

```json
{
  "desc": "My team's standard API setup",
  "tags": ["internal", "python"],
  "files": {
    "README.md": "# {{project}}\n",
    "src/{{project}}/__init__.py": "",
    "src/{{project}}/main.py": "def main(): pass\n"
  }
}
```

```bash
templit add                       # guided setup
templit import ./my-template.json # or import directly
```

---

## Adding a built-in template

Drop a `.json` file into `templit/templates/` — no Python needed. It shows up in `templit list` automatically.

---

## Project structure

```
templit/
├── templates/           built-in templates (plain JSON)
├── sources/
│   ├── builtin.py       loads templates/ at runtime
│   └── disk.py          loads ~/.config/templit/templates/
├── commands/
│   ├── init.py          project detection + suggestions
│   ├── use.py           scaffold + --git
│   ├── list.py          list + show
│   └── manage.py        add, import, export, delete
├── base.py              Template dataclass + TemplateSource ABC
├── registry.py          merges all sources into one namespace
├── cli.py               argparse entry-point
├── color.py             ANSI output helpers
└── config.py            filesystem paths
```

---

## Contributing

Contributions are welcome — especially new templates.

The easiest way to contribute is to add a template for a stack you use. Just create a `.json` file in `templit/templates/`, following the format above, and open a pull request.

---

<div align="center">

Made with ☕ · MIT License

</div>
