# Type Activation: Goals, Process, and Assurances (v1.0)

## 1. Core Purpose

Type activation is the governance and runtime-recognition step that bridges a published `EffectiveDescriptor` artifact into the semantic life of a particular AgentSpace.

It answers:

> Which published `EffectiveDescriptor` artifacts does this AgentSpace currently recognize as valid runtime type definitions?

That is distinct from two other questions:

- **What does the type mean?**
  Answered by the `EffectiveDescriptor`.

- **Does a holon conform to the descriptor it names?**
  Answered by PVL.

Activation answers:

- Is this descriptor recognized by this space?
- Under what governance authority?
- From what point in time?
- Is it active, deprecated, disabled, or superseded?
- Which version or compatibility range is accepted?
- May new instances be created against it?
- Should existing instances remain visible?

The composed guarantee is:

    PVL:
      the holon conforms to the EffectiveDescriptor it names

    Activation:
      the AgentSpace recognizes that EffectiveDescriptor

    Together:
      the holon is a recognized valid instance in this AgentSpace

---

## 2. What Activation Assures

### 2.1 Recognition Assurance

The AgentSpace explicitly recognizes the descriptor as part of its runtime ontology.

This prevents any member from publishing an arbitrary `EffectiveDescriptor`, creating holons against it, and having those holons silently appear as ordinary space data.

Without activation filtering, PVL only provides descriptor-relative validity:

    This holon conforms to the descriptor it chose.

Activation adds:

    This space recognizes that descriptor.

---

### 2.2 Governance Assurance

The activation was authorized under the space’s governance rules.

The activation record should therefore carry verifiable governance evidence. Depending on the AgentSpace model, that might include:

- steward signatures
- threshold signatures
- countersigned actions
- role-based approvals
- agreement references
- governance-decision references

The durable requirement is:

> A reader can independently verify that the activation was authorized by the governance authority recognized by the space.

---

### 2.3 Artifact-Binding Assurance

The activation identifies an exact compiled artifact.

It should bind to:

- the published `EffectiveDescriptor` content address
- the locally provisioned artifact reference, if different
- the semantic type identity
- the semantic version
- the `EffectiveDescriptor` format or encoding version, where relevant

Activation should never refer only to a human-readable type key such as `Person`, because that would leave ambiguity about the exact runtime surface being recognized.

---

### 2.4 Temporal Assurance

Activation establishes recognition over time.

Activation state is inherently temporal and revocable:

    Proposed
    Active
    Deprecated
    Disabled
    Superseded

This is precisely why activation does not belong in Integrity validation. The same historic holon op must not change from valid to invalid merely because governance later disabled its descriptor.

Instead, activation affects whether the holon appears in the space’s current semantic surface.

---

### 2.5 Runtime Consistency Assurance

All ordinary runtime consumers should see the same activation result.

The activated set should be applied at a common ReferenceLayer ingress rather than independently by:

- DAHN
- Query Engine
- Dance Dispatcher
- collection resolution
- direct fetch
- relationship traversal

Otherwise, one subsystem may recognize data that another excludes.

Activation filtering should therefore be mandatory by default, with an explicit diagnostic bypass.

---

## 3. What Activation Does Not Assure

Activation should not accumulate responsibilities that belong elsewhere.

It does not prove:

- that the `EffectiveDescriptor` was correctly compiled from the authored graph
- that the authored graph itself is socially legitimate
- that every dynamic validation rule is trustworthy
- that all existing holons conform to the activated descriptor
- that no conflicting descriptor is also active
- that the descriptor is globally canonical
- that the steward will never revoke or supersede it
- that the type is safe for every Dance or application
- that the type’s data is visible to every role

Those are separate concerns involving:

- compilation governance
- PVL and Nursery validation
- version policy
- agreements
- `RoleAccessDescriptor`s
- TrustChannels
- attestations

---

## 4. Activation Record

A conceptual activation record might contain:

    pub struct TypeActivationRecord {
        pub agent_space_id: AgentSpaceId,

        pub effective_descriptor_hash: EffectiveDescriptorHash,
        pub effective_descriptor_digest: Option<EffectiveDescriptorDigest>,

        pub type_name: TypeName,
        pub semantic_version: Option<SemanticVersion>,
        pub accepted_version_range: Option<VersionRange>,

        pub status: ActivationStatus,
        pub activation_revision: ActivationRevision,

        pub supersedes: Option<ActivationRecordId>,
        pub previous_activation: Option<ActivationRecordId>,

        pub governing_policy: ActivationGovernancePolicyRef,
        pub governance_evidence: GovernanceEvidence,

        pub activation_policy: ActivationPolicy,
    }

Possible status values:

    pub enum ActivationStatus {
        Proposed,
        Active,
        Deprecated,
        Disabled,
        Superseded,
    }

Possible policy fields:

    pub struct ActivationPolicy {
        pub allow_new_instances: bool,
        pub allow_updates_to_existing_instances: bool,
        pub include_existing_instances_in_normal_reads: bool,
    }

These policy distinctions matter because `Disabled` can mean several different things.

Activation records bind the AgentSpace, exact descriptor artifact, activation status, revision, governing policy, and governance evidence. They may duplicate `TypeName` and semantic version for indexing or verification, but the authoritative type semantics remain in the decoded `EffectiveDescriptor` payload.

Activation should bind the local `EffectiveDescriptorHash` whenever the artifact is provisioned into a Holochain AgentSpace. It should also bind `EffectiveDescriptorDigest` when available so readers can verify that the local carrier contains the expected canonical DAG-CBOR payload.

Activation must not bind only to a `TypeName` or version range. A type name describes the logical type; activation recognizes an exact artifact or an explicit compatibility policy over exact artifacts.

---

## 5. Governance Evidence

Governance evidence records why a reader should accept that the activation decision was authorized.

A minimal conceptual evidence structure is:

    pub struct GovernanceEvidence {
        pub policy_ref: ActivationGovernancePolicyRef,
        pub signer_identities: Vec<AgentPubKey>,
        pub signatures: Vec<Signature>,
        pub decision_digest: DecisionDigest,
    }

The signed activation decision should bind:

- AgentSpace
- `EffectiveDescriptorHash`
- `EffectiveDescriptorDigest`, when available
- activation status
- activation revision
- superseded activation, when present
- governing policy
- activation policy

The decision digest is computed over the canonical activation decision, not over mutable local indexes or display metadata.

Initial supported governance should be deliberately small:

- explicit authorized signer, or
- simple M-of-N threshold over configured signer identities

Richer governance models, agreement-mediated approval, delegated authority, and role-based procedures can be layered later. The durable requirement is still that a reader can independently verify authorization under the policy recognized by the AgentSpace.

---

## 6. Activation Verification

Activation verification derives trust in an activation record. It should proceed in this order:

1. validate activation record shape and required fields
2. verify descriptor existence by resolving `EffectiveDescriptorHash`
3. verify `EffectiveDescriptorDigest` against the carrier payload when present
4. recompute and verify the signed decision digest
5. verify signer identities and signatures
6. evaluate the governing policy, such as explicit signer or M-of-N threshold
7. resolve supersession and previous-revision links
8. resolve conflicts with other activation records for the same AgentSpace and descriptor family

Failure at any step prevents the activation record from contributing to the current activated set, but it should remain inspectable through diagnostics.

---

## 7. Activation History

Activation is append-only.

Later records may:

- activate
- deactivate
- deprecate
- disable
- supersede

Current activation state is derived from the verified activation history rather than stored as mutable state on the descriptor artifact.

Append-only history matters because activation is revocable while DHT validity is not retroactively mutable. A descriptor artifact may have been active for earlier holons, deprecated for a migration period, and disabled for new instances later. Diagnostics need that history.

Indexes such as `ActivatedDescriptorSet` are derived views. They may be cached, but they are not the authority.

---

## 8. Activation Lifecycle

### 8.1 Discovery

A descriptor is discovered:

- locally authored
- imported
- referenced by an application
- encountered through a TrustChannel
- required by another activated descriptor

No recognition is implied yet.

---

### 8.2 Artifact Acquisition

The space obtains the steward-published `EffectiveDescriptor`.

For a foreign descriptor:

    TrustChannel dereference
        ↓
    receive EffectiveDescriptor artifact
        ↓
    verify steward authenticity
        ↓
    verify content address

---

### 8.3 Local Provisioning

If the space uses Holochain, the artifact is committed into the local DHT so Integrity can retrieve it with a local `EntryHash`.

    published content address
        ↓
    canonical local carrier
        ↓
    local EntryHash

The local `EntryHash` may equal the steward’s published address when both use the same canonical Holochain carrier, but the cross-substrate architecture should not assume that.

---

### 8.4 Evaluation

Before activation, the space may evaluate:

- semantic type identity
- version
- compatibility
- compiler or format support
- required dependencies
- governance implications
- conflicts with existing activations
- whether the descriptor introduces unsupported PVL constructs
- whether required parent types are already active
- whether related access policies exist

This evaluation is a governance and coordinator concern, not a PVL concern.

---

### 8.5 Approval

The space’s governance authority approves the activation.

This produces verifiable governance evidence.

---

### 8.6 Publication

The activation record is committed to the space.

The activated-set index is updated.

---

### 8.7 Runtime Recognition

Normal reads begin recognizing holons bound to that `EffectiveDescriptor`.

---

### 8.8 Deprecation or Disablement

The space may later change its recognition policy.

This does not delete or retroactively invalidate DHT data.

Instead:

- new instance creation may be blocked
- existing instances may remain visible
- existing instances may become diagnostic-only
- migration recommendations may be surfaced
- a successor descriptor may be activated

---

## 9. Activation Filtering

Activation filtering should happen at a single logical boundary.

Conceptually:

    fn recognize_holon(
        holon: HolonNode,
        activated_set: &ActivatedDescriptorSet,
    ) -> RecognitionResult {
        if activated_set.contains(&holon.effective_descriptor_reference) {
            RecognitionResult::Recognized(holon)
        } else {
            RecognitionResult::Unrecognized(holon)
        }
    }

This filter should be applied to:

- direct holon fetch
- collection members
- query results
- relationship targets
- reverse relationship traversal
- DAHN navigation
- Dance operands
- command targets
- imported references

A diagnostic API can intentionally bypass the filter:

    get_holon(...)
      activation filtering enabled

    get_holon_diagnostic(...)
      activation filtering bypassed

---

## 10. Treatment of Unrecognized Holons

Unrecognized data is not necessarily malformed.

A useful classification is:

    StructurallyInvalid
    StructurallyValidButUnrecognized
    RecognizedAndValid
    RecognizedButSemanticallyProblematic

### Structurally Invalid

Rejected by Integrity and never integrated.

### Structurally Valid but Unrecognized

Integrated into the DHT because it conforms to the descriptor it names, but excluded from ordinary semantic views because that descriptor is not active.

### Recognized and Valid

Conforms to an activated descriptor and appears normally.

### Recognized but Semantically Problematic

May have Nursery warnings, conflicts, deferred checks, or social disputes.

This classification keeps PVL, activation, and higher-layer semantics separate.

---

## 11. Activation and Version Evolution

Activation should support multiple version strategies.

### Exact Activation

    Person 2.1.0 only

Appropriate where exact behavior matters.

### Compatible-Range Activation

    Person ^2

Appropriate where the space accepts compatible versions.

### Concurrent Activation

Multiple versions may be active simultaneously during migration.

    Person 1.x
    Person 2.x

### Supersession

A newer activation may supersede an older one without immediately disabling existing instances.

The space should decide separately:

- may new instances use the old version?
- may existing instances be updated?
- do old instances remain visible?
- is migration required or merely recommended?

---

## 12. Activation Dependencies

A type activation may depend on other activations.

For example, activating `Book` may require:

- `Person`
- `Organization`
- `BookSeries`
- value semantics used by its properties
- required Dance contracts
- relationship target types

The `EffectiveDescriptor` should make these dependencies explicit enough for activation-time analysis.

A policy decision is needed:

- automatically activate dependencies
- require explicit approval for each dependency
- permit unresolved dependencies but mark the type unusable
- bundle activation proposals

For governance clarity, explicit dependency activation is safer than silent transitive activation.

---

## 13. Activation and DAHN

DAHN is one of the most important consumers of activation state.

DAHN should normally:

- display activated types
- render properties from activated `EffectiveDescriptor`s
- expose relationships only when their runtime surfaces are recognized
- hide unrecognized holons and edges by default
- offer an optional diagnostic view of quarantined data
- signal deprecated or superseded types
- support migration affordances where available

Activation is therefore not merely a validation adjunct. It defines the currently navigable ontology of the space.

---

## 14. Activation and Type Authorship Across Spaces

For a foreign type:

    Space A stewards HolonType T
    Space A publishes EffectiveDescriptor E
    Space B provisions E
    Space B activates E
    Space B creates local holons that name E

Important boundaries:

- Space A controls the published descriptor artifact.
- Space B controls whether that artifact is recognized locally.
- Space B does not acquire stewardship of the authored HolonType.
- Space B may retain a local deterministic artifact copy.
- Space B may later disable E without affecting Space A.
- A new version published by Space A does not become active in Space B automatically unless policy explicitly allows that.

This preserves both stewardship and local sovereignty.

---

## 15. Assurance Matrix

| Assurance | Mechanism |
|---|---|
| Holon conforms to named descriptor | PVL |
| Descriptor artifact bytes are intact | Content-address verification |
| Descriptor is available locally | Provisioning plus local DHT storage |
| Descriptor is recognized by the space | Activation record |
| Activation was authorized | Governance evidence |
| Runtime consumers apply recognition consistently | Mandatory ReferenceLayer activation filtering |
| Descriptor remains recognized now | Current activation-set evaluation |
| Descriptor is appropriate for a role | `RoleAccessDescriptor` / Agreement |
| Descriptor was correctly compiled | Steward process, review, attestation, or future compiler proof |
| Data is globally semantically true | Not guaranteed by activation |

---

## 16. Core Design Principle

> **Activation is the revocable governance binding between a published EffectiveDescriptor and an AgentSpace’s current runtime ontology.**

The complete assurance model is:

    Published artifact authenticity
    +
    content-address integrity
    +
    PVL descriptor-relative conformance
    +
    governance-authorized activation
    +
    mandatory read-time activation filtering
    =
    recognized runtime validity within an AgentSpace

The unresolved design choices are primarily about activation authority, version policy, dependency handling, and treatment of disabled descriptors—not about the fundamental role of activation itself.
