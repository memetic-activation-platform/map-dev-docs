# MAP Schema Authoring Guide

## Purpose

This guide describes the current operational workflow for editing and checking
the MAP schema corpus with the `map-schema` tool in the `map-holons`
repository.

The authoritative schema source is:

```text
map-holons/schema-src/*.tdl
```

Generated JSON is a compatibility or interchange projection. It is not the
schema source of truth and should not be edited as the way to change MAP schema
definitions.

Normative language and schema behavior belong to the
[TDL specification](../tdl/tdl-spec.md),
[schema design specification](../schema-design-spec.md), and
[descriptor semantic rules](../descriptor-semantics-rules.md). This guide
explains how to use the current tooling; it does not introduce schema rules.

## Current tool boundary

The current `map-schema` CLI supports:

- `check`: parse and semantically check a TDL input corpus;
- `compile`: convert TDL into loader-compatible JSON files;
- `decompile`: convert JSON import files into TDL; and
- `symbols`: inspect the semantic symbols derived from JSON inputs.

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

TDL files commonly reference descriptors declared in other files. Pass the
complete dependency corpus whenever binding those references requires it:

```bash
npm run map-schema -- check schema-src
npm run map-schema -- compile schema-src --out-dir generated/json-imports
```

A standalone file is checkable or compilable only when it contains, or is
provided alongside, every declaration needed to resolve its references.
Unresolved `Extends`, `DescribedBy`, property, relationship, value-type, or key
rule identities usually indicate an incomplete input corpus rather than a
syntax error in the referencing file.

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

`map-schema check` verifies the syntax and semantic references implemented by
the current authoring tool. It does not by itself prove:

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
