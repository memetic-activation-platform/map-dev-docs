# Coordinator Surface Policy

MAP treats coordinator WASM contents as an explicit production boundary. Test-only application
functions must not become callable merely because they are documented as unsupported or named
`_for_test`.

This policy governs coordinator zomes packaged into production DNA and hApp artifacts, loose
coordinator WASMs used only by tests, classification of every exported WASM symbol, and creation
and execution of test-only authoring probes.

## Production boundary

Every export in a coordinator WASM packaged into a production DNA or hApp is production artifact
surface and must be classified.

Every application function dispatchable through Holochain's zome-call interface is
production-callable surface unless an effective authorization boundary proves otherwise. Names,
comments, undocumented status, or an "internal" designation do not constitute authorization
boundaries.

In particular, ordinary Holochain capability grants cannot deny a function to the cell's own chain
author while allowing other functions to that same author. A test-only function compiled into the
production coordinator must therefore be treated as production-callable.

Test-only application functions must be absent from production artifacts by construction.

## Required export classification

Every export from each production coordinator WASM and test-probe WASM must appear in the
source-controlled coordinator-surface manifest. Each row records:

```text
{ zome, symbol, exposure_kind, classification, rationale }
```

### Exposure kinds

Use the narrowest applicable exposure kind:

- `zome_call`: an application function dispatchable through Holochain's zome-call interface.
- `callback`: a coordinator lifecycle callback invoked by Holochain.
- `integrity_callback`: an Integrity callback present in the linked WASM.
- `abi`: an allocator, deallocator, runtime helper, or other ABI-support function.
- `memory`: exported WASM memory.
- `global`: an exported WASM global.
- Unknown or newly observed export: requires review and an explicit supported kind before the
  artifact may pass inspection.

An unknown export is not implicitly harmless. It is an audit failure until its origin and purpose
are understood.

### Classifications

Use one of these roles:

- `supported`: an intentionally supported production application API.
- `legacy_ingress`: a production-callable application function retained for compatibility or
  pending a contract decision, but not considered a preferred modern API.
- `callback`: a Holochain callback rather than an application-callable API.
- `abi`: generated, linked, or runtime-support surface.
- `test_only`: an application function allowed only in a loose test-probe WASM.

"Internal" is not a separate safety classification for a dispatchable function. If a function
ships and can be called, it must be classified as `supported` or `legacy_ingress` unless an
effective authorization boundary is demonstrated.

Every classification must include a rationale explaining why the symbol belongs in that artifact
and, for application functions, what contract or test need it serves.

## Changing the production coordinator surface

Update the coordinator-surface manifest whenever an export is added, removed, or renamed. This
includes changes caused by:

- adding or removing an `#[hdk_extern]`;
- adding or removing a Holochain callback;
- changing packaged coordinator zomes;
- linking a crate that contributes exported symbols;
- changing Holochain, HDK, Rust, linker, or other toolchain behavior;
- removing an obsolete production entrypoint.

For a new production application function:

1. Confirm that it is an intentional production ingress.
2. Prefer an existing canonical API rather than introducing a parallel path.
3. Classify it as `supported` or `legacy_ingress`.
4. Document its contract and rationale in the surface manifest.
5. Add behavioral coverage appropriate to the new functionality.
6. Rebuild the packaged artifacts and run the exact export audit.

A new export must never be added to the manifest merely to silence the audit. Unexpected linkage
must be investigated before classification.

Removing or renaming a function also requires updating the manifest. The audit compares the
inventory in both directions, so both unclassified exports and stale manifest rows are errors.

## Artifact inspection requirements

Artifact inspection must operate on the coordinator WASM embedded in the packed production DNA
and hApp, not merely on a file found in a Cargo target directory.

The audit must prove:

- the production DNA and hApp contain exactly the approved coordinator zomes;
- no test-probe coordinator is packaged;
- every actual production export is classified;
- every classified production export is present;
- no production export is classified `test_only`;
- every loose probe-WASM export is classified;
- every expected probe function is present;
- the probe WASM contains no production zome-call entrypoints.

Generated functions, callbacks, memory, and globals remain part of the inventory even when they
are not application-callable. Exact accounting prevents unexpected linkage from being mistaken for
harmless runtime support.

## When a test probe is permitted

A new test probe requires explicit justification. A probe is appropriate only when a real
Integrity path cannot be exercised through a canonical production coordinator API. Typical
examples include proving that Integrity rejects:

- malformed serialized data that production encoders cannot create;
- an invalid action topology that canonical persistence resolves or prevents;
- a raw link or entry operation unavailable through supported production APIs.

A probe must not be added merely to simplify test setup, avoid using a canonical API, or expose
otherwise convenient raw storage access. When the canonical production API can reach the required
behavior, the test must use that API instead of a probe.

The probe's rationale must identify:

- the specific Integrity rule being exercised;
- why canonical production APIs cannot construct the relevant operation;
- the minimum raw-authoring capability required;
- the expected Integrity acceptance or rejection being asserted.

## Probe implementation rules

Every test-only application function must live in a separate test-probe coordinator zome. The
probe zome:

- must be built as a loose test artifact;
- must not appear in any production DNA or hApp manifest;
- must not depend on the production coordinator implementation crate;
- may depend on Integrity types and other WASM-safe implementation types it needs;
- must declare its dependency on the installed production Integrity zome;
- must keep error projection local rather than widening production-only helpers;
- must expose only the minimum operations needed by approved Integrity tests;
- must not declare callbacks such as `init` unless the test design specifically requires and
  verifies them.

The prohibition on depending on the production coordinator implementation is structural. HDK
extern symbols contributed through an rlib dependency may survive WASM linking and unintentionally
reproduce the production coordinator API in the probe artifact.

Each probe must have:

- a `test_only` surface-manifest row;
- a narrow input type;
- comments explaining the Integrity path it exists to exercise;
- conductor-level assertions proving the intended acceptance or rejection;
- no broader authoring authority than the test requires.

## Probe test-conductor pattern

Probe-dependent tests must use an isolated conductor. A probe-enabled conductor must never be
shared with production-only assertions because coordinator updates mutate the conductor's
registered DNA definition.

The setup sequence is:

1. Build and install the unchanged packaged production DNA.
2. Call the probe zome before augmentation and prove dispatch fails because the zome is
   unregistered.
3. Capture the installed DNA hash, Integrity-zome definitions, coordinator names, and active
   production coordinator WASM hash.
4. Build a coordinator-update payload containing only the test-probe coordinator.
5. Declare the probe's dependency on the installed production Integrity zome.
6. Apply the update.
7. Reload conductor state when required by the supported Holochain version.
8. Verify that:
    - coordinator names changed only by adding the test-probe coordinator;
    - the active production coordinator WASM hash is unchanged;
    - the probe definition references the freshly built probe WASM;
    - Integrity definitions are unchanged;
    - rehashing the effective updated `DnaDef` produces the installed production `DnaHash`;
    - a normal production coordinator call still succeeds;
    - the probe is now dispatchable.
9. Run the probe-dependent assertions.

The update payload must never include a same-named production coordinator definition. Holochain
replaces an existing coordinator when names match, which would invalidate the claim that tests
retain the installed production coordinator.

## Build ordering

Probe-dependent tests must not consume stale artifacts. The required order is:

```text
build production zomes
pack production DNA and hApp
build the loose probe WASM
audit production and probe artifacts
run conductor tests
```

CI must cover both exact production and probe artifact inspection and the isolated probe-enabled
conductor path.

## Review checklist

A review that changes coordinator code should confirm:

- Does the packaged export inventory change?
- Was every added, removed, or renamed export reflected in the manifest?
- Is each new zome-call function an intentional production API?
- Does its rationale describe the actual contract?
- Could an existing canonical API satisfy the use case?
- Did dependency linkage introduce unexpected exports?
- Are all `test_only` functions confined to the probe zome?
- Is the probe absent from production manifests?
- Does each probe justify an Integrity path canonical APIs cannot reach?
- Do probe-enabled tests install the production DNA before isolated augmentation?
- Do runtime invariance assertions still pass?

## Version assumptions

The isolated augmentation pattern relies on verified Holochain behavior, including the treatment
of coordinator definitions in DNA identity and the append-versus-replace semantics of coordinator
updates. These assumptions must be reverified when upgrading Holochain. Runtime assertions—not this
prose alone—must pin the behavior on which the test boundary depends.

Preserving DNA identity and Integrity definitions does not prove identical validation outcomes
across different chain state, network state, dependency availability, conductor configuration, or
test sequencing.
