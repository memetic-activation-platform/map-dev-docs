# MAP Type Definition Semantics (v2.0)
*(Bootstrap Installation Mode · TypeDefinitionMode · Structural Doctrine · Version Impact)*

## ChangeLog

### v2.0

- aligns type-definition semantics with the MAP Type System v2.0 meta-schema model
- replaces the former `TypeDescriptor` / `MetaTypeDescriptor` recursion assumptions with `DescriptorRoot`, TypeKind-specific meta-types, abstract type anchors, and concrete type descriptors
- distinguishes descriptor description via `DescribedBy` from inheritance via `Extends`
- clarifies that only stabilized concrete type descriptors may describe ordinary runtime holons
- preserves the rule that `Extends` is always acyclic, single-inheritance, additive, and monotonic

This section defines the normative semantics of type definition in MAP.  
It covers:

- Bootstrap Installation Mode (system genesis)
- TypeDefinitionMode (normal transactional schema authoring)
- Structural doctrine
- Version-impacting relationships
- Descriptor usage constraints

Type definition is categorically distinct from type resolution and from instance-level mutation.

---

# 1. Bootstrap Installation Mode
*(Core Ontology Genesis)*

Bootstrap Installation Mode governs the installation of the foundational MAP ontology, including:

- `DescriptorRoot`
- TypeKind-specific meta-types such as `MetaHolonType`, `MetaPropertyType`, `MetaValueType`, and `MetaRelationshipType`
- Abstract type descriptors such as `HolonType`, `PropertyType`, `ValueType`, `DeclaredRelationshipType`, and `InverseRelationshipType`
- Concrete core type descriptors such as `Schema.HolonType`, `Description.Property`, and `MapStringValueType`
- Core relationship types (e.g., Extends, DescribedBy, InstanceProperties, etc.)

## 1.1 Purpose

MAP is self-describing. Its core ontology contains legitimate dependency cycles across relationships such as:

- DescribedBy
- SourceType
- TargetType
- InstanceProperties

Because of these cross-role dependencies:

The core ontology cannot be constructed via strictly sequential descriptor definition.

Bootstrap Installation Mode exists to allow atomic installation of this mutually referential ontology.

---

## 1.2 Dependency Cycles vs Extends Cycles

### Dependency Cycles (Permitted During Bootstrap)

Mutual references across meta-relationships are allowed during bootstrap.

Examples:
- An abstract descriptor such as `HolonType` being described by `MetaHolonType`
- A concrete descriptor such as `Schema.HolonType` being described by `MetaHolonType` and extending `HolonType`
- Relationship types referencing abstract type anchors such as `HolonType`, `PropertyType`, `ValueType`, or `DescriptorRoot`

These cycles are required for ontology-as-data architecture.

---

### Extends Cycles (Always Forbidden)

The Extends graph MUST be acyclic at all times, including during bootstrap.

If any Extends cycle exists:
- Bootstrap MUST fail.
- The system MUST NOT enter normal operation.

Dependency cycles are permitted.  
Inheritance cycles are never permitted.

---

## 1.3 Relaxation of Rule D0 During Bootstrap

During bootstrap:

- `DescriptorRoot` MAY be installed with its special root semantics: no `DescribedBy`, no `Extends`, and no instances.
- Type descriptors MAY reference each other freely.
- Descriptors MAY be used before the full graph is complete.
- Rule D0 (No In-Transaction Descriptor Usage) does NOT apply.

Bootstrap operates under privileged initialization authority and is not transactional schema authoring.

---

## 1.4 Post-Bootstrap Structural Validation

Before entering normal operation, the system MUST:

1. Validate Extends acyclicity.
2. Resolve all descriptors and their `DescribedBy`, `Extends`, and definitional relationship targets.
3. Enforce all structural conflict rules.
4. Ensure all references are resolvable.

If any descriptor fails resolution:
- Bootstrap MUST fail.
- The system MUST NOT proceed.

After successful validation:
- Bootstrap concludes.
- Normal transactional semantics begin.
- Rule D0 becomes active.

---

# 2. TypeDefinitionMode
*(Normal Transactional Schema Authoring)*

TypeDefinitionMode governs all schema mutations occurring within a TransactionContext after bootstrap.

---

## 2.1 Scope of TypeDefinitionMode

Type-definition operations include:

- Creating a type descriptor
- Assigning or changing descriptor `DescribedBy` relationships
- Adding/removing Extends
- Adding/removing InstanceProperties
- Adding/removing InstanceRelationships
- Creating holon, property, value, or relationship type descriptors
- Modifying definitional relationships (SourceType, TargetType, etc.)

All such mutations occur within a Transaction.

---

## 2.2 Structural Doctrine (Normative)

Inheritance in MAP is:

- Additive
- Monotonic
- Conflict-intolerant
- Deterministic
- Order-insensitive

Extends means:

Accumulate structural obligations.

`Extends` is only the inheritance axis. It does not replace `DescribedBy`, and it does not imply `Instances`.

MAP does NOT support:

- Overrides
- Precedence rules
- Shadowing
- Linearization
- Multiple inheritance

If accumulation produces ambiguity, the transaction MUST fail.

---

## 2.3 Rule D0 — No In-Transaction Descriptor Usage

If a type descriptor is created or structurally modified within a transaction:

It MUST NOT be used as a DescribedBy target within that same transaction.

Schema stabilization precedes schema usage.

Only stabilized concrete type descriptors may describe ordinary runtime holons.
Abstract type descriptors and `DescriptorRoot` are never valid `DescribedBy` targets for ordinary runtime instances.

This rule ensures:

- No reliance on partially stabilized schema.
- No transactional resolution overlays.
- Deterministic runtime semantics.

---

## 2.4 Definitional vs Instance Relationships

Relationship types are categorized as:

- Definitional
- Instance

### Definitional Relationships

These alter structural meaning and affect semantic identity.

Examples:
- Extends
- InstanceProperties
- InstanceRelationships
- SourceType
- TargetType
- DescribedBy (for descriptors)
- ComponentOf
- UsesKeyRule

Definitional relationships:
- Affect resolution
- Affect semantic versioning
- Are not expandable in normal algebra mode

### Instance Relationships

These represent domain-level associations.

Examples:
- OWNS
- AuthorOf
- LIKES

Instance relationships:
- Do not affect resolution
- Do not affect semantic identity
- Are expandable in execution algebra

Relationship type descriptors may use abstract descriptors as `SourceType` and `TargetType` anchors.
Validation remains based on type conformance: the source and target holons must be described by concrete descriptors that are equal to, or extend, the relationship's declared source and target anchors.

---

## 2.5 Semantic Versioning Rule

For any holon H:

If a definitional relationship (H)-[R]->(T) is added or removed:

- H MUST be staged as a new semantic version.
- Predecessor MUST be set to prior version.

If a non-definitional relationship is added or removed:

- No semantic version bump occurs.

This aligns structural identity with version chains.

---

## 2.6 Local Emergent Schema (I-Space)

Local schema evolution is supported via multi-transaction choreography:

1. Schema transaction (commit descriptor changes)
2. Data transaction (apply instance changes)

Post-commit undo compensates data only, not schema.

Schema cleanup must occur via explicit maintenance operations.

---

# 3. Summary of Type Definition

Bootstrap:
- Allows dependency cycles
- Forbids Extends cycles
- Temporarily relaxes Rule D0
- Requires post-install validation
- Installs `DescriptorRoot` using its special root semantics

TypeDefinitionMode:
- Enforces structural doctrine
- Enforces Rule D0
- Enforces version-impacting definitional relationships
- Maintains monotonic semantic evolution
