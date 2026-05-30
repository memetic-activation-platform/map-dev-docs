---
name: map-issue-grounder
description: "Generates repository-grounded GitHub Enhancement Issues for MAP implementation work from map-dev-docs roadmap, spec, and implementation-plan artifacts. Use when the user wants to ground a workplan task, track item, PR unit, wave-plan unit, roadmap item, spec item, or implementation-plan item into a map-holons enhancement issue, or when asked to refine or review an implementation issue against the current codebase."
---

# MAP Issue Grounder

Generate implementation-ready GitHub Enhancement Issues for MAP work. This skill is hosted from `map-dev-docs`, where roadmap, design-spec, and implementation-plan artifacts are authoritative; it uses the `map-holons` code repository as a read-only grounding target. The intent is for the enhancement description to specify what is needed to bring the current code base into alignment with the subset of the design specification that is in scope for this issue per the component implementation plan.

## Repository boundaries

- Treat `map-dev-docs` as the source of design intent.
- Treat `map-holons` as read-only unless the user separately asks for code changes.
- Do not copy DevDocs artifacts into `map-holons` as part of issue grounding.
- Do not invent repository structures. If `map-holons` cannot be found locally, ask the user for its path or for the relevant files.
- Prefer existing `map-holons` patterns over new abstractions.
- Prefer this skill for a specific MAP workplan unit, not for general triage or broad implementation planning.

## Required source artifacts

Before generating an issue, make sure the working context includes:

1. Target workplan unit: track-name or identifier plus PR/unit identifier or title. For example, "Dance PR3"
3. Relevant design/specification artifact in `map-dev-docs`, usually under `docs/core/track-name/`.
4. Relevant implementation-plan artifact in `map-dev-docs`, usually under `docs/core/track-name/...`.
5. Enhancement issue template from `map-holons`: `.github/ISSUE_TEMPLATE/enhancement.md`.
6. Current `map-holons` code context for affected modules, APIs, tests, and architectural boundaries.

If any required artifact is missing or ambiguous, ask for the missing path or pasted content. Do not substitute a generic issue format for the repository template.

## Workflow

### 1. Load track-specific DevDocs sources

Find or ask for the relevant design/spec and implementation plan in `map-dev-docs`. Use these to separate conceptual intent, constraints, invariants, implementation strategy, canonical MAP terminology, explicit non-goals, and deferred work.

Record the source document paths that informed the issue.

### 2. Load the map-holons enhancement template

Read `.github/ISSUE_TEMPLATE/enhancement.md` from `map-holons` and use its headings, field names, ordering, checkboxes, comments, and expected structure as the output format.

Remove instructional HTML comments from the final issue unless the repository convention expects them to remain.

### 3. Initial Enhancement Definition

Generate a first draft of the issue that scopes the enhancement to the subset of the design specification that is in scope for this issue per the component implementation plan, completing all sections of the issue template.

### 4. Assess the Implementation Gap

Using the defined enhancement as the scope, assess the existing code base (including type definitions, imported schema definitions, implementation logic and comments, validation, runtime, SDK/API/IPC, migration, compatibility, unit and integration tests) to determine the degree to which it already aligns with the intended effects of the issue and capture the gaps where it falls short.

### 5. Update the Enhancement Issue

Update the enhancement issue to reflect the proposed changes needed to bring the code into alignment with the spec. 

### 6. Surface questions and reconciliation notes

Identify unresolved questions as blocking, non-blocking, or follow-up. Capture DevDocs reconciliation notes for spec clarifications, implementation assumptions, divergences between design intent and code reality, and terminology drift.

Do not hide design uncertainty inside vague acceptance criteria.

### 7. Generate the Enhancement Issue

Use /map-issue-grounder to produce a complete issue body using the `map-holons` enhancement template. The issue must be scoped to the selected track and unit, grounded in current code, explicit about source documents inspected, clear about dependencies and sequencing, and testable through concrete acceptance criteria.

Do not include implementation code unless the user explicitly asks for it.

## Quality rules

- Use the repository's enhancement template, not a generic format.
- Preserve canonical MAP terminology exactly.
- Flag possible terminology drift rather than silently normalizing it.
- Make acceptance criteria observable and testable.
- Keep scope to one coherent PR/unit unless grounding shows it should split.
- Recommend a split only when the unit changes unrelated subsystems, needs independent migrations, mixes foundational infrastructure with convenience APIs, requires unrelated test harnesses, or cannot have coherent acceptance criteria.
- When recommending a split, provide the smallest coherent issue sequence and dependencies, then still generate the best bounded issue possible for the requested unit.
