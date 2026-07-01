# TDL Emitter Acceptance Rubric

The TDL emitter’s job is to generate the most concise valid TDL it can from canonical holon JSON, while preserving recompilable semantic truth. The emitter is successful when it prefers spec-native descriptor syntax wherever that syntax can faithfully represent the source, and uses literal fallback only where concise TDL would lose information or change recompilation behavior.

## 1. Non-Negotiable Fidelity Requirements

These are gating requirements. If any fail, the emitter is not acceptable.

### 1.1 Round-Trip Semantic Fidelity

For the supported corpus, `JSON -> TDL -> JSON` must preserve:

- file partitioning
- holon keys
- descriptor target (`type` / `DescribedBy`) semantics
- property names
- property values
- property ordering
- relationship entries
- relationship ordering
- relationship target shape
- relationship target ordering

Allowed deltas must be explicitly whitelisted. Today that means `meta` differences only.

### 1.2 No Hidden Semantic Reinterpretation

The emitter must not rely on name-based magic that changes the meaning of ordinary TDL syntax.

Examples:

- `property X` must always mean ordinary property-keyword semantics
- `value X` must always mean ordinary value-keyword semantics
- bootstrap names must not silently override keyword injections

If a concise ordinary form would compile with the wrong meaning, the emitter must not use it.

### 1.3 Literal Fallback Must Be Truth-Preserving

Whenever the emitter falls back to literal `properties { ... }` or literal `relationships { Name -> ... }`, recompilation of that emitted TDL must preserve the original JSON semantics exactly.

---

## 2. Concision Requirements

These define what “trying hard” means.

### 2.1 Prefer Spec-Native Descriptor Surface

The emitter should use the most specific valid descriptor form available:

- `value`
- `property`
- `relationship`
- `def relationship`
- `inverse relationship`
- `enum`
- `variant`
- `holon`

It should not emit `holon` when a more specific form can express the same semantics faithfully.

### 2.2 Prefer Semantic Clauses Over Literal Blocks

When source content can be represented faithfully through spec clauses, emit clauses instead of literal payloads.

Prefer:

- `extends Foo`
- `value Bar`
- `source Foo`
- `target Bar`
- `inverse Baz`
- `keyrule Rule`
- `cardinality 0..1`
- `ordered`
- `duplicates`
- `deletion_semantic Allow`

instead of raw literal property/relationship encodings.

### 2.3 Prefer Attachment Blocks Over Raw Relationship Dumps

For holon descriptors, prefer semantic attachment blocks when possible:

- `properties { SomeProperty }`
- `relationships { SomeRelationship }`

Do not emit literal relationship lines when a valid attachment reference expresses the same meaning.

### 2.4 Prefer Enum/Variant Structure When Possible

When enum semantics can be faithfully recovered, emit:

- `enum ...`
- nested `variants { ... }`
- standalone `variant ...` only when needed

Do not flatten enum structure into generic holon literal form unless required for fidelity.

---

## 3. Literal Fallback Rules

Literal fallback is acceptable only when all of the following are true:

1. A spec-native concise form exists syntactically, but using it would change recompilation semantics; or
2. The current TDL surface cannot express the source holon content faithfully; or
3. The concise form would require hidden special cases not defined by the spec.

When fallback is used, it should be the minimum necessary fallback.

### 3.1 Minimal Fallback Principle

If only relationships are not concisely expressible:
- keep concise descriptor keyword and header where valid
- fall back only for the relationship body portion

If only a bootstrap anchor cannot honestly use a specific keyword:
- emit it in literal-safe form
- do not degrade unrelated ordinary descriptors nearby

### 3.2 No Convenience Fallback

Literal fallback must not be used merely because:
- it is easier to implement
- it avoids improving semantic detection
- it avoids deriving descriptor structure that is already available

---

## 4. Bootstrap Handling Rules

### 4.1 No Silent Bootstrap Exceptions

Bootstrap descriptors must not be emitted in ordinary concise forms unless those forms compile back with their true semantics under the published spec.

### 4.2 Honest Bootstrap Surface

If a bootstrap anchor cannot yet be represented honestly in ordinary concise TDL, the emitter must use a more literal-safe surface rather than a misleading concise one.

### 4.3 Bootstrap Cases Must Shrink Explicitly

Any remaining bootstrap literal cases should be tracked explicitly as known expressivity gaps, not left as accidental behavior.

---

## 5. Output Quality Requirements

These are secondary to fidelity, but still required for canonical checked-in TDL.

### 5.1 Stable Formatting

Emitter output must be stable across runs.

### 5.2 Readable Grouping

Use braced form, header blocks, attachment blocks, and clause ordering consistently.

### 5.3 Avoid Redundant Literal Noise

Do not emit raw `properties { ... }` containing fields that are already faithfully represented by:
- header fields
- keyword kind
- clause form
- semantic attachment blocks

unless needed for exact recompilation.

---

## 6. Acceptance Levels

### Level A: Fully Acceptable

- Round-trip fidelity passes
- Core schema output is predominantly concise spec-native TDL
- Literal fallbacks are few, localized, and justified
- No hidden name-based semantic exceptions exist

### Level B: Technically Acceptable, Refinement Needed

- Round-trip fidelity passes
- Output recompiles correctly
- But too much of the corpus is still emitted in literal fallback form
- Remaining fallback surface is larger than necessary

### Level C: Not Acceptable

Any of the following:
- round-trip semantic drift
- key/order/relationship-shape loss
- misleading concise forms that compile back differently
- hidden bootstrap name exceptions
- generic literal dumping used where concise faithful TDL was available

---

## 7. Practical Review Questions

For each emitted descriptor, reviewers should ask:

1. Could this have been emitted with a more specific keyword?
2. Could any literal property have been emitted as header or clause syntax?
3. Could any literal relationship have been emitted as semantic clause or attachment syntax?
4. Is any remaining literal fallback necessary for truth, or just implementation convenience?
5. If this emitted TDL became canonical checked-in source, would a human want to maintain it?

If the answer to 5 is repeatedly “no,” the emitter still needs refinement even if round-trip tests pass.