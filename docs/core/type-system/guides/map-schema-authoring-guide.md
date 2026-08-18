# MAP Schema Authoring Guide

## Purpose

This guide describes the current operational workflow for editing and checking
the MAP schema corpus with the `map-schema` tool in the `map-holons`
repository.

The authoritative schema source is:

```text
map-holons/schema-src/**/*.tdl
```

Generated JSON is a compatibility or interchange projection. It is not the
schema source of truth and should not be edited as the way to change MAP schema
definitions.

Normative language and schema behavior belong to the
[TDL specification](../tdl/tdl-spec.md),
[schema design specification](../schema-design-spec.md), and
[descriptor semantic rules](../descriptor-semantics-rules.md). This guide
explains how to use the current tooling; it does not introduce schema rules.

## Agent-assisted authoring

An agent may draft a TDL change, but it must not invent MAP schema language or
schema facts. Treat the active `schema-src` corpus as the authority for exact
keys, descriptor identities, declaration patterns, and local conventions.
Before editing, inspect the closest existing declarations and the applicable
sections of the TDL specification. The prose design specs define the intended
structure and semantic constraints; they do not provide permission to create
new syntax or substitute guessed names for corpus identities.

For every TDL change, establish and report:

1. the existing declarations used as the syntactic and naming precedent;
2. the schema and direct `depends_on` relationship affected by the change;
3. the exact authored source facts being added, changed, or omitted; and
4. the corpus check and loader/component tests run after the change.

Stop and surface a design question rather than guessing when the corpus and
the authoritative specs do not establish a descriptor identity, relationship
identity, declaration pattern, or schema dependency.

### Schema 2.0 authoring guardrails

- Edit `.tdl` source. Generated JSON is a derived compatibility projection and
  must be regenerated, never patched as the primary schema change.
- Every non-`schema` declaration has exactly one explicit `type` clause. A
  declaration form, key spelling, or local name never selects a describing
  type.
- Author `extends` only when the intended direct descriptor parent is known.
  It is optional and has one target; it is not a shorthand for a type category.
- Do not author or synthesize legacy `TypeKind`, `InstanceTypeKind`, or
  `TypeKindRule` state. Schema 2.0 classification follows the `Extends`
  lineage and explicit local `DefinesInstanceTypeKind true` anchor values.
- Do not guess or materialize effective inherited members, defaults, key
  values, endpoint compatibility, inverse occurrences, or validation results.
  TDL preserves authored facts; Holon Loading, `HolonDescriptor`, and the
  Holon Validator own those later computations.
- Use exact existing property and relationship identities. Property and
  relationship names occupy separate namespaces; a qualified relationship key
  references an existing relationship descriptor and does not redeclare its
  endpoints or behavior.
- Add a direct schema `depends_on` edge for every cross-schema authored
  reference. A transitive dependency does not replace that direct declaration.

This guardrail list is intentionally an operational summary. For declaration
syntax use the [TDL specification](../tdl/tdl-spec.md); for structural and
runtime validity use the [schema design specification](../schema-design-spec.md)
and [descriptor semantic rules](../descriptor-semantics-rules.md).

## Current tool boundary

The current `map-schema` CLI supports:

- `check`: parse a TDL input corpus and report source-level diagnostics;
- `compile`: convert TDL into loader-compatible JSON files;
- `decompile`: convert JSON import files into TDL; and
- `symbols`: inspect source-tooling symbols derived from JSON inputs.

Source conversion does not bind authored holons to their runtime descriptors,
materialize descriptor-defined defaults, or perform descriptor-driven holon
validation. Those operations belong to the holon-loading flow described by the
[Layered Descriptor Architecture](../../descriptors/layered-desc-arch.md).

The target loader architecture allows both TDL and MAP JSON parsers to produce
the loader's holonic reference representation directly. The current
`map-schema compile` command still emits JSON and should be understood as the
implemented conversion surface, not as a requirement that all TDL loading
must pass through JSON.

## Run from the repository root

Run the following commands from the `map-holons` checkout:

```bash
npm run map-schema -- help
npm run map-schema:check:coreschema
```

The first command displays the CLI's current options. The second parses and
checks the complete `schema-src` corpus without writing generated files.

## Everyday authoring workflow

1. Edit the relevant `.tdl` files under `schema-src/`.
2. Include any new file in the same corpus and declare its schema dependencies
   as required by the TDL specification.
3. Check the complete corpus:

   ```bash
   npm run map-schema:check:coreschema
   ```

4. Review every diagnostic. Do not treat generated output as evidence that an
   unresolved or invalid declaration is acceptable.
5. When a consumer still requires JSON imports, regenerate the compatibility
   projection:

   ```bash
   npm run map-schema:compile:coreschema
   ```

6. Run the loader and component tests affected by the schema change.

The compile script currently writes generated imports beneath
`generated/json-imports/`. Those files are derived from TDL.

## Corpus-aware checking and conversion

TDL files commonly reference descriptors declared in other files. Check the
complete dependency corpus so that every authored input is exercised together:

```bash
npm run map-schema -- check schema-src
npm run map-schema -- compile schema-src --out-dir generated/json-imports
```

## Package verification order

Schema packages are loaded explicitly and each package load commits in its own
transaction. The committed verification sequences are:

- Core: `Core`
- Dance: `Core -> Dance`
- Commands: `Core -> Dance -> Commands`
- Query: `Core -> Query`
- QueryDance: `Core -> Dance -> Query -> QueryDance`
- Validation: `Core -> Validation`
- Test: `Core -> Test`

`load_with` entries are relative to the generated artifact that owns them. For
example, `generated/json-imports/query-dance/schema.json` refers to
`../core/root.json`, `../dance/schema.json`, and `../query/schema.json`.
They describe package metadata; runtime package loading remains explicit and
transaction-scoped.

A standalone file is useful only when it includes the declarations needed to
exercise the intended source shape. TDL lowering preserves authored reference
keys in `LoaderRefRep`; guest-side Holon Loading resolves those keys against
the current load and saved holons. A corpus check is therefore not evidence
that guest resolution, descriptor conformance, or validated commit will
succeed.

When testing a schema outside `schema-src`, pass that schema together with its
dependency files or a directory containing the required corpus. A test file
does not become authoritative merely because it is checked alongside the Core
Schema.

## Using decompile

Decompile is useful for migrating, inspecting, or comparing existing JSON
imports:

```bash
npm run map-schema -- decompile <json-file-or-directory> --out-dir <tdl-output-directory>
```

Treat decompiled TDL as candidate authored source. Review its schema identity,
qualified references, dependencies, and formatting before incorporating it
into `schema-src`. Do not overwrite authoritative TDL merely because a JSON
projection differs; first determine which artifact reflects the accepted
schema design.

The convenience command below decompiles the legacy Core Schema JSON corpus:

```bash
npm run map-schema:decompile:coreschema
```

It is a migration and comparison operation, not the normal schema-authoring
direction.

## Diagnostics and verification

`map-schema check` verifies source syntax and source-to-`LoaderRefRep`
lowering diagnostics implemented by the current authoring tool. It does not
by itself prove:

- descriptor-default materialization;
- descriptor-kernel conformance;
- loader reference resolution in the guest;
- transaction commit behavior; or
- persistence and PVL behavior.

Choose additional verification according to the changed schema surface. The
[Schema Ripple Design Spec](../schema-ripple-design-spec.md) describes the
broader impact-analysis responsibility.

## Troubleshooting

**A single TDL file reports unresolved references**

Check or compile it with the files that define its dependencies.

**Multiple inputs require `--out-dir`**

Corpus conversion writes one output per input. Supply an explicit output
directory. Single-document stdin/stdout mode is intended only for one document.

**Compile succeeds but loader behavior fails**

Compilation proves source conversion, not completion, runtime descriptor
validation, or commit. Inspect the loader diagnostics and test the resulting
holonic representation through the appropriate loader path.

**Generated JSON differs from checked-in or historical JSON**

Treat TDL and the accepted schema specs as authoritative. Determine whether the
difference is a deliberate projection change, a compiler defect, or stale
derived output; do not resolve it by editing generated JSON directly.
