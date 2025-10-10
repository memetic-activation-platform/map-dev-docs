# MAP Rust-API Developer Guide

The **Rust-API** is the boundary between your application code and the underlying holon store and services. It provides:

* **Uniform handles (“references”) to holons**, regardless of whether they are transient, staged, or cached/saved.
* A **small, consistent read/write API** that hides internal manager and phase differences.
* High-level **operations** for staging, committing, and deleting.
* A **curated prelude** for ergonomic imports and a stable public API.

This guide explains the API surface and shows how to perform the most common tasks.

---

# Part I – Foundations

## 1. Prelude

To simplify imports, use the MAP prelude:

```rust,ignore
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

```rust,no_run
use holons_prelude::prelude::*;

fn create_and_commit(
    context: &dyn HolonsContextBehavior,
) -> Result<(), HolonError> {
    // Create a new transient holon of a given type
    let transient = new_holon(context, MapString("ExampleType".into()));
    transient.with_property_value(context, P::Key, "example-1".into())?;

    // Stage it for persistence
    let _staged = stage_new_holon_api(context, transient)?;

    // Commit all staged changes
    let response = commit_api(context)?;
    println!("Committed {} holons.", response.commits_attempted);

    Ok(())
}
```

### Key points for developers

* The **context** is always the first parameter to any read or write call. 
  It carries all the state needed to resolve references, access relationships, and enforce permissions.

* You can think of it as your “session” or “workspace.”    Everything that happens during a transaction—reads, writes, staging, commits—occurs *within* this context.

* The context automatically routes requests to the right implementation based on the holon’s phase (transient, staged, or saved).  You never need to know which storage or cache layer is involved.

* Contexts are lightweight and short-lived. They are passed around as immutable references (`&dyn HolonsContextBehavior`), so you can safely use them in async or concurrent flows.

In short: **the context is your gateway to the MAP**. You use it everywhere, but you don’t manage or configure it—just pass it through to the reference-layer API.

---

## 3. Reference Kinds

`HolonReference` is the **universal handle** for accessing any holon in MAP—whether it’s newly created, staged for commit, or already persisted.  
It abstracts over three underlying reference types that represent different lifecycle phases of a holon.

* **`TransientReference`** — in-memory, mutable, not yet persisted.
* **`StagedReference`** — managed by the staging layer and ready to commit.
* **`SmartReference`** — read-only, backed by a saved holon in cache or storage.

All three implement the `ReadableHolon` trait;  
`TransientReference` and `StagedReference` additionally implement `WritableHolon`.

| Type                 | Backing store                 | Read | Write | Commit | Notes                                                                              |
|----------------------|-------------------------------|------|-------|--------|------------------------------------------------------------------------------------|
| `HolonReference`     | Delegates to underlying phase | ✅    | ✅ / ❌ | ✅ / ❌  | Unified handle that wraps any reference type. Enforces access rules automatically. |
| `TransientReference` | In-memory                     | ✅    | ✅     | ❌      | Must be staged before commit.                                                      |
| `StagedReference`    | Staging area                  | ✅    | ✅     | ✅      | Prepared for persistence.                                                          |
| `SmartReference`     | Saved/cache                   | ✅    | ❌     | ❌      | Read-only view of a saved holon.                                                   |

### Unified trait implementation

`HolonReference` implements both `ReadableHolon` **and** `WritableHolon`.  
This means you can call read or write methods directly on a `HolonReference` without downcasting to its internal variant.

However, **write access is phase-dependent**:

* If the reference wraps a `TransientReference` or `StagedReference`, write operations (e.g., `with_property_value`, `add_related_holons`) will succeed normally.
* If the reference wraps a `SmartReference`, any attempt to modify it will result in  
  `HolonError::NotAccessible`.

This design provides ergonomic consistency while maintaining strict access guarantees.

### Typical usage pattern

```rust,ignore
// Works regardless of phase
let title = holon_ref.property_value(context, &P::Title)?;

// Safe to call; will fail gracefully if reference is read-only
holon_ref.with_property_value(context, P::Title, "Updated".into())?;
```

In short:  
**`HolonReference` provides a single, uniform API for all holon phases**, while the combination of context and reference phase determines which operations are actually permitted.

---

# Part II – Holon Operations (HolonOperationsApi)

The **HolonOperationsApi** provides high-level functions for creating, staging, committing, and deleting holons.  It serves as the main entry point for mApp developers who need to persist holons, abstracting away the lower-level service lookups handled by the `HolonSpaceManager`. Where the `ReadableHolon` and `WritableHolon` traits focus on *individual holon content*, the operations in this API focus on *holon lifecycle actions* — such as preparing holons for persistence, committing them to storage, and querying what’s currently staged.

---

## 4. Creating and staging holons

Holons can be created or staged in several ways, depending on the source and intent. All staging operations result in a `StagedReference`, representing a holon managed by the **Nursery** and ready for commit.

### A. Creating a new transient holon

Use `new_holon` to create a new, empty transient holon. Once created, you can use its TransientReference to et its properties or relationships (see `WritableHolon` operations below).

```rust,ignore
let transient = new_holon(context, MapString("BookType".into()))?;
transient.with_property_value(context, P::Title, "The Rustonomicon".into())?;
```

Transient holons are purely in-memory — they can be used ephemerally (e.g., as temporary parameters in a Dance), or later staged for persistence.

---

### B. Staging a new holon from scratch

To prepare a transient holon for persistence, call `stage_new_holon`. This registers it in the Nursery and returns a `StagedReference`.

```rust,ignore
let transient = new_holon(context, MapString("BookType".into()))?;
transient.with_property_value(context, P::Key, "example-1".into())?;

let staged = stage_new_holon(context, transient)?;
```

The newly staged holon now participates in commit operations and can have relationships or properties safely modified.

---

### C. Staging a holon by cloning another

Use `stage_new_from_clone` to create a new staged holon based on an existing one. The `original_holon` may be a transient, staged, or saved holon.  NOTE: stage_new_from_clone on a Transient HolonReference is equivalent to `stage_new_holon`. To distinguish the new holon from the holon it is being cloned from, pass the "key" for the new holon as a parameter.

```rust,ignore
let staged_clone = stage_new_from_clone(context, existing_ref, MapString("copy-001".into()))?;
```

Use this form when you want to *derive* a new holon from an existing one without creating a lineage relationship.

---

### D. Staging a new version of a saved holon

Saved holons (accessed via `SmartReference`) are immutable. To “update” one, you must stage a new holon that explicitly declares the saved holon as its predecessor. This ensures historical lineage and preserves auditability.

```rust,ignore
let staged_version = stage_new_version(context, saved_ref)?;
staged_version.with_property_value(context, P::Status, "Revised".into())?;
```

> Conceptually, `stage_new_version` is the canonical “update” mechanism in MAP.  
> Instead of mutating data, it creates a new holon with lineage continuity.

---

### Summary of staging options

| Use case                      | Input reference kind | Function               | Result            | Lineage | Notes                                |
|-------------------------------|----------------------|------------------------|-------------------|---------|--------------------------------------|
| Create new holon from scratch | None (new)           | `stage_new_holon`      | `StagedReference` | ❌       | Typical create workflow              |
| Derive holon from another     | Any                  | `stage_new_from_clone` | `StagedReference` | ❌       | Copy data from any source            |
| Create new version (update)   | `SmartReference`     | `stage_new_version`    | `StagedReference` | ✅       | Adds predecessor link for versioning |

All three return `StagedReference`, ready to commit.

---

## 5. Committing staged holons

Once one or more holons have been staged, you can persist them together using `commit`.

```rust,ignore
let response = commit(context)?;
println!(
    "Saved: {}, Abandoned: {}, Attempted: {}",
    response.saved_holons.len(),
    response.abandoned_holons.len(),
    response.commits_attempted
);
```

### CommitResponse contents
* **`saved_holons`** — list of successfully persisted holons.
* **`abandoned_holons`** — holons that were skipped or invalidated.
* **`commits_attempted`** — total count of staged holons processed.

A complete commit satisfies:  
`(saved + abandoned == attempted)`

### Commit outcomes

**Complete Commit** – All staged holons and relationships persisted successfully.  
The Nursery is cleared of committed entries.

**Partial Commit** – Some holons committed successfully, others remain staged with error details.  
No staged holons are automatically removed, allowing retries.

**Failure** – System-level issue prevented commit; no changes persisted.

---

### E. Counting and retrieving staged holons

Helper methods are available for diagnostics or introspection:

```rust,ignore
let staged_total = staged_count(context);
let transient_total = transient_count(context);
println!("Currently staged: {}, transient: {}", staged_total, transient_total);
```

You can also look up specific holons by key:

```rust,ignore
let staged_by_key = get_staged_holon_by_base_key(context, &MapString("example-1".into()))?;
```

---

### F. Deleting holons

Holons can be deleted via `delete_holon`, but only local (i.e., space-owned) saved holons may be deleted.

```rust,ignore
delete_holon(context, local_id)?;
```

Deletion removes the holon from the current holon space and, if invoked from the guest side, from the DHT as well.

---

### Conceptual overview

The **HolonOperationsApi** provides the primary bridge between mApp logic and the MAP storage layer.  
It’s designed for developer clarity and consistency:

* **`new_holon`** → Creates new in-memory holons.
* **`stage_new_*`** → Moves holons into the staging area, ready for commit.
* **`commit`** → Persists all staged holons atomically.
* **`delete_holon`** → Removes holons permanently.

Together, these functions represent the canonical workflow for managing holon persistence.

---

# Part III – Individual Holons (ReadableHolon, WritableHolon)

## 7. Reading holons (ReadableHolon)

Every `HolonReference` implements `ReadableHolon`.  
Reads are *kind-safe* and work consistently across transient, staged, and saved holons.

---

### Core reads

`key(context) -> Option<MapString>`

The human-meaningful identifier for the holon, if defined.  
Some holon kinds are keyless, so this may return `None`.

Example:
```rust,ignore
let key_opt = reference.key(context)?;
```

---

`versioned_key(context) -> MapString`

A stable, fully-qualified identifier that includes the base key plus version information (when applicable).  
Since saved holons are immutable, updating a saved holon creates a *new version* with a distinct `versioned_key`.  
If the update doesn’t alter the underlying key properties, the new holon will share the same base key.

Example:
```rust,ignore
let vkey = reference.versioned_key(context)?;
```

---

`property_value(context, name) -> Option<PropertyValue>`

Reads a property by name using **ergonomic inputs**:  
`&str`, `String`, `MapString`, `PropertyName`, or a core enum such as `CorePropertyTypeName::Title`.  
Returns `None` if the property is absent.

Example:
```rust,ignore
let title_opt = reference.property_value(context, "title")?;
```

---

`related_holons(context, name) -> HolonCollection`

Navigates an outgoing relationship and returns a collection of `HolonReference`s to the linked holons.  
Accepts `&str`, `String`, `MapString`, `RelationshipName`, or a core enum.  
Always returns a `HolonCollection` (possibly empty), never `None`.

Example:
```rust,ignore
let children = reference.related_holons(context, "HAS_CHILD")?;
```

---

### When to use which

| Method               | Purpose                                                                                                        |
|----------------------|----------------------------------------------------------------------------------------------------------------|
| **`key`**            | Retrieve or display a meaningful base key. Use for routing, URLs, and user-facing identifiers.                 |
| **`versioned_key`**  | Generate stable identifiers for logging, caching, and cross-system references.                                 |
| **`property_value`** | Read domain fields (e.g., `title`, `status`). Use ergonomic names: `"title"` or `CorePropertyTypeName::Title`. |
| **`related_holons`** | Traverse graph links (e.g., `"HAS_CHILD"`, `CoreRelationshipTypeName::HasChild`) and iterate results.          |

---

### Ergonomic property and relationship access

MAP’s ergonomic wrapper traits make property and relationship access feel natural:

* **`ToPropertyName`** — allows property lookups using core enums, strings, or `MapString`s.
* **`ToRelationshipName`** — allows relationship lookups using core enums or strings.

These remove the need to manually construct `PropertyName(MapString(...))` or `BaseValue::StringValue(...)` and unify access across core and dynamic names.

#### Examples

**Before (verbose):**
```rust,ignore
let title = reference.property_value(
    context,
    PropertyName(MapString("title".into())),
)?;
```

**Now (ergonomic):**
```rust,ignore
let title = reference.property_value(context, "title")?;
let author = reference.property_value(context, CorePropertyTypeName::Author)?;
let children = reference.related_holons(context, CoreRelationshipTypeName::HasChild)?;
```

All inputs are normalized internally (e.g., `"friends"`, `"Friends"`, and `"FRIENDS"` are equivalent).

---

### Example: Reading a property with a default

```rust,ignore
let title = item.property_value(context, "title")?
    .and_then(|v| v.as_string())
    .unwrap_or_else(|| "Untitled".to_string());
```

This retrieves the `"title"` property, converts it to a string if possible, and falls back to `"Untitled"` when the property is missing or not a string.

Step-by-step:
1. `property_value` returns a `Result<Option<PropertyValue>, HolonError>`.  
   The `?` operator unwraps the `Result`, leaving an `Option<PropertyValue>`.
2. `.and_then(|v| v.as_string())` converts the property to a `String` if it’s string-typed.
3. `.unwrap_or_else(|| "Untitled".to_string())` substitutes a default when missing.

In plain language:
> “Get the holon’s title if available; otherwise use `'Untitled'`.”

---

### Example: Traversing relationships

```rust,ignore
let children = reference.related_holons(context, "HAS_CHILD")?;
for child in children.iter() {
    let ck = child.key(context)?;
    println!("Child key: {:?}", ck);
}
```

This fetches and iterates through all linked child holons using an ergonomic relationship lookup.

## 8. Writing holons (WritableHolon)

The `WritableHolon` trait provides mutation APIs for holons that can be modified — namely,  
**`TransientReference`** and **`StagedReference`**.  
Attempting to call any of these methods on a `SmartReference` (saved holon) will return  
`HolonError::NotAccessible`.

Writable methods are kind-safe: they automatically update both the in-memory property/relationship maps and any synchronization state used during staging or commit.

---

### Setting property values

`with_property_value(context, name, value) -> Result<(), HolonError>`

Assigns or replaces a property value.  
Accepts property names using ergonomic `ToPropertyName` conversions (e.g., string literals or core enums) and automatically wraps primitive Rust types into their appropriate `PropertyValue`.

Example:
```rust,ignore
reference.with_property_value(context, "title", "Hello World")?;
reference.with_property_value(context, CorePropertyTypeName::Status, "Draft")?;
```

> You can pass Rust primitives such as `&str`, `String`, `bool`, `i64`, or `f64`.  
> Internally these are converted into the appropriate MAP `BaseValue` variant.

---

### Removing properties

`remove_property_value(context, name) -> Result<(), HolonError>`

Removes the specified property, if present.

Example:
```rust,ignore
reference.remove_property_value(context, "obsolete")?;
```

If the property does not exist, the method simply returns `Ok(())`.

---

### Managing relationships

`add_related_holons(context, name, targets) -> Result<(), HolonError>`

Adds one or more related holons under the given relationship name.  
Each target is a `HolonReference`.  
The relationship name accepts the same ergonomic types as property names.

Example:
```rust,ignore
reference.add_related_holons(
    context,
    CoreRelationshipTypeName::HasChild,
    vec![child_ref],
)?;
```

---

`remove_related_holons(context, name, targets) -> Result<(), HolonError>`

Removes one or more holons from a relationship set.  
Has no effect if the target references are not already related.

Example:
```rust,ignore
reference.remove_related_holons(
    context,
    "HAS_CHILD",
    vec![child_ref],
)?;
```

> Relationship mutations automatically update the holon’s local relationship map.  
> The changes become durable only after commit.

---

### Setting the descriptor

`with_descriptor(context, descriptor_ref) -> Result<(), HolonError>`

Sets or replaces the holon’s **descriptor**, which declares its type.  
Descriptors are always holons themselves (of a `HolonType` kind).  
This call is uncommon in normal app code — it’s primarily used by loaders or editors creating new holons from schema types.

Example:
```rust,ignore
reference.with_descriptor(context, descriptor_ref)?;
```

---

### Setting the predecessor

`with_predecessor(context, predecessor_ref) -> Result<(), HolonError>`

Establishes a lineage relationship between the current holon and its immediate predecessor.  
Used mainly in versioned workflows to record “what this holon was derived from.”

Example:
```rust,ignore
reference.with_predecessor(context, Some(prev_ref))?;
```

To clear a predecessor link, pass `None`.

---

### Summary of writable operations

| Operation               | Purpose                    | Typical use                                                 |
|-------------------------|----------------------------|-------------------------------------------------------------|
| `with_property_value`   | Set or replace a property. | Create or edit domain fields before staging or commit.      |
| `remove_property_value` | Remove a property.         | Clean up unused or obsolete fields.                         |
| `add_related_holons`    | Add linked holons.         | Associate new relationships (e.g., add tasks to a project). |
| `remove_related_holons` | Remove linked holons.      | Detach related entities.                                    |
| `with_descriptor`       | Assign a type descriptor.  | Loader-level operation for schema-driven creation.          |
| `with_predecessor`      | Record lineage.            | Used in versioned updates (`stage_new_version`).            |

---

### Example workflow

Here’s a typical editing flow for a staged holon:

```rust,ignore
// 1. Stage a new version of an existing holon
let staged = stage_new_version(context, saved_ref)?;

// 2. Update its properties
staged.with_property_value(context, "title", "Updated Title")?;
staged.with_property_value(context, CorePropertyTypeName::Status, "Revised")?;

// 3. Add and remove related holons
staged.add_related_holons(context, "HAS_CHILD", vec![child_a])?;
staged.remove_related_holons(context, "HAS_CHILD", vec![child_b])?;

// 4. Commit all staged changes
let resp = commit(context)?;
println!("{} holons saved.", resp.saved_holons.len());
```

This demonstrates the complete writable lifecycle: create or stage → modify → commit.

---

### Error conditions

All writable operations return `Result<(), HolonError>`.  
Common error cases:

- `HolonError::NotAccessible` — write attempted on a read-only holon (`SmartReference`).
- `HolonError::InvalidHolonReference` — target or relationship not resolvable in the current context.
- `HolonError::InvalidType` — provided value type doesn’t match the property’s declared type.
- `HolonError::UnexpectedValueType` — incompatible runtime conversion.

Writable APIs follow a **fail-fast** design — operations either succeed immediately or return a specific `HolonError` explaining what went wrong.

---

**In summary:**  
WritableHolon methods make it easy to set, update, and link holons safely, with ergonomic property and relationship access, automatic type conversion, and strong context enforcement.

---

# Part IV – Collections (HolonCollectionApi)

## 9. Working with collections of holons

A `HolonCollection` represents an unordered set of holon references—often returned when traversing relationships.

### Access and iteration
```rust,ignore
let count   = tasks.len();
let first   = tasks.first();
let by_index  = tasks.get(2);
for holon_ref in &tasks {
    println!("{:?}", holon_ref.key(context)?);
}
```

### Membership and lookup
```rust,ignore
if tasks.contains(&some_ref) {
    println!("Already linked!");
}
```

```rust,ignore
if let Some(found) = tasks.get_by_key(&MapString("task-42".into())) {
    println!("Found task 42: {:?}", found.key(context)?);
}
```

### Mutation
Available only for transient and staged holons.

```rust,ignore
tasks.add(context, HolonReference::Transient(new_task_ref))?;
tasks.remove(context, HolonReference::Smart(old_task_ref))?;
```

---

# Part V – Queries

## 10. Querying holons

The query layer provides a high-level way to search for holons that meet specific criteria.

### Example
```rust,ignore
let expr = QueryExpression::property_equals(P::Title, "Hello".into());
let nodes: NodeCollection = run_query(context, expr)?;
for node in nodes {
    println!("Found: {:?}", node.key(context)?);
}
```

> Note: The query API is evolving and currently supports basic property and relationship predicates.

---

# Part VI – Cross-cutting Topics

## 11. Access Control

| AccessType | Transient | Staged | Smart |
|------------|-----------|--------|-------|
| Read       | ✅         | ✅      | ✅     |
| Write      | ✅         | ✅      | ❌     |
| Clone      | ✅         | ✅      | ✅     |
| Commit     | ❌         | ✅      | ❌     |
| Abandon    | ✅         | ✅      | ❌     |

Unauthorized actions raise `HolonError::NotAccessible`.

---

## 12. Error Handling

All MAP API functions return `Result<_, HolonError>`.  This unified error type is used consistently across the reference layer and ensures that mApp code can handle errors uniformly—whether they originate in the local runtime, the staging layer, or a distributed DHT operation.

---

### How errors propagate

1. **Local logic errors** (e.g., missing property, invalid type) are raised directly by reference-layer methods.
2. **Access control errors** are enforced by context and reference kind before reaching service layers.
3. **Service errors** (e.g., during commit or DHT access) bubble up through the same `HolonError` type for consistent handling.

When using `?`, errors automatically propagate to the caller; explicit matches can be used for fine-grained control.

Example:

```rust,ignore
match reference.property_value(context, "title") {
    Ok(Some(val)) => println!("Title: {:?}", val.as_string()),
    Ok(None) => println!("Title missing."),
    Err(HolonError::NotAccessible) => println!("You do not have read access."),
    Err(err) => eprintln!("Unexpected error: {:?}", err),
}
```

---

### Error categories

| Category                  | Typical causes                                               | Handling strategy                                                           |
|---------------------------|--------------------------------------------------------------|-----------------------------------------------------------------------------|
| **Access**                | Attempted write or read on an inaccessible holon or context. | Verify reference kind and permissions.                                      |
| **Resolution**            | Reference could not be found or resolved.                    | Check that the target holon exists in the current space.                    |
| **Schema / Type**         | Property value type mismatches or missing required fields.   | Validate property types before assignment; use defaults for missing values. |
| **Persistence / Service** | Errors during staging, commit, or DHT operations.            | Retry commit or surface to user; check `CommitResponse` for details.        |
| **Internal**              | Unexpected internal conditions or bugs.                      | Log and escalate.                                                           |

---

### Mapping to ResponseStatusCode

When holon operations are invoked through Dances, `HolonError` variants are automatically mapped to appropriate `ResponseStatusCode` values (e.g., `BadRequest`, `Conflict`, `ServerError`).  
This allows API clients to interpret results consistently across in-process and distributed boundaries.

---

### Best practices

* Use **pattern matching** to handle expected errors gracefully (e.g., missing properties).
* Use the **`?` operator** when you want errors to bubble up.
* Always log or display `HolonError::message()` when debugging.
* Treat `HolonError::InternalError` as a bug indicator — report it.

For a complete list of `HolonError` variants, see **Appendix B – HolonError Reference**.

---

## 13. Style & Conventions

* Use explicit suffixes (`*_reference`) for reference variables.
* When APIs expect `Vec<HolonReference>`, wrap explicitly:

```rust,ignore
HolonReference::Transient(transient_reference)
```

---

## 14. Where to Look

* **Prelude:** `holons_prelude::prelude`
* **Context behavior:** `reference_layer/context_behavior.rs`
* **Operations API:** `reference_layer/holon_operations_api.rs`
* **Reference traits and types:** `reference_layer/holon_reference.rs`, `readable_holon.rs`, `writable_holon.rs`, `staged_reference.rs`, `transient_reference.rs`
* **Access and state:** `core_shared_objects/holon/state.rs`
* **Dance builders:** `holon_dance_builders`
* **Query layer:** `reference_layer/query_api.rs`

---

## 15. Evolving Areas

* Validation runs primarily at commit.
* Fluent chaining (`&Self`) is being standardized in setters.
* The query API will expand to richer predicates.
* Additional Dances (Loader, Validation) will reuse the same reference layer interface.

---

# Appendix A – API Quick Reference Card

## HolonOperationsApi

```rust,ignore
fn new_holon(
    context: &dyn HolonsContextBehavior,
    type_name: MapString,
) -> TransientReference;

fn stage_new_holon_api(
    context: &dyn HolonsContextBehavior,
    transient: TransientReference,
) -> Result<StagedReference, HolonError>;

fn stage_new_version(
    context: &dyn HolonsContextBehavior,
    current_version: SmartReference,
) -> Result<StagedReference, HolonError>;

fn stage_new_from_clone(
    context: &dyn HolonsContextBehavior,
    original_holon: HolonReference,
    new_key: MapString,
) -> Result<StagedReference, HolonError>;

fn commit_api(
    context: &dyn HolonsContextBehavior,
) -> Result<CommitResponse, HolonError>;
```

---

## ReadableHolon

```rust,ignore
fn key(&self, context: &dyn HolonsContextBehavior)
    -> Result<Option<MapString>, HolonError>;

fn versioned_key(&self, context: &dyn HolonsContextBehavior)
    -> Result<VersionedKey, HolonError>;

fn property_value(
    &self,
    context: &dyn HolonsContextBehavior,
    property_name: &PropertyName,
) -> Result<Option<PropertyValue>, HolonError>;

fn related_holons(
    &self,
    context: &dyn HolonsContextBehavior,
    relationship_name: &RelationshipName,
) -> Result<HolonCollection, HolonError>;

fn all_related_holons(
    &self,
    context: &dyn HolonsContextBehavior,
) -> Result<BTreeMap<RelationshipName, HolonCollection>, HolonError>;

fn holon_id(&self, context: &dyn HolonsContextBehavior)
    -> Result<HolonId, HolonError>;

fn predecessor(&self, context: &dyn HolonsContextBehavior)
    -> Result<Option<HolonReference>, HolonError>;

fn essential_content(&self, context: &dyn HolonsContextBehavior)
    -> Result<EssentialHolonContent, HolonError>;

```

---

## WritableHolon

```rust,ignore
fn with_property_value(
    &self,
    context: &dyn HolonsContextBehavior,
    property_name: CorePropertyTypeName,
    value: PropertyValue,
) -> Result<(), HolonError>;

fn remove_property_value(
    &self,
    context: &dyn HolonsContextBehavior,
    property_name: CorePropertyTypeName,
) -> Result<(), HolonError>;

fn add_related_holons(
    &self,
    context: &dyn HolonsContextBehavior,
    relationship_name: RelationshipName,
    targets: Vec<HolonReference>,
) -> Result<(), HolonError>;

fn remove_related_holons(
    &self,
    context: &dyn HolonsContextBehavior,
    relationship_name: RelationshipName,
    targets: Vec<HolonReference>,
) -> Result<(), HolonError>;

fn with_descriptor(
    &self,
    context: &dyn HolonsContextBehavior,
    descriptor_ref: HolonReference,
) -> Result<(), HolonError>;

fn with_predecessor(
    &self,
    context: &dyn HolonsContextBehavior,
    predecessor_ref: Option<HolonReference>,
) -> Result<(), HolonError>;
```

---

## HolonCollectionApi

```rust,ignore
fn len(&self) -> usize;
fn is_empty(&self) -> bool;
fn first(&self) -> Option<&HolonReference>;
fn get(&self, index: usize) -> Option<&HolonReference>;
fn get_by_key(&self, key: &MapString) -> Option<&HolonReference>;
fn contains(&self, target: &HolonReference) -> bool;
fn to_vec(&self) -> Vec<HolonReference>;
fn add(
    &self,
    context: &dyn HolonsContextBehavior,
    target: HolonReference,
) -> Result<(), HolonError>;
fn remove(
    &self,
    context: &dyn HolonsContextBehavior,
    target: HolonReference,
) -> Result<(), HolonError>;
```

---

## Query Layer

```rust,ignore
fn property_equals(
    property_name: CorePropertyTypeName,
    value: PropertyValue,
) -> QueryExpression;

fn run_query(
    context: &dyn HolonsContextBehavior,
    expr: QueryExpression,
) -> Result<NodeCollection, HolonError>;
```

---

This appendix serves as a concise **signature-only** reference for all key API areas, grouped by their functional domains.

---

# Appendix B – HolonError Reference

The `HolonError` enum defines all possible error conditions that may occur while working with holons.  
Each variant captures a distinct failure domain within the MAP reference layer.

| Variant                     | Description                                                          | Common Origin                                                       |
|-----------------------------|----------------------------------------------------------------------|---------------------------------------------------------------------|
| **`NotAccessible`**         | Operation not permitted under current context/kind combination.      | Attempting to modify a `SmartReference`; restricted access context. |
| **`InvalidHolonReference`** | Reference cannot be resolved or is malformed.                        | Dangling or out-of-scope references; deleted holons.                |
| **`InvalidType`**           | The provided value or descriptor does not match the expected type.   | Assigning the wrong `ValueType` or `Descriptor`.                    |
| **`UnexpectedValueType`**   | Runtime value type mismatch (e.g., expected string, found integer).  | Property read or write with incompatible type.                      |
| **`EmptyField`**            | A required field or property is missing or empty.                    | Validation of incomplete holon data.                                |
| **`MissingDescriptor`**     | The holon lacks an associated type descriptor.                       | Loader or schema definition error.                                  |
| **`MissingRelationship`**   | A requested relationship does not exist.                             | Using an undefined relationship name.                               |
| **`DuplicateKey`**          | Attempted to create or stage a holon with a key that already exists. | Staging or import conflicts.                                        |
| **`StagingConflict`**       | Two staged holons conflict on lineage or key.                        | Concurrent edits in the Nursery.                                    |
| **`CommitFailure`**         | One or more holons failed to commit.                                 | DHT or persistence layer error.                                     |
| **`Abandoned`**             | The holon was marked abandoned during commit.                        | Validation failure during persistence.                              |
| **`InvalidContext`**        | The provided context is invalid or no longer active.                 | Using an expired or mismatched context reference.                   |
| **`SerializationError`**    | Failure to encode or decode a holon or property value.               | Cross-boundary transmission or storage.                             |
| **`DeserializationError`**  | Failure to parse persisted data into a holon.                        | Import or cache corruption.                                         |
| **`NetworkError`**          | Communication failure with remote service or DHT.                    | Distributed commit or fetch.                                        |
| **`InternalError`**         | Unexpected internal condition.                                       | Logic bugs or invariant violations.                                 |

---

### Example usage in pattern matches

```rust,ignore
match commit(context) {
    Ok(resp) if resp.is_complete() => println!("Commit succeeded!"),
    Ok(resp) => eprintln!("Partial commit: {:?}", resp.summary()),
    Err(HolonError::CommitFailure) => eprintln!("Commit failed."),
    Err(HolonError::NetworkError) => eprintln!("Network issue, retry later."),
    Err(e) => eprintln!("Unhandled error: {:?}", e),
}
```

---

### Notes

* Most variants are recoverable — for example, `StagingConflict` and `DuplicateKey` can be retried after correction.
* Use `HolonError::to_string()` for concise error summaries in logs.
* `InternalError` and `InvalidContext` indicate deeper systemic problems that typically warrant investigation.

Together, these definitions provide a full picture of how the MAP reference layer communicates problems — predictably, type-safely, and with context.

