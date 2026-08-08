# Schema 2.0 Design Rationale and Comparison

## 1. Document Role

This document records the design pressures and decisions that produced MAP Schema 2.0. It is
retained for comparison with the earlier model; it is not a second normative semantic
specification.

Current authority is divided as follows:

- [Schema Design Spec](schema-design-spec.md): structural schema model and invariants;
- [Descriptor-Kernel Semantic Rules](descriptor-semantics-rules.md): formal definitions,
  effective products, stable validation rules, and conformance;
- [TDL Specification](tdl/tdl-spec.md): concrete syntax, omission, and lowering;
- `map-holons/schema-src`: exact declared identities, inventories, values, and current Instance
  TypeKind anchors; and
- delegated runtime and validation documents: construction, completion, invocation, and
  persistence behavior.

Where historical language in this discussion differs from those authorities, the current
authority wins.

## 2. Problems Schema 2.0 Had to Solve

### 2.1 A type descriptor plays two roles

A type descriptor is itself a holon, but it also defines semantics for other instances. Earlier
designs blurred those roles and made it difficult to tell whether an inherited declaration applied
to the descriptor holon or to the instances described by it.

Schema 2.0 separates the two axes:

```text
Type as holon:      L(D(T))  -> specification T must conform to
Type as classifier: L(T)     -> specification T imposes on its instances
```

`DescribedBy` connects the axes without flattening them. A descriptor conforms through its
describing type while classifying and specializing through its own `Extends` lineage.

### 2.2 Instance contracts were too easily confused with descriptor state

`InstanceProperties` and `InstanceRelationships` declare which properties and relationships
instances may or must populate. They do not represent those occurrences populated on the type
descriptor itself.

Schema 2.0 therefore uses **instance contract** narrowly for the property-and-relationship portion
of a type's effective specification. The broader effective specification also includes, where
applicable, Instance TypeKind, key-rule selection, Commands, Dances, Operators, constraints, and
other inherited descriptor semantics.

### 2.3 `Extends` had accumulated several incompatible meanings

Earlier explanations sometimes treated `Extends` as if it always inherited contract declarations
additively while treating other populated values through a separate mechanism. This made
inheritance behavior depend on the semantic name of a member.

Schema 2.0 instead makes propagation strictly descriptor-driven. `Extends` supplies the lineage;
each populated property or relationship follows the `InheritanceMode` of its own member
descriptor. The Core Schema declares `InstanceProperties`, `InstanceRelationships`,
`AffordsCommand`, `AffordsDance`, and `AffordsOperator` `Additive`, so contract declarations and
behavioral affordances accumulate. The kernel does not special-case any of these relationships.

### 2.4 Authored `TypeKind` flattened two different questions

The old `TypeKind` vocabulary mixed:

- what kind of descriptor holon a type definition is; and
- what kind of instances that type definition describes.

It also encouraged declaration forms, Rust enums, and authored category fields to compete with the
schema graph as classification authority.

Schema 2.0 now answers those questions separately:

- a **meta-type** says what a type definition must look like; and
- an **Instance TypeKind anchor** says what kind of instances that type defines.

### 2.5 Defaults and omission were conflated

Omission in TDL or JSON is source state, not runtime fallback semantics. Reading an omitted required
property through its descriptor on every access would leave the representation implicit and make
later schema changes retroactive.

Schema 2.0 makes defaults creation-time declarations. A workflow that accepts omission as
selection of a default materializes that value before validation. The descriptor kernel validates
explicit state and never injects defaults.

## 3. Resulting Mental Model

### 3.1 Three independent relationships

```text
H --DescribedBy--> T   conformance: which specification governs H
T --Extends-----> P    specialization: classification and semantic lineage
T --Instances---> H    inverse discovery of DescribedBy
```

Every holon has exactly one compatible concrete `DescribedBy` target. Every holon has at most one
direct `Extends` parent; descriptor lineages are acyclic and terminate at `TypeDescriptor`.
`Instances` supports inverse traversal but does not independently define conformance.

### 3.2 One descriptor hierarchy

All descriptors participate in one `Extends` hierarchy rooted at abstract `TypeDescriptor`.
`MetaTypeDescriptor.HolonType` is a descendant of `HolonType.TypeDescriptor`, so meta-types are
holon types as well as descriptors. `RelationshipType.TypeDescriptor` is the common parent of the
declared and inverse relationship categories.

A holon is a descriptor because `TypeDescriptor` appears in its own lineage, not because of a flag,
key suffix, declaration form, or Rust wrapper.

### 3.3 Meta-types and Instance TypeKind anchors

Meta-types define the effective specifications that descriptor holons must conform to. For example,
`MetaPropertyType.MetaTypeDescriptor` describes property descriptors, while
`MetaDanceType.MetaHolonType` describes Dance type descriptors.

The required Boolean property `DefinesInstanceTypeKind` explicitly marks Instance TypeKind
anchors. It has default `false` and `InheritanceMode None`, so designation is local rather than an
inherited Boolean fact. The nearest designated anchor in a descriptor's self-first lineage is its
Instance TypeKind.

Anchors are abstract. `TypeDescriptor` defines no Instance TypeKind; every other descriptor
resolves one nearest anchor. A specialized anchor may extend another anchor. Dance, Command, and
Operator therefore define specialized kinds of holon rather than unrelated storage
representations.

The root-level design is summarized here:

![MAP Core Schema Root 2.0.svg](../media/MAP%20Core%20Schema%20Root%202.0.svg)

The TDL corpus owns the exact anchor list and declarations.

### 3.4 Graph-defined meta-type pairing

A descriptor's two axes cannot vary independently. The nearest Instance TypeKind anchor identifies
the expected meta-type category through the anchor's own `DescribedBy` target. A property
descriptor must therefore be described by the meta-type paired with the Property anchor; a Dance
descriptor must be described by the meta-type paired with the Dance anchor.

This rejects both kinds of mismatch:

```text
MyBook
  DescribedBy MapString.ValueType            # value types do not describe holons

Title.PropertyType
  DescribedBy Book.HolonType                 # descriptor requires a meta-type

Title.PropertyType
  DescribedBy MetaHolonType.MetaTypeDescriptor  # wrong paired meta-type
```

An extension schema can add a new Instance TypeKind and paired meta-type through authored graph
relationships without adding a hard-coded kernel category.

### 3.5 Self-description is ordinary conformance

Core Schema 2.0 authors `MetaHolonType.MetaTypeDescriptor` as self-describing. This is not a hidden
bootstrap exemption or a unique-cycle semantic:

```text
MetaHolonType.MetaTypeDescriptor
  DescribedBy MetaHolonType.MetaTypeDescriptor
```

Any descriptor may be self-describing when it satisfies the same compatibility and conformance
rules as every other descriptor. No semantic rule follows `DescribedBy` transitively or requires
all describing chains to converge on one reflective root.

Evaluation terminates by computing and memoizing effective products before validating conformance.
A self-describing descriptor selects its already computed effective specification; validation does
not recursively invoke itself.

### 3.6 Effective specifications and instance contracts

A type's effective specification is resolved across its own lineage and may include:

- its Instance TypeKind;
- its instance property and relationship contract;
- its effective key rule for holon instances;
- inherited Commands, Dances, and Operators;
- constraints and member definitions; and
- other descriptor members whose `InheritanceMode` makes them effective.

The instance contract is the narrower set of effective `InstanceProperties` and
`InstanceRelationships`. Contract members are identified by resolved descriptor identity. Their
compact names derive from required local `TypeName` values and occupy separate property and
relationship namespaces.

Property values and relationship occurrences are not self-describing holons. Their governing
descriptors are found through the source holon's effective instance contract.

### 3.7 Effective member semantics

Every populated descriptor member follows one of three modes:

- `None`: only local values contribute;
- `Additive`: effective ancestor contributions precede local contributions; or
- `Override`: the nearest locally populated contribution set wins.

Collection policy determines whether the result is a set, multiset, deduplicated sequence, or
sequence. Cardinality applies to that final effective collection. Effective member definitions,
including value type, requiredness, defaults, endpoints, cardinality, ordering, duplicates,
deletion semantics, and constraints, are themselves resolved across the member descriptor's own
lineage.

These algorithms and their validation rule IDs belong to the Descriptor-Kernel Semantic Rules.

### 3.8 Endpoints use both classifications

An ordinary holon may satisfy an endpoint through the lineage of its describing type. A descriptor
holon may also satisfy an endpoint through its own lineage. This is why an ordinary book can satisfy
an endpoint requiring `Book.HolonType`, while `Title.PropertyType` can satisfy one requiring
`PropertyType.TypeDescriptor`.

No alternate `EffectiveEndpointType` object or hard-coded descriptor branch is needed.

### 3.9 Abstract descriptors use member-specific completeness

Abstract descriptors classify and contribute semantics but do not directly describe runtime
instances. Abstractness is not a blanket conformance exemption. Universally required members remain
required; only a member explicitly treated as concrete-only may relax its minimum. Every supplied
value is validated normally.

This allows abstract `PropertyType.TypeDescriptor` to omit a concrete value type without allowing
it to omit structural requirements or populate an invalid value.

### 3.10 Keys and defaults remain explicit state

Holon types select an effective `InstanceKeyRule`; explicit `NoneRule.KeyRuleType` represents
keylessness. Descriptor holons use the key rule selected by their describing meta-type. The retired
`TypeKindRule.KeyRuleType` is not part of Schema 2.0.

A persisted key is historical explicit state and is not recomputed because a later schema changes
a key rule, input, or ancestor.

Defaults are valid only for required properties. A creation workflow that accepts omission as
selection of a default materializes the effective value before validation. Explicit values win,
optional omissions remain absent, and later default changes do not alter existing holons. The
current automatic materialization service is scoped to Holon Loading.

## 4. Before and After

| Concern | Earlier direction | Schema 2.0 result |
|---|---|---|
| Descriptor conformance | Mixed with specialization | Selected only through `D(T)` and `L(D(T))` |
| Described-instance semantics | Often called a contract in the broad sense | Effective specification, with instance contract as one part |
| Descriptor classification | Declaration form, name, or authored `TypeKind` could participate | Descriptor identity and transitive `Extends` |
| Instance representation kind | Flattened into authored `TypeKind` | Nearest explicit `DefinesInstanceTypeKind` anchor |
| Meta-type selection | Kind-specific rules risked hard-coded tables | Paired through the anchor's own `DescribedBy` target |
| Contract inheritance | Separate always-additive algorithm | Ordinary `InheritanceMode Additive` on the two contract relationships |
| Behavior affordance inheritance | Implicit or member-specific behavior | Ordinary `InheritanceMode Additive` on Command, Dance, and Operator affordance relationships |
| Other semantic inheritance | Set-oriented special cases | Policy-aware collections under `None`, `Additive`, or `Override` |
| Endpoint classification | One synthetic effective endpoint type | Uniform compatibility through `L(D(H))` or `L(H)` |
| Self-description | Unique reflective-root cycle and convergence | Ordinary compatibility and conformance; no transitive `DescribedBy` semantic |
| Abstract completeness | Broad exemption or universal-baseline heuristic | Member-specific minimum enforcement |
| Defaults | Read-time fallback or parser-owned insertion | Explicit creation-time materialization outside the kernel |
| Semantic representation | Potential separate semantic IR | Existing holonic representation and `HolonDescriptor` operations |

### 4.1 Topology Migration

Earlier schema diagrams placed descriptor categories and their corresponding meta-types in the
same `Extends` path, for example by making `HolonType` extend `MetaHolonType`. Schema 2.0 does not
preserve that topology. Descriptor categories now classify in the unified hierarchy rooted at
`TypeDescriptor`; concrete meta-types govern descriptor-holon conformance through `DescribedBy`.
The two diagrams therefore express different models and must not be reconciled as alternate views
of one graph.

Migration also replaces the former `UsesKeyRule` vocabulary with `InstanceKeyRule` and authors
directional `DeletionSemantic` values on both declared and inverse relationship descriptors. Old
diagrams, generated projections, and external schema catalogs must be treated as pre-2.0 until
those relationships and the new topology are reflected explicitly.

## 5. Corpus and Implementation Consequences

Alignment of the Schema 2.0 TDL source to this model requires:

- `MetaTypeDescriptor.HolonType` includes `DefinesInstanceTypeKind.PropertyType`;
- the property is Boolean, required, defaults to `false`, and uses `InheritanceMode None`;
- the intended abstract anchors author local `true` values;
- legacy `TypeKind.PropertyType`, `TypeKind.MapEnumValueType`, and
  `TypeKindRule.KeyRuleType` are removed; and
- declaration forms remain syntactic conveniences and do not infer anchors or category state.

Generated JSON remains downstream of the TDL source. It should be regenerated only through the
compiler once the parser accepts the current corpus; it is not hand-edited into semantic authority.

Runtime work must derive any retained `TypeKind` projection from the resolved anchor identity,
implement the four descriptor-kernel jobs through `HolonDescriptor` and existing reference-layer
operations, and keep descriptor-aware Holon Validation separate from descriptor-independent PVL.

## 6. Deliberately Deferred Questions

Schema 2.0 does not settle:

- Extension Schema identity qualification, compatibility, and evolution;
- pairwise inverse deletion execution, cascade termination, and cycle handling;
- a persisted effective-descriptor representation;
- universal use of default materialization outside Holon Loading; or
- migration of persisted Schema 1.2 descriptors and legacy runtime category state.

Those questions may consume this model but must not redefine its classifications or semantic
boundaries.

## 7. Summary

Schema 2.0 reduces the model to two axes over one graph. `L(D(T))` determines what a type descriptor
must conform to as a holon; `L(T)` determines what it imposes on its own instances. Meta-types define
type-definition shape. Explicit Instance TypeKind anchors define the kind of described instances.
Every inherited semantic follows descriptor data, and defaults become explicit before validation.

The concise structural statement belongs in the Schema Design Spec. The exact algorithms and rule
IDs belong in the Descriptor-Kernel Semantic Rules. This document preserves why those choices were
made.
