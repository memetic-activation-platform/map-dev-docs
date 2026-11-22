# Visualizer evaluation baseline evidence — 2026-11-22

Revision: 1166e4bc4490bf824354c72367d86de413b3ed1d.
This is observed implementation evidence, not a design authority.

- [Measurements and source provenance](measurements.json): timer boundaries,
  source SHA-256 hashes, conditions and limitations.
- [Browser startup profile](browser-startup-profile.json): supplied by the user,
  correlated with the matching npm start timestamp; values preserved.
- [Native/build markers](npm-start-selected-markers.txt): selected lines from
  the matching npm-start.log, preserving original line numbers.
- [Composition samples](composition-samples.json): all three test samples,
  semantic operation counts, transport durations and response sizes.
- [Composition markers](composition-selected-markers.txt): source log excerpts.

Full raw logs remain at the local temporary paths listed in measurements.json.
Their retention is not guaranteed. This directory retains compact evidence;
no durable external raw-trace artifact was supplied. The earlier startup attempts
at 08:53 and 08:56 are excluded from the matched 10:31 sample.
