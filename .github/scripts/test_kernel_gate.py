"""Unit checks for kernel_gate.py (run: python3 -m pytest .github/scripts).

Before 2026-10-18 a missing FC_PLATFORM_READ_TOKEN made BOTH pattern jobs
conclude success (geo-stab audit A2, D3): the nightly sweep in particular was
green every night without rendering a single cartridge. These checks pin the
replacement contract: the nightly FAILS without a kernel, a PR exits 0 only
after a warning annotation and a NOT VERIFIED summary, and the token value is
never echoed.
"""

import importlib.util
import pathlib

import pytest

spec = importlib.util.spec_from_file_location(
    "kernel_gate", pathlib.Path(__file__).with_name("kernel_gate.py"))
kg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kg)

SECRET = "github_pat_DO_NOT_PRINT_ME"


@pytest.mark.parametrize("token", [None, "", "   ", "\n"])
def test_nightly_without_kernel_fails(token):
    v = kg.decide(token, "nightly")
    assert v.available is False
    assert v.exit_code == 1
    assert any(line.startswith("::error ") for line in v.stdout)
    assert v.summary[0].startswith("### NOT VERIFIED: no kernel")


@pytest.mark.parametrize("token", [None, "", "  "])
def test_pr_without_kernel_warns_and_exits_zero(token):
    v = kg.decide(token, "pr")
    assert v.available is False
    assert v.exit_code == 0
    assert any(line.startswith("::warning ") for line in v.stdout)
    assert v.summary[0] == "### NOT VERIFIED: no kernel"
    # The summary must not read like a pass.
    assert "does not mean the patterns are verified" in "\n".join(v.summary)


def test_probe_without_kernel_only_reports_availability():
    v = kg.decide(None, "probe")
    assert (v.available, v.exit_code, v.summary) == (False, 0, [])


@pytest.mark.parametrize("lane", kg.LANES)
def test_token_present_runs_the_real_path(lane):
    v = kg.decide(SECRET, lane)
    assert v.available is True
    assert v.exit_code == 0
    assert v.summary == []
    assert not any(line.startswith("::") for line in v.stdout)


@pytest.mark.parametrize("lane", kg.LANES)
@pytest.mark.parametrize("token", [None, SECRET])
def test_token_value_is_never_printed(lane, token):
    v = kg.decide(token, lane)
    assert SECRET not in "\n".join(v.stdout + v.summary)


def test_unknown_lane_is_an_error():
    with pytest.raises(ValueError, match="unknown lane"):
        kg.decide(SECRET, "patterns")


def test_main_writes_output_and_summary(tmp_path, monkeypatch, capsys):
    out, summ = tmp_path / "out", tmp_path / "summary"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summ))
    monkeypatch.delenv(kg.TOKEN_ENV, raising=False)

    assert kg.main(["--lane", "nightly"]) == 1
    assert out.read_text() == "available=false\n"
    assert "NOT VERIFIED: no kernel" in summ.read_text()
    assert "::error " in capsys.readouterr().out

    out.unlink()
    summ.unlink()
    monkeypatch.setenv(kg.TOKEN_ENV, SECRET)
    assert kg.main(["--lane", "pr"]) == 0
    assert out.read_text() == "available=true\n"
    assert not summ.exists()
    assert SECRET not in capsys.readouterr().out
