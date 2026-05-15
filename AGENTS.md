# AGENTS.md

## Project purpose

This repository contains Agent Skills that follow the Agent Skills standard. Each skill is a self-contained directory with its own `SKILL.md`, optional agent metadata, and optional supporting resources.

## Repository layout

- `.agents/skills/<skill-name>/` — local skills intended for Codex discovery.
- `.agents/skills/<skill-name>/SKILL.md` — required skill entrypoint.
- `.agents/skills/<skill-name>/agents/openai.yaml` — OpenAI-specific metadata.
- `.agents/skills/<skill-name>/references/` — optional supporting documentation.
- `.agents/skills/<skill-name>/scripts/` — optional executable helpers.
- `.agents/skills/<skill-name>/assets/` — optional templates, examples, or other static files.

## Documentation editing guidance

- Follow `CONTRIBUTING.md` as the source of truth for documentation governance.
- Design specs describe the authoritative intended design: concepts, invariants, relationships, naming, runtime contracts, and design boundaries.
- Keep issue-specific guidance out of design specs. PR names, implementation sequencing, test checklists, acceptance criteria, and "this issue should not..." guidance belong in GitHub Issues or implementation plans, not design specs.
- GitHub Issues describe the delta needed to bring implementation into conformance with the design spec.

## Skill authoring rules

- Use lowercase, kebab-case skill directory names.
- Every skill must include `SKILL.md`.
- Keep `SKILL.md` concise and operational.
- Put detailed background material in `references/`.
- Put deterministic or fragile repeatable logic in `scripts/`.
- Put reusable templates and static files in `assets/`.
- Do not include generated build artifacts, dependency folders, secrets, or large binary files in skills.
- Prefer examples that show exact expected inputs and outputs.

## `SKILL.md` requirements

Each `SKILL.md` must start with YAML frontmatter:

---
name: example-skill
description: concise description of what the skill does and when to use it.
---

Rules:

- `name` must match the skill directory name.
- `name` must be lowercase kebab-case.
- `description` must explain when the skill should be used.
- The body should describe the workflow, constraints, and any resources to consult.

## Agent metadata

If present, `agents/openai.yaml` should contain OpenAI-specific UI metadata, for example:

interface:
display_name: Example Skill
short_description: Helps with a repeatable task.

## Validation checklist

Before considering a skill complete:

- Confirm the skill has `SKILL.md`.
- Confirm frontmatter includes only `name` and `description`.
- Confirm the skill name is lowercase kebab-case.
- Confirm the description is specific enough to trigger the skill appropriately.
- Remove unused placeholder files.
- Run or inspect any scripts added under `scripts/`.
- Ensure no secrets, credentials, private keys, or large generated files are committed.

## Coding conventions

- Keep scripts small, readable, and deterministic.
- Prefer Python or shell scripts only when procedural reliability is needed.
- Include clear usage comments at the top of scripts.
- Fail loudly with actionable error messages.

## Git conventions

- Keep commits focused.
- Do not mix unrelated skill changes in one commit.
- When modifying a skill, update its supporting files and `SKILL.md` together if needed.
- Do not rewrite history unless explicitly asked.

## What not to do

- Do not place multiple unrelated skills in one skill directory.
- Do not put OpenAI metadata at the repository root.
- Do not duplicate long reference material inside `SKILL.md`.
- Do not assume a skill is complete if it has not been checked against the validation checklist.
