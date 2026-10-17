# Path Inspector Grammar Has Moved

The canonical [Path Inspector Interaction Grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md)
lives with the concrete RootedNavigation implementation. This page is navigation
only. Historical section IDs are retained below; the old nine-state outline is
not a second behavioral authority.

<a id="dahn-path-inspector-interaction-grammar"></a>
<a id="change-log"></a>
<a id="v04"></a>
<a id="v03"></a>
<a id="v02"></a>
<a id="v01"></a>
<a id="status"></a>
<a id="purpose-and-authority"></a>
<a id="1-vocabulary"></a>
<a id="11-rooted-navigation-topology"></a>
<a id="12-root"></a>
<a id="13-occurrence"></a>
<a id="14-focus"></a>
<a id="16-navigation-topology-versus-spatial-projection"></a>
<a id="19-column"></a>
<a id="110-row"></a>
<a id="111-sparse-cell"></a>
<a id="2-topology-production-rules"></a>
<a id="21-inspect"></a>
<a id="8-state-preservation"></a>
<a id="11-relationship-to-space-navigator"></a>

[1 small state model](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#1-small-state-model)

<a id="15-viewport"></a>
<a id="112-spatial-budget"></a>
<a id="4-focus-dependent-geometry"></a>
<a id="41-navigation-focus-determines-allocation-priority"></a>
<a id="42-column-width-is-a-path-inspector-decision"></a>
<a id="43-row-height-is-a-path-inspector-decision"></a>
<a id="44-cell-budget-is-derived"></a>
<a id="propertymap-sub-slot-content-extent"></a>
<a id="45-geometry-emerges-from-topology-and-focus"></a>
<a id="46-minimum-useful-extent-and-surface-growth"></a>
<a id="47-view-operations-and-pinned-chrome"></a>
<a id="5-parent-and-child-spatial-responsibility"></a>
<a id="51-parent-owns-inter-child-geometry"></a>
<a id="52-child-owns-intra-child-adaptation"></a>
<a id="53-recursive-spatial-allocation"></a>
<a id="54-budget-changes-do-not-trigger-reselection-by-default"></a>
<a id="55-semantic-capability-may-constrain-selection"></a>
<a id="6-responsive-child-realization"></a>
<a id="61-responsive-realization-belongs-to-the-child"></a>
<a id="62-compression-is-not-scaling"></a>
<a id="63-semantic-obligations-survive-compression"></a>
<a id="64-responsive-thresholds-belong-to-the-visualizer"></a>
<a id="7-compression-and-overflow"></a>
<a id="71-compression-is-allocation-change"></a>
<a id="72-independent-axis-compression"></a>
<a id="73-partial-and-full-compression"></a>
<a id="74-layout-overflow-versus-off-viewport"></a>
<a id="75-branch-local-overflow"></a>

[7 preferred footprint and constrained viewports](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#7-preferred-footprint-and-constrained-viewports)

<a id="17-horizontal-traversal"></a>
<a id="22-horizontal-traversal"></a>

[3 pure horizontal transitions](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#3-pure-horizontal-transitions)

<a id="18-vertical-traversal"></a>
<a id="23-vertical-traversal"></a>

[2 pure vertical transitions](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#2-pure-vertical-transitions)

<a id="113-semantic-presentation-obligations"></a>
<a id="441-node-inspector-slot-compression-contract"></a>

[3 child slots and their contracts](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#3-child-slots-and-their-contracts)

<a id="24-branch"></a>
<a id="34-vertical-alternative-insertion"></a>
<a id="35-horizontal-alternative-insertion"></a>
<a id="36-grid-band-insertion-preserves-identity"></a>

[5 new and retained alternatives](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#5-new-and-retained-alternatives)

<a id="25-scan"></a>
<a id="26-restore"></a>
<a id="27-re-root"></a>
<a id="29-close-branch"></a>

[4 restore and backtracking](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#4-restore-and-backtracking)

<a id="28-destination-first-transitions"></a>

[Destination first transitions](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#destination-first-transitions)

<a id="3-two-dimensional-grid-projection"></a>
<a id="31-projection-as-a-derived-grid"></a>
<a id="32-traversal-path-integrity"></a>
<a id="33-replaceable-leaves"></a>
<a id="37-sparse-cells-are-not-occurrences"></a>
<a id="38-stable-attachment"></a>
<a id="39-lineage-connectors"></a>

[6 placement and connector rules](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#6-placement-and-connector-rules)

<a id="9-derived-rather-than-enumerated-interaction"></a>
<a id="91-small-grammar-large-state-space"></a>
<a id="92-mockups-as-conformance-examples"></a>
<a id="93-unmocked-paths-must-remain-coherent"></a>
<a id="10-grammar-invariants"></a>
<a id="15-summary"></a>

[9 essential invariants and conformance examples](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#9-essential-invariants-and-conformance-examples)

<a id="12-relationship-to-visualizer-selection"></a>
<a id="13-relationship-to-adjacent-specifications"></a>

[References and revision](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md#references-and-revision)

<a id="14-intentionally-deferred-decisions"></a>

[8 mixed paths specific contract questions](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md#8-mixed-paths-specific-contract-questions)
