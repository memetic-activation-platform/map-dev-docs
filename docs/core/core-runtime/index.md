# MAP Core Runtime

The core runtime documentation defines the shared holonic representation and
runtime behavior used by MAP components. It owns holons, references, runtime
states, typed wrapper conventions, collections, and other cross-cutting runtime
contracts.

Runtime descriptor support is a subsystem of the core runtime. Universal
schema structure and descriptor semantics remain owned by the
[type-system section](../type-system/map-type-system.md).

This directory is the target location for core-runtime documents during the
documentation refactor. See the
[document role manifest](../document-role-manifest.md) for ownership and
authority rules.

## Canonical documents

- [MAP Runtime Shared Types](runtime-shared-types.md) defines the shared runtime
  carriers and representation contracts reused across MAP components.
- [Runtime Descriptor Subsystem](descriptors/descriptors-design-spec.md) defines
  descriptor access and descriptor-driven runtime behavior.
