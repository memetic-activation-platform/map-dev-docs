# Response to the Validation Fable Review

## Scope of This Response

We treated the fable review as a high-value adversarial review of the descriptor/validation architecture and responded across the following artifacts:

- Introduced a new type activation spec:
    - `docs/core/agent-spaces/type-activation-spec.md`

- Updated the EffectiveDescriptor design:
    - `docs/core/descriptors/effective-descriptor.md`
    - `docs/core/descriptors/effective-descriptor-impl-plan.md`

- Refactored the validation architecture and implementation plan:
    - `docs/core/validation/validation-arch.md`
    - `docs/core/validation/validation-impl-plan.md`

- Updated Issue 587 to reflect the semantic-version outcome:
    - `https://github.com/evomimic/map-holons/issues/587`

This response intentionally focuses on the descriptor/runtime validation track. The review also raised important concerns about older security, TrustChannel, AgentSpace, Dynamic Dance Dispatch, and code-level identity docs. Those remain valid follow-up areas but were not the primary scope of this pass.

## Overall Assessment

We accepted the central thrust of the review.

The most important correction was to stop implying that peer validation proves full semantic legitimacy. The docs now state the guarantee more precisely:

- PVL proves descriptor-relative validity.
- TypeActivation proves current AgentSpace recognition.
- Runtime validity is the composition of PVL plus mandatory activation filtering.

That distinction now shapes the EffectiveDescriptor spec, the new TypeActivation spec, the validation architecture, and the validation implementation plan.

## Accepted Substantially As Proposed

### 1. Descriptor-relative validation is the honest PVL guarantee

Accepted.

The validation architecture now states that Integrity/PVL proves only that a holon conforms to the exact content-addressed EffectiveDescriptor artifact it names.

PVL does not prove:

- activation
- social legitimacy
- global canonicality
- descriptor authorship correctness
- role visibility
- open-world semantic truth

The composed runtime guarantee is now explicitly:

    PVL descriptor-relative validity
    +
    mandatory read-time activation filtering
    =
    recognized runtime validity in this AgentSpace

### 2. Activation filtering needed its own spec

Accepted.

We introduced `type-activation-spec.md` to define activation as the governance and runtime-recognition step that answers:

    Which published EffectiveDescriptor artifacts does this AgentSpace currently recognize?

The spec now covers:

- activation records
- governance evidence
- activation status
- activated sets
- read-time recognition filtering
- write-side descriptor selection
- diagnostic bypasses
- why activation must stay out of Integrity/PVL

This directly addresses the review's concern that unactivated-but-structurally-valid data is expected DHT data and must be filtered at runtime rather than rejected by immutable validation.

### 3. Activation filtering should be mandatory at common read ingress

Accepted.

The TypeActivation spec now says activation filtering should be mandatory by default and applied at a common ReferenceLayer ingress rather than left to per-consumer discipline.

Normal runtime consumers should see a consistent activated set across:

- direct fetch
- collection resolution
- relationship traversal
- query results
- DAHN
- Dance dispatch

Diagnostic APIs may explicitly bypass the filter.

### 4. `must_get_valid_record` was the wrong retrieval model

Accepted.

The validation architecture now uses `must_get_entry(effective_descriptor_hash)` for `EffectiveDescriptorHash`.

The docs now explicitly acknowledge the consequence:

- `must_get_entry` retrieves content by entry hash.
- It does not prove the retrieved entry was valid.
- PVL must re-verify the EffectiveDescriptor carrier every time it uses the payload.

This matches the review's recommendation: trust comes from deterministic local re-verification of canonical content, not from another peer's record validity.

### 5. `EffectiveDescriptorHash` must be Holochain `EntryHash` of a canonical carrier

Accepted.

The EffectiveDescriptor spec now distinguishes:

- `EffectiveDescriptorDigest`: substrate-independent BLAKE3 digest of canonical DAG-CBOR payload
- `EffectiveDescriptorHash`: Holochain `EntryHash` of the canonical EffectiveDescriptor carrier HolonNode

The carrier contract now requires exactly the canonical carrier properties:

- `EffectiveDescriptorDagCbor`
- `EffectiveDescriptorDigest`

The carrier must exclude semantic/cosmetic/provenance/activation metadata such as display labels, timestamps, author-dependent metadata, local provenance, activation state, and arbitrary additional properties.

### 6. EffectiveDescriptor artifacts need a bootstrap base case

Accepted.

The validation architecture now defines a bootstrap path for EffectiveDescriptor artifacts.

EffectiveDescriptor artifacts:

- have no `effective_descriptor_hash` dependency
- are validated by fixed bootstrap PVL rules
- must contain the canonical carrier properties
- must decode as canonical DAG-CBOR
- must satisfy `EffectiveDescriptorDigest == BLAKE3(EffectiveDescriptorDagCbor)`
- must use a supported format version
- must respect resource bounds
- must contain only supported PVL-safe constructs

The exact artifact discriminant mechanism remains an implementation decision, but the architecture now requires it to be fixed, deterministic, and safe.

### 7. Cardinality and ordering do not belong in PVL at op granularity

Accepted.

The EffectiveDescriptor and validation docs now keep relationship cardinality, required relationships, exclusivity, global ordering, global absence, and transaction-wide coherence out of PVL.

These belong in:

- Nursery validation
- runtime filtering
- diagnostics
- higher validation layers

The only exception left open is a future transaction-manifest mechanism that might make specific multi-op invariants bounded and peer-reconstructible.

### 8. PVL needs quantified resource bounds

Accepted.

The validation architecture now has an explicit PVL resource-bounds section covering:

- HolonNode entry size
- property count
- property-key length
- scalar value size
- nested value depth and collection length
- EffectiveDescriptor payload size
- EffectiveDescriptor nesting depth
- property and relationship rule counts
- enum value count
- pattern length, if patterns ever become PVL-safe
- SmartLink tag size
- SmartLink decoded field count
- validation dependency count per op

The EffectiveDescriptor spec also defines interpretation-cost bounds for descriptor payloads.

### 9. Unknown PVL constructs must be rejected

Accepted.

The validation architecture now says PVL must reject unknown required semantics. It must not silently ignore unknown opcodes, rule forms, or EffectiveDescriptor format versions.

The implementation plan now includes unknown format, opcode, and required-rule rejection.

### 10. Patterns are unsafe for PVL unless bounded and deterministic

Accepted.

The EffectiveDescriptor spec now says pattern constraints are Nursery-only unless MAP adopts a future deterministic, bounded, linear-time pattern language suitable for PVL.

### 11. `conforms_to` is needed in the compiled surface

Accepted.

The EffectiveDescriptor payload now includes `conforms_to`.

The validation architecture allows local type-conformance checks using `conforms_to` when all required data is in bounded payloads.

This addresses the review's concern that a fully flattened descriptor surface still needs a way to support parent-typed relationships without PVL graph traversal.

### 12. SmartLink validation must be split into classes

Accepted.

The validation architecture now defines:

- SmartLink Class A: intrinsic link envelope and anti-graffiti checks
- SmartLink Class B: optional descriptor-backed relationship typing
- SmartLink Class C: non-PVL relationship semantics

Class A is now explicitly PVL.

Class B is a DNA-level design choice.

Class C is not PVL unless a future transaction-manifest mechanism makes a specific case bounded and peer-reconstructible.

### 13. SmartLink authorship and inverse-link provenance belong in Class A

Accepted.

The validation architecture now treats authorship policy as part of SmartLink Class A.

It also includes the inverse-link provenance pattern:

- inverse link carries forward-link provenance
- PVL may retrieve the forward link by `ActionHash`
- PVL verifies base/target reversal, relationship key match, direction marker correspondence, and author policy

The docs also state that open third-party annotation must be an explicit fixed policy; otherwise third-party link authorship is graph graffiti.

### 14. Updates must not retype holons

Accepted.

The validation architecture now says ordinary HolonNode updates must keep the same `effective_descriptor_hash` as the original.

Retyping means creating a new holon, not updating the descriptor binding of an existing holon.

### 15. EffectiveDanceSet belongs in the compiled surface, but only declaratively

Accepted with clarification.

The EffectiveDescriptor spec now includes `effective_dances`.

It is explicitly declarative and excludes:

- executable implementations
- WASM
- runtime bindings
- deployment information
- host capability grants

Executable dance binding remains a separate runtime artifact.

### 16. Receipts are evidence, not primary PVL proof

Accepted.

The validation architecture now states that ValidationResults and receipts are evidence, not the primary basis of peer validation.

Integrity may verify receipt format, digest binding, validator identity, or signatures only when the receipt acceptance rule is itself PVL-safe.

## Accepted In Spirit, With a Different Response

### 1. Semantic version should not be in the EffectiveDescriptor payload

The review and Issue 587 surfaced a tension around semantic versioning.

The counter-response is now reflected in the EffectiveDescriptor spec and Issue 587:

- Semantic version is publication metadata.
- It is assigned after the source `TypeDescriptor` HolonNode has been saved.
- It is attached through non-definitional `Version` / `VersionFor` relationships.
- It is not part of canonical EffectiveDescriptor payload content.
- It does not participate in `EffectiveDescriptorDigest`.
- Integrity/PVL does not need semantic version to interpret an EffectiveDescriptor.

Therefore the previous `semantic_version: SemanticVersion` field was removed from the canonical EffectiveDescriptor payload and runtime structure.

This accepts the review's broader authored/runtime split while rejecting the premise that semantic version belongs inside the compiled semantic payload.

### 2. Revision identity is needed, but semantic version is not the right pre-publication identifier

Issue 587 exposed the need to distinguish multiple revisions of the same logical type before semantic version assignment.

The response was to introduce `DescriptorRevisionId`.

`DescriptorRevisionId` identifies an authored revision candidate before publication/version assignment. It is useful for authoring, governance, merge, review, and publication workflows.

But it is not part of the canonical EffectiveDescriptor payload, because multiple authored revisions may legitimately compile to the same runtime semantic artifact.

### 3. The review suggested embedding stronger source/provenance fields in the payload; we kept provenance out of the canonical payload

The review suggested fields such as compiled-from identity and compiler identity inside the artifact bytes.

We accepted the need to separate semantic identity from provenance, but chose a narrower payload boundary:

- `CompiledFrom` is provenance/navigation.
- It is not part of the canonical DAG-CBOR payload.
- It is not required by PVL.
- Changing provenance without changing payload must not change the digest.

This keeps the canonical payload focused on effective semantic content.

There may still be a future need for compiler identity, compiler version, or reproducible-compiler receipts, but those are not currently treated as PVL-required semantic payload fields.

### 4. `described_by` consistency should not be a PVL cross-check

The review offered two options: drop `described_by` from the committed representation, or keep a path-independent committed claim.

We chose the simpler path for PVL:

- ordinary Holons bind to validation semantics through `effective_descriptor_hash`
- PVL derives the type claim from the decoded EffectiveDescriptor payload
- graph-level `DescribedBy` may still exist for navigation and introspection
- PVL never chases `DescribedBy`

This keeps peer validation content-addressed and avoids a second type-claim surface that could drift.

### 5. Relationship typing in PVL is left as an explicit launch-DNA decision

The review framed SmartLink Class B as a cost/benefit decision that may be defensibly deferred.

We accepted that framing.

The validation architecture now says descriptor-backed relationship typing may be included in PVL only if the launch DNA accepts the dependency cost.

If Class B is not included in launch PVL, edges are peer-admissible claims rather than peer-validated typed facts, and relationship typing must be enforced by Nursery and runtime filtering.

The important point is now explicit: adding Class B later requires DNA migration for existing spaces.

### 6. Spam/resource exhaustion is acknowledged through bounds and anti-graffiti checks, but not fully solved here

The review raised broader resource-exhaustion concerns.

This pass incorporated the parts directly relevant to descriptor/validation architecture:

- SmartLink anti-graffiti checks in PVL
- fixed link authorship policy
- validation dependency-count bounds
- entry/payload/descriptor/tag size bounds
- unresolved dependency diagnostics

Broader spam controls such as membrane design, per-agent quotas, migration/rescue dances, and security-model rewrites remain follow-up work outside this doc pass.

## Rejected Or Intentionally Not Adopted

### 1. Activation in PVL

Rejected.

Activation is temporal, revocable, and governance-mediated. Putting activation into immutable peer validation would make historic validation verdicts depend on later governance state.

Activation belongs in runtime recognition, not Integrity/PVL.

### 2. Semantic version in canonical EffectiveDescriptor payload or PVL

Rejected.

Semantic version is publication metadata, not compiled semantic content.

Runtime consumers that need version metadata should obtain it from publication, activation, or provenance context rather than from the canonical semantic payload.

### 3. A scalar `SemanticVersion` newtype required by PVL or EffectiveDescriptor payload

Rejected for this milestone.

Issue 587 now reflects that PVL and canonical EffectiveDescriptor decoding do not require a scalar semantic-version value.

A semantic-version facade or value may still be useful in publication/governance/coordinator-side APIs, but it is not required by the EffectiveDescriptor payload or integrity validation path.

### 4. ActionHash as descriptor identity

Rejected.

`ActionHash` is suitable for committed record/provenance identity, including ordinary holon endpoints and some provenance checks.

It must not participate in EffectiveDescriptor content identity.

The current model separates:

- `EffectiveDescriptorDigest`: portable payload identity
- `EffectiveDescriptorHash`: local Holochain EntryHash retrieval identity
- `ActionHash`: committed action/provenance identity
- `ExternalId`: route-sensitive foreign reference

### 5. Cardinality, required relationships, ordering, and global absence in launch PVL

Rejected for current PVL.

These are not op-local invariants under ordinary Holochain validation.

They remain Nursery/runtime/higher-layer concerns unless a future transaction-manifest mechanism makes specific cases bounded and peer-reconstructible.

### 6. Silent forward compatibility for unknown PVL semantics

Rejected.

Unknown required semantics must fail validation rather than be ignored.

Ignoring unknown semantics would silently weaken validation for old peers.

## Deferred Follow-Ups

The review also identified important issues that remain outside the completed response scope:

- arch-overview terminology and no-semantic-replication wording
- TrustChannel doc supersession or reframing
- security model rewrite around actual hard vs. soft enforcement boundaries
- Dynamic Dance Dispatch trust/sandbox/security model
- code-level `ExternalId` / `RemoteObjectId` shape
- distinct code newtypes for descriptor identity values
- cross-space compiled-surface provisioning flow
- PVL migration strategy across DNA versions
- per-agent quota and write-flood mitigation
- compiler identity / reproducible compiler receipts
- activation governance details beyond the conceptual spec

These are not rejected. They are follow-up architecture and implementation tracks.

## Net Result

The current docs now address the spirit of the fable review in the core descriptor/validation path.

The architecture is now clearer on the key boundary:

- EffectiveDescriptor defines the compiled semantic surface.
- PVL validates bounded descriptor-relative structure.
- TypeActivation defines AgentSpace recognition.
- Runtime reads compose PVL validity with activation filtering.
- Nursery owns transaction-local and snapshot-dependent validation.
- Trust, agreement, and social semantics remain above peer validation.

The major remaining design choices are now explicit rather than implicit:

- whether SmartLink Class B enters launch PVL
- exact numeric PVL bounds
- EffectiveDescriptor artifact discriminant mechanism
- PVL opcode / format migration strategy
- whether transaction manifests will ever make selected multi-op semantics PVL-checkable
- how broader spam, security, and dynamic execution concerns are handled in adjacent specs