# Incremental Work Plan: MAP TDL Authoring and Schema Generation Toolchain

## Goal

Move MAP schema authoring from Airtable-managed JSON generation to a Git-based developer workflow where MAP Type Definition Language (TDL) files are the source of truth, JSON import files are generated artifacts, and validation/generation can run locally and in CI.

The near-term objective is a reliable developer experience for defining new MAP types in TDL, generating schema JSON import files, generating Rust enum/name constants and typed HolonReference wrappers, and supporting suite tests that load those JSON files into mock or real conductors.

This work emerged because descriptor-driven implementation has become constrained by the latency of the current Airtable-centered process and by the difficulty of reasoning about a growing schema footprint. The plan is intentionally segmented so that the minimum toolchain needed to unblock Commands, Dances, Queries, and DAHN can land first, while the rest of the TDL tooling matures in parallel.

---

## Milestone segmentation

### Milestone A: TDL baseline and Airtable-parity toolchain

Goal:

Establish TDL as the Git-based source of truth and provide rough parity with the current Airtable process.

Primary outcome:

A developer can modify core schema definitions in TDL, generate JSON import files, generate Rust type/name artifacts, generate typed HolonReference/wrapper skeletons, and run suite tests without waiting on the Airtable update process.

Includes:

- Phase 0: JSON to TDL baseline decompiler
- Phase 1: TDL to JSON compiler
- Phase 2: Shared semantic model and symbol table, scoped to compiler/decompiler/codegen needs
- Phase 3a: Basic semantic validation
- Phase 6: Rust enum/name generation
- Phase 7a: Typed HolonReference and wrapper skeleton generation
- Phase 8: Local developer workflow

Recommended target:

Complete this milestone before making sizable descriptor-driven changes to Commands, Dances, Queries, and DAHN.

---

### Milestone B: Resume descriptor-driven implementation while hardening TDL

Goal:

Use the Milestone A toolchain to unblock descriptor-driven implementation, while continuing to harden schema tooling in parallel.

Primary outcome:

Commands, Dances, Queries, and DAHN work can proceed using TDL PRs as the ordinary schema-change mechanism.

Includes:

- Phase 3b: Expanded semantic validation
- Phase 4: Semantic diff
- Phase 5: CI integration
- Phase 7b: Wrapper generation refinements
- Phase 10a: Contributor documentation and migration policy

Recommended target:

Begin this milestone as soon as Milestone A is good enough to replace the Airtable critical path, even if validation and diffing are still incomplete.

---

### Milestone C: Developer experience and schema intelligence

Goal:

Make TDL authoring feel like normal language-aware development and lay foundations for future Holons Design Workbench capabilities.

Primary outcome:

Developers get IDE support, symbol-aware completions, diagnostics, navigation, hover documentation, and later schema-aware refactoring/analysis.

Includes:

- Phase 9.1: LSP skeleton and diagnostics
- Phase 9.2: VS Code integration
- Phase 9.3: Completion engine
- Phase 9.4: Navigation
- Phase 9.5: Hover and documentation
- Phase 9.6: RustRover / JetBrains integration
- Phase 9.7: Workspace intelligence
- Phase 9.8: Schema-aware refactoring
- Phase 10b: Full documentation and Airtable deprecation

Recommended target:

Run this work in parallel once Milestone A is complete and Milestone B feature work has resumed.

---

## Recommended source-of-truth model

- Source of truth: `schema-src/**/*.tdl`
- Generated artifacts:
    - JSON import files
    - Rust enum/name constants
    - typed HolonReference wrappers
    - optional wrapper skeletons
    - symbol table cache
    - semantic diff reports
- Review surface:
    - primarily TDL diffs
    - secondarily generated semantic diff
    - JSON diffs only as generated verification artifacts

---

## Proposed repository layout

    map-holons/
      schema-src/
        metaschema/
          root.tdl
          property-types.tdl
          relationship-types.tdl
          value-types.tdl
          key-rules.tdl

        core/
          holon-types.tdl
          dance-types.tdl
          query-types.tdl
          command-types.tdl
          relationships.tdl
          properties.tdl

      generated/
        json-imports/
          metaschema-root.json
          metaschema-property-types.json
          metaschema-relationship-types.json
          core-schema.json

        rust/
          core_holon_type_names.rs
          core_property_type_names.rs
          core_relationship_type_names.rs
          core_value_type_names.rs
          wrappers/

      tools/
        map-schema/

---

## Implementation language recommendation

Use Rust for the compiler, decompiler, CLI, semantic analyzer, symbol table, validator, Rust code generation, and eventual language server.

Rationale:

- MAP is already Rust-centered.
- The compiler will likely need to share domain types and validation conventions with the rest of the repo.
- Rust produces a convenient single binary for local and CI use.
- Rust is a good fit for later LSP work.
- Keeping compiler and decompiler in the same Rust crate avoids drift.

---

## Suggested crate structure

Start simple:

    tools/map-schema/
      src/
        ast.rs
        json_model.rs
        parse.rs
        format_tdl.rs
        decompile.rs
        compile.rs
        symbols.rs
        validate.rs
        diff.rs
        codegen_rust.rs
        main.rs

Later, split into crates if needed:

    crates/
      map_schema_ast/
      map_schema_parser/
      map_schema_semantics/
      map_schema_codegen/
      map_schema_cli/
      map_schema_lsp/

---

# Milestone A: TDL baseline and Airtable-parity toolchain

## Phase 0: JSON to TDL baseline decompiler

### Purpose

Create the initial TDL source files from the existing JSON import files.

This is the bridge away from Airtable. The decompiler does not need to become a perfect long-term reverse compiler before descriptor-driven implementation resumes. Its near-term purpose is to generate the initial baseline `.tdl` corpus from the current JSON files so future schema evolution can happen in Git.

### Inputs

- Existing JSON import files
- Existing TDL specification
- Existing MAP import schema
- Current schema partitioning conventions

### Outputs

- Initial `schema-src/**/*.tdl`
- Decompiler diagnostics
- Optional symbol table cache
- Round-trip comparison report

### Core commands

    map-schema decompile import-files/*.json --out schema-src/
    map-schema compile schema-src/ --out generated/json-imports/
    map-schema diff import-files/ generated/json-imports/

### Acceptance criteria

- [ ] Existing JSON import files can be parsed.
- [ ] Decompiler emits valid existing MAP TDL.
- [ ] Generated TDL can compile back to JSON.
- [ ] Round-trip JSON is semantically equivalent to the original JSON.
- [ ] Output TDL is reasonably idiomatic, not merely JSON-shaped TDL.
- [ ] Decompiler preserves descriptions and schema membership.
- [ ] Decompiler emits implicit TDL forms where the TDL already defines them.
- [ ] Baseline TDL files are suitable for Git review and future hand editing.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Medium

Use for:

- Generating Rust struct models for the JSON import format.
- Implementing the first-pass decompiler.
- Writing fixture-based tests.
- Creating semantic equivalence checks.

Escalate to GPT-5.5 with Medium reasoning for:

- Ambiguous decompilation rules.
- Decisions about canonical TDL formatting.
- Resolving edge cases involving defaults, implicit relationships, or schema partitioning.

---

## Phase 1: TDL to JSON compiler

### Purpose

Compile reviewed TDL source files into canonical MAP JSON import files.

This becomes the primary generation path after the baseline TDL files are established.

### Inputs

- `schema-src/**/*.tdl`
- Existing TDL grammar
- Existing MAP JSON import schema
- Existing MAP validation rules

### Outputs

- Generated JSON import files
- Compiler diagnostics
- Symbol table
- Semantic model

### Core commands

    map-schema compile schema-src/ --out generated/json-imports/
    map-schema check schema-src/

### Acceptance criteria

- [ ] TDL parser supports the full existing TDL.
- [ ] Compiler emits JSON import files accepted by the existing schema loader.
- [ ] Compiler correctly generates properties, relationships, value types, enum variants, holon types, and inverse relationships.
- [ ] Compiler emits deterministic JSON ordering.
- [ ] Compiler supports schema-level partitioning.
- [ ] Compiler supports cross-schema references.
- [ ] Compiler can run in CI.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Medium

Use for:

- Parser implementation.
- AST definitions.
- JSON emitter.
- Deterministic formatting.
- Test scaffolding.

Escalate to GPT-5.5 with Medium reasoning for:

- Semantic model design.
- TDL edge cases.
- Cross-schema resolution rules.
- Compiler architecture reviews.

---

## Phase 2: Shared semantic model and symbol table

### Purpose

Create the shared internal representation used by the compiler, decompiler, validator, Rust code generator, and future LSP.

For Milestone A, keep this scoped to what is required for baseline decompilation, compilation, Rust generation, wrapper generation, and basic validation. Avoid trying to design the final Workbench-grade typegraph all at once.

### Conceptual flow

    JSON import files
      -> JSON model
      -> semantic descriptor model
      -> symbol table
      -> TDL AST
      -> TDL formatter

    TDL source
      -> TDL AST
      -> semantic descriptor model
      -> symbol table
      -> JSON model
      -> JSON formatter

### Symbol table contents

- Schemas
- TypeDescriptors
- HolonTypes
- PropertyTypes
- RelationshipTypes
- ValueTypes
- Enum variants
- SourceType and TargetType links
- Extends links
- InverseOf links
- ComponentOf links
- UsesKeyRule links
- Origin metadata: file, line, column, generated source

### Acceptance criteria

- [ ] Every descriptor has a stable symbol identity.
- [ ] Every reference resolves to a symbol or produces a diagnostic.
- [ ] Symbol table supports lookup by name, kind, and schema.
- [ ] Symbol table preserves source location for TDL symbols.
- [ ] Symbol table preserves origin location for JSON-derived symbols where possible.
- [ ] Symbol table supports Rust enum/name generation.
- [ ] Symbol table supports typed HolonReference/wrapper generation.
- [ ] Symbol table can later support semantic diffing and LSP features without redesign.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Medium

Use for:

- Designing the semantic model.
- Avoiding premature overfitting to JSON.
- Establishing symbol identity rules.
- Reviewing lookup and resolution semantics.

Use GPT-5.4 Mini with Medium reasoning for:

- Implementing straightforward lookup tables.
- Serialization of the symbol table cache.
- Unit tests.

---

## Phase 3a: Basic semantic validation

### Purpose

Provide enough validation to make TDL safe for near-term descriptor-driven work and to avoid obvious authoring errors before JSON generation and suite-test import.

### Initial validation rules

- Unknown symbols
- Duplicate type names
- Duplicate relationship definitions
- Invalid source or target type
- Invalid property value type
- Invalid Extends target
- Violation of single inheritance
- Missing required descriptor properties
- Bad cardinality
- Invalid default assumptions where obvious

### Core command

    map-schema check schema-src/

### Acceptance criteria

- [ ] Diagnostics include file, line, column, severity, and message.
- [ ] Validation can fail local generation.
- [ ] Validation does not require a running conductor.
- [ ] Validation can be run independently of JSON generation.
- [ ] Validation catches common schema authoring mistakes before suite tests.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Medium

Use for:

- Implementing validation passes.
- Creating rule-specific test fixtures.
- Building diagnostic formatting.

Escalate to GPT-5.5 with Medium reasoning for:

- Non-obvious MAP type-system rules.
- Inheritance edge cases.
- Cross-schema reference policy.

---

## Phase 6: Rust enum/name generation

### Purpose

Replace Airtable-generated Rust enum/name updates with compiler-generated Rust files.

This is part of Airtable parity and should be included in Milestone A.

### Generated outputs

- `CoreHolonTypeName`
- `CorePropertyTypeName`
- `CoreRelationshipTypeName`
- `CoreValueTypeName`
- Any other name enums currently produced downstream from Airtable

### Core command

    map-schema generate-rust schema-src/ --out generated/rust/

### Acceptance criteria

- [ ] Generated enums match current naming conventions.
- [ ] Generated files are deterministic.
- [ ] Generated names are derived from the symbol table.
- [ ] Generated names compile cleanly.
- [ ] Existing code can migrate from Airtable-generated names to compiler-generated names.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Low or Medium

Use for:

- Rust code generation templates.
- Enum derivations.
- Formatting.
- Tests that assert generated Rust compiles.

Use GPT-5.5 with Medium reasoning for:

- Deciding naming conventions where legacy output is inconsistent.
- Designing compatibility migration.

---

## Phase 7a: Typed HolonReference and wrapper skeleton generation

### Purpose

Generate or assist the creation of Rust wrapper types for core schema holons.

These wrappers encapsulate property and relationship names and provide typed convenience accessors. This phase is included in Milestone A because it directly helps unblock descriptor-driven implementation of Commands, Dances, Queries, and DAHN.

### Recommended generation strategy

Separate generated and manual code.

    generated/wrappers/dance_request.generated.rs
    manual/wrappers/dance_request_ext.rs

Generated file:

    pub struct DanceRequest {
        holon: TypedHolonRef,
    }

    impl DanceRequest {
        pub fn input(&self) -> HolonResult<Option<HolonRef>> {
            // generated accessor using generated relationship name
        }
    }

Manual extension file:

    impl DanceRequest {
        pub fn domain_specific_helper(&self) -> HolonResult<...> {
            // hand-written logic
        }
    }

### Acceptance criteria

- [ ] Wrapper skeletons are generated from HolonType descriptors.
- [ ] Property accessors use generated property-name enums or constants.
- [ ] Relationship accessors use generated relationship-name enums or constants.
- [ ] Generated files are not hand-edited.
- [ ] Manual extension points are preserved.
- [ ] Regeneration does not destroy hand-written logic.
- [ ] Generated wrappers are sufficient to support near-term core schema work.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Medium

Use for:

- Designing the wrapper generation pattern.
- Avoiding awkward Rust ownership/lifetime mistakes.
- Designing typed reference strategy.
- Reviewing generated API ergonomics.

Use GPT-5.4 Mini with Medium reasoning for:

- Implementing codegen once the pattern is clear.
- Creating tests for generated wrappers.

---

## Phase 8: Local developer workflow

### Purpose

Make schema authoring feel like normal code authoring.

### Developer workflow

    1. Edit TDL.
    2. Run map-schema check.
    3. Run map-schema compile.
    4. Run map-schema generate-rust.
    5. Run suite tests.
    6. Commit TDL plus generated artifacts.
    7. Open PR.
    8. Review TDL and generated artifacts.

### Convenience command

    cargo xtask schema

or:

    map-schema all

Equivalent to:

    map-schema check schema-src/
    map-schema compile schema-src/ --out generated/json-imports/
    map-schema generate-rust schema-src/ --out generated/rust/
    cargo test schema_import_tests

### Acceptance criteria

- [ ] One command regenerates all schema artifacts.
- [ ] One command validates all schema artifacts.
- [ ] Errors are understandable to schema authors.
- [ ] The workflow no longer requires Airtable for routine type changes.
- [ ] Existing suite-test import flow continues to work.
- [ ] Commands, Dances, Queries, and DAHN descriptor work can proceed using TDL PRs.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Low

Use for:

- Command wrappers.
- Developer documentation.
- README updates.
- Common troubleshooting guide.

Use GPT-5.5 with Low reasoning for:

- Reviewing the workflow for conceptual gaps.

---

# Milestone B: Resume descriptor-driven implementation while hardening TDL

## Phase 3b: Expanded semantic validation

### Purpose

Move beyond basic validation and enforce richer MAP schema semantics before JSON is generated or imported.

### Expanded validation rules

- Missing inverse relationship where required
- Invalid inverse source/target pairing
- Missing or unnecessary schema dependency
- Use of non-extensible property or relationship type where forbidden
- Key rule mismatch
- Keyless/keyed type consistency
- Abstract/concrete type consistency
- More complete inheritance constraints
- Additional MAP-specific type-system rules as they become codified

### Core command

    map-schema check schema-src/

### Acceptance criteria

- [ ] Diagnostics include file, line, column, severity, and suggested fix where possible.
- [ ] Validation can fail CI.
- [ ] Validation does not require a running conductor.
- [ ] Validation can be run independently of JSON generation.
- [ ] Validation catches common schema authoring mistakes before suite tests.
- [ ] Expanded validation does not block descriptor-driven implementation with excessive false positives.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Medium

Use for:

- Implementing validation passes.
- Creating rule-specific test fixtures.
- Building diagnostic formatting.

Escalate to GPT-5.5 with Medium or High reasoning for:

- Non-obvious MAP type-system rules.
- Inheritance and propagation semantics.
- Key rule semantics.
- Inverse relationship policy.

---

## Phase 4: Semantic diff

### Purpose

Make PR review easier by summarizing schema changes in human-readable form.

### Core command

    map-schema diff base/schema-src head/schema-src

### Example output

    Added PropertyType:
      ISBN
        value: MapStringValueType

    Modified HolonType:
      Book
        added property: ISBN

    Added RelationshipType:
      (Book)-[PublishedBy]->(Organization)

    Generated files changed:
      generated/json-imports/core-schema.json
      generated/rust/core_property_type_names.rs

### Acceptance criteria

- [ ] Diff reports added, removed, and modified descriptors.
- [ ] Diff reports relationship source/target changes.
- [ ] Diff reports property value type changes.
- [ ] Diff reports cardinality changes.
- [ ] Diff reports generated artifact impact.
- [ ] Diff is suitable for PR comments or CI output.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Low or Medium

Use for:

- Implementing report formatting.
- Generating test fixtures.
- Producing Markdown summaries.

Use GPT-5.5 with Low or Medium reasoning for:

- Reviewing semantic diff categories.
- Deciding what information reviewers actually need.

---

## Phase 5: CI integration

### Purpose

Make schema generation and validation part of the normal GitHub PR workflow.

### CI checks

    map-schema check schema-src/
    map-schema compile schema-src/ --out generated/json-imports/
    map-schema generate-rust schema-src/ --out generated/rust/
    git diff --exit-code generated/
    cargo test schema_import_tests

### Acceptance criteria

- [ ] PR fails if TDL is invalid.
- [ ] PR fails if generated JSON is stale.
- [ ] PR fails if generated Rust enum files are stale.
- [ ] PR fails if generated wrappers are stale.
- [ ] PR fails if suite tests cannot load generated JSON.
- [ ] PR includes a semantic diff summary.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Low

Use for:

- GitHub Actions workflow.
- Shell scripts.
- CI command wiring.
- Basic troubleshooting.

Escalate to GPT-5.5 with Low reasoning only if:

- CI architecture gets entangled with repo layout or workspace constraints.

---

## Phase 7b: Wrapper generation refinements

### Purpose

Improve generated wrapper ergonomics after the initial Milestone A implementation has unblocked descriptor-driven work.

### Possible refinements

- More precise typed HolonReference variants
- Better relationship collection accessors
- Required vs optional accessor distinction
- Cardinality-aware return types
- Ordered relationship support
- Better manual extension boundaries
- Documentation comments generated from descriptors
- Test generation for wrapper behavior

### Acceptance criteria

- [ ] Wrapper APIs become easier to use in Commands, Dances, Queries, and DAHN implementation.
- [ ] Generated code remains deterministic.
- [ ] Manual logic remains protected from regeneration.
- [ ] Wrapper ergonomics improve without destabilizing descriptor-driven implementation.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Medium

Use for:

- API ergonomics review.
- Typed reference design.
- Cardinality-aware accessor strategy.

Use GPT-5.4 Mini with Medium reasoning for:

- Implementing agreed-upon templates.
- Adding tests.
- Updating generated documentation comments.

---

## Phase 10a: Contributor documentation and migration policy

### Purpose

Make the new workflow understandable enough for contributors and reviewers while the tooling is still maturing.

### Deliverables

- Short schema authoring guide
- Basic TDL examples
- Generated artifact policy
- PR review checklist
- Airtable transition note

### Suggested policy

During Milestone B:

- Routine schema changes should originate as TDL PRs.
- Airtable should be removed from the ordinary critical path.
- JSON import files should be treated as generated artifacts.
- Generated Rust enum/name files should be treated as generated artifacts.
- Generated wrappers should be treated as generated artifacts.
- Manual edits to generated files should be avoided and eventually rejected by CI.

### Acceptance criteria

- [ ] Contributors know where to make schema changes.
- [ ] Contributors know which generated files to commit.
- [ ] Reviewers know how to review schema PRs.
- [ ] Airtable is no longer required for ordinary schema evolution.
- [ ] Remaining Airtable dependencies are clearly documented.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Low or Medium

Use for:

- Writing migration documentation.
- Writing contributor-facing instructions.
- Creating PR templates.
- Creating review checklists.

Use GPT-5.4 Mini with Low reasoning for:

- Formatting docs.
- Generating examples once content is decided.

---

# Milestone C: Developer experience and schema intelligence

## Phase 9.1: LSP skeleton and diagnostics

### Purpose

Create the first working MAP TDL language server and expose existing parser/validator diagnostics through the Language Server Protocol.

### Deliverables

- LSP executable
- Document open/change handling
- Parse document
- Return syntax diagnostics
- Return basic semantic diagnostics from existing validator
- No autocomplete required yet

### Acceptance criteria

- [ ] LSP starts successfully as a standalone binary.
- [ ] LSP can parse `.tdl` documents.
- [ ] LSP reports syntax diagnostics.
- [ ] LSP reports semantic diagnostics that match CLI behavior.
- [ ] LSP reuses compiler parser and validation logic rather than duplicating them.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Medium

Use for:

- LSP architecture.
- Choosing Rust LSP libraries.
- Diagnostic protocol design.
- Ensuring CLI/LSP diagnostic parity.

Use GPT-5.4 Mini with Medium reasoning for:

- Implementing basic LSP handlers.
- Creating LSP integration tests.

---

## Phase 9.2: VS Code integration

### Purpose

Provide a thin VS Code extension that launches the MAP TDL language server.

### Deliverables

- VS Code extension manifest
- `.tdl` file association
- LSP launcher
- Basic syntax highlighting, if cheap
- Diagnostics display in editor

### Acceptance criteria

- [ ] Opening a `.tdl` file starts or connects to the language server.
- [ ] Diagnostics appear in VS Code.
- [ ] The extension contains minimal language intelligence; intelligence remains in the LSP.
- [ ] Extension setup is documented.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Low

Use for:

- VS Code extension boilerplate.
- File association configuration.
- LSP client setup.
- README instructions.

Escalate to GPT-5.5 with Low reasoning only for:

- Extension architecture decisions that affect future distribution.

---

## Phase 9.3: Completion engine

### Purpose

Add symbol-aware, context-aware autocomplete.

This is the largest early IDE feature because it requires the language server to understand cursor context and descriptor kind constraints.

### Completion examples

When completing after:

    value |

suggest only ValueTypes.

When completing after:

    target |

suggest only compatible HolonTypes.

When completing after:

    source |

suggest only compatible HolonTypes.

When completing under:

    properties
      |

suggest PropertyTypes.

When completing under:

    relationships
      |

suggest RelationshipTypes.

### Deliverables

- Cursor context detection
- Symbol lookup integration
- Descriptor-kind filtering
- Prefix matching
- Completion item labels and details
- Completion docs where available

### Acceptance criteria

- [ ] Completion is based on the symbol table, not raw text scanning.
- [ ] Completion suggestions are filtered by syntactic and semantic context.
- [ ] Completion works across loaded schema files.
- [ ] Completion handles unresolved or partially typed symbols gracefully.
- [ ] Completion item details include descriptor kind and schema.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Medium

Use for:

- Completion architecture.
- Context classification design.
- Descriptor-kind filtering strategy.

Use GPT-5.4 Mini with Medium reasoning for:

- Implementing completion handlers.
- Writing fixtures for cursor-position tests.
- Formatting completion item details.

---

## Phase 9.4: Navigation

### Purpose

Support go-to-definition, find references, and basic rename support.

### Deliverables

- Go To Definition
- Find References
- Basic symbol rename, if safe
- Source location mapping from symbol table

### Acceptance criteria

- [ ] Go To Definition works for local and cross-file symbols.
- [ ] Find References finds references across the workspace.
- [ ] Rename updates references known to the symbol table.
- [ ] Rename refuses unsafe cases rather than performing partial updates.
- [ ] Navigation behavior is consistent with symbol identity rules.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Medium

Use for:

- Symbol identity and rename safety design.
- Navigation semantics.
- Cross-file reference behavior.

Use GPT-5.4 Mini with Medium reasoning for:

- Implementing LSP handlers.
- Writing workspace fixture tests.

---

## Phase 9.5: Hover and documentation

### Purpose

Provide inline schema documentation in the editor.

### Deliverables

- Hover text for TypeDescriptors
- Descriptor kind
- Schema membership
- Description
- Extends information
- SourceType/TargetType for relationships
- ValueType for properties
- Cardinality for relationships

### Acceptance criteria

- [ ] Hover works for known symbols.
- [ ] Hover content is generated from descriptor metadata.
- [ ] Hover content is concise and readable.
- [ ] Hover works across schema files.
- [ ] Missing documentation degrades gracefully.

### Recommended ChatGPT assistance

Model: GPT-5.4 Mini  
Reasoning: Low or Medium

Use for:

- Hover formatting.
- Markdown generation for hover content.
- Tests for common descriptor kinds.

Use GPT-5.5 with Low reasoning for:

- Reviewing what information should appear in hover docs.

---

## Phase 9.6: RustRover / JetBrains integration

### Purpose

Allow RustRover and other JetBrains-based IDEs to use the same MAP TDL language server.

### Deliverables

- JetBrains LSP integration or thin Kotlin plugin
- `.tdl` file association
- LSP launcher configuration
- Diagnostics support
- Completion/navigation support if supported by the client integration

### Acceptance criteria

- [ ] RustRover can open `.tdl` files.
- [ ] RustRover can connect to the same MAP TDL language server used by VS Code.
- [ ] Diagnostics appear in RustRover.
- [ ] At least basic completion works if the JetBrains integration path supports it.
- [ ] No duplicate language intelligence is implemented in the JetBrains plugin.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Medium

Use for:

- JetBrains integration strategy.
- Deciding between native plugin and LSP bridge.
- Packaging and distribution strategy.

Use GPT-5.4 Mini with Medium reasoning for:

- Kotlin plugin boilerplate.
- File association configuration.
- LSP launcher wiring.

---

## Phase 9.7: Workspace intelligence

### Purpose

Add semantic workspace analysis that goes beyond strict compiler errors.

These are not necessarily blocking errors. They are insights that help developers reason about the schema.

### Possible analyses

- Unused PropertyType
- Unused ValueType
- Unused RelationshipType
- Missing dependency
- Unnecessary dependency
- Duplicate descriptor
- Relationship without inverse
- Circular schema dependency
- Types with unexpectedly large schema footprint
- Types with no incoming or outgoing relationships
- Potentially redundant property or relationship definitions

### Deliverables

- Workspace analysis command
- LSP diagnostics or code lenses for selected insights
- Optional report output

### Core command

    map-schema analyze schema-src/

### Acceptance criteria

- [ ] Analysis distinguishes errors from warnings and advisory insights.
- [ ] Findings are grounded in the symbol table.
- [ ] False positives are manageable.
- [ ] Output can be used locally and in CI if desired.
- [ ] Findings are useful for schema review.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Medium

Use for:

- Deciding which analyses are useful.
- Avoiding noisy or misleading diagnostics.
- Designing severity levels.

Use GPT-5.4 Mini with Medium reasoning for:

- Implementing analysis passes.
- Report formatting.
- Fixture tests.

---

## Phase 9.8: Schema-aware refactoring

### Purpose

Add higher-order IDE refactorings that understand MAP schema semantics.

### Possible refactorings

- Rename descriptor safely
- Move descriptor to another schema
- Split schema file
- Extract common PropertyType
- Extract common relationship pattern
- Generate inverse relationship
- Add missing dependency
- Normalize descriptor formatting

### Acceptance criteria

- [ ] Refactorings use the symbol table and semantic model.
- [ ] Refactorings preserve valid TDL.
- [ ] Refactorings refuse unsafe transformations.
- [ ] Refactorings are covered by before/after fixture tests.
- [ ] Refactorings are optional productivity features, not required for core schema authoring.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: High for design, Medium for implementation planning

Use for:

- Designing safe refactoring semantics.
- Identifying dangerous edge cases.
- Determining which refactorings are worth implementing.

Use GPT-5.4 Mini with Medium reasoning for:

- Implementing agreed-upon refactorings.
- Generating fixture tests.
- Wiring LSP code actions.

---

## Phase 10b: Full documentation and Airtable deprecation

### Purpose

Make the new workflow official and reduce or remove dependence on Airtable.

### Deliverables

- Full schema authoring guide
- TDL examples
- Migration guide from Airtable process
- PR review checklist
- Generated artifact policy
- Troubleshooting guide
- Stewardship rules for schema changes
- Airtable archival/deprecation plan

### Suggested policy

After migration:

- Routine schema changes should originate as TDL PRs.
- Airtable should no longer be the source of truth for MAP schema definitions.
- JSON import files should be generated artifacts.
- Generated Rust enum/name files should be generated artifacts.
- Generated wrapper files should be generated artifacts.
- Manual edits to generated files should be rejected by CI.

### Acceptance criteria

- [ ] Contributors know where to make schema changes.
- [ ] Contributors know which generated files to commit.
- [ ] Reviewers know how to review schema PRs.
- [ ] Airtable is no longer required for ordinary schema evolution.
- [ ] The old process is documented as deprecated or archival.
- [ ] Remaining coexistence cases, if any, are explicitly documented.

### Recommended ChatGPT assistance

Model: GPT-5.5  
Reasoning: Low or Medium

Use for:

- Writing migration documentation.
- Writing contributor-facing instructions.
- Creating PR templates.
- Creating review checklists.

Use GPT-5.4 Mini with Low reasoning for:

- Formatting docs.
- Generating examples once content is decided.

---

# Suggested overall model usage strategy

## Best default

Use GPT-5.4 Mini with Low or Medium reasoning for implementation-heavy tasks where the target behavior is clear.

Good examples:

- Rust structs
- parsers
- JSON emitters
- fixture tests
- CLI plumbing
- GitHub Actions
- code generation templates
- VS Code extension boilerplate

## Use larger model selectively

Use GPT-5.5 with Medium reasoning for design-heavy tasks where the hard part is conceptual correctness.

Good examples:

- semantic model design
- symbol identity rules
- cross-schema reference policy
- inverse relationship semantics
- wrapper API design
- LSP architecture
- migration strategy
- workspace intelligence design

## Use High reasoning sparingly

Reserve GPT-5.5 High reasoning for:

- subtle type-system design problems
- ambiguous round-trip equivalence issues
- inheritance and propagation edge cases
- key rule semantics
- schema-aware refactoring semantics
- architectural decisions that will be hard to reverse

---

# Proposed implementation order

## Milestone A: TDL baseline and Airtable-parity toolchain

1. Phase 0: JSON to TDL baseline decompiler
2. Phase 1: TDL to JSON compiler
3. Phase 2: Shared semantic model and symbol table, scoped to Milestone A
4. Phase 3a: Basic semantic validation
5. Phase 6: Rust enum/name generation
6. Phase 7a: Typed HolonReference and wrapper skeleton generation
7. Phase 8: Local developer workflow

## Milestone B: Resume descriptor-driven implementation while hardening TDL

8. Resume Commands, Dances, Queries, and DAHN descriptor-driven implementation using TDL
9. Phase 3b: Expanded semantic validation
10. Phase 4: Semantic diff
11. Phase 5: CI integration
12. Phase 7b: Wrapper generation refinements
13. Phase 10a: Contributor documentation and migration policy

## Milestone C: Developer experience and schema intelligence

14. Phase 9.1: LSP skeleton and diagnostics
15. Phase 9.2: VS Code integration
16. Phase 9.3: Completion engine
17. Phase 9.4: Navigation
18. Phase 9.5: Hover and documentation
19. Phase 9.6: RustRover / JetBrains integration
20. Phase 9.7: Workspace intelligence
21. Phase 9.8: Schema-aware refactoring
22. Phase 10b: Full documentation and Airtable deprecation

---

# Important sequencing notes

Phase 0 and Phase 1 should be developed close together.

The real migration confidence comes from round-tripping:

    JSON -> TDL -> JSON

The compiler and decompiler should share the same semantic model rather than becoming two independent translators.

However, the Phase 0 decompiler should be scoped as a baseline generator, not as a perfect long-term reverse compiler. Its main near-term benefit is producing the initial `.tdl` files from the existing JSON import files.

The first major unblock point is Milestone A, not the entire plan.

Once Milestone A is complete, descriptor-driven implementation work on Commands, Dances, Queries, and DAHN should resume while Milestone B and Milestone C proceed in parallel.

---

# Near-term success definition

This effort is successful when a developer can:

1. Generate baseline TDL files from the existing JSON schema import files.
2. Add or modify a MAP type in TDL.
3. Run one local command.
4. Generate valid JSON import files.
5. Generate required Rust enum/name updates.
6. Generate typed HolonReference/wrapper skeletons for core schema types.
7. Run suite tests that import the generated JSON into a mock conductor.
8. Open a PR where reviewers can inspect the TDL diff and, eventually, the semantic diff instead of reverse-engineering large JSON changes.
9. Continue descriptor-driven implementation of Commands, Dances, Queries, and DAHN without waiting on the Airtable workflow.