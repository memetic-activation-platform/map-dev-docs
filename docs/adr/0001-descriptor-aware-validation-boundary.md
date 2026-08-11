# Descriptor-Aware Validation Boundary

Descriptor-semantic validation belongs to Descriptor-Aware Holon Validation, not to TDL syntax
tooling or descriptor-independent PVL. Validation commitments are modeled holonically through the
Validation Schema, where type descriptors attach compatible `ValidationRule` family holons through
typekind-specific `Validations` relationships sharing the same local relationship name; the first
execution profile uses family-specific `ValidationRule` wrappers that implement built-in
`Validate` execution and dispatch by stable rule identity, while
dynamic `ValidationImplementation` holons, WASM execution, rule-set expansion, and validation
Dances remain deferred.
