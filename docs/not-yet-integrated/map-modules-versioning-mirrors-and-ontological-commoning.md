# MAP Modules, Version Binding, Mirror Holons, and Ontological Commoning

## Purpose and starting point

This inquiry began with a possible refactoring of MAP's schema definitions and TDL source files around **Module boundaries**. It revealed a broader architectural role for Modules: they are semantic units of composition, release, dependency resolution, and coarse-grained version acceptance. That role extends naturally to Mirror Holons and cross-Space references, but the two kinds of boundaries must not be conflated.

The following captures the resulting model, its consequences, and the decisions that remain open. It distinguishes emerging principles from implementation choices that have not yet been settled.

## 1. Modules are semantic boundaries, not files

A **Module** groups semantically cohesive holons. Modules are not restricted to type descriptors or schemas: they may organize any kinds of holons. A Schema can contain multiple Modules, and the containment hierarchy for schema definitions is **Space → Schema → Module → member types**. Membership is contained; references and dependencies can cross Module boundaries.

A TDL file may conveniently express a Module or a cohesive part of one, but **file boundaries and loading order must not define Module semantics**. Refactoring TDL should group related definitions according to conceptual cohesion, not simply according to parser or bootstrap convenience. Shared reusable ValueTypes, PropertyTypes, rules, and constraints should not automatically be absorbed into each consuming HolonType's Module.

The loader should honor semantic dependencies independently of how source files are arranged. A refactor should preserve the meaning of the compiled descriptor graph unless semantic changes are explicitly intended.

## 2. Two scales of versioning, one manageable acceptance decision

MAP already supports immutable holon versions and relationship bindings to either a **specific version** or a **lineage**. Module versioning builds on—not replaces—those semantics.

- **Holon versions** remain the fine-grained units of state evolution.
- **Module versions/releases** identify coherent configurations of member holon versions, their relationship bindings, and the dependencies accepted by that Module.
- **Module bindings** allow consumers to accept a whole coherent configuration rather than manually rebinding every referenced holon.

A Module release is therefore a **unit of coherent acceptance**, not merely a list of changed holons. When Module A accepts Module B's release, A implicitly accepts the holon-level bindings embodied in that release. B's steward decides what configuration constitutes a coherent release; A decides whether and when to adopt it.

This reduces the cognitive and error burden of fine-grained rebinding while preserving MAP's pull-based sovereignty. A release manifest or equivalent immutable resolution record may suffice; the model does **not** require copying the entire relationship graph into every release.

### Binding policies and semantic versions

Policies could automate some acceptance decisions—for example, permitting compatible patch-level releases while requiring review of minor or major changes. Such policies should operate on Module-level semantic compatibility, not simply the number of changed holons. An automatic policy **authorizes an explicit, recorded pull/acceptance transition**; it must not make an Agent's accepted graph change merely because a producer publishes a release.

Version selection, compatibility policy, and the recorded resolved version are distinct concepts.

## 3. Contextual dependency resolution is essential

Consider:

```text
Module A
  ├── direct dependency → Module C @ 1.6
  └── dependency → Module B @ 2.4
                          └── dependency → Module C @ 1.7
```

Accepting B@2.4 **does not silently rebind A's independent direct dependency on C@1.6**. B's accepted dependency on C@1.7 remains valid within B's own resolution context. The same Module lineage—and even the same holon lineage—can consequently be encountered through different accepted contexts.

This is **contextual resolution**, not globally unified dependency resolution. Immutable versions make coexistence possible, but coexistence does not itself prove semantic interoperability. When independently resolved contexts interact, their meanings and contracts must be reconciled explicitly rather than assumed equivalent.

This also means a reference or Mirror cannot be resolved or deduplicated by target holon lineage alone: its **resolution context** matters.

### Transitive acceptance

Accepting B includes the coherent configuration and transitive dependencies that B has accepted **within B's context**. It does not automatically alter A's other dependency bindings. A Space likewise need not impose one globally unified version of every dependency across all its Modules.

## 4. Dependency bookkeeping should follow the actual reference graph

Maintaining independent dependency inventories alongside cross-boundary references risks divergence. The emerging direction is to make dependencies **intrinsic to the references that cross boundaries**, so Module and Space dependencies can be discovered from the graph itself.

A Mirror Holon—or a shared dependency context reached through Mirror Holons—can identify the target and the relevant boundary. Multiple holon Mirrors might share one Module-level accepted binding, avoiding repeated independent decisions.

The representation remains open: a shared `ModuleDependency` holon, a Module Mirror, or another dependency-bearing reference structure could implement this. The essential invariant is **dependency discovery and binding coherence**, not a mandatory additional object or hop for every reference.

## 5. Mirror Holons mediate two importantly different boundaries

Both kinds of Mirror provide locally stewarded reference endpoints, help preserve local graph coherence, and make cross-boundary dependencies discoverable. Their responsibilities differ substantially.

| Concern | Intra-Space, inter-Module Mirror | Inter-Space Mirror |
|---|---|---|
| Boundary | Independently versioned Modules in one Space | Independent Space/Agent membranes |
| Main mediation | Accepted Module release and holon binding context | Agreement-governed visibility, access, and acceptance |
| Authority | Common Home Space authority | Separate Home Space authorities |
| TrustChannel | Not inherently needed | Required for the inter-Space interaction |
| Target dependency | Known target Module and holon | Externally meaningful identity and TrustChannel/shared contract; remote internal Modules need not be exposed |
| Local inverse | Can preserve a local relationship view without forcing another Module's release to change | Memoizes a unilateral local assertion; does not imply remote acknowledgment |
| Semantic interpretation | Local Module/descriptor context | Authorized projection in the shared Agreement ontology |

A cross-Space Mirror should not reveal B's internal Module structure, descriptor versions, or unrelated state merely because A can reference an externally visible holon. **The TrustChannel and shared contract define the external dependency boundary**, rather than an entitlement to inspect the remote implementation.

### Inverses and memoization

MAP relationships have inverse semantics, but eager inverse materialization can inadvertently modify an independently versioned Module, and cross-Space propagation cannot be assumed to be authorized or possible.

A local inverse attached to a Mirror is therefore best understood as **memoization of a local relationship assertion** for graph coherence and possible later agreement-governed binding. It is **not** evidence that the remote Home Space has received, accepted, or incorporated the assertion. Some assertions may remain unilateral indefinitely.

This distinguishes local assertion, possible communication, and remote acceptance. The precise storage and reconciliation mechanics remain design questions.

## 6. Ontological commoning resolves inter-Agent semantic interoperability

MAP interactions between Agents occur within a **We-Space**, with each participating sub-agent connected through a **TrustChannel**. A TrustChannel is governed by a multilateral **Agreement** or a unilateral **Declared External Commitment (DEC)**, which establishes the relevant **Information Access Agreement (IAA)** for the Agent's role. The IAA governs what information may be accessed and the responsibilities for safeguarding it.

The Agreement needs a vocabulary in which to express permissions, obligations, and exchanged information. **Ontological commoning** permits that shared vocabulary to differ from each participant's native ontology. Each Agent maps between its own ontology and the agreed shared ontology.

Therefore:

- Agent A may use descriptor versions different from those used by Agent B.
- Neither Agent must accept the other's native descriptor versions or internal Module dependencies merely to interact.
- Both must be able to interpret their interaction through the **shared Agreement ontology** and honor the IAA.
- Semantic compatibility is established at the shared boundary, not by globally synchronizing native ontologies.

The shared vocabulary may also express assurances or claims relevant to the Agreement, without requiring disclosure of the evidence or private internal definitions behind those claims.

Ontological mappings and shared ontologies can themselves evolve and should have explicit version/compatibility semantics. Whether mappings are implemented as reusable versioned Modules referenced by TrustChannels remains an open design choice.

## 7. Membrane opacity and observable versions

**An Agent must not gain knowledge of what happens inside another Agent's membrane merely because it has an authorized reference.** An inter-Space Mirror represents the **authorized observable projection** of a remote holon under the IAA and shared ontology—not a transparent copy of its native state.

If B changes a holon's internal properties, relationships, descriptor, or Module bindings, but the change does not alter what A is authorized to observe, **A has no new observable version of that holon**. A need not know that B changed anything.

If the authorized projection does change, A may have a new representation available to accept, but its accepted Mirror does not automatically advance. The Mirror's accepted history can thus differ from B's internal version history and from the observable histories of other Agents with different IAAs.

This yields three separate controls:

1. **B** controls its authoritative state and the information it warrants and exposes.
2. **The Agreement/DEC and IAA**, expressed in a shared ontology, constrain what crosses the membrane.
3. **A** controls when to accept changes to its authorized representation.

The relevant comparison is between authorized projections, including visible properties **and relationships**, not between B's private version identifiers. A change in the IAA or shared ontology can also alter the projection without a corresponding change to B's native holon.

## 8. Home Space recognition, external warranty, and trust

Every holon has **exactly one Home Space**, which is authoritative for its state and versions. MAP's validation architecture distinguishes:

| Layer | What it establishes | Responsibility |
|---|---|---|
| **Holochain peer validation / PVL** | Structural and cryptographic invariants expressible in the restricted Peer Validation Language | DHT peers |
| **Descriptor-aware recognition** | Whether a new locally homed holon or link version satisfies the applicable MAP descriptors, constraints, and validation rules | Sub-agents within the Home Space |
| **TrustChannel verification** | Whether information crossing a membrane is authorized, properly interpreted, and conforms to the shared Agreement/IAA contract | Participating boundary mechanisms |

PVL is **not descriptor-aware**. DHT commit and replication alone therefore cannot enforce MAP's full descriptor-defined constraints. A separate **recognition step** is required before a replicated version is recognized as valid within its Home Space.

An external recipient often cannot validate a remote holon against its native descriptor: the IAA may conceal required properties or relationships. More fundamentally, **that is not the receiving Space's responsibility**. The Home Space's Agent **warrants** the validity of information it shares. The recipient evaluates authorization, shared-contract conformance, and whether to trust and accept the representation—not the hidden completeness of the remote holon.

A warranty is an accountable assertion, not an infallible proof. The Agreement and trust relationship determine how inaccurate or breached warranties are handled.

A locally homed Mirror must still satisfy **its own** local descriptor and recognition requirements. That does **not** turn its Space into the validator of the represented remote holon's native type.

Likewise, A can recognize its own relationship assertion to a Mirror without B recognizing that relationship. **Local validity does not imply bilateral acknowledgment.**

## 9. Consequences for the original schema/TDL refactor

The architectural rationale for Module-oriented source organization is now stronger, but implementation should proceed from the semantic model rather than force the model to match current files.

1. Identify **cohesive semantic Modules** across the schema, recognizing that Modules may also group non-descriptor holons.
2. Make **Module membership and cross-Module references** explicit and inspectable; preserve the Space → Schema → Module containment rule for schema definitions.
3. Define an immutable **Module release configuration** and its accepted dependency context, without assuming that full graph duplication is required.
4. Preserve existing holon **specific-version versus lineage** binding semantics within that context.
5. Support **coarse-grained Module acceptance** and policy-driven rebinding as recorded pull operations.
6. Derive dependencies from **actual boundary-crossing references** rather than separately maintained lists.
7. Distinguish **inter-Module Mirrors** (version mediation) from **inter-Space Mirrors** (TrustChannel-mediated observable projections).
8. Keep remote native ontologies, descriptors, Module internals, and private version changes **behind the membrane**.
9. Keep **recognition responsibility with each holon's Home Space**; enforce the shared contract at inter-Space boundaries.
10. Refactor TDL files for semantic cohesion while keeping **loading mechanics independent** and checking that the compiled graph remains equivalent.

## 10. Questions still requiring design decisions

These are not settled merely by adopting the principles above:

- **Module release representation:** manifest of member versions and resolved bindings, graph snapshot, or another immutable structure; how to define release atomicity and validation.
- **Dependency/Mirror representation:** direct references, shared `ModuleDependency` contexts, Module Mirrors, or combinations; ownership, identity, and deduplication rules.
- **Cross-Module inverse semantics:** when to materialize local inverses, when to memoize, and how acceptance changes affect them without silently changing another Module release.
- **Removal or migration:** what happens when a newly accepted Module release omits, replaces, or incompatibly changes a referenced holon.
- **Compatibility checking:** how Module-level semantic-version promises are defined and checked, especially where independently resolved contexts interact.
- **Inter-Space projection identity:** how externally meaningful identities, authorized projection versions, mapping changes, and Mirror acceptance are represented without leaking remote internal versions.
- **TrustChannel mapping architecture:** how reusable ontological mappings are packaged, versioned, validated, and selected for a given Agreement/DEC.
- **Recognition governance:** how sub-agents record and reconcile descriptor-aware recognition outcomes within a Home Space.

## Core synthesis

**Holons evolve individually; Modules publish coherent, contextually resolved configurations; consumers accept Module releases at a human-manageable granularity.**

**Mirror Holons preserve local reference coherence across independently evolving boundaries, but an inter-Space Mirror is an Agreement-governed observable projection, not a window into the remote Agent's native graph.**

**Ontological commoning allows Agents with independent ontologies and version histories to interact through a shared Agreement vocabulary.**

**The Home Space recognizes and warrants its holons; other Spaces verify the shared contract and decide what to accept, without inheriting responsibility for—or visibility into—the remote Space's internal validation.**
