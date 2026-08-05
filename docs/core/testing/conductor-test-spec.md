# Conductor Test Framework — Design Specification

Sweettests in `tests/sweetests/` are written in **two distinct styles**. This document is
authoritative for the second one: **conductor tests**, which call zome externs directly on a live
SweetConductor rather than composing steps in the Dance Test Language.

For the first style, see the [Dance Test Framework](dance-test-spec.md).

---

## 1. Why Two Styles Exist

The Dance Test Framework asserts **client-side semantics**: staging, token chaining, commit
lifecycle, relationship graphs, saved-content equality. It reaches the guest only through the dance
envelope, and it observes results as the client observes them.

Some behavior is invisible from there:

- **which substrate action a write intent becomes** — a `Create`, or an `Update` addressed at a
  lineage root
- **whether the Integrity callback actually fired**, as opposed to a coordinator rejecting the same
  input earlier
- **the exact consensus-visible rejection message** a peer would see
- **what is packaged into a DNA**, and what a conductor will and will not dispatch

Conductor tests exist to assert exactly those things, at the boundary where they happen.

> **Routing rule.** If the behavior under test is expressible as a sequence of client operations,
> it belongs in a dance test. If the assertion is about guest execution, Integrity validation, or
> the substrate record itself, it belongs in a conductor test.

Adding a new `DanceTestStep` in order to reach a guest-side outcome is the wrong answer; see
[Test Step Authoring Guide §7](test-step-authoring-guide.md).

---

## 2. Shape of a Conductor Test

A conductor test is a plain async test function. There is no fixture, no `TestReference`, no
executor, and no registration in `dance_tests.rs`.

    #[tokio::test(flavor = "multi_thread")]
    async fn publish_version_is_rooted_at_the_create_and_round_trips() {
        let backend = setup_test_conductor().await;
        // ... call zome externs on backend.conductor / backend.cell, assert outcomes
    }

Each test constructs **its own backend**. Backends are never shared or pooled between tests.

The suites currently organized this way:

| Suite | Asserts |
|---|---|
| `holon_storage_tests.rs` | Version-aware holon node storage: which action each write intent authors, record-derived metadata, positional batch-read behavior, lineage rejection rules |
| `smartlink_tests.rs` | SmartLink write/expand/delete outcomes that pure comparator unit tests cannot produce |
| `pvl_validation_tests.rs` | PVL enforcement, with coordinator preflight and Integrity validation asserted as separate paths |
| `coordinator_surface_tests.rs` | Runtime coordinator boundary: what a production install will and will not dispatch |

---

## 3. Conductor Setups

Two setups are provided by `tests/sweetests/src/harness/helpers/mock_conductor.rs`. Both return an
`Arc<MockConductorConfig>` holding the `SweetConductor`, the agent key, and the `SweetCell`.

### 3.1 `setup_test_conductor()`

Installs the production DNA. This is the default, and the only setup that may be used to make
assertions about production behavior.

Its conductor config points every WAN endpoint — bootstrap, signal, relay — at an unroutable local
address. Sweettests run a single in-process conductor and never peer, so their network dependency is
accidental rather than designed; leaving an endpoint unassigned silently inherits a public
Holochain server and costs a probe timeout on every conductor start.

### 3.2 `setup_probe_enabled_conductor()`

Installs the production DNA, proves the probe coordinator is unreachable, then appends the probe
coordinator to that one conductor and proves production identity is unchanged. See §5.

> **Isolation rule.** A coordinator update mutates the DNA registered within a conductor. A
> probe-enabled backend must never be pooled with, or reused by, production-only assertions. Each
> probe-dependent test creates its own.

---

## 4. The Test-Probe Coordinator

### 4.1 What it is

`happ/zomes/coordinator/holons_test_probes` is a coordinator zome containing **only** authoring
seams that the typed production APIs deliberately cannot construct. It is built as a **loose WASM
artifact** and is absent from every production DNA and hApp manifest by construction.

Probes exist because some Integrity rules reject operations that canonical coordinator APIs make
unreachable. Proving through a real conductor that such a rule is wired into peer validation
requires a way to author the rejected operation.

> **The rejection is the assertion.** A negative-purpose probe whose call succeeds has failed its
> purpose.

### 4.2 Rules for probes

1. **Narrowest possible ingress.** Each probe is fixed to the single Integrity rule its test needs
   to reach. No generic raw-entry ingress, no generic link ingress. A probe that resolves a target
   must refuse every action and link type other than the one under test.
2. **No dependency on the production coordinator crate.** HDK extern symbols survive WASM linking
   from an rlib dependency. Depending on the production coordinator crate would reproduce its
   entire ingress surface inside the test artifact.
3. **Never called by production.** The crate is the complete, grep-able inventory of unsupported
   authoring.
4. **Pair a rejection with an acceptance where the rule is topological.** When a probe proves that
   an operation is rejected, a companion test should author the *same* seam in the accepted shape,
   so the rejection is demonstrably about the rule and not about the probe.

### 4.3 Artifact boundary enforcement

The boundary is enforced mechanically, not by convention:

- `happ/coordinator-surface.toml` is a source-controlled inventory of **every export of both
  artifacts**, including toolchain-generated symbols and callbacks. Each row carries an
  `exposure_kind`, a `classification`, and a rationale. Exact accounting is the point — it prevents
  a generated symbol from being mistaken for application ingress.
- `tools/happ-artifact-audit` compares the manifest against the WASM inside the bundles being
  shipped, in both directions, so an unclassified new export and a stale row for a removed one both
  fail.
- `--deny-production-test-only` fails the audit if any export classified `test_only` appears in a
  packaged DNA or hApp.

Production application functions belong under a packaged zome classified `supported` or
`legacy_ingress`. Test-only functions belong only under the probe zome and are prohibited from
production artifacts.

---

## 5. Isolated Augmentation

`setup_probe_enabled_conductor()` performs the following sequence. Steps 2, 7, and 8 are assertions
that run inside the helper, so tests that use it stay short.

1. **Install the production DNA** from the packed bundle.
2. **Prove the probe is unreachable** — dispatch must fail with `ZomeError::ZomeNotFound` as the
   precise inner cause, not merely with some error.
3. **Snapshot the pre-update DNA** — coordinator name set, production coordinator WASM hash,
   Integrity zome definitions.
4. **Read the loose probe WASM by path**, not inferred from a Cargo target directory. Build
   ordering (§6) is responsible for having produced that exact artifact.
5. **Append, never replace.** The coordinator update is handed *only* the new zome name. Including
   a second definition under the production name would swap out the active production coordinator
   instead of augmenting the conductor. The probe definition declares its dependency on the
   production Integrity zome.
6. **Restart the conductor.** Holochain 0.6.3 mutates the cached `DnaFile` during a coordinator
   update but does not rebuild the ribosome's derived zome-dependency index. Shutdown followed by
   startup reloads through the updated DNA cache; this is also the upstream coordinator-update
   test's persistence path.
7. **Assert five invariants** — the coordinator set is exactly production plus probe; the
   production WASM hash is unchanged; the probe entry references the freshly read WASM; Integrity
   definitions are unchanged; and rehashing the effective updated DNA definition still yields the
   installed DNA hash.
8. **Call a production extern once**, proving augmentation did not disturb the production
   coordinator at runtime and not merely in the definition.

Static artifact composition is **not** established here — that is the audit's job. These runtime
checks pin the Holochain behavior that static bundle inspection cannot establish.

---

## 6. Build Ordering

Because §5 reads a loose artifact from a fixed path, the sweettest entrypoint must produce it, and
the artifact boundary is re-audited before any test runs:

    build:happ  →  build:probes  →  check:happ-artifacts  →  sweet:test

`npm run sweetest` performs this sequence. The probe build is a separate script from the production
zome build; only the production coordinator is ever packed into the DNA or hApp. The audit also runs
as its own CI gate, so the surface policy stays visible rather than buried inside a test run.

---

## 7. Asserting Rejections

Holochain buries a rejection several error layers deep, and the layers differ depending on **where**
the rejection happened. Three helpers in
`tests/sweetests/src/harness/helpers/pvl_validation.rs` encapsulate that plumbing, and their
separation is itself an assertion about which path fired.

| Helper | Recognizes | Use for |
|---|---|---|
| `assert_commit_rejected_with_pvl` | `SourceChainError::InvalidCommit` | Integrity rejections carrying a `MAP-PVL-` code. Refuses a message without that prefix. |
| `assert_commit_rejected_with_message` | Same path, any exact message | Fixed-policy Integrity rejections that carry no PVL code |
| `assert_preflight_rejected_with_pvl` | `WasmRuntimeError` → `WasmErrorInner::Guest` | Coordinator preflight rejections produced *before* a host write |

Both commit helpers strip Holochain's `"Validation failed while committing: "` prefix and compare
the remainder for exact equality. Consensus-visible messages are pinned, never matched by substring.

> **Keep the two enforcement paths distinct.** Coordinator tests prove typed preflight behavior;
> narrowly scoped probes separately prove Integrity enforcement. Asserting them with one helper
> would let a coordinator guest error be mistaken for evidence of consensus validation coverage.

---

## 8. Conventions

- **Read the substrate directly when asserting about the substrate.** A test that claims a
  particular action was authored must read the raw `Record`, not the feature's own decoding —
  otherwise it validates the decoder against itself.
- **Construct identifiers through their real types.** A well-formed-but-unpersisted id should be
  built through `ActionHash` so its multihash prefix is correct by construction; hand-written bytes
  fail conversion and test the wrong thing.
- **Publish real endpoints.** Integrity rules that require action-hash identity cannot be exercised
  with synthetic ids; commit real holon nodes through the canonical ingress first.
- **Prefer the public ingress when the rule is reachable from it.** A probe is warranted only when
  the operation cannot be constructed through a production API.

---

## 9. Status

This document reflects the current implementation of the conductor test class and the coordinator
artifact boundary it depends on. It is the authoritative source for that boundary within the testing
documentation set; the packaged coordinator policy itself is owned by the Coordinator Surface
Policy.
