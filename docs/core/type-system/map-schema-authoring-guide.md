# MAP Schema Users Guide

The `map-schema` tool is the authoring and transformation surface for MAP schema files. It helps you move between canonical JSON import files and _Type Definition Language_ (TDL) source files, inspect the derived semantic model, and validate authored schema content before using it elsewhere in the MAP toolchain.

This guide explains what the tool is for, how to think about its input and output model, and how to use its common commands.

1. Background and Motivation

Self-describing, active holons and holon relationships comprise the core ontology for the MAP. This makes authoring type definitions a core development activity. Ideally, this should be woven seamlessly into the IDE experience so that authoring and using MAP type descriptors are (almost as natural) as native Rust types.

As one step towards this goal, we defined a Type Definition Language (TDL) as a more concise and readable way of expressing type definitions.

The `map-schema` tool provides the following capabilities 

- decompile canonical JSON import files into TDL
- compile TDL into canonical JSON import files
- check TDL for semantic diagnostics
- inspect derived symbols from JSON inputs

The usual authoring loop is:

1. For now (until AirTable as source of truth is retired), we are using the existing flow: 
   - Update AirTable with new / changed schema elements, 
   - generate the .json files
   - import into our repo
2. decompile existing JSON into TDL
3. run semantic checks
4. compile TDL back to JSON
5. start the app and confirm the generated JSON corpus loads successfully

---

# MAP Schema Authoring Guide

`map-schema` is the authoring tool for MAP schema work. In day-to-day use, you will normally invoke it through the root `npm` scripts rather than calling the Rust binary directly.

This guide centers the `npm` workflows that schema authors actually use, explains when decompile and compile behave differently, and closes with a small appendix for direct standalone invocation.

---

## 1. What this tool is for

`map-schema` supports four practical authoring workflows:

- decompile canonical JSON import files into TDL
- compile TDL into canonical JSON import files
- check TDL for semantic diagnostics
- inspect derived symbols from JSON inputs

The usual authoring loop is:

1. decompile existing JSON into TDL when needed
2. edit TDL
3. run semantic checks
4. compile TDL back to JSON
5. start the app and confirm the generated JSON corpus loads successfully

---

## 2. Default npm workflows

The root `package.json` provides the commands you will most often use.

## Decompile the core schema corpus

    npm run map-schema:decompile:coreschema

This reads canonical JSON from the core-schema import directory and writes TDL into `schema-src`.

## Compile the core schema corpus

    npm run map-schema:compile:coreschema

This reads TDL from `schema-src` and writes JSON imports into `generated/json-imports`.

## Check the core schema corpus

    npm run map-schema:check:coreschema

This validates the TDL corpus in `schema-src` and reports semantic diagnostics.

## Dump symbols for the core schema corpus

    npm run map-schema:symbols:coreschema

This prints the derived symbol table from the core-schema JSON corpus. It is mainly a debugging and visibility tool.

---

## 3. General npm usage

The generic scripts accept explicit input paths and, for corpus transforms, an explicit output directory.

## Decompile a directory or file set

    npm run map-schema:decompile -- <inputs...> --out-dir <output-dir>

Example:

    npm run map-schema:decompile -- tests/sweetests/import_files/*.json --out-dir generated/json-imports

## Compile a directory or file set

    npm run map-schema:compile -- <inputs...> --out-dir <output-dir>

Example:

    npm run map-schema:compile -- schema-src --out-dir generated

## Check a directory or file set

    npm run map-schema:check -- <inputs...>

Example:

    npm run map-schema:check -- schema-src

## Dump symbols for a directory or file set

    npm run map-schema:symbols -- <inputs...>

Example:

    npm run map-schema:symbols -- host/import_files/map-schema/core-schema

---

## 4. Important command-line detail

When using the npm wrapper, the output flag must be passed as an actual option token.

Correct:

    npm run map-schema:compile -- schema-src --out-dir generated

Also correct:

    npm run map-schema:compile -- schema-src --out generated

Incorrect:

    npm run map-schema:compile -- schema-src -- out-dir generated

Incorrect:

    npm run map-schema:compile -- schema-src -- outdir generated

The incorrect forms pass `out-dir` or `outdir` as plain positional arguments instead of an option, which makes the tool think you supplied extra inputs.

---

## 5. Decompile vs compile: the key authoring lesson

A practical lesson from recent usage is that decompile and compile have different dependency expectations.

## Decompile can often work on an individual JSON file

This command successfully decompiled an individual JSON import file:

    npm run map-schema:decompile -- /Users/stevemelville/dev/map-proto/map-dev/map-holons/tests/sweetests/import_files/*.json --out-dir generated/json-imports

That works because JSON to TDL decompile does not always require cross-file dependency resolution. If the individual JSON file contains enough information on its own, `map-schema` can lower it directly into TDL.

## Compile is stricter

TDL to JSON compile requires semantic references to resolve successfully. That includes references such as:

- `Extends`
- `ValueType`
- relationship endpoint types
- other referenced base descriptors

So a single TDL file may decompile fine from JSON and still fail to compile by itself if it depends on descriptors defined elsewhere.

In practice:

- decompile may succeed for one file
- compile may fail for that same file if its dependency corpus is not included

---

## 6. What to do when compile fails on a single TDL file

If compile reports unresolved references such as:

- `HolonType`
- `DeclaredRelationshipType`
- `InverseRelationshipType`
- `PropertyType`
- `MapStringValueType`

that usually means the TDL file is not self-contained. It depends on the surrounding schema corpus.

The practical fix is to compile it in a directory where its dependencies are also present.

That is exactly what worked for the recent test schema case:

- the test `.tdl` was moved into `schema-src`
- compile was then run over the full `schema-src` corpus
- compilation succeeded
- `npm start` then loaded all generated `.json` files, including the test schema, successfully

## Recommended rule of thumb

Use this mental model:

- **JSON to TDL decompile** can often be done one file at a time
- **TDL to JSON compile** should usually be treated as a corpus operation unless the file is truly self-contained

If a TDL file extends or references descriptors defined elsewhere, compile it together with the directory that contains those dependencies.

Recommended compile pattern:

    npm run map-schema:compile -- schema-src --out-dir generated

---

## 7. Where to place test schemas

If you are authoring a test schema that depends on core schema descriptors, place it where the compilation corpus can see its dependencies.

In practice, that usually means one of these approaches:

- place the dependent test TDL in `schema-src` and compile the full corpus
- provide a compile input set that includes both the test schema and the dependency corpus

For routine local authoring, the first option is simpler and less error-prone.

---

## 8. Directory and path behavior

`map-schema` no longer bakes in hidden assumptions about core-schema file locations. Instead:

- you supply explicit inputs
- you supply an explicit `--out-dir` for corpus transforms
- the npm scripts provide convenient defaults for the standard repo workflows

A few path-handling rules matter:

## Relative directory structure is preserved

For corpus transforms, file paths are preserved relative to the input root and reproduced under the output directory.

## Duplicate relative paths are rejected

If you pass multiple input roots that would collapse onto the same relative output path, the tool fails loudly instead of silently aliasing or overwriting files.

## Dependency matching is path-aware

The tool no longer relies on basename-only guessing for dependency resolution. This makes nested directory work more stable and less surprising.

---

## 9. Recommended everyday workflows

## Editing core schema TDL

Use:

    npm run map-schema:check:coreschema
    npm run map-schema:compile:coreschema

Then confirm application loading with:

    npm start

## Starting from an existing JSON file

Use decompile to get a TDL starting point:

    npm run map-schema:decompile -- <json-inputs> --out-dir <tdl-output-dir>

Then move or place the resulting TDL into the corpus directory that contains the dependencies required for compile.

## Creating or iterating on a dependent test schema

1. author or decompile the test schema into TDL
2. place it into `schema-src` if it depends on the core schema corpus
3. run:

   npm run map-schema:check -- schema-src
   npm run map-schema:compile -- schema-src --out-dir generated

4. run:

   npm start

5. confirm the generated JSON corpus loads successfully

---

## 10. Troubleshooting

## “multiple inputs require --out-dir”

Cause:
You passed what should have been an option as plain positional tokens.

Fix:
Use `--out-dir` or `--out` exactly.

Example:

    npm run map-schema:compile -- schema-src --out-dir generated

## “unresolved Extends reference ...” or similar semantic errors

Cause:
You are compiling a TDL file without the dependency corpus that defines the referenced descriptors.

Fix:
Compile the whole corpus or include the dependency directories in the compile input set.

## Decompile works but compile fails

Cause:
This is normal when the file can be lowered from JSON independently but cannot be semantically recompiled from TDL without its referenced base descriptors.

Fix:
Treat compile as a corpus operation for dependent schemas.

## Generated JSON compiles but loader behavior is still uncertain

Fix:
Run:

    npm start

If the application loads the generated `.json` corpus successfully, that is a strong end-to-end confirmation that the compiled schema set is loadable in practice.

---

## 11. Summary

For real MAP schema authoring, prefer the npm scripts.

Keep these rules in mind:

- use `npm run map-schema:*` as the default interface
- use `--out-dir` correctly for corpus transforms
- expect decompile to be more permissive on individual files
- expect compile to require dependencies to be present
- compile dependent test schemas together with the corpus they rely on
- use `npm start` as an end-to-end load confirmation after regeneration

If you remember one mental model, make it this:

**Decompile can often start from one file. Compile usually needs the whole semantic neighborhood.**

---

## Appendix A: direct standalone invocation

The npm scripts are the preferred interface, but the underlying Rust CLI can also be called directly.

## Direct decompile

    cargo run --manifest-path tools/map-schema/Cargo.toml -- decompile <inputs...> --out-dir <output-dir>

## Direct compile

    cargo run --manifest-path tools/map-schema/Cargo.toml -- compile <inputs...> --out-dir <output-dir>

## Direct check

    cargo run --manifest-path tools/map-schema/Cargo.toml -- check <inputs...>

## Direct symbols

    cargo run --manifest-path tools/map-schema/Cargo.toml -- symbols <inputs...>

## Single-document stdin/stdout mode

The standalone CLI also supports single-document stdin/stdout operation for one-file transforms.

Examples:

    cat some-schema.json | cargo run --manifest-path tools/map-schema/Cargo.toml -- decompile

    cat some-schema.tdl | cargo run --manifest-path tools/map-schema/Cargo.toml -- compile

    cat some-schema.tdl | cargo run --manifest-path tools/map-schema/Cargo.toml -- check

These modes are useful for experiments, editor tooling, and ad hoc piping, but normal repository authoring should center the npm workflows described above.