# Result-dependency audit

Source `a3a280d1`; inspected the shared production/report-only assessment path and transitive
configuration/dispatch consumers. No active evaluator consumes another candidate's installed
ValidationState or overall validation report. The following acceptance channels belong to the
scheduler, not the check contract. The current implementation plan's Source today entries remain
accurate; no reviewed decision amendment is proposed by this audit.

| Channel / source | Meaning today | Classification | Step A/C disposition |
| --- | --- | --- | --- |
| `PackageState::{Constructing,Constructed}` | Package construction progress | Lifecycle, not semantic acceptance | Remove readiness enum; retain explicit missing-preparation errors |
| `PackageState::{Validated,Blocked}` / `DescriptorPackages::finish` | Computed from readiness invalid set and contract Result | Acceptance | Remove finish and acceptance gate |
| `assess_candidate`: ordinary instance requires Validated package | Whole package acceptance gates all conformance | Acceptance | Replace with scoped usable-fact guards |
| `ConstructedAssessment::assess::invalid` | Mixes malformed lineage, any contract product finding, declaration finding, Schema cycle, any subject product finding | Mixed facts promoted to acceptance | Preserve individual defects/diagnosis; remove promotion to global invalidity |
| `route_definition_findings` → invalid | Every routed declaration finding invalidates a definition | Acceptance routing side effect | Preserve ordered candidate fan-out and carriers; remove invalid-set mutation |
| `ReadinessPropagation::observe` | Maps any collector finding to a dependency identity; aliases of immutable saved definitions are excluded appropriately | Acceptance | Remove; retain exact identity and independent outcome routing |
| `invalidate`, reverse map, `blocking_dependency` | Transitive invalidity over all nine edges | Acceptance | Remove reverse propagation and dependency gate |
| Post-hoc peer loop / `diagnosed` | Adds blocker to previously assessed peer if later peer fails | Acceptance | Remove; completed usable peer products remain consumable |
| `commitment_order`, `dependency_groups` | Broad discovery plus SCC schedule for provisional peers | Scheduling based on acceptance | Remove. `rg dependency_groups` shows production caller only commitment_order; module tests do not justify keeping helper |
| `SchemaRuleProducts::has_findings` | DependsOn cycle evidence | Semantic fact | Keep DS-SCHEMA-001 finding, remove invalidity propagation to member |
| `DescriptorRuleProducts::{has_findings, diagnostics}` | Structural, kind, contract and vocabulary facts, including usable repetition/redeclaration | Mixed usability and semantic defects | Preserve diagnostics, classify by condition; do not use has_findings as blanket blocker |
| `CheckedConstraint.valid` | Concrete type resolution, parameter membership, and family configuration validity, cached per exact attachment | Configuration fact, **not another candidate's overall acceptance** | Keep scoped configuration checks/evidence; do not propagate to sibling attachments or all subject checks |
| `assess_contributions`: `!checked.valid` → dependency finding | An attachment cannot supply a valid configured obligation; also checks applicability independently | Scoped attachment declaration dependency | Preserve explanatory finding and inherited-obligation check. This is already the constraint-attachment/configuration boundary, not a new overall check-result prerequisite |
| `assess_constraint`, `assess_descriptor`, `assess_contributions` boolean results | Summaries of declaration/configuration facts | Scoped result | Commit callers discard these booleans (`?;`); collector and products retain findings. No caller tests a configured holon's whole validation outcome |
| `ConstraintContributions::missing_inherited`, constraint_type Option | Missing inherited obligations and uninterpretable concrete type | Usability/evidence | Keep complete provenance; missing type blocks only affected obligation |
| `BindingRoleMemo` Result<bool>, compatibility bool | Exact family/declaring role membership; required read failure retained | Interpretation/configuration | Keep prepared role facts; Step C removes fallback lineage walk, not role checks |
| `prepare_bindings` filtering / registered implementation | Key, level, family, declaring role, native kind compatibility | Dispatch fact | Keep fail closed per binding; unknown key must not trigger family reads |
| `RuleOutcome::Continue` and product `emit_prerequisites` | Handler dispatch and explanation when bound handlers absent | Local execution/explanation | Preserve; no external acceptance prerequisite |
| Effective schema/contract Result, cached name-index errors | Product availability or diagnosed construction/read errors | Preparation/usability | Keep runtime error contract, distinguish diagnosed authored defects from operational errors |
| Outcome `PreparedAssessment::from_scope` / `install_outcomes` | Completed candidate-specific findings determine installed state | Final acceptance | Keep atomic installation; report-only consumes report without mutation |

`CheckedConstraint.valid` merits particular care: `check_membership` rejects undeclared parameters
and `check_family` interprets bounds, inclusivity and presence-only uniqueness. It does not run the
constraint holon's ordinary conformance checks or consume their findings. The dependency finding
is generated directly from these scoped configuration facts. Calling this a whole-candidate result
would recreate the acceptance policy being removed. If Step A uncovers a further dependency beyond
these inputs, add a reviewed guard row before implementing it; this audit is not authorization for
new blockers.

Semantic Extends and Schema DependsOn cycles remain independently checked. Removing SCC scheduling
does not remove those checks. Candidate names, exact definition identities and source aliases must
remain distinct after deleting scheduler-owned maps.
