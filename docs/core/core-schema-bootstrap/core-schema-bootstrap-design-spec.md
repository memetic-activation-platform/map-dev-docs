# Core Schema Bootstrap Design Specification

## Purpose

This specification defines how MAP provisions the Core Schema exactly once in
the first cell of the first Space, and how that Space becomes the
`CoreSchemaSpace` that stewards the resulting descriptor holons.

The Core Schema is a normal, self-describing holon graph. Bootstrap is the
exceptional lifecycle by which that graph and its stewarding `HolonSpace` first
become available; it does not introduce exceptional descriptor, relationship,
Reference Layer, or Commit semantics.

## Scope

This specification owns:

- `CoreSchemaSpace` identity and role;
- first-space bootstrap authority and readiness;
- the host-owned provisioning lifecycle;
- recovery and retry requirements for incomplete provisioning; and
- the contract by which later Spaces obtain Core Schema references.

It does not define the Core Schema's declarations, generic loader behavior,
transaction or Commit semantics, descriptor semantics, or storage-layer
implementation.

## CoreSchemaSpace

`CoreSchemaSpace` is the Space that stewards the initial Core Schema graph.
For the first cell that provisions MAP, it is also that cell's local
`HolonSpace`. The identity is semantic, not merely an implementation alias for
the `LocalHolonSpace` infrastructure anchor.

The bootstrap load set must create the `CoreSchemaSpace` holon with metadata
that identifies this role, and must include the Core Schema holons it stewards.
The relationship graph must include the authored `OwnedBy` facts from the
schema holons to that staged `CoreSchemaSpace`.

## Provisioning Lifecycle

### Host ownership

Bootstrap is a host provisioning responsibility. The Holochain guest cannot
read the local JSON import files and must not acquire OS or local-filesystem
access for this purpose. The host performs file access and parsing, then sends
the existing loader-reference representation to the guest through the ordinary
loader ingress.

Conductora owns startup sequencing. Its `AppBuilder` must invoke a dedicated
`ensure_core_schema_space(&AppHandle)` service after
`runtime::init_from_state` has created and published the `RuntimeSession`, and
before `SetupManager::create_window` or the `startup:ready` event. The service
belongs in `host/conductora/src/setup/core_schema_bootstrap.rs`.

The service must:

1. read the initialized `RuntimeState` and use its `RuntimeSession` to open a
   dedicated bootstrap transaction;
2. check the durable Core Schema bootstrap readiness predicate;
3. when bootstrap is not ready, read the dedicated bootstrap JSON inputs,
   construct the existing `ContentSet`, and execute the existing
   `TransactionAction::LoadHolons` path;
4. verify readiness after Commit; and
5. close or archive the bootstrap transaction before returning.

Any error must fail startup. Conductora must not create the UI window or emit
`startup:ready` until the service returns successfully.

`HolochainSetup::handle_new_app_installation` is not the bootstrap owner. It
executes before the receptor and commands runtime required by the established
loader route exist, and a hApp installation result does not prove bootstrap is
complete. Bootstrap is likewise not a Tauri command or a UI IPC round trip.

### First-space bootstrap

For this bootstrap lifecycle, first-space provisioning is a single-origin
event. The Conductora installation that creates or opens the initial cell is
the only permitted bootstrap actor, and it must serialize concurrent local
calls to `ensure_core_schema_space`. No additional cell or host may begin
normal MAP use until a ready `CoreSchemaSpace` exists.

This is a deployment and startup-orchestration invariant, not a distributed
claim encoded in the DHT. After a successful bootstrap, the fixed
`LocalHolonSpace` infrastructure anchor is the durable discovery fact for the
ready `CoreSchemaSpace`; it is not an exclusive lock or leader-election
mechanism. A process that observes an absent anchor may make a fresh bootstrap
attempt only under the single-origin provisioning contract. It must fail closed
rather than select an arbitrary candidate or replay the full load set if it
detects incomplete or competing bootstrap state.

Supporting simultaneous cold starts by independent Conductora hosts is outside
this specification. It requires a separately designed DHT-level claim,
election, and conflict-recovery protocol.

When no ready `CoreSchemaSpace` exists, the host must:

1. construct the dedicated Core Schema bootstrap load set;
2. submit it through the ordinary loader and transaction path;
3. allow staged key references to resolve the `CoreSchemaSpace` and Core
   Schema graph together; and
4. regard bootstrap as complete only after the transaction commits and the
   readiness predicate succeeds.

The load set stages all holons before relationships are committed. Existing
two-pass Commit behavior therefore persists the staged holons before it
materializes declared relationships and their inverses. Bootstrap must not add
special `OwnedBy` / `Owns` inverse handling or descriptorless Commit paths.

### Bootstrap load-set source

The bootstrap load set is a generated, versioned Core Schema release bundle.
`schema-src/**/*.tdl` remains the only editable schema source. In particular,
`schema-src/core/core-schema-bootstrap.tdl` owns the `CoreSchemaSpace` holon
and bootstrap ownership overlay; it is compiled with the Core corpus rather
than hand-authored as loader JSON.

`map-schema` must generate a bootstrap bundle containing:

- the selected Core JSON loader imports;
- the generated bootstrap overlay; and
- a manifest recording the Core Schema release identity, required stable keys,
  selected imports, and their digests.

The generated bundle lives under `generated/core-schema-bootstrap/`. The
Conductora build copies it to
`host/conductora/resources/core-schema-bootstrap/` and includes that directory
as a Tauri resource. That copy is a distribution artifact, not an independently
maintained schema representation. Conductora reads the packaged files into the
existing in-memory `ContentSet`.

Conductora must select imports only through the generated manifest. It must not
glob `generated/json-imports/core/` at runtime, because that would make the
bootstrap release implicit and could include unrelated generated files.

### Bootstrap graph contents

One bootstrap transaction loads every import selected by the Core release
manifest and the generated bootstrap overlay. The graph contains the Core
Schema holon, its descriptors, value/property/relationship types, rules,
constraints, and every other holon emitted by that manifest.

The overlay stages one normal `HolonSpace.HolonType` instance:

```text
key: MAP.CoreSchemaSpace
HolonSpaceName: MAP.CoreSchemaSpace
DisplayName: MAP Core Schema Space
Description: The stewarding HolonSpace for the initial MAP Core Schema release.
DescribedBy: HolonSpace.HolonType
```

`HolonSpace.HolonType` must declare `HolonSpaceName`, `DisplayName`, and
`Description` as required instance properties. Its `InstanceKeyRule` is the
configured `HolonSpaceNameRule`, an ordinary instance described by
`FormatRule.KeyRuleType` with key `HolonSpaceNameRule.FormatRule`, template `$0`, and the single ordered
`HolonSpaceName.PropertyType` parameter.

Every persisted `HolonSpace` is a DHT anchor and is non-deletable. This is a
general descriptor-driven policy, not a CoreSchemaSpace exception:
`InstanceDeletionAllowed.PropertyType` is a required Boolean property with
`DefaultValue true` in `MetaHolonType.MetaTypeDescriptor`'s
`InstanceProperties`, and `HolonSpace.HolonType` explicitly sets it to
`false`. Deletion resolves the target's describing `HolonType` and its
effective deletion policy before it reaches guest persistence. `false`, an
absent required policy, a malformed value, or an unresolvable descriptor
rejects deletion with `HolonError::DeletionNotAllowed`.

The policy is restrictive through the describing-type `Extends` lineage: its
effective value is the logical AND of declarations in that lineage, with an
absent declaration using the `true` default. A subtype of
`HolonSpace.HolonType` therefore cannot make its instances deletable.

Every holon emitted by the Core release manifest, including the versioned Core
Schema holon, has a declared `OwnedBy -> MAP.CoreSchemaSpace` relationship.
Ordinary Commit materializes the corresponding `Owns` inverses. The
`CoreSchemaSpace` itself declares `OwnedBy -> MAP.CoreSchemaSpace`. Its
corresponding self `Owns` occurrence is the canonical root marker for the
first Space; it preserves the inherited exactly-one ownership contract without
requiring a schema exception.

`OwnedBy` expresses stewardship and membership, not an ancestry tree.
Implementations must not recursively follow it as a containment hierarchy.
`GetAllHolons` resolves the current space, traverses `Owns`, and excludes that
root reference itself from the returned collection.

The Reference/descriptor runtime currently treats an `InstanceKeyRule` target
as a key-rule descriptor. It must instead accept a configured key-rule holon,
classify it through its `DescribedBy` descriptor, and evaluate `FormatRule`
from its `TemplateString` and ordered `TemplateParameters`. This is required
before `HolonSpaceNameRule` can govern a live `HolonSpace` key.

### Discovery for later cells

The fixed `LocalHolonSpace` infrastructure path and link are the sole locator
for a cell's local `HolonSpace`, including the initial CoreSchemaSpace. No
CoreSchemaSpace-specific anchor is introduced.

Lookup must read all `LocalHolonSpace` links at the fixed path, retain only
targets that resolve to lineage-root `HolonNode` records, and require exactly
one valid candidate. Zero candidates means absent; more than one is ambiguous
and fails closed. Timestamp ordering or “newest link wins” is not a selection
policy.

Core bootstrap readiness applies the CoreSchemaSpace identity and release
manifest checks to that candidate. Ordinary later Spaces use the same locator
without requiring their local space to be CoreSchemaSpace. Additional cells
discover the anchor only; they do not invoke guest-side create-or-ensure
behavior.

### Current-space injection

The initial bootstrap transaction is the sole exception to the requirement
that a transaction begin with a persisted local-space ID: CoreSchemaSpace does
not exist before this transaction stages it. Conductora creates this as an
explicit `BootstrapProvisioning` transaction mode.

Only `BootstrapProvisioning` may cross the host-to-guest boundary without a
local-space ID. Guest ingress creates an unbound context for that mode and
must not invoke `ensure_local_holon_space`; the mode is restricted to the
bootstrap loader, Commit, and fixed infrastructure-anchor flow.

After Commit, Conductora discovers and verifies the persisted CoreSchemaSpace,
then calls the existing `HolonSpaceBehavior::set_space_holon_id` on the shared
`RuntimeSession` space manager. Every later transaction inherits that ID. The
existing session envelope carries it as a persisted smart reference and guest
context initialization binds it before any staging begins.

An ordinary transaction with no current-space ID fails immediately. Lazy
guest-side creation is not a fallback behavior.

### Ingress gate

Conductora owns an explicit in-process bootstrap gate with the phases
`Bootstrapping`, `Ready`, and `Failed`. It transitions to `Ready` only after
the bootstrap transaction has committed, the manifest-based readiness predicate
has succeeded, and the verified `CoreSchemaSpace` reference has been injected
into the shared runtime session.

`SetupManager::create_window` and the `startup:ready` event remain downstream
of that transition. In addition, each normal Conductora command ingress must
reject work while the gate is not `Ready`: the MAP Commands
`dispatch_map_command` route must do so before it binds or executes a command,
and the legacy `map_request` route must apply the same guard. `is_service_ready`
is true only when receptors, the MAP Commands runtime, and this bootstrap gate
are ready.

`BootstrapProvisioning` is the sole internal exception. It is invoked directly
by the Conductora bootstrap service and is not exposed through Tauri IPC. A
failed bootstrap leaves the gate `Failed` and terminates startup; the process
must not later accept ordinary work without a new startup and explicit recovery
where required.

### Bootstrap authorization boundary

Only `core_schema_bootstrap::ensure_core_schema_space` may create a
`BootstrapProvisioning` transaction. The mode is not representable by
`MapCommandWire`, Tauri IPC, or a user-provided `ContentSet`; Conductora alone
constructs its host-to-guest envelope.

The mode authorizes only the exceptional work needed for first-space
provisioning: beginning without a current-space ID, loading the packaged
manifest-verified bootstrap bundle, and writing the fixed `LocalHolonSpace`
anchor after the bootstrap graph commits. It does not grant a general-purpose
bootstrap API to a caller.

Ordinary `TransactionAction::LoadHolons` remains the generic import operation.
It always has a bound current space and follows normal command authorization.
It cannot select `BootstrapProvisioning`, supply an arbitrary bootstrap bundle,
or create the initial infrastructure anchor.

### Ready and incomplete states

The bootstrap design requires a durable readiness predicate that distinguishes:

- absent: no usable `CoreSchemaSpace` is discoverable;
- incomplete: a candidate anchor or partial graph exists but does not satisfy
  the bootstrap graph requirements; and
- ready: the stewarding `CoreSchemaSpace`, Core Schema graph, and required
  relationships are present and usable.

Readiness is manifest-based. It is satisfied only when:

1. the fixed `LocalHolonSpace` anchor resolves unambiguously to one
   lineage-root `CoreSchemaSpace`;
2. that holon has the bootstrap release's canonical key and
   `DescribedBy -> HolonSpace.HolonType` relationship;
3. every required holon in the versioned Core bootstrap manifest is persisted
   and resolvable by its stable key;
4. every required holon has its expected `DescribedBy` relationship and its
   declared `OwnedBy -> CoreSchemaSpace` relationship;
5. the corresponding `CoreSchemaSpace -> Owns` inverses are materialized; and
6. the manifest's Core Schema identity and version match the bootstrap release
   expected by the runtime.

The manifest is a complete minimum set, not an exact equality requirement on
the `Owns` collection. A later, separately governed schema evolution may add
owned holons without making an otherwise valid `CoreSchemaSpace` incomplete.

A failed or interrupted attempt must be safe to detect, and must not silently
select an arbitrary candidate when multiple bootstrap anchors exist.

### Failure and retry

Bootstrap uses a fail-closed, classification-based recovery policy:

- a bootstrap JSON parse or structural-validation failure is a packaged-input
  error: Conductora fails startup and does not retry it;
- a ready manifest predicate allows startup to continue, including after a
  previous process interruption;
- an absent state permits one fresh ordinary bootstrap transaction during that
  startup;
- a loader or transport error, or a Commit response whose
  `CommitRequestStatus` is not complete, fails startup; and
- incomplete or ambiguous durable state on a later startup fails startup and
  requires an explicit recovery action.

The service must inspect the loader and Commit response; absence of a Rust
error alone does not prove bootstrap success. It must archive the bootstrap
transaction and retain diagnostic context for every failed attempt. It must not
blindly replay the bootstrap load from incomplete state, because current Commit
behavior can persist pass-one holons before a pass-two relationship failure
marks the result incomplete.

### Schema evolution

This lifecycle provisions one initial, immutable Core Schema release; it does
not upgrade that release. `ensure_core_schema_space` may continue only when
the ready candidate has the bootstrap bundle's expected manifest identity. It
may load the packaged bundle once only for a truly absent first-space state.
A ready candidate for a different release, an incomplete state, or ambiguity
is a typed compatibility or recovery failure, not permission to rerun
bootstrap, append a release, or replace the anchored `CoreSchemaSpace`.

Core Schema evolution requires a distinct, explicitly authorized migration
lifecycle with declared source and target versions, compatibility checks, a
migration transaction, verification, and recovery or rollback semantics. It
is outside this bootstrap lifecycle.

## Subsequent Cells and Spaces

Additional cells in the first Space discover and reuse its ready
`CoreSchemaSpace`; they do not reload the Core Schema.

New Spaces are created from existing Spaces that already know their applicable
schemas. The eventual spawning contract is a `SchemaStewardSet`: it supplies a
persisted reference to the ready `CoreSchemaSpace` with a compatible versioned
Core Schema identity and, for every selected non-Core schema, a persisted
reference to that schema's stewarding `HolonSpace`, versioned `Schema` holon,
and resolution access route or trust channel. The selected schemas include
their direct `DependsOn` dependency closure.

For this bootstrap lifecycle, only the CoreSchemaSpace reference is required.
A new Space must reuse that established Core steward and must not load a second
local Core Schema merely because it creates a local `HolonSpace`. The spawn
command, transport representation, trust provisioning, and selection policy
for optional schemas are downstream work; this specification does not impose a
parent/child ownership model between Spaces.

## Delegated Contracts

| Concern | Authoritative document |
| --- | --- |
| Core Schema declarations and descriptor semantics | Type System specifications and `map-holons/schema-src/**/*.tdl` |
| Loader keys, staged-first resolution, and JSON representation | Holon Data Loader Design Specification |
| Staging, Commit, inverse materialization, and recovery | Transaction specifications |
| `LocalHolonSpace` infrastructure-link write and lookup mechanics | Storage Layer and SmartLink Design Specification |
| Host startup integration | Implementation plan derived from this specification |

## Deferred Design Work

No unresolved design decision blocks the initial bootstrap lifecycle described
here. The following are deliberately outside #674 and require separately
authorized designs:

1. DHT-level claim/election and conflict recovery for simultaneous independent
   Conductora cold starts;
2. administrative repair or rebuild of damaged durable bootstrap state;
3. later-space spawn commands, wire representation, trust provisioning, and
   optional-schema selection; and
4. Core Schema migration, release evolution, replacement, and steward
   succession.
