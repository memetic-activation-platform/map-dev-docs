# Storage Layer Query Algebra and SmartLink Tag Design

## Summary

This document consolidates the current design decisions regarding the MAP storage layer query algebra, the SmartLink tag encoding, and the rationale behind those decisions.

The primary architectural principle is that the storage layer remains a generic graph storage abstraction. Semantic interpretation belongs to the coordination/reference layer.

---

# Storage Layer Responsibilities

The storage layer is intentionally unaware of MAP concepts such as:

- HolonSpace
- EffectiveDescriptor
- current versions
- query execution
- HolonCollections

It understands only:

- HolonNodes
- SmartLinks
- source identifiers
- relationship names
- canonical keys
- SmartLink tags

The coordination layer interprets graph structure.

For example:

- "Return every holon in a HolonSpace" is implemented by expanding the `Owns` relationship from the HolonSpace.
- The storage layer has no special concept of "contents of a HolonSpace."

---

# Storage Layer Read Algebra

The current minimal storage read surface consists of:

- Retrieve a single HolonNode by LocalId.
- Retrieve multiple HolonNodes by LocalId.
- Expand every outgoing SmartLink from a source.
- Expand outgoing SmartLinks for a specific relationship.
- Expand outgoing SmartLinks for a relationship whose canonical key matches a supplied prefix.

Conceptually:

    get_holon(local_id)

    get_holons(local_ids)

    expand_all_from_source(source)

    expand_from_source(source, relationship_name)

    expand_from_source_by_key(source, relationship_name, key_prefix)

These operations are sufficient to support all higher-level graph navigation.

Filtering, projection, sorting, version selection, duplicate elimination, query execution, and HolonCollection construction remain coordination-layer responsibilities.

---

# Storage Layer Return Types

The storage layer returns only storage objects:

- HolonNodes
- SmartLinks
- collections of SmartLinks

It never returns:

- HolonCollections
- query results
- projections
- semantic objects

The storage layer exposes graph facts.

The coordination layer constructs semantic results.

---

# SmartLink Design Goals

SmartLinks intentionally serve as lightweight covering indexes rather than simple graph edges.

Their purpose is to allow many query operations to execute without first retrieving target HolonNodes.

The SmartReference abstraction implements read-through behavior:

1. Consult the cached property values stored in the SmartLink.
2. If the requested property is present, return it immediately.
3. Otherwise retrieve the target HolonNode and return the authoritative value.

The cached property map is therefore:

- non-authoritative
- opportunistic
- adaptive
- performance-oriented

Different SmartLinks pointing to the same target may legitimately cache different subsets of target properties.

---

# Canonical Key Materialization

Canonical keys are intentionally materialized inside SmartLinks.

Although keys are theoretically derivable from Holon properties, in practice they may depend upon:

- multiple properties
- descriptor-defined ordering rules
- normalization rules
- values obtained through relationships

Materializing the canonical key allows efficient distributed prefix lookup without retrieving target HolonNodes.

The storage layer stores canonical key bytes.

The coordination/reference layer computes and validates those keys.

---

# SmartLink Tag Encoding

The current preferred encoding is:

    RelationshipName

    0x00

    CanonicalKey

    0x00

    PropertyMap

The property map occupies the remainder of the tag.

This preserves Holochain prefix lookup while allowing decoding of both the canonical key and the encoded property values.

---

# Prefix Semantics

The delimiter-based encoding naturally supports hierarchical lookup.

Relationship lookup:

    RelationshipName + 0x00

Relationship plus key prefix lookup:

    RelationshipName + 0x00 + partial key

Relationship plus exact key lookup:

    RelationshipName + 0x00 + complete key + 0x00

No length prefix is placed before the canonical key because that would destroy prefix matching.

---

# Delimiter Choice

A single null byte (0x00) separates variable-length sections.

The delimiter appears:

- after the relationship name
- after the canonical key

This requires that neither value may contain an embedded null byte.

---

# Value-Type Constraints

The delimiter restriction belongs in the MAP type system rather than the SmartLink encoder.

A core value type defines:

- UTF-8
- no embedded null byte (0x00)

RelationshipName uses this value type.

CanonicalKey also uses this value type (along with any additional canonical-key constraints).

Validation therefore occurs uniformly through MAP value types rather than only during SmartLink serialization.

---

# Relationship Names vs Relationship IDs

The current decision is to store canonical relationship names rather than relationship identifiers.

Reasons include:

- human-readable SmartLinks
- easier debugging
- more useful logs
- descriptor lookup is unnecessary merely to understand a SmartLink
- storage tooling remains straightforward

Relationship names need only be unique within an EffectiveDescriptor.

They are not globally unique.

---

# Effective Descriptor Uniqueness

Descriptor authoring guarantees that inherited and locally declared members cannot produce duplicate names.

Within an EffectiveDescriptor:

- property names are unique
- relationship names are unique

Given:

- the source Holon
- its EffectiveDescriptor
- a relationship name

the corresponding relationship descriptor is unambiguous.

---

# Mutability

The relationship-name versus relationship-ID decision does not fundamentally change descriptor evolution.

Under the immutable Holochain model, descriptor updates always create new versions.

Questions surrounding semantic evolution are broader MAP concerns rather than SmartLink encoding concerns.

---

# SmartLink Property Categories

The SmartLink property map contains two distinct categories of values.

## 1. Authoritative Link Properties

These describe the relationship instance itself.

Characteristics:

- authoritative
- link-local
- never recovered from the target Holon
- always encoded when required by the relationship descriptor

Current built-in example:

- SequencePosition

## 2. Cached Target Properties

These are projections of target Holon properties.

Characteristics:

- non-authoritative
- adaptive
- optional
- recoverable from the target Holon
- included only as space permits

Examples include:

- Name
- Status
- CreatedDate

Different SmartLinks may cache different subsets of target properties.

---

# SmartLink Property Packing

Properties are encoded in order of storage importance rather than query importance.

The packing order is:

1. RelationshipName
2. CanonicalKey
3. All required authoritative link properties
4. Cached target properties until the SmartLink tag reaches capacity

This ordering reflects recoverability.

Authoritative link properties cannot be reconstructed elsewhere.

Cached target properties can always be recovered from the target Holon if omitted.

Consequently:

- authoritative link properties always have priority
- cached target properties are best-effort

---

# Manually Ordered Relationships

Relationship descriptors may declare that their targets are manually ordered.

For such relationships, the ordering information is stored directly in the SmartLink.

The current reserved property is:

- SequencePosition

SequencePosition is authoritative relationship-instance data.

It is not a property of either endpoint.

It therefore cannot correctly be stored on:

- the source Holon
- the target Holon

The SmartLink is the natural home for this information.

---

# SmartReference Semantics

Property lookup depends upon the property category.

For SequencePosition:

- read directly from the SmartLink
- never fall through to the target Holon

For cached target properties:

- return the cached value when present
- otherwise retrieve the target Holon and return the authoritative value

Thus only cached target properties participate in read-through behavior.

---

# Sorting and Manual Ordering

The storage layer never imposes semantic ordering on returned SmartLinks.

Expansion operations return an unordered collection of links.

Even for manually ordered relationships, the storage layer does not sort by SequencePosition.

Instead, SequencePosition is treated as an ordinary sortable property.

The query layer reconstructs manual ordering explicitly:

    Expand relationship

    OrderBy SequencePosition

This preserves composability.

Queries remain free to sort by:

- SequencePosition
- Name
- CreatedDate
- any cached property
- multiple sort keys

Manual ordering is simply one available ordering strategy.

---

# Relationship Descriptor Responsibilities

If a relationship descriptor specifies manual ordering:

- SequencePosition becomes a required authoritative SmartLink property.
- Validation ensures that every corresponding SmartLink contains a valid SequencePosition.
- Query execution may use SequencePosition as the default ordering for that relationship.
- Queries remain free to override that ordering explicitly.

---

# Cached Property Selection

Cached target properties are selected adaptively based on expected query benefit.

Typical candidates include properties frequently used for:

- filtering
- sorting
- pagination
- projection

Since cached properties are non-authoritative, different SmartLinks may legitimately cache different property subsets.

If a requested property is absent, SmartReference transparently retrieves the target Holon.

---

# Architectural Separation

Storage layer responsibilities:

- store HolonNodes
- store SmartLinks
- perform prefix retrieval
- encode relationship names
- encode canonical keys
- store authoritative link-local properties
- opportunistically cache target properties

Coordination layer responsibilities:

- resolve EffectiveDescriptors
- compute canonical keys
- interpret relationship semantics
- retrieve missing target properties
- filter
- sort
- perform version resolution
- construct HolonCollections
- execute the query algebra

This separation keeps the storage layer generic while allowing increasingly sophisticated semantic behavior above it.