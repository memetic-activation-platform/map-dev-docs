# Baseline consumer and read inventory

Source: map-holons `a3a280d1b59745038b63e9eb84f47b27b2193ff9` (production behavior
unchanged from semantic baseline `3d053ba8`). Paths below are relative to
`shared_crates/holons_validation/src/` unless prefixed `holons_core`. Both public assessment
entrypoints use `construct_assessment_with_observer` → `ConstructedAssessment::assess`;
only validation installs outcomes. This is an inventory of today's implementation, not new policy.

A relationship input includes its requested-empty membership. Retaining a target means retaining
content for ordinary bound reads, not copying runtime references into a wire product. Every exact
reference stays exact; shared ancestry never substitutes a staged successor. The definition product
index and candidate outcome routing are separate.

| Consuming operation / source | Exact source and memberships, including empty | Required retained target content / evidence | Today's product, derivation, and further traversal |
| --- | --- | --- | --- |
| Staging invariant (`commit_assessment::ensure_staged_ancestry_invariant`) | Each update candidate's local `Predecessor` | Saved source identity; touched-name state | Staged-memory read only; no schema traversal |
| Structural preparation (`construct_assessment_with_observer`) | Exact candidate definition `DescribedBy`; subject and unique governor `Extends` | Lineage keys, direct parent occurrences, cycle/multiple-parent defects | `ExtendsLineageDiagnosis::assess` per definition; governor may be diagnosed again elsewhere |
| Kind classification (`descriptor_rules::prepare_kind`, core `kind_semantics`) | Diagnosed subject/governing lineages; selected kind anchor's direct `DescribedBy` | Keys, `DefinesInstanceTypeKind`, `IsAbstractType`; anchor/describer role identity | Supplied diagnosis plus bound fields; bootstrap role primitives, no independent anchor lookup |
| Ownership/workset (`schema_view::prepare`, core `schema_ownership`) | Candidate `ComponentOf`/`RuleOf`; each encountered owner's `DescribedBy` and describing `Extends` | Exact owner identity and Schema role; ownership defect attribution | Bounded owners and staged members only; no saved `Components`/`Rules` scan |
| Package discovery (`descriptor_package::construct_with_observer`) | Each reached definition: `DescribedBy`, `Extends`, `InstanceProperties`, `InstanceRelationships`, `ValueType`, `Constraints`, `ValidationBindings`, `ComponentOf`, `RuleOf` | Saved source content lease; every target occurrence | Breadth-first exact identity × role walk. Relationship members additionally request `SourceType`/`TargetType`; constraint types `ApplicableToDescriptorTypes`; Schema role `DependsOn`. Endpoint/applicability targets do not recurse from those edges; all other edges enqueue targets |
| Effective product preparation (same function; core `ComputedEffectiveSchema`) | Every reached definition's lineage and shared kernel `collections()` inventory | Complete lossless occurrences: member, declaring definition, source collection, local position | Snapshot lookup only when affected-Schema workset empty; otherwise fresh `resolve`. Registry lookup scans transported snapshot today; no new assessment registry index |
| Complete-payload collection inventory (core `effective_holon_descriptor::collections`) | Lineage `InstanceProperties`, `InstanceRelationships`, `AffordsDance`, `AffordsCommand`, `ValidationBindings`, `Constraints`, `InstanceKeyRule` | Complete occurrence/provenance sets even for fields unused by validator | One shared kernel inventory, not the package nine-edge list; first four feed contract/vocabulary, last three additional semantic products |
| NameIndexes (core `effective_schema::name_index`, `effective_relationships::navigable_occurrences_in_lineage`) | Properties/Dances/Commands from completed collections; Relationships additionally lineage `SourceOf`, discovered member `SourceType`, member classification `Extends` | All member `TypeName` values and category keys, SourceType identity; unnamed and repeated entries retained | All reached definitions get first three indexes; HolonType lineage gets Relationships. Navigation is computed here, including inverse discovery. See exact miss inventory below |
| Graph-only overlap (`graph_only_deltas::classify_graph_only_delta_overlaps`) | Exact governor effective relationship lookup; staged delta collections; added target lineage/identity/key | Relationship target binding, target keys, source candidate IDs, bounded added occurrences | Prepared schema plus bound target-binding/identity/key interpretation; no saved subject relationship populations. Early non-overlap paths do not prove overlap branch coverage |
| Binding roles (`subject_assessment::BindingRoleMemo::prepare`) | Prepared effective bindings; registered rule's `DescribedBy`; family and declaring definition `Extends` | Required rule key; family/declaring role keys | Uses diagnosed governing lineage when available; `extends_role` fallback otherwise. Unsupported keys skip family preparation; reached required role errors remain operational |
| Universal minimum (`commit_assessment::prepare_universal_contracts`) | Exact governing meta-type lineage and effective member contributions | Universal member identities, names and contribution evidence | `UniversalDescriptorContract::from_meta_type` independently derives; memoized per exact meta-type; does not consume package contributions yet |
| Supporting-contract checks (`ConstructedAssessment::assess`) | Candidate descriptor and unique governor lineage | Prepared effective member and vocabulary indexes; local requiredness, member category, endpoints, value selection | Re-diagnoses lineage; `prepare_effective_schema` consumes projection, with bound member reads/derivations. Saved governor defects produce one aggregate finding, currently also invalidate consumers |
| Contract member usability (`descriptor_rules::prepare_effective_schema`, core `descriptor_rules` helpers) | Property/relationship member `Extends`; effective `ValueType`; relationship effective `SourceType`/`TargetType` | Member names/categories, concrete ValueType identity, endpoint role facts; repeated/redeclared/name conflict evidence | Category and endpoint checks are fact checks, not full member subject validation; failures currently enter broad invalid set |
| Constraint discovery (`constraint_declarations::assess_descriptor`) | Valid descriptor lineage `Constraints`, including inherited parent obligations | All attachment identities and declaring provenance; missing inherited occurrences | Calls `ConstraintContributions::resolve` during assessment despite package product availability. Discovery independent of bindings |
| Configured declarations (`assess_configured_rule`, `check_constraint`) | Rule/attachment `DescribedBy`; concrete type `Extends`; `ApplicableToDescriptorTypes`; inherited `InstanceProperties` | Concrete type `IsAbstractType`; parameter names; actual configuration Minimum/Maximum/inclusivity fields; complete property set | `extends_role` and structural diagnosis during assessment; parameter membership and family checks; memo per exact configured definition within declaration workset |
| Schema cycle (`schema_rules::dependency_cycles`) | Exact affected Schema `DependsOn` transitive closure | Exact dependency IDs and cycle witness | Iterative DFS during assessment; no member discovery. Binding preparation for unstaged Schema also reads its `DescribedBy` |
| Subject declaration gate (`subject_assessment::assess_holon`) | Every populated staged relationship, including unknown names | Stable sorted relationship names; target occurrence identity | Calls `schema_rules::authored_targets`; production subjects are always staged. Its Smart branch independently resolves contract and prepares declared collections but is unreachable here |
| Holon/property conformance (`assess_holon`, `assess_property`) | Prepared governor properties/relationships, property effective bindings/constraints | All property names; subject property map; rule key/family, attachment concrete type | Today names deduplicated to first property before assessment. Complete matches still exist in shared product. Member ambiguity currently blocks through readiness |
| Requiredness (core `PropertyDescriptor::is_required`) | Property lineage, `DescribedBy`, governing property membership/default | Inherited `IsValueRequired`, legacy `IsRequired`; governing `IsValueRequired` member `DefaultValue` | Assessment-time inherited-field/default interpretation. Property `DescribedBy` is required demand, not incidental; migration changes selection semantics in Step C |
| Value selection (`subject_assessment::assess_property`) | Property effective `ValueType` through `effective_relationship_targets` | Selected exact target, contribution evidence | Assessment-time lineage derivation; invoked only for present value today, after requiredness |
| Native kind / compatible dispatch (`assess_value`, `compatible_binding`) | Selected value descriptor lineage | Native anchor keys, governing kind; actual subject BaseValue kind | `ValueDescriptor::value_kind` → validation classification, repeated during assessment. Must become prepared kind in Step C |
| Constraint execution (`subject_constraints`) | Prepared effective `Constraints`; attachment `DescribedBy` | Concrete evaluator key, attachment/provenance | Registry lookup and fail-closed unsupported finding; scalar evaluator activation remains #811 |
| Readiness (`commitment_order`, `ReadinessPropagation`) | Every reached definition's same nine common edges, transitively | Exact IDs/labels; collector finding subjects | A second discovery walk, SCC grouping and reverse invalidity propagation; no active check needs another candidate's overall outcome |

## NameIndexes link reads

`../diagnostics/name-index-link-reads.json` is generated from the original inventory logs at
`0c033b6bca8f84de4be890967033b6001a53162e`, matching both SHA-256 hashes in
`name-index-inventory.json`. These are cache-membership misses inside the operation; aggregate
link-query counts corroborate their backend attribution. They are not all logical requests.

| Capture | Sample | SourceOf misses | SourceType misses | Total |
| --- | --- | --- | --- | --- |
| usage | 0 | 27 | 50 | 77 |
| usage | 1 | 26 | 49 | 75 |
| registry-thirtytwo-hit | 0 | 26 | 49 | 75 |
| registry-thirtytwo-hit | 1 | 26 | 49 | 75 |

The observed missing memberships are navigation inputs, not `AffordsDance`, `AffordsCommand`,
or `InstanceKeyRule`. Those three are read earlier by complete effective-schema computation.
Source content misses (63 semantic sources) remain in the separate original inventory.
Decide the required Relationships-index scope in Step C before preparing navigation inputs;
retain content for the selected consumers. Do not conclude that
prefetching only the seven source collections also prepares inverse navigation. Category `Extends`
and member `SourceType` bound reads need their own retention/demand accounting.

## Assessment-only versus contextual reads

Subject local properties and populated staged collections are legitimate execution reads. DS-KEY-006
`prepare_key_evidence` independently queries keyed saved lineage (`Owns` evidence) once per eligible
key for creates/new versions. Neither is a schema preparation regression. Both report-only and
installing paths share these reads; error handling differs only at final outcome installation.

No incorrect **Source today** classification was found in the reviewed consumer/input matrix.
This finer inventory expands its named rows without changing the reviewed decisions.

## Step C decisions to carry forward

NameIndexes first reads of lineage `SourceOf` and member `SourceType` are outside the
shared collection list. A bigger cache cannot remove those first reads. Step C must decide
whether validation's Relationships index needs inverse navigation at all. If retained,
these reads become named demand; the baseline inventory alone does not establish that need.

833's ValueType `DerivedDescriptor` also reads `AffordsOperator`. Account for that as
complete-payload acquisition overhead when adopting the merged foundation; it is not a
new validation consumer and is not part of this baseline's shared collection inventory.
