# Evolution of Life in MAP
### Application Evolution, We-Space Transformation, and Commitment-Preserving Membranes

Just as the “Origin of Life in MAP” describes how identity, membranes, and the CoreSchema emerge in the first place, this document describes how life *evolves* within the MAP ecosystem.

Evolution in MAP occurs not only at the planetary schema level, but also through:

- the creation and refinement of new agents,
- the evolution of mApps (MAP Applications),
- the controlled evolution of We-Spaces through agreements,
- the stewardship processes that govern mApp development, and
- the policies that determine how and when new behaviors become active.

MAP is intentionally patterned after biological organisms:  
open-ended, adaptive, extensible, and self-organizing — yet guided by membranes that maintain identity and protect integrity.

This document explains how evolution happens safely, coherently, and consensually in MAP.

---

# 1. The Evolutionary Landscape in MAP

Within a single MAP CoreSchema version, evolution occurs in three primary places:

1. **Agent-Level Evolution**  
   Each agent’s I-Space evolves as it installs, updates, or removes mApps.

2. **mApp Evolution in Their Stewardship Spaces**  
   Applications are independently stewarded, versioned, and released — much like biological lineages.

3. **We-Space Evolution Through Agreement Evolution**  
   Each We-Space is defined by an Agreement that establishes its behavioral membrane.  
   As mApps evolve, the Agreement may evolve with them.

This mirrors biological evolution:

- Variation (new versions, new dances, new descriptors)
- Selection (adoption or rejection by We-Spaces)
- Continuity (life-code promises and membrane constraints)

MAP preserves both flexibility and integrity by anchoring evolution in **explicit, policy-driven Agreements**.

---

# 2. Stewardship Spaces as Repositories
### The Git-Like Evolution Model for mApps

Every mApp is stewarded by a **Stewardship Space** — the home space of all canonical descriptor holons that define that application.

This behaves like a **git origin repository**, containing:

- TypeDescriptors
- DanceDescriptors
- RelationshipDescriptors
- Protocol and Policy descriptors
- Release (version-tag) holons

The Stewardship Space is the source of truth for:  
*what the app is, how it behaves, and how it evolves.*

---

## 2.1. Developers Work in Their I-Spaces (Local Clones)

To modify or extend an mApp:

1. A developer imports the app’s descriptors as **HolonReferences** into their I-Space.
2. Any descriptor they modify becomes a **new descriptor holon** in their I-Space.
3. They test and simulate changes locally, in a private workspace.

This is the holonic equivalent of a **local git clone**.  
It allows experimentation without affecting global state.

---

## 2.2. Feature We-Spaces as Shared Branches

For collaborative work, developers create **Feature We-Spaces**, analogous to shared git branches.

These spaces:

- contain Agreements defining their purpose,
- reference the same starting descriptors,
- allow multiple contributors to push/pull changes,
- function as integration and review environments.

This provides a clean workflow:

> I-Space (local) ↔ Feature We-Space (shared branch) ↔ Stewardship Space (origin)

---

## 2.3. Pull Requests as Dances

When a change is ready for review:

- A **PullRequest dance** is sent to the Stewardship Space.
- It contains references to modified descriptors, base versions, and metadata.
- Automated structural merges run.
- Any semantic conflicts generate **MergeConflict holons**.

Crucially:

- Conflicts are **never hidden**.
- Humans resolve what automated merging cannot.
- All results are explicit and preserved in the version graph.

This mirrors the best aspects of git, but with holonic semantics and human-centered conflict resolution.

---

## 2.4. Releases as Version Tags

Stewardship Spaces publish **Release holons**, each bundling a coherent set of descriptor versions and assigning a semantic version number.

Releases:

- define stable integration points,
- serve as the basis for Agreement dependency declarations,
- reflect deliberate governance decisions about readiness and maturity.

Apps can evolve freely, but *nothing is pushed onto adopters*.

---

# 3. Agreements as Behavioral Membranes

A **We-Space** is a social organism instantiated by an Agreement that defines:

- its members,
- its roles,
- its permitted dances,
- its information access policies,
- its commitments (life-code promises),
- and its dependent mApps.

An Agreement is a **membrane**:  
it defines what happens *inside* the We-Space, what is *allowed*, and how members interact.

Crucially:

> An Agreement defines not only the current state of a We-Space,  
> but how it is allowed to *evolve* over time.

This is where MAP’s biological-patterned design shines.

---

# 4. Versioning and the Membrane
### Why Agreements Do Not Pin Exact mApp Versions

In early formulations, we tied Agreements tightly to specific mApp versions.  
This proved too rigid.

Instead:

- Agreements specify **version ranges**, not exact versions.
- They include **upgrade policies** that determine which new releases are allowable.
- They separate the *current selected versions* (lockfile) from the *policy* (semantic or reputation-based constraints).

This dramatically increases flexibility while preserving membrane integrity.

---

# 5. Release Adoption & Agreement Evolution Policies
### How We-Spaces Safely Evolve With New mApp Versions

We-Spaces do not auto-upgrade by default.  
Instead, each Agreement’s policy determines how and when new mApp releases are adopted.

MAP distinguishes **three categories of evolution**.

---

## 5.1 Automatic Evolution (Safe Drift)

Allowed when:

- changes are backward compatible
- patch-level or minor release
- no breaking changes
- no altered life-code commitments
- no expanded information access obligations

The Agreement specifies something like:

```
upgrade_policy: AutomaticFor(Patch | Minor)
```

The new release is adopted automatically.  
The lockfile updates.  
The membrane’s integrity remains intact.

---

## 5.2 Semi-Automatic Evolution (Attended Drift)

Changes may require:

- notification
- human review
- maturity thresholds
- adoption criteria (e.g. reputation or ecosystem usage)

Examples:

- minor behavior modifications
- schema updates introducing new required fields
- dances that alter default workflows

Agreements may specify:

```
upgrade_policy:
  - Minor: NotifyThenAutoAfter(7 days)
  - Patch: Auto
```

These policies allow We-Spaces to evolve without excessive ceremony.

---

## 5.3 Explicit Evolution (Membrane Transformation)

Some changes require a **new Agreement**:

- major version bumps
- removed or altered core dances
- expanded access rules or privacy changes
- altered roles or governance
- changes to life-code promises

All members must explicitly accept before the new Agreement activates.

If even one party declines:

- the old Agreement remains in force,
- the proposed Agreement becomes an alternative or fork.

This models **speciation** in biological systems.

---

# 6. Evolution Without Coercion
### No Agent Is Ever Forced to Upgrade

MAP adheres to a strict principle:

> All change is *pulled* by sovereign agents; none is pushed.

This means:

- mApps evolve freely in their Stewardship Spaces
- We-Spaces adopt new releases according to their own rules
- Agents remain sovereign
- Agreements remain stable
- Evolution becomes flexible, safe, and self-determined

No lockstep upgrades.  
No forced migrations.  
No central authority dictating evolution.

This is essential for a planetary-scale, agent-centric ecosystem.

---

# 7. Cross-Version Interoperability
### Transitional We-Spaces and Dual-Participation

When some members upgrade and others do not:

- the new Agreement remains in “proposed” state,
- but the old Agreement continues to mediate interactions,
- agents who upgrade may participate in *both* Agreement versions,
- transitional We-Spaces (bridging spaces) can be used to interact across version boundaries.

This supports:

- gradual adoption
- non-disruptive migration
- long-tail support for older versions
- safe interoperability across evolutionary boundaries

MAP treats Agreement versions as *coexisting membranes*, not destructive replacements.

---

# 8. Summary: Life Evolves, Membranes Protect

Evolution in MAP is not a bolt-on feature.  
It is a primary design principle.

MAP promotes:

- **continuous variation** (new mApp versions)
- **sovereign selection** (upgrade policies)
- **commitment continuity** (membrane constraints)
- **collaborative development** (stewardship spaces as repos)
- **safe adoption** (agreement evolution)
- **non-disruptive migration** (cross-version interoperability)

MAP is neither centralized nor static.  
It is a living ecosystem, patterned after biology,  
where change is continuous but never coerced,  
and where membranes preserve integrity while allowing creative evolution.

This is the **Evolution of Life in MAP**.