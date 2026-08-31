"""Rights gate: no third-party observation may become publicly tracked again.

This test exists because `data/trajectories.jsonl` (163 fixtures, 32,880 quoted-price
observations), `data/closing_lines.csv`, and four derived caches embedding verbatim
sharp-book lines were published here in error and had to be removed from every commit
by a history rewrite on 2026-08-31.

It fails on two independent signals, so a rename alone cannot defeat it:
  1. a restricted FILENAME becoming tracked again;
  2. any tracked JSON/CSV/JSONL carrying observation-level field names, regardless of path.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

RESTRICTED_NAMES = {
    "trajectories.jsonl", "closing_lines.csv", "features_cache.json",
    "encompass_cache.json", "handoff_backtest.json", "program_a_cache.json",
    "remaining_snapshots.json", "starter_tiers.json",
    "book_panel.jsonl", "game_state_panel.jsonl", "team_total_panel.jsonl",
    "market_provenance.jsonl", "provenance_probe.jsonl", "ledger.jsonl",
}
RESTRICTED_PREFIXES = ("book_panel.", "game_state_panel.", "provenance_probe.",
                       "market_provenance.", "team_total_panel.")

# Field names that only appear in per-observation records.
OBSERVATION_FIELDS = {
    "over_dec", "under_dec", "over_odds", "under_odds", "fixture_id",
    "line_at_exit", "line_by_inn", "x_cache", "cache_control",
    "recv_minus_server_s", "server_date", "market_id", "event_id",
}


def tracked() -> list[str]:
    out = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                         capture_output=True, text=True, check=True).stdout
    return [l for l in out.splitlines() if l.strip()]


def test_no_restricted_filenames_tracked():
    bad = [p for p in tracked()
           if Path(p).name in RESTRICTED_NAMES
           or Path(p).name.startswith(RESTRICTED_PREFIXES)]
    assert not bad, (
        "Restricted third-party data files are tracked publicly again: "
        f"{bad}. These carry sportsbook quotes or bulk MLBAM records and may not be "
        "redistributed. Keep them in the private research repository.")


@pytest.mark.parametrize("suffix", [".json", ".jsonl", ".csv"])
def test_no_observation_level_fields_tracked(suffix):
    offenders = []
    for rel in tracked():
        if not rel.endswith(suffix):
            continue
        f = ROOT / rel
        if not f.is_file() or f.stat().st_size > 8_000_000:
            continue
        head = f.read_text(errors="replace")[:200_000]
        hits = sorted(k for k in OBSERVATION_FIELDS if f'"{k}"' in head or f",{k}," in head)
        # figdata files name these words only in their prose description
        if hits and not rel.startswith("paper/figdata/"):
            offenders.append((rel, hits))
    assert not offenders, (
        f"Observation-level third-party fields found in tracked {suffix} files: "
        f"{offenders}. Publish aggregates instead.")


def test_aggregate_inputs_are_present_and_non_reconstructive():
    """The published figure inputs must exist and must stay aggregate."""
    for name, minimum in (("fig_market_calibration_agg.json", 100),
                          ("fig_weather_runs_agg.json", 10)):
        f = ROOT / "paper" / "figdata" / name
        assert f.is_file(), f"missing rights-safe aggregate {name}"
        blob = json.loads(f.read_text())
        assert "_description" in blob
        if "reliability_bins" in blob:
            assert min(b["n"] for b in blob["reliability_bins"]) >= 5, \
                "a reliability bin is small enough to disclose an individual observation"
            assert blob["_n_snapshots"] >= minimum
        if "buckets" in blob:
            assert min(b["n_games"] for b in blob["buckets"]) >= 5, \
                "a weather bucket is small enough to disclose an individual game"


def test_figure_generators_have_no_fallback_to_restricted_caches():
    """A rewired generator must never reach for the private cache if the aggregate is gone.

    Checked against the parsed AST. Every string constant EXCEPT a docstring is examined,
    so ``_load("encompass_cache.json")`` trips it while a docstring that merely describes
    the old input does not. Comments never enter the AST and are excluded for free.
    """
    import ast

    banned = ("encompass_cache", "features_cache", "program_a_cache",
              "trajectories", "closing_lines", "remaining_snapshots")

    for rel in ("paper/make_figures.py", "docs/make_companion_figures.py"):
        tree = ast.parse((ROOT / rel).read_text())
        docstrings = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                body = getattr(node, "body", None)
                if body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) \
                        and isinstance(body[0].value.value, str):
                    docstrings.add(id(body[0].value))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
                continue
            if id(node) in docstrings:
                continue
            for b in banned:
                assert b not in node.value, (
                    f"{rel} line {node.lineno}: executable code references the restricted "
                    f"input {b!r} ({node.value!r}). Figures must be driven from "
                    f"paper/figdata/ aggregates only, with no fallback.")
