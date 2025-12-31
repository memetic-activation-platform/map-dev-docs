# MAP Command Transport Specification (Partitioned Query / Mutation Model)

**Status:** Proposed (updated)  
**Scope:** Privileged TypeScript ↔ Rust client interface via Conductora  
**Intent:** Provide a clean, type-safe command model that supports authorization, undo/redo, and extensibility without introducing full CQRS complexity.

---

## 1. Overview

All privileged interactions between the TypeScript client and the Rust client are funneled through a **single command channel** exposed by Conductora via Tauri.

This specification introduces a **type-level partition** of commands into:

- **Queries** — read-only, replay-safe
- **Mutations** — state-changing, undoable

This is **not** a full CQRS architecture:
- There is a single execution pipeline.
- A unified state model is preserved.
- Partitioning exists solely to make intent explicit and enforceable.

---

## 2. Top-Level Transport Objects

### 2.1 MapRequest

`MapRequest` represents one privileged MAP command invocation.

```
pub struct MapRequest {
    /// Stable dispatch key within Conductora
    pub name: String,

    /// The command being executed (query or mutation)
    pub body: CommandBody,

    /// Execution context
    pub space: HolonSpace,
}
```

**Notes**
- `name` is for routing, logging, and observability.
- All semantic intent lives in `CommandBody`.

---

### 2.2 MapResponse

Uniform envelope for all command results.

```
pub struct MapResponse {
    /// Whether execution completed successfully
    pub success: bool,

    /// Command-specific response payload
    pub body: Option<CommandResponse>,

    /// Zero or more errors or warnings
    pub errors: Vec<HolonError>,
}
```

**Notes**
- No HTTP semantics.
- Errors may accompany successful responses.
- Partial success is allowed.

---

## 3. CommandBody (Partitioned by Intent)

`CommandBody` is owned by **MAP Core / Conductora**, not the Dances layer.

```
pub enum CommandBody {
    Query(QueryCommand),
    Mutation(MutationCommand),
}
```

This partition is the primary leverage point for:
- authorization
- undo/redo stacking
- caching and replay rules

---

## 4. Query Commands (Read-Only)

Queries are guaranteed to:
- not mutate state (including nursery/transient),
- be safe to replay,
- never participate in undo/redo.

### 4.1 QueryCommand

```
pub enum QueryCommand {
    Holon(HolonQuery),
    Operations(OperationsQuery),
}
```

---

### 4.2 HolonQuery (ReadableHolon)

Object-scoped queries serialize method calls on a holon reference.

```
pub struct HolonQuery {
    pub target: HolonReference,
    pub action: HolonQueryAction,
}
```

```
pub enum HolonQueryAction {
    CloneHolon,
    EssentialContent,
    HolonId,
    Predecessor,
    Key,
    VersionedKey,
    AllRelatedHolons,

    GetPropertyValue {
        property: PropertyName,
    },

    GetRelatedHolons {
        relationship: RelationshipName,
    },
}
```

---

### 4.3 OperationsQuery (Read-Only Operations)

```
pub enum OperationsQuery {
    GetAll,
    Summarize,
    StagedCount,
    TransientCount,
}
```

---

## 5. Mutation Commands (State-Changing)

Mutations may:
- change nursery or transient state,
- allocate new references,
- affect commit outcomes.

They are:
- undoable,
- authorization-sensitive,
- never cached or replayed blindly.

### 5.1 MutationCommand

```
pub enum MutationCommand {
    Holon(HolonMutation),
    Operations(OperationsMutation),
    ExecuteDance(ExecuteDanceCommand),
}
```

---

### 5.2 HolonMutation (WritableHolon)

```
pub struct HolonMutation {
    pub target: HolonReference,
    pub action: HolonMutationAction,
}
```

```
pub enum HolonMutationAction {
    AddRelatedHolons {
        relationship: RelationshipName,
        holons: Vec<HolonReference>,
    },

    RemoveRelatedHolons {
        relationship: RelationshipName,
        holons: Vec<HolonReference>,
    },

    WithPropertyValue {
        property: PropertyName,
        value: BaseValue,
    },

    RemovePropertyValue {
        property: PropertyName,
    },

    WithPredecessor {
        predecessor: Option<HolonReference>,
    },

    WithDescriptor {
        descriptor: HolonReference,
    },
}
```

---

### 5.3 OperationsMutation (HolonOperations)

```
pub enum OperationsMutation {
    NewHolon {
        key: String,
    },

    DeleteHolon {
        target: HolonReference,
    },

    StageNewHolon {
        type_name: TypeName,
        properties: PropertyMap,
    },

    StageNewVersion {
        source: HolonReference,
        properties: PropertyMap,
    },

    StageFromClone {
        source: HolonReference,
    },

    Commit,
}
```

---

### 5.4 ExecuteDanceCommand (Extensibility)

Dances are treated as **mutation commands by default**.

```
pub struct ExecuteDanceCommand {
    pub dance_name: String,
    pub request: DanceRequestBody,
}
```

**Notes**
- `DanceRequestBody` is owned by the Dances layer.
- TrustChannels are not involved at this boundary.
- Query dances may be introduced later via explicit declaration.

---

## 6. CommandResponse

`CommandResponse` provides structured, typed results.

```
pub enum CommandResponse {

    /* ---------- Holon Queries ---------- */

    HolonReference {
        reference: HolonReference,
    },

    EssentialHolonContent {
        content: EssentialHolonContent,
    },

    PropertyValue {
        value: Option<BaseValue>,
    },

    RelationshipMap {
        relationships: RelationshipMap,
    },

    HolonCollection {
        members: Vec<HolonReference>,
    },

    StringValue {
        value: Option<String>,
    },

    /* ---------- Operations Queries ---------- */

    Summary {
        summary: SummarizeResponse,
    },

    Count {
        count: usize,
    },

    HolonReferenceList {
        holons: Vec<HolonReference>,
    },

    /* ---------- Mutations ---------- */

    CommitResult {
        committed: usize,
    },

    /* ---------- Dance ---------- */

    DanceResult {
        response: DanceResponseBody,
    },
}
```

**Notes**
- Some commands return no body (`body = None`).
- Response shape is structural, not reflective.

---

## 7. Undo / Redo Semantics

- Only `CommandBody::Mutation` is eligible for undo/redo.
- Each mutation may emit an internal undo record.
- Queries are never recorded.

This requires no heuristics — intent is explicit.

---

## 8. Authorization Semantics

Authorization may be applied at multiple levels:

- Query vs Mutation
- Holon vs Operations vs ExecuteDance
- Specific action variants

Because intent is structural, policy is declarative.

---

## 9. Design Guarantees

This model ensures:

- **Single transport channel**
- **Explicit intent**
- **Object-oriented semantics preserved**
- **Extensibility without core pollution**
- **No accidental state mutation**
- **No premature CQRS complexity**

---

## 10. Summary

This partitioned command model:

- keeps MAP Core clean and inspectable,
- aligns perfectly with the TypeScript SDK façade,
- gives Conductora a powerful leverage point,
- and future-proofs undo, auth, and extensibility.

It reflects the architecture MAP has already grown into — now expressed clearly and safely in the type system.