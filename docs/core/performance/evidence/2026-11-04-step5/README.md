# November 4 post-unit-5 startup measurement

Latest mounted UI run: 2026-11-04T12:58:50.421Z, 196.011 s.
Comparator: 2026-11-04T12:05:01.868Z, 88.671 s, prior guest-profiled startup.
The screenshot's Canvas timer was unfinished. The pasted attachment contains five
historical records; startup-profile.json is the newest completed record.

Source Rust log: /private/tmp/map-descriptor-profile.log; immutable local snapshot:
/private/tmp/map-step5-measurement-2026-11-04/snapshot.log.
Prior snapshot: /private/tmp/map-guest-descriptor-profile-2026-11-04/snapshot.log.
Both logs contain descriptor-performance-profiling markers and use WASM_LOG=warn.

Call records select completed guest calls whose completion timestamp falls inside
the corresponding mounted startup interval. Concurrent calls overlap: summed call
and SDK-command durations are not additive wall-time partitions. Context arrays
retain recorded command/request and relationship spans. No storage source IDs are
included in these markers, so repeated relationship names alone do not prove that
the exact same source membership was fetched again.
