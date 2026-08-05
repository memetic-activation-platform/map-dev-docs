# Runtime Descriptor Subsystem

The runtime descriptor subsystem prepares explicit holon graphs for descriptor
evaluation, invokes the descriptor kernel, and exposes descriptor-specific
runtime behavior through the core holonic runtime.

This section owns runtime integration and layering. The structural schema model
and representation-neutral descriptor algorithms belong to the type system.

## Design Documents

- [Runtime Descriptor Subsystem Design Spec](descriptors-design-spec.md) is the
  master runtime descriptor design and delegation point.
- [Layered Descriptor Architecture](../../descriptors/layered-desc-arch.md)
  defines creation, completion, representation, and kernel-invocation layers.
  It remains at its previous path until that document's focused review.

See the [document role manifest](../../document-role-manifest.md) for ownership
and authority rules.
