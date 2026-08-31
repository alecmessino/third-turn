#!/usr/bin/env python3
"""Supplementary / companion figures (talks, repo, social) — NOT part of the frozen paper.

    supp_line_movement.png  — one game's live total tracking the runs it scores. FROZEN RENDER
                              ONLY: its input is observation-level and withheld for rights
                              reasons, so this generator skips it and the committed image stands.
    supp_weather_diamond.png — the run-environment: how weather and park move fly-ball carry,
                              the physics the market already prices (and, in our data, over-adjusts)
    supp_weather_runs.png   — runs and over-rate by weather bucket, driven by the rights-safe
                              aggregate in paper/figdata/.

    python the_third_turn/docs/make_companion_figures.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict


class SkipFigure(RuntimeError):
    """Raised by a generator whose input is withheld for rights reasons."""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Wedge, Circle, FancyBboxPatch

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "paper"))
import figstyle as fs  # noqa: E402

AGG = Path(__file__).resolve().parent.parent / "paper" / "figdata"
OUT = HERE.parent / "output"
FIGDIR = HERE / "figures"
FIGDIR.mkdir(exist_ok=True)
GRASS, DIRT = "#D7E8D0", "#E7D7B4"


# ─────────────────────────────────────────────────────────────────────────────
# Line movement: the market's live total tracking the runs actually scored
# ─────────────────────────────────────────────────────────────────────────────
def line_movement(game_pk=823541):
    """FROZEN RENDER ONLY — not regenerable from the public package.

    RIGHTS. This figure plots one identified fixture's live line trajectory. Its input is
    irreducibly observation-level: a sequence of sharp-book lines keyed to an MLB game id.
    No aggregate can reproduce it without being that series. The series is therefore
    withheld pending written permission from the data provider, and the committed
    supp_line_movement.{svg,pdf,png} are the published artifact.

    There is deliberately no fallback to output/encompass_cache.json.
    """
    raise SkipFigure(
        "supp_line_movement is observation-level and ships as a frozen render; "
        "its source series is withheld pending data-provider permission")

def weather_diamond():
    fs.setup()
    fig, ax = plt.subplots(figsize=(fs.FULL_W, 5.0))
    ax.set_xlim(-9, 9); ax.set_ylim(-1.6, 11.2); ax.axis("off"); ax.set_aspect("equal")

    # field: grass wedge (foul lines at 45 and 135 deg) + dirt infield diamond
    ax.add_patch(Wedge((0, 0), 7.6, 45, 135, facecolor=GRASS, edgecolor="none", zorder=1))
    ax.add_patch(Wedge((0, 0), 7.6, 45, 135, width=0.12, facecolor=fs.MUTED, edgecolor="none", zorder=2))  # fence
    for a in (45, 135):  # foul lines
        r = np.deg2rad(a)
        ax.plot([0, 7.55 * np.cos(r)], [0, 7.55 * np.sin(r)], color="white", lw=1.6, zorder=2)
    dia = [(0, 0), (2.3, 2.3), (0, 4.6), (-2.3, 2.3)]
    ax.add_patch(Polygon(dia, closed=True, facecolor=DIRT, edgecolor="white", lw=1.6, zorder=3))
    for (bx, by) in dia[1:]:
        ax.add_patch(plt.Rectangle((bx - 0.16, by - 0.16), 0.32, 0.32, facecolor="white",
                                   edgecolor=fs.MUTED, lw=0.8, zorder=4))
    ax.add_patch(plt.Polygon([(-0.16, -0.02), (0.16, -0.02), (0.16, 0.14), (0, 0.28), (-0.16, 0.14)],
                             closed=True, facecolor="white", edgecolor=fs.MUTED, lw=0.8, zorder=4))  # home
    ax.add_patch(Circle((0, 2.3), 0.28, facecolor=DIRT, edgecolor="white", lw=1.2, zorder=4))  # mound

    # wind arrow, out to center
    ax.add_patch(FancyArrowPatch((0, 0.9), (0, 6.7), arrowstyle="-|>", mutation_scale=22,
                                 color=fs.PALETTE[0], lw=3.0, zorder=5, alpha=0.85))
    ax.text(0.35, 5.9, "WIND OUT", rotation=90, va="center", ha="left", color=fs.PALETTE[0],
            fontsize=10, fontweight="bold")
    ax.text(-0.4, 5.9, "10 · 20 · 30 mph", rotation=90, va="center", ha="right", color=fs.PALETTE[0],
            fontsize=8.5)

    def chip(x, y, title, body, col=fs.INK):
        ax.add_patch(FancyBboxPatch((x, y), 4.5, 1.5, boxstyle="round,pad=0.05,rounding_size=0.12",
                                    facecolor="#F6F6F4", edgecolor=fs.GRID, lw=1.0, zorder=6))
        ax.text(x + 0.22, y + 1.16, title, ha="left", va="center", color=col, fontsize=9.2,
                fontweight="bold", zorder=7)
        ax.text(x + 0.22, y + 0.5, body, ha="left", va="center", color=fs.MUTED, fontsize=8.5,
                zorder=7)

    chip(-8.7, 8.9, "Temperature", "warm air is thinner →\nball carries ~+2.5 ft per +10°F", fs.PALETTE[3])
    chip(4.2, 8.9, "Humidity", "humid air is LESS dense →\nslightly more carry (counter-intuitive)", fs.PALETTE[0])
    chip(-8.7, 0.1, "Wind to center", "out: more carry, more runs\nin: knocks fly balls down", fs.PALETTE[0])
    chip(4.2, 0.1, "Park factor", "100 = neutral · 112 = hitter\n120+ ≈ Coors (altitude, thin air)", fs.PALETTE[2])

    ax.text(0, 10.75, "The run environment: the physics the market already prices",
            ha="center", va="center", fontsize=12, fontweight="bold", color=fs.INK)
    ax.text(0, -1.15,
            # Split across two lines: as one line this caption set the figure's
            # cropped width to 7.8in against a 6.77in measure, shrinking every
            # label in the figure to 7.4pt on the page.
            "Fly-ball carry ≈ f(air density): temperature, altitude,\n"
            "barometric pressure, humidity, wind.  Denser air = less carry = fewer runs.",
            ha="center", va="center", fontsize=8.5, color=fs.INK,
            bbox=dict(facecolor="#F1F1EE", edgecolor=fs.GRID, boxstyle="round,pad=0.4"))
    fs.save_at_measure(fig, FIGDIR / "supp_weather_diamond.png")
    plt.close(fig)


def _wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, c - h), min(1.0, c + h))


def weather_runs():
    """Real sample: runs rise with hitter weather, but the over never reliably beats break-even.

    RIGHTS. Driven by a pre-computed aggregate of six weather buckets. The pregame line
    entered only through the comparison final > pre; its value is discarded in the
    aggregate. No fallback to output/encompass_cache.json.
    """
    agg = json.load(open(AGG / "fig_weather_runs_agg.json"))
    labels = ["wind in\n(≤ −4)", "calm", "wind out\n(≥ +4)",
              "cooler\n(< 75°)", "warm\n(75–84°)", "hot\n(≥ 85°)"]
    bk = agg["buckets"]
    runs = [b["mean_runs"] for b in bk]
    ns = [b["n_games"] for b in bk]
    hit = [b["over_rate_pct"] for b in bk]
    lo = [b["ci_lo_pct"] for b in bk]
    hi = [b["ci_hi_pct"] for b in bk]
    cols = [fs.PALETTE[0]] * 3 + [fs.PALETTE[3]] * 3

    fs.setup()
    fig, (axA, axR) = plt.subplots(1, 2, figsize=(fs.FULL_W, 4.2))
    x = np.arange(6)

    axA.bar(x, runs, color=cols, width=0.72, zorder=3)
    for xi, r, n in zip(x, runs, ns):
        axA.text(xi, r + 0.12, f"{r:.1f}", ha="center", va="bottom", fontsize=8.5, fontweight="bold")
        axA.text(xi, 0.35, f"n={n}", ha="center", va="bottom", color="white",
                 fontsize=8.5, fontweight="bold", zorder=4, rotation=90)
    axA.set_ylabel("mean runs scored per game")
    axA.set_ylim(0, max(runs) + 1.4)
    axA.set_xticks(x)
    axA.set_xticklabels(labels, fontsize=8.5, rotation=30, ha="right",
                        rotation_mode="anchor")
    axA.set_title("Runs rise with\nhitter-friendly weather", fontsize=10.6, pad=8)

    axR.bar(x, hit, color=cols, width=0.72, alpha=0.85, zorder=3)
    axR.errorbar(x, hit, yerr=[[h - l for h, l in zip(hit, lo)], [u - h for h, u in zip(hit, hi)]],
                 fmt="none", ecolor=fs.INK, elinewidth=1.3, capsize=4, zorder=4)
    axR.axhline(50, color=fs.MUTED, lw=1.1, ls="--")
    axR.axhline(52.38, color=fs.FAIL, lw=1.3, ls="--")
    axR.text(5.55, 50, "coin flip", va="center", ha="left", fontsize=8.5, color=fs.MUTED)
    axR.text(5.55, 52.6, "break-even", va="bottom", ha="left", fontsize=8.5, color=fs.FAIL)
    axR.set_ylabel("over hit-rate (%)")
    axR.set_ylim(28, 76)
    axR.set_xticks(x)
    axR.set_xticklabels(labels, fontsize=8.5, rotation=30, ha="right",
                        rotation_mode="anchor")
    axR.set_title("...but the over never\nreliably clears break-even", fontsize=10.6, pad=8)

    fig.suptitle("Weather moves runs; it does not move the price enough to beat it",
                 fontsize=11.6, fontweight="bold", y=1.10, wrap=True)
    fs.save_at_measure(fig, FIGDIR / "supp_weather_runs.png")
    plt.close(fig)


def main() -> int:
    wrote, skipped = [], []
    for fn, name in ((line_movement, "supp_line_movement"),
                     (weather_diamond, "supp_weather_diamond"),
                     (weather_runs, "supp_weather_runs")):
        try:
            fn(); wrote.append(name)
        except SkipFigure as e:
            skipped.append(f"{name}: {e}")
    print("wrote: " + ", ".join(f"{w}.png" for w in wrote))
    for msg in skipped:
        print(f"SKIPPED (frozen render retained) — {msg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
