# MAP Modules Architecture — Reconciliation of the Working Design and Subsequent Inquiry

**Status:** Reconciled working architecture; explicit unresolved decisions remain.  
**Sources:** `module-arch.md` (earlier working design) and `map-modules-versioning-mirrors-and-ontological-commoning.md` (subsequent architectural synthesis).  
**Purpose:** Preserve the earlier document's release/publication lifecycle and implementation constraints while incorporating contextual dependency resolution, Mirror distinctions, ontological commoning, membrane opacity, and Home Space recognition. This is not a claim that the implementation already conforms.

## 1. What the earlier design established

The earlier design remains foundational on several points:

1. A **Module** is a sub-Space unit of coordinated development, release, publication, dependency management, and adoption—not a Space, Agent, namespace, or merely an arbitrary collection.
2. **Commit is not release.** A Module Workspace may contain durable, committed but unreleased holon versions; intermediate versions must not become externally published through inverse side effects.
3. A **Module Release** is an immutable, validated, deterministically resolved configuration of member HolonVersions and dependency bindings. A manifest/release package expresses its closure without requiring physical copies of externally homed holons.
4. **Publication is not adoption.** Stewardship Anchors/release lineage support successor discovery, while consumers retain control over adopting a successor. Adoption produces new local versioned state rather than mutating existing released state.
5. **Packaging does not change intrinsic holon identity.** Module membership belongs primarily to the containing release; ordinary relationship identifiers and syntax need not be module-qualified. A HolonVersion's inclusion in a release need not re-version the holon.
6. Boundary-crossing inverse *visibility* must be governed by release/publication rather than unconditional holon commit. Historical, released-head, and locally adopted inverse views are different projections.
7. Release publication should be semantically atomic, validated, idempotent, and recoverable even when storage operations are not atomic. Workspace representation, nesting, exports, and release branching remain open.

The newer inquiry **extends** these principles; it does not replace the commit/workspace/release/publication/adoption lifecycle.

## 2. Revised core model

### 2.1 Semantic Modules, independent of files

A Module groups holons into a semantically cohesive body that can evolve privately and release coherently. Modules apply to arbitrary holons, not only schema descriptors. TDL files and loader passes are representations and mechanisms, not Module boundaries. Reorganizing the Core Schema TDL should follow semantic cohesion while preserving the compiled graph unless a separate semantic change is approved.

For schema definitions, preserve **Space → Schema → Module → member types** as the working containment model. The earlier document's generic **AgentSpace → Module → Holon** and possible *nested Modules* are not necessarily contradictory: they describe a more general packaging model. However, whether a Schema is always an obligatory intermediate container for a Module, and whether nested Modules are legal within schema containment, **must be specified rather than inferred**. Do not silently implement either tree as universal.

A Module is not a new Home Space or authority membrane. Holons retain exactly one Home Space. Module membership should not be embedded in holon identity or ordinary relationship syntax. Whether membership is exclusive, and how generic Modules outside schema definitions are contained, remain open.

### 2.2 Two levels of versioning

- **HolonVersion:** immutable fine-grained state.
- **Relationship binding:** retains the existing distinction between a specific version and a lineage.
- **Module Workspace:** mutable/durable unpublished configuration.
- **Module Release:** immutable validated configuration identifying exact member versions and effective resolved dependencies.
- **Module binding:** the consumer's accepted release (or a policy used to choose a successor).
- **Stewardship Anchor/release lineage:** enduring discovery channel for published successors, not a mutable binding that changes existing releases.

The key advance is **coarse-grained acceptance**: accepting B's release means accepting the constituent holon versions and dependency configuration B released, rather than rebinding each constituent separately. Semantic-version compatibility policies may authorize automatic acceptance, but the result is still an explicit, recorded adoption transition. Human-readable SemVer labels are optional; deterministic release identity is essential.

**Determinism versus lineage:** The earlier rule against mutable `latest` in released graphs is retained. A lineage-bound relationship may retain its lineage *intent*, but its effective resolution **within a particular immutable release context** must be reproducible. An adopted successor creates new local versioned/released state; it does not retroactively change an old release. Exact version pins that conflict with a Module release's included versions require an explicit resolution rule; do not silently reinterpret them.

### 2.3 Contextual dependency resolution

```
Module A @ R3
  |-- direct dependency: C @ R1
  `-- dependency: B @ R4
                         `-- dependency: C @ R2
```

A's adoption of B@R4 accepts B's dependency on C@R2 **within B's context**; it does not change A's independent binding to C@R1. Multiple versions of a Module or holon lineage may coexist in a larger Space. This is a deliberate alternative to global dependency unification.

Coexistence does not guarantee semantic compatibility. When data interpreted in different contexts interacts, a contract, mapping, or validation rule must establish the required compatibility. Resolution context is therefore part of reference interpretation, even when it is not encoded in ordinary holon identity or relationship syntax.

**Transitive closure** is a deterministic closure of *bindings in their respective contexts*, not a command to flatten every dependency lineage into one Space-wide version.

## 3. References, dependencies, and Mirrors

### 3.1 Preserve direct references; derive dependency context

The earlier design explicitly protects ordinary direct references (`X@v4 → Y@v2`) and warns against rewriting them into `Module::Y` or changing holon identity when packaging changes. The newer inquiry insists that dependencies be discoverable from the *actual cross-boundary reference graph*, rather than maintained in parallel lists.

These requirements can coexist if **semantic target identity remains independent of dependency-resolution metadata**. A reference can retain its direct semantic target while its resolution/publication context is discovered or represented through a dependency-bearing Mirror or shared binding context.

**Not yet settled:** whether *every* cross-Module reference must route physically through a Mirror/ModuleDependency. That stronger requirement could contradict the earlier direct-reference principle and create packaging-induced reference churn. Treat mandatory indirection as a design candidate, not an established invariant. An explicit Module-export reference remains a distinct optional feature.

### 3.2 Two Mirror roles

| Dimension | Same Space, different Modules | Different Spaces |
|---|---|---|
| Boundary | Versioned publication/acceptance context | Authority and information membrane, plus version acceptance |
| Target knowledge | Native holon/Module may be known | Only externally authorized identity and semantics need be known |
| Mediation | Accepted Module release and contextual holon resolution | TrustChannel, Agreement/DEC, IAA, shared ontology, observable projection |
| Inverse | Local memoization avoids forcing target Module release changes | Local unilateral assertion; not remote acknowledgment |
| Validation | Shared Home Space recognizes authoritative holons | Remote Home Space recognizes authoritative holon; receiver validates its Mirror and shared contract |

Both may provide local relationship endpoints and dependency discovery, but **do not assume they must be one concrete HolonType**. A shared Module dependency context may support several Mirrors; whether to materialize a Mirror for each reference is open.

An inter-Space Mirror should **not require disclosure of the remote native Module, descriptor lineage, or internal version history**. The external dependency may be on a TrustChannel and shared semantic contract rather than on a remote internal Module. This is a substantive refinement of the earlier sketch in which a foreign reference could directly resolve a remote `HolonVersion`.

### 3.3 Relationship assertions, inverses, and release gates

Distinguish:

1. **Local commit:** persist a working assertion in its Home Space; do not expose unreleased intermediate versions across publication boundaries.
2. **Module release:** validate and establish the immutable published assertion set. This is the earliest point at which a cross-boundary assertion becomes eligible for publication.
3. **External communication:** transmit or expose an authorized assertion or projection, if the governing TrustChannel/IAA permits it.
4. **Remote acknowledgment/recognition:** optional and separately governed; it does not follow from an inverse being locally memoized.
5. **Consumer adoption:** separately accept an offered successor or observable projection into new local versioned state.

The earlier document's phrase **"publish inverses at release" must be read as "make eligible released assertions and their authorized derived inverse views available"**, **not** as an instruction to write inverse links into a foreign authoritative holon or to assume remote acknowledgment. Release is necessary but not sufficient for inter-Space disclosure: TrustChannel authority and the IAA also apply.

Historical, released-head, and adopted views must remain distinguishable. Successor availability belongs to release lineage/Stewardship Anchors, not to domain inverse semantics.

## 4. Ontological commoning and membrane opacity

Inter-Agent interactions take place within a **We-Space**. Each participating sub-agent has a TrustChannel into that We-Space, governed by a multilateral Agreement or unilateral Declared External Commitment (DEC). The applicable Information Access Agreement (IAA) specifies accessible information and safeguarding responsibilities according to the participant's role.

**Ontological commoning** provides a shared Agreement vocabulary to which each Agent maps its native ontology. Agent A and Agent B need not share native descriptor versions, Module releases, or internal dependency graphs to interact. The shared ontology is the interoperability contract; native ontologies remain sovereign.

Consequently, an inter-Space Mirror is best understood as **A's accepted authorized projection of B's externally shared information**, not a replica of B's native holon. It may expose only a subset of properties and relationships, expressed in the shared vocabulary. Different participants can have different projections and observable version histories under different IAAs.

If B changes an internal holon version but the authorized projection to A is unchanged, **A has no new observable version to accept and should not learn of the private change merely through the reference**. A new authorized projection can become available without automatically replacing A's accepted Mirror. Changes to the IAA or shared ontology may also change the projection.

The older document's release discovery and update-candidate machinery remains applicable, but **cross-Space candidates must be described in terms of authorized observable changes**, not necessarily B's private native version identifiers. Release notifications themselves must respect membrane opacity.

## 5. Validation, recognition, warranty, and acceptance

A holon has exactly one authoritative Home Space. Holochain DHT peer validation, constrained by MAP's Peer Validation Language (PVL), is **not descriptor-aware** and cannot enforce the full descriptor-defined semantic rules. A separate **recognition** step is required within the Home Space for newly committed/replicated holon and link versions.

| Stage | Meaning | Responsible party |
|---|---|---|
| DHT peer validation | PVL-expressible structural/cryptographic integrity | Validating DHT peers |
| Home Space recognition | Descriptor-aware validity of authoritative holon/link versions | Home Space sub-agents |
| Module release validation | Coherence, membership, binding determinism, publishability of the proposed release | Releasing Space |
| Cross-Space warranty | Assertion that shared information is valid and properly offered under the Agreement/DEC | Originating Agent |
| TrustChannel verification | Authorization and conformity of disclosed information to IAA/shared ontology | Boundary mechanisms |
| Local acceptance | Decision to incorporate an authorized representation or newer release | Receiving Agent/Module |

These are **not interchangeable validations**. The receiving Space cannot necessarily see a required native property, and is not responsible for revalidating a remotely homed holon against its native descriptor. It does recognize its own locally homed Mirror as a Mirror and checks the authorized projection against the shared contract. Warranty is accountable trust, not absolute proof.

Release validation in the earlier document therefore needs two qualifications: (a) it does not replace the Home Space's descriptor-aware recognition; and (b) a cross-Space release must not presume it can inspect or validate hidden native remote state. It validates its own released state and the contractually visible external dependencies.

## 6. Reconciled lifecycle

```
LOCAL AUTHORITATIVE SPACE
  edit / stage
      -> local commit (DHT peer validation)
      -> descriptor-aware recognition
      -> durable Module Workspace (not externally published)
      -> Module release validation
      -> immutable Module Release + manifest / exact contextual bindings
      -> release activation / publication eligibility
      -> Stewardship Anchor successor availability

SAME-SPACE CONSUMING MODULE
  discover released successor
      -> assess candidate under policy
      -> rebind accepted Module context in local working state
      -> validate and release new consuming Module version

CROSS-SPACE PARTICIPANT
  authorized TrustChannel / Agreement or DEC / IAA
      -> map to shared ontology and enforce disclosure contract
      -> expose authorized projection (not native internal graph)
      -> consumer detects meaningful observable successor
      -> consumer verifies shared contract and chooses acceptance
      -> locally recognized Mirror / new local accepted state

RELATIONSHIP INVERSES
  local memoization may preserve graph coherence
      != remote communication
      != remote recognition
      != adoption
```

The exact ordering and coordination of recognition, workspace persistence, release validation, and publication activation must be reconciled with current runtime behavior. The diagram specifies responsibilities, not a final implementation call graph.

## 7. Design tensions requiring explicit decisions

| ID | Tension | Reconciled position / open question |
|---|---|---|
| D1 | `AgentSpace → Module` versus `Space → Schema → Module` | Schema containment is explicit for schema types; generic Module containment and optional nesting need a unified rule. |
| D2 | Semantic cohesion versus release cohesion | Modules should group semantically cohesive holons *and* serve coordinated release boundaries; neither source-file layout nor domain taxonomy alone defines membership. |
| D3 | Direct references versus mandatory Mirror routing | Preserve stable target identity and ordinary relationship syntax. Whether a physical Mirror is required for each boundary-crossing reference remains open. |
| D4 | Deterministic release versus lineage binding | Retain lineage intent but record reproducible effective bindings for each immutable release. Define how explicit pins interact with Module releases. |
| D5 | Transitive acceptance versus global unification | Accept B's resolved dependency context without modifying A's independent dependencies. Compatibility at points of interaction is separate. |
| D6 | Release-time inverse publication versus remote autonomy | Release gates eligibility; external IAA governs disclosure; inverse views do not mutate foreign authoritative holons or imply acknowledgment. |
| D7 | Stewardship Anchor discovery versus membrane opacity | External successor discovery may expose only authorized projection changes, not remote native releases/versions. |
| D8 | Native validation versus shared-contract verification | Home Space recognizes native holons; recipient validates local Mirror and shared representation, relying on remote warranty. |
| D9 | Release membership versus holon identity | Membership belongs to release, not intrinsic holon identity. Exclusive membership, aggregate releases, and nesting remain open. |
| D10 | Semantic versions and automated policies | Optional labels and policies; adoption must yield recorded local state. Compatibility criteria and migration/removal behavior remain open. |
| D11 | Projection identity and versioning | Define stable external identity, observational equivalence (visible properties and relationships), mapping/IAA changes, and acceptance histories without exposing private native IDs. |
| D12 | Release publication atomicity | Retain earlier requirements for validation, idempotency, staging/activation, recovery, and historical/current/adopted query views. |

## 8. Implementation implications and sequencing

**First, retain the earlier minimal Module vertical slice**, subject to its stronger cross-boundary interpretation:

1. Introduce a minimal Module identity and membership/release context without changing ordinary holon identities.
2. Distinguish committed/unreleased working versions from released versions.
3. Produce immutable Module Releases with exact member versions and reproducible contextual dependency bindings.
4. Gate cross-Module and cross-Space *publication eligibility* on release; prevent unreleased inverse leakage.
5. Keep external inverse views non-authoritative; do not assume a release can directly publish into another Home Space.
6. Support Stewardship Anchor successor discovery, recorded pull-based adoption, and historical/released-head/adopted views.
7. Test release atomicity, idempotency, recovery, and the absence of intermediate-version leakage.

**Then specify and implement the dependency-resolution layer**: contextual resolution, shared Module bindings, holon pin/lineage interaction, optional Mirror materialization, and compatibility/removal cases. Avoid forcing Module-qualified identity or universal physical indirection before those semantics are tested.

**Treat the cross-Space projection/TrustChannel layer as a distinct integration track**: Agreement/DEC/IAA vocabulary, mapping, authorization, projection identity, membrane opacity, remote warranty, and local Mirror recognition. The Module vertical slice should not falsely claim these are already implemented.

**Finally, reorganize schema TDL by cohesive Modules** once the semantic membership and dependency rules are stable. Use graph-equivalence checks against the current compiled Core Schema and keep loader staging/ordering independent of the chosen Module boundaries.

## 9. Reconciled invariants

1. **Single Home Space:** Packaging never changes a holon's authoritative Home Space.
2. **Commit ≠ recognition ≠ release ≠ publication ≠ adoption:** Each has distinct semantics and authority.
3. **Deterministic releases:** Every immutable Module Release reproducibly identifies exact effective versions and dependency bindings, even where source relationships express lineage intent.
4. **Contextual acceptance:** A consumer accepts a Module's coherent configuration without globally rebinding other independent dependency contexts.
5. **Identity neutrality:** Ordinary holon identity and relationship syntax are not rewritten merely because packaging changes.
6. **No intermediate leakage:** Unreleased working versions do not cross Module publication boundaries through inverse side effects.
7. **Non-authoritative inverse:** A locally memoized or externally discoverable inverse is not proof of remote re-authoring or acknowledgment.
8. **Agreement-governed membrane:** Cross-Space visibility is limited to authorized shared-ontology projections; remote native ontology and version history remain private unless separately authorized.
9. **Observable evolution:** Private remote changes that leave an authorized projection unchanged do not generate a new observable version for that recipient.
10. **Home Space recognition and warranty:** The Home Space recognizes authoritative versions and warrants shared information; receivers verify the shared contract, not hidden native descriptor completeness.
11. **Pull-based adoption:** Publication and successor discovery do not mutate existing consumer bindings; automated policies authorize recorded local transitions.
12. **Safe publication:** Release activation is semantically atomic, idempotent, validated, and recoverable.

## 10. Overall conclusion

The earlier architecture supplies the **lifecycle mechanics**: private Module work, immutable releases, deterministic manifests, release-gated publication, Stewardship Anchors, and pull-based adoption. The later inquiry supplies the **semantic boundary model**: contextual dependency resolution, coarse-grained binding, two Mirror roles, ontological commoning, membrane opacity, and Home Space validation sovereignty.

These are broadly complementary. The substantive corrections are that cross-Space inverse publication cannot imply remote authoritative mutation or recognition; cross-Space Mirrors need not expose remote native Modules or versions; direct references must not be casually replaced by mandatory packaging-qualified indirection; and schema-specific containment must be reconciled with the earlier generic/nested Module model.

**Working architectural summary:** *Holons evolve and are recognized within their unique Home Space. Modules develop privately and publish deterministic, contextually resolved configurations. Consumers adopt coherent releases by pull. Mirrors mediate reference boundaries without compromising authoritative ownership. Across Agent membranes, TrustChannels expose only Agreement-governed shared-ontology projections, whose validity is warranted by the originating Agent rather than revalidated against inaccessible native descriptors by the recipient.*
