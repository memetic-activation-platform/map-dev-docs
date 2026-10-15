# Inspector geometry: four-mode design review

Status: proposed for review, 2026-10-15. This assessment records the project
owner's new geometry direction and identifies decisions still needing review.
It does not declare implementation complete or supersede the merged specifications
until their coordinated revisions are accepted. Performance work is deferred.
No enhancement issue or runtime change is part of this review.

## 1. Existing foundation and required changes

The implementation inspection used map-holons commit `f44cd25d`. The authoritative
documentation baseline is map-dev-docs commit `68e4ddf`.

Already aligned:

- Path Inspector allocates shared row heights and column widths from explicit
  policy. It does not size tracks from rendered child contents.
- Node inspectors allocate their own child regions. Generic and loader inspectors
  already share private geometry machinery.
- The Node slot requires an explicit local Visualizer Operator; Rust checks
  required/offered participation before selection, and materialization checks
  callable bindings. Dimensions and semantic requirements arrive together.
- Pending and realized destinations receive the same rectangle. Traversal topology,
  retained alternatives, stable occurrence identities, viewport movement and
  view-only zoom are established mechanisms to preserve.
- Selected Title Bar composition and its centrally declared actions remain useful.
  The Holon remains its semantic subject.

Conflicts requiring a coordinated revision:

| Existing rule or mechanism | Proposed replacement |
| --- | --- |
| Final shared-track states determine each occurrence's capability set | Per-occurrence presentation requirement is independent of the resulting track dimensions |
| Nine-state axis/capability matrix, including simultaneous singular and collection navigation | Four semantic slot intents; no combined intent unless a concrete case proves it necessary |
| Normal inspection divides space between properties, singular rail and an open collection | Properties and Collection share one main content region |
| Local property/collection maximization retains compatible siblings | Local full-content switching hides the other content view and preserves its state |
| Temporary context clears local expansion, with no remembered resumption | Per-occurrence memory of the last Properties or Collection view survives contextual presentation |
| Collection access can be exposed through source compression | A vertical source is already in Collection mode; only its allocation changes |
| Track compression implies presentation changes throughout the track | Each occurrence receives its own intent, including Compact identity in a large cell |

Relevant implementation seams are `visualizer-src/path-inspector.js`
(`allocateRows`), `node-presentation.js`, `inspector-layout.js`,
`holon-inspector.js`, `load-holons-inspector.js`, and `node-title-bar.js` under
map-holons `host/conductora/`. The existing nine-combination browser fixtures
must be replaced deliberately rather than treated as the target policy.

Connections First was deliberately retired in the preceding slice. References to
repairing or regression-testing that implementation in the supplied proposal are
stale relative to that decision. Preserve retirement; use an independent compatible
participant to test substitution, together with the retained loader specialization.

## 2. Proposed presentation model

Holon Inspector has four private modes:

| Mode | Required presentation |
| --- | --- |
| Properties | Identity/actions, properties, singular navigation and collection tabs; no collection viewer |
| Collection | Identity/actions, visible return-to-Properties control, tabs, collection actions and active viewer; no properties or singular rail |
| Relationship | Singular navigation, identity and restore; no properties, tabs or collection viewer |
| Compact identity | Recognizable identity and restore, responsive to the assigned aspect ratio |

Collection tab selection enters Collection mode. Returning to Properties hides
rather than reconstructs the collection. Neither local switch changes Path tracks.
Selected children, bound references, edits, tab, selection and scroll position
survive. Hidden content is inert and absent from keyboard navigation.

Each occurrence remembers its last full-content view, Properties or Collection.
Relationship and Compact identity do not overwrite it. Restore requests expanded
space through the immediate parent, then restores that view after an accepted
grant. A refused request preserves the current valid presentation. Never restore
a saved pixel rectangle. New ordinary occurrences start in Properties; specialized
loader defaults need an explicit semantic justification and initialization rule.

Recommended recovery control: a visible, labeled Properties control above the
collection tabs. Exact styling remains bounded review work. Do not introduce a
new label such as Fields or depend on an unlabeled gesture.

The slot speaks in implementation-independent intents:

| Intent | Obligation |
| --- | --- |
| Inspect | Normal inspection in the occurrence's remembered full-content view |
| Singular-navigation context | Singular navigation remains usable |
| Collection-navigation context | Collection navigation and already active content remain usable |
| Compact identity | Recognizable identity and restore access |

These are proposed contract concepts, not final executable identifiers. Use one
canonical assignment containing dimensions and one intent. The child's private
mode is a realization of that assignment and retained local state, not another
independently mutable parent input. Operations are local Visualizer Operations,
not Dances. A substitute need not reproduce Holon Inspector's private panes.
An incompatible Operator shape/meaning requires an explicit contract migration;
old and new participants must not silently share incompatible semantics.

## 3. Track policy and illustrative paths

Path assigns an intent per occurrence from navigation state, then allocates shared
tracks adequate for those obligations using parent-owned policy minima. Aggregating
track sizes does not aggregate or upgrade presentation intents. Minima belong in
the parent policy, checked against the promised participation range before selection;
rendered-content reports never determine them.

Notation: `P` Properties, `C` Collection, `R` Relationship, `K` Compact identity.
`WI/HI` are normal inspection budgets; `WR/HR` singular-context budgets;
`WC/HC` collection-context budgets; `WK/HK` compact budgets. These are policy
symbols, not measured contents or accepted numerical constants. `max` combines
requirements sharing a track. Each policy budget has preferred and minimum values.
Connector channels and framing are additional, counted by their actual owner.

Before a downward step, the source switches locally to C by selecting a collection.
The tables describe the result after traversal. For ordinary initial occurrences,
P and R remember P; C remembers the active collection. K keeps the last P/C value.

Pure vertical A↓B↓C: A:K (remembers C), B:C (remembers C), C:P
(remembers P); one column `max(WK,WC,WI)`, rows `HK,HC,HI`.
Prefer the three cells and two labeled channels in view. Further traversal pans
older context away rather than progressively shrinking the destination.

Pure horizontal A→B→C: A:K (remembers P), B:R (remembers P), C:P
(remembers P); columns `WK,WR,WI`, one row `max(HK,HR,HI)`.
The singular rail remains capped and right-aligned even if shared tracks give R
extra width. Extra height/width does not force K into full inspection.

The project owner accepted retaining the latest source on each axis along the
focused ancestry, at most two sources (2026-10-15). Each occurrence keeps its
independent presentation intent; shared track dimensions do not combine or upgrade
those obligations. For A→B↓C, A remains Relationship, B remains Collection and C
opens in Properties. This accepts the mixed-context space cost, with viewport
recovery when needed, rather than reducing retention to the immediate source.
Coordinates below are (column,row), zero-based, with no retained alternatives
displacing bands.

| Focus / step | Occurrence modes | Remembered views | Column widths | Row heights | Preferred visible context |
| --- | --- | --- | --- | --- | --- |
| A→B | A:R, B:P | A:P, B:P | WR,WI | max(HR,HI) | A,B |
| B↓C | A:R, B:C, C:P | A:P, B:C, C:P | WR,max(WC,WI) | max(HR,HC),HI | A,B,C |
| A↓B | A:C, B:P | A:C, B:P | max(WC,WI) | HC,HI | A,B |
| B→C | A:C, B:R, C:P | A:C, B:P, C:P | max(WC,WR),WI | HC,max(HR,HI) | A,B,C |
| A→B↓C→D | A:K, B:C, C:R, D:P | A:P, B:C, C:P, D:P | WK,max(WC,WR),WI | max(HK,HC),max(HR,HI) | A,B,C,D if budget permits |
| A→B↓C→D↓E | A:K, B:K, C:R, D:C, E:P | A:P, B:C, C:P, D:C, E:P | WK,max(WK,WR),max(WC,WI) | HK,max(HR,HC),HI | B,C,D,E if budget permits; A pan-recoverable |

The two-source mixed footprint can exceed the preferred pure-axis viewport.
Do not promise simultaneous visibility at every size. Preserve useful minima and
pan recovery. Compact and contextual cells may incidentally be visible outside
the preferred footprint; history does not reduce the policy budgets.

Restore C in A→B↓C→D↓E without moving it: C returns to remembered P;
A:R and B:C are its contextual ancestry under the accepted two-source rule;
D/E become K while retaining remembered C/P. Track budgets follow these new intents
at the same coordinates, and the viewport follows restored C. Restore does not
promote a retained branch or delete descendants.

For a retained alternative, retain A→B↓C plus A↓X. First B↓C inserts a whole row,
so X lies below C at (0,2). With C focused, A:R, B:C, C:P, X:K;
columns `WR,max(WC,WI)`, rows `max(HR,HC),HI,HK`.
Direct Restore X keeps placement and makes X:P (or its remembered C), A:C,
B/C:K; columns `max(WC,WI,WK),WK`, rows `max(HC,HK),HK,HI`.
The viewport follows A/X as useful; B/C stay pan-recoverable. Selecting a retained
destination through A instead invokes the existing topology promotion/exchange
rules and recomputes the same intent policy at the resulting coordinates.

For different selected inspector implementations in shared tracks, apply their
admitted common slot intents using the same parent policy. Each realizes its own
private view within the shared dimensions. No descendant probing, copied geometry,
or selection-on-resize is introduced. An offered contract must promise the entire
supported allocation range before the implementation is eligible.

### Concrete mixed-path questions

1. Resolved (project-owner acceptance, 2026-10-15): retained alternatives
   preserve history without adding presentation obligations outside the focused
   ancestry. With A→B↓C focused and alternative A↓X retained, A remains
   Relationship; X does not require simultaneous collection navigation in A.
   Restore A and select its collection to navigate downward. X and its descendants
   retain identity and state throughout.
2. Resolved: after A→B↓C, retain A:R and B:C. Latest-source-per-axis
   retention with independent occurrence intents is accepted; immediate-source-only
   retention is not the chosen policy. Track dimensions still aggregate adequate
   budgets without altering those intents.
3. While a parent requires collection context, may the local Properties control
   implicitly request a return to full inspection? Recommendation: yes, as an
   explicit parent-mediated Restore/Inspect request; apply Properties only after
   the grant. It cannot locally violate the current collection-context obligation.
   Under Inspect, Properties↔Collection remains wholly local.
4. Loader outcome presentation may justify initial Collection rather than P.
   Confirm that initial default separately from the shared restoration behavior;
   avoid resetting retained evidence or selected outcome content on Restore.

These reviewed paths do not require simultaneous singular and collection
navigation. The accepted retained-alternative rule removes that proposed combined
obligation: restoring the source provides access to the other direction. Any future
case requiring both at once must be reviewed explicitly; do not add a silent fifth
mode.

## 4. Authoritative specification revision map

| Authority | Coordinated revision after policy decisions |
| --- | --- |
| [Path interaction grammar](../hx/visualizers/structure/rooted-navigation/path-inspector/interaction-grammar.md) | Replace §4.4.1 nine-state derivation, shared-track protection examples and related §§6.3/7.3 references; define independent intents, adequate track minima, mixed/restore examples and viewport policy |
| [Path design](../hx/visualizers/structure/rooted-navigation/path-inspector/design-spec.md) | Replace track-derived capabilities, update source transition and restoration descriptions; preserve topology ownership |
| [Holon Inspector](../hx/visualizers/node/holon-inspector/design-spec.md) | Define four modes, full-content memory, Properties/Collection switching and contextual recovery; replace simultaneous-pane/maximization rules and property-height redistribution between those panes |
| [DAHN](../hx/dahn-design-spec.md) | Preserve general downward allocation and Operator admission; reconcile concrete participation references without creating a universal DAHN mode matrix |
| [Data Loader](../dancers/data-loader/data-loader-design-spec.md) | Specify justified initial outcome view and retained evidence/state; reuse allocation/restoration while keeping loader execution independent of presentation |
| [Space Navigator plan](space-navigator-impl-plan.md) | Record accepted replacement scope, delivery sequence and verification; retain Connections First retirement |

Keep existing topology rules, centralized title actions, selected child inspection,
semantic subjects and downward architectural dependencies. Do not rename established
roles just to append or remove Visualizer. `NodeInspector.VisualizerSlot` names a
role; Holon Inspector names an implementation.

## 5. Bounded implementation and verification sequence

Implementation and enhancement issues wait for design acceptance. First resolve
mixed retention/recovery decisions, revise the owning specifications coherently,
and review the documentation PR. Numerical minima are established through usable
allocation fixtures rather than rendered-row feedback or arbitrary universal counts.

1. Define the revised explicit assignment contract and participation migration;
   implement local P↔C switching under Inspect. Verify unchanged outer dimensions,
   selected child identities, edits, keyboard access and scroll/selection state.
2. Prove pure vertical traversal, final-rectangle pending feedback, source C retention,
   per-occurrence restoration, and the compact+collection+properties preferred budget.
3. Prove pure horizontal traversal, R source, capped right-aligned rail and Restore.
4. Prove K at wide/shallow, narrow/tall and small aspect ratios. Preserve identity,
   Restore and stable typography without allowing large tracks to imply Inspect.
5. Prove each reviewed mixed example, backtracking, branch promotion, alternatives,
   shared tracks, minimum overflow and viewport recovery. Check intent independently
   of geometry; dimensions alone cannot establish conformance.
6. Verify loader-specific semantics and an independent compatible participant using
   shared mechanisms. Preserve Connections First retirement and its historical
   overlap case as a containment regression.

At preferred dimensions include comfortable content plus connector/padding slack.
Reduce slack before reaching useful minima, then use owned scrolling and viewport
movement. Zoom to Fit remains view-only. Test actual selected non-table collection
and PropertyMap children, not implementations that mirror the layout algorithm.
