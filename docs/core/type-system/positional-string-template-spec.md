# Positional String Template Specification

A positional string template renders an ordered sequence of prepared scalar inputs into a
`MapString`. It supports literal text, required and optional substitutions, and segments whose
punctuation is emitted only when all their referenced inputs are present.

## Scope and responsibilities

Position zero identifies the first parameter. Rendering operates on the supplied sequence and
requires no descriptor resolution, property or relationship traversal, version selection, or
holon mutation. Key-rule strategies acquire their own inputs. `FormatRule` uses its ordered
`TemplateParameters` relationship to property descriptors. Other strategies can supply values
through their own input contracts. The template language defines positional references and
absence behavior. Schema-level property requiredness remains an independent obligation.

Key composition is read-only. When a strategy uses a related holon's key, it reads the stored
key of the exact selected version. Producers explicitly compose and set keys. Commit derives an
expected key where the key-policy execution boundary requires it and compares it with the stored
key. [Key composition and identity contract](schema-design-spec.md#96-key-composition-and-identity-contract)

## Schema representation

`TemplateString.PropertyType` selects `PositionalStringTemplateValueType.MapStringValueType`,
a specialization of `MapStringValueType.StringValueType`. Template source is stored as an
ordinary String. The ValueType's mandatory, presence-only
`PositionalStringTemplateSyntaxConstraint` uses the same parser as template construction. Its
evaluation checks syntax independently of parameter resolution and key composition. Validation
fails closed when no evaluator is registered. [Value Constraints Design Specification](value-constraints-design-spec.md#constraint-interpretation-and-errors)

Inherited String operators retain their semantics. When the subject has the template ValueType,
authored `Equals` and `LessThan` operands must also conform to that ValueType. `Contains` takes
an ordinary String operand, which can be an incomplete template fragment such as `{0`.
[Query operand conformance](../map-queries/query-engine-design-spec.md#typed-literal-operands)

## Surface syntax

| Form | Meaning |
| --- | --- |
| `{0}` | Required substitution at the top level |
| `[1]` | Optional substitution. An absent input emits nothing. |
| `[.{1}]` | Optional segment. An absent input omits both the dot and the substitution. |
| `[{1}-{2}]` | Optional segment that requires both inputs to be present |
| `{{` and `}}` | Literal opening and closing braces |
| `\[` and `\]` | Literal opening and closing brackets |
| `\\` | Literal backslash |
| `\$` | Literal dollar sign, including before a digit |

All examples show decoded templates. TDL and JSON apply their own quoting and escaping before
the template parser receives the text.

## Grammar

The grammar operates on Unicode scalar values. Quoted terminals represent exact characters.
The backslashes in single-quoted terminals are literal characters in this notation.

```ebnf
template         = { piece } ;
piece            = literal | escape | required | optional-field | optional-segment ;
required         = "{", index, "}" ;
optional-field   = "[", index, "]" ;
optional-segment = "[", segment-body, "]" ;
segment-body     = { segment-piece } ;
segment-piece    = literal | escape | required ;
index            = "0" | nonzero-digit, { digit } ;
digit            = "0" | nonzero-digit ;
nonzero-digit    = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
escape           = "{{" | "}}" | '\[' | '\]' | '\\' | '\$' ;
literal          = scalar-except-delimiters ;
```

`scalar-except-delimiters` admits any Unicode scalar value other than `{`, `}`, `[`, `]`, or
backslash, subject to the NUL and legacy-placeholder rules below. A parser may coalesce adjacent
literals.

- An optional segment contains at least one unescaped required substitution. `[1]` is an
  optional field. `[1{2}]` is a segment containing literal `1` and a substitution for parameter 2.
- Segments cannot nest or contain optional fields. `[.{1}[2]]` is invalid.
- Recognize escapes before opening a substitution or segment. Within a substitution, the index
  must be followed by its matching closing delimiter. Escapes are unavailable inside indices.
- Indices use ASCII digits with no signs, leading zeros, or surrounding whitespace. `{01}`,
  `{-1}`, `{ 0 }`, and `[01]` are invalid.
- Every opening construct must close. Unmatched unescaped delimiters, a trailing backslash, and
  unknown escapes such as `\n` are errors.
- U+0000 is forbidden in template literals, including optional segments. An unescaped `$`
  immediately followed by an ASCII digit is a legacy-placeholder syntax error. Use `{0}` for
  substitution and `\$0` for literal `$0`.

The grammar has no format specifiers, default-value expressions, named variables, property
paths, arithmetic, filters, loops, includes, macros, comments, or whitespace-control operators.
Unsupported constructs produce syntax errors.

## Configuration validity

Syntax validation checks the decoded template independently of its parameters. Configuration
validation checks the parsed template against the `N` ordered parameter positions supplied by
the consuming strategy, independently of any subject's values. `FormatRule` gets its parameters
from `TemplateParameters`. A fixed-input strategy supplies its parameter count from its contract.
`RelationshipPairRule` has two positions. `FirstKeyRelationship` supplies position 0 and
`SecondKeyRelationship` supplies position 1. A pair template must reference both positions at
least once, may repeat them in any order, and may reference only those two positions.

- Every referenced index must be in `[0, N)`, including references in optional segments that
   rendering might omit. An arbitrarily large, correctly spelled index is syntactically valid
  and fails configuration if it is out of range. Index handling must prevent integer wraparound.
- Every supplied parameter position must appear in a required substitution, optional field, or optional
  segment. Escaped placeholder text does not count. A parameter used in a suppressed segment
  still counts.
- Repeated references and out-of-order references are valid. Positions refer to the original
  parameter sequence. The renderer preserves its ordering and multiplicity. For `FormatRule`,
  the relationship's duplicate policy governs repeated property descriptor identities.
- Declared parameter kinds must be supported. A configured rule with malformed syntax, an
  out-of-range index, an unused parameter, or an unsupported declared kind is invalid even if
  no subject exercises the defective portion.

The general renderer accepts literal-only templates with zero parameters. An empty template is
also valid and renders an empty String with zero parameters. A literal-only or empty template
with listed parameters fails the coverage check. Persisted `FormatRule` instances retain the
`OneOrMore` cardinality of `TemplateParameters` and therefore require at least one parameter.

## Input states and presence

Preparation supplies exactly one state per parameter. `Present` carries one explicit, valid value
of a supported scalar kind. `Absent` means complete evidence establishes that the subject has no
explicit value for that input. An unavailable prerequisite, insufficient evidence, ambiguous
binding, or malformed value cannot supply an `Absent` state. Composition reports unevaluable
prerequisites through its ordinary outcome contract and propagates operational read failures.

Producers materialize any defaults intended as inputs before composing. Rendering uses the
explicit input states without substituting schema defaults, display labels, or other fallback
values. An ingress null or invalid value is governed by the property's value contract. The
template input model has only `Present` and `Absent`.

| Input | Present? | Rendered value |
| --- | --- | --- |
| Absent property | No | No value |
| Empty string | Yes | Empty text |
| Boolean false | Yes | `false` |
| Integer zero | Yes | `0` |
| String containing spaces | Yes | Exact spaces |

Every supplied present value must be valid and renderable, including values referenced in a
segment that another absent parameter would suppress.

## Evaluation

1. Check parameter configuration before rendering. Validate and canonically render each present
   parameter once, retaining absent states separately.
2. Check that every parameter referenced by a top-level required substitution is present.
3. Emit top-level pieces in source order. A literal or escape emits its literal text. A required
   substitution emits its value. An optional field emits its value when present. An optional
   segment emits its complete body only when every referenced parameter is present.
4. Return the resulting String, subject to the output bound.

Rendering stops at the first failing step. For example, an invalid present input takes
precedence over a missing required input. Within a step, the order of multiple errors is
unspecified.

A suppressed segment emits none of its punctuation. A repeated reference within a segment
imposes one presence requirement. A present empty string satisfies that requirement, so `[.{1}]`
emits `.` when parameter 1 is present and empty.

An index may appear in multiple forms. For `{0}[0]`, an absent parameter 0 produces a
missing-required-input error. A present parameter 0 is emitted twice. A substitution inside an
optional segment imposes a requirement on that segment. Only a top-level required substitution
imposes a requirement on the entire template.

Substitution is a single pass. Inserted delimiters and backslashes are emitted unchanged and
never interpreted as template syntax.

## Canonical scalar rendering

| Value kind | Rendering |
| --- | --- |
| String | Exact Unicode content, preserving normalization form, case, whitespace, and literal characters |
| Integer | Base-10 ASCII digits, with `-` only for negative values and no leading `+`, digit grouping, or leading zeros. Zero renders as `0`. |
| Boolean | Exactly `true` or `false` |
| Enum | Exact stored token, independent of the variant key and display name |

Integer rendering is exact throughout the MAP integer range and uses integer arithmetic.
Rendering follows these conversions independently of locale, host-language formatting defaults,
generic `Display`, or serialization and encoding conventions such as JSON, HTML, and URI encoding.
Bytes, floating-point values, arrays, objects, and other unsupported kinds produce errors.
Additional scalar kinds require an explicit rendering contract.

## Literals and escaping

Literal whitespace is preserved, including leading and trailing spaces and decoded line breaks.
To include a newline, the TDL or JSON decoder must supply an actual newline. The two-character
sequence `\n` is an unknown escape in the decoded template. Doubled brackets `[[` and `]]` have
no escape meaning. Backslash escapes for brackets distinguish a segment's closing `]` from a
following escaped literal `\]`. Braces use doubled spelling. Backslash-brace sequences are invalid.

| Decoded template | Inputs | Output |
| --- | --- | --- |
| `{{0}}` | None | `{0}` |
| `\[1\]` | None | `[1]` |
| `{{{0}}}` | `A` | `{A}` |
| `{0}\\[1]` | `A`, `B` | `A\B` |
| `{0}[.{1}]\]` | `A`, absent | `A]` |
| `{0}[.{1}]\]` | `A`, `B` | `A.B]` |
| `\$0` | None | `$0` |

## Rendering bounds and key validity

Given the same valid template and prepared inputs, rendering produces the same UTF-8 bytes on
all supported platforms. It requires no filesystem, network, clock, randomness, locale, or
mutable environment. The language has no recursive expansion or iteration over data values.

The caller supplies an output bound in UTF-8 bytes. While appending pieces, the renderer checks
output growth without integer overflow and reports a resource error if the bound would be
exceeded. Suppressed segments contribute zero output bytes. The renderer can detect oversized
expansions before allocating the full result and returns no truncated or partial output.
Templates and parameter lists remain subject to their existing storage and validation bounds.
The grammar defines no independent numeric size limits.

The renderer returns a `MapString`. The consuming key strategy checks that its completed key is
nonempty, NUL-free, and within the authoritative `MAX_CANONICAL_KEY_BYTES` limit. That limit
governs semantic keys. General String consumers supply their own rendering bounds. Whitespace
alone does not invalidate a template or its rendered String. Any additional component
restrictions come from the applicable key strategy. [Key composition and identity contract](schema-design-spec.md#96-key-composition-and-identity-contract)

Distinct inputs can produce the same String. For `{0}{1}`, `AB` followed by `C` and `A` followed
by `BC` both produce `ABC`. Optional omission can also yield the same String for distinct
input sequences. The renderer performs no reverse mapping of values. Committed and candidate
key claims remain subject to [DS-KEY-006](descriptor-semantics-rules.md#ds-key-006-key-uniqueness-across-lineages).

## Diagnostics

| Category | Example | Outcome |
| --- | --- | --- |
| Invalid template syntax | Unmatched delimiter, unsupported escape, invalid index spelling | Template construction or syntax validation failure |
| Invalid rule configuration | Out-of-range index, unused parameter, unsupported declared kind | Invalid configured rule |
| Missing required input | Proven absence for a top-level required substitution | Missing-input finding |
| Invalid input | Malformed or unsupported populated value | Input failure |
| Insufficient semantic evidence | Unresolved descriptor or incomplete scope | Unevaluable composition |
| Operational failure | Backend read failure during preparation | Operational error |
| Rendering resource failure | Output would exceed the caller's bound | Rendering failure |
| Invalid composed key | Empty result, NUL, or excessive key byte length | Key-shape failure |
| Stored-key mismatch | Expected key differs from stored key | Key-rule validation finding |
| Key collision | Another lineage claims the complete key | Separate uniqueness finding |

Syntax diagnostics identify a half-open UTF-8 byte span in the decoded template. Input
diagnostics identify the parameter index and retain caller-supplied provenance. A containing
format may also map spans to source locations in TDL or JSON. The category distinctions are
normative and can use the existing composition and error types. Diagnostic wording is independent
of the key format.

## Behavioral examples

`absent` in these examples denotes the prepared `Absent` state.

| Decoded template | Inputs in parameter order | Result |
| --- | --- | --- |
| `{0}.[1].[2]` | `A`, `B`, `C` | `A.B.C` |
| `{0}.[1].[2]` | `A`, absent, `C` | `A..C` |
| `{0}.[1].[2]` | `A`, absent, absent | `A..` |
| `{0}[.{1}][.{2}]` | `A`, absent, `C` | `A.C` |
| `{0}[.{1}][.{2}]` | `A`, absent, absent | `A` |
| `{0}[.{1}][.{2}]` | `A`, empty string, absent | `A.` |
| `{0}[.{1}]` | `A`, Boolean false | `A.false` |
| `{0}[.{1}]` | `A`, integer zero | `A.0` |
| `{0}[.{1}-{2}]` | `A`, `B`, absent | `A` |
| `{0}[.{1}-{2}]` | `A`, `B`, `C` | `A.B-C` |
| `{1}-{0}-{1}` | `A`, `B` | `B-A-B` |
| `{0}[0]` | absent | Missing required input 0 |
| `[0]` | absent | Empty String, which the key consumer rejects |
| `Singleton` | None | `Singleton` |
| Empty template | None | Empty String |
| `{0}` | String `{1}` | Literal output `{1}` |
| `{0}[.{2}]` | `A`, absent | Invalid index 2 regardless of segment omission |
| `{0}` | `A`, `B` | Unused parameter 1 |
| `{0}[.{1}-{2}]` | `A`, absent, malformed value | Invalid input prevents successful omission |
