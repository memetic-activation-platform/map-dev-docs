# Migration Checklist: Remove Legacy Ingress Path Through Holochain Receptor

## Summary
This checklist captures the safest removal sequence for the legacy ingress path that currently flows through `HolonsClient` -> `MultiplexService.dance()` -> `invoke("map_request")` -> deprecated holochain receptor handling.

The key principle is:

- migrate callers first
- verify no remaining UI/runtime consumers
- then remove host registration and deprecated runtime plumbing
- only remove the legacy ingress command after the last caller is gone

## Current dependency map

### Already migrated
- `uploadHolons(contentSet)` in `host/ui/src/app/stores/content.store.ts`
- SDK transport via `dispatch_map_command` in `host/map-sdk/src/internal/transport.ts`

### Still dependent on the legacy path
- Angular `HolonsClient` in `host/ui/src/app/clients/holons.client.ts`
- `MultiplexService.dance()` in `host/ui/src/app/services/multiplex.service.ts`
- most content-space store operations in `host/ui/src/app/stores/content.store.ts`
- Tauri `map_request` ingress in `host/conductora/src/map_commands/map_request.rs`
- deprecated receptor registration in `host/conductora/src/setup/providers/holochain/setup.rs`
- legacy Rust bridge in `host/crates/holons_client/src/lib.rs`
- deprecated runtime implementation in `host/crates/holochain_receptor/src/deprecated_holochain_receptor.rs`

## Goal
Remove the deprecated holochain receptor ingress without breaking content-space UI behavior, while preserving the new SDK/command-runtime path as the single supported ingress.

## Recommended migration sequence

### Phase 1: Freeze scope and identify remaining legacy callers
- [ ] Confirm that no new UI work should be added on top of `HolonsClient`
- [ ] Inventory every remaining call site of `HolonsClient` methods
- [ ] Inventory every remaining `invoke("map_request", ...)` call
- [ ] Document the mapping from each legacy client operation to its SDK or `dispatch_map_command` replacement

### Phase 2: Migrate the content-space store off the legacy client
- [ ] Replace `loadall()` in `host/ui/src/app/stores/content.store.ts` with SDK-backed reads
- [ ] Replace `createClone(...)` with SDK-backed transaction/runtime commands
- [ ] Replace `updateOneWithProperties(...)` with SDK-backed transaction/runtime commands
- [ ] Replace `createOne(...)` with SDK-backed transaction/runtime commands
- [ ] Replace `commitOne(...)` with SDK-backed transaction/runtime commands
- [ ] Replace `stageOne(...)` with SDK-backed transaction/runtime commands
- [ ] Replace `commitAllStaged()` with SDK-backed transaction/runtime commands
- [ ] Replace the fallback `getHolon(...)` hydration reads with SDK-backed holon reads

### Phase 3: Remove UI dependence on `HolonsClient`
- [ ] Stop injecting `HolonsClient` into `ContentStore`
- [ ] Remove any remaining direct component/controller use of `HolonsClient`
- [ ] Keep all content-space mutations and reads flowing through the store and SDK path
- [ ] Verify the uploader flow still works after the rest of the store is migrated

### Phase 4: Remove UI dependence on `MultiplexService.dance()`
- [ ] Confirm that no content-space flows still call `MultiplexService.dance()`
- [ ] Confirm whether `MultiplexService` is still needed for any non-content-space path
- [ ] If still needed elsewhere, narrow its responsibility explicitly
- [ ] If no longer needed, remove `MultiplexService.dance()` and its `map_request` transport usage

### Phase 5: Verify host-side command coverage on the new path
- [ ] Confirm that `dispatch_map_command` supports every migrated store operation
- [ ] Fill any missing command coverage in:
    - `host/crates/map_commands_wire`
    - `host/crates/map_commands_contract`
    - `host/crates/map_commands_runtime`
- [ ] Verify wire-to-runtime binding stays at the ingress boundary
- [ ] Verify no new `MapRequest`-shaped fallback logic was introduced during migration

### Phase 6: Remove deprecated receptor registration from host setup
- [ ] Remove the deprecated-path block in `host/conductora/src/setup/providers/holochain/setup.rs`
- [ ] Stop calling `build_receptor(...)` for deprecated consumers
- [ ] Stop calling `register_receptor(...)` when no legacy consumers remain
- [ ] Keep `ActiveStorageReceptor` and `RuntimeInitiatorState` wiring intact for the new path

### Phase 7: Remove legacy Tauri ingress
- [ ] Remove `map_request` command registration from host app setup
- [ ] Remove `host/conductora/src/map_commands/map_request.rs`
- [ ] Verify no frontend code still invokes `map_request`
- [ ] Verify no tests/fixtures still depend on `map_request`

### Phase 8: Remove deprecated Rust bridge types and implementation
- [ ] Remove legacy `Receptor` usage in `host/crates/holons_client/src/lib.rs`
- [ ] Remove `DeprecatedHolochainReceptor` usage in `host/crates/holochain_receptor/src/deprecated_holochain_receptor.rs`
- [ ] Remove deprecated shared types or config structures that only exist for that path
- [ ] Remove any setup helpers that only serve deprecated receptor registration

### Phase 9: Clean up tests and fixtures
- [ ] Update UI tests to use the SDK-backed path assumptions
- [ ] Update host tests to validate `dispatch_map_command` instead of `map_request`
- [ ] Remove fixtures that only exercise deprecated receptor ingress
- [ ] Add regression coverage for each migrated content-space operation

## Safe checkpoints after each phase

### After Phase 2
- [ ] Content space can still load
- [ ] Create/stage/commit flows still work
- [ ] Loader result presentation still works
- [ ] No regression in single-file error presentation

### After Phase 4
- [ ] No content-space path uses `HolonsClient`
- [ ] No content-space path uses `MultiplexService.dance()`

### After Phase 6
- [ ] App startup still succeeds without deprecated receptor registration
- [ ] Runtime initialization still succeeds
- [ ] Space queries still resolve through `ActiveStorageReceptor`

### After Phase 8
- [ ] No references remain to deprecated receptor types
- [ ] No `map_request` ingress remains in frontend or host
- [ ] New command-runtime ingress is the only supported path

## Suggested validation steps
- [ ] Run `npm run web:typecheck -w map-host`
- [ ] Run `npm run check`
- [ ] Run `npm run test:unit`
- [ ] Run `npm run sweetest`
- [ ] Manually verify:
    - content-space load
    - create holon
    - stage holon
    - commit one
    - commit all staged
    - clone flow
    - loader success case
    - loader error case

## Removal completion criteria
- [ ] No frontend code imports or calls `HolonsClient` for content-space operations
- [ ] No frontend code calls `invoke("map_request", ...)`
- [ ] `map_request` is no longer registered in the host
- [ ] Deprecated holochain receptor registration is removed from startup
- [ ] Deprecated receptor implementation is deleted
- [ ] Regression coverage exists for all migrated operations
- [ ] The SDK/command-runtime path is the single ingress path for content-space behavior

## Notes
The safest cut line is to treat `ContentStore` migration as the main dependency breaker. Once `ContentStore` no longer depends on `HolonsClient`, the rest of the legacy removal becomes much more mechanical and lower risk.