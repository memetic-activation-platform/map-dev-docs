# Matched Holochain 0.6.3 / 0.7.1 evidence

Captured October 21, 2026, on macOS arm64. This published set contains **one final paired capture per experiment**, rather than every exploratory run. See [findings](../../holochain-link-read-findings.md) for the call paths, timing definitions and interpretation.

## Primary comparison: authenticated reads

- [authenticated-reads.json](authenticated-reads.json): all 20 observations (five holon fetches and five DescribedBy reads per version), per-operation medians, configuration/limitations, and captured source/artifact/lockfile hashes.
- [authenticated-read-summary.csv](authenticated-read-summary.csv): compact aggregate at matching client, adapter and HDK boundaries.
- [authenticated-diagnostic.rs](authenticated-diagnostic.rs) and [dance-adapter.rs](dance-adapter.rs): the exact common diagnostic and measured adapter source.

Both operations used authenticated `AppWebsocket.call_zome`. The broader relationship path contains one source-holon `get_details` and one `get_links`, returning the expected target reference. Each holon fetch contains one `get_details`. Every authenticated sample is retained. Outside-adapter medians are calculated from paired per-call differences, not subtraction of separately computed medians. The adapter interval ends before final logging, destruction and generated response serialization. The residual includes both incoming and outgoing work; its split and cause remain unmeasured.

## Supporting comparison: repeated guest HDK reads

- [link-read-hc06.json](link-read-hc06.json), [link-read-hc07.json](link-read-hc07.json): all raw samples and canonical link results, including first observations.
- [link-read-summary.csv](link-read-summary.csv), [link-host-controls.csv](link-host-controls.csv): repeated-sample statistics.
- [link-read-metadata.json](link-read-metadata.json): captured configuration, limitations, commits and source/artifact/lockfile/native hashes.
- [link-diagnostic.rs](link-diagnostic.rs) and [link-probes.rs](link-probes.rs): matched harness and common test-only HDK measurement functions.

Each bucket has 200 default, 200 Local and 200 repeated Local samples. Default/Local alternate pair order; repeated Local follows. Sample 0 for default/Local and the rotating host controls is retained but excluded from repeated statistics; first observations are not guaranteed cold. All retrieval strategies must return identical links. The clock, sys_time, zome_info and empty Local controls follow the bucket tests in the same conductor. Timers surround HDK calls inside a guest invocation; they exclude query construction, result comparison and the enclosing invocation. These probes use direct SweetConductor calls and must not be mixed into the authenticated-call profile. No native SQL control was repeated.

## Configuration and reproduction

Both versions used the same Rust 1.95.0 toolchain and native dev `opt-level="z"`; guest release `opt-level="z"`, LTO and one codegen unit. Each experiment bootstrapped a fresh single-agent Core Schema database, with live local rendezvous, full storage authority, and publishing/gossip disabled. Measurements ran sequentially after builds completed. Both versions passed both diagnostics and production/probe artifact audits. Version-specific dependency/API adaptations remain part of the comparison.

[Reproduction instructions](reproduce.md), [0.6 support patch](diagnostic-support-hc06.patch), [0.7 support patch](diagnostic-support-hc07.patch), and [compiler identification](toolchain.txt) accompany the common source snapshots. They preserve the full MAP-based test setup, not a minimal echo-zome reproducer. Local paths in metadata identify captured worktrees/artifacts; adapt paths on another machine. Captured log/native hashes provide provenance; verbose logs, binaries, duplicate exports and superseded exploratory captures are not part of this published set.

One fresh conductor per version per experiment and five authenticated calls per operation provide screening evidence, not independent-boot or production-percentile estimates. No production schema/index or caching-policy changes were introduced for the diagnostics. The cause of the extra time outside the adapter has not been isolated.
