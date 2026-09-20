# September 2026 startup evidence

- [Canvas profiles](canvas-profiles.json): eight distinct browser profiles supplied
  in this investigation, deduplicated by UTC run timestamp. Includes all original
  phase and command records, with counts, total durations, and maxima. Durations
  are milliseconds. The browser's stored history contains multiple runs; the
  first entry in a pasted array is not necessarily the latest run.
- [Startup markers](startup-markers.txt): selected native startup markers from
  the September 19, 23:41 UTC app run, including provider setup, both LoadHolons
  calls, Core Schema bootstrap, Canvas selection, and native setup completion.

These are observational runs across an evolving uncommitted worktree, not a
controlled A/B. Build hashes, exact patches per browser run, and systematic
machine-load measurements were not captured. A phase's name identifies its
instrumented boundary, not exclusive CPU ownership. Command totals may be
nested within phase totals and must not be added to them.

Browser profiles originated in user-pasted `map.startupProfiles` histories.
The normalized file preserves records from attachments beginning with runs
17:22:25.919Z and 19:32:51.844Z; overlapping records were checked for equality.
The native markers originated in `/tmp/map-package-activation-profile.log`.
The normalized data and excerpts here are durable; those original local paths
are not required to read the results.
