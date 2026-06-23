---
name: estimate-dev-points
description: Estimate MAP development effort using the lightweight Dev Points rubric for workplan tasks, especially PR chunks. Use when assigning, reviewing, recalibrating, or explaining Dev Points for planned chunks, defined GitHub issues, merged PRs, delivered actuals, tracking sheets, velocity forecasting, issue-grounding workflows, or GitHub issue/PR artifact lookup during estimation.
---

# Estimate Dev Points

This skill uses the following 'dev points system' to estimate upcoming work and assess actual delivery effort for delivered work.

- `1` = tightly bounded
- `2` = small
- `3` = medium
- `5` = large
- `8` = unusually uncertain or cross-cutting
- `too big` = the chunk is too large to estimate and should be decomposed into smaller implementation units

## Source of Truth

When working inside `map-dev-docs`, prefer the live repository sources over memory.

The MAP design is decomposed into "concept areas". Concept areas usually have a map-dev-docs spec directory whose contents, collectively, specify the design for that concept area. Each concept area should also have an implementation plan that defines PR chunks. Look for that implementation plan in the concept area directory first; if it is missing, search `docs/roadmap/`, `archive/`, and the rest of `docs/`, then name the source used.

The current concept areas and their associated map-dev-docs directory are as follows:

Descriptors -- docs/core/descriptors
Validation -- docs/core/validation
Query -- docs/core/map-queries
Dance -- docs/core/dances
DAHN -- docs/core/hx
Command -- docs/core/commands-and-runtime
TS SDK -- docs/core/ts-sdk

Dev points are assigned (only) at the PR chunk level. Wave estimates are simple roll-ups of the PR-chunk estimates assigned to that wave. No "wave-level" estimating is required.

Each PR chunk goes through 3 lifecycle phases:

1. Planned -- when the chunk is defined in an impl-plan that references a documented design
2. Defined -- when the GitHub issue has been defined for that chunk
3. Done -- when the chunk is delivered and its PR merged

1. Estimates of dev points for a "Planned" PR chunk are based on its impl-plan definition and design spec
2. Estimates of dev points for a "Defined" PR chunk also consider its GitHub Issue definition
3. Delivered actuals for a "Done" PR chunk also consider the PR description, changed files, and delivered code shape

Thus, to generate estimates this skill needs to use the

- concept area's design specs in map-dev-docs
- the concept area's implementation plan
- the GitHub Issue definition (required for Defined chunks)
- the GitHub Pull Request's description and changed files record (required for Done chunks)

As PRs are merged, I am tracking delivered points and completion dates. This allows me to calculate actual delivery velocity and, when coupled with estimated work remaining, to predict delivery dates for a work plan. This method relies on a consistent approach to estimating work and evaluating completed work.

For delivered work, distinguish the planned or defined estimate from the delivered actual. Do not overwrite historical tracker values unless the user explicitly asks to update them. If a completed chunk needs follow-on work, estimate that follow-on work as a separate PR chunk.

## GitHub Artifact Handling

For Defined or Done chunks, try to locate the relevant GitHub artifact from the user's prompt, local files, tracker references, issue/PR numbers, URLs, or available GitHub tooling.

If the required GitHub Issue or Pull Request file cannot be located, stop and ask the user for the missing issue or PR number, URL, local file path, or pasted content before estimating.

Do not estimate a Defined chunk without the GitHub Issue definition unless the user explicitly asks for a provisional estimate from the implementation plan only.

Do not assess a Done chunk's delivered actual without the Pull Request description and changed-files record unless the user explicitly asks for a provisional assessment from partial evidence.

## Workflow

1. Identify the unit being estimated: PR chunk within a concept area
2. Load the relevant MAP source artifacts before estimating:
   - implementation plan or roadmap section that defines the unit
   - design/spec artifact that supplies the intended behavior
   - GitHub Issue definition, required for Defined and Done chunks
   - GitHub Pull Request description and changed-files record, required for Done chunks
   - code context only when estimating implementation difficulty against current reality
3. Separate planned estimates, defined estimates, delivered actuals, and follow-on work.
4. Score the smallest coherent deliverable. If a unit combines unrelated subsystems, migrations, or test harnesses, mark it `too big` and recommend a decomposition.
5. Assign one score from the scale, or `too big`, and include a short rationale.
6. Record assumptions, dependencies, and likely re-estimation triggers.

## Scoring Heuristics

Use `1` when the change is tightly scoped, follows an obvious existing pattern, has little design uncertainty, and has a small test surface.

Use `2` when the work is small but requires touching more than one file, adapting an existing pattern, or adding focused tests.

Use `3` when the work has a meaningful implementation path but involves several modules, a nontrivial contract boundary, or enough tests to validate behavior across a small workflow.

Use `5` when the work is large, spans a real subsystem boundary, requires migration or compatibility judgment, or needs coordinated updates across implementation, docs, and tests.

Use `8` when the work is unusually uncertain or cross-cutting: hidden coupling is likely, sequencing is not stable, multiple tracks depend on the outcome, or the unit should probably be split but cannot yet be split safely.

Use `too big` when the requested unit is not a coherent PR chunk and should be decomposed before it can be estimated responsibly.

## Output Shape

For a single unit, use:

```markdown
Estimate: 3 Dev Points

Rationale: ...

Assumptions:
- ...

Re-estimate if:
- ...
```

For delivered work, use `Delivered Actual` instead of `Estimate` when the user asks to assess completed effort.

For several units, use a compact table with columns for unit, lifecycle phase, estimate or delivered actual, rationale, and re-estimation trigger.
