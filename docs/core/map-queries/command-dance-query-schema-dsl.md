# Command, Dance, and Query Schema DSL

Status: Step 3 draft for review.

This document captures the schema-level seam between Commands, Dances, and Queries
as a compact DSL. It is grounded in the generated core-schema JSON under:

```text
/Users/stevemelville/dev/map-proto/map-dev/map-holons/host/import_files/map-schema/core-schema
```

The generated JSON files are derived from Airtable and must not be edited directly.
Entries marked `existing` describe the current generated schema. Entries marked
`proposed` describe additions for the query schema. Entries marked
`suggested-change` describe changes that should be made in the Airtable source
before regenerating schema JSON.

## Design Rule

```text
Command = ingress envelope and lifecycle policy.
Dance = descriptor-afforded executable behavior.
Query = request payload supplied to a Query Dance.
```

The canonical query execution path is:

```text
Transaction.HolonType
  AffordsCommand -> Dance.CommandType

Dance.CommandType
  payload -> DanceInvocation.HolonType

DanceInvocation.HolonType
  InvokesDance -> QueryDance.DanceType
  AffordingHolon -> HolonType
  Request      -> QueryDanceRequest.HolonType

QueryDanceRequest.HolonType
  QueryGraph      -> QueryGraph.HolonType
  InitialBindings -> ExecutionBinding.HolonType

ExecutionInstance.HolonType
  ExecutesRequest   -> QueryDanceRequest.HolonType
  ExecutionBindings -> ExecutionBinding.HolonType
  ExecutionResult   -> HolonCollection.HolonType

QueryDance.DanceType
  Response -> QueryDanceResponse.DanceResponseType

QueryDanceResponse.DanceResponseType
  ResponseBody -> HolonCollection.HolonType
```

Narrative (non-normative):

This path is the seam we are trying to sharpen. A `Command` is the ingress
surface. A `DanceInvocation` says which dance is being invoked, by which
affording holon, and with which request holon. The query itself is not the
command and not the dance. It is the structured payload carried by the request.
Execution then produces an `ExecutionInstance` for that run and a
`HolonCollection` as the externally meaningful result.

## DSL Conventions

```text
schema <key> [status] {
  depends_on <schema-key>
}

holon_type <key> [status] {
  type_name <TypeName>
  extends <type-key>
  abstract <true|false>
  properties <property-type-key>...
  relationships <relationship-type-key>...
}

property_type <key> [status] {
  type_name <TypeName>
  value_type <value-type-key>
}

value_type <key> [status] {
  type_name <TypeName>
  kind <TypeKind.*>
  variants <variant-key>...
}

relationship_type <key> [status] {
  type_name <TypeName>
  source <source-type-key>
  target <target-type-key>
  inverse <inverse-relationship-type-key>
  definitional <true|false>
  ordered <true|false>
  duplicates <true|false>
  cardinality <min>..<max>
}
```

All relationship types declared in this draft have an inverse. When the current
generated core schema lacks an inverse, the missing inverse is marked
`suggested-change`.

## Shared Existing Types

```map-schema-dsl
schema MAP Core Schema-v0.0.7 existing

schema MAP Dance Schema-v0.0.4 existing {
  depends_on MAP Core Schema-v0.0.7
}

value_type MapStringValueType existing {
  type_name MapStringValueType
  kind TypeKind.Value.String
}

value_type MapIntegerValueType existing {
  type_name MapIntegerValueType
  kind TypeKind.Value.Integer
}

value_type MapBooleanValueType existing {
  type_name MapBooleanValueType
  kind TypeKind.Value.Boolean
}

value_type MapBytesValueType existing {
  type_name MapBytesValueType
  kind TypeKind.Value.Bytes
}

holon_type HolonType existing {
  type_name HolonType
  abstract true
}

holon_type TypeDescriptor.HolonType existing {
  type_name TypeDescriptor
  extends HolonType
  abstract false
}

holon_type Schema.HolonType existing {
  type_name Schema
  extends HolonType
  abstract false
}

holon_type HolonSpace.HolonType existing {
  type_name HolonSpace
  extends HolonType
  abstract false
}

holon_type Transaction.HolonType existing {
  type_name Transaction
  extends HolonType
  abstract false
  relationships
    (HolonType)-[AffordsCommand]->(CommandType.HolonType)
}

holon_type HolonCollection.HolonType existing {
  type_name HolonCollection
  extends HolonType
  abstract false
  properties
    CollectionType.PropertyType
    IsOrdered.PropertyType
    AllowsDuplicates.PropertyType
  relationships
    (HolonCollection.HolonType)-[CollectionMembers]->(HolonType)
    (HolonCollection.HolonType)-[ElementType]->(HolonType)
}

relationship_type (HolonCollection.HolonType)-[CollectionMembers]->(HolonType) existing {
  type_name CollectionMembers
  source HolonCollection.HolonType
  target HolonType
  inverse (HolonType)-[MemberOfCollection]->(HolonCollection.HolonType)
  definitional false
  ordered true
  duplicates true
  cardinality 0..32767
}

relationship_type (HolonType)-[MemberOfCollection]->(HolonCollection.HolonType) existing {
  type_name MemberOfCollection
  source HolonType
  target HolonCollection.HolonType
  inverse (HolonCollection.HolonType)-[CollectionMembers]->(HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (HolonCollection.HolonType)-[ElementType]->(HolonType) existing {
  type_name ElementType
  source HolonCollection.HolonType
  target HolonType
  inverse (HolonType)-[ElementTypeFor]->(HolonCollection.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (HolonType)-[ElementTypeFor]->(HolonCollection.HolonType) existing {
  type_name ElementTypeFor
  source HolonType
  target HolonCollection.HolonType
  inverse (HolonCollection.HolonType)-[ElementType]->(HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}
```

## Command Schema

The current Command schema defines command descriptors, not persistent command
request holons. Runtime command ingress is represented in Rust by command enums
and wire types. For `Dance.CommandType`, the payload is the typed
`DanceInvocation` reference carried by `TransactionAction::DanceV2`.

```map-schema-dsl
holon_type CommandType.HolonType existing {
  type_name CommandType
  extends HolonType
  abstract true
}

holon_type BeginTransaction.CommandType existing { type_name BeginTransaction extends CommandType.HolonType abstract false }
holon_type CloneHolon.CommandType existing { type_name CloneHolon extends CommandType.HolonType abstract false }
holon_type GetEssentialContent.CommandType existing { type_name GetEssentialContent extends CommandType.HolonType abstract false }
holon_type Summarize.CommandType existing { type_name Summarize extends CommandType.HolonType abstract false }
holon_type GetHolonId.CommandType existing { type_name GetHolonId extends CommandType.HolonType abstract false }
holon_type GetPredecessor.CommandType existing { type_name GetPredecessor extends CommandType.HolonType abstract false }
holon_type GetKey.CommandType existing { type_name GetKey extends CommandType.HolonType abstract false }
holon_type GetVersionedKey.CommandType existing { type_name GetVersionedKey extends CommandType.HolonType abstract false }
holon_type GetPropertyValue.CommandType existing { type_name GetPropertyValue extends CommandType.HolonType abstract false }
holon_type GetRelatedHolons.CommandType existing { type_name GetRelatedHolons extends CommandType.HolonType abstract false }
holon_type WithPropertyValue.CommandType existing { type_name WithPropertyValue extends CommandType.HolonType abstract false }
holon_type RemovePropertyValue.CommandType existing { type_name RemovePropertyValue extends CommandType.HolonType abstract false }
holon_type AddRelatedHolons.CommandType existing { type_name AddRelatedHolons extends CommandType.HolonType abstract false }
holon_type RemoveRelatedHolons.CommandType existing { type_name RemoveRelatedHolons extends CommandType.HolonType abstract false }
holon_type WithDescriptor.CommandType existing { type_name WithDescriptor extends CommandType.HolonType abstract false }
holon_type Commit.CommandType existing { type_name Commit extends CommandType.HolonType abstract false }
holon_type UndoLast.CommandType existing { type_name UndoLast extends CommandType.HolonType abstract false }
holon_type RedoLast.CommandType existing { type_name RedoLast extends CommandType.HolonType abstract false }
holon_type UndoToMarker.CommandType existing { type_name UndoToMarker extends CommandType.HolonType abstract false }
holon_type RedoToMarker.CommandType existing { type_name RedoToMarker extends CommandType.HolonType abstract false }
holon_type LoadHolons.CommandType existing { type_name LoadHolons extends CommandType.HolonType abstract false }

holon_type Dance.CommandType existing {
  type_name Dance
  extends CommandType.HolonType
  abstract false
}

holon_type Query.CommandType existing {
  type_name Query
  extends CommandType.HolonType
  abstract false
}

holon_type GetAllHolons.CommandType existing { type_name GetAllHolons extends CommandType.HolonType abstract false }
holon_type GetStagedHolonByBaseKey.CommandType existing { type_name GetStagedHolonByBaseKey extends CommandType.HolonType abstract false }
holon_type GetStagedHolonsByBaseKey.CommandType existing { type_name GetStagedHolonsByBaseKey extends CommandType.HolonType abstract false }
holon_type GetStagedHolonByVersionedKey.CommandType existing { type_name GetStagedHolonByVersionedKey extends CommandType.HolonType abstract false }
holon_type GetTransientHolonByBaseKey.CommandType existing { type_name GetTransientHolonByBaseKey extends CommandType.HolonType abstract false }
holon_type GetTransientHolonByVersionedKey.CommandType existing { type_name GetTransientHolonByVersionedKey extends CommandType.HolonType abstract false }
holon_type GetStagedCount.CommandType existing { type_name GetStagedCount extends CommandType.HolonType abstract false }
holon_type GetTransientCount.CommandType existing { type_name GetTransientCount extends CommandType.HolonType abstract false }
holon_type NewHolon.CommandType existing { type_name NewHolon extends CommandType.HolonType abstract false }
holon_type StageNewHolon.CommandType existing { type_name StageNewHolon extends CommandType.HolonType abstract false }
holon_type StageNewFromClone.CommandType existing { type_name StageNewFromClone extends CommandType.HolonType abstract false }
holon_type StageNewVersion.CommandType existing { type_name StageNewVersion extends CommandType.HolonType abstract false }
holon_type StageNewVersionFromId.CommandType existing { type_name StageNewVersionFromId extends CommandType.HolonType abstract false }
holon_type DeleteHolon.CommandType existing { type_name DeleteHolon extends CommandType.HolonType abstract false }

relationship_type (HolonType)-[AffordsCommand]->(CommandType.HolonType) existing {
  type_name AffordsCommand
  source HolonType
  target CommandType.HolonType
  inverse (CommandType.HolonType)-[AffordedBy]->(HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (CommandType.HolonType)-[AffordedBy]->(HolonType) existing {
  type_name AffordedBy
  source CommandType.HolonType
  target HolonType
  inverse (HolonType)-[AffordsCommand]->(CommandType.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_assertion Transaction.HolonType existing {
  AffordsCommand
    Commit.CommandType
    UndoLast.CommandType
    RedoLast.CommandType
    UndoToMarker.CommandType
    RedoToMarker.CommandType
    LoadHolons.CommandType
    Dance.CommandType
    Query.CommandType
    GetAllHolons.CommandType
    GetStagedHolonByBaseKey.CommandType
    GetStagedHolonsByBaseKey.CommandType
    GetStagedHolonByVersionedKey.CommandType
    GetTransientHolonByBaseKey.CommandType
    GetTransientHolonByVersionedKey.CommandType
    GetStagedCount.CommandType
    GetTransientCount.CommandType
    NewHolon.CommandType
    StageNewHolon.CommandType
    StageNewFromClone.CommandType
    StageNewVersion.CommandType
    StageNewVersionFromId.CommandType
    DeleteHolon.CommandType
}
```

Suggested Command schema sharpening:

```map-schema-dsl
relationship_type (CommandType.HolonType)-[CommandPayloadType]->(HolonType) suggested-change {
  type_name CommandPayloadType
  source CommandType.HolonType
  target HolonType
  inverse (HolonType)-[CommandPayloadTypeFor]->(CommandType.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (HolonType)-[CommandPayloadTypeFor]->(CommandType.HolonType) suggested-change {
  type_name CommandPayloadTypeFor
  source HolonType
  target CommandType.HolonType
  inverse (CommandType.HolonType)-[CommandPayloadType]->(HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_assertion Dance.CommandType suggested-change {
  CommandPayloadType DanceInvocation.HolonType
}

relationship_assertion Query.CommandType suggested-change {
  deprecated_by Dance.CommandType
  note "If retained, Query.CommandType should lower to Dance.CommandType with a QueryDance invocation."
}
```

## Dance Schema

This DSL normalizes the intended Dance seam directly. The status markers show
which parts are already present in generated schema and which still need to be
carried back into the Airtable source.

The intended Dance schema is:

```text
DanceType.HolonType
  DanceInput -> HolonType
  Response   -> DanceResponseType.HolonType

DanceInvocation.HolonType
  AffordingHolon -> HolonType
```

Annotation: this allows a dance input to be a fixed-shape holon rather than
forcing it into the `Projection` family, and it names the subject holon as the
holon affording the dance rather than implying it is merely the target object
of the dance.

```map-schema-dsl
holon_type DanceType.HolonType suggested-change {
  type_name DanceType
  extends HolonType
  abstract true
  properties
    DanceDescription.PropertyType
  relationships
    (DanceType.HolonType)-[DanceInput]->(HolonType)
    (DanceType.HolonType)-[Response]->(DanceResponseType.HolonType)
}

holon_type DanceInvocation.HolonType suggested-change {
  type_name DanceInvocation
  extends HolonType
  abstract false
  properties
    Context.PropertyType
  relationships
    (DanceInvocation.HolonType)-[InvokesDance]->(DanceType.HolonType)
    (DanceInvocation.HolonType)-[AffordingHolon]->(HolonType)
    (DanceInvocation.HolonType)-[Request]->(HolonType)
}

Narrative (non-normative)

`AffordingHolon -> HolonType` remains intentionally general. Any holon instance
may serve as the affording holon for a dance invocation, provided that the
instance's effective descriptor affords the dance referenced by
`InvokesDance`.

In other words, the schema-level relationship target is broad, but invocation
validity is constrained by an instance-level affordance rule:

```text
if invocation.InvokesDance = D
and invocation.AffordingHolon = H
then H must be an instance whose type affords D
```

For query execution, `HolonSpace` is the ordinary affording holon in the
current design, but that is a specialization of this rule, not a narrowing of
the base `DanceInvocation` schema.

holon_type DanceResponseType.HolonType existing {
  type_name DanceResponseType
  extends HolonType
  abstract true
  relationships
    (DanceResponseType.HolonType)-[ResponseBody]->(HolonType)
    (DanceResponseType.HolonType)-[Diagnostics]->(DanceDiagnostic.HolonType)
}

holon_type ResponseBodyType.HolonType existing {
  type_name ResponseBodyType
  extends HolonType
  abstract true
  note "Deprecated old-world response body base. New-world response bodies are ordinary holon types."
}

holon_type DanceImplementation.HolonType existing {
  type_name DanceImplementation
  extends HolonType
  abstract false
  properties
    Engine.PropertyType
    ModuleRef.PropertyType
    Entrypoint.PropertyType
    AbiId.PropertyType
    Version.PropertyType
    Compat.PropertyType
    DanceSummary.PropertyType
  relationships
    (DanceImplementation.HolonType)-[ForDance]->(DanceType.HolonType)
}

holon_type DanceDiagnostic.HolonType existing {
  type_name DanceDiagnostic
  extends HolonType
  abstract false
  properties
    DanceDiagnosticSeverity.PropertyType
    DiagnosticCode.PropertyType
    DiagnosticMessage.PropertyType
}

holon_type Projection.HolonType existing {
  type_name Projection
  extends HolonType
  abstract true
}

property_type DanceName.PropertyType existing { type_name DanceName value_type MapStringValueType }
property_type DanceDescription.PropertyType existing { type_name DanceDescription value_type MapStringValueType }
property_type Context.PropertyType existing { type_name Context value_type InvocationSource }
property_type DanceDiagnosticSeverity.PropertyType existing { type_name DanceDiagnosticSeverity value_type DanceDiagnosticSeverity }
property_type DiagnosticCode.PropertyType existing { type_name DiagnosticCode value_type MapStringValueType }
property_type DiagnosticMessage.PropertyType existing { type_name DiagnosticMessage value_type MapStringValueType }
property_type ResponseStatusCode.PropertyType existing { type_name ResponseStatusCode value_type ResponseStatusCode }
property_type Engine.PropertyType existing { type_name Engine value_type DanceEngine }
property_type ModuleRef.PropertyType existing { type_name ModuleRef value_type MapStringValueType }
property_type Entrypoint.PropertyType existing { type_name Entrypoint value_type MapStringValueType }
property_type AbiId.PropertyType existing { type_name AbiId value_type MapStringValueType }
property_type Version.PropertyType existing { type_name Version value_type MapStringValueType }
property_type Compat.PropertyType existing { type_name Compat value_type MapStringValueType }
property_type DanceSummary.PropertyType existing { type_name DanceSummary value_type MapStringValueType }

value_type InvocationSource existing {
  type_name InvocationSource
  kind TypeKind.Value.Enum
  variants
    InvocationSource.ClientCommand
    InvocationSource.TrustChannel
    InvocationSource.Internal
}

value_type DanceDiagnosticSeverity existing {
  type_name DanceDiagnosticSeverity
  kind TypeKind.Value.Enum
  variants
    DanceDiagnosticSeverity.Info
    DanceDiagnosticSeverity.Warning
}

value_type ResponseStatusCode existing {
  type_name ResponseStatusCode
  kind TypeKind.Value.Enum
  variants
    ResponseStatusCode.OK
    ResponseStatusCode.Accepted
    ResponseStatusCode.BadRequest
    ResponseStatusCode.Unauthorized
    ResponseStatusCode.Forbidden
    ResponseStatusCode.NotFound
    ResponseStatusCode.Conflict
    ResponseStatusCode.UnprocessableEntity
    ResponseStatusCode.ServerError
    ResponseStatusCode.NotImplemented
    ResponseStatusCode.ServiceUnavailable
}

value_type DanceEngine existing {
  type_name DanceEngine
  kind TypeKind.Value.Enum
  variants
    DanceEngine.WasmWasi
    DanceEngine.Process
    DanceEngine.RustDylib
    DanceEngine.Builtin
}
```

Dance relationship types:

```map-schema-dsl
relationship_type (HolonType)-[Affords]->(DanceType.HolonType) existing {
  type_name Affords
  source HolonType
  target DanceType.HolonType
  inverse (DanceType.HolonType)-[AffordedBy]->(HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceType.HolonType)-[AffordedBy]->(HolonType) existing {
  type_name AffordedBy
  source DanceType.HolonType
  target HolonType
  inverse (HolonType)-[Affords]->(DanceType.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (TypeDescriptor.HolonType)-[ImplementsDance]->(DanceImplementation.HolonType) existing {
  type_name ImplementsDance
  source TypeDescriptor.HolonType
  target DanceImplementation.HolonType
  inverse (DanceImplementation.HolonType)-[ImplementedFor]->(TypeDescriptor.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceImplementation.HolonType)-[ImplementedFor]->(TypeDescriptor.HolonType) existing {
  type_name ImplementedFor
  source DanceImplementation.HolonType
  target TypeDescriptor.HolonType
  inverse (TypeDescriptor.HolonType)-[ImplementsDance]->(DanceImplementation.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceImplementation.HolonType)-[ForDance]->(DanceType.HolonType) existing {
  type_name ForDance
  source DanceImplementation.HolonType
  target DanceType.HolonType
  inverse (DanceType.HolonType)-[HasImplementation]->(DanceImplementation.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (DanceType.HolonType)-[HasImplementation]->(DanceImplementation.HolonType) existing {
  type_name HasImplementation
  source DanceType.HolonType
  target DanceImplementation.HolonType
  inverse (DanceImplementation.HolonType)-[ForDance]->(DanceType.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceType.HolonType)-[DanceInput]->(HolonType) suggested-change {
  type_name DanceInput
  source DanceType.HolonType
  target HolonType
  inverse (HolonType)-[DanceInputFor]->(DanceType.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (HolonType)-[DanceInputFor]->(DanceType.HolonType) suggested-change {
  type_name DanceInputFor
  source HolonType
  target DanceType.HolonType
  inverse (DanceType.HolonType)-[DanceInput]->(HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceType.HolonType)-[Response]->(DanceResponseType.HolonType) existing {
  type_name Response
  source DanceType.HolonType
  target DanceResponseType.HolonType
  inverse (DanceResponseType.HolonType)-[ResponseFor]->(DanceType.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (DanceResponseType.HolonType)-[ResponseFor]->(DanceType.HolonType) existing {
  type_name ResponseFor
  source DanceResponseType.HolonType
  target DanceType.HolonType
  inverse (DanceType.HolonType)-[Response]->(DanceResponseType.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 1..32767
}

relationship_type (DanceResponseType.HolonType)-[ResponseBody]->(HolonType) existing {
  type_name ResponseBody
  source DanceResponseType.HolonType
  target HolonType
  inverse (HolonType)-[ResponseBodyFor]->(DanceResponseType.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (HolonType)-[ResponseBodyFor]->(DanceResponseType.HolonType) existing {
  type_name ResponseBodyFor
  source HolonType
  target DanceResponseType.HolonType
  inverse (DanceResponseType.HolonType)-[ResponseBody]->(HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceInvocation.HolonType)-[InvokesDance]->(DanceType.HolonType) existing {
  type_name InvokesDance
  source DanceInvocation.HolonType
  target DanceType.HolonType
  inverse (DanceType.HolonType)-[InvokedBy]->(DanceInvocation.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (DanceType.HolonType)-[InvokedBy]->(DanceInvocation.HolonType) suggested-change {
  type_name InvokedBy
  source DanceType.HolonType
  target DanceInvocation.HolonType
  inverse (DanceInvocation.HolonType)-[InvokesDance]->(DanceType.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceInvocation.HolonType)-[AffordingHolon]->(HolonType) suggested-change {
  type_name AffordingHolon
  source DanceInvocation.HolonType
  target HolonType
  inverse (HolonType)-[AffordsDanceInvocation]->(DanceInvocation.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (HolonType)-[AffordsDanceInvocation]->(DanceInvocation.HolonType) suggested-change {
  type_name AffordsDanceInvocation
  source HolonType
  target DanceInvocation.HolonType
  inverse (DanceInvocation.HolonType)-[AffordingHolon]->(HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceInvocation.HolonType)-[Request]->(HolonType) existing {
  type_name Request
  source DanceInvocation.HolonType
  target HolonType
  inverse (HolonType)-[RequestFor]->(DanceInvocation.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (HolonType)-[RequestFor]->(DanceInvocation.HolonType) existing {
  type_name RequestFor
  source HolonType
  target DanceInvocation.HolonType
  inverse (DanceInvocation.HolonType)-[Request]->(HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceResponseType.HolonType)-[Diagnostics]->(DanceDiagnostic.HolonType) existing {
  type_name Diagnostics
  source DanceResponseType.HolonType
  target DanceDiagnostic.HolonType
  inverse (DanceDiagnostic.HolonType)-[DiagnosticFor]->(DanceResponseType.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (DanceDiagnostic.HolonType)-[DiagnosticFor]->(DanceResponseType.HolonType) existing {
  type_name DiagnosticFor
  source DanceDiagnostic.HolonType
  target DanceResponseType.HolonType
  inverse (DanceResponseType.HolonType)-[Diagnostics]->(DanceDiagnostic.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}
```

## Query Schema

The Query schema is proposed. It depends on the Core and Dance schemas, but it
does not replace either one. Query execution remains a Dance. The query itself
is the request payload of that Dance.

This draft treats `DanceInput` as the correct normative seam for dance request
contracts:

```text
DanceType.HolonType
  DanceInput -> HolonType
```

This removes the pressure to pretend every dance request is a `Projection`.
`Projection.HolonType` remains useful for value-shaped parameter and result
artifacts, but a dance request can now be any ordinary holon type with a fixed
structure.

To stay true to the query algebra design spec, the query schema keeps these
invariants:

- `QueryGraph` is symbolic structure only.
- `ExecutionInstance` owns runtime execution state for one execution of one request.
- `HolonCollection` is the primary runtime carrier.
- Every initial query step consumes a `HolonCollection` and produces a `HolonCollection`.
- `Project` still returns a `HolonCollection`, specifically a collection of `Projection` references.
- `QueryStep` chains through `StepDependsOn`; only root steps explicitly consume request-supplied initial bindings.

In this query design, `QueryDanceRequest` is a fixed-shape request holon:

```text
QueryDanceRequest
  QueryGraph      -> QueryGraph
  InitialBindings -> ExecutionBinding
```

The external result of query execution is simply a `HolonCollection.HolonType`.
Runtime bindings and transient execution results belong to `ExecutionInstance`,
an ephemeral runtime holon, not to `QueryGraph` and not to a separate
`QueryResult` wrapper.

`QueryBinding` is symbolic only. It carries the variable name used by the plan.
`ExecutionBinding` is the binding shape that associates a `QueryBinding` with a
`HolonCollection`. A `QueryDanceRequest` may supply initial bindings in that
shape; once execution is underway, the live binding set belongs to
`ExecutionInstance`.

`QueryStep` is intentionally chain-oriented in this draft. Non-root steps
consume the output of predecessor steps through `StepDependsOn`. Only root steps
should use `UsesInitialBinding` to name a request-supplied starting binding.

The generated schema still needs to be regenerated from Airtable to pick up the
`DanceInput` and `AffordingHolon` changes reflected normatively in this DSL.

```map-schema-dsl
schema MAP Query Schema-v0.0.1 proposed {
  depends_on MAP Core Schema-v0.0.7
  depends_on MAP Dance Schema-v0.0.4
}

holon_type QueryDanceRequest.HolonType proposed {
  type_name QueryDanceRequest
  extends HolonType
  abstract false
  relationships
    (QueryDanceRequest.HolonType)-[QueryGraph]->(QueryGraph.HolonType)
    (QueryDanceRequest.HolonType)-[InitialBindings]->(ExecutionBinding.HolonType)
}
```

Narrative (non-normative):

`QueryDanceRequest` is the fixed-shape input contract for a query dance. It
contains the symbolic plan to execute and the caller-supplied starting bindings
for that execution. This keeps the request compact and explicit: what plan is
being executed, and what named collections is that plan starting from.

```map-schema-dsl
holon_type QueryDanceResponse.DanceResponseType proposed {
  type_name QueryDanceResponse
  extends DanceResponseType.HolonType
  abstract false
  relationships
    (DanceResponseType.HolonType)-[ResponseBody]->(HolonCollection.HolonType)
}
```

Narrative (non-normative):

`QueryDanceResponse` is intentionally simple. A query run returns a
`HolonCollection`, not a special query-only result wrapper. Diagnostics and
status live at the dance-response layer and execution state lives on
`ExecutionInstance`, but the query's externally meaningful payload is just the
result collection.

```map-schema-dsl
holon_type QueryGraph.HolonType proposed {
  type_name QueryGraph
  extends HolonType
  abstract false
  properties
    QueryName.PropertyType
    QueryDescription.PropertyType
  relationships
    (QueryGraph.HolonType)-[QuerySteps]->(QueryStep.HolonType)
    (QueryGraph.HolonType)-[DeclaredInputBindings]->(QueryBinding.HolonType)
    (QueryGraph.HolonType)-[DeclaredResultBinding]->(QueryBinding.HolonType)
}
```

Narrative (non-normative):

`QueryGraph` is the symbolic query plan. It is the reusable, saveable,
shareable artifact that describes what the query means without carrying live
runtime state.

`QuerySteps` is the body of the plan: the operations owned by this query graph.
The graph may be linear, tree-shaped, or eventually fully graph-shaped. The
topology is expressed by the steps and their dependency relationships, not by
runtime collections.

`DeclaredInputBindings` defines the graph's external input contract. These are
the symbolic binding names the plan is allowed to expect from a caller. They do
not contain runtime collections themselves. Instead, they declare the names that
may be satisfied by `QueryDanceRequest.InitialBindings`.

`DeclaredResultBinding` defines the graph's exported output contract. A plan may
create several intermediate named bindings, but exactly one declared binding is
designated as the graph's externally meaningful result. That is the binding
whose runtime value should be treated as the query result when execution
completes.

So in plain terms:

- `DeclaredInputBindings` = the named inputs the query accepts
- `DeclaredResultBinding` = the named output the query promises
- `QuerySteps` = the transformations in between

```map-schema-dsl
holon_type QueryStep.HolonType proposed {
  type_name QueryStep
  extends HolonType
  abstract false
  properties
    StepOrdinal.PropertyType
    StepLabel.PropertyType
  relationships
    (QueryStep.HolonType)-[StepKind]->(QueryStepKind.HolonType)
    (QueryStep.HolonType)-[UsesInitialBinding]->(QueryBinding.HolonType)
    (QueryStep.HolonType)-[StepOutputBinding]->(QueryBinding.HolonType)
    (QueryStep.HolonType)-[StepParameters]->(Projection.HolonType)
    (QueryStep.HolonType)-[StepDependsOn]->(QueryStep.HolonType)
}
```

Narrative (non-normative):

`QueryStep` is intentionally small in this draft. A step says what kind of
operation it is, what parameters that operation needs, what earlier steps it
depends on, and optionally what symbolic binding name should be attached to its
output.

This is a chain-oriented model. Most steps do not explicitly name their input;
they consume the output of predecessor steps through `StepDependsOn`. Only a
root step uses `UsesInitialBinding`, which is how a query graph explicitly says
which caller-supplied starting binding it consumes.

`StepOutputBinding` is optional because not every intermediate result needs a
stable symbolic name. A step may simply feed the next step structurally through
the dependency chain. When a name is useful for external result designation,
branching, reuse, or explanation, the step can expose one.

```map-schema-dsl
holon_type QueryStepKind.HolonType proposed {
  type_name QueryStepKind
  extends HolonType
  abstract true
  relationships
    (QueryStepKind.HolonType)-[StepInputType]->(HolonCollection.HolonType)
    (QueryStepKind.HolonType)-[StepResultType]->(HolonCollection.HolonType)
    (QueryStepKind.HolonType)-[StepParameterType]->(Projection.HolonType)
}

holon_type QueryBinding.HolonType proposed {
  type_name QueryBinding
  extends HolonType
  abstract false
  properties
    BindingName.PropertyType
}

holon_type ExecutionInstance.HolonType proposed {
  type_name ExecutionInstance
  extends HolonType
  abstract false
  properties
    ExecutionStatus.PropertyType
  relationships
    (ExecutionInstance.HolonType)-[ExecutesRequest]->(QueryDanceRequest.HolonType)
    (ExecutionInstance.HolonType)-[ExecutionBindings]->(ExecutionBinding.HolonType)
    (ExecutionInstance.HolonType)-[ExecutionResult]->(HolonCollection.HolonType)
}
```

Narrative (non-normative):

`ExecutionInstance` is one ephemeral runtime execution of one
`QueryDanceRequest`. It is where live execution state belongs.

`ExecutesRequest` ties the run back to the request specification that produced
it. That makes the plan, the initial bindings, and the execution provenance
reachable without duplicating them on the runtime instance.

`ExecutionBindings` is the live binding map as execution proceeds. It may begin
from the request's initial bindings and then grow or change as steps produce new
results.

`ExecutionResult` is the final result collection for that run. It remains
separate from the request and separate from the query graph because it is a
runtime artifact, not part of the symbolic plan.

```map-schema-dsl
holon_type ExecutionBinding.HolonType proposed {
  type_name ExecutionBinding
  extends HolonType
  abstract false
  relationships
    (ExecutionBinding.HolonType)-[BindsQueryVariable]->(QueryBinding.HolonType)
    (ExecutionBinding.HolonType)-[BoundCollection]->(HolonCollection.HolonType)
}

holon_type ExpandParameters.Projection proposed {
  type_name ExpandParameters
  extends Projection.HolonType
  abstract false
  properties
    RelationshipName.PropertyType
}

holon_type FilterParameters.Projection proposed {
  type_name FilterParameters
  extends Projection.HolonType
  abstract false
  relationships
    (FilterParameters.Projection)-[FilterRules]->(FilterRule.HolonType)
}

holon_type ProjectParameters.Projection proposed {
  type_name ProjectParameters
  extends Projection.HolonType
  abstract false
  properties
    PropertyNameList.PropertyType
}

holon_type OrderByParameters.Projection proposed {
  type_name OrderByParameters
  extends Projection.HolonType
  abstract false
  relationships
    (OrderByParameters.Projection)-[OrderByRules]->(OrderByRule.HolonType)
}

holon_type LimitParameters.Projection proposed {
  type_name LimitParameters
  extends Projection.HolonType
  abstract false
  properties
    LimitCount.PropertyType
}

holon_type SkipParameters.Projection proposed {
  type_name SkipParameters
  extends Projection.HolonType
  abstract false
  properties
    SkipCount.PropertyType
}

holon_type FilterRule.HolonType proposed {
  type_name FilterRule
  extends HolonType
  abstract false
  note "Concrete filter rule structure remains to be specified. This holon type exists so filter semantics are modeled structurally rather than as opaque expression strings."
}

holon_type OrderByRule.HolonType proposed {
  type_name OrderByRule
  extends HolonType
  abstract false
  note "Concrete ordering rule structure remains to be specified. This holon type exists so ordering semantics are modeled structurally rather than as opaque expression strings."
}
```

Query property and value types:

```map-schema-dsl
property_type QueryName.PropertyType proposed { type_name QueryName value_type MapStringValueType }
property_type QueryDescription.PropertyType proposed { type_name QueryDescription value_type MapStringValueType }
property_type BindingName.PropertyType proposed { type_name BindingName value_type MapStringValueType }
property_type StepOrdinal.PropertyType proposed { type_name StepOrdinal value_type MapIntegerValueType }
property_type StepLabel.PropertyType proposed { type_name StepLabel value_type MapStringValueType }
property_type ExecutionStatus.PropertyType proposed { type_name ExecutionStatus value_type ExecutionStatus }
property_type RelationshipName.PropertyType proposed { type_name RelationshipName value_type MapStringValueType }
property_type PropertyNameList.PropertyType proposed { type_name PropertyNameList value_type ValueArrayValueType }
property_type LimitCount.PropertyType proposed { type_name LimitCount value_type MapIntegerValueType }
property_type SkipCount.PropertyType proposed { type_name SkipCount value_type MapIntegerValueType }

note proposed {
  "PropertyNameList should be a ValueArrayValueType whose element value type is PropertyName."
}

value_type PropertyName proposed {
  type_name PropertyName
  kind TypeKind.Value.String
}

value_type ExecutionStatus proposed {
  type_name ExecutionStatus
  kind TypeKind.Value.Enum
  variants
    ExecutionStatus.Pending
    ExecutionStatus.Running
    ExecutionStatus.Complete
    ExecutionStatus.Failed
}
```

Query relationship types:

```map-schema-dsl
relationship_type (QueryDanceRequest.HolonType)-[QueryGraph]->(QueryGraph.HolonType) proposed {
  type_name QueryGraph
  source QueryDanceRequest.HolonType
  target QueryGraph.HolonType
  inverse (QueryGraph.HolonType)-[GraphForQueryDanceRequest]->(QueryDanceRequest.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (QueryGraph.HolonType)-[GraphForQueryDanceRequest]->(QueryDanceRequest.HolonType) proposed {
  type_name GraphForQueryDanceRequest
  source QueryGraph.HolonType
  target QueryDanceRequest.HolonType
  inverse (QueryDanceRequest.HolonType)-[QueryGraph]->(QueryGraph.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_assertion QueryDanceRequest.HolonType proposed {
  QueryGraph QueryGraph.HolonType
  InitialBindings ExecutionBinding.HolonType
}

relationship_type (QueryDanceRequest.HolonType)-[InitialBindings]->(ExecutionBinding.HolonType) proposed {
  type_name InitialBindings
  source QueryDanceRequest.HolonType
  target ExecutionBinding.HolonType
  inverse (ExecutionBinding.HolonType)-[InitialBindingForQueryDanceRequest]->(QueryDanceRequest.HolonType)
  definitional true
  ordered true
  duplicates false
  cardinality 0..32767
}

relationship_type (ExecutionBinding.HolonType)-[InitialBindingForQueryDanceRequest]->(QueryDanceRequest.HolonType) proposed {
  type_name InitialBindingForQueryDanceRequest
  source ExecutionBinding.HolonType
  target QueryDanceRequest.HolonType
  inverse (QueryDanceRequest.HolonType)-[InitialBindings]->(ExecutionBinding.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryGraph.HolonType)-[QuerySteps]->(QueryStep.HolonType) proposed {
  type_name QuerySteps
  source QueryGraph.HolonType
  target QueryStep.HolonType
  inverse (QueryStep.HolonType)-[StepInQueryGraph]->(QueryGraph.HolonType)
  definitional true
  ordered true
  duplicates false
  cardinality 1..32767
}

relationship_type (QueryStep.HolonType)-[StepInQueryGraph]->(QueryGraph.HolonType) proposed {
  type_name StepInQueryGraph
  source QueryStep.HolonType
  target QueryGraph.HolonType
  inverse (QueryGraph.HolonType)-[QuerySteps]->(QueryStep.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (QueryGraph.HolonType)-[DeclaredInputBindings]->(QueryBinding.HolonType) proposed {
  type_name DeclaredInputBindings
  source QueryGraph.HolonType
  target QueryBinding.HolonType
  inverse (QueryBinding.HolonType)-[InputBindingForQueryGraph]->(QueryGraph.HolonType)
  definitional true
  ordered true
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryBinding.HolonType)-[InputBindingForQueryGraph]->(QueryGraph.HolonType) proposed {
  type_name InputBindingForQueryGraph
  source QueryBinding.HolonType
  target QueryGraph.HolonType
  inverse (QueryGraph.HolonType)-[DeclaredInputBindings]->(QueryBinding.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryGraph.HolonType)-[DeclaredResultBinding]->(QueryBinding.HolonType) proposed {
  type_name DeclaredResultBinding
  source QueryGraph.HolonType
  target QueryBinding.HolonType
  inverse (QueryBinding.HolonType)-[ResultBindingForQueryGraph]->(QueryGraph.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (QueryBinding.HolonType)-[ResultBindingForQueryGraph]->(QueryGraph.HolonType) proposed {
  type_name ResultBindingForQueryGraph
  source QueryBinding.HolonType
  target QueryGraph.HolonType
  inverse (QueryGraph.HolonType)-[DeclaredResultBinding]->(QueryBinding.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (QueryStep.HolonType)-[StepKind]->(QueryStepKind.HolonType) proposed {
  type_name StepKind
  source QueryStep.HolonType
  target QueryStepKind.HolonType
  inverse (QueryStepKind.HolonType)-[StepKindFor]->(QueryStep.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (QueryStepKind.HolonType)-[StepKindFor]->(QueryStep.HolonType) proposed {
  type_name StepKindFor
  source QueryStepKind.HolonType
  target QueryStep.HolonType
  inverse (QueryStep.HolonType)-[StepKind]->(QueryStepKind.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryStep.HolonType)-[UsesInitialBinding]->(QueryBinding.HolonType) proposed {
  type_name UsesInitialBinding
  source QueryStep.HolonType
  target QueryBinding.HolonType
  inverse (QueryBinding.HolonType)-[InitialBindingUsedByStep]->(QueryStep.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (QueryBinding.HolonType)-[InitialBindingUsedByStep]->(QueryStep.HolonType) proposed {
  type_name InitialBindingUsedByStep
  source QueryBinding.HolonType
  target QueryStep.HolonType
  inverse (QueryStep.HolonType)-[UsesInitialBinding]->(QueryBinding.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryStep.HolonType)-[StepOutputBinding]->(QueryBinding.HolonType) proposed {
  type_name StepOutputBinding
  source QueryStep.HolonType
  target QueryBinding.HolonType
  inverse (QueryBinding.HolonType)-[OutputBindingForStep]->(QueryStep.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (QueryBinding.HolonType)-[OutputBindingForStep]->(QueryStep.HolonType) proposed {
  type_name OutputBindingForStep
  source QueryBinding.HolonType
  target QueryStep.HolonType
  inverse (QueryStep.HolonType)-[StepOutputBinding]->(QueryBinding.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (QueryStep.HolonType)-[StepParameters]->(Projection.HolonType) proposed {
  type_name StepParameters
  source QueryStep.HolonType
  target Projection.HolonType
  inverse (Projection.HolonType)-[ParametersForStep]->(QueryStep.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (FilterParameters.Projection)-[FilterRules]->(FilterRule.HolonType) proposed {
  type_name FilterRules
  source FilterParameters.Projection
  target FilterRule.HolonType
  inverse (FilterRule.HolonType)-[FilterRuleFor]->(FilterParameters.Projection)
  definitional true
  ordered true
  duplicates false
  cardinality 1..32767
}

relationship_type (FilterRule.HolonType)-[FilterRuleFor]->(FilterParameters.Projection) proposed {
  type_name FilterRuleFor
  source FilterRule.HolonType
  target FilterParameters.Projection
  inverse (FilterParameters.Projection)-[FilterRules]->(FilterRule.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (OrderByParameters.Projection)-[OrderByRules]->(OrderByRule.HolonType) proposed {
  type_name OrderByRules
  source OrderByParameters.Projection
  target OrderByRule.HolonType
  inverse (OrderByRule.HolonType)-[OrderByRuleFor]->(OrderByParameters.Projection)
  definitional true
  ordered true
  duplicates false
  cardinality 1..32767
}

relationship_type (OrderByRule.HolonType)-[OrderByRuleFor]->(OrderByParameters.Projection) proposed {
  type_name OrderByRuleFor
  source OrderByRule.HolonType
  target OrderByParameters.Projection
  inverse (OrderByParameters.Projection)-[OrderByRules]->(OrderByRule.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (Projection.HolonType)-[ParametersForStep]->(QueryStep.HolonType) proposed {
  type_name ParametersForStep
  source Projection.HolonType
  target QueryStep.HolonType
  inverse (QueryStep.HolonType)-[StepParameters]->(Projection.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryStep.HolonType)-[StepDependsOn]->(QueryStep.HolonType) proposed {
  type_name StepDependsOn
  source QueryStep.HolonType
  target QueryStep.HolonType
  inverse (QueryStep.HolonType)-[StepDependedOnBy]->(QueryStep.HolonType)
  definitional true
  ordered true
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryStep.HolonType)-[StepDependedOnBy]->(QueryStep.HolonType) proposed {
  type_name StepDependedOnBy
  source QueryStep.HolonType
  target QueryStep.HolonType
  inverse (QueryStep.HolonType)-[StepDependsOn]->(QueryStep.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryStepKind.HolonType)-[StepInputType]->(HolonCollection.HolonType) proposed {
  type_name StepInputType
  source QueryStepKind.HolonType
  target HolonCollection.HolonType
  inverse (HolonCollection.HolonType)-[InputTypeForStepKind]->(QueryStepKind.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (HolonCollection.HolonType)-[InputTypeForStepKind]->(QueryStepKind.HolonType) proposed {
  type_name InputTypeForStepKind
  source HolonCollection.HolonType
  target QueryStepKind.HolonType
  inverse (QueryStepKind.HolonType)-[StepInputType]->(HolonCollection.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryStepKind.HolonType)-[StepResultType]->(HolonCollection.HolonType) proposed {
  type_name StepResultType
  source QueryStepKind.HolonType
  target HolonCollection.HolonType
  inverse (HolonCollection.HolonType)-[ResultTypeForStepKind]->(QueryStepKind.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (HolonCollection.HolonType)-[ResultTypeForStepKind]->(QueryStepKind.HolonType) proposed {
  type_name ResultTypeForStepKind
  source HolonCollection.HolonType
  target QueryStepKind.HolonType
  inverse (QueryStepKind.HolonType)-[StepResultType]->(HolonCollection.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (QueryStepKind.HolonType)-[StepParameterType]->(Projection.HolonType) proposed {
  type_name StepParameterType
  source QueryStepKind.HolonType
  target Projection.HolonType
  inverse (Projection.HolonType)-[ParameterTypeForStepKind]->(QueryStepKind.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (Projection.HolonType)-[ParameterTypeForStepKind]->(QueryStepKind.HolonType) proposed {
  type_name ParameterTypeForStepKind
  source Projection.HolonType
  target QueryStepKind.HolonType
  inverse (QueryStepKind.HolonType)-[StepParameterType]->(Projection.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (ExecutionInstance.HolonType)-[ExecutesRequest]->(QueryDanceRequest.HolonType) proposed {
  type_name ExecutesRequest
  source ExecutionInstance.HolonType
  target QueryDanceRequest.HolonType
  inverse (QueryDanceRequest.HolonType)-[ExecutedBy]->(ExecutionInstance.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (QueryDanceRequest.HolonType)-[ExecutedBy]->(ExecutionInstance.HolonType) proposed {
  type_name ExecutedBy
  source QueryDanceRequest.HolonType
  target ExecutionInstance.HolonType
  inverse (ExecutionInstance.HolonType)-[ExecutesRequest]->(QueryDanceRequest.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (ExecutionInstance.HolonType)-[ExecutionBindings]->(ExecutionBinding.HolonType) proposed {
  type_name ExecutionBindings
  source ExecutionInstance.HolonType
  target ExecutionBinding.HolonType
  inverse (ExecutionBinding.HolonType)-[BindingForExecutionInstance]->(ExecutionInstance.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (ExecutionBinding.HolonType)-[BindingForExecutionInstance]->(ExecutionInstance.HolonType) proposed {
  type_name BindingForExecutionInstance
  source ExecutionBinding.HolonType
  target ExecutionInstance.HolonType
  inverse (ExecutionInstance.HolonType)-[ExecutionBindings]->(ExecutionBinding.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (ExecutionBinding.HolonType)-[BindsQueryVariable]->(QueryBinding.HolonType) proposed {
  type_name BindsQueryVariable
  source ExecutionBinding.HolonType
  target QueryBinding.HolonType
  inverse (QueryBinding.HolonType)-[ExecutionVariableBinding]->(ExecutionBinding.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (QueryBinding.HolonType)-[ExecutionVariableBinding]->(ExecutionBinding.HolonType) proposed {
  type_name ExecutionVariableBinding
  source QueryBinding.HolonType
  target ExecutionBinding.HolonType
  inverse (ExecutionBinding.HolonType)-[BindsQueryVariable]->(QueryBinding.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (ExecutionBinding.HolonType)-[BoundCollection]->(HolonCollection.HolonType) proposed {
  type_name BoundCollection
  source ExecutionBinding.HolonType
  target HolonCollection.HolonType
  inverse (HolonCollection.HolonType)-[CollectionBoundIn]->(ExecutionBinding.HolonType)
  definitional true
  ordered false
  duplicates false
  cardinality 1..1
}

relationship_type (HolonCollection.HolonType)-[CollectionBoundIn]->(ExecutionBinding.HolonType) proposed {
  type_name CollectionBoundIn
  source HolonCollection.HolonType
  target ExecutionBinding.HolonType
  inverse (ExecutionBinding.HolonType)-[BoundCollection]->(HolonCollection.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_type (ExecutionInstance.HolonType)-[ExecutionResult]->(HolonCollection.HolonType) proposed {
  type_name ExecutionResult
  source ExecutionInstance.HolonType
  target HolonCollection.HolonType
  inverse (HolonCollection.HolonType)-[ResultOfExecution]->(ExecutionInstance.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..1
}

relationship_type (HolonCollection.HolonType)-[ResultOfExecution]->(ExecutionInstance.HolonType) proposed {
  type_name ResultOfExecution
  source HolonCollection.HolonType
  target ExecutionInstance.HolonType
  inverse (ExecutionInstance.HolonType)-[ExecutionResult]->(HolonCollection.HolonType)
  definitional false
  ordered false
  duplicates false
  cardinality 0..32767
}

relationship_assertion ExecutionInstance.HolonType proposed {
  ExecutesRequest QueryDanceRequest.HolonType
  ExecutionBindings ExecutionBinding.HolonType
  ExecutionResult HolonCollection.HolonType
}
```

Concrete query dance and query step declarations:

```map-schema-dsl
holon_type QueryDance.DanceType proposed {
  type_name QueryDance
  extends DanceType.HolonType
  abstract false
  properties
    DanceDescription.PropertyType
  relationships
    (DanceType.HolonType)-[DanceInput]->(HolonType)
    (DanceType.HolonType)-[Response]->(DanceResponseType.HolonType)
    (DanceType.HolonType)-[HasImplementation]->(DanceImplementation.HolonType)
}

relationship_assertion HolonSpace.HolonType proposed {
  Affords QueryDance.DanceType
}

relationship_assertion QueryDance.DanceType proposed {
  DanceInput QueryDanceRequest.HolonType
  Response QueryDanceResponse.DanceResponseType
}

relationship_assertion QueryDanceResponse.DanceResponseType proposed {
  ResponseBody HolonCollection.HolonType
}

holon_instance GraphQueryEngine.DanceImplementation proposed {
  type DanceImplementation.HolonType
  Engine DanceEngine.Builtin
  Entrypoint "execute_query_dance"
  ForDance QueryDance.DanceType
}

holon_type SeedHolonsQueryStepType.HolonType proposed {
  type_name SeedHolonsQueryStepType
  extends QueryStepKind.HolonType
  abstract false
  relationships
    StepResultType HolonCollection.HolonType
}

holon_type ExpandQueryStepType.HolonType proposed {
  type_name ExpandQueryStepType
  extends QueryStepKind.HolonType
  abstract false
  relationships
    StepInputType HolonCollection.HolonType
    StepResultType HolonCollection.HolonType
    StepParameterType ExpandParameters.Projection
}

holon_type FilterQueryStepType.HolonType proposed {
  type_name FilterQueryStepType
  extends QueryStepKind.HolonType
  abstract false
  relationships
    StepInputType HolonCollection.HolonType
    StepResultType HolonCollection.HolonType
    StepParameterType FilterParameters.Projection
}

holon_type ProjectQueryStepType.HolonType proposed {
  type_name ProjectQueryStepType
  extends QueryStepKind.HolonType
  abstract false
  relationships
    StepInputType HolonCollection.HolonType
    StepResultType HolonCollection.HolonType
    StepParameterType ProjectParameters.Projection
}

holon_type OrderByQueryStepType.HolonType proposed {
  type_name OrderByQueryStepType
  extends QueryStepKind.HolonType
  abstract false
  relationships
    StepInputType HolonCollection.HolonType
    StepResultType HolonCollection.HolonType
    StepParameterType OrderByParameters.Projection
}

holon_type SkipQueryStepType.HolonType proposed {
  type_name SkipQueryStepType
  extends QueryStepKind.HolonType
  abstract false
  relationships
    StepInputType HolonCollection.HolonType
    StepResultType HolonCollection.HolonType
    StepParameterType SkipParameters.Projection
}

holon_type LimitQueryStepType.HolonType proposed {
  type_name LimitQueryStepType
  extends QueryStepKind.HolonType
  abstract false
  relationships
    StepInputType HolonCollection.HolonType
    StepResultType HolonCollection.HolonType
    StepParameterType LimitParameters.Projection
}

holon_type DistinctQueryStepType.HolonType proposed {
  type_name DistinctQueryStepType
  extends QueryStepKind.HolonType
  abstract false
  relationships
    StepInputType HolonCollection.HolonType
    StepResultType HolonCollection.HolonType
}

note proposed {
  "This query schema follows the query-algebra spec's initial operation set: SeedHolons, Expand, Filter, OrderBy, Skip, Limit, Distinct, and Project."
}

note proposed {
  "Every initial query step produces HolonCollection. Project produces HolonCollection of Projection references rather than leaving the HolonCollection substrate."
}

note proposed {
  "QueryStep input is normally implicit through StepDependsOn. UsesInitialBinding exists only so a root step can consume a request-supplied initial binding."
}

note proposed {
  "Filter and OrderBy parameterization should be structural. FilterRules and OrderByRules are modeled as holons rather than opaque string-expression properties. Project parameterization is a PropertyNameList rather than a free-form projection expression string."
}
```

## Cross-Schema Seam

```map-schema-dsl
seam CommandToDanceToQuery proposed {
  command_surface Dance.CommandType
  command_payload DanceInvocation.HolonType
  dance_type QueryDance.DanceType
  dance_request QueryDanceRequest.HolonType
  query_graph QueryGraph.HolonType
  initial_bindings ExecutionBinding.HolonType
  execution_instance ExecutionInstance.HolonType
  dance_response QueryDanceResponse.DanceResponseType
  response_body HolonCollection.HolonType
}
```

Narrative (non-normative):

This seam definition summarizes the whole design in one place.

- `Dance.CommandType` is the command surface.
- `DanceInvocation.HolonType` is the command payload that says which dance is
  being invoked and with what request.
- `QueryDanceRequest.HolonType` is the structured query request.
- `QueryGraph.HolonType` is the symbolic plan.
- `ExecutionBinding.HolonType` supplies named input collections.
- `ExecutionInstance.HolonType` is the runtime realization of one execution.
- `QueryDanceResponse.DanceResponseType` returns the final
  `HolonCollection.HolonType`.

This keeps the layers distinct:

- command = ingress and lifecycle
- dance = afforded executable behavior
- query = symbolic plan plus named inputs
- execution instance = ephemeral runtime state
- holon collection = runtime query result substrate

The seam means:

```text
A query is not a command.
A query is not a dance.
A query is the payload supplied to a QueryDance through DanceInvocation.Request.
```

## Rust Wrapper Layer (Design Only)

The schema above is now sharp enough to justify a typed Rust wrapper layer.
This section is design documentation only. It does not propose immediate
implementation work.

Narrative (non-normative):

The purpose of these wrappers is not to duplicate holon state in Rust structs.
The purpose is to make intent explicit where a bare `HolonReference` is too
generic. A `HolonReference` can point at anything. A `QueryGraphHolon` tells the
reader, the compiler, and future APIs that this reference is intended to be a
`QueryGraph.HolonType`.

This follows the same spirit as existing command-layer domain structs such as
`TransactionCommand` and `HolonCommand` in `map_commands_contract`: use small
domain-shaped Rust types to make boundary and intent explicit. Unlike those
command structs, these query wrappers should keep all holon state inside the
referenced holon itself rather than mirroring fields into Rust struct storage.

### Standard Wrapper Pattern

```rust
use holons_core::reference_layer::HolonReference;
use holons_core::HolonError;

pub trait TypedHolon: Sized {
    const EXPECTED_TYPE_NAME: &'static str;

    fn try_new(holon_ref: HolonReference) -> Result<Self, HolonError>;
}
```

Recommended concrete pattern:

```rust
#[derive(Clone, Debug)]
pub struct QueryGraphHolon {
    holon_ref: HolonReference,
}

impl TypedHolon for QueryGraphHolon {
    const EXPECTED_TYPE_NAME: &'static str = "QueryGraph";

    fn try_new(holon_ref: HolonReference) -> Result<Self, HolonError> {
        // Validate that the reference resolves to the expected holon type.
        Ok(Self { holon_ref })
    }
}
```

Design rules for all wrappers:

- each wrapper owns exactly one `HolonReference`
- no mirrored schema state should be stored in Rust fields
- constructor validation should confirm the referenced holon has the expected type
- public APIs should prefer typed accessor methods over exposing the wrapped reference
- getters should resolve properties and relationships by reading through the holon reference
- relationship-returning getters should return other typed wrappers where possible
- mutating methods should update the underlying holon through the reference layer

The public accessor pattern should follow the spirit of
`holons_core::descriptors::accessor_helpers.rs`: small helpers that enforce
cardinality, type expectations, and error shape at the boundary instead of
making each caller manually inspect related holons and collections.

### Collection Reference Newtype

For query execution in particular, callers often know they expect a reference to
a `HolonCollection`. That expectation should be explicit in the Rust type:

```rust
#[derive(Clone, Debug)]
pub struct HolonCollectionReference {
    holon_ref: HolonReference,
}

impl HolonCollectionReference {
    pub fn try_new(holon_ref: HolonReference) -> Result<Self, HolonError>;

    pub fn single_member(&self) -> Result<HolonReference, HolonError>;

    pub fn optional_single_member(&self) -> Result<Option<HolonReference>, HolonError>;

    pub fn members(&self) -> Result<Vec<HolonReference>, HolonError>;
}
```

Narrative (non-normative):

`HolonCollectionReference` is not a wrapper for the `HolonCollection` holon
type in the same sense as `QueryGraphHolon` or `ExecutionInstanceHolon`. It is a
reference newtype that says: this reference is expected to denote a
`HolonCollection`, and callers want collection-oriented read helpers rather than
a generic `HolonReference`.

### Core Wrapper Types

These are the primary wrappers needed to make the command/dance/query seam clear
in Rust:

```rust
pub struct DanceInvocationHolon { holon_ref: HolonReference }
pub struct QueryDanceTypeHolon { holon_ref: HolonReference }
pub struct QueryDanceRequestHolon { holon_ref: HolonReference }
pub struct QueryDanceResponseHolon { holon_ref: HolonReference }
```

Narrative (non-normative):

These wrappers cover the dance-side seam. They are useful at the boundary where
command dispatch hands off into dance execution and where a caller wants to talk
about a query dance request or response as a first-class domain thing rather
than as an untyped holon reference.

```rust
pub struct QueryGraphHolon { holon_ref: HolonReference }
pub struct QueryStepHolon { holon_ref: HolonReference }
pub struct QueryStepKindHolon { holon_ref: HolonReference }
pub struct QueryBindingHolon { holon_ref: HolonReference }
```

Narrative (non-normative):

These wrappers cover the symbolic query-plan layer.

- `QueryGraphHolon` is the reusable plan.
- `QueryStepHolon` is one operation node in that plan.
- `QueryStepKindHolon` is the step's operation descriptor.
- `QueryBindingHolon` is a symbolic variable name used by the plan.

This is the layer where structure, naming, and topology live, without runtime
values.

```rust
pub struct ExecutionBindingHolon { holon_ref: HolonReference }
pub struct ExecutionInstanceHolon { holon_ref: HolonReference }
pub struct HolonCollectionReference { holon_ref: HolonReference }
```

Narrative (non-normative):

These wrappers cover runtime execution state.

- `ExecutionBindingHolon` ties a symbolic query binding to a runtime collection.
- `ExecutionInstanceHolon` is one ephemeral run of one request.
- `HolonCollectionReference` is the collection-shaped runtime carrier that query
  steps consume and produce.

```rust
pub struct ExpandParametersProjection { holon_ref: HolonReference }
pub struct FilterParametersProjection { holon_ref: HolonReference }
pub struct ProjectParametersProjection { holon_ref: HolonReference }
pub struct OrderByParametersProjection { holon_ref: HolonReference }
pub struct LimitParametersProjection { holon_ref: HolonReference }
pub struct SkipParametersProjection { holon_ref: HolonReference }
```

Narrative (non-normative):

These wrappers are for step-parameter projections. The projection wrappers are
separate because parameter shape belongs to the step configuration, not to the
step kind descriptor and not to the runtime execution state.

```rust
pub struct FilterRuleHolon { holon_ref: HolonReference }
pub struct OrderByRuleHolon { holon_ref: HolonReference }
```

Narrative (non-normative):

`FilterRuleHolon` and `OrderByRuleHolon` are intentionally separate from the
parameter projections because they are expected to grow into small structural
mini-models of their own. That is exactly why they are better modeled as holons
than as opaque string expressions.

These thin wrappers are also useful for concrete step-kind descriptors:

```rust
pub struct SeedHolonsQueryStepTypeHolon { holon_ref: HolonReference }
pub struct ExpandQueryStepTypeHolon { holon_ref: HolonReference }
pub struct FilterQueryStepTypeHolon { holon_ref: HolonReference }
pub struct ProjectQueryStepTypeHolon { holon_ref: HolonReference }
pub struct OrderByQueryStepTypeHolon { holon_ref: HolonReference }
pub struct SkipQueryStepTypeHolon { holon_ref: HolonReference }
pub struct LimitQueryStepTypeHolon { holon_ref: HolonReference }
pub struct DistinctQueryStepTypeHolon { holon_ref: HolonReference }
```

Narrative (non-normative):

These concrete step-kind wrappers are optional but helpful when a caller needs
to branch on a known step kind and then ask kind-specific questions without
dropping back to raw type-name inspection.

### Intent-Conveying APIs

Recommended minimal API surface for the most important wrappers:

```rust
impl DanceInvocationHolon {
    pub fn invoked_dance(&self) -> Result<QueryDanceTypeHolon, HolonError>;
    pub fn affording_holon(&self) -> Result<HolonReference, HolonError>;
    pub fn request(&self) -> Result<QueryDanceRequestHolon, HolonError>;
}

impl QueryDanceRequestHolon {
    pub fn query_graph(&self) -> Result<QueryGraphHolon, HolonError>;
    pub fn initial_bindings(&self) -> Result<Vec<ExecutionBindingHolon>, HolonError>;
}

impl QueryGraphHolon {
    pub fn query_name(&self) -> Result<Option<String>, HolonError>;
    pub fn query_description(&self) -> Result<Option<String>, HolonError>;
    pub fn steps(&self) -> Result<Vec<QueryStepHolon>, HolonError>;
    pub fn declared_input_bindings(&self) -> Result<Vec<QueryBindingHolon>, HolonError>;
    pub fn declared_result_binding(&self) -> Result<QueryBindingHolon, HolonError>;
}

impl QueryStepHolon {
    pub fn ordinal(&self) -> Result<i64, HolonError>;
    pub fn label(&self) -> Result<Option<String>, HolonError>;
    pub fn kind(&self) -> Result<QueryStepKindHolon, HolonError>;
    pub fn depends_on(&self) -> Result<Vec<QueryStepHolon>, HolonError>;
    pub fn uses_initial_binding(&self) -> Result<Option<QueryBindingHolon>, HolonError>;
    pub fn output_binding(&self) -> Result<Option<QueryBindingHolon>, HolonError>;
    pub fn parameters(&self) -> Result<Option<HolonReference>, HolonError>;
}

impl QueryBindingHolon {
    pub fn binding_name(&self) -> Result<String, HolonError>;
}

impl ExecutionBindingHolon {
    pub fn query_variable(&self) -> Result<QueryBindingHolon, HolonError>;
    pub fn bound_collection(&self) -> Result<HolonCollectionReference, HolonError>;
}

impl ExecutionInstanceHolon {
    pub fn executes_request(&self) -> Result<QueryDanceRequestHolon, HolonError>;
    pub fn status(&self) -> Result<String, HolonError>;
    pub fn execution_bindings(&self) -> Result<Vec<ExecutionBindingHolon>, HolonError>;
    pub fn execution_result(&self) -> Result<Option<HolonCollectionReference>, HolonError>;
}

impl ProjectParametersProjection {
    pub fn property_names(&self) -> Result<Vec<String>, HolonError>;
}

impl FilterParametersProjection {
    pub fn filter_rules(&self) -> Result<Vec<FilterRuleHolon>, HolonError>;
}

impl OrderByParametersProjection {
    pub fn order_by_rules(&self) -> Result<Vec<OrderByRuleHolon>, HolonError>;
}
```

### Internal Accessor Helpers

The wrappers should share a small internal helper layer, patterned after
`descriptors/accessor_helpers.rs`, so callers do not repeatedly hand-roll
cardinality and type checks:

```rust
fn require_string(holon: &HolonReference, property_name: &str) -> Result<String, HolonError>;
fn optional_string(holon: &HolonReference, property_name: &str) -> Result<Option<String>, HolonError>;

fn require_single_related_typed<T: TypedHolon>(
    holon: &HolonReference,
    relationship_name: &str,
) -> Result<T, HolonError>;

fn optional_single_related_typed<T: TypedHolon>(
    holon: &HolonReference,
    relationship_name: &str,
) -> Result<Option<T>, HolonError>;

fn related_typed<T: TypedHolon>(
    holon: &HolonReference,
    relationship_name: &str,
) -> Result<Vec<T>, HolonError>;

fn require_collection_reference(
    holon: &HolonReference,
    relationship_name: &str,
) -> Result<HolonCollectionReference, HolonError>;

fn optional_collection_reference(
    holon: &HolonReference,
    relationship_name: &str,
) -> Result<Option<HolonCollectionReference>, HolonError>;
```

Narrative (non-normative):

These helpers should remain internal to the wrapper layer. The point is that a
caller should ask a domain question like `declared_result_binding()` or
`execution_result()` and receive a strongly shaped answer, rather than first
pulling out a raw `HolonReference` and then repeating structural inspection
logic at every call site.

### Typed Parameter Access

`QueryStepHolon::parameters()` should likely remain generic at the lowest level,
because `StepKind` determines which parameter wrapper is valid. A convenience
layer should then provide kind-aware accessors:

```rust
pub enum QueryStepParameters {
    Expand(ExpandParametersProjection),
    Filter(FilterParametersProjection),
    Project(ProjectParametersProjection),
    OrderBy(OrderByParametersProjection),
    Limit(LimitParametersProjection),
    Skip(SkipParametersProjection),
    None,
}

impl QueryStepHolon {
    pub fn typed_parameters(&self) -> Result<QueryStepParameters, HolonError>;
}
```

This keeps the base wrapper honest while still giving callers ergonomic typed
access once the step kind is known.

### Relationship To Runtime Commands

These wrappers should not replace `TransactionCommand`, `HolonCommand`, or
`DanceInvocation`. They sit one layer below those ingress types.

- command-layer structs decide lifecycle and dispatch
- typed holon wrappers express schema intent after a holon reference is in hand
- execution still happens through the underlying reference-layer and command APIs

### Naming Rule

Use Rust type names that make the wrapped holon type unambiguous:

- `<SchemaTypeName>Holon` for holon types
- `<SchemaTypeName>Projection` for projection types

Examples:

- `QueryGraphHolon`
- `QueryStepHolon`
- `ExecutionInstanceHolon`
- `FilterRuleHolon`
- `OrderByParametersProjection`

This avoids ambiguous names like `QueryGraph` or `ExecutionInstance` that could
be confused with non-wrapper domain structs later.

## Suggested Airtable/Core-Schema Changes

These should be made in the Airtable source and then regenerated into JSON.

```map-schema-dsl
suggested-change AddCommandPayloadRelationship {
  add relationship_type (CommandType.HolonType)-[CommandPayloadType]->(HolonType)
  add relationship_type (HolonType)-[CommandPayloadTypeFor]->(CommandType.HolonType)
  add assertion Dance.CommandType CommandPayloadType DanceInvocation.HolonType
}

suggested-change AddInvokesDanceInverse {
  add relationship_type (DanceType.HolonType)-[InvokedBy]->(DanceInvocation.HolonType)
  inverse_of (DanceInvocation.HolonType)-[InvokesDance]->(DanceType.HolonType)
}

suggested-change AlignDanceTypeInputSeam {
  promote relationship_type (DanceType.HolonType)-[DanceInput]->(HolonType)
  promote relationship_type (HolonType)-[DanceInputFor]->(DanceType.HolonType)
  update DanceType.HolonType to declare DanceInput as its normative input seam
  note "Dance input may be any fixed-shape holon type, not only a Projection subtype."
}

suggested-change AlignDanceInvocationSubjectSeam {
  promote relationship_type (DanceInvocation.HolonType)-[AffordingHolon]->(HolonType)
  promote relationship_type (HolonType)-[AffordsDanceInvocation]->(DanceInvocation.HolonType)
  update DanceInvocation.HolonType to declare AffordingHolon as its normative subject seam
  note "The related holon is the subject affording the dance."
}

suggested-change ClarifyQueryCommand {
  either deprecate Query.CommandType
  or define Query.CommandType as compatibility sugar that lowers to:
    Dance.CommandType + DanceInvocation.InvokesDance(QueryDance.DanceType)
}

suggested-change AddQuerySchema {
  add schema MAP Query Schema-v0.0.1
  add all proposed Query holon types, property types, and relationship pairs from this DSL
}

suggested-change QueryDanceRequestAsHolon {
  note "Once DanceInput exists, QueryDanceRequest should be an ordinary holon type rather than a Projection subtype."
  define QueryDanceRequest.HolonType as a concrete fixed-shape request holon
  assert QueryDance.DanceType DanceInput QueryDanceRequest.HolonType
}
```
