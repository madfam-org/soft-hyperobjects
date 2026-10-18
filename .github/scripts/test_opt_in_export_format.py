"""Unit checks for opt_in_export_format.py (run: python3 -m pytest .github/scripts).

The sweep rewrites 500+ hand-authored manifests, so the properties it claims are
pinned here: canonical order from the keystone enum, byte-preserving outside the
`export_formats` array, idempotent, and fail-visible on anything it cannot
place. Needs the keystone (`fc_spec`) installed, as the CI job that runs it does.
"""

import importlib.util
import json
import pathlib

import pytest

spec = importlib.util.spec_from_file_location(
    "opt_in_export_format", pathlib.Path(__file__).with_name("opt_in_export_format.py"))
oi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oi)

ORDER = ["svg", "dxf", "dxf-aama", "json", "pdf"]

EXPANDED = """{
  "project": {"slug": "x"},
  "export_formats": [
    "svg",
    "dxf",
    "json",
    "pdf"
  ],
  "fabrics": ["cotton-jersey"]
}
"""
ONE_LINE = '{\n  "export_formats": ["svg", "dxf", "json", "pdf"],\n  "x": 1\n}\n'


def test_the_keystone_enum_is_the_canonical_order():
    assert oi.canonical_order() == ORDER


def test_expanded_array_gains_the_format_in_place_and_nothing_else_moves():
    out = oi.opt_in(EXPANDED, "dxf-aama", ORDER)
    assert json.loads(out)["export_formats"] == ORDER
    assert out == EXPANDED.replace('    "dxf",\n', '    "dxf",\n    "dxf-aama",\n')


def test_one_line_array_keeps_its_style():
    out = oi.opt_in(ONE_LINE, "dxf-aama", ORDER)
    assert out == ONE_LINE.replace('"dxf", "json"', '"dxf", "dxf-aama", "json"')


def test_idempotent():
    once = oi.opt_in(EXPANDED, "dxf-aama", ORDER)
    assert oi.opt_in(once, "dxf-aama", ORDER) == once


def test_refuses_unknown_entries_and_a_missing_field():
    with pytest.raises(ValueError, match="does not know"):
        oi.opt_in('{\n  "export_formats": ["svg", "hpgl"]\n}', "dxf-aama", ORDER)
    with pytest.raises(ValueError, match="no 'export_formats'"):
        oi.opt_in('{"x": 1}', "dxf-aama", ORDER)


def _commons(tmp_path):
    for slug, text in (("a", EXPANDED), ("b", ONE_LINE), ("c", EXPANDED)):
        (tmp_path / slug).mkdir()
        (tmp_path / slug / "project.json").write_text(text, encoding="utf-8")
    skip = tmp_path / "skip.txt"
    skip.write_text("# deferred\nc  # piece \"back\" has no grainline\n", encoding="utf-8")
    return skip


def test_main_applies_skips_and_is_idempotent(tmp_path, capsys):
    skip = _commons(tmp_path)
    args = ["dxf-aama", "--skip-file", str(skip)]
    assert oi.main(args + ["--check"], root=tmp_path) == 1
    assert "would_add=2" in capsys.readouterr().out
    assert oi.main(args, root=tmp_path) == 0
    assert "added=2 already=0 skipped=1 problems=0" in capsys.readouterr().out
    assert (tmp_path / "c" / "project.json").read_text(encoding="utf-8") == EXPANDED
    assert oi.main(args + ["--check"], root=tmp_path) == 0
    assert "would_add=0 already=2 skipped=1" in capsys.readouterr().out


def test_main_fails_visible(tmp_path, capsys):
    skip = _commons(tmp_path)
    skip.write_text("ghost  # no such cartridge\n", encoding="utf-8")
    assert oi.main(["dxf-aama", "--skip-file", str(skip)], root=tmp_path) == 1
    assert "skip-file names 'ghost'" in capsys.readouterr().out
    assert oi.main(["hpgl"], root=tmp_path) == 1
    empty = tmp_path / "empty"
    empty.mkdir()
    assert oi.main(["dxf-aama"], root=empty) == 1


def test_the_committed_skip_file_names_real_cartridges():
    root = pathlib.Path(__file__).resolve().parents[2]
    skip = oi.read_skip_file(pathlib.Path(__file__).with_name("dxf-aama-deferred.txt"))
    assert skip, "the deferred list is empty — delete the file instead"
    for slug, reason in skip.items():
        assert (root / slug / "project.json").is_file(), slug
        assert reason, f"{slug}: a deferral needs its reason"
