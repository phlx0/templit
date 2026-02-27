# Contributing to templit

First off — thank you for taking the time to contribute. Every template, bug fix, and idea makes templit better for everyone.

---

## Ways to contribute

- **Add a template** — the most impactful contribution. See below.
- **Report a bug** — open an issue using the bug report template.
- **Suggest a feature** — open an issue using the feature request template.
- **Improve the docs** — fix typos, clarify explanations, improve examples.
- **Fix a bug** — pick an open issue and open a pull request.

---

## Setup

```bash
git clone https://github.com/yourname/templit.git
cd templit
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Verify it works:

```bash
templit list
```

---

## Adding a built-in template

This is the easiest way to contribute and requires no Python knowledge.

1. Create a new `.json` file in `templit/templates/`:

```json
{
  "desc": "A short one-line description",
  "tags": ["relevant", "tags"],
  "files": {
    "README.md": "# {{project}}\n",
    "src/{{project}}/main.py": "def main(): pass\n"
  }
}
```

2. Use `{{project}}` as a placeholder — it gets replaced with the project name at scaffold time. It works in both file paths and file contents.

3. Test it:

```bash
templit list                              # should appear in the list
templit use your-template-name test --dry-run  # preview the files
templit use your-template-name test           # scaffold for real
```

4. Add it to the template table in `README.md`.

5. Open a pull request.

**Good templates are:**
- Generic enough that most people using that stack would want them
- Minimal — the starting point, not the finished product
- Well-tagged so they show up in searches

---

## Code changes

- Follow the existing code style — run `ruff check .` before committing
- Keep `cli.py` thin — it only wires things, no logic
- New subcommands go in their own file in `commands/`
- New template sources subclass `TemplateSource` from `base.py`

---

## Opening a pull request

1. Fork the repo and create a branch: `git checkout -b my-feature`
2. Make your changes
3. Test manually: `templit list`, `templit use ...`, `templit init`
4. Open a pull request with a clear description of what you changed and why

---

## Questions?

Open an issue — no question is too small.
