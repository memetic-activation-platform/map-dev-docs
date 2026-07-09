# External IDs, Trust Channels, and Definition Hashes

## Core insight

We should keep `ExternalId` as a compact two-part identifier, but reinterpret the first part as a synthesized local proxy for a routable external steward.

    ExternalId = OutboundProxyId + RemoteObjectId

Where:

    OutboundProxyId = local proxy for (TrustChannel + RemoteSteward)
    RemoteObjectId = identifier/key/alias meaningful to the remote steward

This avoids expanding every external reference into a three-part identifier:

    TrustChannelId + AgentId + RemoteObjectId

The three-part structure still exists conceptually, but it is hidden behind the local `OutboundProxyId`.

## OutboundProxyId

An `OutboundProxyId` identifies a locally known route to an external steward.

That steward may be:

- A personal agent space
- A member agent inside a We-Space
- The We-Space itself
- Another agent/space reachable through a trust channel

The proxy record can contain:

    trust_channel_id
    remote_steward_id
    routing policy
    capabilities
    agreement context
    access metadata

This means the same remote agent may have multiple outbound proxies if it is reachable through multiple trust channels.

It also means a single trust channel may support multiple outbound proxies if it exposes multiple stewards.

## RemoteObjectId

The second part of the external ID should not be assumed to be the remote steward’s internal identifier.

It only needs to be an identifier that the remote steward can map to the intended object.

That could be:

- The actual internal holon ID
- An opaque public alias
- A revocable mapping key
- A scoped reference meaningful only within a particular agreement or trust channel

So the better conceptual form is:

    ExternalId = OutboundProxyId + RemoteObjectId

not:

    ExternalId = SpaceId + HolonId

## Dereferencing

Dereferencing an `ExternalId` means:

    1. Resolve the OutboundProxyId locally.
    2. Determine the TrustChannel and remote steward.
    3. Send the dereference request through that channel.
    4. Present the RemoteObjectId to the remote steward.
    5. Let the remote steward resolve that object according to its own policies.

The external ID is therefore not a global address. It is a durable local reference through a locally known route.

## Reference chains

Suppose:

- S1 references an object stewarded by S2.
- That S2 object has relationships to objects stewarded by S3, S4, and S5.
- S2 has trust channels and agreements with S3, S4, and S5.
- S1 is allowed, under some policy, to discover or access those related references.

There are two possible dereference models.

### Routed-through-chain access

S1 asks S2, and S2 dereferences or mediates access to S3/S4/S5 on S1’s behalf.

Advantages:

- Simple authority model.
- S1 only needs a relationship with S2.
- S2 remains responsible for enforcing what it is allowed to reveal.

Disadvantages:

- Adds latency and dependency on intermediaries.
- S1 may not be able to cache or directly re-use downstream references.
- Long reference paths become operationally fragile.

### Direct downstream access

S1 receives or derives an identifier for an object in S5 and goes directly to S5.

This requires one of:

- A direct trust channel between S1 and S5
- A delegated capability from S2
- A provenance chain proving that S1 is authorized
- A negotiated proxy agreement between S1 and S5

Advantages:

- More efficient once established.
- Reduces dependency on intermediate spaces.
- Allows S1 to form durable direct references to downstream stewards.

Disadvantages:

- Requires more sophisticated authority/provenance handling.
- May leak relationship topology.
- Requires S5 to understand why S1 is authorized.

## Key distinction

External IDs are path-sensitive.

The same remote holon may be known through different routes, producing different external IDs.

That is acceptable because `ExternalId` is about dereference and authority, not semantic equivalence.

## Descriptor problem

Descriptors and other definition-like holons create a special case.

The same descriptor may be reachable through different proxy paths and therefore have different external IDs.

If descriptor cache lookup depends on external IDs, then equivalent descriptors may fail to share cache entries.

This weakens the utility of descriptor caching.

## Definition hashes

For descriptors and other definitional holons, use a path-insensitive definition hash.

    DefinitionHash = hash(canonical_definitional_surface)

This should be independent of:

- Trust channel
- Outbound proxy path
- Remote steward route
- Local database identity
- Incidental provenance

Two definitionally equivalent descriptors should produce the same hash, regardless of how they were discovered.

## Two identifier regimes

We therefore need two distinct regimes.

### Routable references

Used for dereferencing stewarded holons.

    ExternalId = OutboundProxyId + RemoteObjectId

These are:

- Path-sensitive
- Authority-sensitive
- Route-dependent
- Steward-mediated

### Definitional references

Used for recognizing equivalent definitions.

    DefinitionHash = hash(canonical_definitional_surface)

These are:

- Path-insensitive
- Content-addressed
- Cache-friendly
- Useful for definitional equivalence

## Where the hash belongs

The definition hash should belong to the holon node or record, not primarily to the link.

A link may cache or index the hash, but the hash describes the canonical definitional content of the holon itself.

Possible field:

    definition_hash: Option<DefinitionHash>

This is better than a generic `content_hash`, because we are not necessarily hashing all content. We are hashing the canonical definitional surface.

## What participates in the definition hash

Only definitional content should participate.

Include:

- Definitional properties
- Definitional relationships
- Constraints
- Value type references
- Declared property references
- Declared relationship references
- Structural semantics needed to determine equivalence

Exclude:

- Routing relationships
- Trust channel relationships
- Provenance relationships
- Operational/cache metadata
- Local IDs
- External IDs
- Agreement-specific access paths
- Incidental contextual relationships

## Relationship classification

Relationships should be classified, at least conceptually, into:

- Definitional relationships
- Operational relationships
- Contextual relationships
- Provenance/routing relationships

Only definitional relationships participate in the definition hash.

## Hashing relationship references

For definitional relationships, the hash should not depend on route-specific IDs.

Instead, related definitional holons should be represented by their own definition hashes or canonical semantic references.

Example:

    HolonType definition hash includes:
      type name
      abstract/concrete status
      extends relationship
      declared properties
      declared relationships
      constraints

    PropertyType definition hash includes:
      property name
      value type
      requiredness
      default constraints
      validation constraints

    RelationshipType definition hash includes:
      relationship name
      source type
      target type
      cardinality
      ordering
      inverse relationship
      semantic description

## Practical cache model

Descriptor cache lookup can become:

    DefinitionHash -> LocalDescriptorHolonId

Dereference remains:

    OutboundProxyId + RemoteObjectId -> Remote stewarded holon

So reference chains do not destroy cacheability.

They only affect routing, authority, and provenance.

Definitional equivalence is handled separately through canonical content hashes.

## Working conclusion

Do not make `ExternalId` carry all routing, authority, and equivalence semantics.

Instead:

- Keep `ExternalId` compact and routable.
- Let `OutboundProxyId` encapsulate `TrustChannel + RemoteSteward`.
- Let `RemoteObjectId` remain steward-defined and possibly opaque.
- Use `DefinitionHash` for descriptor equivalence and cacheability.
- Treat route-sensitive dereference and path-insensitive definition equivalence as separate concerns.