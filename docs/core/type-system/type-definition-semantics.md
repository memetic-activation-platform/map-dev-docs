# MAP Type Definition Semantics
*(Bootstrap Installation Mode · TypeDefinitionMode · Structural Doctrine · Version Impact)*

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

- TypeDescriptor
- Meta-types
- Abstract types
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
- A type described by TypeDescriptor
- TypeDescriptor extending HolonType
- Relationship types referencing abstract types

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

- TypeDescriptors MAY reference each other freely.
- Descriptors MAY be used before the full graph is complete.
- Rule D0 (No In-Transaction Descriptor Usage) does NOT apply.

Bootstrap operates under privileged initialization authority and is not transactional schema authoring.

---

## 1.4 Post-Bootstrap Structural Validation

Before entering normal operation, the system MUST:

1. Validate Extends acyclicity.
2. Resolve all TypeDescriptors.
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

- Creating a TypeDescriptor
- Adding/removing Extends
- Adding/removing InstanceProperties
- Adding/removing InstanceRelationships
- Creating PropertyType or RelationshipType descriptors
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

MAP does NOT support:

- Overrides
- Precedence rules
- Shadowing
- Linearization

If accumulation produces ambiguity, the transaction MUST fail.

---

## 2.3 Rule D0 — No In-Transaction Descriptor Usage

If a TypeDescriptor is created or structurally modified within a transaction:

It MUST NOT be used as a DescribedBy target within that same transaction.

Schema stabilization precedes schema usage.

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

TypeDefinitionMode:
- Enforces structural doctrine
- Enforces Rule D0
- Enforces version-impacting definitional relationships
- Maintains monotonic semantic evolution