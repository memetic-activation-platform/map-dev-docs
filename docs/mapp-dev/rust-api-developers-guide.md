# MAP Rust-API Developer Guide

The **reference layer** is the boundary between your application code and the underlying holon store and services. It provides:

* **Uniform handles (“references”) to holons**, regardless of whether they are transient, staged, or cached/saved.
* A **small, consistent read/write API** that hides internal manager and phase differences.
* High-level **operations** for staging, committing, and deleting.
* A **curated prelude** for ergonomic imports and a stable public API.

This guide explains the API surface and shows how to perform the most common tasks.

---

## 1. Prelude

To simplify imports, use the MAP prelude:

```rust
use holons_prelude::prelude::*;
```

This brings into scope:

* Core value and identifier types (`BaseValue`, `MapString`, `HolonId`)
* Reference traits and types (`HolonReference`, `ReadableHolon`, `WritableHolon`, `TransientReference`, `StagedReference`, `SmartReference`)
* Context traits (`HolonsContextBehavior`)
* Common operations (`stage_new_holon_api`, `commit_api`, etc.)
* Type-name helpers (`CorePropertyTypeName`, `CoreRelationshipTypeName`, `ToPropertyName`, `ToRelationshipName`)
* Dance protocol builders (`holon_dance_builders::*`)
* Query types (`Node`, `NodeCollection`, `QueryExpression`)

> Use `holons_prelude::prelude::v1::*` if you need to pin to a stable prelude version.

---

## 2. Context: your execution environment

Every holon operation in MAP runs within a **context** that implements the `HolonsContextBehavior` trait. This context is the execution environment for all read, write, and commit actions—it provides access to the active workspace where your holons live.

As a developer, you don’t create or manage the context yourself. Your mApp receives it from the runtime whenever you perform operations that touch holons.  
You simply pass it along to each API call that needs it.

Example — staging and committing a holon:

```rust
fn create_and_commit(
    context: &dyn HolonsContextBehavior,
) -> Result<(), HolonError> {
    // Create a new transient holon of a given type
    let transient = create_empty_transient_holon(context, MapString("ExampleType".into()));
    transient.with_property_value(context, P::Key, "example-1".into())?;

    // Stage it for persistence
    let staged = stage_new_holon_api(context, transient)?;

    // Commit all staged changes
    let response = commit_api(context)?;
    println!("Committed {} holons.", response.commits_attempted);

    Ok(())
}
```

### Key points for developers

* The **context** is always the first parameter to any read or write call.  
  It carries all the state needed to resolve references, access relationships, and enforce permissions.

* You can think of it as your “session” or “workspace.”  
  Everything that happens during a transaction—reads, writes, staging, commits—occurs *within* this context.

* The context automatically routes requests to the right implementation based on the holon’s phase (transient, staged, or saved).  
  You never need to know which storage or cache layer is involved.

* Contexts are lightweight and short-lived.  
  They are passed around as immutable references (`&dyn HolonsContextBehavior`), so you can safely use them in async or concurrent flows.

In short: **the context is your gateway to the MAP**.  
You use it everywhere, but you don’t manage or configure it—just pass it through to the reference-layer API.

---

## 3. Reference Kinds

`HolonReference` is the umbrella type that can represent any phase:

* **`TransientReference`** — in-memory, mutable, not persisted.
* **`StagedReference`** — managed and ready to commit.
* **`SmartReference`** — read-only, backed by a saved holon in cache or storage.

All three implement the `ReadableHolon` trait; transient and staged also implement `WritableHolon`.

| Type                 | Backing store | Read | Write | Commit |
| -------------------- | --------------| ---- | ----- | ------- |
| `TransientReference` | In-memory | ✅ | ✅ | ❌ (must stage) |
| `StagedReference` | Staging area | ✅ | ✅ | ✅ |
| `SmartReference` | Saved/cache | ✅ | ❌ | ❌ |

---

## 4. Collections

A `HolonCollection` represents an **ordered set of holon references**.  Collections are most commonly returned when traversing relationships—especially many-to-many or one-to-many links between holons. For example, a `Project` holon might have a `HasTask` relationship that returns a `HolonCollection` of `Task` holons.

### Example: Reading related holons

```rust
let tasks = project_ref.related_holons(context, R::HasTask.as_relationship_name())?;
for task_ref in tasks.iter() {
    let title = task_ref.property_value(context, &P::Title)?;
    println!("Task: {:?}", title);
}
```

### Key capabilities

#### 1. Access and iteration

`HolonCollection` behaves like a lightweight, reference-aware vector:

```rust
let count = tasks.len();
let first = tasks.first();
let by_index = tasks.get(2);
let all = tasks.to_vec(); // Clones references into a Vec<HolonReference>
```

You can iterate directly:

```rust
for holon_ref in &tasks {
    println!("{:?}", holon_ref.key(context)?);
}
```

#### 2. Membership and lookup

```rust
if tasks.contains(&some_ref) {
    println!("Already linked!");
}
```

If the collection is keyed (e.g., by `MapString`), you can look up by key:

```rust
if let Some(found) = tasks.get_by_key(&MapString("task-42".into())) {
    println!("Found task 42: {:?}", found.key(context)?);
}
```

#### 3. Mutation (transient and staged only)

Collections tied to writable holons can be updated via the `HolonCollectionApi` trait.  
These operations automatically update both the in-memory collection and the relationship map on the parent holon.

```rust
// Add a new related holon
tasks.add(context, HolonReference::Transient(new_task_ref))?;

// Remove an existing related holon
tasks.remove(context, HolonReference::Smart(old_task_ref))?;
```

Behind the scenes, this uses the same logic as calling:
```rust
parent_ref.add_related_holons(context, R::HasTask.as_relationship_name(), vec![child_ref])?;
```

#### 4. Access control and phase safety

* Read-only collections (from `SmartReference`) cannot be mutated.
* Transient and staged collections support add/remove operations.
* Attempting to mutate a read-only collection returns `HolonError::NotAccessible`.

#### 5. Use cases

* **Navigation:** traverse relationships, fetch related holons, inspect their properties.
* **Editing:** attach or detach related holons while editing staged or transient instances.
* **Synchronization:** check if a relationship set has changed before committing.

---

### Summary

| Operation | Available on | Description |
|------------|--------------|--------------|
| `iter()` | All | Iterate through member references |
| `len()` / `is_empty()` | All | Get collection size |
| `get(index)` / `get_by_key()` | All | Access by position or key |
| `add()` / `remove()` | Transient, Staged | Modify collection membership |
| `contains()` | All | Check membership |
| `to_vec()` | All | Convert to owned vector |

---

In short:  
**HolonCollection** gives you a simple, phase-safe way to traverse and manipulate sets of related holons, just like a Rust `Vec`, but with built-in access control and automatic relationship synchronization.

---

## 5. Read API (all reference types)

Every `HolonReference` implements `ReadableHolon`. That means **the same read calls work** on `TransientReference`, `StagedReference`, and `SmartReference` alike. Reads are phase-safe and route through the active `HolonsContextBehavior`.

### Core calls

```rust
let key_opt      = reference.key(context)?;                               // Option<MapString>
let vkey         = reference.versioned_key(context)?;                     // Versioned key (type+key+rev/epoch)
let title_opt    = reference.property_value(context, &P::Title)?;         // Option<PropertyValue>
let children     = reference.related_holons(context, R::HasChild.as_relationship_name())?; // HolonCollection
```

Other useful calls:
- `all_related_holons(context)` – returns a map of **all** relationship names → `HolonCollection`
- `holon_id(context)` – low-level persistent identifier (when applicable)
- `predecessor(context)` – previous version (if any)
- `essential_content(context)` – minimal content needed to reconstruct the holon
- `into_model(context)` – materialize a snapshot model (e.g., for serialization or UI presentation)

---

### Ergonomic usage patterns

#### 1) Keys and versioned keys
Use `key()` where present (some holons may be keyless) and fall back gracefully:

```rust
let label = reference
    .key(context)?
    .map(|k| format!("key: {}", k.0))
    .unwrap_or_else(|| "keyless".to_string());

let vkey = reference.versioned_key(context)?; // Stable for logs, audit, and idempotency
```

#### 2) Properties with defaults
`property_value` returns `Option<PropertyValue>`. Provide sensible defaults at the edge:

```rust
let title = reference
    .property_value(context, &P::Title)?
    .and_then(|v| v.as_string())                // Convert if your ValueType is String-like
    .unwrap_or_else(|| "Untitled".to_string());
```

> Tip: keep **type conversion at the edge** (e.g., UI layer). Treat raw `PropertyValue` as data until you must render or compute.

#### 3) Navigating relationships
Use relationship constants for clarity and refactor safety:

```rust
let children = reference.related_holons(context, R::HasChild.as_relationship_name())?;
for child in children.iter() {
    let ck = child.key(context)?;
    let ct = child.property_value(context, &P::Title)?.and_then(|v| v.as_string());
    println!("child {:?} titled {:?}", ck, ct);
}
```

Fetch all relationships when you need to render a full card/graph:

```rust
let relmap = reference.all_related_holons(context)?;
for (rel_name, collection) in relmap.iter() {
    println!("{}: {} linked holons", rel_name, collection.len());
}
```

#### 4) Lineage-aware reads
When building edit screens for saved holons:

```rust
if let Some(prev) = reference.predecessor(context)? {
    println!("has predecessor with key {:?}", prev.key(context)?);
}
```

#### 5) Snapshotting for UI/persistence
Prefer `into_model` for immutable snapshots passed to views or serialization:

```rust
let model = reference.into_model(context)?;
// pass `model` to your presentation layer or serializer
```

---

### Applicability (access rules)

- **Read is allowed on all phases**: Transient ✅, Staged ✅, Smart ✅.
- Access control is automatically enforced; if a read is not permitted **you’ll get an error** (see below).
- The same method set works across phases, so you can write one code path for all references.

> You never need to detect the phase to read. Call the method; the context routes it correctly.

---

### Error behavior you should expect here

All reads return `Result<_, HolonError>`. Common cases for this section:

- `HolonError::NotAccessible` — read not permitted for the current state of this holon
- `HolonError::InvalidHolonReference` — reference cannot be resolved (e.g., missing, malformed, or out-of-scope).
- `HolonError::InvalidType` / `HolonError::UnexpectedValueType` — property exists but the value type doesn’t match your expectation.
- `HolonError::EmptyField` — property required by your logic is unset.

> The guide’s **Error Handling** section enumerates all variants and recommended remedies. In read paths, prefer **graceful fallbacks** and **edge validation** (e.g., default titles, optional render elements).

---

### Practical examples

**Read a title with a default and render children count**
```rust
fn render_card(
    context: &dyn HolonsContextBehavior,
    item: &HolonReference,
) -> Result<(), HolonError> {
    let title = item.property_value(context, &P::Title)?
        .and_then(|v| v.as_string())
        .unwrap_or_else(|| "Untitled".to_string());

    let kids = item.related_holons(context, R::HasChild.as_relationship_name())?;
    println!("{} ({} items)", title, kids.len());
    Ok(())
}
```

**Collect all related holons for a relationship-aware widget**
```rust
fn gather_relationships(
    context: &dyn HolonsContextBehavior,
    item: &HolonReference,
) -> Result<Vec<(RelationshipName, Vec<HolonReference>)>, HolonError> {
    let mut out = Vec::new();
    for (rel_name, coll) in item.all_related_holons(context)? {
        out.push((rel_name.clone(), coll.to_vec()));
    }
    Ok(out)
}
```

---

### Summary table

| Method | Returns | Notes |
|---|---|---|
| `key(context)` | `Result<Option<MapString>, HolonError>` | Keyless holons return `None`. |
| `versioned_key(context)` | `Result<VersionedKey, HolonError>` | Stable identifier for logs/audits. |
| `property_value(context, &P::X)` | `Result<Option<PropertyValue>, HolonError>` | Convert at the edge (`as_string()`, etc.). |
| `related_holons(context, R::X)` | `Result<HolonCollection, HolonError>` | Ordered, phase-safe collection. |
| `all_related_holons(context)` | `Result<BTreeMap<RelationshipName, HolonCollection>, HolonError>` | Full relationship map. |
| `holon_id(context)` | `Result<HolonId, HolonError>` | May be unavailable for purely transient holons. |
| `predecessor(context)` | `Result<Option<HolonReference>, HolonError>` | Present on versioned/saved lineages. |
| `essential_content(context)` | `Result<EssentialHolonContent, HolonError>` | Minimal reconstruction payload. |
| `into_model(context)` | `Result<HolonNodeModel, HolonError>` | Immutable snapshot for UI/serialization. |

**Takeaways**
- One trait, all phases: **write once, read anywhere**.
- Treat properties as optional until rendered; **fail soft** at the edge.
- Use relationship constants for clarity and stability.

## 6. Write API (transient/staged only)

Available via `WritableHolon`:

```rust
reference.with_property_value(context, P::Title, "Hello".into())?;
reference.remove_property_value(context, P::Obsolete)?;
reference.add_related_holons(context, R::HasChild.as_relationship_name(), vec![child_ref])?;
reference.remove_related_holons(context, R::HasChild.as_relationship_name(), vec![child_ref])?;
reference.with_descriptor(context, descriptor_ref)?;
reference.with_predecessor(context, Some(prev_ref))?;
```

---

## 7. Staging and Commit

High-level helpers in `holon_operations_api`:

* **Stage a new holon**
  ```rust
  let staged = stage_new_holon_api(context, transient)?;
  ```
* **Stage a new version** of a saved holon
  ```rust
  let staged = stage_new_version(context, smart_ref)?;
  ```
* **Commit all staged changes**
  ```rust
  let commit_response = commit_api(context)?;
  ```

`CommitResponse` includes:
* `saved_holons`
* `abandoned_holons`
* `commits_attempted`

`(saved + abandoned == attempted)` indicates completion.

---

## 8. Cloning holons

MAP offers three public clone operations, depending on your intent.

### A. `ReadableHolon::clone_holon` → `TransientReference`

```rust
fn clone_holon(
    &self,
    context: &dyn HolonsContextBehavior,
) -> Result<TransientReference, HolonError>
```

Any holon—saved, staged, or transient—can be cloned.  
The result is always a **new transient holon**, detached from lineage or staging metadata but preserving its property and relationship data.

Use this for creating a **scratch copy**:

```rust
let transient_clone = any_reference.clone_holon(context)?;
transient_clone.with_property_value(context, P::Title, "Draft copy".into())?;
```

---

### B. `stage_new_version` → `StagedReference`

```rust
fn stage_new_version(
    context: &dyn HolonsContextBehavior,
    current_version: SmartReference,
) -> Result<StagedReference, HolonError>
```

Creates a **new staged holon** as an update to an existing saved holon, retaining lineage through the `Predecessor` relationship.

```rust
let staged = stage_new_version(context, saved_ref)?;
staged.with_property_value(context, P::Status, "Revised".into())?;
```

---

### C. `stage_new_from_clone` → `StagedReference`

```rust
fn stage_new_from_clone(
    context: &dyn HolonsContextBehavior,
    original_holon: HolonReference,
    new_key: MapString,
) -> Result<StagedReference, HolonError>
```

Creates a **new staged holon** from any existing one, **without** lineage.  
Ideal for templates or derivatives.

```rust
let staged_clone = stage_new_from_clone(context, original_ref, MapString("copy-123".into()))?;
```

| Operation | Input | Output | Lineage | Typical use |
|------------|--------|---------|----------|--------------|
| `clone_holon` | Any | `TransientReference` | ❌ | Scratch copy |
| `stage_new_version` | `SmartReference` | `StagedReference` | ✅ | Update existing |
| `stage_new_from_clone` | Any | `StagedReference` | ❌ | Derive new holon |

---

## 9. Typical Flows

### Create → stage → commit

```rust
let t = create_empty_transient_holon(context, MapString("MyType".into()));
t.with_property_value(context, P::Key, "example-1".into())?;
let staged = stage_new_holon_api(context, t)?;
let resp = commit_api(context)?;
```

### Fetch saved holon → stage new version

```rust
let smart = HolonReference::from_id(saved_id);
let staged = stage_new_version(context, smart)?;
staged.with_property_value(context, P::Title, "updated".into())?;
let resp = commit_api(context)?;
```

### Derive new staged holon from existing

```rust
let staged_clone = stage_new_from_clone(context, existing_ref, MapString("copy-2".into()))?;
```

---

## 10. Relationships

* **Read**:  
  Smart holons fetch from cache (with fetch-on-miss).  
  Staged and transient holons use local relationship maps.

* **Write**:  
  Only staged or transient references can modify relationships.  
  Use `add_related_holons`, `remove_related_holons`, or `with_descriptor`.

---

## 11. Query Layer

`Node`, `NodeCollection`, and `QueryExpression` express queries over holons.

```rust
let expr = QueryExpression::property_equals(P::Title, "Hello".into());
let nodes: NodeCollection = run_query(context, expr)?;
for node in nodes {
    println!("Found: {:?}", node.key(context)?);
}
```

> Note: The query API is evolving. Current support includes basic property and relationship predicates.

---

## 12. Dance Builders

`holon_dance_builders::*` provides ergonomic constructors for standard Dances:

```rust
let request = build_commit_dance_request(staged_refs);
let response: DanceResponse = send_dance(context, request)?;
if response.status_code == ResponseStatusCode::Ok {
    println!("Commit succeeded!");
}
```

Builders are the preferred way to trigger standardized Dances that cross the membrane boundary.

---

## 13. Access Control

All reference operations are validated against an `AccessType`:

| AccessType | Transient | Staged | Smart |
|-------------|------------|--------|--------|
| Read | ✅ | ✅ | ✅ |
| Write | ✅ | ✅ | ❌ |
| Clone | ✅ | ✅ | ✅ |
| Commit | ❌ | ✅ | ❌ |
| Abandon | ✅ | ✅ | ❌ |

Unauthorized actions raise `HolonError::NotAccessible`.

---

## 14. Error Handling

All functions return `Result<_, HolonError>`.  
Common variants include:

* `NotAccessible` – operation not permitted in this phase
* `InvalidHolonReference` – bad or missing reference
* `InvalidType`, `UnexpectedValueType`, `EmptyField` – schema or data errors

Errors returned through Dances can also be mapped to `ResponseStatusCode`.

---

## 15. Style & Conventions

* Use explicit suffixes (`*_reference`) for reference variables.
* When APIs expect `Vec<HolonReference>`, wrap explicitly:

  ```rust
  HolonReference::Transient(transient_reference)
  ```

---

## 16. Where to Look

* **Prelude:** `holons_prelude::prelude`
* **Context behavior:** `reference_layer/context_behavior.rs`
* **Operations API:** `reference_layer/holon_operations_api.rs`
* **Reference traits and types:** `reference_layer/holon_reference.rs`, `readable_holon.rs`, `writable_holon.rs`, `staged_reference.rs`, `transient_reference.rs`
* **Access and state:** `core_shared_objects/holon/state.rs`
* **Dance builders:** `holon_dance_builders`
* **Query layer:** `reference_layer/query_api.rs`

---

## 17. Evolving Areas

* Validation runs primarily at commit.
* Fluent chaining (`&Self`) is being standardized in setters.
* The query API will expand to richer predicates.
* Additional Dances (Loader, Validation) will reuse the same reference layer interface.