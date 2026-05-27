---
name: map-issue-grounder
description: "Generates repository-grounded GitHub Enhancement Issues for MAP implementation work from map-dev-docs roadmap, spec, and implementation-plan artifacts. Use when the user wants to ground a workplan task, track item, PR unit, wave-plan unit, roadmap item, spec item, or implementation-plan item into a map-holons enhancement issue, or when asked to refine or review an implementation issue against the current codebase."
---

# MAP Issue Grounder

Generate implementation-ready GitHub Enhancement Issues for MAP work. This skill is hosted from `map-dev-docs`, where roadmap, design-spec, and implementation-plan artifacts are authoritative; it uses the `map-holons` code repository as a read-only grounding target.

## Repository boundaries

- Treat `map-dev-docs` as the source of design intent.
- Treat `map-holons` as read-only unless the user separately asks for code changes.
- Do not copy DevDocs artifacts into `map-holons` as part of issue grounding.
- Do not invent repository structures. If `map-holons` cannot be found locally, ask the user for its path or for the relevant files.
- Prefer existing `map-holons` patterns over new abstractions.
- Prefer this skill for a specific MAP workplan unit, not for general triage or broad implementation planning.

## Required source artifacts

Before generating an issue, make sure the working context includes:

1. Overall roadmap/workplan: `docs/roadmap/desc-driven-impl-plan.md`.
2. Target workplan unit: track name or identifier plus PR/unit identifier or title.
3. Relevant design/specification artifact in `map-dev-docs`, usually under `docs/core/...`.
4. Relevant implementation-plan artifact in `map-dev-docs`, usually under `docs/core/...`.
5. Enhancement issue template from `map-holons`: `.github/ISSUE_TEMPLATE/enhancement.md`.
6. Current `map-holons` code context for affected modules, APIs, tests, and architectural boundaries.

If any required artifact is missing or ambiguous, ask for the missing path or pasted content. Do not substitute a generic issue format for the repository template.

## Workflow

### 1. Identify the target unit

Use `docs/roadmap/desc-driven-impl-plan.md` to locate the selected track and PR/unit. Extract:

- PR purpose and intended capability
- scope boundary and non-goals
- prerequisites, downstream dependents, expected deliverables, and wave context

Preserve the selected unit boundary. Do not silently expand scope.

### 2. Load track-specific DevDocs sources

Find or ask for the relevant design/spec and implementation plan in `map-dev-docs`. Use these to separate conceptual intent, constraints, invariants, implementation strategy, canonical MAP terminology, explicit non-goals, and deferred work.

Record the source document paths that informed the issue.

### 3. Load the map-holons enhancement template

Read `.github/ISSUE_TEMPLATE/enhancement.md` from `map-holons` and use its headings, field names, ordering, checkboxes, comments, and expected structure as the output format.

Remove instructional HTML comments from the final issue unless the repository convention expects them to remain.

### 4. Inspect repository reality

Inspect the read-only `map-holons` codebase for adjacent modules, structs/classes, traits/interfaces, functions, tests, fixtures, harnesses, public API/SDK/bridge surfaces, naming conventions, architectural boundaries, and current transaction, staging, versioning, validation, dance, command, query, descriptor, and SDK patterns.

Record only repository-grounded findings. Mark inferences as assumptions.

### 5. Map intent to implementation substrate

Translate the selected unit into concrete repository work: affected files/modules, data structure, descriptor, relationship, validation, runtime, SDK/API/IPC, test, migration, compatibility, and sequencing changes.

Separate required work from optional enhancements, deferred follow-ups, and out-of-scope items.

### 6. Surface questions and reconciliation notes

Identify unresolved questions as blocking, non-blocking, or follow-up. Capture DevDocs reconciliation notes for spec clarifications, implementation assumptions, divergences between design intent and code reality, and terminology drift.

Do not hide design uncertainty inside vague acceptance criteria.

### 7. Generate the Enhancement Issue

Produce a complete issue body using the `map-holons` enhancement template. The issue must be scoped to the selected track and unit, grounded in current code, explicit about source documents inspected, clear about dependencies and sequencing, and testable through concrete acceptance criteria.

Do not include implementation code unless the user explicitly asks for it.

## Quality rules

- Use the repository's enhancement template, not a generic format.
- Preserve canonical MAP terminology exactly.
- Flag possible terminology drift rather than silently normalizing it.
- Make acceptance criteria observable and testable.
- Keep scope to one coherent PR/unit unless grounding shows it should split.
- Recommend a split only when the unit changes unrelated subsystems, needs independent migrations, mixes foundational infrastructure with convenience APIs, requires unrelated test harnesses, or cannot have coherent acceptance criteria.
- When recommending a split, provide the smallest coherent issue sequence and dependencies, then still generate the best bounded issue possible for the requested unit.
