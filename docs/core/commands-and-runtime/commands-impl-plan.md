# Commands Implementation Plan (v1.0)
## Parallel IPC Contract and Descriptor-Bound Routing Delivery Sequence

## Change Log

### v1.0

- establishes the command implementation plan alongside the existing query and dance implementation plans
- aligns command delivery with the runtime shared types and bound-first dance/query contract refactor
- treats `docs/core/type-system/runtime-shared-types.md` as the canonical shared type foundation for command payloads and results
- preserves command-owned envelopes, scope containers, and wire/domain separation instead of collapsing Commands into runtime shared types
- separates IPC contract and adapter work from descriptor-backed command affordance and routing work
- recognizes `DanceRequest` and `QueryExpression` as transitional bridge payloads and `DanceV2(DanceInvocation)` as the new-world dance ingress path
- plans descriptor-backed `CommandType` / `AffordsCommand` anchoring without making Commands the semantic home of dance or query behavior

This document translates the current MAP Commands specification into a practical implementation sequence aligned with the descriptor-driven implementation roadmap.

It is intended to:

- break command delivery into concrete, dependency-aware phases
- distinguish IPC contract / wire-domain adapter stabilization from descriptor-dependent command affordance and routing work
- preserve a single phase sequence while allowing multiple PR tracks within that sequence
- prevent Commands from becoming the semantic owner of query, dance, validation, or descriptor behavior
- provide a basis for issue definition, sequencing, and parallel work decisions

This plan assumes:

- Commands own the TypeScript-to-host IPC ingress and structural command contract
- Commands do not own query semantics, dance semantics, descriptor semantics, or distributed behavior
- the single `dispatch_map_command` entrypoint and wire/domain sandwich model are normative
- the runtime shared type foundation now exists as a cross-surface baseline
- command envelopes and scope containers remain command-owned even when their inner payloads and results reuse runtime shared types
- general command payloads and results should converge on the canonical runtime shared type family
- narrower specialized types remain appropriate where they encode real legality or lifecycle constraints
- `CommandType` and `AffordsCommand` are the descriptor-backed anchor for command discovery
- command descriptor anchoring and static routing are layers on top of the IPC contract, not replacements for it

Related references:

- `docs/core/commands-and-runtime/commands.md`
- `docs/core/commands-and-runtime/commands-cheat-sheet.md`
- `docs/core/type-system/runtime-shared-types.md`
- `docs/core/descriptors/descriptors-design-spec.md`
- `docs/core/map-queries/queries-impl-plan.md`
- `docs/core/dances/dances-impl-plan.md`
- `docs/roadmap/desc-driven-impl-plan.md`

---

# 1. Delivery Principles

The implementation sequence follows these rules:

- `dispatch_map_command` remains the single IPC entrypoint for MAP command execution
- wire types must not cross below the binding seam
- runtime execution accepts already-bound domain commands only
- command scope remains explicit and structural rather than inferred from session state
- Commands adapt query and dance invocation into their owning substrates, but do not own query or dance semantics
- command contracts should prefer canonical runtime shared types for general payloads and results
- specialized command operands should remain where they encode real lifecycle or legality constraints
- descriptor-backed command affordances should discover commands, not replace the command IPC contract
- descriptor-bound routing should shrink central dispatch only after command descriptor anchoring is real

---

# 2. Phase Overview

The recommended command implementation sequence is:

1. IPC Contract and Runtime Shared Type Alignment
2. Wire / Domain Binding and Result Mapping Stabilization
3. Command Descriptor Schema Anchoring
4. Descriptor-Afforded Command Discovery
5. Descriptor-Bound Runtime Routing and Policy Enforcement
6. Cross-Surface Ingress Convergence and Bridge Migration
7. Dispatch Redistribution and TS / DAHN Readiness

The recommended PR segmentation uses two tracks:

- `PRO` = IPC / wire-domain / runtime-shared-type / contract track
- `PRS` = descriptor / policy / routing track

Recommended command PRs:

1. Command PRO1 - IPC Contract and Runtime Shared Type Alignment
2. Command PRO2 - Wire / Domain Binding and Result Mapping Stabilization
3. Command PRS1 - Command Descriptor Schema Anchoring
4. Command PRS2 - Descriptor-Afforded Command Discovery
5. Command PRS3 - Descriptor-Bound Runtime Routing and Policy Enforcement
6. Command PRO3 - Query and Dance Ingress Contract Convergence
7. Command PRS4 - Dispatch Redistribution and TS / DAHN Readiness

Each phase below defines:

- goal
- major deliverables
- why the phase exists
- dependencies
- exit criteria

---

# 3. Phase 1 - IPC Contract and Runtime Shared Type Alignment

## Goal

Align the command contract with the canonical runtime shared type family while preserving command-owned envelopes, scope containers, and wire/domain separation.

## Major Deliverables

- Command PRO1:
    - command contract alignment with runtime shared types
    - command payload/result disposition table in implementation issue form

- explicit command usage posture for:
    - `HolonReference`
    - `BoundHolonCollection`
    - `SmartReference` where smart-link-aware lifecycle behavior is contract-significant
    - `BaseValue`
    - `Row`
    - `RowSet`
- preservation of specialized command operands such as:
    - `TransientReference`
    - `LocalId`
    - `HolonId`
    - `PropertyName`
    - `RelationshipName`
- plural command result convergence on `BoundHolonCollection`
- restricted direct `Holon` use for infrastructure-level full-state transfer only
- explicit treatment of `HolonCollection` and `Vec<HolonReference>` as migration bridges or implementation helpers rather than command contract centers

## Why This Phase Exists

Commands sit at the TypeScript-to-host contract boundary, so they need stable payload and result shapes before descriptor-bound routing can safely harden.

After the runtime shared type refactor, this phase should be read as command-specific adoption of an existing cross-surface type foundation. It should not redefine runtime shared types or flatten command envelopes into the shared type family.

Without this phase:

- command result shapes will keep drifting independently from query and dance contracts
- plural command results may continue to harden around legacy collection forms
- command contracts may accidentally force projection where bound references are sufficient
- later TS and DAHN realignment will inherit avoidable shape churn

## Dependencies

- runtime shared types foundation
- Commands specification v1.1 contract posture

## PR Identity

- Command PRO1 / IPC contract and runtime shared type alignment

## Exit Criteria

- command payload and result shapes align with the canonical runtime shared type family
- command envelopes and scope containers remain command-owned
- specialized command operands are preserved only where they encode real constraints
- plural command contract results have a clear `BoundHolonCollection` target posture
- legacy collection and full-state transfer forms are explicitly classified

---

# 4. Phase 2 - Wire / Domain Binding and Result Mapping Stabilization

## Goal

Stabilize the host adapter seam so wire types bind into domain commands before runtime execution and domain results map back to wire results after execution.

## Major Deliverables

- Command PRO2:
    - binding seam stabilization
    - result mapping stabilization
    - wire leakage tests

- `MapIpcRequest` / `MapIpcResponse` envelope handling remains in the adapter layer
- `MapCommandWire` binds into `MapCommand`
- wire transaction identity binds to `Arc<TransactionContext>` where required
- wire holon references bind to domain `HolonReference`
- domain `MapResult` maps back to `MapResultWire`
- `Runtime::execute_command` receives no `*Wire` types
- `Runtime` remains independent of `map_commands_wire`
- request metadata such as `snapshot_after` remains IPC-layer metadata rather than descriptor policy

## Why This Phase Exists

The sandwich model is the strongest boundary in the command architecture. The implementation plan needs a dedicated phase for it because later descriptor routing and policy enforcement depend on a clean distinction between adapter binding and runtime execution.

Without this phase:

- wire types may leak into runtime code
- runtime may start owning IPC envelope behavior
- descriptor policy may be mixed with transport parsing
- query and dance ingress may become harder to adapt cleanly

## Dependencies

- Command PRO1 / IPC contract and runtime shared type alignment
- current three-crate command split

## PR Identity

- Command PRO2 / wire-domain binding and result mapping stabilization

## Exit Criteria

- adapter-owned binding and result mapping are explicit and tested
- runtime command execution receives only bound domain types
- no `*Wire` type crosses below the binding seam
- `map_commands_runtime` remains independent of `map_commands_wire`
- request metadata remains distinct from command lifecycle policy

---

# 5. Phase 3 - Command Descriptor Schema Anchoring

## Goal

Introduce descriptor-backed command identity through `CommandType`, `CommandDescriptor`, and `AffordsCommand` without changing the established IPC contract.

## Major Deliverables

- Command PRS1:
    - `CommandType` schema anchoring
    - `CommandDescriptor` wrapper reservation
    - `CommandLifecyclePolicy` rename for the existing lifecycle metadata type

- concrete `CommandType` holons for stable leaf command identities
- `AffordsCommand` / `AffordedBy` relationship shape
- command names derived from the descriptor header `type_name`
- `CoreCommandTypeName` or equivalent implementation aid for stable core command names
- no separate `CommandName` schema property in this phase
- explicit treatment of dance/query command-envelope identities as command descriptors whose invoked behavior semantics are owned elsewhere

## Why This Phase Exists

Commands need descriptor ownership for uniform behavior discovery, DAHN affordance surfaces, and future TS descriptor clients. But descriptor anchoring must not accidentally replace or duplicate the IPC command contract.

Without this phase:

- command discovery remains separate from descriptor-owned behavior lookup
- DAHN cannot present command affordances through the same model as dances
- central command routing cannot shrink safely
- the `CommandDescriptor` name remains ambiguous between schema wrapper and lifecycle metadata

## Dependencies

- Descriptor PR1 / runtime spine
- Descriptor PR2 / schema-backed structural descriptor surface
- command inventory from the Commands specification

## PR Identity

- Command PRS1 / command descriptor schema anchoring

## Exit Criteria

- `CommandType` exists as the schema type for command descriptors
- `CommandDescriptor` refers to the schema-backed wrapper
- existing lifecycle metadata is renamed to `CommandLifecyclePolicy`
- stable leaf command identities have concrete `CommandType` holons
- `AffordsCommand` is available as the command affordance relationship shape

---

# 6. Phase 4 - Descriptor-Afforded Command Discovery

## Goal

Expose descriptor-backed command discovery through the same effective inherited affordance model used for other descriptor-owned behavior.

## Major Deliverables

- Command PRS2:
    - descriptor-afforded command discovery surfaces
    - inherited flattened command affordance lookup

- `HolonDescriptor::afforded_commands()`
- `HolonDescriptor::get_command_by_name(...)`
- `HolonSpaceDescriptor::transaction_model()`
- `TransactionDescriptor::afforded_commands()`
- `TransactionDescriptor::get_command_by_name(...)`
- `HolonSpaceType` affords `BeginTransaction`
- `TransactionType` affords transaction-scoped MAP Commands
- effective command lookup through flattened `Extends`
- no caller-side inheritance reconstruction
- no global command registry as the caller-facing source of command existence

## Why This Phase Exists

This phase makes command affordances visible through descriptors before runtime dispatch is redistributed. That order lets clients and DAHN consume command discovery without coupling directly to handler internals.

Without this phase:

- TS and DAHN affordance work will need temporary command lookup mechanisms
- callers may reconstruct inheritance or scope rules manually
- descriptor-bound routing would lack a stable discovery surface

## Dependencies

- Command PRS1 / command descriptor schema anchoring
- descriptor inherited affordance lookup support

## PR Identity

- Command PRS2 / descriptor-afforded command discovery

## Exit Criteria

- commands are discoverable through descriptor-backed lookup
- effective inherited command lookup is flattened and caller-facing
- transaction-scoped command discovery is anchored through `TransactionDescriptor`
- no caller needs a second lookup mechanism for command existence

---

# 7. Phase 5 - Descriptor-Bound Runtime Routing and Policy Enforcement

## Goal

Route bound command execution through descriptor-resolved command affordances while preserving `Runtime` as the single execution and policy boundary.

## Major Deliverables

- Command PRS3:
    - descriptor-bound command routing
    - command lifecycle policy enforcement through descriptor-resolved command metadata

- runtime routing keyed by structural command variant plus descriptor-resolved command identity
- `CommandLifecyclePolicy` use for:
    - mutation classification
    - open transaction requirements
    - commit guard requirements
- scope-sensitive lifecycle semantics preserved
- command policy derived from descriptor metadata rather than ad hoc enum branching
- static Rust-local command dispatch in this phase
- dynamic command implementation loading explicitly out of scope

## Why This Phase Exists

Commands already have structural dispatch. This phase does not remove that useful shape; it adds descriptor-owned behavior identity and policy so routing and lifecycle enforcement converge with the broader descriptor model.

Without this phase:

- command descriptors remain discoverable but not operationally meaningful
- lifecycle policy remains detached from command identity
- central dispatch cannot shrink safely
- DAHN and TS clients may see affordances that do not match runtime execution policy

## Dependencies

- Command PRO2 / wire-domain binding and result mapping stabilization
- Command PRS2 / descriptor-afforded command discovery
- lifecycle policy metadata availability

## PR Identity

- Command PRS3 / descriptor-bound runtime routing and policy enforcement

## Exit Criteria

- bound command execution verifies descriptor-afforded command identity before execution where applicable
- lifecycle policy is enforced through command metadata
- runtime remains the single domain execution boundary
- static command dispatch is descriptor-anchored without introducing dynamic implementation loading

---

# 8. Phase 6 - Cross-Surface Ingress Convergence and Bridge Migration

## Goal

Converge command ingress for query and dance execution on their canonical new-world envelopes while preserving legacy bridge compatibility during transition.

## Major Deliverables

- Command PRO3:
    - query ingress contract convergence
    - dance ingress contract convergence
    - bridge payload migration posture

- `DanceV2(DanceInvocation)` remains the new-world dance command ingress path
- `Dance(DanceRequest)` remains legacy-only until cutover
- `Query(QueryExpression)` is treated as transitional ingress while Query PRO2 stabilizes the new query contract path
- Commands adapt query requests into the shared host query substrate rather than owning query execution semantics
- Commands adapt dance invocation into the dance execution substrate rather than owning dance semantics
- compatibility guidance for TS SDK callers during migration
- explicit deprecation posture for bridge payloads once downstream contracts are stable

## Why This Phase Exists

Commands are the TS-to-host front door, so query and dance contract transitions inevitably pass through the command layer. This phase makes that ingress work explicit without letting Commands absorb the semantics owned by query and dance documents.

Without this phase:

- legacy bridge payloads may harden into permanent architecture
- query and dance contract convergence may diverge at the command boundary
- TS callers may get conflicting migration signals

## Dependencies

- Command PRO1 / IPC contract and runtime shared type alignment
- Command PRO2 / wire-domain binding and result mapping stabilization
- Query PRO2 / query envelope and contract stabilization
- Dance PRO1 / shared invocation and result envelope foundation
- Dance PRO2 / runtime shared type and ABI alignment

## PR Identity

- Command PRO3 / query and dance ingress contract convergence

## Exit Criteria

- command ingress for dances targets `DanceInvocation` through `DanceV2`
- query command ingress has a documented path toward the Query PRO2 contract
- legacy bridge payloads are isolated and migration-scoped
- Commands remain adapters into query and dance substrates rather than semantic owners

---

# 9. Phase 7 - Dispatch Redistribution and TS / DAHN Readiness

## Goal

Shrink central dispatch and prepare command affordances for TS and DAHN consumption once descriptor-bound routing is real.

## Major Deliverables

- Command PRS4:
    - dispatch redistribution away from central dispatch
    - TS / DAHN command affordance readiness

- descriptor-local static command dispatch attachment points
- reduced central handler knowledge where descriptor-local routing can safely own it
- TS-facing command affordance shape for descriptor clients
- DAHN-facing command affordance menu readiness
- tests showing descriptor-discovered commands match executable command paths
- explicit non-goal for domain-definable commands in this phase

## Why This Phase Exists

Descriptor-backed discovery becomes fully useful when clients can rely on it and when runtime routing no longer depends on a parallel central registry. This phase intentionally waits until descriptor anchoring and policy enforcement have landed.

Without this phase:

- descriptor-discovered commands may remain presentation-only
- DAHN may still need temporary command menu sources
- central routing can remain larger than necessary

## Dependencies

- Command PRS3 / descriptor-bound runtime routing and policy enforcement
- TS descriptor client planning
- DAHN affordance menu planning

## PR Identity

- Command PRS4 / dispatch redistribution and TS / DAHN readiness

## Exit Criteria

- central dispatch is shrinking where descriptor-local routing is ready
- TS and DAHN can consume command affordances through descriptor-oriented surfaces
- executable command paths remain aligned with descriptor-discovered affordances
- command discovery becomes uniform with descriptor-owned dance discovery where applicable

---

# 10. Cross-Phase Dependency Summary

## Critical Path

1. Command contract alignment with runtime shared types
2. Wire / domain binding and result mapping stabilization
3. Command descriptor schema anchoring
4. Descriptor-afforded command discovery
5. Descriptor-bound runtime routing and policy enforcement
6. Query and dance ingress convergence
7. Dispatch redistribution and TS / DAHN readiness

## Key Dependency Rules

- command envelopes and scope containers remain command-owned even when inner payloads reuse runtime shared types
- wire/domain binding must be stable before descriptor-bound runtime routing hardens
- `CommandType` and `AffordsCommand` should exist before clients consume descriptor-backed command discovery
- descriptor-backed discovery should land before dispatch redistribution
- query and dance ingress migration should follow their owning contract plans rather than being invented inside Commands
- command descriptors identify command affordances; they do not make Commands the semantic home of query or dance behavior
- dynamic command implementation loading is out of scope for this plan

---

# 11. Parallel Work Guidance

## Safe Earlier Work

- command implementation sequence planning
- Command PRO1 / runtime shared type adoption for command payloads and results
- Command PRO2 / wire-domain binding and result mapping stabilization
- command inventory and bridge-type disposition review
- issue definition for command descriptor anchoring

## Safe Once Descriptor Structural Surface Exists

- Command PRS1 / command descriptor schema anchoring
- Command PRS2 / descriptor-afforded command discovery
- `CommandLifecyclePolicy` rename planning
- `HolonSpaceDescriptor` / `TransactionDescriptor` command discovery planning

## Safe Once Command Discovery Exists

- Command PRS3 / descriptor-bound runtime routing and policy enforcement
- static dispatch attachment-point design
- DAHN-facing command affordance planning

## Safe Once Query and Dance Contracts Stabilize

- Command PRO3 / query and dance ingress convergence
- bridge payload deprecation planning
- TS SDK migration guidance

## Safe Once Descriptor-Bound Routing Is Real

- Command PRS4 / dispatch redistribution
- TS descriptor client command affordance surfaces
- DAHN command affordance menus

---

# 12. Recommended Initial Issue / PR Sequence

A likely issue sequence is:

1. Command PRO1
   - align command payload and result contracts with the runtime shared type family
   - classify specialized operands, bridge payloads, and legacy collection forms
2. Command PRO2
   - stabilize wire-to-domain binding and domain-to-wire result mapping
   - add seam tests proving no wire leakage below binding
3. Command PRS1
   - introduce `CommandType`, `CommandDescriptor`, and `AffordsCommand`
   - rename lifecycle metadata to `CommandLifecyclePolicy`
4. Command PRS2
   - expose descriptor-backed command discovery on `HolonDescriptor`, `HolonSpaceDescriptor`, and `TransactionDescriptor`
   - define and test effective inherited command affordance lookup
5. Command PRS3
   - route command execution through descriptor-resolved command identity and lifecycle policy
6. Command PRO3
   - align query and dance command ingress with their canonical envelopes and bridge migration plans
7. Command PRS4
   - redistribute dispatch where descriptor-local static routing is ready
   - prepare TS and DAHN command affordance consumption

---

# 13. Immediate Next Step

The immediate next step should be to define the first issue in each early track:

- Command PRO1:
  - command runtime shared type adoption
  - command payload/result disposition table
  - plural command result convergence on `BoundHolonCollection`
  - bridge payload and direct `Holon` restrictions

- Command PRS1:
  - `CommandType` schema anchor
  - `AffordsCommand` relationship shape
  - `CommandDescriptor` wrapper reservation
  - `CommandLifecyclePolicy` rename

Those issues are the natural entry points for the command track.
