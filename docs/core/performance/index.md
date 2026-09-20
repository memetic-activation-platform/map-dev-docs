# Performance

This section preserves performance investigations, measurements, experiments,
rejected approaches, and recommendations for MAP Core. It records what was
observed under specific conditions; it does not define runtime semantics or
replace the owning design specifications. See the
[document role manifest](../document-role-manifest.md).

## Investigations

| Investigation | Status | Strongest current finding |
|---|---|---|
| [Application startup and Canvas](startup-and-canvas.md) | Regression and recovery observed | Canvas recovered from 118.7 s to 14–15 s while schema load remained slow |
| [Caching lessons](caching.md) | Implemented policies and future options | Cache lifetime and descriptor lookup cost differ fundamentally between host and guest |
| [Core Schema load](schema-load.md) | Open; measurements from September 19–20, 2026 | Substantial latency remains after coordinator return; increasing integrity WASM initial memory to 4 MiB made it worse |

GitHub issues track implementation scope, acceptance criteria, and delivery.
These pages preserve evidence and reasoning beyond an issue's lifetime.
[DevDocs issue #46](https://github.com/memetic-activation-platform/map-dev-docs/issues/46)
establishes this section.

## Key lessons from the startup investigation

[Key architectural insights](key-insights.md) explains how execution context,
self-description, relationship semantics, and runtime infrastructure shape these
results and future optimization choices.

- Optimize a named execution phase, not an undifferentiated startup total.
- Shared code does not imply shared policy: host retention and guest request-local
  reuse have different costs and purposes.
- Cache-policy lookup can cost more than the read it governs. Protect declared
  definitional reuse and avoid guest descriptor lookup merely for retention.
- Observed recovery is valuable evidence, but multiple simultaneous changes do
  not establish individual causality or quantify the benefit of TTL.
- Bigger allocations and more caching are hypotheses, not guaranteed improvements.
- Preserve failed experiments, identity-level measurements, and environment
  differences so later work does not repeat earlier mistakes.

## Measurement conventions

- Name the workload and timer boundaries. Distinguish Core Schema loading,
  activation-package loading, home-Dancer selection, and Canvas startup.
- Identify the execution context: host, coordinator guest, native conductor,
  or integrity guest. Shared source code does not imply shared cache lifetime
  or equivalent runtime costs.
- Record build profile, optimization, dependency versions, logging/profiling,
  artifact hashes, input counts, and fresh versus reused process/state.
- Repeat measurements. Prefer alternating controls and treatments with one
  changed variable. Keep individual runs, not only averages or medians.
- Separate wall time from CPU samples, waiting, and overlapping timers.
  Independently calculated component medians need not sum to the total median.
- Record instrumentation overhead and differences between test and app paths.
  Do not infer an app speedup from a different harness alone.
- Check correctness and workload counts alongside performance. Faster execution
  caused by skipped work is not an equivalent result.

## Recording an investigation

Use a focused page per workload or problem, with:

1. Scope, status, dates, and links to owning architecture/specifications.
2. Execution boundaries and a timing table.
3. Confirmed findings, including the evidence supporting each claim.
4. Experiments: hypothesis, controlled change, results, limitations, and decision.
5. Open questions and recommendations, clearly distinguished from findings.
6. Links to durable supporting evidence and the implementation issue when available.

Keep compact results, selected log excerpts, and provenance under `evidence/`.
Do not rely on temporary filesystem paths. Large raw traces and binaries belong
in durable external artifacts linked from the evidence record, with checksums
and retention limitations. Exclude credentials and unrelated application data.

Preserve unsuccessful experiments. When later results supersede a conclusion,
add the new conditions and evidence rather than silently rewriting history.
Promote accepted architectural decisions into their existing authoritative
specifications and link to them here.
