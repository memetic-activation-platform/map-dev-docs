# MAP Validation Architecture Design Spec

## Overview

This document outlines an **extensible, declarative validation system**, grounded in holonic design, dance-based dispatch, and Promise Theory alignment. It allows validation logic to be declared, discovered, and executed in a way that is modular, inspectable, and open to extension by communities and contributors.

---

## Core Concepts

### ✅ Validation is:
- **Rule-driven**: Each validation behavior is encapsulated in a `ValidationRule` holon.
- **Declaratively extensible**: ValidationRules are holons that declare their type, purpose, scope, and implementation.
- **Dynamically dispatched**: ValidationRules perform standardized Dances against holon instances.
- **Promise-aware**: Rules implicitly or explicitly advertise their availability using Promise Theory.

---

## Holon Types

### `ValidationRule`
A holon that defines a single unit of validation logic.

```json
{
  "key": "KeyRequired.Rule",
  "type": "#ValidationRule",
  "display_name": "Key is Required",
  "description": "Ensures that a holon instance of this type has a key defined.",
  "properties": {
    "severity": "error",
    "applicability_scope": "instance",
    "engine": "wasm"
  },
  "relationships": {
    "Implements": [{ "$ref": "#check-key.WasmScript" }],
    "PerformsDance": [{ "$ref": "#ValidateInstance.Dance" }],
    "AppliesTo": [{ "$ref": "#MetaHolonType" }]
  }
}
```

#### Standard properties:
- `severity`: `"error" | "warning" | "suggestion"`
- `applicability_scope`: `"instance" | "type | file"`
- `engine`: `"wasm" | "jsonlogic" | "rust" | ...`

#### Standard relationships:
- `Implements`: Link to executable logic (WASM, JSONLogic, Rust code, etc.)
- `PerformsDance`: References the `DanceType` (typically `#ValidateInstance.Dance`)
- `AppliesTo`: List of `MetaType` or `TypeDescriptor` holons to which this rule applies
- `Overrides`: (Optional) Overrides another rule definition

---

### `ValidationRuleSet`
A collection of `ValidationRule` holons for reuse and grouping.

```json
{
  "key": "StandardHolonRules.RuleSet",
  "type": "#ValidationRuleSet",
  "relationships": {
    "IncludesRule": [
      { "$ref": "#KeyRequired.Rule" },
      { "$ref": "#ValidTypeReference.Rule" }
    ]
  }
}
```

---

### `ValidateInstance.Dance`
A standard DanceType for performing validation of a holon instance.

```json
{
  "key": "ValidateInstance.Dance",
  "type": "#DanceType",
  "display_name": "Validate Holon Instance",
  "description": "A validation rule evaluates a single holon instance and returns a structured result."
}
```

---

## Execution Model

Validation is invoked via the **Dance Dispatch Engine**:

```rust
fn validate_instance(instance: &Holon, type_descriptor: &TypeDescriptor) -> Vec<ValidationResult> {
    let rules = collect_applicable_rules(type_descriptor);
    rules.iter().map(|rule| {
        perform_dance(
            dancer = rule,
            target = instance,
            dance_type = "ValidateInstance.Dance"
        )
    }).collect()
}
```

Each dance produces one or more `ValidationResult` holons.

---

## Integration with Type System

### `MetaType` holons declare:
```json
{
  "key": "MetaHolonType",
  "type": "#MetaTypeDescriptor",
  "relationships": {
    "ValidationRules": [
      { "$ref": "#KeyRequired.Rule" },
      { "$ref": "#ValidTypeReference.Rule" }
    ]
  }
}
```

### `TypeDescriptor` holons:
- Inherit rules from their `Extends` relationship
- May declare additional rules in `ValidationRules`

---

## Promise Theory Alignment

Each `ValidationRule` holon is a **Promise**:
- "I promise to perform validation for instances of X."
- This promise is made visible via the `AppliesTo` and `PerformsDance` relationships.

The **Dance** is the actualization of that promise:
- A rule (the dancer) performs validation on a target (the holon instance) of a given type.

Promise Theory ensures:
- Voluntary participation
- Declarative trust boundaries (via membranes)
- Self-description and introspection of all commitments

---

## Benefits

| Feature               | Description |
|------------------------|-------------|
| **Extensibility**      | Anyone can publish new validation rules as holons |
| **Declarativity**      | Validation behavior is explicitly described and inspectable |
| **Modularity**         | Rules are composable, reusable, and versioned |
| **Runtime dispatch**   | Rules are dynamically discovered and executed as dances |
| **Auditability**       | All validation results are traceable through `DanceResult` holons |
| **Unified execution**  | Same engine handles both system and user-defined rules |

---

## Future Extensions

- **Parameterized Rules** (e.g., “must-have-property” with a parameter for property name)
- **ValidationWorkflows** to sequence rules
- **Human-in-the-loop Rules** (using `Performer: Human`)
- **Rule Scoping and Targeting** by context, agent, or domain
