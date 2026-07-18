# Three Levels of Evolution

## 1. Staging

Changes exist only within a Nursery (transaction or working state).

Properties, relationships, and even multiple holons may be freely created, modified, removed, and reconsidered.

Characteristics:

- private
- fluid
- reversible
- collaborative if desired
- no lineage extension
- no DHT persistence
- no external visibility

Purpose:

Explore and refine a coherent set of changes before committing them.

---

## 2. Publish (Commit)

The staged changes are committed.

New immutable versions are created for every affected holon and persisted into the steward's HolonSpace.

This extends the lineage of individual holons.

Characteristics:

- immutable
- versioned
- persisted
- externally referenceable
- extends lineages
- does **not** imply adoption by dependents

Purpose:

Record the evolution of individual knowledge artifacts.

Publishing answers the question:

> "What is the current state of this particular holon?"

It does **not** answer:

> "What should everyone else adopt?"

---

## 3. Release

A release is an explicit statement by the steward that a coherent collection of published versions should now be considered together as an adoptable unit.

A release is itself a versioned holon.

Its definitional relationships pin the exact versions that comprise the release.

Characteristics:

- coherent
- intentionally curated
- suitable for adoption
- compatibility assessed
- impact documented
- stable reference point

Purpose:

Coordinate adoption.

A release answers the question:

> "What collection of changes is recommended to be adopted together?"

Dependent holons evaluate releases—not individual commits—when deciding whether to evolve.

---

# Why the distinction matters

Individual holons often evolve at different rates.

Many intermediate commits represent work in progress, experimentation, discussion, clarification, or refinement.

Publishing those versions preserves history and enables collaboration, but it should not create pressure for every dependent to continually evaluate whether they should update.

Releases establish meaningful synchronization points.

They reduce administrative burden by allowing dependents to evaluate one coherent proposal rather than a stream of fine-grained changes.

---

# Relationship to Pull-Based Evolution

The pull model naturally operates at the release level.

Stewards may publish many intermediate versions while refining a knowledge artifact.

Only when a release is created do dependents have a meaningful candidate for adoption.

Adoption remains explicit.

Publishing extends the steward's lineage.

Releasing proposes a coherent state.

Pulling creates a new version of the dependent that adopts that released state.

Nothing is ever pushed into an existing version.