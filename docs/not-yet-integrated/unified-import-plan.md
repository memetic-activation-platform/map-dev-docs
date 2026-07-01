# Reconciled Status + Immediate Next Actions

We are proceeding under the updated IR-unification replan expressed in this thread, not the older `map-dev-docs` V2 text for the later phases. The current canonical direction is: the `Canonical Holon IR` is the single semantic source of truth, while symbol tables, lookup structures, diagnostics helpers, and future LSP services are derived index layers over that IR. Current status is: `V2-A0` through `V2-A3` are substantially in place, `V2-A4` is in progress but not complete, and `V2-A5` has begun only in a limited sense. We should treat the project as being on the `A4/A5 boundary`, with `A4` still the gating step.

The gating requirement for `V2-A4` is now explicit: `JSON -> TDL -> JSON` must faithfully round-trip arbitrary holon-shaped import files, not merely schema-authoring patterns. That means preserving file partitioning, holon keys, descriptor types, property names and values, property order, relationship entries, relationship order, and target shape, with only explicitly whitelisted `meta` deltas allowed. No new schema-specific heuristics, ordering rules, or special treatment of relationship names should be introduced. In particular, `InstanceRelationships` must not be treated as semantically privileged; it is just another relationship name within a holon record.

## Immediate Next Actions

1. Finish `V2-A4` by removing remaining round-trip fidelity losses in the `JSON <-> TDL <-> Canonical Holon IR` path, using the round-trip test as the gating signal.
2. Preserve source ordering structurally, not heuristically, by keeping JSON-facing holon content in insertion-order-preserving structures end to end.
3. Eliminate any remaining name-based or schema-specific special cases in emit/decompile logic that reinterpret literal holon content.
4. Resume `V2-A5` only for validation that is clearly representation-neutral and does not depend on incomplete round-trip behavior.
5. After round-trip fidelity passes, complete `V2-A5` by centering checks and diagnostics on the Canonical Holon IR plus derived indexes, then proceed to later phases from that stable base.

Operationally, the rule for the codebase is: treat the Canonical Holon IR as a literal holon IR first, and only derive schema-analysis behavior from it second.