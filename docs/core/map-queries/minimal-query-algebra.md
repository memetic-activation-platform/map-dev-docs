# Minimal Execution Algebra Plan for MAP Core
*(Human-First DAHN Navigation → Cypher-Ready Foundation)*

This plan defines the smallest execution algebra that can subsume:

- Current MAP imperative operations
- A powerful subset of Cypher
- Future extensibility toward declarative query compilation

It incorporates:

- Transaction-scoped execution
- Flattened `ResolvedType` runtime projection
- Strict separation of structure vs state
- Semantic newtypes for descriptor references
- No query optimization (yet)

---

## Step 1 — Stabilize the Three-Layer Architecture

Before introducing algebra, explicitly formalize three runtime layers:

### 1. Ontology Layer (Persistent, Holonic)
- `TypeDescriptor`
- `Extends`
- `InstanceProperties`
- `InstanceRelationships`
- All schema semantics remain declarative

### 2. Runtime Structural Layer (Ephemeral Projection)
Introduce immutable:

```
ResolvedType {
    descriptor: TypeDescriptorRef,
    extends_closure: HashSet<TypeDescriptorRef>,
    effective_property_types: BTreeMap<PropertyName, PropertyTypeRef>,
    effective_relationship_types: HashMap<RelationshipName, RelationshipTypeRef>,
}
```

Properties:
- Built once per descriptor load
- Cached in `HolonSpaceManager`
- Immutable
- Not persisted
- Not exposed over IPC

### 3. Instance State Layer (Transaction-Scoped)
Unchanged:
- `PropertyMap`
- `RelationshipMap`
- Undo-aware
- Mutable

This separation prevents structural/state leakage and simplifies execution.

---

## Step 2 — Introduce Semantic Newtypes

Define thin wrappers over `HolonReference`:

- `TypeDescriptorRef`
- `PropertyTypeRef`
- `RelationshipTypeRef`
- (Optional) `InstanceHolonRef`

Purpose:
- Compile-time role distinction
- Safer algebra implementation
- Cleaner API signatures
- Future Cypher compilation alignment

Avoid excessive newtypes — focus only on semantic boundaries.

---

## Step 3 — Define the Minimal Operand Set

Introduce only three execution operands:

### 1. Value

```
enum Value {
    Scalar(BaseValue),
    Holon(InstanceHolonRef),
    List(Vec<Value>),
    Null,
}
```

No new scalar types introduced.

---

### 2. Row

```
struct Row {
    bindings: BTreeMap<VariableName, Value>
}
```

Rows are:
- In-memory only
- Transaction-scoped
- Not persisted
- Not IPC-visible

---

### 3. RowSet

```
type RowSet = Vec<Row>;
```

Materialized for now.
Streaming later if needed.

No additional operand types.

---

## Step 4 — Define the Minimal Expression AST

Keep expressions small and structural:

- `Var(name)`
- `Literal(Value)`
- `Property(var, PropertyName)`
- `Eq`, `Neq`, `Gt`, `Gte`, `Lt`, `Lte`
- `And`, `Or`, `Not`
- `ConformsTo(var, TypeDescriptorRef)`
- `Exists(Property(...))`
- Optional: `StartsWith`, `Contains`, `In`

Key detail:

`ConformsTo` checks membership in `extends_closure`.

No recursive descriptor walking during execution.

---

## Step 5 — Define the Minimal PlanStep Set

Implement a linear pipeline (no tree optimization yet):

- `SeedSpace { as }`
- `SeedHolon { ref, as }`
- `Expand { from, rel: RelationshipName, dir, to, bind_rel? }`
- `Filter { predicate }`
- `Project { items }`
- `Distinct`
- `OrderBy`
- `Skip`
- `Limit`

Optional (later but easy):
- `OptionalExpand`
- `Union`

This already supports a powerful Cypher subset.

---

## Step 6 — Use OWNS as Canonical Root Scan

Human “search” begins with:

1. `SeedSpace`
2. `Expand (space)-[:OWNS]->(h)`
3. `Filter ConformsTo(h, T)`
4. `Filter property predicates`
5. `Limit`
6. `Project`

This models:

```
MATCH (h:T)
WHERE ...
RETURN ...
```

without introducing label primitives.

Type filtering uses `extends_closure`.

---

## Step 7 — Make Interactive Query Building Append-Only

Represent interactive navigation as:

```
struct ExecutionPlan {
    steps: Vec<PlanStep>
}
```

Each user gesture appends:

- Search → Filter
- Navigate → Expand
- Refine → Filter
- Shape → Project

The plan remains:
- Serializable
- Replayable
- Persistable as a holon
- Versionable

No optimization required.

---

## Step 8 — Integrate with Command Envelope

Add a new command variant:

```
QueryCommand::ExecutePlan { plan }
```

Execution guarantees:
- Transaction-relative
- Read-only
- No undo participation
- No IPC leakage of execution internals

Existing imperative mutation commands remain unchanged.

Future:
- Mutating plans can become a unified algebra surface.

---

## Step 9 — Enforce Structural Validation via ResolvedType

All validation checks become constant-time:

### Type filtering
```
resolved_type.extends_closure.contains(T)
```

### Property mutation validation
```
resolved_type.effective_property_types.contains_key(name)
```

### Relationship mutation validation
```
resolved_type.effective_relationship_types.contains_key(rel)
```

No runtime inheritance traversal.
No descriptor walking.
No recursive validation.

---

## Step 10 — Prepare for Future Cypher Compilation

This minimal algebra already supports:

- MATCH
- WHERE
- RETURN
- Basic pattern chaining
- Typed relationship navigation
- Property filtering
- Pagination

When ready, an OpenCypher compiler can:

1. Parse declarative syntax
2. Produce `ExecutionPlan`
3. (Later) Apply plan rewrites for optimization
4. Execute via the same interpreter

No operand redesign required.

No structural changes to MAP Core required.

Optimization becomes an execution concern, not a semantic redesign.

---

# Final Architectural Summary

This plan achieves:

- Human-first interactive navigation
- Minimal algebraic surface
- Strict separation of ontology vs execution
- Multi-label semantics via `extends_closure`
- Structural flattening of properties and relationships
- Future Cypher compatibility
- No premature optimization

The system evolves from:

Imperative API Calls  
→ Transaction-Scoped Algebra Interpreter  
→ Declarative Cypher Compilation Target

Without changing the core ontology or persistence model.

This is the smallest stable execution algebra that subsumes:

- Current MAP operations
- A meaningful Cypher subset
- Long-term extensibility

And it does so without introducing new operand categories or destabilizing MAP’s holonic architecture.