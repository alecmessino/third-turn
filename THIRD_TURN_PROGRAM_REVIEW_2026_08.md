# The Third Turn — Program Review

**Date of review:** 2026-08-22
**Repository state reviewed:** `alecmessino/third-turn`, commit `82fc298` ("The Third Turn v1.0 — protocol, benchmark dataset, and Paper 1 reproduction"), authored and committed **2026-07-29T02:47:12Z**. Single commit; branch `main` only; **no tags, no releases** (verified against the GitHub API, 2026-08-22).
**As-of timestamp for all computed counts:** **2026-08-22T17:13:06Z** (working tree at `82fc298`).
**Status of this document:** program-level assessment. It **adds no analysis to, and changes nothing in**, any frozen artifact, methodology document, gate, governance register, or historical record. Every recommendation below is a recommendation, not an applied edit.

---

## 0. Reading key — evidence classes used throughout

| Class | Meaning |
|---|---|
| **[FACT]** | Verified directly against this repository during this review, with the command or file cited. |
| **[RECORD]** | Asserted by a committed project document (ledger, register, report). Trustworthy as a record of what was believed and when; not independently re-verified here unless marked. |
| **[GAP]** | The repository does not contain what would be needed to answer. Stated as absence, never filled by inference. |
| **[JUDGMENT]** | My assessment, labelled as such, resting on the facts cited beside it. |

---

# 1. Executive assessment

## 1.1 The single most important finding: the mandate's Paper 2 frame is not in this repository

The review mandate instructs me to "use Outcome C and GD-21 as authoritative," to confirm the disposition of a bounded QC list, to check `§5.3`/`§7.4` consistency in Paper 2, to verify that `λ_price`, `λ_feed`, `λ_deliv` and `λ_samp` remain distinct, and to adjudicate Conditions 1, 2 and 4 as GD-21-scoped non-passes.

**None of that exists in this repository.** [FACT]

| Mandate object | Repository state |
|---|---|
| `GD-21` | Governance Decision Log ends at **GD-14 (2026-07-28)**. GD-15…GD-21: absent. |
| "Outcome C" | String does not occur anywhere in the repository. |
| Paper 2 manuscript | Absent. Only `paper/PAPER2_DESIGN_BRIEF.md` (a governing specification, 122 lines) exists. There is no Paper 2 `§5.3`, `§7.4`, abstract, table, figure or caption to check. (`§5.3` and `§7.4` *do* exist — in **Paper 1** and its outline.) |
| `λ_price`, `λ_feed`, `λ_deliv`, `λ_samp` | None of these four symbols occurs anywhere. The design brief defines a **different** notation: `λ_b = E[t_b(E) − t_E]` per book, and the contrast `Δλ = λ_bovada − λ_fanduel`. A four-way latency decomposition is not on the record. |
| Bounded QC list / item dispositions | Absent. No QC register, checklist or item log exists. |
| Conditions 1, 2, 4 | The design brief `§9` states **four conditions** required before Results may be written (RD-3 closed; A2 verified; A4 resolved; A5 satisfied). Whether these are the mandate's "Conditions 1, 2, 4" is not determinable from this repository. |
| "28.6% recovered agreement" | The figure **28.6%** does exist, three times, with a specific and different referent: **three reasonable main-line extraction definitions agree only 28.6% of the time** (E-017, 2026-07-19; also `ASSUMPTION_REGISTER.md` A-11 and `BOOK_CHARACTERIZATION.md`). It is used consistently in all three places. It is not described anywhere as a "recovered agreement result." |
| Live data panels | `output/*_panel.jsonl` are referenced by the README, by eight scripts and by the health tooling, but **are not in the repository**. |
| Provenance panel · watchdog | Never built. "Watchdog" appears only as a *rejected or deferred* option (GD-1, ED-6, postmortem §Residual risk). |

**Consequence for this review.** [JUDGMENT] Either the mandate's frame describes work done after 2026-07-29 that was never committed here, or it describes a different working state. In both cases the instruction "use the current repository as the authoritative state" and the instruction "use Outcome C and GD-21 as authoritative" cannot both be honoured. I have followed the first, because it is the one I can verify, and I have refused to invent the second. **§3 below is therefore answered against what is on the record (GD-13, GD-14, the design brief), and every item I cannot assess is named as unassessable rather than guessed.**

If the missing work exists, the correct next action is to commit it — a governance program whose authoritative decisions live outside its own audit trail has lost the property that makes the audit trail worth having.

## 1.2 What has genuinely been built

Three assets, in descending order of durability. [JUDGMENT]

1. **A reproducible negative result of unusual quality.** Paper 1 is complete, internally consistent, and **verified to reproduce exactly** during this review (§2.2). Its central claim — that a sharp live baseball market's forecast error is not predictable out of sample from any public state variable tested (OOS R² = −0.037), with a stated MDE and a documented survivorship-bias deconstruction — is a real, publishable contribution. Negative results this carefully bounded are rare.
2. **A governance and falsification apparatus that demonstrably works.** The Evidence Ledger, Assumption Register, Research Debt register, Confidence Register, Decision Log and Inference Graph are not decoration: they caught the PI's own overreaches on the record (E-016 self-correction; E-017 superseding E-016's magnitude; GD-13 admitting unlogged scope drift by name). [RECORD] This is the most transferable thing the program has produced and is under-exploited.
3. **An instrument that is far weaker than its documentation implies.** The live collection platform ran for ~24 days, banked ~404k rows, and cleared three of four SR-1 sub-gates — but this review found **three previously undocumented structural defects** (§1.3) that materially change what the panels can support.

## 1.3 Three previously undocumented defects found in this review

These are **new findings**, verified against source in this repository, and **absent from every governance register** (RD-1…RD-8, ED-1…ED-7, KU-1…KU-4, A-01…A-12). [FACT]

**(a) The live panels have no unique game identifier.**
`Quote.game_key` and `LiveGameState.game_key` are both `f"{away}@{home}"` (`sources/base.py:34`, `sources/base.py:71`). Panel rows carry `{ts, game, book, line, over_odds, under_odds, live, status}` (`live_engine.py:418-419`) — **no `game_pk`, no date**. Consequences:
- Every game of a series (MLB plays 2–4 consecutive nights against the same opponent) shares one key. Doubleheaders are indistinguishable even in principle.
- `collection_health.py:108-142` builds `series[game][book]` and forward-fills across the *whole concatenated key series with no game boundary*. `overlap_games` therefore counts **distinct matchups, not distinct games**. `microstructure_probe.py:26` has the identical collapse.
- **SR-1 Criterion 3 reads "≥ 100 independent games with live overlap." The satisfied count (105) is of matchups.** The underlying games are more numerous, but they are not individually identified, and games sharing a key are not independent (same two clubs, adjacent rotation slots, same park, same weather regime).
- EP-4's confirmed prediction ("overlap-games advances on new-game enrollment, not collection time") is better explained as **new-*matchup* enrollment**; the 45-game plateau across 07-11→07-16 coincides with both matchup-key saturation and a collection outage (§1.3c).
- Recoverable for non-doubleheader games by joining `ts` → `shared_piping/mlb_schedule.pair_date_map`, which itself resolves doubleheaders by `setdefault` ("keep the first game of the day (best-effort)", `mlb_schedule.py:45`). **Not recoverable for doubleheaders.**
- **Paper 1 is unaffected.** `data/trajectories.jsonl` carries `game_pk`: 163 rows, 163 unique `game_pk`, 163 unique `fixture_id`. [FACT]

[JUDGMENT] This is the concrete mechanism that a phrase like "truncated matchup slices" would describe. See §3.4 for its disposition.

**(b) There is no delivery/provenance instrumentation, and it cannot be added retroactively.**
`SourceResult` (`sources/base.py:84-95`) carries `http_status`, `latency_ms` and `payload_bytes` — and these are surfaced **only** in `connection_check.py`, an interactive one-shot diagnostic. They are **never persisted to any panel**. No response headers are captured at all: no `ETag`, no `Age`, no response `Date`, no response `Cache-Control`, no CDN/edge markers. Requests *send* `Cache-Control: no-cache` (`shared_piping/headers.py:37`) but nothing verifies the delivered object was origin-fresh. The only age measurement anywhere is the MLB Stats API's own `data_age_seconds`, used for alert gating and written to the trigger ledger — not to a panel. [FACT]
⇒ **Any decomposition separating price-formation latency from feed-transport, delivery and sampling latency is not identified with current instrumentation, and no amount of further collection under the current collector will identify it.** This is exactly assumption **A4** of the design brief, which the brief itself names "the paper's hinge."

**(c) A ~4.5-day collection outage (2026-07-12 → 2026-07-16) is nowhere documented.**
From `output/metrics_history.jsonl`, daily `book_panel_rows` deltas: [FACT]

| Date | Δ rows | Δ pairs |
|---|---|---|
| 2026-07-12 | +7,723 | +2,062 |
| **2026-07-13** | **0** | **0** |
| **2026-07-14** | **0** | **0** |
| **2026-07-15** | **+37** | **+3** |
| **2026-07-16** | **+105** | **+19** |
| 2026-07-17 | +16,024 | +564 |

Against a window mean of **15,371 rows/day**, four consecutive days produced **142 rows in total** — while the daily health report kept generating normally (checkpoints exist for every one of those dates). That is ~17% of the collection window lost. There is a postmortem for the 8.4-hour 07-06 outage; there is **no postmortem, no Evidence-Ledger entry and no Decision-Log entry for this one**, which was roughly 13× longer. [JUDGMENT] The 07-06 postmortem's own diagnosis — "there is no liveness alarm on checkpoint freshness… the last report is frozen and still reads healthy" — predicted precisely this failure mode, and the accepted mitigation (`always()` re-arm, no watchdog) did not cover it.

**(d) Related, lower severity: the vig series is sampled only at line-change instants.**
`_log_panel` skips a row whenever `line` is unchanged (`live_engine.py:414-416`). Odds-only moves at a constant handicap are therefore **never banked**. The over/under odds series exists only at line-change moments. [FACT]
⇒ The GD-7/GD-13 "within-book vig / inventory dynamics" paper is **structurally under-instrumented by the current collector**, and the E-016/E-017 vig statistics (median vig, vig IQR) are computed on a line-change-triggered subsample, not on the vig process. [JUDGMENT]

## 1.4 Bottom line

[JUDGMENT]

- **Paper 1 is real, reproducible, and close to submittable.** It needs an afternoon of editorial and metadata work plus a release/DOI, not more research. Verdict in §2.
- **Paper 2 does not exist as an object and cannot be assessed for readiness.** Its governing brief prohibits Results until four conditions clear; **zero have cleared**, one (A4) is now shown to be un-clearable without new instrumentation, and a fifth defect (no game IDs) is undocumented. Verdict in §3.
- **The dataset's headline numbers overstate it.** 403,633 rows is real; "105 independent games" is not what the counter measures; two recreational books at 30 s with no delivery provenance and no game IDs is a much thinner instrument than the row count suggests. §5.
- **The commercial value is low as data and modest as method.** Data ownership and sportsbook terms are a genuine, currently-live exposure — including for material already published in this repository. §7.
- **The program's greatest risk is not failure but perpetuation.** It has excellent machinery for deciding *not* to conclude, and no mechanism for deciding to *stop*. §9, §10.

---

# 2. Paper 1 readiness

## 2.1 Inventory

| Item | State | Detail |
|---|---|---|
| `paper/paper1.md` | **Frozen** | 804 lines; Draft 1.0; abstract, 8 sections, Appendices A/B/C, 16 references. Scientific content frozen by owner ruling 2026-07-28 [RECORD]. |
| `paper/paper1.pdf` | **Frozen** | 1,343,491 bytes, 23 pages, PDF `CreationDate` 2026-07-29T02:47:03Z — i.e. built minutes before the commit. [FACT] |
| `paper/paper1.html` | Build intermediate | Regenerated by `build_pdf.py`. |
| `paper/figures/` | **Frozen** | **11** PNGs (Figures 1–9 + B1 + C1). |
| `paper/paper1_outline.md` | Working doc | 266 lines; section-level plan. Mutable. |
| `paper/PUBLICATION_PACKAGE.md` | Operational checklist | Accurate and unusually good. Correctly states 11 figures and 1,312 KB. |
| `paper/SUBMISSION_KIT.md` | Ready-to-paste assets | D1–D8: abstract, keywords/JEL, arXiv metadata, IJF cover letter, plain-language summary, social copy, outreach email. Publication-facing, complete. |
| `docs/VISUAL_COMPANION.md` / `.pdf` | **Supplement — explicitly non-citable** | 3 figures (S1–S3). Header states: "**This is not part of the paper** and carries no citable claim." Correct and well-handled. |
| `benchmark/` | Released, preview status | README, CHANGELOG, CITATION.cff, `dataset/schema.md`, `dataset/reference_results.md`, `dataset/baseline/README.md`, `examples/report_template.md`. |
| `protocol/` | **Protocol v1.0, frozen** | `protocol.md` (7 rungs), `safeguards.md` (S-01…S-14), `stopping_rules.md` (SR-1…SR-3). |
| `output/*.json` | **Frozen result caches** | Verified byte-reproducible (§2.2). |
| `data/trajectories.jsonl` | **Frozen source data** | 163 games, 32,880 quote points. |

## 2.2 Reproducibility — verified, not asserted [FACT]

Executed in a clean container, 2026-08-22:

| Check | Result |
|---|---|
| `python3 paper/make_figures.py` | All 11 PNGs regenerate. Byte-comparison of PNG chunks: **every IDAT (pixel) chunk is byte-identical**. The only difference in any file is the `tEXt` `Software` string — committed `Matplotlib version3.11.0`, rebuilt `3.11.1`. **Figures are pixel-exact.** |
| `python3 paper/make_concept_figures.py` | Runs clean. |
| `python3 paper/build_pdf.py` | Produces 1,343,491 bytes, 23 pages — identical length to the committed PDF; only `CreationDate` differs. |
| `python3 encompass.py`, `program_a.py`, `remaining_runs.py`, `calibration.py` | All exit 0. `git status output/` **clean** — every regenerated `output/*.json` is **byte-identical** to the committed version. |
| `python3 -m pytest tests/ -q` | **113 passed in 0.76s.** |
| Key numbers spot-checked | `encompass.json`: r2_market 0.304, r2_features 0.279, r2_both 0.286, gain −0.0173, err_r2 −0.037, n 2505. `calibration.json`: auc_tier 0.42 → biased 0.61 → debiased 0.524. `remaining_runs.json`: R² 0.226, ΔMAE −0.001. `revision1.json`: CW by-game −0.12, p 0.547, gain CI [−0.0359, +0.0018], MDE 0.0071 / 0.0985. **All match the manuscript.** |

[JUDGMENT] This is a genuinely strong reproducibility result and should be stated plainly in the paper and the release notes. It is materially better than most published empirical work in this literature.

**But the environment is not publication-grade.** [FACT]
- `requirements.txt` is entirely unpinned (`>=`), lists packages irrelevant to reproduction (`streamlit`, `pybaseball`, `pyarrow`, `tqdm`), and **omits `markdown`**, which `build_pdf.py` needs (it self-installs it at runtime — a reproducibility anti-pattern).
- `paper/requirements.txt` is a second, partial list (`markdown`, `matplotlib`, `numpy`).
- The README's four-line reproduction block is **insufficient**: re-running the analysis scripts additionally requires `rich`, `pydantic` and `aiohttp`, none of which the block mentions. I hit all three as hard `ModuleNotFoundError`s.
- No Python version is declared anywhere (3.11.15 used here). The exact matplotlib version that produced the committed figures (3.11.0) is recoverable **only from PNG metadata**.
- No lockfile, no container, no CI.
- `pytest` is not in any requirements file.
- **Zero tests cover the publication-critical path** — nothing in `tests/` exercises `encompass.py`, `calibration.py`, `program_a.py` or `remaining_runs.py`. The 113 passing tests cover collector-side modules.

## 2.3 Does Paper 2 create a required correction, clarification, limitation or cross-reference?

**Required: no.** [JUDGMENT, resting on RECORD]
E-011 (2026-07-09) verified by adversarial audit that the live panels are **100% July, 0 of 103,494 rows in June**, and are disjoint from Paper 1 by time, book and data type. GD-14 (2026-07-28) verified independently that the instrument changed on all four axes (benchmark book Pinnacle→FanDuel/Bovada; `vdrop` present→absent; weather present→absent; cadence ~1 min→30 s), concluding that running Paper 1's pipeline on the new month "would confound time with instrument." Nothing collected after the freeze can bear on Paper 1's estimates. The freeze is correct and should hold.

**Optional and worth doing — two one-sentence clarifications, both permitted under the freeze because neither changes an empirical claim:** [JUDGMENT]

1. **A cross-reference to the extraction-sensitivity result.** E-017 established that three reasonable "main line" definitions agree only 28.6% of the time and can swing a level-based magnitude between 1.1× and 9.5×. Paper 1's construction is immune (a single feed, an explicitly *balanced* main total, §3.1) — but a referee who reads the follow-on work will ask. One sentence in §6 Limitations stating that the balanced-line convention is a definitional choice, invariant here because the benchmark is single-source, converts a latent objection into a demonstration of care.
2. **The E-016 → E-017 self-correction is an asset, not a liability.** [JUDGMENT] The program publicly refuted its own book-heterogeneity magnitude within the same day. If Paper 3 (the protocol/methods spin-out, §6) is ever written, that episode belongs in it.

## 2.4 Is the frozen 163-game analysis still the correct publication object?

**Yes.** [JUDGMENT] Three independent reasons:
- The June sample is the only sample in which the benchmark is a **Pinnacle-grade sharp line**. The paper's entire framing — "a sharp live betting line as an incumbent forecast" — depends on it. The post-freeze data are two *recreational* books (GD-14; E-007: Pinnacle 6 pregame rows, 0 live, ever).
- `vdrop`, the survivorship-bias centrepiece and the paper's most persuasive exhibit, is **absent** from all post-freeze data (Baseball Savant 403).
- Pooling would destroy the temporal hold-out that ROADMAP §1 correctly reserves for Paper 1.1. Adding data to a frozen null in order to make it look bigger is the exact behaviour the protocol exists to prevent.

## 2.5 Does any language overstate what a one-minute, single-book design establishes?

Largely **no** — S-13 is applied conscientiously and the binding appears in the abstract, §5.3, §6 and the reference results. Three items nonetheless: [FACT for the quotations, JUDGMENT for the assessment]

1. **The §6 forward-promise is the one substantive issue.** §6 Limitations currently reads: *"…a temporal replication on a later, non-overlapping month **is reported separately** rather than pooled into these estimates…"* This asserts as accomplished fact something GD-14 established is **blocked on host access and instrument-confounded**, and which does not exist. `PUBLICATION_PACKAGE.md` pre-flight claims "§6 forward-promise error: **fixed**" — the sentence in the committed `paper1.md` still promises it. **This must be fixed before submission**; a referee who asks to see the separately-reported replication will not find one.
2. **Cadence.** The abstract says "one-minute live total trajectories." Computed from `data/trajectories.jsonl`: median inter-quote gap **60 s**, but p25 60 s, **p75 240 s, p90 960 s, max 34,980 s**; only **58.4%** of gaps are ≤65 s. [FACT] One minute is the *modal* cadence, not the sampling interval. §3.1 and §6 already say "roughly one-minute intervals," which is fine; the abstract should match, and one clause in §3.1 giving the actual quantiles would pre-empt the objection outright. This is a precision improvement, not a correction — it does not touch a result.
3. **Minor.** §7 ("Remaining Questions") repeatedly says the follow-on streams "are being assembled to support" these questions. Given §1.3(b) — no delivery provenance, ever — the sentence about *"the timing of price formation"* (§5.3) and *"does information propagate across books with a measurable lag"* (§7) promises more than the collector can deliver. These are stated as open questions, not claims, so they are defensible; but they are a hostage to fortune. [JUDGMENT] Softening "are being assembled to support" to "are being assembled toward" costs nothing.

## 2.6 Publication metadata, repository, citation, DOI, data availability [FACT]

Every one of these is currently **not publication-grade**:

| Item | State |
|---|---|
| Repository URL in the paper | **Absent.** `paper1.md` contains no repository link at all. |
| Data-and-code-availability statement | Reads: *"A persistent DOI and packaged archive are pending publication. Until then, materials are available from the author."* **This is now false** — the repository is public. Replacement text is pre-drafted in `PUBLICATION_PACKAGE.md` §4.4. |
| §3.5 reproducibility paragraph | Pre-drafted in `PUBLICATION_PACKAGE.md` §4b, **not yet applied**. |
| Tag | **None exists.** |
| GitHub Release | **None exists.** |
| Zenodo / DOI | **None exists.** |
| Root `CITATION.cff` | No `repository-code`, no `doi`, no `version`, no `commit`. `date-released: 2026-07-14` — 15 days before the artifact it describes was built. |
| `benchmark/CITATION.cff` | **`repository-code: "https://github.com/alecmessino/project"` — wrong repository.** Also carries a *different title* ("Forecast Encompassing as a Test of Predictive Signals…") from both the root CITATION and the manuscript, and says "**Draft 0.9**" while the paper is Draft 1.0. |
| License | `LICENSE` is MIT (code). CC BY 4.0 for data/text is asserted in prose in `README.md` and `benchmark/README.md`, and `benchmark/README.md` itself hedges: "intended; to be finalized at the DOI release." **No `LICENSE-DATA` file exists.** See §7.1 — the right to grant CC BY over this data is not established. |
| Collector orchestration | `.github/workflows/the_third_turn_live.yml`, cited in `RESEARCH_LOG.md` as the artifact that produced every panel, **is not in the repository.** No `.github/` directory exists. |
| Documentation drift | `README.md` says "all **nine** figures" (there are 11). `ROADMAP.md` §0 says "**7 figures**" and gives a **different paper title** ("The Efficient Frontier of Public Information: Evidence from High-Frequency Sports Betting Markets"). `INFERENCE_GRAPH.md` IG-1 cites the velocity result as "Figure 5"; it is Figure 7. |

## 2.7 Supplement consistency

The visual companion is **numerically and conceptually consistent** and correctly disclaimed. [FACT] Its three quantitative claims all trace to the manuscript: hitter-friendly Overs 46% vs 50% (§Appendix A, `context_study.py`); overall Over hit rate 49%; break-even 52.4%. Its explicit refusal to carry a citable claim, and its instruction to "read the direction, not the decimals," are exactly right for a 163-game bucketed figure. **No action required.** [JUDGMENT]

## 2.8 Verdict — Paper 1

> ## **READY AFTER EDITORIAL / REPRODUCIBILITY CLEANUP**

The science is done, frozen, and verified to reproduce exactly. Nothing in the required list is empirical.

**Genuinely required before submission** (ordered; estimated total ≈ 1 working day plus DOI turnaround):

1. **Fix the §6 forward-promise sentence** so the paper does not assert a temporal replication that does not exist. *(The only substantive item on this list.)*
2. **Tag `v1.0`, cut a GitHub Release, wire Zenodo, mint the DOI.** Everything below depends on it, and SSAC 2027 requires a public repository link.
3. **Apply the two pre-drafted edits** — the data-availability replacement (`PUBLICATION_PACKAGE.md` §4.4) and the §3.5 reproducibility paragraph (§4b) — substituting the real repository URL and DOI. Rebuild the PDF.
4. **Repair citation metadata.** Correct `benchmark/CITATION.cff`'s `repository-code` (currently points at a repository that is not this one), reconcile the two divergent titles and the 0.9/1.0 draft status, and add `repository-code`, `version`, `commit` and `doi` to the root `CITATION.cff`.
5. **Pin the environment.** A fully pinned requirements file (matplotlib **3.11.0**, numpy, markdown, rich, pydantic, aiohttp) plus a declared Python version, and correct the README reproduction block to name the three currently-undocumented dependencies. Then execute the exact published command sequence in a clean clone — `PUBLICATION_PACKAGE.md` already mandates this ("Do not ship a reproduction command that has not been executed as written"); as written today it **fails**.
6. **Resolve the data-licensing question in §7.1 before minting the DOI.** Archiving to Zenodo under CC BY 4.0 is an irrevocable public act. Do it after the answer, not before.
7. **Either commit the collector workflow or state in the README that the orchestration is not released.** Right now the paper's infrastructure contribution has a hole a reviewer will find.
8. **Fix the figure-count and title drift** in `README.md` and `ROADMAP.md`.

**Explicitly not required:** any re-analysis, any new data, any change to a number, figure, or claim.

**Nice-to-have (not blocking):** a `LICENSE-DATA` file; a CI job running `pytest` + the reproduction; four assertion tests pinning `encompass.json`'s headline values so a future refactor cannot silently move a published number; the §6 cadence-quantile clause and the E-017 cross-reference from §2.3.

---

# 3. Paper 2 readiness

## 3.1 What is actually on the record

**Authoritative scope:** GD-13 (approved 2026-07-28) — *Paper 2 = the identification paper, one research question.* GD-7's within-book vig/inventory concept is explicitly **re-homed as a separate future paper**, at the owner's direction ("I do not want Paper 2 trying to answer two research questions"). GD-14 (2026-07-28) authorises **drafting of non-result sections only**, and splits Track 2 into a host-blocked confirmatory arm and an exploratory arm that may never be reported as replicating Paper 1. GD-12 (2026-07-19) stands: *de-risk the measurement system, do not discover results.* [RECORD]

**Governing specification:** `paper/PAPER2_DESIGN_BRIEF.md`. Estimand `λ_b = E[t_b(E) − t_E]`; contrast `Δλ = λ_bovada − λ_fanduel`; six identification assumptions A1–A6; **A4 (feed-transport latency separable from price-formation latency) named as "the paper's hinge."** [RECORD]

**Manuscript:** **does not exist.** [FACT] No draft, no sections, no figures, no tables. The brief's §7 lists Figures 1–3 as "draftable now"; none has been drafted.

## 3.2 The four gating conditions — current state [FACT against RECORD]

| # | Condition (design brief §9) | State as of `82fc298` |
|---|---|---|
| 1 | **RD-3 closed** — a main-line discriminator fixed in code, unit-tested, shown to make the leadership statistic definition-invariant | **NOT CLEARED.** RD-3 remains open and is named "the primary measurement debt; all others are subordinate." No discriminator exists in code; no test references one. |
| 2 | **A2 verified** — collector-clock audit establishing event/quote timestamp comparability | **NOT CLEARED.** Marked "**Untested**" in the brief. No audit exists. |
| 3 | **A4 resolved in one direction** — latency reference, common-mode argument, or documented impossibility | **NOT CLEARED — and now demonstrably un-clearable by collection.** §1.3(b): no transport metadata is persisted anywhere, ever. The brief's own escape hatch (a *documented impossibility*, which "also satisfies this condition") is the only route still open, and §1.3(b) is most of the argument for it. |
| 4 | **A5 satisfied** — third live book, or the GD-9 outlier-detection substitute | **NOT CLEARED.** E-019 (2026-07-28): SR-1 books-quoting-live **2/3**; gate 91%, **BLOCKED**. Pinnacle dead 22.5 days at that point (ED-1, root cause unknown, KU-1). |

**Zero of four.** Under the brief's own terms, "Results/Discussion/Abstract-findings/Conclusion remain prohibited."

## 3.3 The mandate's specific checks — what I can and cannot confirm

| Mandate check | Assessment |
|---|---|
| Bounded QC status and final disposition of every item | **Cannot assess.** No QC register exists in this repository. [GAP] |
| §5.3 and §7.4 substantively consistent | **Cannot assess.** No Paper 2 manuscript exists; those section numbers belong to Paper 1. [GAP] |
| Contemporaneity statistic treated as a dated cumulative statistic, not a timeless constant | **Confirmed on the record, and handled well.** [FACT] `metrics_history.jsonl` shows median sync lag moving 579 → 487 → 213 → **31** → **91** → 61 → 30 → **0.0** s across the window. E-014 explicitly logs the 30→91 s move as "**non-monotonic**… a further symptom of the implementation-dependent metric, not a synchronization regression." E-006, ED-2, RD-1, GD-3 and `SR1_sync_lag_design_review.md` all treat it as an instrument-dependent, date-stamped quantity, and GD-3 **refused to revise the threshold** on the strength of it. This is exactly the right handling. |
| 28.6% used consistently as the authoritative result | **Confirmed for the referent that exists.** [FACT] Appears in `EVIDENCE_LEDGER.md` E-017, `ASSUMPTION_REGISTER.md` A-11, `BOOK_CHARACTERIZATION.md` — all three meaning *three main-line definitions agree only 28.6% of the time*, all three consistent, all three citing E-017. **It is not described anywhere as a "recovered agreement" result**; if the mandate means a different quantity, that quantity is not here. |
| `game` / matchup terminology correct | **NO — this is a real defect, and it is the one substantive item I can confirm.** §1.3(a). The panel field is named `game`, the health tool reports "overlap **games**", and SR-1 Criterion 3 is written as "≥100 independent **games**" — but the identifier is a **matchup** (`AWY@HOM`) with no date. The terminology is wrong at the schema, the tooling and the gate simultaneously. |
| `λ_price`, `λ_feed`, `λ_deliv`, `λ_samp` remain distinct | **Cannot assess — these symbols do not exist here.** [GAP] What I *can* say bears on the underlying question: with no persisted transport metadata (§1.3b), a feed/delivery component is **not separately identified**, and with a 30 s poll quantizing all lags to {0} ∪ [30 s, ∞) (E-006, EP-3), a sampling component is **confounded with everything below 30 s**. Any four-way decomposition claimed on this data would need to state which components are identified and which are assumed. |
| Conditions 1, 2, 4 remain non-passes scoped by GD-21 | **Cannot assess as stated** (no GD-21). Against the brief's §9: conditions 1, 2, 3 and 4 are **all non-passes**, none retroactively satisfied, and nothing in the repository claims otherwise. [FACT] |
| No language implies an identified pricing-leadership estimate | **Confirmed for every document that exists, and the discipline is exemplary.** [FACT] `BOOK_CHARACTERIZATION.md` explicitly **refuses** to answer "which book leads," and proves the naive metric worthless by showing the leader flips (69% Bovada vs 76% FanDuel) with nonsensical ~24 h gaps. E-018 is classified "*methodological feasibility only, **NOT** a gated finding*." `INFERENCE_GRAPH.md` IG-3 **terminates at Candidate** with an explicit `╳ STOPPING RULE SR-1: BLOCKED → NO Finding → NO Paper Claim`. GD-11 states E-018 is "an identifiability/feasibility result, explicitly **not** a gated efficiency finding." I found **no** sentence anywhere implying an identified leadership estimate. |

## 3.4 The truncated-matchup-slice question — disposition

The mandate asks me to classify a specific unresolved QC item as publication-blocking, disclosure-only, or appropriately deferred, **on existing evidence only**, and to stop rather than run new analysis if the question cannot be settled.

**I cannot locate that QC item** — no QC register exists here. [GAP] But I did independently find, and verify against source, the defect such an item would most plausibly describe (§1.3a), so I will rule on that, clearly labelled as my own finding rather than as a disposition of the mandate's item.

**Ruling: publication-blocking for any Paper 2 result that uses the panel `game` field as an analytic unit — and it is not deferrable, because it is currently invisible to the governance system.** [JUDGMENT]

Reasoning, on existing evidence only:
- It is **not disclosure-only.** A limitations paragraph does not repair a unit-of-analysis error. `overlap_games` is the counter that satisfies **SR-1 Criterion 3**, the gate that authorises the analysis. A gate satisfied by the wrong unit is not a satisfied gate.
- It is **not appropriately deferred**, on the program's own rules. `RESEARCH_DEBT.md` defines its scope as "a conclusion drawn from this data could be **wrong or unidentifiable** even if the machine runs perfectly" — this is exactly that, and it is **absent from the register**. GD-8's block-typing makes it a **Measurement / Engineering** block, which the same entry defines as "**never self-resolving**." More collection cannot fix it.
- It is **partially remediable without new collection**, which is why it is not fatal: `ts` → `shared_piping/mlb_schedule.pair_date_map` recovers game identity for non-doubleheader games from data already banked. Doubleheaders are not recoverable (the map itself keeps only the first game of a day).
- It **does not touch Paper 1** (163 unique `game_pk`, verified).

**Is a new bounded analysis required to settle publication readiness?** **No** — and this is the important part. Paper 2's readiness is already determined without it: **zero of four §9 conditions have cleared**, and the brief itself prohibits Results. The game-ID defect changes nothing about that verdict; it adds a **fifth** unmet prerequisite. No new analysis is needed, and I have run none.

**Recommended (not performed):** log this as a new Research-Debt item and a new Governance-Decision entry. I have deliberately **not** appended to either register — the mandate forbids silently altering governance records, and appending to an append-only audit trail is the owner's act, not the reviewer's.

## 3.5 Verdict — Paper 2

> ## **NOT READY**

Not a close call, and for a reason prior to any QC question: **there is no manuscript.** Beneath that, zero of four gating conditions have cleared, condition 3 (A4) is now shown to be un-clearable by further collection under the current collector, and a fifth structural defect has surfaced that no register records.

[JUDGMENT] **The honest reframing — and it is a good one.** The design brief already anticipates it: *"A4/A5 may not clear at all — and that is a finding, not a failure,"* and success criterion 4 admits "**a defended impossibility result**." Section §1.3(b) of this review is most of that defence, from source, without new data. **Paper 2 should be rescoped from "under what conditions is leadership identifiable" to "why observational public-endpoint quote data cannot identify it, and what instrumentation would."** That paper is writable now, inherits Paper 1's character exactly, requires no gate to clear, and is the most valuable thing the live panels can produce. See §6.13 and §8.

---

# 4. Publication-package checklist

## 4.1 Paper 1

| Component | State | Must-have before submission | Nice-to-have |
|---|---|---|---|
| Manuscript | `paper1.pdf` (23 pp), `paper1.md` | ✅ have — **after** the §6 forward-promise fix and the two pre-drafted edits | Journal-specific single-column recast |
| Supplement | `docs/VISUAL_COMPANION.pdf` | ✅ have; correctly non-citable | — |
| Figures / tables | 11 figures; Appendix A table; Appendix B penalty table | ✅ have, pixel-reproducible | Vector (PDF/SVG) figures for print |
| Appendices | A (hypotheses), B (construction/power/level), C (transaction costs) | ✅ have | — |
| Data | `data/trajectories.jsonl` + 4 frozen caches | ⚠️ **legal review first** (§7.1) | Parquet mirror |
| Code | 41 top-level scripts + `shared_piping/` + `sources/` | ✅ have | Prune the 14 superseded exploratory scripts into `legacy/` (§9.7 — check imports first) |
| README | Root README | ⚠️ fix figure count; add the 3 missing dependencies | Add the verified-reproduction result from §2.2 |
| Environment / lock | `requirements.txt`, `paper/requirements.txt` | ❌ **unpinned, incomplete, contradictory** — must pin | Container image or `uv.lock` |
| Replication instructions | README 4-line block | ❌ **fails as written** — must be corrected and executed | `make repro` target |
| CITATION metadata | 2 `.cff` files | ❌ **wrong repo URL; divergent titles; no DOI/version** | ORCID |
| Release / tag | — | ❌ **none exists** — `v1.0` required (SSAC needs the link) | Signed tag |
| Persistent archive / DOI | — | ❌ **none exists** — Zenodo, after §7.1 | Separate dataset DOI |
| Data dictionary / schema | `benchmark/dataset/schema.md` | ✅ have — genuinely good | Machine-readable JSON Schema / Frictionless |
| Provenance / limitations | §6, §7; `protocol/safeguards.md`; `ops/` | ✅ have — unusually strong | One-page provenance summary in the release |
| Journal-facing | `SUBMISSION_KIT.md` D1–D8 | ✅ have — cover letter, abstract, JEL, arXiv metadata all drafted | arXiv endorser secured in advance |
| CI | — | — | Test + reproduction on push |

## 4.2 Paper 2

Not applicable. **Every component is absent.** The only publication-package work that is meaningful today is (a) drafting the brief's Figures 1–3 and Tables 1–3, all marked "draftable now" from E-016/E-017/E-018 material already generated, and (b) writing the impossibility argument of §3.5. Both are permitted under GD-14 (non-result sections). Nothing else should be packaged.

## 4.3 Recommended venues

**Paper 1** [JUDGMENT] — the existing `ROADMAP`/`SUBMISSION_KIT` targeting is well-reasoned; I agree with it and would order it:

| Rank | Venue | Reasoning |
|---|---|---|
| 1 | **International Journal of Forecasting** | The best fit by a wide margin. Chong-Hendry encompassing, Diebold-Mariano, Clark-West and MDE-reported nulls are its native toolkit, and it publishes negative forecast comparisons — which most journals will not. The paper is already written in this register. Cover letter D4 is drafted. |
| 2 | **SSRN + OSF preprint, immediately** | Zero friction, establishes priority, and is required infrastructure for everything else. Do this the day the DOI lands. arXiv `q-fin.ST` is worth pursuing but needs an endorser — start that ask early; it is the most likely source of delay. |
| 3 | **MIT Sloan SSAC 2027** | Highest visibility, and the **only hard deadline: abstract due 2026-10-01**. Requires a public repository link, which is why §2.8 item 2 is on the critical path. Verify the date on the live call. |
| 4 | **Journal of Quantitative Analysis in Sports** | Where Brill-Deshpande-Wyner published the TTOP work this paper independently reproduces. A natural, receptive home if IJF declines. |
| 5 | *Journal of Sports Economics* | Solid fallback. |
| — | *Management Science* | Listed as aspirational in the ROADMAP. [JUDGMENT] **I would not submit there.** A single-month, single-book, 163-game null without the cross-book robustness leg is very likely a desk reject, and the cost is months. Revisit only if Paper 1.1 lands. |

**Audience beyond journals:** the forecast-evaluation and prediction-market communities will value the encompassing framing more than the sports-analytics community will; the sports community will value the survivorship-bias deconstruction more. Lead with the appropriate half for each. `SUBMISSION_KIT.md` D5–D8 already does this correctly.

**Paper 2:** unassessable until an object exists. If rescoped per §3.5, the natural targets are a measurement/methods venue rather than a markets one — the contribution would be about what public-endpoint observational data can and cannot identify, which travels well beyond sport.

**No submission or dissemination has been performed.**

---

# 5. Current dataset inventory and quality

All counts computed from the working tree at `82fc298`. **As-of: 2026-08-22T17:13:06Z.** No count below is carried over from any prior message.

## 5.1 In-repository data — Benchmark Dataset v1 (frozen) [FACT]

| Property | Value |
|---|---|
| Source file | `data/trajectories.jsonl`, 2,638,424 bytes |
| Games | **163** |
| **Unique game IDs** | **163 unique `game_pk`; 163 unique `fixture_id`** — 1:1, no collisions |
| Date coverage (game start) | 2026-06-01T22:40Z → 2026-06-23T23:10Z |
| Date coverage (quotes) | 2026-05-31T20:35 → 2026-06-24T02:37 |
| Distinct slate dates | 15 |
| Books | **1** (single Pinnacle-grade feed via Odds Papi historical). No `book` field — the file is single-source by construction |
| Total quote observations | **32,880** |
| Per-game quotes | min 94 · median 203 · max 336 |
| Quote changes (any field) | **23,472** |
| Line-level changes | **7,024** |
| Distinct line values | 22, spanning 3.5 → 14.0; **100% on the 0.5 grid** |
| Polling cadence | median gap **60 s**; p25 60 s · p75 240 s · p90 960 s · max 34,980 s. **58.4%** of gaps ≤65 s |
| Null odds | **0** |
| Implied overround | median **4.73%** (p10 2.89% · p90 5.76%) |
| Main vs alternate lines | Not applicable — one balanced main total per timestamp; **no alt-line contamination** |
| Pregame vs live | Both; trajectories begin ~1 day before first pitch |
| Simultaneous / cross-book pairs | **0** — single book |
| Game-state observations | 2,859 half-inning states (`remaining_snapshots.json`), 163 games |
| Encompassing snapshots | **2,505**, 163 games, 10 features + Y, B, game; **0 nulls in any field** |
| Event matches | **6,414** (`program_a_cache.json`): single 1,631 · walk 937 · pitching_change 2,810 · home_run 389 · double 485 · hit_by_pitch 115 · **triple 47** |
| Per-game features | 163 games (`features_cache.json`, 2.7 MB); **weather complete on 163/163** |
| Provenance observations | **0** |
| Cache / header / freshness | **0** |
| Delivered-object staleness | **0** |
| Temporal gaps / outages | None material within the June window |
| Update rate | **Frozen.** Does not accumulate |
| Storage | 12 MB working tree · 3.42 MiB packed. Largest: `features_cache.json` 2.7 MB · `trajectories.jsonl` 2.6 MB · `paper1.pdf` 1.3 MB |
| Reproducibility | **Verified byte-exact this review** (§2.2) |

**Ancillary:** `data/closing_lines.csv` — 31 rows, 31 unique `game_pk`, commence 2026-06-24T01:45Z → 2026-07-03T02:11Z, sources `theoddsapi` / `oddspapi`, 1–9 books. Note this is **post-freeze** and is **not** Paper 1 input.

## 5.2 Live panels — last-observed state [RECORD; files absent from repository]

**The panel files themselves are not in this repository.** [FACT] `README.md`, eight scripts and the health tooling all reference `output/*_panel.jsonl`; none exists. This was a deliberate release decision (`PUBLICATION_PACKAGE.md` §3: "**Exclude for v1** … bundle drops 106 MB → 12 MB"). The counts below are therefore the **last committed observations**, from `output/metrics_history.jsonl` and `output/health_report.txt`.

**As-of for this table: 2026-07-29T02:32:10Z** — the final checkpoint. **Nothing after that date exists in the repository. As of this review that is a 24-day blind spot, and the repository contains no evidence of whether collection continued, stopped, or was lost.**

| Property | Last-observed value |
|---|---|
| Window | 2026-07-03 → 2026-07-29 (24 daily checkpoints, first 2026-07-06) |
| `book_panel` rows | **403,633** |
| Live rows | **97,451** — fanduel 52,410 · bovada 45,041 · **pinnacle 0** |
| Books | **2 live** (FanDuel, Bovada). Pinnacle: 6 pregame rows in one burst, 0 live ever; last quote ~22.8 days before the checkpoint |
| Game keys — book panel / live / overlap | 112 / 107 / **105** — **all matchup keys, not games** (§1.3a) |
| Games by books-live | 2 books: **105** · 1 book: 1 · 0 books: 6 |
| Simultaneous live pairs | **53,769** |
| Median sync lag | **0.0 s** — certifies same-poll co-capture, **not** market contemporaneity (E-006, RD-1) |
| `team_total_panel` rows | **25,294** (Pinnacle per-team implied run PMF: line, σ, skew, full pmf) |
| `game_state_panel` | Present; row count not carried in the metrics series |
| Polling cadence | 30 s (`config.py:133`) |
| Quote changes | Change-only logging, **triggered on line change only** — odds-only moves never banked (§1.3d) |
| Main / alternate lines | Interleaved, **no discriminator**; ~95% of (game, book, ts) groups carry 2–3 lines (E-010, RD-3, ED-3) |
| Market status (live rows) | unset **45,041** (all Bovada) · OPEN 48,090 · SUSPENDED 4,093 · REMOVED 227 — **single-book coverage** (E-008, RD-4) |
| Innings covered | 1–12 |
| Provenance observations | **0** |
| Cache / header / freshness | **0** |
| Delivered-object staleness | **0** |
| Integrity | 0 malformed · 0 missing-field · 0 duplicate · 0 future-ts — **under a 4-field definition only** (`ts/game/book/line`); odds, status and line-type unchecked (ED-4). 61 null-odds rows pass (E-009, RD-5) |
| Temporal gaps | **8.4 h, 2026-07-06** (postmortem exists). **~4.5 days, 2026-07-12 → 07-16 — undocumented** (§1.3c). **24 days, 2026-07-29 → 2026-08-22 — unknown** |
| Storage | ~85 MB (`PUBLICATION_PACKAGE.md`, 2026-07-28) |
| Update rate | **15,371 rows/day** mean over the window |

## 5.3 Classification

### Tier 1 — Scientifically clean now
- **`data/trajectories.jsonl` and the four frozen caches.** Unique game IDs, no nulls, single unambiguous main line, complete weather, verified byte-reproducible, fully documented schema, and every derived number checked against the manuscript. This is publication-grade data. [JUDGMENT]
- **`output/metrics_history.jsonl`.** 24 honest daily checkpoints including the days the system was failing. As an operational record it is clean and, unusually, self-incriminating — which is what makes it credible.

### Tier 2 — Useful with qualifications
- **`team_total_panel` (25,294 rows).** [JUDGMENT] Genuinely the most unusual thing the program has collected: a per-team **full implied probability mass function** (line, σ, skew, complete pmf over run buckets) from a sharp book, joined to game state, at ~90 s throttle. Most odds datasets carry line + price only. Qualifications: single-source; change-only on `implied_line` at a 0.05 threshold (so the σ/skew series is *sampled at mean-change instants*, a subtler version of §1.3d); shares the matchup-key defect; the "8+" bucket uses an assumed centroid of 8.5 (`team_totals.py:33`); and SR-2's counters were never instrumented. **This is the asset most worth rescuing.**
- **`game_state_panel`.** Rich (inning, half, outs, score, bases, TTO, pitch count, starter-on, tier, pitcher_id, velo early/recent/drop), change-only, and it is the exogenous clock the whole event-anchored design needs. Qualified by the same matchup-key defect and by an unverified clock-comparability assumption (A2, untested).
- **`book_panel` for *within-book, transition-based* work.** E-018 established that transition metrics are **invariant** to the main-line definition (modal ≡ balanced, byte-identical output), which is precisely why A-11 was frozen. Transition-based questions on a single book are the defensible use.

### Tier 3 — Structurally limited in interpretation
- **Any cross-book level statistic.** A-11 refuted for level metrics; three definitions agree 28.6% of the time and swing magnitudes 1.1×–9.5× (E-017).
- **Any leadership or lead-lag estimate.** A4 not separable and, per §1.3(b), not separable *in principle* from banked data. SR-1 blocked. A-04 Weak, A-12 provisional single-window.
- **Any suspension- or staleness-filtered comparison.** Bovada emits no status on any of 45,041 live rows; filtering one book and not the other is asymmetric selection (RD-4, A-06 **Refuted as implemented**).
- **Any analysis using the panel `game` field as a unit.** §1.3(a).
- **Any within-book vig or inventory dynamics.** §1.3(d) — the vig series is sampled at line-change instants only. This limitation applies directly to the GD-13 "separate future paper."
- **The 07-12→07-16 window.** ~17% of the collection period is essentially empty, undocumented, and would silently distort any time-series or day-fixed-effect specification.

## 5.4 How unusual and valuable is this dataset, honestly?

[JUDGMENT] **Moderately unusual academically; close to worthless commercially as data.** Both halves of that sentence matter.

**What is genuinely hard to recreate:**
1. **It is retrospectively impossible.** Live odds tape is not archived by the books. A researcher deciding today to study June–July 2026 cannot obtain this at any price except from a vendor who happened to be recording. That is the single strongest property, and it is a property of *time*, not of skill.
2. **The per-team implied PMF is rare.** Most vendor products expose line + price. A full de-vigged distribution per team per snapshot, joined to game state, is unusual in academic hands.
3. **The joined structure.** Odds × game-state × pitch-level velocity on a common clock is more work than it looks, and most researchers building it would get the joins subtly wrong.
4. **The governance trail.** [JUDGMENT] **This is the actually scarce asset and it is not data.** An Evidence Ledger where E-016 is publicly superseded by E-017 the same day, an Assumption Register where six of twelve assumptions are Weak/Challenged/Refuted *on the record*, and an Inference Graph whose live-data chains explicitly terminate with `NO Finding → NO Paper Claim` — that combination is genuinely rare, and it is what would make a referee trust a null.

**What makes it easy to recreate, or not worth recreating:** [JUDGMENT] — being deliberately unflattering, as instructed.
- **Anyone can start collecting tomorrow.** The endpoints are public, the adapters are ~100 lines each, and the whole collector runs on a free GitHub Actions runner. A competent engineer reproduces the *capability* in a weekend. Only the historical window is scarce.
- **The books are wrong for the question.** Two recreational books. The sharp source — the one the entire Paper-1 framing rests on — was never captured live at all.
- **30 s is too coarse.** It quantizes every lag to {0} ∪ [30 s, ∞), which is the root of RD-1 and E-006. Real microstructure work at this question needs sub-second.
- **No volume, no order flow, no depth.** So no PIN, no Kyle lambda, no adverse selection, no liquidity measure. GD-7 identified this correctly.
- **No delivery provenance**, so no latency decomposition — ever, retroactively.
- **No unique game IDs.**
- **~17% of the window is missing and undocumented.**
- **Commercial vendors already sell better.** Sportradar, Genius Sports, OddsJam, Unabated and others sell tick-level multi-book feeds with real identifiers, licensed, at prices a research group can afford. A sportsbook has vastly better internal data than this. **No sportsbook, vendor or institutional betting group would pay for these panels.**

**Net.** [JUDGMENT] As a *research* asset for a specific, honestly-scoped measurement question — what can and cannot be identified from public sportsbook endpoints — it is a good and defensible dataset, and the one genuinely novel component (the implied-PMF panel) is under-exploited. As a *product*, it is not competitive and should not be marketed as one.

---

# 6. Research opportunity map

Ranked by expected value = scientific importance × identification quality × novelty ÷ incremental work. [JUDGMENT throughout; identification classifications rest on the facts of §1.3 and §5.3.] **No analysis was started.**

| # | Question | Identification with current data | Novelty | Incremental work | P(credible paper) |
|---|---|---|---|---|---|
| **1** | **Methodological work on public-endpoint measurement** — what is and is not identifiable from public sportsbook endpoints; the frequency/extraction/latency artifact taxonomy, each shown to *manufacture* a false leader | **Identified** — this is the one question the data's *limitations* answer rather than obstruct | **High** — nobody has written it, and every applied group needs it | **Low.** E-016/E-017/E-018 already generated; §1.3(b) supplies the latency argument; brief Figures 1–3 draftable now | **High** |
| **2** | **Paper 1 replication / extension (Paper 1.1)** — the frozen pipeline on a second, non-overlapping month | **Requires new instrumentation** — needs Pinnacle historical + Statcast on a reachable host (GD-14, both 403 in-container). Method is not the blocker | Moderate; high *credibility* value | **Low if hosts unblock; unbounded if not.** ~2,500 snapshots / ~150 games | **High, conditional on host access** |
| **3** | **Price-path calibration / distribution dynamics (SR-2)** — does the market update σ, skew and tails as well as it updates the mean? | **Partially identified.** 25,294 PMF rows exist; single-source (needs no cross-book sync, which is why SR-2 is looser); blocked by within-game continuity, matchup keys, and un-instrumented counters | **High** — Paper 1 rules out the first moment, making higher moments the natural next target. KU-4 asks whether this is the better paper; on my read, **yes** | **Moderate** — instrument SR-2's counters, split by game, verify continuity | **Moderate-High** |
| **4** | **Response to discrete game events (transfer function, live)** — event-anchored line response by event type, on live data | **Partially identified.** Event-anchoring is the design brief's central methodological move and removes the frequency confound; A2 (clock comparability) untested | Moderate — extends Paper 1's Figure 8 from historical to live | **Moderate** — needs the `book_panel × game_state_panel` join (data exists, join never materialized) | **Moderate** |
| **5** | **Update-frequency microstructure** — the two books as instruments; how cadence alone manufactures apparent leadership | **Identified for direction; not for magnitude** (E-016 direction robust; magnitude 1.1×–9.5×, E-017) | Moderate; strongest as a component of #1 | **Very low** — largely written in `BOOK_CHARACTERIZATION.md` | **Moderate as a section; low standalone** |
| **6** | **Cross-sport replication** — the protocol unchanged on NBA totals or NFL spreads | **Requires new instrumentation** (new feeds), but no new *method* | Moderate — directly supports the "citable protocol" claim | **Moderate** — adapters + a season | **Moderate-High.** Best value-per-effort *extension*, as the ROADMAP already says |
| **7** | **Market robustness around shocks** — information half-life τ½ by event type | **Partially identified.** τ½ is confounded with poll cadence at 30 s and with delivery latency (never measured) | Moderate | Moderate | **Low-Moderate** |
| **8** | **Pregame→live transition** — does the frontier move at first pitch? | **Partially identified.** Both regimes present; ~90% of early rows pregame; regime boundary recoverable from `live` flag | Moderate — genuinely under-studied | Moderate | **Moderate** |
| **9** | **Market disagreement / dispersion** — when do books disagree, and does dispersion collapse after shocks? | **Partially identified.** Two books only (dispersion across n=2 is a difference, not a dispersion); RD-8 asymmetry; matchup keys | Low-Moderate | Moderate | **Low-Moderate** |
| **10** | **Event-dependent availability / liquidity** — suspension and reopen behaviour around events | **Not identified.** Bovada emits no status on any of 45,041 live rows. `BOOK_CHARACTERIZATION.md` calls this "**unanswerable with the current two-book roster, full stop — not a to-do**," and I agree | Would be high if measurable | Requires a third book that emits status | **Very low without new instrumentation** |
| **11** | **Within-book vig / inventory dynamics vs leverage** (the GD-13 separate future paper) | **Not identified as instrumented.** §1.3(d): odds-only moves at constant line are never banked | Low-Moderate — a conventional microstructure study | Requires a collector change *and* forward re-collection | **Low now; Moderate after a collector fix + a season** |
| **12** | **Cross-book leadership magnitude** — who leads, by how much | **Not identified, and not identifiable from banked data.** A4 un-separable (§1.3b); SR-1 books 2/3; 30 s quantization | High if answered | Requires sub-second capture, ≥3 books incl. a sharp one, and per-request transport metadata | **Very low. Do not pursue as a magnitude question** — pursue as #1 |
| **13** | **Stale-object / reordering behaviour; delivery infrastructure as microstructure** | **Requires new instrumentation, entirely.** Zero header, cache, ETag, Age or payload metadata has ever been persisted | High — genuinely novel framing | A new collector capturing full response provenance, plus a fresh window | **Low near-term; Moderate as a designed successor study** |

**The ranking's single message:** [JUDGMENT] the highest-value research left is **#1**, and it is the *cheapest*, because the data's limitations are its subject matter. Everything in the "requires new instrumentation" column should be understood as *a different collector*, not *more of this one*.

---

# 7. Commercial and monetization opportunity map

[JUDGMENT throughout. I have been deliberately skeptical, as instructed.]

## 7.1 Legal and ownership — read this before anything else in §7

**These are live exposures, and one of them is already public.** [FACT for the mechanisms; JUDGMENT for the risk assessment. **I am not a lawyer and this is not legal advice.**]

1. **The most urgent item: `data/trajectories.jsonl` is already published under CC BY 4.0.** [FACT] `README.md` licenses "Data and paper text: Creative Commons Attribution 4.0." That file contains **32,880 quote observations sourced from Odds Papi**, a commercial odds API (`.env.example`: "Odds Papi key… FREE tier HAS historical odds… Free plan = 250 requests total"; `harvest_trajectories.py`). Commercial odds APIs essentially universally prohibit bulk redistribution. **The project is asserting a CC BY 4.0 grant over data it very likely lacks the right to relicense, in a public repository, today.** Minting a Zenodo DOI would make this permanent and irrevocable. **Resolve this before §2.8 item 2.**
2. **The collector's posture is documented ToS avoidance.** [FACT] `shared_piping/headers.py` states its purpose plainly: sportsbook feeds "reject the default `aiohttp`/`python-requests` User-Agent, so every request goes out looking like a real desktop browser. We rotate across a small pool so a run doesn't hammer a book with one identical fingerprint." `sources/pinnacle.py:28` uses a "public guest key **embedded in Pinnacle's own web client**." DraftKings 403s the IP at the Akamai edge. This is written down, in the repository, in the project's own words — which is admirable honesty and also a discovery exhibit.
3. **What the risk actually is.** In the US, contract (terms-of-service) claims are the realistic exposure, not CFAA — post-*hiQ* and *Van Buren*, scraping public pages is weak ground for a computer-fraud theory, but ToS breach and unjust-enrichment theories are not. In the EU/UK, **sui generis database rights** may attach to the books' odds compilations independently of copyright. Sports-data rights holders litigate this space actively.
4. **Redistribution vs. use are different questions.** Non-commercial academic *use* of scraped public data is defensible and routine. **Bulk redistribution under an open license, and any commercial exploitation, are materially different and materially riskier.**
5. **The README disclaimer is not clearance.** "Verify the relevant terms before redistribution or commercial use" transfers the question to the reader; it does not answer it for the publisher.

**Recommendations:** [JUDGMENT]
- **Do not commercialize any panel data, in any form, without written counsel review.** Not licensing, not a data product, not a sample, not a demo.
- **Before minting the DOI**, get a written answer on `trajectories.jsonl` under Odds Papi's terms. If the answer is negative, the tractable fix is to publish the **derived caches** (`encompass_cache.json`, `program_a_cache.json`, `remaining_snapshots.json` — from which every published number reproduces, verified in §2.2) and withhold or gate the raw quote file. Paper 1's reproducibility is fully preserved by that split.
- **Add an explicit `LICENSE-DATA`** stating what is licensed, by whom, and on what basis. The current prose grant is the weakest possible position: maximum exposure, minimum clarity.
- **Never release the panels commercially.** Their scientific value survives an academic-use framing; it does not survive a licensing framing.

## 7.2 Opportunity assessment

I assessed six categories against the mandated audiences (academics, sports-analytics firms, sportsbooks, market-data vendors, media/data publishers, institutional betting groups, prediction-market researchers, adjacent microstructure users). **Four of the six do not clear the bar.** I state those first and briefly, because the useful output of a commercial review is usually the eliminations.

### Not viable — stated plainly

| Category | Why not |
|---|---|
| **Data products** (selling the panels) | Two recreational books, 30 s, one month, no game IDs, ~17% missing, no volume, no depth. Vendors sell strictly better, licensed. Sportsbooks have vastly better internal data. **And §7.1 says the data may not be ours to sell.** No viable customer at any price. |
| **APIs / infrastructure** (hosting a live odds API) | A commodity with entrenched incumbents, a permanent scraping-arms-race cost structure, no differentiation, and the full weight of §7.1. |
| **Analytics / decision support** (betting signals) | **Paper 1 is the falsification of this product.** The program spent a year establishing that no public variable improves on the price. Selling decision support off this work would require contradicting its own central finding. Do not do it. |
| **Institutional betting groups as customers** | They need sharp-book, sub-second, executable data with real identifiers. This is none of those. They would not buy it, and they are right not to. |

### The two that are real

---

**Opportunity A — Research/intelligence: measurement-validity review as a service**

| | |
|---|---|
| **Customer** | Sports-analytics firms, prediction-market and forecasting research groups, quant teams with an internal backtest they do not fully trust, and (the best-fit segment) **investors or boards doing technical diligence on a forecasting or betting-analytics claim**. |
| **Problem solved** | "We have a signal that looks real. Is it?" This is the single most expensive unanswered question in applied forecasting, and almost nobody has a method for it. The failure modes the program has *already catalogued and priced* — post-treatment selection (AUC 0.61 → 0.52), frequency-confounded lead-lag (73:5 → indistinguishable), definition-sensitive extraction (28.6% agreement, 1.1×–9.5× swing), mean-vs-median functional-target confusion (+0.49 "bias" that was an intercept) — are exactly the errors that kill applied work. |
| **Deliverable** | A protocol-based validity review: the seven-rung ladder applied to a client's candidate signal, an explicit elimination rung, an MDE statement, and a written artifact in the `benchmark/examples/report_template.md` format. |
| **Differentiation** | The credibility is unusually strong and unusually cheap to demonstrate: a published paper, a reproducible benchmark, a citable protocol, **and a public audit trail in which the author refutes his own results by name**. Almost no consultant can show that last thing. |
| **Additional requirements** | Publication (§2.8) and a public DOI. **No data, no engineering, no licensing** — this monetizes the method, which the program unambiguously owns. |
| **Model** | Project fees or retainer. Realistically five figures per engagement. |
| **Defensibility** | Weak as IP (the ladder is published, deliberately, and standard components). Moderate as reputation — the durable moat is the demonstrated track record of self-falsification, which cannot be copied without doing the work. |
| **Principal risk** | It is consulting: it scales with the founder's hours and not otherwise. Also a real conflict of interest — a validity reviewer whose incentive is repeat business faces pressure to find the client's signal survivable. That must be structurally addressed (fixed fee, no contingency, published method) or the credibility that is the entire product erodes. |
| **Viability** | **Modest additional work** — gated only on publication. |

---

**Opportunity B — Third Turn Protocol as research-brand / open IP**

| | |
|---|---|
| **Customer** | The research community, indirectly. Not a paying customer. |
| **Problem solved** | Applied forecasting and betting research has no shared standard for "does this signal add anything," so every group rebuilds the argument badly. A named, citable ladder with a reference implementation and a benchmark to report against fills a real gap. |
| **Deliverable** | Protocol v1.0, safeguards S-01…S-14, SR-1…SR-3, Benchmark Dataset v1, reference implementations, report template. **All already written.** |
| **Differentiation** | The deliberate separation of Protocol (method) and Benchmark (data) with independent versioning is correct and rare. The domain-generality claim ("finance, weather, elections, forecasting competitions") is credible on the face of the ladder. |
| **Additional requirements** | Publication + DOI + a citable identity. Possibly Paper 3 (the methods spin-out), which the ROADMAP correctly makes **reception-gated** — decide after Paper 1's first response, not before. |
| **Model** | **Not directly monetized.** It is the asset that makes Opportunity A sellable, makes speaking and expert work available, and compounds through citation. |
| **Defensibility** | None as IP, by design — an open protocol's value *is* its adoption. Defensibility is authorship. |
| **Principal risk** | Nobody adopts it. Adoption of a named method by an independent researcher with one paper is a low-base-rate event, and the honest expected value is low. |
| **Viability** | **Now**, at essentially zero marginal cost, since the artifacts exist. |

---

**Licensing / partnerships:** [JUDGMENT] Not viable as data licensing (§7.1). The one plausible *inbound* form is a data-sharing arrangement in the other direction — a vendor or book granting research access in exchange for co-authorship or a published methodology. That is worth an ask once Paper 1 is public and gives something to trade; it is not a revenue line.

## 7.3 Commercial bottom line

[JUDGMENT] **The honest assessment is that Third Turn is not a business, and the attempt to make it one would damage the thing that is actually valuable.**

The data cannot be sold (no market, and probably no right). The signals do not exist — the program proved it. What remains is a **method with unusually well-documented credibility**, which converts into consulting, expert work, and reputation, at a scale measured in tens of thousands of dollars a year with real founder-hour constraints. That is a genuinely good outcome for a research program. It is not a company, and treating it as one would mean either selling decision support the research refutes, or licensing data the project may not own.

---

# 8. Ranked strategic priorities

## 8.1 By academic / research value

| Rank | Path | Upside | Effort | Principal dependency | Fastest falsification / abandonment criterion |
|---|---|---|---|---|---|
| 1 | **Publish Paper 1** (§2.8) | The entire program's output becomes citable and real | **~1 day** + DOI turnaround | §7.1 data-licensing answer | Not falsifiable — this is banked work. Abandon only if counsel blocks the data release, in which case ship the derived-cache split |
| 2 | **Rescope Paper 2 as the impossibility/identification result** (§3.5) | A second real paper from data already banked, needing no gate to clear | **2–4 weeks** | Owner approval of the rescope (a decision-log entry superseding the brief's §9) | If a referee or reader shows A4 *is* separable from banked data, the paper collapses — test that in week 1 by writing the argument first |
| 3 | **Paper 1.1 temporal replication** | Converts a single-month null into a replicated one; the biggest single credibility gain available | **1–2 weeks of work**, unbounded waiting | A host where Baseball Savant and Odds Papi are both reachable, plus budgeted Odds Papi credits | Try one Statcast + one Odds Papi call from a candidate host. If either 403s, the path is closed **today** — stop, do not engineer around it |
| 4 | **SR-2 distribution dynamics** (the implied-PMF panel) | The most novel asset the program holds; Paper 1 rules out the first moment, making this the natural target | **4–8 weeks** | Panel files recovered; matchup keys resolved; SR-2 counters instrumented | Count games with continuous PMF coverage through ≥6 innings. If <50 (the SR-2 threshold), stop and say so |
| 5 | **Cross-sport replication** | Directly substantiates the domain-generality claim, which is the protocol's whole value | **4–6 weeks** | New adapters + a season of a second sport | If the ladder needs modification to transfer, the generality claim is weakened — report *that* and stop |
| 6 | **Event-anchored live transfer function** | Extends Paper 1's Figure 8 from historical to live | 3–4 weeks | The `book_panel × game_state_panel` join; A2 clock audit | If the clock audit shows uncontrolled skew, the design fails at the first step |

## 8.2 By commercial / economic value

| Rank | Path | Upside | Effort | Principal dependency | Fastest falsification |
|---|---|---|---|---|---|
| 1 | **Publish + DOI + public profile** | Prerequisite for every other commercial path; nothing is sellable without it | ~1 day | §7.1 | — |
| 2 | **Validity-review consulting** (Opp. A) | Realistic five figures per engagement | 2 weeks of positioning after publication | Publication | Approach 5 plausible buyers after the preprint. Zero interest in 90 days → the demand does not exist. Stop |
| 3 | **SSAC 2027 + speaking** | The highest-leverage single audience for this work | Abstract by **2026-10-01** | Public repository link | Rejected → the sports-analytics channel is weaker than assumed; reweight to forecasting venues |
| 4 | **Protocol adoption** (Opp. B) | Compounding, but slow and low-probability | Near-zero marginal | Publication | No external citation or use within 12 months → treat as authorship credit only, and stop investing |
| 5 | **Inbound data partnership** | Would unlock everything currently gated | Weeks of outreach | Something to trade — i.e. publication | 10 asks, no reply → closed |
| — | *Data licensing / API / signals* | — | — | — | **Do not start.** §7.1, §7.2 |

## 8.3 Combined strategic value

1. **Publish Paper 1.** It is the gate on literally everything else, academic and commercial, and it is one day of work.
2. **Rescope and write Paper 2 as an identification/impossibility result.** Turns the program's biggest liability — a blocked gate that will never clear — into its second publication, from data already banked.
3. **Decide the collector's fate, explicitly and in writing** (§10). It has been in an undefined state for 24 days.
4. **Attempt Paper 1.1**, with a hard one-week timebox on the host question.
5. **Test the consulting demand** with five real conversations after the preprint.
6. **Fix or formally retire the panels** — resolve the matchup-key defect and document the 07-12 outage, or freeze the panels as-is with the defects disclosed. Either is acceptable; leaving them undocumented is not.

## 8.4 Where marginal effort has the highest return

**One additional week → publish Paper 1.** [JUDGMENT] Not close. One day of editorial and metadata work plus a DOI converts a year of work from private to citable, unlocks SSAC (deadline 2026-10-01), unlocks every commercial path, and requires no research. The single most valuable week available to this program is the one that ships what is already finished. Everything else on every list above is gated behind it.

**One additional month → publish Paper 1, then draft Paper 2 as the identification/impossibility paper.** [JUDGMENT] Weeks 2–4 produce a second paper from material already generated (E-016/E-017/E-018 plus the §1.3b argument), needing no gate, no new data, and no new instrumentation. It inherits Paper 1's character precisely — method and honest limits over positive findings — and it converts the program's most frustrating dead end into a result. Its own governing brief already sanctions this: "a defended impossibility… **is a finding, not a failure.**"

**Six additional months → two published papers, a decided platform, and one deliberate new instrument or a deliberate stop.** [JUDGMENT] Concretely: months 1–2 ship Papers 1 and 2 and attempt Paper 1.1 (timeboxed). Month 3 makes the platform decision — either (a) freeze the collector, version the panels as Benchmark v2 with defects disclosed, and stop; or (b) build **one** successor collector specified against a **single named hypothesis**, with unique game IDs, full response provenance, sub-second capture where the question needs it, and a sharp source — and if a sharp live source cannot be obtained, choose (a). Months 4–6 execute exactly one of: SR-2 distribution dynamics (best odds), cross-sport replication (best support for the protocol claim), or the validity-review practice. **Not all three.**

The failure mode to avoid over six months is obvious from the record and worth naming: **another six months of disciplined accumulation against a gate whose fourth criterion depends on a feed that has been dead since 2026-07-06 with an undiagnosed root cause.** That is not patience; it is waiting for something that is not coming.

---

# 9. Stop-doing list

[JUDGMENT, each grounded in the cited fact]

**1. Stop collecting toward SR-1.** Its fourth criterion needs a third live book. Pinnacle has produced 0 live quotes ever, root cause **unknown** (ED-1 "Top" risk, KU-1 open since 2026-07-09), and EP-5 predicted — correctly, on the record — that it "will stay stillborn until the collector integration is changed." Criterion 3 is satisfied only in matchups (§1.3a). Collecting more rows moves neither. **Either diagnose ED-1 in a bounded session (≤1 day) or formally retire SR-1 as unachievable with this roster.**

**2. Stop pursuing cross-book leadership as a magnitude.** A4 is not separable from banked data and never will be (§1.3b). The program has already learned this three times (S-10, S-11, E-018) and its own doctrine (GD-12) paused it. Convert it into the identification paper and close the question.

**3. Stop the "within-book vig / inventory dynamics" paper in its current form.** GD-13 re-homed it as attractive because "less blocked." §1.3(d) shows it is blocked differently and more fundamentally: the vig series is sampled only at line-change instants. It needs a collector change *and* a fresh window. **Reclassify it from "unscheduled future paper" to "requires new instrumentation."**

**4. Stop adding governance artifacts — and enforce the rule already written.** GD-6 declared the framework feature-complete on 2026-07-09 with an admission rule. That rule has held. **The active risk is different and worse: three material defects (§1.3) went undetected by twelve registers, and a 4.5-day outage was never logged by any of them.** The governance system is now large enough to feel like coverage while missing schema-level facts. Do not add a thirteenth artifact. Instead, run one adversarial pass **against the schema and the tooling** rather than against the analysis — which is precisely what this review did, and it found three things in a day.

**5. Stop the daily governance review.** It served a real purpose during active development. On a frozen paper and a collector in an undefined state, it produces "no scientific progress today" — which GD-2 correctly says is an acceptable verdict, but 24 consecutive acceptable verdicts is a signal to change cadence, not to keep reporting. Move to weekly, or to event-triggered.

**6. Stop treating row counts as progress.** 403,633 rows and 15,371/day are engineering metrics. Dataset maturity has been **Low** since 2026-07-09 and the Confidence Register's own discipline says a level "never rises on 'more data collected.'" Honour that by not reporting volume as an achievement.

**7. Stop the exploratory-script accumulation.** 14 of 41 top-level scripts (`v1_altline`, `v2_early_runs`, `v3_team_velocity`, `v4_bullpen`, `simple_drop_test`, `drop_sweep`, `sweep_edge_thresholds`, `anchor_robustness`, `backtest_handoff`, `gradient_signal`, `conditional_drop_reversion`, `investigate_line_edge`, `context_study`, `backtest_thesis`) test hypotheses that are **refuted and closed**. They are history, not tooling. Move them to `legacy/` so a reader can see the handful that are load-bearing. Keeps the falsification record; stops the repository reading as an active search for an edge that was concluded not to exist. **Do not move `calibrate_decay.py` or `features.py`** — despite their exploratory names they are imported by `encompass.py`, `program_a.py` and `remaining_runs.py` and are on the reproduction path. Verify imports before moving anything, and re-run the reproduction afterwards.

**8. Stop the alerting path entirely.** `send_test_alert.py`, the Discord notifier, `ripeness_check.py` and the ARM/CONFIRM ledger all serve a **refuted** binary gate — `RESEARCH_LOG.md` says so outright: "The legacy Discord alerts fire from the **refuted** binary gate — informational, not +EV." Live alerts from a refuted rule are a standing invitation to act on a signal the program disproved. Remove or hard-disable.

**9. Stop planning any product the data cannot support.** No signals product (Paper 1 refutes it). No data licensing (§7.1). No API. If a future idea requires selling odds data, it is answered in advance.

**10. Stop collecting without a named hypothesis.** The collector has run for ~24 days past the last checkpoint with no defined purpose in the repository. Under GD-2 the panels are "a growing asset"; §1.3 shows they are a growing asset with three structural defects that growth does not fix. **Every future byte should be collected against a written hypothesis or product, or not at all.** This is §10's central recommendation.

**11. Stop the arms race with book endpoints.** UA rotation, embedded guest keys, and the DK 403 are a permanent maintenance cost with escalating legal exposure (§7.1) in service of data that has already been characterized as insufficient. Do not invest further in access.

**12. On p-hacking risk — the program's actual posture is good; do not relax it.** GD-14's mandatory Track-2 discipline (arm 1 pre-registered before looking; arm 2 labelled `Exploratory` and barred from any paper without independent confirmation) is exactly right. The specific live risk is #10: an undefined collector plus 400k rows plus a frozen paper is the garden of forking paths waiting to happen. The stop-collecting rule closes it structurally, which is better than closing it by willpower.

---

# 10. Recommended operating state

[JUDGMENT throughout]

## 10.1 Should the collector continue, and for what purpose?

**No — not in its current form. Stop it, deliberately and in writing.**

Three reasons, all from this review: it is instrumented for a question it cannot answer (§1.3b); its output has a unit-of-analysis defect that further collection compounds rather than fixes (§1.3a); and it has been in an undefined state for 24 days, with a 4.5-day outage in its own history that nothing detected (§1.3c).

**The specific action:** stop the collector, write a governance-decision entry recording the stop and its reasons, and freeze the panels at their final state as **Benchmark Dataset v2 (2026.07)** with every defect in §1.3 and §5.3 disclosed in the changelog.

**It should only restart against a written hypothesis**, and if it does, the successor collector needs four things the current one lacks:
1. **A real game identifier** (`game_pk` at capture time, not reconstructed after).
2. **Full response provenance** per fetch, persisted: status, latency, payload size, `Date`, `Age`, `ETag`, `Cache-Control`, any edge markers. Without this, A4 is permanently unanswerable.
3. **Row-on-any-change**, not row-on-line-change — otherwise the vig process stays invisible.
4. **A liveness alarm external to the collector.** The 07-06 postmortem diagnosed this exactly ("the last report is frozen and still reads healthy"), the mitigation chosen did not cover it, and the 07-12 outage is the proof. This is a ~20-line watchdog, and it is the one piece of infrastructure work with unambiguously positive return.

If a **sharp live source** cannot be secured, do not build the successor at all. Two recreational books is the binding constraint on every remaining microstructure question, and no engineering fixes it.

## 10.2 What should be frozen and versioned now

- **Paper 1** — already frozen. Hold it. The only permitted edits remain the enumerated ones (§2.8).
- **Protocol v1.0** — frozen. Bump only on a genuinely new failure mode.
- **Benchmark Dataset v1 (2026.06)** — frozen; tag `v1.0`; Zenodo DOI, after §7.1.
- **The live panels → Benchmark Dataset v2 (2026.07)** — freeze at the final checkpoint, with a changelog entry recording: two books; 30 s cadence; **matchup keys, not game IDs**; the 07-06 and 07-12→07-16 gaps; the line-change-only logging rule; single-book status coverage; alt-line interleaving. **Publish the defects with the data or do not publish the data.**
- **The governance registers** — freeze as a historical record at the point of the stop decision. They are a completed artifact of a completed program phase, and their value is as a record, not as a live process.

## 10.3 What should remain live

Very little, deliberately.
- **The reproduction path** — `paper/make_figures.py`, `build_pdf.py`, the four analysis scripts, `tests/`. Add CI so it stays true. This is the only thing that must not rot.
- **The Governance Decision Log** — append-only, for genuine decisions (the collector stop, the Paper 2 rescope, the licensing resolution). Not for daily reviews.
- **`SUBMISSION_KIT.md` / `PUBLICATION_PACKAGE.md`** — active until Paper 1 is out.

## 10.4 What future data should only be collected against a hypothesis or product?

**All of it.** Concretely: no collection without (a) a written research question, (b) a stated estimand and identification argument, (c) the instrumentation the estimand actually requires — verified *before* collection, not discovered after — and (d) a stopping criterion. The program already has the machinery for (a), (b) and (d); §1.3(b) is what happens when (c) is skipped. Six months of collection cannot recover a field that was never captured.

## 10.5 Should Papers 1 and 2 be treated as a completed first research program?

**Yes — and this is the most important recommendation in this review.**

The arc is complete and unusually coherent: a trading hypothesis → its refutation → the generalization of the refutation into a boundary → a protocol for finding such boundaries → and, in Paper 2 rescoped, an honest account of what the instrument that produced it cannot see. That is a finished program with a real beginning, middle and end. **Declare it complete on publication.**

The alternative — treating Paper 2 as perpetually pending until SR-1 clears — means waiting on a criterion that depends on a feed dead since 2026-07-06 with an undiagnosed cause. That is not discipline. **The program's own doctrine already contains the resolution, in the design brief's own words: "A4/A5 may not clear at all — and that is a finding, not a failure."** Take the finding.

## 10.6 What should become a reusable research platform?

**The method and the governance pattern. Not the collector, and not the data.**

- **The Third Turn Protocol** — the seven rungs, S-01…S-14, the report template, the reference implementations. Domain-general as claimed, already written, already versioned separately from the data. This is the reusable asset.
- **The governance pattern** — Evidence Ledger → Assumption Register → Research Debt → Confidence Register → Decision Log → Inference Graph, with the discipline that a confidence level never moves on data volume and a chain may terminate before a claim. [JUDGMENT] **I regard this as more transferable than the protocol itself**, and it is currently filed under "optional reading" in the README. It deserves better framing: it is a working answer to "how does a small team avoid fooling itself," and it has receipts.
- **The reproduction harness** — pinned, CI-verified, so `v1.0` still builds in 2031.

**Not reusable:** the collector (wrong instrumentation), the panels (structurally limited), the ~15 refuted exploratory scripts, the alerting path.

## 10.7 What has credible potential as a business?

**One thing, modestly: the validity-review practice (§7.2, Opportunity A).** It monetizes the method, which the program clearly owns; it needs no data, no engineering, and no license; it is gated only on publication; and its credibility rests on the one thing that is genuinely hard to fake — a public record of refuting one's own results. Realistically it is a five-figures-per-engagement consulting practice bounded by founder hours. **That is a good outcome for a research program. It is not a company, and it should not be forced into becoming one.**

Everything else fails on a customer, a right, or a finding: the data has no buyer and possibly no owner; the API is a commodity in an arms race; and the signals product is refuted by the program's own central result.

---

## Closing assessment

[JUDGMENT] Third Turn set out to find an edge, found a boundary, and then — to its considerable credit — spent months building the apparatus to make sure the boundary was real rather than another artifact. That apparatus works: it caught the PI's own overreaches on the record, more than once, by name.

What the apparatus did not catch, and what this review found, is that **the instrument had three structural defects that no register described** — a missing game identifier, absent delivery provenance, and a 4.5-day silent outage. Governance that audits inference but not schema will find exactly the errors it is pointed at.

The right response is not more governance. It is to **ship the finished paper, write the honest impossibility result the data can actually support, stop the collector, and declare the first program complete.** The question the program set out to answer has been answered, twice — once about baseball, and once about the instrument. Both answers are worth publishing. Neither requires another row of data.

---

*Prepared 2026-08-22 against `alecmessino/third-turn@82fc298`. No frozen analysis, methodology document, gate, governance record or historical artifact was modified in the course of this review. All working-tree changes made during reproducibility verification were reverted; the tree was confirmed clean before this file was written. No new empirical research was conducted. Nothing was submitted or disseminated.*
