# MAP Knowledge Evolution Architecture (v0)

**Status:** Draft  
**Document Type:** Architectural Framework  
**Abbreviation:** KEA

## 1. Purpose

The MAP Knowledge Evolution Architecture (KEA) defines how knowledge-bearing holons evolve, branch, merge, compose, release, and become adopted across independently governed spaces.

The architecture applies both to individual holons and to larger stewarded knowledge artifacts composed of many holons, including:

- schemas
- ontologies
- vocabularies
- taxonomies
- governance models
- agreements
- protocols
- methodologies
- curricula
- standards
- other coherent bodies of structured knowledge

KEA provides the overarching conceptual framework for a family of subordinate design specifications. It establishes the architectural principles, primary concepts, lifecycle stages, and responsibility boundaries within which those detailed mechanisms operate.

KEA does not assume that all participants converge on one authoritative representation of knowledge. Instead, independently stewarded knowledge may evolve along distinct lineages, remain in use indefinitely, and become interoperable through explicit mappings, releases, dependencies, and voluntary adoption.

The central principle is:

> Knowledge evolution extends immutable lineages and offers new states for adoption. It does not silently replace prior states or push changes into dependent artifacts.

---

## 2. Architectural Scope

KEA governs five related forms of evolution:

1. **Holon evolution**  
   The creation of new immutable versions of an individual holon.

2. **Concurrent evolution**  
   The creation and reconciliation of multiple versions derived independently from a shared predecessor.

3. **Composite-artifact evolution**  
   The evolution of a knowledge artifact whose definition includes exact versions of component holons or subordinate artifacts.

4. **Release evolution**  
   The intentional designation of a coherent published composition as an adoptable milestone.

5. **Dependency evolution**  
   The explicit adoption of newer versions or releases by dependent holons and knowledge artifacts.

KEA defines how these forms relate but delegates their detailed implementation to subordinate specifications.

---

## 3. Architectural Drivers

### 3.1 Preserve information

Concurrent changes must not be discarded merely because another change was committed later.

A last-write-wins policy may produce convergence, but it does so by selecting one state and suppressing another. Such a policy is an arbitration rule, not evidence that no conflict existed.

KEA therefore preserves concurrent lineage extensions until they are explicitly reconciled.

### 3.2 Support local autonomy

An agent or agreement-based space must be able to evolve its own knowledge without requiring synchronous coordination with every dependent or collaborating party.

### 3.3 Prevent silent semantic drift

A dependent artifact must not change merely because one of its dependencies publishes a new version.

Adoption is explicit and produces a new version of the adopting artifact.

### 3.4 Distinguish development from release

Not every committed state is suitable for coordinated adoption.

KEA distinguishes:

- fluid staged work
- committed and published versions
- intentionally designated releases

### 3.5 Support semantic composition

Knowledge artifacts are not merely files or opaque packages. Their component relationships may be definitional, version-specific, typed, constrained, and subject to compatibility analysis.

### 3.6 Preserve provenance

The architecture must retain enough lineage and stewardship information to explain:

- where a version came from
- which versions it supersedes or merges
- which composition a release represents
- who authorized a release or conflict resolution
- which dependency versions were adopted

### 3.7 Permit pluralism

Different agents and spaces may retain different vocabularies, schemas, governance models, and interpretations.

Interoperability may emerge through mappings and negotiated commoning rather than forced replacement.

---

## 4. Core Principles

### 4.1 Immutable publication

Once committed, a version is immutable.

Changes produce new versions rather than mutating existing versions.

### 4.2 Complete lineage preservation

Every committed version remains part of the historical record unless an exceptional governance or privacy process explicitly limits its availability.

### 4.3 Pull rather than push

Publishers offer new versions and releases.

Dependents decide whether and when to adopt them.

### 4.4 Branching is valid state

Multiple current heads in one lineage are not inherently erroneous.

They represent concurrent or otherwise divergent evolution.

### 4.5 Conflict is explicit

A conflict exists when independently valid changes cannot be composed without a semantic choice.

Conflicts must not be hidden by generic convergence rules.

### 4.6 Automatic merge must be semantics-preserving

Changes may be merged automatically only when the applicable merge semantics establish that the result preserves the relevant information and satisfies all constraints.

### 4.7 Release is a stewardship act

A release is not merely a version number or tag.

It is an intentional assertion that a specific published composition is sufficiently coherent and stable to be offered for adoption.

### 4.8 Adoption creates a new dependent state

Even when adoption is automated, the adopting holon or artifact receives a new version.

Existing versions remain unchanged.

### 4.9 Derived state should not be stored as intrinsic truth

Properties such as current head, latest version, preferred version, or current release are context-dependent and should normally be resolved through queries or policies rather than stored as immutable properties of a version.

### 4.10 Meaning governs evolution

The semantics of a property or relationship determine how its changes affect versioning, merging, compatibility, and composition.

Storage order, arrival time, or physical replication alone must not determine semantic outcomes.

---

## 5. Core Concepts

## 5.1 Holon Version

A **Holon Version** is an immutable committed state of a logical holon.

A version contains the complete definitional state required by the applicable descriptors, rather than merely a delta from a predecessor.

The runtime representation of a saved holon combines two distinct sources of
state:

- persisted semantic content decoded from the `HolonNode` entry
- runtime version metadata derived from the enclosing Holochain `Record`

Only the persisted semantic content participates in descriptor-defined
equivalence and ordinary property operations. Record-derived version metadata
identifies the saved version and its lineage but is not authored domain
content.

A version may have:

- no predecessors, if it is the lineage root
- one predecessor, if it is an ordinary successor
- multiple predecessors, if it reconciles multiple branches

---

## 5.2 Lineage

A **Lineage** is the directed acyclic graph of all committed versions descended from one lineage root.

A lineage represents the evolution of one logical holon.

A lineage is not assumed to be linear.

Example:

    v1
    ├── v2a
    │   └── v3a
    └── v2b
        └── v3b

A later merge may reconcile the branches:

    v1
    ├── v2a
    │   └── v3a ──┐
    └── v2b        ├── v4
        └── v3b ───┘

---

## 5.3 Lineage Root

The **Lineage Root** is the first committed version in a lineage.

It provides a stable identity for the logical holon across all of its versions.

Every version in a lineage resolves to the same effective lineage identifier.

The lineage root is not a separate holon representing the lineage. It is the first version itself.

The root does not duplicate its own identifier in a persisted lineage field.
Its runtime `lineage_id` is absent, and its `version_id` supplies the effective
lineage identifier. For every update, runtime `lineage_id` identifies the root
`Create` action.

Conceptually:

    lineage_root(v1) = v1
    lineage_root(v2) = v1
    lineage_root(v3) = v1

The detailed representation of this identity is defined by the Version Lineage Design Specification.

---

## 5.4 Runtime Version Metadata

**Version Metadata** is runtime state derived when the storage layer decodes
the Holochain `Record` enclosing a saved `HolonNode` entry.

Its intended shape is:

```rust
struct VersionMetadata {
    version_id: LocalId,
    lineage_id: Option<LineageId>,
}
```

The fields have the following semantics:

- `version_id` identifies the exact persisted holon version represented by the
  enclosing record.
- `lineage_id == None` means the version is the lineage root.
- `lineage_id == Some(root)` means the version belongs to the lineage rooted at
  `root`.

The storage layer derives these values from the enclosing Holochain action:

- For a `Create`, `version_id` is derived from the record's action hash and
  `lineage_id` is `None`.
- For an `Update`, `version_id` is derived from the record's action hash and
  `lineage_id` is derived from `Update.original_action_address`.

The effective lineage identifier is:

```text
lineage_id.unwrap_or(version_id)
```

`VersionMetadata` is not serialized into the persisted `HolonNode`. In
particular, `LineageId` is not a `PropertyType`, is not definitional state, does
not participate in definitional equivalence, and cannot be changed through
ordinary property operations.

Version metadata establishes exact-version identity and lineage membership.
It does not establish immediate ancestry, which remains represented by
`Predecessor` and `Successor` SmartLinks.

---

## 5.5 Predecessor

A **Predecessor** is an immediate prior version from which a version descends.

Predecessor references form the edges of the version DAG.

A predecessor reference:

- identifies an immediate parent, not every ancestor
- is immutable
- is part of version provenance
- must reference a version in the same lineage
- must not create a cycle

Examples:

    ordinary successor:
    v2 → predecessor v1

    concurrent branches:
    v2a → predecessor v1
    v2b → predecessor v1

    merge:
    v3 → predecessors {v2a, v2b}

`Predecessor` is an ordinary declared relationship persisted as a SmartLink.
Its materialized inverse is `Successor`. This allows immediate version topology
to use the same relationship descriptors, inverse-realization rules, storage
algebra, and query traversal mechanisms as the rest of the MAP graph.

---

## 5.6 Head

A **Head** is a version for which no known successor exists within the relevant knowledge context.

A lineage may have:

- one head
- multiple heads
- temporarily no locally resolvable head because of incomplete information or access constraints

Head status is derived.

It must not be treated as an intrinsic immutable property of a version.

Because MAP is distributed, head resolution may be knowledge-relative. One peer may know about a successor that another peer has not yet observed.

---

## 5.7 Branch

A **Branch** is a lineage path that diverges from another path after a common ancestor.

Branches may arise through:

- concurrent editing
- deliberate experimentation
- alternative proposals
- disconnected operation
- partial replication
- independent stewardship decisions

Branching does not itself imply a conflict.

---

## 5.8 Merge

A **Merge** is the creation of a new version that reconciles two or more lineage heads.

A merge version references every reconciled head as a predecessor.

A merge does not erase its source branches.

It extends the lineage with a new version that acknowledges all reconciled histories.

---

## 5.9 Merge Base

A **Merge Base** is the common ancestor used to determine what changed independently in each branch.

Merge-base selection is derived from the lineage graph.

It is not ordinarily required as permanent version metadata, although a merge process may preserve it as provenance.

---

## 5.10 Conflict

A **Conflict** is an incompatibility discovered while attempting to reconcile independent changes.

Multiple branches are not necessarily conflicting.

For example:

    Base:
        Name = Alice
        City = Boulder

    Branch A:
        Name = Alicia
        City = Boulder

    Branch B:
        Name = Alice
        City = Denver

These changes are independent and may be merged automatically.

By contrast:

    Base:
        City = Boulder

    Branch A:
        City = Denver

    Branch B:
        City = Chicago

requires arbitration unless the property descriptor defines a valid information-preserving merge operation.

---

## 5.11 Arbitration

**Arbitration** is an intentional choice among incompatible candidate outcomes.

Arbitration may be performed by:

- a person
- a stewarding body
- an authorized agent
- a declared policy
- a deterministic domain-specific rule

An automated policy does not make the original conflict cease to have existed.

Where provenance matters, the arbitration decision should record:

- the conflict
- the candidates
- the selected outcome
- the resolving agent or policy
- any rationale
- the resulting version

---

## 5.12 Knowledge Artifact

A **Knowledge Artifact** is a coherent, stewarded body of knowledge that may be composed from multiple versioned holons or subordinate knowledge artifacts.

Examples include:

- a schema
- an ontology
- a governance model
- a shared vocabulary
- a methodology
- a protocol
- a standard

A knowledge artifact may itself be used as a component of a larger artifact.

This produces a fractal composition pattern.

---

## 5.13 Stewardship Anchor

A **Stewardship Anchor** represents the enduring identity, purpose, and stewardship context of a knowledge artifact.

It answers:

> What continuing body of knowledge is this, and under whose stewardship does it evolve?

The stewardship anchor may identify:

- the artifact name
- its purpose
- its stewarding agents or spaces
- its governance process
- its development history
- its release history

The stewardship anchor is not necessarily the complete compositional state of the artifact.

A new component version should not automatically redefine the enduring identity of the artifact.

---

## 5.14 Working Composition

A **Working Composition** is a committed, immutable aggregate state that pins the exact versions of the components currently composing a knowledge artifact.

Its relationships to its components are definitional.

Changing any selected component produces a new working-composition version.

Example:

    Working Composition 27
        Includes Person Type v8
        Includes Organization Type v5
        Includes Membership Type v11

    Working Composition 28
        Includes Person Type v9
        Includes Organization Type v5
        Includes Membership Type v11

Working compositions preserve detailed development history.

They may proliferate as the artifact evolves and need not each receive a public release label.

---

## 5.15 Release

A **Release** is an intentional, steward-authorized designation of a specific published composition as an adoptable milestone.

A release pins one exact working-composition version or an equivalent exact set of component versions.

A release may include:

- a release label
- compatibility assertions
- computed impact classifications
- release notes
- migration guidance
- approval records
- stability status
- release channel
- deprecation information
- supersession relationships

A release is not created automatically merely because one or more components have changed.

---

## 5.16 Dependency

A **Dependency** is an explicit reliance by one holon or knowledge artifact on another version or release.

Dependencies may be:

- definitional
- operational
- advisory
- release-pinned
- version-range constrained
- governed by adoption policy

Dependency changes are pull-based.

A publisher may announce availability, but it does not rewrite the dependent.

---

## 5.17 Adoption

**Adoption** is the act of incorporating a selected version or release into a dependent holon or knowledge artifact.

Adoption produces a new dependent version.

Adoption may be:

- manually approved
- automatically staged
- automatically committed under prior authorization
- rejected
- deferred
- partially incorporated through mapping or migration

---

## 5.18 Mapping

A **Mapping** expresses correspondence between independently evolving knowledge representations.

Mappings support interoperability without requiring one representation to replace another.

Examples include:

- ontology concept equivalence
- vocabulary translation
- schema field correspondence
- governance-role correspondence
- compatibility adapters

Mappings may themselves be stewarded, versioned knowledge artifacts.

---

## 6. The Three-Level Change Model

KEA distinguishes three principal levels of change.

## 6.1 Staging

Staging occurs within a Nursery or equivalent transactional workspace.

During staging:

- properties may be added, changed, or removed
- relationships may be added, changed, or removed
- multiple holons may be edited together
- candidate states may be revised repeatedly
- changes may be abandoned
- validation may be performed incrementally

Staged changes do not individually create committed versions.

Multiple edits to the same holon may be consolidated into one successor version when committed.

Staging is fluid and reversible.

---

## 6.2 Publication

Publication occurs when staged changes are committed.

Commit:

- creates immutable holon versions
- persists `Create` or `Update` records from which runtime `VersionMetadata`
  can be derived
- establishes `Predecessor` / `Successor` SmartLinks
- persists the versions in the applicable HolonSpace
- makes the resulting versions referenceable according to access policy
- extends one or more lineages

Publication records that a state existed.

It does not necessarily assert that the state is stable, recommended, or suitable for adoption.

A stewarding body may publish many intermediate component and composition versions while debating or refining an artifact.

---

## 6.3 Release

Release occurs when a stewarding agent or body intentionally designates a published composition as an adoption point.

Release:

- selects an exact published composition
- records a governance decision
- provides a stable reference for dependents
- communicates compatibility and migration expectations
- may assign a semantic release label

Release is therefore distinct from commit.

Not every publication is a release.

Every release must refer to already published immutable state.

---

## 7. A More Detailed Evolution Pipeline

For composite knowledge artifacts, the full pipeline may be understood as:

    Nursery changes
        ↓
    Component commits
        ↓
    Working-composition commit
        ↓
    Steward review
        ↓
    Release designation
        ↓
    Publication of release metadata
        ↓
    Dependent assessment
        ↓
    Adoption
        ↓
    New dependent version

Component commits and working-composition commits may occur within one transaction, but they remain semantically distinct.

The component commit records fine-grained change.

The composition commit records the exact aggregate state.

The release records stewardship intent.

The adoption records a dependent's decision.

---

## 8. Version Lineage Architecture

## 8.1 Version DAG

Each logical holon evolves as a directed acyclic graph.

The graph supports:

- linear succession
- branching
- merging
- historical traversal
- head resolution
- common-ancestor resolution

The architecture must not assume a single total ordering of versions.

---

## 8.2 Lineage invariants

The Version Lineage Design Specification must define and enforce at least the following invariants:

1. Every committed version resolves to exactly one effective lineage identifier.
2. A root version has `lineage_id == None`, and its effective lineage identifier
   is its own `version_id`.
3. An update has `lineage_id == Some(root)`, where `root` identifies the
   lineage's root `Create` action.
4. Every predecessor has the same effective lineage identifier as the
   successor.
5. Predecessor references identify immediate parents.
6. The predecessor graph is acyclic.
7. A root version has no predecessors.
8. An ordinary successor has one predecessor.
9. A merge successor has two or more predecessors.
10. A committed version is immutable.
11. Head status is derived rather than stored as authoritative state.

---

## 8.3 Holochain integration

Holochain provides native update and action-chain structures, but those structures do not by themselves express the complete MAP version DAG.

MAP therefore defines its own lineage semantics above the Holochain storage substrate.

MAP adopts Holochain's list topology for lineage membership. When storage
decodes a saved holon's enclosing `Record`, it derives `VersionMetadata` from
the record's action. A `Create` yields `lineage_id == None`; an `Update` yields
`lineage_id == Some(root)` from `Update.original_action_address`. The enclosing
action's hash supplies `version_id` in both cases.

This metadata is part of the runtime representation of the saved holon, not
the persisted semantic content of its `HolonNode` entry. MAP therefore does
not model `LineageId` as a `PropertyType`, include it in descriptor-defined
equivalence, or expose it to ordinary property mutation.

Immediate ancestry is represented by the ordinary declared `Predecessor`
relationship. `Successor` is its materialized inverse, produced through the
normal inverse-relationship mechanism. A merge is represented by multiple
`Predecessor` occurrences on the merge version; no specialized
`AdditionalPredecessor` mechanism is required.

This is an intentional architectural choice in favor of a single persisted
graph-edge representation. Version topology reuses:

- relationship descriptors
- SmartLink encoding and storage
- inverse realization
- ordinary relationship expansion
- query traversal

Exact-version identity, lineage membership, and immediate ancestry remain
distinct facts:

- Runtime `VersionMetadata.version_id` establishes exact-version identity.
- Runtime `VersionMetadata.lineage_id`, derived from the enclosing action,
  establishes lineage membership together with `version_id` for a root.
- `Predecessor` is authoritative for immediate ancestry.
- `Successor` is the materialized inverse of `Predecessor` and is not an
  independently authoritative lineage fact.

`Predecessor` participates in ordinary MAP relationship commit processing. A
version publication relies on the general MAP commit contract to persist the
`HolonNode`, declared relationship occurrences, and required inverse
occurrences. KEA introduces no lineage-specific completion, retry, or recovery
protocol.

Except for the first update after a root, `Update.original_action_address`
normally differs from every immediate predecessor. Holochain update metadata
must not be interpreted as replacing MAP's multi-predecessor version graph.

---

## 9. Merge and Reconciliation Architecture

## 9.1 Three-way merge

Reconciliation compares:

- the common base
- the first candidate branch
- the second candidate branch

For more than two branches, the implementation may perform pairwise or multi-parent reconciliation while preserving all source heads as predecessors of the committed merge version.

---

## 9.2 Change classification

Relative to the merge base, each property or relationship member may be classified as:

- unchanged
- added
- removed
- modified
- independently changed to an equivalent result
- independently changed to different results
- removed on one branch and modified on another

---

## 9.3 Default property merge semantics

For a single-valued property, the conservative default is:

| Branch A | Branch B | Result |
|---|---|---|
| unchanged | unchanged | preserve base |
| changed | unchanged | accept A |
| unchanged | changed | accept B |
| changed to same value | changed to same value | accept shared value |
| changed differently | changed differently | conflict |
| removed | unchanged | remove |
| unchanged | removed | remove |
| removed | changed | conflict |
| changed | removed | conflict |

A `ValueDescriptor` may define more specialized merge semantics.

Examples may include:

- summing counter deltas
- set union
- observed-remove set behavior
- text-sequence reconciliation
- domain-specific state-transition arbitration

Such semantics must be explicit, deterministic, and appropriate to the value's meaning.

---

## 9.4 Relationship merge semantics

Relationship merge operates on the complete relationship state defined by the source version.

For independently added members, the default may be set union, subject to:

- cardinality
- duplicate policy
- target typing
- uniqueness
- relationship-property constraints
- cross-holon validation

Removal on one branch and no change on another ordinarily results in removal.

Removal on one branch and modification of the same member on another creates a conflict.

Two independently selected target versions may create a conflict unless descriptor-level semantics establish that one safely supersedes or reconciles the other.

---

## 9.5 Relationship member identity

Relationship merge must use the same member-identity semantics used for duplicate detection and collection behavior.

`OccurrenceId` has a limited and specific role.

It is introduced only when a relationship permits duplicate members. It distinguishes otherwise equivalent members within that duplicate-permitting relationship.

It is not a universal relationship identity.

For duplicate-permitting relationships:

    member identity = OccurrenceId

For duplicate-disallowing relationships:

    member identity = descriptor-defined equality or uniqueness semantics

The detailed relationship model must provide sufficient semantics to determine whether two relationship representations refer to the same set member.

---

## 9.6 Definitional relationships

Definitional relationships are part of the immutable definitional state of the source holon.

Changing a definitional relationship requires a new source version.

During merge, definitional relationships are reconciled as part of the complete source state.

The resulting merge version must satisfy all applicable descriptors and transaction-level invariants.

---

## 9.7 Materialized inverse SmartLinks

MAP may materialize direction-specific SmartLinks for both directions of a semantic relationship.

These are projections of one logical relationship fact, not independently authoritative facts.

Forward and inverse projections must not be reconciled independently.

For version lineage, `Predecessor` is the authoritative declared relationship
and `Successor` is its materialized inverse. Merge and reconciliation logic
reasons from `Predecessor` occurrences; it must not treat a separately observed
`Successor` projection as a competing lineage fact.

The merge process operates on the authoritative relationship state and then recreates or validates the required inverse projections.

---

## 9.8 Merge workspace

A merge begins in the Nursery.

A merge workflow conceptually performs:

    select candidate heads
    resolve merge base
    calculate branch-relative changes
    apply non-conflicting changes
    identify conflicts
    stage candidate merged state
    resolve conflicts
    validate complete result
    commit merge version

The merge candidate remains mutable until commit.

---

## 9.9 Merge provenance

A merge result must identify all reconciled predecessor heads.

Additional merge provenance may include:

- selected merge base
- generated change sets
- detected conflicts
- applied automatic rules
- arbitration decisions
- resolving agents
- rationale
- validation outcomes

Such provenance may be transient, persisted, or selectively disclosed according to the applicable design specification and governance policy.

---

## 10. CRDT and Convergence Position

KEA does not reject all CRDT techniques.

It distinguishes between two categories.

### 10.1 Information-preserving convergence

Some data types have operations that can be composed without losing relevant information.

Examples include:

- grow-only sets
- observed-remove sets
- append-only logs
- counters
- causally ordered event sets

These mechanisms may be used where their semantics match the domain.

### 10.2 Policy-based conflict suppression

Other strategies obtain one converged value by choosing among incompatible candidates.

Examples include:

- last-write-wins
- preferred-device-wins
- preferred-authority-wins
- timestamp ordering

These are arbitration policies.

They must not be described as intrinsically conflict-free when they discard or suppress meaningful alternatives.

KEA therefore adopts this rule:

> Automatic convergence is permitted only where the applicable descriptor or declared policy defines the semantic consequences of that convergence. Information-discarding selection remains an arbitration decision and should retain appropriate provenance.

---

## 11. Knowledge Artifact Composition

## 11.1 Separation of identity and composition

The enduring identity of a knowledge artifact is distinct from any one exact composition.

The stewardship anchor represents the continuing artifact.

A working composition represents one exact aggregate state.

A release represents the intentional designation of one such state.

This prevents low-level component changes from forcing the artifact's enduring identity object to serve simultaneously as:

- identity
- working state
- release
- release label
- governance decision

---

## 11.2 Definitional component relationships

A working composition's relationships to its included components are definitional.

Each relationship pins one exact component version or exact subordinate release.

Changing a selected component creates a new working-composition version.

---

## 11.3 Fractal composition

A component may itself be a composite knowledge artifact.

For example:

    Governance Model
        Includes Decision Process
        Includes Role Model
        Includes Meeting Protocol

    Decision Process
        Includes Proposal Model
        Includes Objection Model
        Includes Consent Test

Each composite artifact may have:

- its own stewardship anchor
- its own component lineages
- its own working compositions
- its own releases
- its own dependents

A higher-level release may pin exact releases or versions of subordinate artifacts without absorbing their identities or histories.

---

## 11.4 Development history and release history

A knowledge artifact has at least two related histories:

1. **Development history**  
   The detailed lineage of published component and working-composition versions.

2. **Release history**  
   The sparser sequence of steward-designated adoptable milestones.

These histories must not be conflated.

---

## 12. Release Architecture

## 12.1 Release requirements

A valid release must:

- refer to exact immutable published state
- identify the released knowledge artifact
- carry a release label or equivalent stable identifier
- identify the stewarding authority or approval basis
- preserve its composition permanently
- not be retroactively repointed to another composition

---

## 12.2 Release labels

A release label is a steward-assigned identifier for a release.

It may use semantic versioning, calendar versioning, named milestones, or another declared scheme.

Intermediate working-composition versions need not receive externally meaningful labels.

---

## 12.3 Computed impact versus assigned release number

The system may compute the minimum apparent impact of changes since a prior release.

For example:

- compatible correction
- compatible extension
- compatibility risk
- breaking change

This computation informs release governance.

It does not automatically create a release or dictate the final public label.

A steward may choose a larger increment than the computed minimum.

A steward must not claim a smaller compatibility impact than the actual change set supports without producing an explicit exception or revised compatibility analysis.

---

## 12.4 Release channels

A future design specification may define channels such as:

- experimental
- preview
- candidate
- stable
- long-term support
- deprecated

Channels express stewardship intent and expected adoption behavior.

They do not change the immutability of the underlying release.

---

## 13. Compatibility Architecture

## 13.1 Compatibility is multidimensional

Compatibility is not a single boolean.

Relevant directions may include:

- old data under a new schema
- new data under an old schema
- old consumers reading new data
- new consumers reading old data
- mappings between ontology versions
- migrations between governance-model releases
- higher-level artifacts consuming changed subordinate releases

---

## 13.2 Intrinsic and dependent-relative compatibility

KEA distinguishes:

1. **Intrinsic compatibility**  
   Analysis based on the changed artifact itself.

2. **Dependent-relative compatibility**  
   Analysis based on the requirements and commitments of a particular consumer.

A change may be intrinsically compatible yet break a consumer that relied on an undocumented behavior.

Conversely, a broadly breaking change may remain compatible with a particular dependent that does not use the affected feature.

---

## 13.3 Compatibility evidence

Compatibility assessments may include:

- structural diff
- descriptor diff
- validation results
- migration results
- tests
- steward assertions
- dependent-declared requirements
- machine-verifiable compatibility receipts

The detailed representation belongs in the Compatibility and Evolution Analysis Design Specification.

---

## 14. Dependency and Adoption Architecture

## 14.1 Explicit dependencies

Dependencies must be represented explicitly enough to determine:

- what is depended upon
- whether the dependency is version-pinned or release-pinned
- what compatibility range is acceptable
- what adoption policy applies
- whether migration is required

---

## 14.2 Pull-based adoption

When a dependency publishes a new release:

1. The release becomes discoverable.
2. Dependents may assess compatibility.
3. Adoption policy determines whether to ignore, notify, stage, or approve.
4. Any adoption changes are staged.
5. Validation and migration are performed.
6. A new dependent version is committed.

The publisher does not rewrite the dependent.

---

## 14.3 Adoption policies

A dependency may carry or reference an adoption policy such as:

- never adopt automatically
- notify on any new release
- automatically stage compatible patches
- automatically commit approved compatibility classes
- require explicit approval for minor changes
- prohibit automatic adoption of breaking changes
- follow only a named release channel

Any automatic policy acts under prior authorization from the dependent's steward.

---

## 14.4 Release dependency versus moving dependency

KEA favors exact dependencies in committed definitional state.

A committed dependent version should normally identify the exact version or release it uses.

A moving expression such as "latest compatible release" is a resolution policy used when creating a new dependent version, not an unstable pointer embedded in an immutable version.

---

## 14.5 Adoption provenance

An adopted dependent version may record:

- prior dependency version
- newly adopted version
- compatibility assessment
- migration applied
- policy or person authorizing adoption
- validation results

---

## 15. Semantic Sovereignty

KEA is founded on **semantic sovereignty**.

Semantic sovereignty means that each agent or agreement-based space retains authority over the knowledge representations it adopts.

A shared ontology does not erase local vocabularies.

A new schema release does not rewrite existing applications.

A revised governance model does not silently alter existing agreements.

Publication creates an opportunity to adopt.

Release creates a coordinated proposal for adoption.

Mapping creates interoperability.

Adoption creates a new locally authorized state.

This enables ontological commoning:

    My vocabulary
          ↘
        Shared ontology
          ↗
    Your vocabulary

All three may evolve independently.

The shared ontology is itself a stewarded knowledge artifact rather than a mandatory universal replacement.

---

## 16. Responsibility Boundaries

## 16.1 Nursery

The Nursery is responsible for:

- staging edits
- staging merge candidates
- applying change operations
- maintaining transaction-local state
- running incremental checks
- resolving conflicts
- validating the complete candidate state
- committing new versions atomically where required

---

## 16.2 Reference layer

The reference layer is responsible for:

- exposing saved holons with their runtime `VersionMetadata`
- interpreting `Predecessor` / `Successor` SmartLinks
- retrieving exact versions
- resolving lineage roots
- traversing predecessors and successors
- identifying candidate heads
- comparing complete states
- computing changes
- constructing merge candidates
- applying descriptor-defined merge semantics

---

## 16.3 Storage layer

The storage layer is responsible for:

- persisting immutable `HolonNode` entries without embedding runtime
  `VersionMetadata` in their semantic content
- deriving `version_id` and optional `lineage_id` from each enclosing
  Holochain `Record` when decoding a saved holon
- persisting `Predecessor` and `Successor` as ordinary SmartLinks
- retrieving exact versions and links
- returning plural results where multiple versions or heads exist
- avoiding implicit semantic version resolution

Storage must not silently choose a preferred head or latest version.

---

## 16.4 Query layer

The query layer is responsible for interpreting version graphs according to explicit policies, including:

- exact version
- all versions
- lineage
- current heads
- single preferred head
- historical state
- released compositions
- dependency-compatible releases

---

## 16.5 Validation architecture

Validation is responsible for ensuring that committed versions and merges satisfy:

- descriptor constraints
- lineage invariants
- relationship cardinalities
- uniqueness rules
- cross-property rules
- cross-holon transaction invariants
- release integrity
- dependency constraints where applicable

Lineage and merge validation must remain deterministic and bounded at the integrity layer.

Broader impact and migration analysis may occur in higher layers and produce verifiable receipts.

---

## 16.6 Stewardship governance

Stewardship governance is responsible for:

- deciding when development state is ready for release
- assigning release labels
- approving compatibility claims
- defining adoption expectations
- publishing migration guidance
- deprecating releases
- managing stewardship succession
- arbitrating contested evolution where required

---

## 17. Subordinate Design Specifications

KEA is an architectural framework.

Detailed normative behavior should be defined in subordinate specifications.

The initial specification family is expected to include:

### KEA-01 — Version Lineage Design Specification

Defines:

- lineage root
- runtime `VersionMetadata` and its derivation from Holochain records
- separation of version metadata from persisted `HolonNode` content
- `Predecessor` and `Successor` relationship semantics
- version DAG invariants
- branches
- heads
- ancestry
- merge-parent representation
- storage mapping
- lineage queries

### KEA-02 — Knowledge Artifact Composition Design Specification

Defines:

- knowledge artifacts
- stewardship anchors
- components
- working compositions
- nested composition
- exact component pinning
- development and release histories

### KEA-03 — Merge and Reconciliation Design Specification

Defines:

- merge-base selection
- change-set calculation
- property merging
- relationship merging
- duplicate-member handling
- conflicts
- arbitration
- merge provenance
- merge operations

### KEA-04 — Publication and Release Design Specification

Defines:

- staging
- commit
- publication
- release creation
- release labels
- release governance
- channels
- deprecation
- release provenance

### KEA-05 — Compatibility and Evolution Analysis Design Specification

Defines:

- change classification
- compatibility dimensions
- semantic-impact derivation
- migration analysis
- dependent-relative compatibility
- compatibility receipts

### KEA-06 — Dependency and Adoption Design Specification

Defines:

- dependency representation
- version and release pinning
- adoption policies
- pull workflows
- automated staging and adoption
- migration execution
- adoption provenance

### KEA-07 — Knowledge Mapping Design Specification

Defines:

- mappings between independently evolving artifacts
- mapping lineage
- mapping releases
- equivalence and correspondence assertions
- transformation rules
- ontological commoning workflows

The numbering and decomposition may evolve as the design matures.

---

## 18. Initial Architectural Decisions

KEA establishes the following initial decisions.

1. Holon versions form a DAG rather than a strictly linear chain.
2. Every version resolves to one effective lineage identifier.
3. The lineage root is the first version, not a separate lineage holon.
4. A saved holon's runtime representation includes `VersionMetadata` derived
   from its enclosing Holochain `Record`.
5. `VersionMetadata` is not persisted in `HolonNode`, does not participate in
   definitional equivalence, and is not mutable through property operations.
6. A root has `lineage_id == None`; an update has
   `lineage_id == Some(root)`; effective lineage identity is
   `lineage_id.unwrap_or(version_id)`.
7. A version may have zero, one, or many immediate predecessors.
8. MAP uses `Update.original_action_address` as a lineage-root pointer, not as
   an immediate-predecessor pointer.
9. Immediate version ancestry is represented by ordinary `Predecessor`
   SmartLinks, with `Successor` as the materialized inverse.
10. Concurrent commits create multiple heads and do not overwrite one another.
11. Multiple heads are valid until reconciled or otherwise governed.
12. Merge uses common-ancestor comparison.
13. Independent changes may be composed automatically.
14. Incompatible changes remain explicit until arbitrated.
15. Automatic convergence is used only under declared semantic rules.
16. Every committed merge identifies all reconciled heads as predecessors.
17. Committed versions contain complete definitional state.
18. Definitional relationships participate in source-version merging.
19. Materialized inverse SmartLinks are projections and are not independently reconciled.
20. `OccurrenceId` is used only to distinguish members where duplicates are allowed.
21. Duplicate-disallowing relationships use descriptor-defined member equality.
22. Head status, latest status, and merge base are derived.
23. Staging, publication, and release are distinct lifecycle stages.
24. A release pins exact immutable composition.
25. Release designation is a stewardship decision.
26. Semantic release labels apply to releases, not every internal composition version.
27. Dependencies are adopted through pull.
28. Adoption always creates a new dependent version.
29. Independently stewarded knowledge artifacts may coexist indefinitely.
30. Interoperability may be achieved through versioned mappings rather than forced convergence.

---

## 19. Open Architectural Questions

The following questions remain for subordinate design work:

1. How should storage validate record-derived `VersionMetadata`, including root
   `Create` identity and the `Update.original_action_address` root-pointer
   invariant?
2. What common-ancestor algorithm should be used for complex DAGs with multiple best merge bases?
3. Should change sets be persisted, derived on demand, or both?
4. Which merge records are transient, and which should be preserved as durable provenance?
5. How are relationship members identified when duplicates are disallowed but targets may advance across versions?
6. Which merge semantics belong on `ValueDescriptor`, `PropertyDescriptor`, and `RelationshipDescriptor`?
7. How are cross-holon merge conflicts represented?
8. How are incompatible descriptor changes classified and migrated?
9. What exact relationship exists between a stewardship anchor and its working-composition lineage?
10. Should a release pin one working composition or directly pin every component?
11. How are releases of nested artifacts incorporated into higher-level compositions?
12. Which release-governance mechanisms belong in core MAP schemas versus domain-specific schemas?
13. How are compatibility receipts represented and validated?
14. How are adoption policies authorized and constrained?
15. How should private, shared, and public development histories differ?
16. How are abandoned branches, rejected proposals, and superseded releases represented without deleting history?
17. How are redaction, privacy, and legal erasure requirements reconciled with immutable lineage?
18. How should mappings evolve when either mapped artifact branches or releases a new version?

---

## 20. Architectural Summary

MAP treats knowledge evolution as the controlled extension of immutable semantic lineages.

At the individual-holon level:

- staged edits become immutable versions
- concurrent versions produce branches
- independent changes may merge automatically
- incompatible changes remain explicit conflicts
- reconciliation creates multi-predecessor merge versions

At the composite-artifact level:

- component versions are pinned into exact working compositions
- development may produce many published intermediate compositions
- stewards intentionally designate selected compositions as releases
- releases provide coherent adoption points

At the ecosystem level:

- publishers offer releases
- dependents assess and pull them
- adoption produces new dependent versions
- independently governed representations may continue to coexist
- mappings support interoperability without forced replacement

The resulting architecture combines:

- immutable history
- local-first development
- semantic merge
- explicit conflict handling
- compositional release management
- pull-based dependency adoption
- stewarded governance
- semantic sovereignty

KEA therefore provides a general architecture for evolving knowledge without requiring either centralized control or information-destroying convergence.
