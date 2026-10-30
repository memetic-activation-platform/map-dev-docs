# MAP Module Design — Working Architecture for Sub-Space Packaging, Release, and Publication

## Status

Working design intended to drive specification and implementation-plan updates.

This captures the Module concept as developed so far. `Module` is the current working term; terminology may still evolve, but the architectural distinctions below should be treated as the substantive design.

---

# 1. Motivation

MAP currently has a strong concept of the `Space` as an agent boundary and home for holons.

A Space may contain many holons that are actively being developed and may also contain relationships to holons homed in other Spaces.

The current versioning model allows a holon version to be created by cloning its predecessor, including its declared relationships. This creates a problem when such changes are immediately made externally visible through inverse relationship propagation.

Consider:

    A1 --depends_on--> B1

where:

- `A1` is homed in Space A.
- `B1` is homed in Space B.
- the relationship has an inverse such that Space B can navigate from `B1` back to `A1`.

If a new version `A2` is created by cloning `A1`, it initially inherits:

    A2 --depends_on--> B1

If ordinary commit immediately propagates the inverse, Space B may now observe:

    B1 <--depended_on_by-- A2

even though:

- `A2` may only be an intermediate working version;
- further versions `A3`, `A4`, etc. may follow before anything is ready for external consumption;
- the set of changes may temporarily be internally inconsistent;
- no coordinated release has occurred;
- and downstream Spaces should not be distracted by every intermediate state.

This reveals the need for a packaging and release boundary below the level of a Space.

That construct is currently called a **Module**.

---

# 2. Core Concept

A `Module` is a bounded, stewarded body of holons within a Space that can be evolved privately and released as a coherent unit.

A Module is:

- below the Space level;
- contained within a Space;
- not itself an AgentSpace;
- not a new agent boundary;
- not necessarily independently authoritative in the same sense as a Space;
- a development boundary;
- a release boundary;
- a publication boundary;
- a dependency-management boundary;
- and potentially a nested unit of organization.

A concise working definition is:

> A Module is a bounded body of holons within a Space that is developed privately and released as a coherent unit.

The critical behavior is that changes made within an unreleased Module do not automatically become externally visible merely because individual holon versions have been committed.

---

# 3. Architectural Placement

The conceptual containment hierarchy is:

    AgentSpace
        └── Module
              ├── Holon
              ├── Holon
              ├── Holon
              └── possibly nested Module

A Space may contain:

- holons not currently governed by a Module;
- one or more Modules;
- potentially nested Modules;
- working state for Modules;
- released Module versions.

A Module does not create another agent membrane comparable to the membrane around an AgentSpace.

It is an internal packaging and publication boundary within the containing Space.

---

# 4. Why Module Is Not a Space

Do not model a Module as a Subspace or smaller AgentSpace.

A Space carries semantics associated with:

- agency;
- stewardship authority;
- home-space identity;
- trust channels;
- inter-agent membranes;
- external proxy or mirror behavior;
- and potentially its own execution and governance boundary.

A Module exists inside such a Space and does not independently acquire those semantics.

In particular:

> A holon remains homed in its Space. Inclusion in a Module does not create a new home Space.

---

# 5. The Two Rhythms of Change

The Module model introduces an explicit distinction between:

1. **private development**, and
2. **released state**.

Within private development, change can be fine-grained and fluid.

A Module workspace may contain:

- staged holons;
- committed new holon versions;
- multiple successive working versions;
- changes to properties;
- changes to relationships;
- temporary inconsistencies;
- dependency upgrades under evaluation;
- incomplete migrations;
- refactorings;
- experimental alternatives;
- and other states that should not yet become part of the externally observable MAP.

By contrast, release establishes a coherent state intended for external consumption.

This creates the following broad lifecycle:

    transient state
        ↓
    committed but unreleased state
        ↓
    validated module state
        ↓
    module release
        ↓
    externally published state

The distinction between `commit` and `release` is fundamental.

---

# 6. Commit Is Not Release

A commit means approximately:

> Persist this holon version or relationship state within its home Space.

A release means approximately:

> Publish this coordinated, validated Module state as an externally consumable versioned offering.

Therefore:

> A committed holon version inside an unreleased Module must not automatically become part of the externally visible release graph.

This is especially important for inverse relationship behavior.

---

# 7. Module Workspace

A Module should have a concept corresponding to mutable, unreleased working state.

Working term:

**Module Workspace**

A Module Workspace contains the current development state of the Module.

Its state may include holon versions that have been durably committed inside the Space but have not yet been released.

A Module Workspace is therefore not merely transient memory.

It may be durable while still remaining unpublished.

Possible conceptual states include:

    Module M
        Released state: R7
        Working state:
            A8
            B12
            C4
            external dependencies under evaluation

The workspace may advance through multiple holon versions without creating a Module Release.

---

# 8. Module Release

A **Module Release** is an immutable published state of a Module.

A release identifies a coherent set of exact holon versions and dependency bindings.

Conceptually:

    Module M
        Release R7
            Holon A v12
            Holon B v4
            Holon C v19
            External X v8
            External Y v3

A Module Release is analogous in some respects to:

- a software package release;
- a package lockfile;
- a build manifest;
- a Git release;
- or a Merkle-rooted snapshot.

However, the semantics are MAP-native and apply to arbitrary holonic structures, not merely executable software.

---

# 9. Release Package

`Release Package` remains a useful term for the immutable artifact or dependency closure produced by releasing a Module.

The distinction is:

- **Module** — enduring organizational and stewardship construct.
- **Module Workspace** — mutable unreleased development state.
- **Module Release** — one immutable released state of the Module.
- **Release Package** — the exact deterministic content/dependency closure represented by that Module Release.
- **Module Manifest** — explicit description of the versions and bindings included in a release.

These may ultimately collapse into fewer concrete types, but the semantic distinctions should remain clear.

---

# 10. Stewardship Anchor

The existing concept of a **Stewardship Anchor** fits naturally into the Module design.

A Stewardship Anchor is the enduring identity and discovery point through which successive releases of a governed body of holons become available.

A useful distinction is:

> Stewardship Anchor = enduring identity and release channel.

> Stewardship Anchor Version = one immutable release event.

> Release Package = the deterministic dependency closure designated by that release.

Conceptually:

    Stewardship Anchor M
        ├── Release R5
        ├── Release R6
        └── Release R7

A consumer that follows the Stewardship Anchor may learn that `R7` exists without automatically adopting it.

---

# 11. Deterministic Release Bindings

A released state must not contain unspecified moving dependencies.

Core invariant:

> Released holons must not depend on an unspecified or mutable "latest" version of another holon.

Every dependency in a release must resolve to a specific immutable version, either:

- directly to a HolonVersion; or
- indirectly through a specific immutable Module Release or Stewardship Anchor Version that deterministically resolves to exact versions.

For example:

    Module M / Release R7

        A v12
            depends_on -> X v8

        B v4
            depends_on -> Y v3

The release may track where successor versions of `X` or `Y` can later be discovered, but the released graph remains bound to the exact versions originally adopted.

---

# 12. Module Manifest

A Module Release should be able to determine exactly what state was released.

A conceptual Module Manifest may contain:

    ModuleRelease
        module_identity
        release_identity
        previous_release
        released_roots[]
        included_holon_versions[]
        dependency_bindings[]
        release_metadata
        validation_evidence
        exports[]

A dependency binding may conceptually contain:

    DependencyBinding
        dependency_identity
        home_space
        adopted_version
        upstream_stewardship_anchor
        upstream_release

The exact physical representation remains open.

The important requirement is determinism.

---

# 13. Release Closure

A release must establish enough closure to determine its meaning reproducibly.

This does not mean copying every externally homed holon into the release.

An external holon remains homed and stewarded by its own Space.

The Module Release instead binds to the exact external version against which the release was developed and validated.

Therefore:

> Release closure is a closure of deterministic bindings, not necessarily a closure of physical ownership or storage.

---

# 14. Modules May Be Nested

Modules may need to exist at multiple levels of granularity.

For example:

    I-Space
        ├── Personal Knowledge Module
        │     ├── Research Module
        │     └── Bibliography Module
        │
        └── MAP Development Module
              ├── Core Schema Module
              └── Query Module

A higher-level Module Release may bind to released versions of nested Modules rather than enumerating every leaf holon directly.

For example:

    MAP Development Release R12
        Core Schema Module Release R7
        Query Module Release R3

This allows each Module to evolve and release at an appropriate cadence.

It avoids forcing the entire Space onto a single synchronized release train.

---

# 15. Module Membership and Holon Identity

A major design decision is:

> Module membership should not be encoded into ordinary Holon identity.

Suppose:

    X --references--> Y

and later `Y` is included in Module `M`.

Do not automatically transform the relationship into something equivalent to:

    X --references--> M::Y

and do not require a new version of `Y` merely because it has been packaged into `M`.

The guiding principle is:

> Inclusion in a Module Release is definitional to the containing release, but is not necessarily definitional to the included holon.

In other words:

    ModuleRelease R7 includes Y v2

changes the definition of `R7`.

It does not necessarily change the intrinsic definition or identity of `Y v2`.

This avoids coupling Holon identity to packaging topology.

---

# 16. Why Module Membership Should Not Be in Relationship Identifiers

Encoding Module boundaries into ordinary relationship targets would create undesirable ripple effects.

For example, if:

    X --references--> Y

and then `Y` is placed into Module `M`, module-qualified identity could force the reference to become:

    X --references--> M::Y

Consequences would include:

- moving a holon into a Module becoming a definitional change;
- inbound relationships potentially requiring replacement;
- unnecessary creation of new holon versions;
- identity churn caused by packaging reorganization;
- nested Modules making identifiers increasingly complex;
- dependency syntax becoming coupled to deployment topology;
- packaging concerns leaking into ordinary semantic relationships.

This should be avoided unless a specific use case explicitly requires a module-qualified export reference.

---

# 17. Module Membership Belongs to the Containing Structure

The preferred direction is:

> Membership belongs to the Module Release, not intrinsically to the member Holon.

For example:

    Module M / Release R7
        includes Y v2

rather than:

    Y v2
        module = M

This also supports the possibility that an immutable HolonVersion may participate in more than one higher-level release package without requiring duplication or redefinition.

Whether MAP ultimately permits a HolonVersion to participate in multiple Modules or imposes stronger ownership constraints remains a separate policy question.

The relationship identity model should not preclude either option unnecessarily.

---

# 18. Direct References Remain Direct

An ordinary deterministic relationship should continue to look conceptually like:

    X v4 --references--> Y v2

The relationship itself need not encode:

- which Module published `Y v2`;
- which release contained it;
- which stewardship anchor governs its future versions;
- or what Module currently packages it.

Those facts can be discovered from publication and provenance metadata where required.

This preserves ordinary MAP relationship semantics.

---

# 19. Module-Qualified Exports May Be a Separate Feature

Although Module identity should not infect every relationship expression, Modules may eventually expose a deliberate public surface.

For example:

    Module M exports:
        customer_schema -> Y v2
        validation_rules -> Z v5

A consumer may then intentionally reference an exported binding rather than a raw holon identity.

Conceptually:

    X depends_on -> Module M / Release R7 / Export customer_schema

which resolves deterministically to:

    Y v2

This creates two valid forms of dependency:

## 19.1 Direct Holon Reference

    X -> Y v2

Meaning:

> This relationship depends specifically on this HolonVersion.

## 19.2 Module Export Reference

    X -> Module M / Release R7 / Export E

Meaning:

> This relationship depends on a public binding exposed by this specific Module Release.

This distinction should not be implemented prematurely unless needed, but the Module design should leave room for it.

---

# 20. Cross-Space Relationships and the Existing Problem

Consider a released state:

    A1 --depends_on--> B1

where `B1` is homed in another Space.

The current system may maintain the inverse:

    B1 <--depended_on_by-- A1

When `A2` is created from `A1`, the forward relationship is cloned:

    A2 --depends_on--> B1

Under immediate inverse propagation, this may cause:

    B1 <--depended_on_by-- A2

This is premature if `A2` is merely an unreleased working version.

If development continues:

    A2
    A3
    A4
    A5

then all intermediate versions might otherwise appear externally.

That would create noise and expose states never intended for external consumption.

---

# 21. New Inverse Publication Rule

The Module design changes the treatment of inverses crossing publication boundaries.

Core rule:

> A relationship whose source HolonVersion is part of unreleased Module working state must not create externally visible inverse relationship state merely because that source version was committed.

More generally:

> Cross-boundary inverse visibility is derived only from released relationship assertions.

The transition that makes the relationship externally visible is therefore Module release, not ordinary holon commit.

---

# 22. Commit-Time Versus Release-Time Behavior

The current conceptual behavior may resemble:

    commit relationship
        ↓
    inspect RelationshipDescriptor
        ↓
    determine inverse
        ↓
    propagate inverse

The Module-aware behavior should instead distinguish local persistence from external publication.

Local commit:

    commit relationship
        ↓
    persist declared relationship locally
        ↓
    if governed by unreleased Module state:
        do not publish external inverse

Module release:

    validate Module Workspace
        ↓
    establish immutable Module Release
        ↓
    determine externally publishable relationship assertions
        ↓
    publish or index inverse visibility as appropriate

Therefore:

> Cross-Space inverse propagation should no longer be treated as an unconditional side effect of individual HolonVersion commit.

---

# 23. Intermediate Versions Are Never Published

Suppose the history is:

    A1  released
    A2  committed, unreleased
    A3  committed, unreleased
    A4  committed, unreleased
    A5  released

and every version declares:

    Ai --depends_on--> B1

Then only:

    A1
    A5

should ever participate in externally visible released relationship assertions.

`A2`, `A3`, and `A4` are not "published and later compressed."

They should simply never cross the publication boundary.

This is an important semantic distinction.

---

# 24. Release Publication Is Not Adoption

A second distinction is equally important.

Suppose `A5` is released.

Making the released assertion visible:

    A5 --depends_on--> B1

or making the inverse navigable:

    B1 <--depended_on_by-- A5

does not mean any downstream consumer has adopted `A5`.

Publication means:

> A new released assertion exists.

Adoption means:

> A consumer has explicitly changed one of its own bindings to use that new released version.

These must remain separate concepts.

---

# 25. Semantic Relationship Versus Successor Availability

The system should not overload inverse relationships to mean that a new version is available.

These are distinct concepts.

## 25.1 Semantic Relationship

    A5 --depends_on--> B1

This is part of the released graph.

## 25.2 Derived Inverse Visibility

    B1 <--depended_on_by-- A5

This is a navigational reflection of the published assertion.

## 25.3 Successor Availability

    Stewardship Anchor A
        Release R7
            contains A5
            succeeds prior released state containing A1

This tells downstream consumers that a newer candidate release exists.

Successor availability should come through the release lineage or Stewardship Anchor, not by abusing domain relationship inverse propagation.

---

# 26. External Holons Should Not Be Mutated by Foreign Publication

A deeper architectural principle follows from home-space stewardship.

If `B1` is homed in Space B, then publication from Space A should not semantically mutate the authoritative state of `B1`.

Therefore, an inverse originating from a relationship authored in Space A should be understood as one of:

- a derived inverse view;
- an inbound-reference index;
- a published external assertion;
- a relationship projection;
- or some equivalent non-authoritative representation.

The authoritative relationship remains:

    A5 --depends_on--> B1

Space B may expose inverse navigation based on that assertion, but the existence of the inverse does not imply that `B1` itself was re-authored or versioned.

Core principle:

> Foreign publication may make an inverse discoverable without making the foreign Space the author of that relationship.

---

# 27. Historical Inverse Versus Current Views

After multiple releases, a target Holon may legitimately have published relationships from several immutable source versions.

For example:

    B1 <--depended_on_by-- A1
    B1 <--depended_on_by-- A5
    B1 <--depended_on_by-- A9

All may be historically true.

Different query surfaces may choose different projections.

Possible views include:

## 27.1 Historical View

Return every released source version.

    A1
    A5
    A9

Useful for:

- provenance;
- audit;
- historical analysis.

## 27.2 Released-Head View

Collapse versions by stewardship lineage and return only the latest relevant released head.

    A9

Useful for ordinary navigation.

## 27.3 Adopted View

Return the version actually selected by a local consumer.

This might still be:

    A5

even though `A9` is available.

These are query/projection semantics and should not be confused with underlying immutable assertions.

---

# 28. Sense-and-Respond Behavior

The broader MAP model includes active sensing at references to externally stewarded holons.

Conceptually, an I-Space contains:

- locally homed holons;
- relationships extending to holons homed in other Spaces;
- and active boundary behavior that can detect when successor releases become available.

The imagery is of local holons with "tentacles" reaching toward externally homed holons.

At the endpoints of those tentacles are distributed sense-and-respond behaviors.

A reference may know:

- the currently adopted external version;
- the Stewardship Anchor or release channel being followed;
- newly available releases;
- update/adoption policy;
- trust conditions;
- compatibility criteria;
- delegated decision authority;
- and adoption history.

These should not require the human steward to synchronously approve every minor update.

Decision authority may be delegated to Dancers or other subsidiary agents under policy.

---

# 29. Detecting a New Release Does Not Change a Binding

Suppose a local relationship currently resolves to:

    X --references--> A1

and the Stewardship Anchor later publishes a release containing `A5`.

The existing released relationship remains:

    X --references--> A1

The system may now know:

    A5 is an available successor candidate

but it must not silently change the existing binding.

A candidate update is distinct from the current relationship.

---

# 30. Update Candidate

A useful conceptual object or state may be an `UpdateCandidate`.

This does not yet imply that a concrete HolonType must be created, but specifications should preserve the distinction.

Conceptually:

    UpdateCandidate
        existing_binding
        current_target_version
        candidate_target_version
        discovered_via_release
        discovered_via_stewardship_anchor
        state

Possible states might include:

    unassessed
    evaluating
    deferred
    rejected
    accepted

If accepted, adoption results in new local versioned state.

It does not mutate previously released local state.

---

# 31. Adoption Flow

A downstream Space may respond to an upstream release as follows:

    upstream Module Release becomes available
        ↓
    sense successor release
        ↓
    identify locally affected bindings
        ↓
    create/update candidates
        ↓
    evaluate through human or delegated policy
        ↓
    optionally create private Module Workspace changes
        ↓
    adapt related local holons together
        ↓
    validate coordinated state
        ↓
    create new local Module Release
        ↓
    publish downstream

This creates asynchronous propagation of coherent change without global synchronization.

---

# 32. Pull Over Push

The Module design should preserve MAP's existing pull-over-push philosophy.

An upstream release is made **available**.

It does not force downstream Spaces to advance.

Each consumer decides when and whether to take the release on board.

Therefore:

> Publication is push-like only in the limited sense of making availability discoverable. Semantic adoption remains pull-based and locally governed.

A consumer may:

- adopt immediately;
- evaluate automatically;
- wait for a compatibility condition;
- defer until a coordinated local release window;
- reject;
- or continue indefinitely with an older valid release.

---

# 33. Local Coordination of Upstream Changes

A downstream Space may depend on several items from an upstream Module.

When a new release appears, it may be undesirable to update those dependencies one by one.

Instead:

    upstream Release R8 detected
        ↓
    downstream Module Workspace created or updated
        ↓
    relevant bindings updated together
        ↓
    adaptations made
        ↓
    validation performed
        ↓
    downstream Module Release created

This allows external change to be incorporated in coordinated local units rather than as uncontrolled fine-grained mutation.

---

# 34. Module Release as a Publication Boundary

The Module is fundamentally a publication boundary.

Changes inside the boundary may occur frequently.

Only selected coherent states cross it.

This gives the following invariant:

> Internal commit frequency is independent of external publication frequency.

For example:

    47 HolonVersion commits
        ↓
    1 Module Release

There should be no requirement that every committed state become externally visible.

---

# 35. Module Boundary and Relationship Syntax

The preferred working design is:

> Do not modify general relationship syntax to encode Module boundaries.

Ordinary relationship expressions remain based on semantic source, RelationshipType, and target.

For example:

    X v4 --references--> Y v2

not:

    X v4 --references--> ModuleM::Y v2

Module context is discovered separately where needed.

This avoids introducing a pervasive packaging concern into MAP's fundamental relationship model.

---

# 36. Module Boundary and Resolution

Although Module membership is not part of ordinary relationship syntax, the runtime may need to resolve publication context for a HolonVersion.

Given:

    source = X v4

the runtime may need to determine:

- Is this source part of a Module Workspace?
- Has this source been included in a Module Release?
- Which Module governs publication of this source?
- Which Module Release published it?
- Is the target inside or outside the same Module?
- Is the target inside or outside the same Space?
- Does crossing this boundary trigger publication behavior?
- Does an applicable agreement permit publication?

This is contextual metadata used by the publication pipeline.

It is not necessarily embedded in the relationship identifier.

---

# 37. Release-Time Relationship Publication

At Module release time, the system should calculate the externally relevant relationship delta or publication set.

Conceptually:

    ModuleRelease R7

        for each released source HolonVersion:
            inspect its declared relationships

            for each relationship:
                determine target
                determine target publication/home context
                determine inverse descriptor if applicable
                determine whether relationship crosses Module boundary
                determine whether relationship crosses Space boundary
                determine applicable publication/access policy

                publish only assertions permitted by the release

The exact implementation may optimize this process through manifests, dependency indices, release deltas, caches, or precomputed metadata.

The semantics should remain release-driven.

---

# 38. Same-Module Relationships

Relationships whose source and target both belong to the same Module release are internal to that released package.

They should not need the same cross-boundary publication treatment as relationships that leave the Module.

For example:

    Module M / Release R7
        A12 -> B4
        B4  -> C19

These relationships participate naturally in the released Module graph.

Whether local inverse indexes are populated at commit or release remains an implementation choice if there is no externally observable semantic difference.

The critical constraint is on boundary-crossing visibility.

---

# 39. Cross-Module Relationships Within the Same Space

A relationship may cross Module boundaries while remaining within one AgentSpace.

For example:

    Module A / Holon X
        references
    Module B / Holon Y

This is one reason the Module concept cannot be reduced to cross-Space behavior.

The same release/publication principle may apply:

- Module A may be under active development.
- `X2`, `X3`, and `X4` may remain unreleased.
- Module B should not necessarily observe every intermediate relationship assertion.
- Module A Release R9 should establish the externally visible Module-to-Module state.

The system therefore needs to distinguish:

- same Module;
- different Module, same Space;
- different Space.

The exact policy may vary, but Module boundaries matter independently of Space membranes.

---

# 40. Cross-Space Relationships

Cross-Space publication adds further constraints:

- home-space authority;
- TrustChannels;
- applicable agreements;
- access controls;
- possible proxy/mirror representations;
- externally indexed inverse relationships;
- distributed release discovery.

Module release does not replace those mechanisms.

Instead:

> Module release determines when an assertion becomes eligible to cross those existing inter-Space boundaries.

---

# 41. Relationship Descriptor Semantics Remain Intact

The RelationshipDescriptor still determines semantic relationship behavior such as:

- relationship identity/type;
- source constraints;
- target constraints;
- cardinality;
- inverse RelationshipType or descriptor;
- other declared semantics.

The Module does not replace descriptor-aware relationship semantics.

Instead, publication now requires both:

1. relationship-level semantic information from the descriptor; and
2. source publication context from the Module/release system.

So the effective decision becomes something like:

    relationship semantics
        +
    publication context
        +
    boundary context
        +
    applicable policy
        =
    publication behavior

---

# 42. Module Membership Should Not Require Holon Re-Versioning by Itself

If an existing immutable HolonVersion `Y1` is subsequently included in Module `M`, that inclusion should not inherently require creation of `Y2`.

The new fact can be expressed as:

    Module M / Release R1
        includes Y1

rather than modifying `Y1`.

Similarly, removing `Y1` from a later Module Release changes the Module Release definition, not the historical definition of `Y1`.

This preserves immutable HolonVersion identity.

---

# 43. A Holon's Packaging History Can Change Without Rewriting Its History

For example:

    Release M/R1 includes Y1
    Release M/R2 includes Y2
    Release M/R3 no longer includes Y

These facts belong to Module release history.

The historical HolonVersions remain unchanged.

This separation is important for:

- auditability;
- provenance;
- reproducibility;
- stable referencing;
- historical query semantics.

---

# 44. Potential Module Surface

A Module may eventually define a deliberate external/public surface.

Possible concepts include:

- exports;
- published roots;
- externally navigable Holons;
- released relationship assertions;
- entry points;
- supported Dances;
- schemas or interfaces;
- dependency declarations.

A Module should not necessarily expose every internal Holon merely because that Holon participates in its release closure.

This distinction is analogous to the difference between:

- package internals; and
- package exports/public API.

The detailed Module Surface design remains open.

---

# 45. Release Validation

Before a Module Release becomes externally published, it should undergo validation appropriate to its content.

Potential validation categories include:

- descriptor-aware Holon validation;
- relationship cardinality;
- relationship target validity;
- dependency resolution;
- deterministic dependency binding;
- absence of unresolved working references;
- Module membership consistency;
- Module export validity;
- release closure completeness;
- external dependency availability;
- agreement/access constraints;
- migration compatibility where applicable.

The exact validation rule set should be specified separately.

The important architectural rule is:

> Publication occurs only after release validation succeeds.

---

# 46. Relationship Inverses and Release Validation

Release validation should be able to calculate or verify the inverse effects that publication will create.

For example:

    A5 --depends_on--> B1

with declared inverse:

    B1 <--depended_on_by-- A5

The release process can:

1. inspect the forward RelationshipDescriptor;
2. discover the inverse RelationshipDescriptor;
3. determine whether the relationship crosses a Module or Space boundary;
4. determine whether it is eligible for external publication;
5. calculate the resulting inverse publication;
6. publish it only once the Module Release succeeds.

This prevents failed or abandoned working state from producing external inverse residue.

---

# 47. Publication Should Be Atomic at the Module Release Level

The conceptual external effect of a Module Release should be atomic even if physical propagation requires multiple storage operations.

Observers should not intentionally be exposed to a partially published Module Release.

At the semantic level:

> A Module Release either exists as a coherent released state or it does not.

Implementation may require transactional strategies, release markers, completion records, staged indexes, or other mechanisms depending on storage-provider capabilities.

This should be explored in the implementation plan.

---

# 48. Release Lineage

A Module should expose release lineage.

For example:

    Module M
        R5
         ↓
        R6
         ↓
        R7

Successor relationships between Module Releases allow consumers to determine that a new release is available.

This is preferable to trying to infer successor availability from inverse domain relationships.

Release lineage should support:

- deterministic predecessor/successor navigation;
- release discovery;
- change comparison;
- candidate update generation;
- provenance.

Whether releases permit branching and merging is an open design question.

Do not assume a strictly linear history unless existing MAP versioning semantics already require it.

---

# 49. Stewardship Anchor and Module Relationship

A likely model is:

    StewardshipAnchor
        stewards -> Module identity
        exposes -> Module Releases

or possibly:

    Module
        has StewardshipAnchor

The exact relationship orientation and type naming should be determined based on existing MAP schema conventions.

The important semantic role is that consumers follow an enduring release identity rather than a mutable "latest Holon" pointer.

---

# 50. Relationship to Existing External-ID / Proxy / Mirror Concepts

Existing cross-Space reference mechanisms remain relevant.

When a target is homed in another Space, MAP may use concepts such as:

- external IDs;
- outbound proxies;
- Mirror Holons;
- remote object IDs;
- Agent/Space proxies.

Module support should not unnecessarily replace these.

Instead, Module context adds release and publication semantics around them.

A foreign reference may conceptually resolve:

    local relationship
        ↓
    external target identity
        ↓
    remote home Space
        ↓
    target HolonVersion

while the update-discovery path may separately resolve:

    current target version
        ↓
    governing Stewardship Anchor
        ↓
    newer Module Release
        ↓
    candidate successor version

Do not collapse reference identity and update-channel identity unless there is a compelling reason.

---

# 51. Module Is Not a Namespace

A Module should not initially be treated as a namespace.

The following should remain distinct concepts:

- identity;
- naming;
- containment;
- packaging;
- release;
- publication.

Module-qualified names may later exist for human or export resolution, but they should not drive fundamental Holon identity unless separately justified.

---

# 52. Module Is Not Merely a Collection

A Module differs from an ordinary collection because it carries behavioral semantics.

A Module establishes at least:

- a development boundary;
- a release boundary;
- a publication boundary;
- a dependency boundary;
- a version/release lineage;
- and a coherent unit of adoption.

Therefore, avoid implementing Module merely as another arbitrary Collection without these lifecycle semantics.

---

# 53. Module Is Not Necessarily Semantic Domain

Do not conflate Module with a conceptual or ontological Domain.

A Domain groups things according to subject matter or semantic community.

A Module groups things according to coordinated development, release, and publication.

These may often coincide, but they need not.

---

# 54. Relationship to Semantic-Web Concepts

Relevant precedents include:

- RDF Named Graphs;
- RDF Datasets;
- ontology modules;
- versioned ontologies;
- modular knowledge graphs.

However, MAP Modules have richer lifecycle semantics.

A Module combines concerns that Semantic Web systems often treat separately:

- graph grouping;
- provenance;
- publication;
- versioning;
- release;
- stewardship;
- dependency management;
- asynchronous downstream adoption.

Therefore, Semantic Web terminology can inform the design but should not constrain MAP to a weaker model.

---

# 55. Terminology

Current working vocabulary:

## Module

The enduring sub-Space unit whose holons are developed and released together.

## Module Workspace

Mutable and potentially durable unreleased working state associated with a Module.

## Module Release

An immutable, validated, published state of a Module.

## Release Package

The deterministic set/closure of specific versions and bindings represented by a Module Release.

May ultimately remain conceptual rather than become a separate first-class HolonType.

## Module Manifest

The explicit description of the exact content and dependency bindings of a Module Release.

May likewise be conceptual or derived rather than separately persisted.

## Module Surface

The explicitly exposed/public portion of a Module Release.

Still under design.

## Module Export

A stable public name or binding exposed by a Module Release.

Potential future capability.

## Stewardship Anchor

The enduring identity/release-discovery point through which consumers discover successive Module Releases.

## Update Candidate

A locally observed opportunity to replace an adopted external binding with a newer released version.

Potential conceptual or first-class construct.

---

# 56. Candidate High-Level Invariants

The following invariants should guide the specification.

## MOD-INV-001 — Space Home Authority

A Module does not change the home Space of any HolonVersion it contains.

## MOD-INV-002 — Commit Is Not Publication

Committing a HolonVersion inside an unreleased Module does not make that version externally published.

## MOD-INV-003 — Release Controls Boundary Visibility

Boundary-crossing relationship assertions become externally visible only through release/publication behavior, not merely through local commit.

## MOD-INV-004 — No Intermediate Publication

HolonVersions created during Module development but never included in a Module Release must not become externally visible solely through inverse propagation.

## MOD-INV-005 — Deterministic Release

A Module Release resolves to a deterministic set of exact HolonVersions and dependency versions.

## MOD-INV-006 — No Moving Released Dependencies

A released dependency may not semantically mean "whatever version is currently latest."

## MOD-INV-007 — Publication Is Not Adoption

Availability or publication of a newer release does not alter existing downstream bindings.

## MOD-INV-008 — Adoption Creates New Local State

Adopting an updated dependency results in new local versioned state rather than mutation of previously released state.

## MOD-INV-009 — Packaging Is Not Intrinsic Identity

Including an immutable HolonVersion in a Module Release does not inherently alter that HolonVersion's identity or require a replacement version.

## MOD-INV-010 — Relationship Syntax Is Packaging-Neutral

Ordinary Holon relationship identifiers do not encode Module boundaries.

## MOD-INV-011 — Membership Defined by Container

Module Release membership is primarily asserted by the Module Release rather than intrinsically by each member HolonVersion.

## MOD-INV-012 — Foreign Publication Does Not Re-Author Target

Publishing a relationship to a remotely homed Holon must not imply modification of that target Holon's authoritative versioned state.

## MOD-INV-013 — Inverse Visibility Is Derived

Cross-Space inverse navigation reflects published relationship assertions and does not imply ownership or adoption by the target Space.

## MOD-INV-014 — Successor Discovery Is Separate From Domain Inverses

New-release availability is discovered through release lineage / Stewardship Anchors, not inferred by overloading semantic inverse relationships.

## MOD-INV-015 — Module Boundary Exists Below Space Boundary

The system must support meaningful release/publication behavior across Module boundaries even when both Modules are contained in the same Space.

---

# 57. Illustrative Scenario

Initial released state:

    Space S1

        Module M
            Release R1
                A1

        A1 --depends_on--> B1

    Space S2

        B1

External inverse visibility may expose:

    B1 <--depended_on_by-- A1

Development begins in Module M:

    Module M / Workspace

        A2 --depends_on--> B1
        A3 --depends_on--> B1
        A4 --depends_on--> B1
        A5 --depends_on--> B1

`A2`, `A3`, and `A4` may each be committed locally.

None should become externally visible.

Eventually Module M releases:

    Module M
        Release R2
            A5

At release time:

    A5 --depends_on--> B1

becomes a published assertion.

Space S2 may now expose:

    B1 <--depended_on_by-- A1
    B1 <--depended_on_by-- A5

Historical navigation may expose both.

A released-head view may expose only `A5`.

No downstream reference to `A1` automatically changes.

A consumer that follows the Stewardship Anchor for Module M may learn that Release R2 exists and create an UpdateCandidate from `A1` to `A5`.

Only after adoption does the downstream Space create new local versioned state referring to `A5`.

---

# 58. Illustrative Same-Space Cross-Module Scenario

Consider:

    Space S1

        Module M1
            X1

        Module M2
            Y1

with:

    X1 --references--> Y1

Now work begins on M1:

    X2 --references--> Y1
    X3 --references--> Y1
    X4 --references--> Y1

If `X2` through `X4` are unreleased working versions, Module M2 should not necessarily observe every intermediate state merely because both Modules are in the same Space.

When M1 releases:

    M1 / Release R8
        X4

the relationship from `X4` to `Y1` becomes part of the released Module-to-Module topology.

This demonstrates that Module publication semantics are not reducible to cross-Space membranes.

---

# 59. Potential Runtime Questions

The implementation will need efficient answers to questions such as:

- Is this HolonVersion governed by a Module?
- Which Module?
- Is it part of the current Module Workspace?
- Which Module Releases include it?
- Is it part of the current released head?
- Is the target in the same Module?
- Is the target in another Module in the same Space?
- Is the target in another Space?
- Which Stewardship Anchor governs successor discovery?
- Which release currently binds this dependency?
- Has a newer release become available?
- Does this relationship have a declared inverse?
- Is the inverse eligible for publication?
- Has that inverse already been published for this Module Release?
- Which released relationship assertions should appear in a current-head projection?
- Which should appear in a historical projection?

The implementation plan should identify indexes or lookup structures required to make these questions practical.

---

# 60. Potential Schema Concepts

Codex should evaluate whether the design requires new explicit HolonTypes and RelationshipTypes.

Candidate HolonTypes may include:

- Module
- ModuleRelease
- ModuleWorkspace, if persistent representation is required
- ModuleManifest, if not derived
- ModuleExport
- UpdateCandidate
- StewardshipAnchor, if not already modeled

Candidate relationships may include concepts such as:

- Module Contains/Includes HolonVersion
- Module HasRelease ModuleRelease
- ModuleRelease Succeeds ModuleRelease
- ModuleRelease Includes HolonVersion
- ModuleRelease DependsOn ModuleRelease
- Module HasStewardshipAnchor StewardshipAnchor
- ModuleRelease Exports HolonVersion
- ModuleRelease HasManifest ModuleManifest

Do not adopt these names mechanically.

First inspect the existing ontology and reuse or extend existing concepts where appropriate.

---

# 61. Potential Implementation Boundary

The implementation should avoid scattering Module logic throughout unrelated relationship code.

Prefer introducing an explicit release/publication layer.

Conceptually:

    Holon editing/versioning
        ↓
    local commit
        ↓
    Module Workspace state
        ↓
    Module release validation
        ↓
    Module Release creation
        ↓
    publication planning
        ↓
    external relationship/inverse publication
        ↓
    release availability signaling

This keeps ordinary Holon commit semantics simpler and makes release behavior explicit.

---

# 62. Publication Planning

Consider representing release effects before applying them.

A publication plan might contain:

    PublicationPlan
        released_versions[]
        new_external_assertions[]
        retired_current-head_assertions[]
        derived_inverse_updates[]
        stewardship_notifications[]
        dependency_release_bindings[]
        validation_results[]

This could support:

- validation before publication;
- transactional application;
- auditability;
- idempotency;
- recovery;
- testing.

Whether this becomes a first-class persistent object is open.

---

# 63. Idempotency

Release publication must be idempotent.

Retrying publication of the same immutable Module Release must not produce duplicate relationship assertions, inverse entries, notifications, or other externally visible artifacts.

The implementation plan should identify stable keys for release-published assertions.

A likely basis is some deterministic combination of:

- Module Release identity;
- source HolonVersion;
- RelationshipType;
- target HolonVersion;
- relationship ordinal/key where relevant.

Exact representation depends on existing MAP relationship identity semantics.

---

# 64. Failure Semantics

The spec should define what happens if physical publication partially fails.

At the semantic level, the Module Release should not appear as partially published.

Potential strategies include:

- staged publication followed by release activation;
- release-complete marker;
- idempotent replay;
- compensating cleanup;
- provider-level transactional semantics where available.

This is an implementation-design area requiring explicit treatment.

---

# 65. Interaction With Caching and Release Refresh Policies

MAP already distinguishes release-driven refresh from ordinary TTL or epoch-driven refresh.

Modules provide a natural unit for the existing `Release` cache policy.

A consumer following an upstream Module should be able to say conceptually:

> Continue using the currently adopted Module Release until I deliberately pull and accept a successor release.

This reinforces the policy:

> The ontological world does not change out from underneath a consumer.

New releases are made available.

Consumers pull them when appropriate.

---

# 66. Interaction With Mirror/Proxy Holons

If MAP adopts the `Mirror Holon` terminology for local representations of externally homed holons, Module release should interact with Mirrors carefully.

A Mirror may represent:

- the locally known identity of a remote Holon;
- the currently adopted remote version;
- locally cached remote state;
- provenance/home Space;
- release-channel information.

A newly available upstream Module Release should not automatically rewrite the Mirror's adopted target.

Instead, the Mirror or associated reference machinery may record availability and participate in UpdateCandidate evaluation.

The exact Mirror/Module integration remains to be specified.

---

# 67. What This Design Does Not Yet Decide

The following remain open and should be surfaced explicitly rather than silently assumed.

## 67.1 Exclusive Module Membership

Can one immutable HolonVersion be included in multiple Modules or Module Releases?

Possible models:

- exactly one governing Module;
- one primary Module plus aggregate Modules;
- arbitrary inclusion in multiple release packages.

The current design does not require a final answer.

## 67.2 Nested Module Semantics

If Modules nest:

- does the child independently release?
- does the parent bind to a child release?
- may the parent contain working child state?
- does parent release require all child Modules to have released states?

Needs specification.

## 67.3 Release Branching

Can Module release lineage branch?

If yes, consumers may follow channels or lines of release.

Do not assume linear semantic versioning prematurely.

## 67.4 Semantic Version Labels

Whether Module Releases use semantic versions such as `2.3.1`, opaque version IDs, hashes, sequence IDs, or some combination remains open.

Deterministic immutable identity is required; human-facing semantic labeling is separable.

## 67.5 Module Surface

It is not yet decided whether every released HolonVersion is externally discoverable or whether Modules expose explicit public exports.

## 67.6 Workspace Representation

It remains open whether `ModuleWorkspace` is itself a persisted HolonType or is represented through existing staged/Nursery state.

## 67.7 Inverse Storage Representation

The design requires release-gated inverse visibility but does not yet prescribe whether inverse state is:

- stored links;
- derived query results;
- relationship Holons;
- indexes;
- projections;
- cached affordances.

This must respect existing Holochain/link constraints and MAP relationship design.

## 67.8 Same-Space Publication Optimization

Cross-Module publication within one Space may be implemented more cheaply than cross-Space publication, but should preserve equivalent semantics.

## 67.9 Release Events

How release availability is signaled may use:

- event subscription;
- Stewardship Anchor observation;
- release indexes;
- polling;
- cache policy mechanisms;
- or another distributed notification mechanism.

The semantic requirement is more important than the transport mechanism.

---

# 68. Required Spec Updates

Codex should inspect the current specifications and identify every area impacted by introducing Modules.

At minimum evaluate updates to:

- Holon version lifecycle;
- commit semantics;
- staged/Nursery state;
- relationship creation;
- relationship cloning during version creation;
- inverse relationship propagation;
- relationship persistence;
- cross-Space references;
- proxy/Mirror behavior;
- Stewardship Anchors;
- release/version semantics;
- caching and `Release` refresh policy;
- query semantics for inverse relationships;
- historical versus current-head projections;
- descriptor-aware validation;
- Space containment rules;
- discovery hierarchy if Modules become discoverable;
- DAHN/Space Navigator behavior if Modules become navigable;
- TrustChannel/agreement checks for published assertions;
- loader behavior if Module membership is loadable;
- schema bootstrap if new core types are introduced.

Search current main before deciding which files actually require changes.

---

# 69. Required Implementation-Plan Analysis

Codex should produce an implementation plan that identifies:

1. Existing code paths where relationship inverses are currently created or propagated.
2. Existing code paths where new HolonVersions clone declared relationships.
3. Current distinction, if any, between local commit and externally visible state.
4. Existing Stewardship Anchor implementation and semantics.
5. Existing release/version concepts that can be reused.
6. Current Space containment representation.
7. How to determine Module membership efficiently from a HolonVersion.
8. How a release manifest should be represented or derived.
9. How release validation should work.
10. How release publication should be staged.
11. How external inverse assertions should be generated.
12. How publication should be made idempotent.
13. How partial publication failures should recover.
14. How historical inverse navigation differs from released-head navigation.
15. How consumers discover successor Module Releases.
16. How UpdateCandidates or equivalent pending-adoption state should be represented.
17. How adoption flows create new local versions without mutating released state.
18. How nested Modules would affect the initial implementation.
19. Which pieces belong in the first vertical slice versus later extensions.

---

# 70. Suggested First Vertical Slice

Avoid implementing every possible Module capability at once.

A useful first vertical slice may be:

1. Introduce a minimal `Module` concept.
2. Allow exact HolonVersions to be associated with a Module release boundary.
3. Distinguish committed/unreleased HolonVersions from released HolonVersions.
4. Introduce immutable `ModuleRelease`.
5. Bind one ModuleRelease to exact HolonVersions.
6. Prevent cross-boundary inverse publication for unreleased Module state.
7. On Module release, publish inverses only for HolonVersions included in that release.
8. Ensure intermediate working versions never become externally visible.
9. Preserve existing ordinary relationship syntax.
10. Preserve exact target-version binding.
11. Add release lineage sufficient to discover a successor ModuleRelease.
12. Demonstrate that discovering a successor does not automatically update a consumer relationship.

Defer unless already required:

- nested Modules;
- Module exports;
- semantic versioning;
- sophisticated release channels;
- branching release histories;
- automatic adoption policies;
- rich Module UI;
- generalized package registries.

---

# 71. Essential Tests

The implementation plan should include tests corresponding to the semantic invariants.

At minimum:

## Test A — Working Version Does Not Publish Inverse

Given:

    A1 released
    A1 -> B1
    inverse visible from B1

When:

    A2 is created from A1 inside Module Workspace

Then:

    A2 -> B1 exists locally

But:

    inverse B1 -> A2 is not externally published

## Test B — Multiple Intermediate Versions Remain Private

Given successive local committed versions:

    A2
    A3
    A4

Then no released inverse visibility exists for any of them.

## Test C — Released Head Publishes

When:

    A5 is included in Module Release R2

Then:

    A5 -> B1

becomes externally publishable and its declared inverse becomes externally navigable according to policy.

## Test D — Historical Released Versions Remain Addressable

After R2:

    A1
    A5

remain immutable released versions.

Historical inverse query can identify both where appropriate.

## Test E — Current-Head Projection

A released-head inverse query can select `A5` rather than exposing all intermediate/historical versions by default.

## Test F — Publication Does Not Update Consumer

Given:

    X -> A1

When:

    A5 is released

Then:

    X -> A1

remains unchanged.

## Test G — Successor Availability

After release of `A5`, a consumer following the governing Stewardship Anchor can discover `A5` as an available successor.

## Test H — Adoption Creates New Version

When the consumer adopts `A5`, the system creates new local versioned state rather than modifying an already released version containing `X -> A1`.

## Test I — Packaging Does Not Reidentify Holon

Given existing immutable `Y1`:

When `Y1` is included in Module M Release R1:

Then `Y1` does not require a replacement version merely because of Module inclusion.

## Test J — Relationship Syntax Unchanged

Existing relationship identity to `Y1` remains valid after `Y1` is packaged into a Module.

## Test K — Same-Space Cross-Module Suppression

Unreleased changes in Module A must not become visible to Module B merely because both share one Space.

## Test L — Release Publication Idempotency

Publishing the same immutable ModuleRelease more than once produces no duplicate semantic effects.

---

# 72. Design Direction Summary

The working architectural direction is:

> Introduce Module as a sub-Space unit of coordinated development and release.

> Keep ordinary Holon identity independent of Module packaging.

> Keep ordinary relationship syntax independent of Module boundaries.

> Treat Module Release membership as a property of the containing release, not an intrinsic mutation of each HolonVersion.

> Separate local commit from external publication.

> Stop treating cross-boundary inverse propagation as an unconditional commit-time side effect.

> Publish boundary-crossing relationship assertions only from released state.

> Never publish intermediate working versions that were not selected for release.

> Treat inverses as derived visibility of authoritative forward assertions rather than proof that the target's authoritative Holon state was mutated.

> Separate semantic relationship publication from successor-release notification.

> Use Stewardship Anchors / release lineage for successor discovery.

> Preserve pull-based adoption: availability never silently changes existing bindings.

> Require released dependencies to bind deterministically to exact immutable versions.

> Allow Module Releases to become the unit through which coherent change propagates asynchronously across the MAP.

---

# 73. Codex Task

Using this design as the architectural source of truth:

1. Inspect the current MAP ontology, specs, validation rules, versioning model, relationship commit/inverse behavior, Stewardship Anchor implementation, and relevant roadmap/implementation plans.
2. Identify where current documentation or implementation assumptions conflict with this Module model.
3. Propose the smallest coherent schema changes needed to introduce Modules.
4. Update specifications to clearly distinguish:
    - commit;
    - Module working state;
    - Module release;
    - publication;
    - successor availability;
    - adoption.
5. Replace any assumption that external inverse propagation necessarily occurs at ordinary Holon commit with release-aware semantics.
6. Preserve existing relationship identity and syntax unless a concrete requirement demonstrates otherwise.
7. Define the required invariants and validation rules.
8. Define release publication and failure/idempotency semantics.
9. Produce an implementation plan that prioritizes the smallest vertical slice proving:
    - private Module evolution;
    - coordinated release;
    - release-time inverse publication;
    - suppression of intermediate versions;
    - successor discovery;
    - and explicit downstream adoption.
10. Clearly mark open design questions rather than silently resolving them.
11. Reuse existing MAP concepts wherever they already provide the required semantics instead of creating parallel abstractions.
12. Keep the implementation aligned with MAP's broader principles:
- one authoritative home Space per Holon;
- immutable version identity;
- deterministic released dependency bindings;
- pull over push;
- autonomy-preserving adoption;
- descriptor-aware semantics;
- nested belonging;
- and asynchronous coordination rather than global synchronization.