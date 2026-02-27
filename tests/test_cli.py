"""Smoke tests for the CLI entry-point."""

from __future__ import annotations

from templit.cli import main


def test_no_args_returns_0() -> None:
    assert main([]) == 0


def test_version_flag(capsys) -> None:
    try:
        main(["--version"])
    except SystemExit as exc:
        assert exc.code == 0
    captured = capsys.readouterr()
    assert "templit" in captured.out


def test_list_returns_0() -> None:
    assert main(["list"]) == 0


def test_list_search_returns_0() -> None:
    assert main(["list", "--search", "python"]) == 0


def test_show_unknown_template_returns_1() -> None:
    assert main(["show", "this-does-not-exist-xyz"]) == 1


def test_use_unknown_template_returns_1() -> None:
    assert main(["use", "this-does-not-exist-xyz", "proj"]) == 1
