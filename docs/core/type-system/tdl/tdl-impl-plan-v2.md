# TDL Implementation Plan v2: Canonical Holon IR-Centered Toolchain

## Purpose

This plan supersedes the original TDL implementation plan and updates the earlier v2 correction.

The original TDL effort was rightly aimed at moving MAP schema authoring from Airtable-managed JSON exports to Git-managed TDL source files. Since then, the implementation has taught us two important things:

1. canonical MAP JSON import files are a general holon import format, not merely a schema format,
2. TDL remains a descriptor-authoring language specialized for concise type-definition work, even though its compiler target is that general holon import format.

The plan therefore centers a single **Canonical Holon IR** as the semantic source of truth for the tooling pipeline. Symbol tables, schema-aware validation, semantic diffing, code generation, and LSP services are derived layers over that IR, not competing semantic cores.

At the same time, this plan preserves the important distinction between:

- **canonical JSON** as a general-purpose holon import syntax,
- **TDL** as a concise schema/type authoring syntax defined by `tdl-spec.md`.

The goal is not to turn TDL into an arbitrary instance-authoring language. The goal is to make TDL compile through the same faithful holon representation that canonical JSON already implies.

---

## Reconciled Status

We are proceeding under the updated IR-unification replan established during implementation, not the older later-phase decomposition from the first v2 draft.

Current practical status in `map-holons`:

- `V2-A0` through `V2-A3` are substantially complete in spirit.
- `V2-A4` round-trip fidelity work has largely been completed and is now the baseline assumption for further work.
- `R1` toolchain stabilization is complete.
- The project is no longer primarily blocked on decompile/compile parity.
- The current planning/documentation work is reconciling the written plan with the implementation, after which the next implementation-heavy step is promotion of the Canonical Holon IR beyond the current tool-local implementation.

What is already true in the codebase:

- JSON -> TDL decompilation exists.
- TDL -> JSON compilation exists.
- `map-schema:check` exists and now runs through a largely unified semantic path.
- Round-trip tests now enforce that JSON -> TDL -> JSON preserves holon semantics and review-relevant structure, with only explicitly tolerated `meta` deltas.
- Diagnostics, symbol indexes, and schema-aware checks are increasingly derived from a single semantic center.

What is not yet true:

- the Canonical Holon IR has not yet been cleanly promoted out of `tools/map-schema` into a reusable shared layer,
- validation/diff/codegen/LSP are not yet all explicitly organized as derived services over that IR,
- runtime loader unification is intentionally deferred until after the tooling and authoring stack are stable.

---

## Core Decision

### Canonical semantic center

Use a single **Canonical Holon IR** as the shared semantic representation.

That IR is:

- holon-general,
- source-neutral,
- literal first,
- review-friendly,
- suitable as the common lowering target for JSON and the common emission source for generated JSON,
- capable of supporting schema-aware derived views without becoming schema-only.

### Derived layers

The following are derived layers over the Canonical Holon IR, not separate semantic truths:

- schema-aware descriptor projection,
- symbol indexes and lookup tables,
- diagnostics,
- semantic diff,
- code generation,
- LSP/editor services.

### TDL scope

TDL remains descriptor-focused under `tdl-spec.md`.

That means:

- canonical JSON remains the general holon import surface,
- TDL remains the concise authoring syntax for schema/type definitions,
- decompilation should prefer concise spec-native TDL where that is truthful,
- literal fallback is acceptable where concise surface forms would lose semantic fidelity,
- no hidden schema-only heuristics should reinterpret arbitrary holon content.

---

## Key Invariants

1. **One semantic middle**
   JSON, TDL, diagnostics, diffing, codegen, and LSP all normalize through the Canonical Holon IR.

2. **Holon generality is preserved**
   Canonical JSON must remain able to represent and import arbitrary holons, including but not limited to schema descriptors.

3. **Schema semantics are derived, not privileged**
   A schema descriptor is still just a holon in the generic IR. Schema-aware meaning comes from projection and validation layers, not from a separate foundational representation.

4. **Ordering is preserved structurally, not heuristically**
   File partitioning, holon ordering, property ordering, relationship ordering, and target ordering should be preserved end-to-end wherever the source provides them.

5. **Keys are exact**
   Key spelling normalization differences are not acceptable. Exact key preservation is part of semantic fidelity.

6. **No hidden semantic cores**
   There must not be one lookup model for the compiler and another unrelated lookup model for the loader story.

7. **Runtime handles stay out of the IR**
   The IR must not embed `TransactionContext`, `HolonReference`, staged handles, guest resolver state, or host-only APIs.

8. **Runtime loader unification is deferred**
   We will not push runtime loader unification ahead of authoring, validation, diff, codegen, and LSP stabilization.

---

## Relationship Between JSON, TDL, and the Canonical Holon IR

```text
canonical JSON
  -> general holon import syntax
  -> Canonical Holon IR

TDL
  -> descriptor-authoring syntax
  -> schema-aware lowering
  -> Canonical Holon IR

Canonical Holon IR
  -> literal holon semantics
  -> derived schema projection
  -> diagnostics / diff / codegen / LSP indexes
  -> canonical JSON emitter
```

This preserves the crucial asymmetry:

- JSON is general-purpose import syntax for holons.
- TDL is specialized authoring syntax for type descriptors.
- Both still meet at the same shared semantic middle.

---

## Current Implementation Baseline

The current codebase already provides the following starting point.

### Runtime loader baseline

The Holons Data Loader already supports:

```text
ContentSet
  -> parse/validate canonical JSON
  -> transient host-side loader graph preparation
  -> guest loader resolution passes
  -> staged and committed holons
```

This existing runtime path remains the authoritative loader behavior baseline.

### Tooling baseline

`tools/map-schema` already provides:

- JSON-to-TDL decompilation,
- TDL-to-JSON compilation,
- semantic checking,
- symbol dumping,
- round-trip validation coverage,
- a now-partially unified semantic implementation.

### Round-trip baseline

The gating round-trip invariant is now:

> For holon-shaped import files, JSON -> TDL -> JSON must preserve file partitioning, holon keys, descriptor types, property names and values, property order, relationship entries, relationship order, and target shape, with only explicitly whitelisted `meta` differences allowed.

---

## TDL Emitter Acceptance Rubric

The decompiler/emitter should be judged by the following rubric.

1. **Semantic fidelity is mandatory**
   Emitted TDL must compile back to semantically equivalent holon import content.

2. **Spec-native concision is preferred**
   When a holon can be expressed faithfully using concise TDL forms defined by `tdl-spec.md`, emit those concise forms.

3. **Literal fallback is correct behavior**
   When concise surface forms would lose information, change ordering, distort relationships, or imply semantics not present in the source, emit a more literal form.

4. **No hidden name-based reinterpretation**
   The emitter/compiler must not special-case relationship or property names as if some literal holon content were intrinsically privileged schema syntax.

5. **Bootstrap exceptions are explicit and narrow**
   Any bootstrap-specific compiler exceptions must be deliberate, documented, and limited to cases required by the spec or by foundational bootstrapping constraints.

---

## Reconciled Phase Plan

The older `V2-B` through `V2-H` decomposition is no longer the active sequencing model for implementation tracking. The active sequencing is the following reconciled phase plan.

### R1: Toolchain stabilization

Status: complete.

Planning metadata:

- Dev point estimate: 5
- Recommended GPT model: GPT-5
- Recommended reasoning level: medium

Purpose:

- stabilize round-trip behavior,
- stabilize diagnostics and validation flow,
- remove ambiguity about the current semantic center.

Completed outcomes include:

- round-trip fidelity tests as a gating signal,
- improved diagnostic clarity,
- stronger alignment between decompile, compile, and semantic checks.

### R2: Reconcile plan, docs, and naming

Status: underway.

Planning metadata:

- Dev point estimate: 2
- Recommended GPT model: GPT-5
- Recommended reasoning level: low

Purpose:

- align the written plan with actual implementation direction,
- replace stale phase sequencing,
- consistently use `Canonical Holon IR` language,
- clearly state that runtime loader unification is deferred.

Acceptance criteria:

- implementation docs reflect the current phase map,
- obsolete sequencing language is removed or clearly marked historical,
- the plan explicitly distinguishes JSON generality from TDL specialization.

### R3: Promote Canonical Holon IR beyond `tools/map-schema`

Planning metadata:

- Dev point estimate: 8
- Recommended GPT model: GPT-5
- Recommended reasoning level: high

Purpose:

- make the Canonical Holon IR a reusable semantic layer rather than a tool-local one,
- promote the semantic center into a dedicated WASM-safe shared crate instead of leaving it owned by `tools/map-schema`,
- preserve the source-neutral, literal-first lowering model for both JSON and TDL.

Work:

- introduce a small source-neutral literal value model in the shared semantic crate instead of promoting raw `serde_json::Value` as semantic truth,
- move the Canonical Holon IR, semantic resolution, derived symbol/index foundations, and narrow semantic diagnostics into the shared semantic crate,
- keep the shared crate structure explicit, with separate modules for literal values, IR types, index derivation, semantic resolution, and semantic diagnostics,
- keep `tools/map-schema` focused on JSON/TDL parsing, decompile rendering, and loader JSON projection,
- keep temporary migration shims in `tools/map-schema` only as forwarding re-exports during the transition,
- preserve build-local symbol identity for resolved references rather than introducing stable cross-run semantic identifiers in R3,
- keep public APIs small and explicit,
- preserve current round-trip and validation behavior while moving ownership.

Acceptance criteria:

- `tools/map-schema` no longer owns the only canonical IR implementation,
- the shared crate is the canonical owner of the IR, literal model, semantic resolution, symbol/index derivation, and semantic diagnostics,
- the IR is reusable by validation, diff, codegen, and future editor services,
- the resulting layer remains runtime-handle-free and WASM-safe,
- JSON and TDL still normalize through one semantic middle without treating JSON as the canonical literal substrate,
- compatibility shims in `tools/map-schema` are temporary and do not retain semantic ownership.

### R4: Validation and diff on Canonical Holon IR

Planning metadata:

- Dev point estimate: 5
- Recommended GPT model: GPT-5
- Recommended reasoning level: medium

Purpose:

- make validation layers explicit,
- make semantic review operate on the shared semantic representation.

Work:

- separate syntax validation, IR structural validation, schema-aware validation, and runtime-loader validation conceptually and in diagnostics,
- define semantic diff for schema-authoring use cases over the derived schema view,
- define generic holon diff where needed over the literal holon IR.

Acceptance criteria:

- diagnostics can be attributed to a named layer,
- semantic diff ignores irrelevant JSON noise,
- schema diff and generic holon diff are related but not conflated.

### R5: Code generation from Canonical Holon IR and derived schema indexes

Planning metadata:

- Dev point estimate: 5
- Recommended GPT model: GPT-5
- Recommended reasoning level: medium

Purpose:

- generate downstream artifacts from the same shared semantic center.

Work:

- generate Rust name constants,
- generate typed wrapper skeletons where appropriate,
- keep generated wrappers subordinate to established runtime reference APIs.

Acceptance criteria:

- code generation uses the same IR/index stack as validation,
- generated artifacts are deterministic,
- no parallel semantic scanner over generated JSON is needed.

### R6: LSP and editor services

Planning metadata:

- Dev point estimate: 8
- Recommended GPT model: GPT-5
- Recommended reasoning level: high

Purpose:

- expose the same semantic foundation to authoring tools.

Work:

- add source-ranged TDL frontend support where needed,
- publish diagnostics from the same semantic stack used by the CLI,
- add completion, hover, navigation, and later rename/refactoring.

Acceptance criteria:

- LSP diagnostics match CLI semantics for complete files,
- navigation and completion are backed by resolved semantic identity,
- editor features use derived indexes over the Canonical Holon IR rather than bespoke text heuristics.

### R7: Migration polish, workflow, and contributor ergonomics

Planning metadata:

- Dev point estimate: 3
- Recommended GPT model: GPT-5
- Recommended reasoning level: low

Purpose:

- make the authoring workflow sustainable and review-friendly.

Work:

- finish contributor documentation,
- clarify regeneration and review workflows,
- make semantic diff and round-trip checks practical in everyday development,
- ensure the decompiler is good enough for one-time core schema generation and ongoing maintenance.

Acceptance criteria:

- contributor workflow is documented and predictable,
- TDL is the practical source-of-truth path for schema authors,
- generated JSON remains easy to inspect and review.

### R8: Runtime Loader Unification

Planning metadata:

- Dev point estimate: 8
- Recommended GPT model: GPT-5
- Recommended reasoning level: high

Purpose:

- only after the authoring/tooling stack is stable, unify the runtime loader internals around the same Canonical Holon IR boundary.

Work:

- refactor JSON ingestion in the loader client to lower through the shared IR,
- refactor transient loader graph construction to consume that IR,
- preserve loader runtime behavior and guest resolution semantics.

Acceptance criteria:

- runtime loader behavior is unchanged for existing canonical JSON import files,
- the runtime path uses the same foundational IR model as the tooling stack,
- no parallel semantic ingestion model remains in long-term architecture.

---

## Historical Mapping from Earlier v2 Phases

The earlier milestone structure is still useful as provenance, but it should now be understood as roughly mapping into the reconciled phases above.

- `V2-A0` to `V2-A4` -> mostly covered by `R1`
- earlier plan-reconciliation work -> `R2`
- `V2-B`, `V2-C`, and `V2-D` intentions -> largely redistributed across `R3`, `R4`, and `R5`
- `V2-E` -> primarily `R4`
- `V2-F` -> `R5`
- `V2-G` -> `R6`
- migration and contributor hardening not cleanly represented before -> `R7`
- `V2-H` runtime integration refinements -> now intentionally deferred to `R8`

This document should be read using the reconciled `R1`-`R8` sequence as the active implementation plan.

---

## Repository Shape Direction

Keep the repository evolution incremental.

Near-term direction:

```text
shared_crates/type_system/... or equivalent WASM-safe shared crate
  canonical_holon_ir
  schema-aware derived projection
  diagnostics
  symbol/index layer

tools/map-schema
  JSON frontend
  TDL frontend
  canonical JSON emitter
  TDL emitter
  check / symbols / diff / codegen entrypoints
```

Rules:

- do not move foundational semantic ownership into `host/`,
- do not let runtime-only concerns bleed into the shared IR,
- do not create many crates before the IR boundaries are fully proven.

---

## Migration Rules

- Do not hand-edit canonical generated core schema JSON as part of normal migration work.
- Preserve current round-trip guarantees unless a phase explicitly changes them.
- Prefer moving tests and assertions before changing behavior.
- Preserve exact key spelling.
- Preserve source ordering structurally rather than with schema-specific ordering heuristics.
- Keep TDL descriptor-focused unless `tdl-spec.md` is deliberately expanded.
- Keep canonical JSON holon-general even while TDL remains descriptor-focused.
- Avoid introducing schema-name or relationship-name special cases that reinterpret literal holon content.

---

## Updated Source-of-Truth Model

Near term:

- schema authoring source of truth: `schema-src/**/*.tdl`
- generated runtime/review artifacts: `generated/json-imports/**/*.json`
- runtime loader input: canonical JSON `ContentSet`
- semantic review basis: Canonical Holon IR plus derived schema-aware diff/reporting

Longer term:

- TDL remains the maintained schema authoring format,
- canonical JSON remains the runtime interchange/import format,
- Canonical Holon IR is the shared semantic center for tooling,
- runtime loader unification may later align the loader internals to that same center.

---

## Open Design Decisions

1. What is the cleanest WASM-safe home for the Canonical Holon IR and its derived layers?
2. How much provenance and source-range information should live in the shared IR versus editor-facing companion layers?
3. What is the narrowest schema-aware projection API that still supports validation, diff, codegen, and LSP well?
4. Which validation failures should block JSON emission versus only block runtime loading?
5. When `R8` begins, should loader ingestion lower directly to the shared IR in one step, or should it retain an internal transitional adapter during migration?

---

## Success Criteria

This correction is successful when:

- JSON and TDL both flow through the same Canonical Holon IR,
- schema-aware validation is a derived layer over that IR,
- semantic diff, codegen, and LSP reuse the same semantic center,
- generated canonical JSON remains runtime-compatible and review-friendly,
- there is no second hidden semantic model in the compiler/tooling stack,
- runtime loader unification, when eventually undertaken, can adopt the same foundation rather than forcing another semantic redesign.

At that point, TDL authoring, canonical JSON generation, semantic validation, code generation, and IDE intelligence all share one trustworthy middle without sacrificing the holon generality of the existing loader architecture.
