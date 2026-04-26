# MAP Execution-Time Type Resolution v1.1
*(Schema-Driven · Ontology-as-Data · Deterministic · Cached)*

This section defines the normative execution-time semantics of type resolution in MAP.

Type resolution compiles a committed `TypeDescriptor` holon into a deterministic structural contract called `ResolvedType`.

Resolution is:

- Fully derived from the meta-schema
- Deterministic
- Conflict-intolerant
- Immutable
- Cached in the TypeRegistry

No Rust enums duplicate ontology concepts.
All structural behavior is derived from committed schema holons.

Descriptor synthesis note:

- this document now describes an execution-time structural projection layer, not the final semantic home of runtime structure
- descriptor wrappers should increasingly be the caller-facing semantic surface
- any `ResolvedType`-like cache should support descriptor-backed lookup rather than compete with it

---

# 1. Semantic Reference Types

```rust
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, HashMap, HashSet};
use std::sync::Arc;

#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct TypeDescriptorReference(pub HolonReference);

#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct PropertyTypeReference(pub HolonReference);

#[derive(Clone, Debug, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct RelationshipTypeReference(pub HolonReference);
```

These are semantic wrappers over `HolonReference`.
They encode no ontology rules.

---

# 2. ResolvedType

`ResolvedType` is the flattened structural contract of a committed descriptor.

In v1.1, it should be interpreted as an execution aid rather than as the primary semantic facade.

```rust
#[derive(Clone, Debug)]
pub struct ResolvedType {
    /// The descriptor being resolved
    pub descriptor: TypeDescriptorReference,

    /// All transitive parents via Extends (excluding descriptor)
    pub extends_closure: HashSet<TypeDescriptorReference>,

    /// Flattened property contract
    pub effective_property_types: BTreeMap<PropertyName, PropertyTypeReference>,

    /// Flattened instance-level relationship contract
    ///
    /// Derived via:
    /// (HolonType)-[SourceOf]->(DeclaredRelationshipType)
    ///
    /// Excludes:
    /// - Relationships where IsDefinitional = true
    /// - InverseRelationshipTypes
    pub effective_relationship_types: HashMap<RelationshipName, RelationshipTypeReference>,
}
```

---

# 3. TypeRegistry Runtime Cache

Resolution results are cached per descriptor version.

```rust
#[derive(Default)]
pub struct TypeRegistry {
    pub resolved_types: HashMap<TypeDescriptorReference, Arc<ResolvedType>>,
}

impl TypeRegistry {
    pub fn get_or_resolve(
        &mut self,
        descriptor: TypeDescriptorReference,
        resolve: impl FnOnce(&TypeDescriptorReference) -> Result<ResolvedType, HolonError>,
    ) -> Result<Arc<ResolvedType>, HolonError> {
        if let Some(existing) = self.resolved_types.get(&descriptor) {
            return Ok(existing.clone());
        }

        let resolved = Arc::new(resolve(&descriptor)?);
        self.resolved_types.insert(descriptor, resolved.clone());
        Ok(resolved)
    }
}
```

Resolution is:

- Per committed descriptor version
- Immutable
- O(1) lookup after first resolution

Caller-facing rule in v1.1:

- query, validation, and SDK consumers should prefer descriptor-facing APIs
- caches like `ResolvedType` should remain internal runtime support structures where possible

---

# 4. Extends Closure

Resolution begins by computing the transitive closure of `Extends`.

Rules:

- Leaf descriptor is NOT included in closure
- Extends graph MUST be acyclic
- Any cycle causes resolution failure

```rust
pub fn compute_extends_closure(
    load: impl Fn(&TypeDescriptorReference) -> Result<TypeDescriptorView, HolonError>,
    descriptor: &TypeDescriptorReference,
) -> Result<HashSet<TypeDescriptorReference>, HolonError> {
    let mut closure = HashSet::new();
    let mut stack = load(descriptor)?.extends;

    while let Some(parent) = stack.pop() {
        if closure.insert(parent.clone()) {
            let view = load(&parent)?;
            for p in view.extends {
                if p == *descriptor {
                    return Err(HolonError::schema_invalid("Extends cycle detected"));
                }
                stack.push(p);
            }
        }
    }

    Ok(closure)
}
```

---

# 5. Effective Property Resolution

Properties are accumulated from:

1. All descriptors in `extends_closure`
2. Then the leaf descriptor

Structural enforcement:

- No conflicting PropertyType versions with same structural key
- No duplicate `PropertyName` with different identities

```rust
pub fn accumulate_effective_properties(
    types: impl IntoIterator<Item = TypeDescriptorView>,
) -> Result<BTreeMap<PropertyName, PropertyTypeReference>, HolonError> {
    let mut by_structural_key = HashMap::new();
    let mut by_name = BTreeMap::new();

    for td in types {
        for p in td.instance_properties {
            let structural_key = p.structural_key();

            if let Some(existing) = by_structural_key.get(&structural_key) {
                if existing != &p.reference {
                    return Err(HolonError::schema_invalid(
                        "Conflicting PropertyType versions",
                    ));
                }
            } else {
                by_structural_key.insert(structural_key, p.reference.clone());
            }

            if let Some(existing) = by_name.get(&p.property_name) {
                if existing != &p.reference {
                    return Err(HolonError::schema_invalid(
                        "Duplicate PropertyName with different identities",
                    ));
                }
            } else {
                by_name.insert(p.property_name.clone(), p.reference.clone());
            }
        }
    }

    Ok(by_name)
}
```

---

# 6. Effective Instance Relationship Resolution

Relationships included in `effective_relationship_types` are derived exclusively from the meta-schema.

For a resolved descriptor `D`:

1. Let `T ∈ {D} ∪ extends_closure`
2. For each `T`, retrieve:

   T.get_related_holons("SourceOf")

3. Each returned holon is a `DeclaredRelationshipType` for which `T` participates as SourceType.
4. Exclude any relationship descriptor where:

   IsDefinitional = true

InverseRelationshipTypes are never included because:

- They are not reachable via `SourceOf` from `HolonType`

No manual SourceType conformance logic is required.
The schema already encodes source eligibility.

```rust
pub fn accumulate_effective_instance_relationships(
    descriptor: &TypeDescriptorReference,
    closure: &HashSet<TypeDescriptorReference>,
    get_source_of: impl Fn(&TypeDescriptorReference) -> Result<Vec<RelationshipTypeReference>, HolonError>,
    load_relationship: impl Fn(&RelationshipTypeReference) -> Result<RelationshipTypeView, HolonError>,
) -> Result<HashMap<RelationshipName, RelationshipTypeReference>, HolonError> {

    let mut by_structural_key = HashMap::new();
    let mut by_name = HashMap::new();

    let mut all_types = closure.clone();
    all_types.insert(descriptor.clone());

    for t in all_types {
        let relationships = get_source_of(&t)?;

        for r_ref in relationships {
            let r = load_relationship(&r_ref)?;

            // Exclude definitional relationships
            if r.has_property("IsDefinitional", true) {
                continue;
            }

            let structural_key = r.structural_key();

            if let Some(existing) = by_structural_key.get(&structural_key) {
                if existing != &r.reference {
                    return Err(HolonError::schema_invalid(
                        "Conflicting RelationshipType versions",
                    ));
                }
            } else {
                by_structural_key.insert(structural_key, r.reference.clone());
            }

            if let Some(existing) = by_name.get(&r.relationship_name) {
                if existing != &r.reference {
                    return Err(HolonError::schema_invalid(
                        "Duplicate RelationshipName with different identities",
                    ));
                }
            } else {
                by_name.insert(r.relationship_name.clone(), r.reference.clone());
            }
        }
    }

    Ok(by_name)
}
```

Resolution logic contains:

- No hardcoded relationship categories
- No manual SourceType checks
- No Declared vs Inverse enums
- No ontology duplication

Everything is derived from:

- Extends
- SourceOf
- IsDefinitional

---

# 7. Execution Algebra Interaction

Given:

Expand { from_variable, relationship, direction }

Validation rules:

- Outgoing expansion:
    - relationship MUST exist in effective_relationship_types

- Incoming expansion:
    - relationship.inverse MUST exist in effective_relationship_types

Inverse descriptors are derived via HasInverse.
They are not duplicated in ResolvedType.

---

# 8. Deterministic Guarantees

For any committed descriptor successfully resolved:

- Extends graph is acyclic
- Property contract is conflict-free
- Instance relationship contract is conflict-free
- Definitional relationships are excluded from adjacency
- Inheritance is fully flattened
- Runtime inheritance traversal is eliminated

Resolution produces a deterministic, immutable structural contract suitable for:

- Instance validation
- Query planning
- ExecutionPlan validation
- Runtime enforcement
- Introspection

MAP inheritance accumulates structure.
