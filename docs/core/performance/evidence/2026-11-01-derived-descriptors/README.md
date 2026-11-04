# Initial ValueType and PropertyType DerivedDescriptor observation

The [Canvas investigation](../../startup-and-canvas.md#november-1-2026-initial-valuetype-and-propertytype-derived-descriptors)
records this historical comparison, supplied again by the user on November 2.

- [canvas-profiles.json](canvas-profiles.json): completed November 1 browser profiles
  at 14:37:10.999 and 19:33:55.929 UTC.
- [comparison.json](comparison.json): request-associated guest-call and relationship
  counts recomputed from retained parsed native traces, with provenance limits.

Request-associated calls must start and finish inside the profile interval.
This gives 383 calls before and 384 after. The previously reported 385 for the
later run admitted a boundary call via a small interval tolerance; use the strict
384 count when comparing startup requests. Excluding background calls matters:
the earlier native trace also contains background work during the same wall window.

These observations support faster mounting with unchanged relationship/Extends
query counts, not demonstrated DD cache hits or an achieved memoization saving.
Full raw native logs, matching source patches/artifact hashes and CPU conditions
were not archived for this pair; do not treat it as a controlled causal experiment.
