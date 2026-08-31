# Rights-safe aggregate figure inputs

These files exist so that figures whose generators read a private, licensed cache can still be
regenerated from a public release **without redistributing any third-party observation**.

Each file contains only binned or bucketed aggregates. No quoted line, price, odds value,
timestamp, book identity, fixture identifier or per-observation record is present, and none can be
reconstructed from what is here.

| File | Figure | Replaces | Contents |
|---|---|---|---|
| `fig_market_calibration_agg.json` | Paper 1, Figure 6 (market calibration) | `output/encompass_cache.json` | 10 reliability deciles (n, mean B, mean Y, 95% CI) over 2,505 snapshots; a 40-bin histogram of forecast error with counts; error mean and median |
| `fig_weather_runs_agg.json` | Visual Companion, Figure S3 (weather vs runs) | `output/encompass_cache.json` | 6 weather buckets (n games, mean runs, over-hit rate, Wilson interval) over 163 games |

**Why aggregates.** The generators originally read `output/encompass_cache.json`, which carries the
sharp-book line `B` per half-inning snapshot keyed to an MLB game identifier. That is a verbatim
third-party quoted value, and The Odds API's terms prohibit redistributing its data as downloadable
files. The cache is retained privately. The figures below are exactly reproducible from these
aggregates because both figures only ever displayed binned quantities.

**Not covered.** Visual Companion Figure S1 (single-game line movement) plots an observation-level
trajectory for one identified fixture. No aggregate can reproduce it without being the series
itself. It ships as a frozen rendered image only, and its source series is withheld pending written
permission from the data provider.
