# MAP Dev Docs Context (v1.0)

This context defines the shared language for MAP design documentation, especially query, command, dance, descriptor, and runtime contract work.

## Change Log

### v1.0

- establishes the versioned context baseline
- records Issue 17's canonical Dance vocabulary: name-addressed invocation,
  `RequestType`, affordance requirements, structural request/response
  validation, the `LoadHolons` / `QueryDance` `HolonSpace` posture, and the
  separate TrustChannel/Agreement authorization boundary

## Language

**LoaderRefRep**:
The transient, schema-backed loader holon graph rooted at `HolonLoadSet`, including
`HolonLoaderBundle`, `LoaderHolon`, `LoaderRelationshipReference`, and
`LoaderHolonReference` holons. Host and guest use this same holonic representation; it is
serialized through the normal holon transport mechanism as the loader dance request. JSON and TDL
creation paths both compile into `LoaderRefRep` when authored references are expressed by key
rather than by resolved holon ID.
_Avoid_: Treating obsolete `loader_ir` DTOs as an architectural layer, defining separate host and
guest loader representations, or treating `LoaderRefRep` as the application holon graph validated
for commit

**Holon Loading**:
The existing end-to-end Holon Data Loader process. A concrete-syntax parser produces
`LoaderRefRep`; the Holon Loader client submits it through the loader dance; guest loader
components construct and resolve staged application holons, invoke descriptor-default
materialization, and call commit.
_Avoid_: Introducing a parallel generic creation-orchestration framework for TDL

**Validated Commit**:
The runtime invariant that commit invokes the reusable Holon Validator over the
default-materialized staged holon graph and persists nothing when blocking violations remain.
_Avoid_: Requiring each parser or loader caller to invoke final validation correctly before calling an
otherwise unguarded commit operation, or making commit mutate staged holons by materializing
descriptor defaults

**Holon Validator**:
The reusable service that performs descriptor-driven validation of holons. It validates ordinary
holons and descriptor holons against their effective descriptor contracts, delegates semantic
computation to the descriptor kernel, and accumulates violations. It is callable by commit and by
consumers outside Holon Loading.
_Avoid_: “Descriptor Validator,” which incorrectly suggests that only descriptor holons are
validated

**Descriptor-Aware Holon Validation**:
The validation layer above descriptor-independent PVL that validates ordinary and descriptor holons
against resolved descriptor semantics through the Holon Validator.
_Avoid_: Coordinator-zome validation as the canonical term, or TDL validation for descriptor-semantic
checks

**ValidationRule**:
A holon that names one semantic validation condition; its abstract root type is
ValidationRule.HolonType, and concrete rule holons are described by narrower ValidationRule Family
types.
_Avoid_: Treating Core Schema invariants, the executable implementation, or TDL-only checks as
application- or extension-authorable ValidationRules

**ValidationRule Family**:
A specialization branch under ValidationRule for rules whose metadata and parameters share a
validator level or descriptor family, such as HolonValidationRule or StringValidationRule.
_Avoid_: Forcing all validation rules into one generic property shape

**MetaValidationRule**:
The validation-specific meta-type that describes ValidationRule family descriptors and permits them
to afford the local Validate operator.
_Avoid_: Adding local operator affordances broadly to every MetaHolonType-described descriptor

**Validate Operator**:
The local operator afforded by ValidationRule family descriptors to evaluate a validation rule.
_Avoid_: Modeling initial validation execution as a client Command or host-to-host Dance

**ValidationRule Wrapper**:
A Rust typed wrapper around a HolonReference to a ValidationRule holon that exposes schema-backed
rule metadata and dispatch inputs to the validation runtime.
_Avoid_: Treating the wrapper as the normative semantic rule or as the descriptor-kernel algorithm

**Validations**:
The common local relationship name used by qualified validation-attachment relationship descriptors
from type descriptors to compatible ValidationRule Family targets.
_Avoid_: InstanceValidations or typekind-specific local relationship names as canonical attachment
language

**Validation Schema**:
The schema package that defines validation-owned holon types, relationships, result/evidence
surfaces, and executable validation binding metadata.
_Avoid_: Putting every validation concept directly into MAP Core

**ValidationRule Wrapper Factory**:
The initial static runtime mechanism that selects a family-specific ValidationRule Wrapper for a
ValidationRule holon.
_Avoid_: A separate concrete-rule-to-implementation registry before wrapper-based Validate
execution is insufficient

**UnsupportedValidationRule**:
The validation outcome reported when a mandatory ValidationRule applies in the current validation
profile but no compatible built-in wrapper Validate implementation is available.
_Avoid_: Silently passing, ignoring, or downgrading mandatory commit-path validation commitments

**Descriptor-Default Materialization Service**:
The initially Holon-Loader-specific service that detects omitted properties, obtains effective
property declarations through `HolonDescriptor`, reads declared defaults through
`PropertyDescriptor::default_value()`, and writes applicable values through staged-holon mutation
APIs. Its public contract is graph-level, such as `materialize_defaults(staged_graph)`;
property-level lookup and writes remain internal implementation details. Its boundaries remain
modular so later creation paths may reuse it without restructuring descriptor semantics.
_Avoid_: Kernel `get_default_value` or `set_default` operations, or exposing kernel-specific result types to
ordinary creation-path callers, or requiring interactive creation flows to silently accept defaults

**Old-World Query Types**:
Deprecated compatibility query/navigation types retained without renaming while replacement query contracts are introduced.
_Avoid_: Legacy-prefixed renames, new PRO3 foundations

**New-World Query Contract**:
The resolved MAP navigation posture: concrete navigation behavior is implemented as Dances, while the ExecutionPlan, InteractiveNavigationSession, and later DeclarativeQuery HolonTypes provide replay/session/declarative layers.
_Avoid_: Reified Query object or standalone query envelope as the default runtime center

**NavigationQueryRequest**:
Retired candidate name for a standalone new-world query request envelope.
_Avoid_: Introducing this as a PRO3 runtime requirement

**NavigationQuerySpec**:
Retired candidate name for a standalone new-world query request discriminator.
_Avoid_: Introducing this as a PRO3 runtime requirement

**NavigationQueryResult**:
Retired or rename-pending candidate name for a navigation operation result holon.
_Avoid_: Freezing query-specific naming before the result holon name is settled

**NavigationQueryResultReference**:
Retired or rename-pending candidate name for a typed reference to a navigation operation result holon.
_Avoid_: Freezing query-specific naming before the result reference name is settled

**Host-Owned Holon State**:
The runtime rule that authoritative HolonState lives in the host; clients hold references and use commands to inspect or mutate state.
_Avoid_: Client-owned HolonState cache as source of truth

**Commands**:
The stable client-to-host ingress, binding, dispatch, and lifecycle-control surface for MAP operations.
_Avoid_: Semantic owner of query, dance, descriptor, or distributed behavior

**MapRequest**:
Deprecated generic request type from an older ingress model.
_Avoid_: Canonical wrapper for Commands, Dances, Queries, or IPC

**MapIpcRequest**:
The Commands-specific IPC wrapper at the TypeScript-to-host ingress boundary.
_Avoid_: Generic cross-surface request envelope

**Dances**:
Descriptor-afforded behavior/workflow invocations that execute domain or coordination behavior through the dance substrate.
_Avoid_: Treating dance invocation as the command transport contract or query algebra

**Dance Invocation**:
 A transient holon record that identifies the requested dance by required canonical `DanceName`, may name an affording holon and request value holon, and carries trusted ingress metadata. The host resolves `DanceName` to exactly one local schema-backed `DanceType` before validating and dispatching; no match or more than one match is a dispatch error.
_Avoid_: `InvokesDance` / `InvokedBy`, a supplied descriptor-holon reference as invocation identity, or a client-owned dispatch authority

**DanceName**:
The canonical identity of a DanceType: its inherited `TypeDescriptor.TypeName`, exposed by a Dance-specific Rust accessor. `DanceInvocation.DanceName` carries that value for name-addressed dispatch. `LoadHolons`, for example, is both the descriptor type name and its canonical DanceName.
_Avoid_: A separate DanceType naming property or a transport-specific alias as the semantic dance identity

**QueryDance**:
The Query–Dance adapter's canonical DanceName, derived from `QueryDance.DanceType`'s `TypeName`. A transport or API alias such as `map.query.execute` is not its Dance identity.
_Avoid_: Treating a transport alias as the schema-resolved DanceName

**Dance Affordance**:
The generic schema relationship pair `HolonType -[AffordsDance]-> DanceType` and `DanceType -[DanceAffordedBy]-> HolonType`. `HolonDescriptor::afforded_dances()` is its runtime discovery surface. QueryDance owns a distinct, adapter-specific relationship pair with the same local names.
_Avoid_: Shortened `Affords` / `AffordedBy` schema names or collapsing qualified relationship identities by local name

**Affording Holon Requirement**:
A DanceType-level policy governing whether a DanceInvocation must carry an `AffordingHolon`. `Required` demands a present subject whose effective descriptor affords the resolved Dance; `Optional` permits absence but validates an offered subject the same way; `Prohibited` demands absence. The current `LoadHolons` and `QueryDance` Dances require a HolonSpace subject.
_Avoid_: Conflating the affording holon with request payload or Dance ownership

**Dance Implementation Selection**:
The initial executor requires exactly one eligible `DanceImplementation` related through `ForDance`. Deterministic selection among multiple semantically interchangeable implementations is a later activation-phase capability.
_Avoid_: Treating multiple implementation candidates as valid before activation and selection policy exists

**Dance Request Contract**:
The optional `DanceType.RequestType` descriptor, with inverse `RequestTypeFor`, against which a supplied request holon is structurally validated by the shared descriptor-aware validation capability at Dance ingress. A matching request descriptor reference is optional and does not determine acceptance. When absent, an invocation must omit `Request`; it does not accept an unconstrained request value.
_Avoid_: Exact request-descriptor identity as the conformance test, minting a request descriptor per invocation, a Dance-local structural validator, or treating no contract as permissive input

**Dance Response Contract**:
Before returning a successful result, the Dance executor structurally validates the implementation's response holon against the resolved `DanceType.Response` contract. This establishes valid data at the inner execution boundary; a TrustChannel subsequently applies the Agreement's role, permission, and information-access constraints before anything crosses the outbound trust boundary.
_Avoid_: Treating descriptor validation as authorization, or applying disclosure rules to an unchecked implementation result

**Dance and Trust Boundary**:
The Dance cutover establishes the structural input and output contract only. TrustChannel and Agreement disclosure authorization are the outer boundary that consumes a structurally valid Dance response and remain separate work.
_Avoid_: Expanding Dance dispatch work into TrustChannel policy enforcement

**Holon Load Dance**:
`LoadHolons` is a Dance afforded by `HolonSpace`; its work is scoped to the selected HolonSpace rather than being a global or standalone invocation.
_Avoid_: Treating `LoadHolons` as unafforded solely because its request is a `HolonLoadSet`

**Dance Contract Cutover**:
The Dance v2.1 contract is a clean-slate implementation target: no deployed compatibility requirement preserves superseded Dance schema members, direct descriptor-reference invocation, `DanceRequest` / `DanceResponse` bridge payloads, legacy adapters, or their compatibility tests.
_Avoid_: Retaining deprecated Dance artifacts merely to minimize local implementation ripple

**Envelope Ownership**:
The rule that Commands, Dances, and Queries keep their own request/result envelopes even when one surface invokes or carries another.
_Avoid_: Flattened or mixed envelopes such as treating MapIpcRequest as a dance/query envelope

**Queries**:
The host-owned read/navigation substrate for MAP query semantics, including ExecutionPlan holon structure, NavigationExecutionBindings, algebra operations, validation, and result shaping.
_Avoid_: Implementing query semantics inside Commands or exposing query-internal state as a Dance ABI

**Navigation Operation Dance**:
A dance afforded by HolonCollection or another navigation-relevant type that performs one concrete navigation operation such as Expand, Filter, OrderBy, Skip, Limit, or Seed.
_Avoid_: Reified Query object as the required execution target for each operation

**Interactive Route**:
The PRO3 query path where each navigation operation executes immediately and is appended to an accumulating ExecutionPlan holon.
_Avoid_: Submit-only saved query execution

**Interactive Navigation Session**:
A reified, host-owned session holon that is the aggregate root for the Interactive Route.
_Avoid_: Client-resubmitted full plan as the primary interaction model, ExecutionPlan holon alone as immediate-execution owner

**Navigation Operation Intent**:
The operation description supplied to InteractiveNavigationSession.ApplyOperation.
_Avoid_: Treating the operation intent as a standalone query envelope

**Apply Operation Dance**:
The dance afforded by InteractiveNavigationSession that appends a navigation operation to the session's ExecutionPlan holon and may execute it immediately.
_Avoid_: Each operation dance independently mutating plans as an incidental side effect

**ExecutionPlan Execute Dance**:
The dance afforded by the ExecutionPlan HolonType that replays or executes a previously defined plan holon.
_Avoid_: Treating every interactive navigation gesture as saved-plan execution

**DeclarativeQuery**:
A future holon that holds declarative query text, such as OpenCypher or GQL, for parsing and optimization into an ExecutionPlan holon.
_Avoid_: Making declarative query text part of the PRO3 interactive runtime substrate

**HolonCollection**:
The primary runtime carrier for holon-oriented query execution.
_Avoid_: RowSet as execution carrier, introducing a new plural carrier without a distinct lifecycle

**Query**:
The MAP HolonType for a reusable symbolic query definition rooted at a
QueryExpression. Query is independently invocable by peer Rust objects; the
Query–Dance adapter is an optional Dance-layer ingress surface.
_Avoid_: Treating a Dance request or runtime execution record as the query definition

**ExecutionInstance**:
Runtime state for one execution of a Query, including expression executions and
the final result. It is not a query definition and does not execute a
Dance-owned request object.
_Avoid_: ExecutionPlan or QueryDanceRequest as the runtime semantic owner

**NavigationExecutionBindings**:
The narrow binding set that maps ExecutionPlan holon variables to values during navigation plan capture, replay, or interactive execution.
_Avoid_: generic runtime context terminology, embedding variable names in HolonCollection

**Projection Result**:
A materialized result view such as BaseValue, Row, or RowSet produced at an explicit projection or boundary.
_Avoid_: Internal execution state

**DAHN Critical Path**:
The minimum descriptor-driven implementation path needed to deliver the initial Dynamic Adaptive Holon Navigator.
_Avoid_: Blocking DAHN on saved-plan, interactive-session, or declarative-query work when navigation operation Dances and shared runtime types are sufficient

## Relationships

- **LoaderRefRep** is a construction and unresolved-reference representation made from ordinary
  transient holons; it is not a separate semantic IR or a parallel set of transport DTOs.
- TDL and MAP JSON source conversion uses **LoaderRefRep** directly: `TDL -> LoaderRefRep -> JSON`
  and `JSON -> LoaderRefRep -> TDL`. Translation alone does not invoke guest-side default
  materialization, descriptor validation, or persistence.
- The Holon Loader resolves **LoaderRefRep** into the staged application holon graph on which
  descriptor-default materialization and validation operate.
- Each supported concrete syntax has a parser that produces **LoaderRefRep**. Existing Holon Loader
  client and guest components continue to own **Holon Loading** orchestration.
- TDL references already contain loader keys. The TDL parser copies those keys into
  `LoaderHolonReference`s; existing guest `LoaderReferenceResolution` resolves them against the
  current load and previously saved holons. There is no host-side symbol-resolution phase.
- Concrete-syntax parsers report syntax and source-to-`LoaderRefRep` lowering failures only.
  Existing guest loader components own duplicate loader keys and keyed-reference failures; the
  Holon Validator owns descriptor-driven violations. Loader provenance maps guest diagnostics back
  to source locations.
- **Validated Commit** makes descriptor-driven holon validation an invariant of persistence by
  invoking the reusable **Holon Validator**. The validator remains independently callable outside
  commit and the loader flow.
- The **Holon Validator** is the reusable validation entry point. It owns validation scope,
  context, rule coordination, and result accumulation while delegating Schema 2.0 semantic
  predicates and conformance algorithms to the pure descriptor kernel.
- **Descriptor-Aware Holon Validation** is the semantic validation boundary above
  descriptor-independent PVL. TDL tooling may feed this layer through Holon Loading, but does not
  own its descriptor-semantic checks.
- **ValidationRule** holons express descriptor-authored validation commitments. Concrete
  **ValidationRule Family** subtypes provide rule shapes for holon, property, relationship,
  transaction, and value-family-specific validation.
- Validations that follow directly from Core Schema-defined descriptor semantics are represented as
  MAP-seeded, non-authorable **ValidationRule** holons. They are loaded as a non-revokable base set
  and attached through additive **Validations** relationships; application and extension descriptor
  authors cannot remove, replace, opt into, or opt out of them.
- **MetaValidationRule** describes **ValidationRule Family** descriptors. Those descriptors afford
  the **Validate Operator** through `AffordsOperator`; the first wrapper-based implementation is
  the built-in execution route for that local operator.
- Type descriptors attach validation commitments through fully qualified **Validations**
  relationship descriptors. The local relationship name may be the same across type kinds because
  relationship descriptor identity is qualified by source type, relationship name, and target type.
  The kernel assigns **Validations** relationships `Additive` so validation commitments
  accumulate down `Extends`.
- **ValidationRule Wrapper** types expose `ValidationRule` holon metadata to Rust validation code.
  They implement built-in `Validate` execution for supported concrete rule keys and delegate
  normative `DS-*` semantics to the descriptor kernel where applicable.
- The **Validation Schema** owns validation-specific holon types such as **ValidationRule**,
  `ValidationImplementation`, `ValidationRuleSet`, and `ValidationResult`, and owns the
  **Validations** attachment relationships unless a concrete bootstrap constraint requires
  a narrower Core hook.
- The first Descriptor-Aware Holon Validation implementation uses the **ValidationRule Wrapper
  Factory** to construct a family-specific wrapper. The wrapper's `Validate` implementation
  dispatches by concrete **ValidationRule** holon identity while preserving the future path to
  `ValidationImplementation` holons and validation Dances.
- Built-in **ValidationRule** identity is a stable authored semantic key, such as
  `StringLength.ValidationRule`, not a generated storage identity.
- A mandatory **ValidationRule** that applies in a commit-oriented validation profile but has no
  compatible wrapper-based `Validate` implementation produces **UnsupportedValidationRule** and
  blocks commit.
  Advisory or runtime-only rules may instead defer, warn, or be not applicable according to rule
  metadata and profile selection.
- A **ValidationRule** declares default severity and blocking behavior. A **Validations**
  binding or validation profile may narrow that behavior, including making a rule stricter, but
  must not weaken a rule below the rule's own minimum or the active profile's requirement.
- Validation parameters are layered: **ValidationRule** defines parameter schema and defaults,
  **Validations** supplies descriptor-specific or profile-specific overrides, and the
  target descriptor supplies domain parameters already intrinsic to its own semantics.
- `ValidationRuleSet` belongs to the **Validation Schema** model but is deferred as an execution
  feature until individual **ValidationRule** identity, wrapper-based dispatch, **Validations**,
  unsupported-rule handling, and result reporting are stable.
- **Validated Commit** accumulates independently discoverable descriptor violations across the
  transaction and persists nothing if any blocking violation exists. Fatal graph-access or
  infrastructure failures may stop validation when further results would be unreliable.
- Descriptor-default materialization occurs before **Validated Commit** and remains the
  responsibility of creation/load orchestration; commit validates but does not materialize
  defaults or otherwise mutate staged holons.
- Creation/load orchestration materializes descriptor defaults only after the complete staged
  application graph has been constructed, all keyed references have been resolved, and each
  holon's `DescribedBy` relationship is bound.
- `HolonDescriptor::instance_properties()` supplies effective property declarations, and
  `PropertyDescriptor::default_value()` supplies each declaration's schema-backed default. Default
  lookup requires no separate kernel helper.
- The **Descriptor-Default Materialization Service** encapsulates effective-property lookup and the
  concrete staged-holon write while preserving descriptor-wrapper encapsulation.
- Creation/load orchestration invokes the **Descriptor-Default Materialization Service** once for
  the fully constructed and resolved staged graph; it does not enumerate omitted properties.
- Initial automatic default materialization belongs to **Holon Loading**. Interactive creation may
  display a descriptor default for human confirmation before writing it rather than silently
  materializing it.
- Any descriptor-default materialization error prevents creation/load orchestration from invoking
  **Validated Commit**. Whether successful default writes remain visible in the uncommitted staged
  graph is a separate error-recovery policy.
- Default materialization accumulates errors across the staged graph where practical. Successful
  default writes are not individually reverted after an error; they remain available for
  diagnostics until creation/load orchestration abandons or rolls back the failed transaction.
- The **Descriptor-Default Materialization Service** reports only failures to determine or apply a
  declared default. It leaves required properties without defaults absent; the **Holon Validator**
  owns the resulting required-property violation.
- A materialized default becomes ordinary explicit property state. Loader-side provenance may
  identify it temporarily for diagnostics, but commit persists no authored-versus-default marker,
  and later descriptor-default changes do not alter saved holons.
- **Old-World Query Types** remain intact for compatibility and are not renamed to `Legacy*`.
- **New-World Query Contract** does not require **NavigationQueryRequest**, **NavigationQuerySpec**, or a reified `Query` object for PRO3.
- Navigation operation result holons remain valid, but the query-specific `NavigationQueryResult` naming is rename-pending.
- **MapRequest** is deprecated and should not be used as the canonical ingress or cross-surface wrapper.
- **MapIpcRequest** belongs to **Commands** and wraps command ingress only.
- **Commands** are ingress adapters: they bind client/wire requests to host runtime context, enforce command lifecycle rules, and route query or dance requests to the owning substrate.
- **Queries** own query/navigation semantics: ExecutionPlan holon structure, NavigationExecutionBindings, algebra operation behavior, descriptor-backed validation, and query result shaping.
- **Dances** own behavior/workflow semantics for dance invocations and may call into query/navigation services when behavior needs query results.
- A command that invokes a query does not make **Commands** the query engine; a dance that invokes a query does not make **Dances** the query algebra.
- **Envelope Ownership** allows nesting without mixing: **Commands** may carry **Dances**, and **Dances** may carry or invoke **Queries**, but each layer retains its own envelope and semantic owner.
- **Navigation Operation Dances** are the first implementation unit for concrete navigation behavior.
- Collection-transforming **Navigation Operation Dances** such as Expand, Filter, OrderBy, Skip, and Limit are afforded by **HolonCollection**.
- **Seed** operations may be afforded by a space, execution domain, session, or other host-defined navigation scope rather than by an existing **HolonCollection**.
- **Interactive Route** is the initial path implemented by the **New-World Query Contract**.
- In the **Interactive Route**, each navigation operation executes immediately and appends a deterministic operation to an **ExecutionPlan holon**.
- **ExecutionPlan** is a **HolonType**; an accumulated or saved plan is an **ExecutionPlan holon**.
- An **Interactive Navigation Session** is a reified host-owned holon and the aggregate root for interactive navigation.
- An **Interactive Navigation Session** owns the authoritative live **NavigationExecutionBindings** and relates to the accumulating **ExecutionPlan holon**.
- **Apply Operation Dance** appends the requested operation to the session's **ExecutionPlan holon** and, when requested, executes it immediately against the session's **NavigationExecutionBindings**.
- A **Navigation Operation Intent** carries only the next operation description; the host resolves inputs from the session's **NavigationExecutionBindings**.
- **ExecutionPlan Execute Dance** comes after interactive session support and executes previously defined plans.
- **DeclarativeQuery** support comes after **ExecutionPlan Execute Dance** and compiles declarative OpenCypher/GQL text into an imperative **ExecutionPlan holon**.
- A navigation operation result holon records at least the output binding and links to result state, the updated **ExecutionPlan holon** where applicable, and diagnostics.
- A navigation operation result holon may include a session id when the result belongs to an **Interactive Navigation Session**.
- **NavigationExecutionBindings** maps **ExecutionPlan holon** variables to **HolonCollection** or **Projection Result** values.
- **Projection Result** values are produced at projection or boundary points, not as the default execution carrier.
- The **DAHN Critical Path** depends on stable Commands, Dance invocation, descriptor affordances, `HolonReference`, `HolonCollection`, and projection-boundary types; it does not depend on Query PRs for `ExecutionPlan`, `InteractiveNavigationSession`, or declarative query support.

## Example Dialogue

> **Dev:** "Should we add a new `QueryRequest` envelope for PRO3 navigation?"
> **Domain expert:** "No. Navigation behavior is invoked through Dances. Add ExecutionPlan holons, InteractiveNavigationSession holons, and DeclarativeQuery holons only where those concrete runtime objects are needed."

## Flagged Ambiguities

- "query request" can mean the old-world compatibility `QueryRequest`, a retired **NavigationQueryRequest** candidate, a Dance invocation, or a future declarative-query request. Resolved: PRO3 navigation operation execution uses Dance invocation, not a new standalone query envelope.
- "query result" can mean old-world `QueryResult`, a materialized projection result, or a navigation operation result holon. Resolved: avoid freezing the **NavigationQueryResult** name; use navigation operation result holon until a concrete type name is chosen.
- "execute a query" can mean submitting a complete saved plan or taking one interactive navigation step. Resolved: PRO3 starts with the **Interactive Route**.
- "interactive execution state" could be owned by the client or the host. Resolved: the host owns the **Interactive Navigation Session** while results expose enough plan/session information for client visibility and recovery.
- "navigation query result" can mean a materialized payload or host-owned result state. Resolved: PRO3 may use host-owned navigation operation result holons, but query-specific result naming remains rename-pending.
- "map request" can mean deprecated **MapRequest** or command-owned **MapIpcRequest**. Resolved: use **MapIpcRequest** only for the Commands IPC boundary and do not generalize it to Dances or Queries.
- "wrapping" can mean command ingress carrying a dance, or dance behavior carrying/invoking a query. Resolved: nested invocation does not transfer envelope ownership or semantics to the outer layer.
- "query" can mean a reified runtime object, a capability area, an executable plan holon, a declarative query document, or a family of navigation dances. Resolved: PRO3 does not require a reified `Query` object; concrete runtime objects are navigation operation dances, InteractiveNavigationSession holons, ExecutionPlan holons, and result holons. A future **DeclarativeQuery** holon may represent OpenCypher/GQL text.
- "operation execution" can mean invoking a navigation dance directly with an `ExecutionPlan` holon reference parameter, or invoking an `ExecutionPlan`/session dance such as `AddOperation` that appends and optionally executes immediately. Resolved: PRO3 reifies **Interactive Navigation Session** as the interactive route aggregate root.
- "result relationship" can mean a direct relationship from a navigation operation result holon to output holons, a relationship to a collection/result-set holon, or a relationship to a projection result holon. Unresolved: choose the initial shape for `HolonCollection` outputs.
- "coordinator-zome validation" can mean the implementation location for pre-commit checks or the
  semantic validation boundary above PVL. Resolved: use **Descriptor-Aware Holon Validation** for
  the semantic boundary and reserve implementation-location wording for delivery plans.
- "TDL validation" can mean syntax/lowering/fidelity checks or descriptor-semantic conformance.
  Resolved: TDL owns syntax, lowering, and source fidelity; **Descriptor-Aware Holon Validation**
  owns descriptor-semantic conformance.
- "local validation" can mean an adaptive-system local extension attachment or the general
  descriptor-authored validation mechanism. Resolved: use **Validations** as the canonical local
  relationship name for qualified relationships from type descriptors to compatible
  **ValidationRule Family** targets; avoid `HasLocalValidation`.
- "validation in Core" can mean the minimal type-descriptor attachment hook or the whole validation
  object model. Resolved: keep the validation object model and **Validations** attachment
  relationships in the **Validation Schema** unless bootstrapping proves a narrower Core hook is
  required.
