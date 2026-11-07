# Guest trace diagnostic experiment

This diagnostic run is **outside the measurement chain**. It compares uncorrected Step A
`ced364a4` with the same source and only the guest `SmartReference::get_rc_holon` trace commented
out. The patches, metadata, measurements and original `comparison-to-step-a.json` are preserved
byte-for-byte from the temporary capture. This is not the corrected `f374e25c` Step A checkpoint.

The trace removal still awaits the architect’s agreement. The cache checkpoint and corrected
checkpoint both retain the trace. No production change is included with this evidence.

Each workload directory retains its raw log locally. Logs are git-ignored; re-parsing requires a
checkout or archive where those logs were retained. Metadata and patches record the exact source,
artifact and conditions. The original comparison JSON is diagnostic evidence, not a substitute for
matched capture-foundation checks or replication.
