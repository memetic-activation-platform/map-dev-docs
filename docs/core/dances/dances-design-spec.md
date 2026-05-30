# MAP Design Spec: Dances, Descriptor Affordances, and Holonic Invocation (v2.0)

## ChangeLog



### v2.0

The old spec (v1.3) has been moved to the archive. Starting a new changelog here. These are the principal changes from 1.3.

- consolidates the revised holonic dance design as the current target posture
- re-centers dance contracts on `DanceType`, `DanceInvocation`,
  `DanceResponseType`, `DanceImplementation`, and `Projection`
- replaces dance-specific wire envelopes with holon-backed invocation and
  response records
- clarifies `Projection` as the base shell for value-shaped request, response,
  and projection-result holons
- simplifies implementation binding so active implementations are selected by
  `ForDance` rather than per-target dynamic dispatch
- restores concrete guidance for query/navigation dance categories under the
  new holonic design
- restores a legacy surface disposition appendix, updated to clarify
  `Deprecated` suffix strategy for deprecated schema descriptors
- adds a Dances DSL authoring section and aligns the spec with the updated MAP
  type-definition DSL work

- **Status:** Draft
- **Intent:** Specify the MAP Dances design: dances are descriptor-afforded behaviors, invocations are holons, responses are holons, and command ingress carries holon references rather than dance-specific wire payloads.
- **Scope:** Dance type definition, afforded dances, request and response shapes, invocation records, response bodies, implementation binding, ABI, command ingress, dispatch, validation, persistence, audit posture, performance, and test migration posture.

---

## 1) Design Summary

A dance is a behavior afforded by a MAP type. The dance is described by a
`DanceType` descriptor. A holon type affords a dance through `Affords`, and
runtime code satisfies that behavior through a `DanceImplementation` selected
for the dance.

A dance invocation is a holon. `DanceInvocation` records the dance being
invoked, the optional target holon, the request holon supplied to the dance, and
the ingress source of the invocation. The invocation record is part of the
holonic model; it is not a bespoke request wire object.

A successful dance response is a holon whose descriptor extends
`DanceResponseType`. The response can point to its structured result body
through `ResponseBody`. Result state lives in normal MAP holon state managers
and is reached by relationship, not embedded in a command payload.

Navigation and query operations are ordinary dances. Operations such as seed,
expand, filter, order, skip, limit, project, and execute-plan are modeled as
dances afforded by the relevant holon types, especially `HolonCollection` and
plan/session holon types. They do not require a separate query command envelope
or row-shaped query runtime.

---

## 2) Relationship to Descriptor Design

The descriptor design owns the structure and interpretation of MAP type
descriptors. It defines how holon types declare properties, relationships,
commands, dances, inheritance, abstract target constraints, and descriptor-local
lookup. The Dances design builds on that foundation; it does not define a
second descriptor system.

Descriptor design owns:

- `TypeDescriptor`, `HolonType`, and the meta-type structure
- `Extends` inheritance and effective descriptor flattening
- `HolonDescriptor` as the caller-facing lookup surface for type structure and
  affordances
- relationship source and target constraints, including abstract target
  constraints such as `HolonType`
- property and relationship validation for ordinary holon state

Dances design owns:

- `DanceType` as the descriptor family for executable behavior
- `Affords` as the behavior affordance from holon types to dances
- `DanceImplementation` as the executable binding model
- `DanceInvocation` as the holonic execution request record
- `DanceResponseType` as the successful response model
- dance dispatch, implementation selection, command ingress, and audit posture

The Dances design must not introduce a second global dance registry, require
callers to reconstruct `Extends` inheritance, detach behavior meaning from
descriptors, or make ABI payload encoding the semantic owner of invocation and
response meaning. A caller asks descriptors what a holon affords; the dance
runtime executes the afforded behavior.

---

## 3) Foundational Assumptions

1. **Self-describing types**
    - MAP types are holons described by descriptor holons.
    - Runtime wrappers are typed views over `HolonReference`.
    - Structural and behavioral affordances are discovered through descriptors.

2. **Descriptor-owned affordance lookup**
    - Dances are behaviors afforded by `HolonType` descriptors.
    - Effective dance lookup is inherited and flattened through `Extends`.
    - `HolonDescriptor` owns the caller-facing dance discovery surface.

3. **Holonic execution records**
    - Dance invocation is represented by `DanceInvocation`.
    - Successful dance response is represented by a holon whose descriptor
      extends `DanceResponseType`.
    - Result state is reached through relationships and `HolonReference`, not
      embedded as command payload state.

4. **Ingress adapters do not own dance meaning**
    - Commands and TrustChannels are ingress paths into dance execution.
    - They carry references and enforce ingress policy.
    - They do not define separate dance request, response, query, or result
      semantics.

5. **Query and navigation are dances**
    - Query and navigation operations are ordinary descriptor-afforded dances.
    - Plural holon-backed results use `HolonCollection`.
    - Projection records are holons described by concrete extensions of
      `Projection`, including `TransientHolonType`s for dynamic projections.
    - Row-shaped query result contracts are not part of the Dances design.

6. **Value semantics stay with value descriptors**
    - Dances do not own scalar value meaning or operator semantics.
    - Value validation and operator support are resolved through
      `ValueDescriptor`.

---

## 4) Dances Schema

The Dances Schema is organized around four primary concepts:

- dance type definition
- dance implementation binding
- dance invocation
- dance response

```text
Abstract HolonType: DanceType
Abstract HolonType: DanceResponseType

HolonType: DanceImplementation
HolonType: DanceInvocation
HolonType: DanceDiagnostic
HolonType: Projection

EnumValueType: InvocationSource
EnumValueType: DanceDiagnosticSeverity
```

Rust may expose typed wrappers over these holon types. For example,
`DanceResponse` is a Rust wrapper around a response holon whose descriptor
extends `DanceResponseType`; it is not a separate schema type.

`Projection` is included as the base type for value-shaped holons. Its core
definition is intentionally only a shell that extends `HolonType`. Concrete
request, response, parameter, and projected-result shapes are expressed by
holon types that extend `Projection` when their state is a property map rather
than a reference to another whole holon. Domain dances define their own
extensions when their contracts require them.

---

## 5) Dance Type Definition

`DanceType` is the abstract type for dance descriptor holons.

```text
Abstract HolonType: DanceType

Properties:
  DanceName
  DanceDescription

Relationships:
  RequestType -> HolonType [0..1]
  Response -> DanceResponseType [1..1]
```

Because `DanceType` descriptors are `TypeDescriptor` holons, ordinary
descriptor metadata such as `type_name`, `display_name`, and `description`
comes from the shared descriptor model. `DanceName` and `DanceDescription` are
the dance-specific fields.

`DanceName` is the stable dance name used for lookup and dispatch.
`DanceDescription` describes what the dance does and when it should be invoked.

`RequestType` declares the holon type expected as the dance's request body. In
plain English, this is the dance's parameter shape. A dance with no request
body leaves `RequestType` absent.

`Response` declares the response holon type returned by successful execution.
The response type extends `DanceResponseType`.

Request body and response body holon types are owned by the dance that declares
them. Core-defined dances may define core request and response body types.
Domain-defined dances define their own request and response body types. The
Dances design does not define a generic `Parameter` holon type just to hold
dance inputs. When a dance needs value-based parameters, its request type can
extend `Projection` and declare the required instance properties directly.

### 5.1) Dance Signature DSL

The holonic representation is the canonical design, but it is verbose for human
authors. A Dances DSL is therefore desirable as a concise authoring surface for
declaring dance signatures. Its purpose is to let a human describe a dance's
inputs, parameter shape, target expectations, and result shape in a compact
form that compiles into the underlying holon types and relationships.

The DSL does not replace the holonic model. It is a shorthand for generating
it. The compiled result is still:

- a `DanceType` descriptor
- a `RequestType`, when the dance accepts a structured request body
- a `DanceResponseType` descriptor
- concrete request, response-body, or projection holon types where needed
- ordinary `Affords`, `Response`, `ResponseBody`, and related schema
  relationships

The DSL should be designed around the same principles as the Rust typed-wrapper
pattern: a concise, human-friendly surface over a holonic internal
representation. The DSL exists to reduce ceremony and authoring mistakes, not
to define a second semantic model.

Authoring goals:

- declare dance signatures in a compact, readable form
- compile deterministically into MAP schema types and relationships
- reuse existing `PropertyType` and `ValueDescriptor` definitions when possible
- support value-shaped request and result bodies through concrete extensions of
  `Projection`
- support query-time dynamic projection shapes through transient types when the
  result shape is not statically known

The DSL should be able to express at least three common cases:

1. target-only dances with no structured request body
2. dances with a value-shaped request body
3. dances with a value-shaped projected result body

Example 1: target-only dance

```text
dance ArchiveNote
  target MeetingNote
  response ArchiveNoteResponse
```

This compiles to a `DanceType` descriptor for `ArchiveNote`, a concrete
response type extending `DanceResponseType`, and an affordance from
`MeetingNote` to `ArchiveNote`. No `RequestType` is generated because the dance
has no structured request body.

Example 2: dance with value-shaped request parameters

```text
dance Summarize
  target Article
  request SummarizeRequest extends Projection
    properties
      max_sentences: PositiveInteger
      tone: SummaryTone
  response SummarizeResponse
  response_body SummaryProjection extends Projection
    properties
      summary_text: LongString
```

This compiles to:

- a `DanceType` descriptor for `Summarize`
- a `SummarizeRequest` holon type extending `Projection`
- a `SummarizeResponse` holon type extending `DanceResponseType`
- a `SummaryProjection` holon type extending `Projection`
- `Summarize -[RequestType]-> SummarizeRequest`
- `Summarize -[Response]-> SummarizeResponse`
- `SummarizeResponse -[ResponseBody]-> SummaryProjection`
- `Article -[Affords]-> Summarize`

Example 3: query-time dynamic projection

```text
dance Project
  target HolonCollection
  request ProjectRequest extends Projection
    properties
      selection_spec: ProjectionSelection
  response ProjectResponse
  response_body transient Projection
```

This expresses that the request shape is known in advance, but the projected
result shape is determined at runtime from the projection specification. The
compiled static schema includes the dance, request type, and response type. At
execution time, the runtime may construct a transient holon type extending
`Projection` to describe the actual projected record shape.

Compilation rules:

- a DSL `request` clause compiles to `DanceType.RequestType`
- a DSL `response` clause compiles to `DanceType.Response`
- a DSL `response_body` clause compiles to `DanceResponseType.ResponseBody`
- value-shaped request or result bodies compile to concrete holon types that
  extend `Projection`
- target declarations compile to `Affords` relationships from the target type
  to the dance
- the generated types remain ordinary MAP schema descriptors and inherit normal
  descriptor fields from `TypeDescriptor`

The DSL should prefer existing property definitions over generating new ones
when the projected or parameter fields already correspond to known MAP
properties. It may define new property types where genuinely needed, such as
aggregate or computed fields that do not correspond to a single existing source
property.

The Dances DSL is a design direction for authoring convenience. The canonical
runtime and persistence model remains the underlying holonic representation.

---

## 6) Afforded Dances

Holon types afford dances through `Affords`.

```text
HolonType -[Affords]-> DanceType
DanceType -[AffordedBy]-> HolonType
```

Interpretation rules:

- `Affords` means instances of the source holon type may invoke the target
  dance.
- Dance affordances inherit through `Extends` using the same descriptor
  flattening rules as other type affordances.
- Callers ask `HolonDescriptor` for effective afforded dances rather than
  walking `Extends` themselves.
- `AffordedBy` is the inverse of `Affords`.

---

## 7) Dance Implementation Binding

`DanceImplementation` describes executable code that can satisfy a dance.

```text
HolonType: DanceImplementation

Properties:
  Engine
  ModuleRef
  Entrypoint
  AbiId
  Version
  Compat
  DanceSummary

Relationships:
  ForDance -> DanceType [1..1]
```

Implementation binding is represented by:

```text
DanceImplementation -[ForDance]-> DanceType
DanceType -[HasImplementation]-> DanceImplementation
```

The descriptor affordance says what behavior exists. The implementation binding
says which executable code may satisfy that dance. Static Rust dispatch and
dynamic module dispatch both satisfy the same model.

`ForDance` names the dance behavior implemented by this executable binding.
Implementation eligibility is by `DanceType`, not by target holon type. If a
holon type effectively affords a dance, any active implementation for that
dance must support that holon type under the dance's declared request,
response, ABI, and semantic contract.

Concrete example:

```text
DanceType:
  Summarize

HolonType descriptors:
  Article
  MeetingNote
  ProjectUpdate

DanceImplementation:
  text-summary-v1

Relationships:
  Article -[Affords]-> Summarize
  MeetingNote -[Affords]-> Summarize
  ProjectUpdate -[Affords]-> Summarize

  text-summary-v1 -[ForDance]-> Summarize
```

In this example, `Article`, `MeetingNote`, and `ProjectUpdate` are holon types,
and all three afford the `Summarize` dance. The `text-summary-v1`
implementation must support all three because it implements `Summarize`. If
`ProjectUpdate` needs a different summary contract or behavior that
`text-summary-v1` cannot satisfy, the model should define a different
`DanceType` for that behavior and have `ProjectUpdate` afford that dance
instead.

Validation rule:

- A `DanceImplementation` must have exactly one `ForDance` target.
- A `DanceImplementation` must honor the declared contract of its `ForDance`
  target for every holon type that effectively affords that dance.
- Holon-type-specific implementation variation is represented by defining a
  distinct `DanceType`.

### 7.1 Deterministic Implementation Selection

For a given invocation, the runtime resolves candidate implementations from the
invoked dance. Candidate selection is deterministic and independent of traversal
order, insertion order, or host-local registration order.

Candidate implementations must satisfy:

- `ForDance` points to the invoked `DanceType`
- `Engine`, `AbiId`, `Version`, and `Compat` are compatible with the host and
  invocation
- runtime policy allows the implementation for the invocation source and
  execution context

Activation-time validation narrows this eligible set before the runtime chooses
or invokes an implementation.

Multiple active implementations for the same `DanceType` must be semantically
interchangeable under that dance's declared contract. Implementation selection
chooses an executable binding for the dance; it is not target-type-specific
method dispatch.

When more than one candidate is eligible, the runtime chooses one using this
stable ordering:

1. host-supported `Engine` and `AbiId` match
2. highest compatible `Version`
3. policy-preferred implementation when policy defines a preference
4. stable implementation identity as the final tiebreaker

If no candidate is eligible, dispatch fails with `HolonError`. If policy
requires uniqueness and the ordering cannot produce a single winner, dispatch
fails rather than choosing nondeterministically.

---

## 8) Dance Invocation

`DanceInvocation` records a request to execute a dance.

```text
HolonType: DanceInvocation

Properties:
  InvocationSource

Relationships:
  InvokesDance -> DanceType [1..1]
  Target -> HolonType [0..1]
  Request -> HolonType [0..1]
```

`InvokesDance` points to the `DanceType` being invoked.

`Target` points to the holon being acted on, when the dance is target-based.
The relationship target constraint is abstract `HolonType`, so the relationship
may point to any holon whose concrete descriptor extends `HolonType`. It does
not point to an instance of abstract `HolonType`.

`Request` points to the actual request holon supplied for this invocation. The
request holon's descriptor must conform to the type declared by
`InvokesDance.RequestType`.

The request model uses distinct names for the type-level contract and the
instance-level request:

```text
DanceType -[RequestType]-> HolonType
DanceInvocation -[Request]-> HolonType
```

The first relationship declares the request type for a dance. The second
relationship points to the concrete request holon for one invocation.

### 8.1 Invocation Source

```text
EnumValueType: InvocationSource

InvocationSource =
  | ClientCommand
  | TrustChannel
  | Internal
```

`InvocationSource` records how the invocation entered the runtime. It is set or
validated by trusted ingress code. For example, the Commands adapter stamps
command-originated invocations as `ClientCommand`; a client cannot claim
`TrustChannel` or `Internal` authority for itself.

Authorization, trust provenance, and capability claims are modeled as
first-class security or provenance holons when needed. They are related to
invocations explicitly rather than hidden as generic optional invocation fields.

---

## 9) Dance Response

A successful dance execution returns a response holon whose descriptor extends
`DanceResponseType`.

```text
Abstract HolonType: DanceResponseType

Relationships:
  ResponseBody -> HolonType [0..1]
  Diagnostics -> DanceDiagnostic [0..*]
```

`ResponseBody` points to the structured result body, when successful execution
produces one. The response body is a holon, not an embedded payload.

`ResponseStatusCode` is retired. Success and failure are represented by the
outer result shape: successful execution returns a response holon, and failed
execution returns `HolonError`.

`OutcomeOf` is dropped as redundant. The runtime already knows which invocation
produced the response during execution, and audit or provenance models can
record that association if they need it.

```text
DanceExecutionResult = Result<DanceResponse, HolonError>
```

### 9.1 Response Body

The response body holon is the result body. It may be a domain result, a scalar
result holon, a `HolonCollection`, a holon described by a concrete extension of
`Projection`, or another concrete holon type promised by the dance's response
contract. In all cases, the result is represented by `HolonReference`; its
concrete shape is given by the referenced holon's `DescribedBy` relationship to
a `HolonType`.

Core response body holon types are defined only for core dances. Domain dances
define their own response body holon types. `HolonCollection` is already a
holon type and can be used for plural holon-backed results.

`Projection` is the base holon type for property-map result bodies. Core dances
that return value projections may define concrete extensions of `Projection`
with the expected instance properties. Query dances may also use incrementally
defined `TransientHolonType`s that extend `Projection` when the projected shape
is known only at runtime. Those transient projection types do not need to be
saved unless the query plan itself is persisted.

Produced state lives in the appropriate MAP state manager:

- `Nursery` for staged holons
- `TransientHolonManager` for transient holons
- `HolonsCache` for saved holons

Across runtime and API boundaries, the response and response body are carried
by `HolonReference`.

### 9.2 Diagnostics

`DanceDiagnostic` records non-fatal notes attached to a successful response.

```text
HolonType: DanceDiagnostic

Properties:
  DanceDiagnosticSeverity
  DiagnosticCode
  DiagnosticMessage
```

```text
EnumValueType: DanceDiagnosticSeverity

DanceDiagnosticSeverity =
  | Info
  | Warning
```

Diagnostics do not replace `HolonError`. A failed invocation returns
`HolonError`; it does not return a successful response with an error-shaped
diagnostic.

### 9.3 Events

The Dances Schema does not define `DanceEvent`.

Event-like artifacts belong in the Dances Schema only when there is a concrete
consumer, such as an outbox, subscription surface, audit stream, or projection
invalidation mechanism. The asynchronous event-handling side of the
architecture is intentionally deferred. If dance events are added later, they
are holons related explicitly to the invocation, response, or response body
they describe.

---

## 10) Command Ingress and Wire Posture

The Commands layer is an ingress adapter for dance execution. It does not
define a second dance request or response model.

Conceptual command signature:

```text
DanceV2(invocation: DanceInvocation) -> Result<DanceResponse, HolonError>
```

Wire-level command signature:

```text
DanceV2(invocation: HolonReference) -> Result<HolonReference, HolonError>
```

The input reference points to a `DanceInvocation` holon. The output reference
points to a concrete response holon whose descriptor extends
`DanceResponseType`.

Rust domain code may use typed wrappers:

```rust
pub enum TransactionAction {
    DanceV2 { invocation: DanceInvocation },
}
```

Wire code carries references:

```rust
pub enum TransactionActionWire {
    DanceV2 { invocation: HolonReferenceWire },
}
```

Execution flow:

1. The ingress adapter receives a reference to a `DanceInvocation` holon.
2. It validates or stamps `InvocationSource`.
3. It binds the reference to a `DanceInvocation` wrapper.
4. Runtime validates the invocation holon and its related state.
5. Runtime executes the resolved dance.
6. Runtime creates or identifies a response holon described by
   `DanceResponseType`.
7. Runtime relates the response to the result body through `ResponseBody`, when
   a response body exists.
8. The command returns the response holon reference.

The Dances design does not define `DanceInvocationWire`, `DanceResponseWire`,
dance-request wire types, or dance-result wire unions.

---

## 11) Dance ABI

The dance ABI is the contract between the runtime that dispatches a dance and
the implementation that executes it. The ABI is deliberately small: it carries
the invocation identity, gives the implementation access to related holon
state, and returns either a response holon or `HolonError`.

### 11.1 ABI Goals

The ABI must provide:

- a stable host/implementation contract across supported dance engines
- clear separation between successful response and failed invocation
- deterministic invocation and response semantics
- compatibility with typed Rust wrappers and dynamic module implementations
- no requirement for dance-specific request or response wire types
- enough version and compatibility metadata to validate implementations before
  activation

### 11.2 ABI Inputs and Outputs

ABI input is a `DanceInvocation` wrapper or a `HolonReference` that resolves to
a `DanceInvocation` holon.

Through that invocation, the implementation can reach:

- the invoked `DanceType`
- the optional target holon
- the optional request holon
- the invocation source
- the target descriptor used for affordance validation, when target-based
  affordance applies
- descriptor and value semantics needed to validate request values,
  relationships, predicates, and operators
- MAP state managers needed to read or create holon state

The Dances design assumes one common host runtime surface for dance
implementations. Query/navigation dances and side-effecting dances use the same
host import surface, though query/navigation dances typically use only the
read-oriented subset in practice. The spec does not currently define a separate
read-only dance ABI or a second host capability tier.

ABI output is:

```text
Result<DanceResponse, HolonError>
```

At command or host/guest boundaries, the equivalent wire shape is:

```text
Result<HolonReference, HolonError>
```

On success, the returned reference points to a response holon whose descriptor
extends `DanceResponseType`. Any response body or diagnostics are reached
through relationships from that response holon. On failure, no successful
response holon is required; the failure is represented by `HolonError`.

### 11.3 Opaque Encoding Constraints

An implementation engine may use an opaque byte encoding at its module
boundary. That encoding is a transport detail, not the semantic model.

Opaque ABI encoding must preserve these distinctions:

- invocation failure versus successful response
- dance identity versus selected implementation identity
- target holon versus request holon
- invocation source versus authorization or provenance claims
- response holon versus response body holon
- response body references versus separately transferred holon state
- diagnostics attached to a successful response versus fatal `HolonError`

Opaque ABI payloads must not require all dances to collapse into a single
untyped request or result blob. The payload may encode references, compact
runtime handles, or serialized state snapshots, but the receiving side must be
able to recover the holonic structure promised by the Dances design.

---

## 12) Query and Navigation Dances

Query and navigation behavior is modeled as ordinary dances.

Examples:

- `Seed`
- `Expand`
- `Filter`
- `OrderBy`
- `Skip`
- `Limit`
- `Project`
- `ExecutePlan`

These dances use normal MAP holon-backed structures:

- `HolonReference` for singular holon handles
- `HolonCollection` for plural holon-backed results
- holons described by concrete extensions of `Projection` for projected records
- `HolonCollection` for projected record sets
- `TransientHolonType`s for projection shapes that are defined at runtime
- `BaseValue` as property values on request or response-body holons
- `ExecutionPlan` or session holons where replay or session semantics are
  needed

Guidance by dance category:

| Dance Category             | Preferred Request/Response Posture                                                                                                                                                                                                                                                         |
|----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Scalar or transform dance  | Request holon may be absent or may extend `Projection` with `BaseValue`-typed properties. Response body is typically a scalar-result holon or a concrete `Projection` extension whose properties hold the produced values.                                                                 |
| Holon-local action         | `DanceInvocation.Target` points to the acted-on holon. Request holon carries any structured parameters. Response body usually points to a staged, transient, or saved holon produced by the action.                                                                                        |
| Navigation operation dance | Request holon carries `HolonReference`, `HolonCollection`, or navigation-control properties as needed. Response body usually points to a `HolonCollection`.                                                                                                                                |
| Projection-boundary dance  | Request holon commonly extends `Projection` and describes selection or projection intent. Response body points to a `HolonCollection` whose members are holons described by concrete extensions of `Projection`, including transient projection types when shape is known only at runtime. |
| Plan or session dance      | Request and response bodies point to `ExecutionPlan`, session holons, or related control holons when replay or interactive execution semantics matter. Runtime result state may still be centered on `HolonCollection` or `Projection`-described holons.                                   |
| Bulk dance                 | Request holon carries collection-oriented or batch-oriented input. Response body points to `HolonCollection`, a structured batch-result holon, or another concrete result holon promised by the dance contract.                                                                            |

The query algebra does not need a separate request envelope, result envelope,
row model, or command action. A query operation is a dance invocation whose
target, request, response, and response body are normal holons.

---

## 13) Descriptor and Value Semantics Inside Dances

Dances use descriptor-owned semantics when interpreting properties, values,
relationships, and operators. Dance implementation code may perform business
logic, navigation, mutation, projection, and orchestration, but it does not
become the semantic owner of MAP value interpretation.

When a dance validates input values, applies filters, compares values, or
interprets predicates, it uses `ValueDescriptor` and descriptor-backed operator
support. A filter dance checks whether the relevant value descriptor supports
the requested operator. An edit dance validates candidate property values
through the descriptor for that property. A projection dance returns holons
described by concrete extensions of `Projection`, including incrementally
defined `TransientHolonType`s when the selected projection shape is dynamic,
rather than inventing ad hoc row shapes.

Interpretation rules:

- property legality comes from the target holon's effective `HolonDescriptor`
- relationship legality comes from the relevant relationship descriptor
- scalar value validation comes from `ValueDescriptor`
- operator availability comes from descriptor-backed operator affordances
- unsupported operators fail explicitly with `HolonError`
- dance-specific code does not silently reinterpret descriptor semantics

This keeps dance logic from becoming a semantic dumping ground. Dances execute
behavior; descriptors define what values, relationships, and operators mean.

---

## 14) Dispatch Semantics

Given a `DanceInvocation` holon, runtime dispatch:

1. Loads the `DanceInvocation` wrapper from its `HolonReference`.
2. Verifies that the holon is described by `DanceInvocation`.
3. Reads `InvokesDance`, `Target`, `Request`, and `InvocationSource`.
4. Validates the request holon against `InvokesDance.RequestType`.
5. If `Target` is present and the dance is target-afforded, resolves the
   target's `HolonDescriptor`.
6. Verifies that the target descriptor effectively affords the invoked dance
   through `Affords`.
7. Resolves candidate implementations through `ForDance`.
8. Applies activation-time validation and the deterministic implementation
   selection rules.
9. Executes the implementation through the dance ABI.
10. Places produced state in the correct MAP state manager.
11. Creates or identifies a concrete response holon whose descriptor extends
    `DanceResponseType`.
12. Relates the response to its response body through `ResponseBody`, when a
    body exists.
13. Returns the response wrapper or reference.

Successful execution returns a response holon reference. Failed execution
returns `HolonError`.

---

## 15) Validation Rules

Schema-time validation:

- Concrete dance descriptors extend `DanceType`.
- `DanceType.RequestType`, when present, points to a `HolonType` descriptor.
- `DanceType.Response` points to a `DanceResponseType` descriptor.
- `DanceResponseType.ResponseBody`, when present, points to a `HolonType`.
- `Affords` points from `HolonType` to `DanceType`.
- `ForDance` points from `DanceImplementation` to `DanceType`.
- A `DanceImplementation` honors the declared contract of its `ForDance` target
  for every holon type that effectively affords that dance.
- Implementation selection produces a deterministic result or fails.

Invocation-time validation:

- `DanceInvocation.InvokesDance` is required.
- `DanceInvocation.Target`, when present, points to a holon whose concrete
  descriptor satisfies the relationship constraint.
- `DanceInvocation.Request`, when present, conforms to the invoked dance's
  `RequestType`.
- `InvocationSource` is valid for the ingress path.
- If target-based affordance applies, the target descriptor effectively affords
  the invoked dance through `Affords`.
- Request values and predicates conform to descriptor-owned value and operator
  semantics.

Activation-time validation:

- `abi-compat`: the implementation's `AbiId`, `Version`, and `Compat` are
  compatible with the host, selected engine, and invoked dance contract.
- `module-integrity`: the executable module or built-in implementation identity
  matches the descriptor's declared module, entrypoint, and integrity policy.
- `policy-eligibility`: runtime policy permits the implementation for the
  invocation source, trust context, invoked dance, and target holon.
- `engine-readiness`: the selected `Engine` is available and can load or reuse
  the implementation.
- `shape-conformance`: request and response descriptors are available before
  the implementation is invoked.

Response-time validation:

- The returned response holon is described by a concrete type extending
  `DanceResponseType`.
- `ResponseBody`, when present, points to a holon described by a concrete
  `HolonType`.
- Response body state lives in `Nursery`, `TransientHolonManager`, or
  `HolonsCache`; it is not embedded as a full `Holon` payload in the command
  response.
- `Diagnostics` points to `DanceDiagnostic` holons.
- Response-body values and projected records conform to their concrete
  `HolonType` descriptors.

Abstract relationship target rule:

- A relationship whose target constraint is abstract `HolonType` may point to
  any holon whose concrete descriptor extends `HolonType`.
- Such a relationship does not point to an instance of abstract `HolonType`.

---

## 16) Persistence, Audit, and Observability

Dynamically generated invocation and response holons are transient. They are
created for execution and remain in transient shared-object state; they do not
become staged or saved holons.

```text
Execution:
  transient DanceInvocation and DanceResponseType-derived response holons

Cross-boundary:
  HolonReference values plus separately transferred holon state
```

The Dances Schema does not treat invocation and response holons as a durable
execution log. If durable audit, provenance, or observability records are
needed, they should be represented by separate holons or operational logs that
record the relevant execution facts without changing the transient lifecycle of
`DanceInvocation` and `DanceResponseType`-derived response holons.

Any separate durable audit or provenance record should be able to recover:

- invocation holon
- invocation source
- invoked `DanceType`
- target holon, when present
- request holon, when present
- target descriptor used for affordance validation, when present
- selected `DanceImplementation`
- implementation engine, module, entrypoint, ABI, version, and compatibility
- response holon
- response body holon, when present
- diagnostics, when present
- failure classification for failed dispatch or execution
- execution timing and resource-use summary, when the host records runtime
  metrics

Security, authorization, capability, and provenance models are specified as
first-class holonic models and related to invocations or responses explicitly.
They are not hidden as generic optional fields on `DanceInvocation`.

---

## 17) Wire-Type Boundary

Dance invocation and response cross command and host/guest boundaries as
references to holons plus separately transferred holon state.

The Dances design uses:

- `HolonReference`
- `HolonCollection`
- normal holon serialization/deserialization
- typed Rust wrappers over holonic state
- command and trust-channel adapters that carry references

The Dances design does not use:

- dance-specific invocation wire types
- dance-specific response wire types
- dance-specific request-body wire types
- dance-specific result wire unions
- direct full-`Holon` dance result payloads
- row-shaped query result contracts
- a standalone query command envelope

---

## 18) Performance Posture

The Dances design does not introduce a dance-specific caching layer. Dance
invocation, target, request, response, and response body state are carried by
`HolonReference`, so dance execution already benefits from the Shared Objects
Layer:

- `Nursery` for staged holons
- `TransientHolonManager` for transient holons
- `HolonsCache` for saved holons

Descriptor access follows the same rule. `ReadableHolon::holon_descriptor`
provides access to the `HolonType` descriptor for a holon. If that accessor
caches the descriptor reference, that is a Shared Objects Layer decision, not a
Dances design concern.

Performance optimizations should be added only in response to measured
problems. They must not change dance semantics, duplicate shared-object state,
or create a second source of truth for descriptors, affordances, invocations,
responses, or response bodies.

---

## 19) Parallel Buildout and Test Migration

The canonical dance model is holonic: invocation, response, response body,
diagnostics, and implementation bindings are represented as holons and
relationships.

The Dances design does not require backward compatibility with the old-world
dance model. The new-world model is built in parallel with the old-world model
so existing tests and callers can continue to run while the new model becomes
complete enough to replace them.

Old-world schema entries may remain present during parallel build-out, but they
are deprecated once their new-world replacements are defined. Deprecated
old-world schema entries are not part of the active dance contract and must not
be used as the basis for new-world runtime behavior. For now, that
deprecation is expressed in descriptor descriptions only, not through a new
schema-level deprecation marker.

Mappings from old-world concepts to new-world concepts are useful as migration
guidance for tests, examples, and implementation planning. They are not runtime
translation requirements.

Migration guidance:

- old-world request envelopes are replaced by `DanceInvocation` holons
- old-world response envelopes are replaced by `DanceResponseType`-derived
  response holons
- old-world query/navigation entry points are replaced by ordinary
  query/navigation dances
- row-shaped query results are replaced by `HolonCollection`,
  projection-result holons, or other response-body holons described by
  `HolonType`
- boundary serialization transfers holon state separately from the response
  reference when the receiving side needs state hydration
- typed Rust structs remain wrappers over `HolonReference`, so behavior can
  evolve without creating new wire types

Tests should move to the new-world model when the new model can fully express
the behavior being tested. Until then, old-world tests remain old-world tests.
The Dances design should not introduce adapter code whose only purpose is to
translate old-world dance requests into new-world invocations.

Migration work must preserve the semantic distinction between:

- the dance requested by the caller
- the descriptor that affords the dance
- the implementation selected by the runtime
- the response holon returned by successful execution
- the response body holon that carries result state
- `HolonError` returned by failed execution

---

## 20) Deferred Design Decisions

- `DanceEvent` is deferred until the asynchronous event-handling architecture
  is designed and a concrete event consumer requires it.

---

## Appendix A) Legacy Surface Disposition

This appendix records how retained old-world dance surfaces relate to the
current new-world dance design.

The active canonical contract uses unsuffixed names. When a deprecated schema
descriptor would otherwise collide with an active canonical descriptor, the
deprecated schema descriptor should be renamed with a `Deprecated` suffix. This
preserves global uniqueness for fully qualified descriptor and relationship
names while keeping the active contract readable.

Interpretation rules:

- unsuffixed names belong to the active canonical contract
- deprecated schema descriptors use a `Deprecated` suffix when needed to avoid
  collision with active canonical names
- deprecated runtime bridges may remain temporarily in code during migration,
  but they are not part of the target design
- deprecated surfaces exist only for parallel build-out and test preservation;
  they must not become the basis for new-world runtime behavior

| Surface                                                                                                    | Classification                                            | Canonical posture                                                                                                                | Deprecated or legacy posture                                                                       |
|------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| `DanceInvocation`                                                                                          | Active canonical holon type                               | Keep unsuffixed                                                                                                                  | None                                                                                               |
| `DanceResponseType`                                                                                        | Active canonical response descriptor root                 | Keep unsuffixed                                                                                                                  | None                                                                                               |
| `DanceImplementation`                                                                                      | Active canonical implementation binding holon type        | Keep unsuffixed                                                                                                                  | None                                                                                               |
| `Projection`                                                                                               | Active canonical base holon type for value-shaped records | Keep unsuffixed                                                                                                                  | None                                                                                               |
| `DanceRequest`                                                                                             | Deprecated runtime bridge                                 | Do not use as target design                                                                                                      | May remain temporarily in runtime and adapter compatibility layers                                 |
| `DanceResponse`                                                                                            | Deprecated runtime bridge                                 | Do not use as target design                                                                                                      | May remain temporarily in runtime and adapter compatibility layers                                 |
| `RequestBody`                                                                                              | Deprecated runtime bridge                                 | Do not use as target design                                                                                                      | May remain temporarily for old-world payload compatibility                                         |
| `ResponseBody`                                                                                             | Deprecated runtime bridge                                 | Do not use as target design                                                                                                      | May remain temporarily for old-world payload compatibility                                         |
| `ResponseStatusCodeDeprecated`                                                                             | Deprecated schema enum and related property type          | Active contract uses outer `Result<DanceResponse, HolonError>` instead                                                           | Retained only if old-world schema compatibility still needs it                                     |
| `ResponseBodyTypeDeprecated`                                                                               | Deprecated schema abstract holon type                     | Active response bodies point directly to concrete `HolonType`s                                                                   | Retained only if old-world schema compatibility still needs it                                     |
| `ImplementsDanceDeprecated`                                                                                | Deprecated schema relationship                            | Active implementation binding uses `ForDance`                                                                                    | Retained only if old-world schema compatibility still needs it                                     |
| `ImplementedForDeprecated`                                                                                 | Deprecated schema inverse relationship                    | Active implementation binding does not use per-target implementation applicability                                               | Retained only if old-world schema compatibility still needs it                                     |
| `ResponseBodyDeprecated`                                                                                   | Deprecated schema relationship                            | Active `ResponseBody` points from `DanceResponseType` to `HolonType`                                                             | Retained only if old-world schema compatibility still needs it                                     |
| `ResponseBodyForDeprecated`                                                                                | Deprecated schema inverse relationship                    | Active `ResponseBodyFor` inverts the canonical `ResponseBody` relationship                                                       | Retained only if old-world schema compatibility still needs it                                     |
| `CommitResponseDeprecated`                                                                                 | Deprecated old-world commit response body holon type      | Commit-related new-world response bodies should be ordinary concrete holon types                                                 | Retained only if old-world schema compatibility still needs it                                     |
| `Node`, `NodeCollection`, `QueryPathMap`, `QueryExpression`                                                | Deprecated Issue 508 compatibility surfaces               | Do not use in new navigation/query dances                                                                                        | May remain temporarily only for old-world relationship traversal flows                             |
| `NodeWire`, `NodeCollectionWire`, `QueryPathMapWire`                                                       | Deprecated compatibility wire surfaces                    | Do not use in new-world dance/query contracts                                                                                    | May remain temporarily only for existing client, guest, boundary, SDK, and sweettest compatibility |
| `query_relationships`, `fetch_all_related_holons`                                                          | Deprecated old-world query/navigation entry points        | New relationship navigation should be ordinary descriptor-backed dances over `HolonCollection` and `Projection`-described holons | May remain temporarily only for old-world flows                                                    |
| `Value`, `Row`, `RowSet`, `BoundHolonCollection`, broad query `RuntimeValue`, standalone `Query` contracts | Removed query contract artifacts                          | Do not use in the new-world dance/query design                                                                                   | None                                                                                               |
