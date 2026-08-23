# Descriptor-Aware Validation Boundary

Descriptor-semantic validation belongs to Descriptor-Aware Holon Validation, not to TDL syntax
tooling or descriptor-independent PVL. Validation commitments are modeled holonically through the
Validation Schema and Core Schema together: each applicable type declares compatible implemented
`ValidationRule` family holons through definitional `ValidationBindings` relationships. The first
execution profile uses family-specific `ValidationRule` wrappers that implement built-in
`Validate` execution and dispatch by stable rule identity, while
dynamic `ValidationImplementation` holons, WASM execution, rule-set expansion, and validation
Dances remain deferred.
