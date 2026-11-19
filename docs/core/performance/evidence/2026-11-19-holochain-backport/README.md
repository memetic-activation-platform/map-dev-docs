# November 19: Holochain initialization-backport application capture

**Status:** substantial observed startup/navigation improvement; historical comparison,
not a matched whole-application attribution to the backport.
**Related implementation:** [MAP PR 879](https://github.com/evomimic/map-holons/pull/879),
head `13fb3bca1ad8066aceef727df101e65d22a0c330` examined for source analysis.
Actual running native/guest artifact hashes were not supplied.

## Observed application results

The new startup profile began at **2026-11-19T12:52:27.256Z** and completed
`mounted` in **18.790 s**. First/repeat navigation began at 12:53:54.174Z and
12:54:03.211Z; both completed `new node`.

The latest corresponding stored comparators are the November 4
[post-clean startup](../2026-11-04-step5/startup-profile-fresh.json) and
[first](../2026-11-04-step4/first-navigation.json)/
[repeat](../2026-11-04-step4/repeat-navigation.json) navigation captures.

| Measurement | Corresponding baseline | November 19 | Time reduction |
| --- | ---: | ---: | ---: |
| Canvas mounted | 94.944 s | **18.790 s** | **80.2%** |
| First DescribedBy | 86.263 s | **3.721 s** | **95.7%** |
| Close then DescribedBy | 8.604 s | **0.274 s** | **96.8%** |
| Materialize Canvas | 13.449 s | 2.025 s | 84.9% |
| Construct Canvas | 80.275 s | 16.576 s | 79.4% |

SDK command counts closely match: startup **429 -> 431** (two additional property
reads), first navigation **383 -> 383**, repeat **372 -> 372**. The gains do not
come from omitting top-level SDK commands. Result identities and complete data
content are not independently equated by these timing records.

Canvas SelectVisualizer accumulated time fell **44.861 -> 10.576 s** across
12 calls. First-navigation selection fell **71.480 -> 2.049 s** across 23 calls.
Repeated effective-descriptor access fell **3.815 -> 0.008 s** across four calls;
property-array classification fell **2.439 -> 0.008 s** across nine calls.

Small slower counters remain: startup RecordVisualizerUse **86 -> 132 ms**
(+46 ms), first navigation **102 -> 115 ms** (+13 ms); other positive command-time
deltas are approximately 1–3 ms. These single-sample differences do not establish
a persistent regression. Construction and selection remain the largest reported
Canvas costs. Command and span durations overlap; do not add them as exclusive
wall-time partitions.

## Why the backend call count increased

Completed-call selection uses the same completion-timestamp-within-UI-window
convention as the baseline. These are invocation counts, not CPU/SQL work units.

| Startup guest operation | Baseline | Current | Delta |
| --- | ---: | ---: | ---: |
| All completed guest calls | 299 | **592** | +293 (+98.0%) |
| query_relationships | 169 | **401** | +232 (+137.3%) |
| get_holon_by_id | 66 | **132** | +66 |
| fetch_all_related_holons | 0 | **7** | +7 |
| get_saved_holon_by_key | 41 | 37 | -4 |
| canonical | 10 | 3 | -7 |
| get_holons_by_ids | 2 | 1 | -1 |
| resolve_visualizer_usage | 11 | 11 | 0 |

The increase is concentrated in saved VisualizerUsage handling:

- `select_visualizer`: **80 -> 215** relationship queries (+135).
- `select_visualizer_usage`: **22 -> 94** (+72).
- Together these account for **207 of the 232** additional relationship queries.
- Current startup records **seven `cloned_saved`** resolutions, seven transient
  reuses and no `initialized_new` resolution. All seven bulk relationship fetches
  occur in `clone_saved_usage`; **74** current exact-holon fetches occur there.
- The baseline has **zero** exact-holon fetches under that clone phase. Instead,
  18 occur under `initialize_defaults` and three under `resolve_saved_inputs`.

The new relationship population is explicit: `ForSubjectType` **0 -> 40**,
`UsesVisualizer` **0 -> 40**, `SelectedForSlot` **0 -> 34**, `ApplicableToType`
**0 -> 20**, `SourceOf` **0 -> 21**, and `Extends` **25 -> 93**. Conversely,
`HasApplicableVisualizer` falls **9 -> 0** in the host-side call records.

Source paths: [slot Usage selection](https://github.com/evomimic/map-holons/blob/13fb3bca1ad8066aceef727df101e65d22a0c330/shared_crates/holons_core/src/dahn/candidates.rs#L236) and
[saved Usage preparation](https://github.com/evomimic/map-holons/blob/13fb3bca1ad8066aceef727df101e65d22a0c330/host/crates/map_commands_runtime/src/usage_transactions.rs#L532).

This matches the code paths: `select_slot_usage` inspects a Slot's saved
HasSelectedUsage members, validates their identity relationships, checks
applicability and traverses Extends. `UsageTransactions::select_prevalidated`
chooses `clone_saved_usage` when a committed configuration is found;
`project` calls `caller.clone_holon`. These reads support loading retained
configuration instead of creating fresh defaults.

The relationship-policy binding change
[`303c8950`](https://github.com/evomimic/map-holons/commit/303c8950), authored after
the baseline capture, also preserves SourceOf candidates. Intervening descriptor
retention changes are another reason the repeat is not a backport-only comparison.
The older navigation record explicitly included a background Commit that retired
derived Session state between navigations.

**Supported diagnosis:** different persisted-Usage/data-state paths explain most
of the added reads, with intervening MAP code changes also present. The backport
itself does not modify these MAP selection routines. Source identities, relationship
result sizes and a paired current-code store control were not captured, so the
records do not justify allocating every extra query to one cause or claiming all
additional reads are redundant. Detailed deltas are in [backend-work.json](backend-work.json).

Despite more calls, the startup relationship-call median fell **307.363 -> 2.013 ms**;
its summed duration fell **51.882 -> 14.499 s**. All **1,220** logged guest calls
in the original application capture reported success, with no ERROR-level events.
These observations agree with the earlier matched invocation diagnostic while
remaining distinct from its causal evidence.

## Publication warnings: repeated attempts without remote destinations

The original analysis counted **48,270** `NoPeersForLocation("publish", ...)`
warnings. The app remained running and the log continued growing. A later frozen
snapshot contains **80,450** warnings: **five sweeps of 16,090 distinct routing
locations**, with identical location sets in every sweep. The original count is
three such sweeps. These are not 48,270 unique missing holons or agents; a publish
batch for a basis can contain multiple DHT operations.

| Sweep start (UTC) | Warnings | Distinct locations |
| --- | ---: | ---: |
| 12:52:22.830 | 16,090 | 16,090 |
| 12:53:24.363 | 16,090 | 16,090 |
| 12:55:27.676 | 16,090 | 16,090 |
| 12:59:37.280 | 16,090 | 16,090 |
| 13:04:40.499 | 16,090 | 16,090 |

Holochain's publish implementation returns this error for a nonempty batch when
there are no eligible remote destination URLs. Peer selection excludes agents
local to the conductor and filters unresponsive peers; tombstones and missing
URLs are also excluded. **A single-agent/single-conductor run therefore naturally
has no remote publication destination.** The warning alone does not prove the
network has exactly one agent: discovery, connectivity or peer-responsiveness
problems can produce the same result in a multi-node deployment.

The publish workflow records publication time only for successfully admitted
batches and keeps its loop active while operations still need publishing. The
consumer backs off from one minute to a five-minute maximum, matching the
observed approximately 1-, 2-, 4-, and 5-minute intervals. The current log runs
with **MAP_START_MODE=prod**; MAP's dev-mode logging normally suppresses these
publish warnings at ERROR while leaving publication itself enabled. Production
retains WARN, which explains why the failure stream is visible here.

This is consistent with an isolated agent and is not evidence of failed local
reads/Commit or data loss. It **does mean remote publication/replication has not
been established for these attempts**. It also performs repeated real work and
produces substantial log volume. None of the five bursts overlaps the three
supplied UI timing windows, so the trace does not establish warning-emission
contention as the cause of those UI durations.

Source checkpoints examined: `holochain` 0.7.1
`publish_dht_ops_workflow.rs` and `publish_dht_ops_consumer.rs` (preserved in PR 879),
`holochain_p2p` 0.7.1 `src/spawn/actor.rs` (`publish`), and `kitsune2_core` 0.5.2
`src/common.rs` (`get_responsive_remote_agents_near_location`, `filter_local_agents`).
The publish workflow is outside the init/source-chain backport's changed files.
See [publication-warning-bursts.json](publication-warning-bursts.json).

## Comparison limits and provenance

- This is a retained-store production-mode launch: conductor launch **3.1 s**,
  discovery of an existing Space, retained saved Usages, and no `load_holons` call.
  It does **not** measure cold Core Schema loading or package activation.
- The comparison spans November 4 -> November 19 and intervening MAP changes.
  The November 4 step-5 notes record **WASM_LOG=warn**; this run records
  **WASM_LOG=info**. Neither code nor data nor logging was held fully constant.
- The new process reports optimized dev code. Actual running native/guest hashes
  were not supplied, so examining source at the PR head is not binary provenance.
- A single application capture does not isolate a backport-only speedup. The
  earlier matched native diagnostic remains the evidence for the initialization
  scan fix. Backend count changes are not necessarily changes in total CPU work.

The raw log is retained **locally only** at
`/private/tmp/map-holochain-backport-profile-2026-11-19.log`; the frozen analysis
copy is `/private/tmp/map-backport-app-comparison/backend-snapshot.log`.
It is not uploaded as a durable public artifact. [provenance.json](provenance.json)
records the frozen byte count/hash and this retention limitation. The compact
profiles, call records, deltas and selected markers needed for this comparison
are retained alongside this page. Raw-log timestamps and filenames use UTC where
specified; the run occurred on November 19 in America/Denver.

| File | Contents |
| --- | --- |
| [browser-profiles.json](browser-profiles.json) | Supplied completed startup and first/repeat navigation reports |
| [comparison.json](comparison.json) | Command/phase differences against corresponding baselines |
| [backend-summary.json](backend-summary.json) | Guest-call durations and counts in each UI window |
| [startup-calls.json](startup-calls.json) | 592 completed startup call records and contexts |
| [first-navigation-calls.json](first-navigation-calls.json) | First navigation call records |
| [repeat-navigation-calls.json](repeat-navigation-calls.json) | Repeat navigation call records |
| [backend-work.json](backend-work.json) | Operation, relationship, command and Usage-phase count deltas |
| [publication-warning-bursts.json](publication-warning-bursts.json) | Fixed-snapshot warning counts, timestamps and repeated location-set checks |
| [selected-backend-markers.txt](selected-backend-markers.txt) | Launch/filter and first/last warning markers per burst |
| [provenance.json](provenance.json) | Observed settings, input hashes and raw-log retention limits |

## Subsequent fresh Welcome capture

The separate [fresh Welcome run](../2026-11-19-fresh-welcome/README.md) measures
Core Schema provisioning: 81.852 s with 1,180 holons, approximately unchanged
against the historical matching command timer. A 35.116 s interval remains
after loader completion before the host round-trip report. This cold-store
measurement complements the retained-store startup/navigation results above.
