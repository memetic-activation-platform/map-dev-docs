# Candidate Shared DesignToken Vocabulary

## Executive finding

A defensible shared DesignToken vocabulary is already latent across major design systems, but it is much smaller than any one system's token catalog. The strongest convergence is not around exact token names. It is around a recurring semantic grammar: **surface**, **content/foreground**, **boundary/border**, **accent/primary action**, **focus**, **interaction state**, and **feedback/status**. Typography also has a real shared semantic core around **body**, **heading/title**, **label/caption**, and **display**, although the size hierarchies and composition details diverge.

Material, Fluent, Spectrum, Carbon, and Salesforce all independently encode much of this grammar. They differ in how they factor it: Material emphasizes role pairs such as `surface` / `onSurface`; Fluent composes neutral/brand/status with background/foreground/stroke and interaction state; Carbon uses functional families such as background/layer, text/icon, border, support, focus, and interaction-state variants; Spectrum distinguishes neutral/accent/feedback semantics and semantic content/background roles; Salesforce SLDS 2 has moved toward semantic global styling hooks such as surface, surface-container, on-surface, accent, border, and feedback families.[1][2][3][4][5]

The recommended outcome is therefore **not** a DAHN-owned master ontology. It is a small candidate commons whose concepts are peers with Material, Fluent, Spectrum, Carbon, Salesforce, and other vocabularies. Its authority comes only from adoption. Cross-vocabulary mappings preserve provenance and pluralism, and the MAP/DAHN vocabulary itself remains mappable rather than privileged.

For DAHN Selector eligibility, semantic mappings must be treated more conservatively than ordinary ontology browsing. A mapping that is merely "close" should not silently expand an MDS guarantee set. Only mappings explicitly asserted as substitutable for presentation-contract purposes should participate automatically in token satisfaction.

---

## 1. Research question

The practical DAHN requirement is:

    selected Theme -> one effective MDS
    effective MDS -> guaranteed DesignToken set
    Visualizer -> required DesignToken set

    selectable iff required tokens subset-of guaranteed tokens

This makes DesignToken identities an executable compatibility contract between independently authored Visualizers and Meta Design Systems. The research question is therefore not simply "which token names are popular?" It is:

> What semantic presentation concepts recur strongly enough across established design systems that they are credible candidates for a shared DesignToken commons, while retaining explicit mappings back to each source vocabulary?

A second question follows:

> Which mappings are semantically strong enough to participate in automated compatibility decisions, and which should remain informative mappings only?

---

## 2. Standards baseline: what DTCG does and does not provide

The Design Tokens Community Group (DTCG) provides the strongest current interoperability foundation for representing and exchanging design tokens. Its 2025.10 format standardizes token structure, values, types, references/aliases, groups, and exchange syntax. It intentionally leaves token methodology and organizational strategy to design-system authors.[6][7]

That means DTCG gives this work two important pieces:

1. **Design Token** is an appropriate general term for the named design decisions in the commons.
2. **Type** supplies standardized value classifications such as color, dimension, font family, font weight, and other token value types.

DTCG does **not** define a standard semantic vocabulary such as `Surface`, `Content.Primary`, `Focus.Indicator`, or `Status.Error`. The vocabulary proposed below therefore is not "the DTCG vocabulary". It is a candidate semantic commons represented using DTCG-aligned token concepts and types.

DTCG aliases are also narrower than the semantic mapping problem addressed here. DTCG defines an alias/reference as one token's value referencing another token. Aliases are useful for expressing design choices and semantic relationships, but they fundamentally encode value resolution inside a token system.[6] Cross-vocabulary commoning additionally needs to express degrees and directions of semantic correspondence.

---

## 3. A standards precedent for cross-vocabulary commoning: SKOS

W3C SKOS is directly relevant to the mapping layer. It was designed to connect concepts across independently governed concept schemes without requiring those schemes to merge. SKOS defines `exactMatch`, `closeMatch`, `broadMatch`, `narrowMatch`, and `relatedMatch`.[8]

This is unusually well aligned with the ontological-commoning posture:

- `exactMatch` expresses a high-confidence equivalence across schemes.
- `closeMatch` expresses sufficient similarity for some interchange uses but is deliberately non-transitive.
- `broadMatch` and `narrowMatch` preserve differences in semantic scope.
- `relatedMatch` records useful association without claiming equivalence.

SKOS explicitly notes that open environments make the distinction between one unified scheme and multiple schemes with mappings inherently contextual; it allows both points of view to coexist.[8] That is nearly the governance property desired here: a shared vocabulary may emerge and gain adoption without making other vocabularies subordinate to it.

MAP need not literally implement RDF/SKOS to benefit from this precedent. But its mapping semantics should be at least this discriminating.

---

## 4. Evidence of a latent common grammar

### 4.1 Material

Material 3 explicitly describes its color system in terms of semantic roles rather than raw colors. Its system tokens include `primary`, `secondary`, `tertiary`, `surface`, multiple `surfaceContainer` levels, `onSurface`, `onSurfaceVariant`, `outline`, `outlineVariant`, and `error` / `onError` role pairs.[9][10]

Material Web distinguishes reference tokens from system tokens: reference tokens hold concrete values, while system tokens define design decisions and roles spanning color, typography, elevation, and shape.[11]

Material's typography roles are similarly semantic: display, headline, title, body, and label, with size variants.[12]

### 4.2 Microsoft Fluent 2

Fluent explicitly uses two layers: context-agnostic global tokens and semantic alias tokens. Fluent says alias token names are intended to make their function recognizable without knowing concrete values.[13]

Its color aliases are structured into neutral, brand, status, and generic families. Neutral aliases include `Background`, `Foreground`, and `Stroke`, with hover, pressed, selected, and disabled variants. Brand aliases use the same background/foreground/stroke grammar. Status aliases distinguish danger, success, and warning across background, foreground, and border/stroke roles.[14]

Fluent's typography ramp uses semantic labels including caption, body, subtitle, title, large title, and display.[15] Its broader token categories include spacing, border radius, font, line height, stroke width, shadow, duration, and easing.[16]

### 4.3 Adobe Spectrum

Spectrum states that semantic meanings are codified in design tokens and identifies informative, accent, negative, notice, and positive as semantic color meanings.[17]

Current Spectrum Web Components documentation describes semantic token aliases such as `--spectrum-background-base-color`, `--spectrum-neutral-content-color-default`, `--spectrum-neutral-subdued-content-color-default`, `--spectrum-disabled-background-color`, and `--spectrum-focus-indicator-color`. It distinguishes fixed/global values from semantic aliases whose concrete values change with theme and scale.[3]

Spectrum also has semantic typography families including heading, body, detail, and code, and a platform-independent spacing scale.[3][18]

### 4.4 IBM Carbon

Carbon's core color-token families are unusually explicit: Background, Layer, Layer accent, Field, Border, Text, Link, Icon, Support, Focus, and Miscellaneous.[4]

Representative semantic tokens include `$background`, `$layer-01`, `$text-primary`, `$text-secondary`, `$text-disabled`, `$icon-primary`, `$border-subtle`, `$support-error`, `$support-success`, `$support-warning`, `$support-info`, and `$focus`. Carbon also defines state variants such as `$background-hover`, `$background-active`, and `$background-selected`.[4]

Carbon's typography is tokenized into roles such as body, heading, label, helper text, and code.[19] Carbon also defines a systematic spacing scale, but the scale positions are primarily numeric/reference-like rather than semantic presentation roles.[20]

### 4.5 Salesforce Lightning Design System 2

Salesforce is currently moving from its older design-token system toward SLDS 2 global styling hooks. Salesforce documentation recommends semantic hooks over raw palette values and says the latest SLDS 2 adds semantic UI color global styling hooks.[21][22]

The current SLDS 2 ecosystem exposes semantic families such as `surface`, `surface-container`, `on-surface`, `accent`, `border`, and feedback concepts including error, success, and warning. Salesforce's own migration guidance emphasizes selecting hooks according to semantic context rather than matching raw color values.[5][23]

Salesforce also exposes categories for spacing, typography, border/radius, shadow, timing, and dimensions, but—as with several other systems—the non-color scales are more strongly standardized internally than semantically aligned across vendors.[24]

---

## 5. Candidate shared vocabulary

The table below is deliberately conservative. It separates concepts with strong evidence of shared semantics from those that merely have superficially similar names.

### Tier A — strongest candidates for a shared commons

| Candidate concept | Intended semantic meaning | Material | Fluent | Spectrum | Carbon | Salesforce | Assessment |
|---|---|---|---|---|---|---|---|
| `Surface` | Base visual surface/canvas on which content appears | `surface` / `background` | `colorNeutralBackground1` family | `background-base-color` | `$background` | `surface-1` | Very strong |
| `Surface.Container` | Contained/layered surface above or within a base surface | `surfaceContainer*` | neutral background levels / card background | layered/background semantic aliases | `$layer-*` | `surface-container-*` | Strong concept; mappings often close rather than exact |
| `Content.Primary` | Highest-normal-emphasis foreground content on a neutral surface | `onSurface` | `colorNeutralForeground1` | `neutral-content-color-default` | `$text-primary`, `$icon-primary` | `on-surface-*` high-emphasis role | Very strong; source systems differ on whether text/icon are split |
| `Content.Secondary` | Lower-emphasis foreground content | `onSurfaceVariant` | `colorNeutralForeground2/3` | neutral subdued content | `$text-secondary`, `$icon-secondary` | lower-emphasis `on-surface-*` | Very strong concept; rank mappings need care |
| `Border` | Default visible boundary/divider treatment | `outline` | `colorNeutralStroke1` | semantic border roles | `$border-*` | `border-*` | Very strong |
| `Accent` | Primary product/brand/interactive emphasis | `primary` | `Brand*` aliases | `accent` | `$interactive` / brand roles | `accent-*` | Strong but not exact in scope |
| `Focus.Indicator` | Visible keyboard/input focus indication | component focus roles, often primary/outline based | focus uses differentiated stroke treatment | `focus-indicator-color` | `$focus` | focus/ring/shadow semantic treatment | Strong semantic capability even when not represented as one global token |

### Tier B — strong recurrent concepts, but with meaningful vocabulary/scope differences

| Candidate concept | Cross-system evidence | Main caveat |
|---|---|---|
| `Content.Disabled` | Fluent disabled foreground; Spectrum disabled semantics; Carbon text/icon disabled; Salesforce disabled families; Material component-state handling | Material often composes disabled treatment rather than exposing one system color role |
| `Surface.Inverse` / `Content.Inverse` | Material inverse surface roles; Fluent inverted roles; Carbon background/text inverse; Salesforce inverse surface families | Spectrum models high-contrast/static contexts differently |
| `Status.Error` | Material error; Fluent danger; Spectrum negative; Carbon support-error; Salesforce error | `danger`, `negative`, and `error` overlap strongly but are not always extensionally identical |
| `Status.Success` | Fluent success; Spectrum positive; Carbon support-success; Salesforce success | Material lacks an equivalent core M3 system role |
| `Status.Warning` | Fluent warning; Spectrum notice; Carbon support-warning; Salesforce warning | Material lacks an equivalent core M3 system role; "notice" can be broader than warning |
| `Status.Info` | Spectrum informative; Carbon support-info; Salesforce info family; information patterns in Fluent | Fluent's currently documented core status alias page foregrounds danger/success/warning rather than a directly parallel info family |
| `Typography.Body` | Material body; Fluent body; Spectrum body; Carbon body; Salesforce body styles | Exact sizes and density assumptions differ |
| `Typography.Heading` | Material headline/title; Fluent title/subtitle; Spectrum heading; Carbon heading; Salesforce heading | Systems disagree on headline vs title distinctions |
| `Typography.Label` | Material label; Carbon label; Fluent caption/body styles used for labels; Spectrum detail; Salesforce label/text utilities | Most systems have the role, but naming and intended use differ |
| `Typography.Display` | Material display; Fluent display; Carbon display/fluid heading; large Spectrum headings | Not universally treated as a distinct semantic family |

### Tier C — common design-system machinery, but not yet a shared semantic vocabulary

These should **not** be promoted into a shared semantic DesignToken commons merely because all systems have them:

- spacing scales;
- radius/corner scales;
- stroke-width scales;
- elevation/shadow scales;
- duration and easing scales;
- raw font sizes/weights;
- raw color palettes.

The systems strongly agree that these values should be tokenized. They do **not** strongly agree on semantic role identities for the individual scale steps. For example, Carbon uses numbered spacing tokens, Spectrum uses numeric scale positions, Fluent uses size labels, and Salesforce uses its own numbered hooks.[16][18][20][24]

A commons can add semantic spacing or radius roles later if actual cross-system usage supports them. It should not manufacture them now simply to make the ontology look complete.

---

## 6. Interaction state is better understood as an orthogonal semantic dimension

Hover, pressed/active, selected, disabled, and focus recur across all five ecosystems, but they are not consistently modeled as standalone tokens. Fluent appends state variants to background/foreground/stroke aliases; Carbon provides background/layer selected, hover, and active variants; Spectrum component tokens encode default/hover/down/focus states; Material often handles state at the component-token/state-layer level; Salesforce similarly exposes contextual state treatment.[4][14][17]

This suggests that the common semantic structure is closer to:

    presentation role x emphasis/context x interaction state

than to a flat global list.

For example:

    Surface + Selected
    Surface + Hover
    Content.Primary + Disabled
    Accent + Pressed
    Border + Focus

Whether MAP represents these as independently addressable DesignToken holons, compositional relationships, or precomposed token instances is a separate schema question. The research finding is that **state is a cross-cutting dimension**, not naturally a peer of `Surface` or `Content`.

This matters for DAHN because a flat vocabulary created by taking the union of vendor token names would create a huge and brittle token set. A factored semantic model can express the same contract with fewer concepts and more faithful mappings.

---

## 7. Proposed candidate commons v0.1

If the goal were to publish a deliberately small vocabulary today, the evidence supports starting here:

    Surface
    Surface.Container

    Content.Primary
    Content.Secondary

    Border
    Accent
    Focus.Indicator

with interaction-state concepts:

    Hover
    Pressed
    Selected
    Disabled

and, as a slightly less universal feedback extension:

    Status.Error
    Status.Success
    Status.Warning
    Status.Info

For typography, a parallel compact vocabulary is defensible:

    Typography.Body
    Typography.Heading
    Typography.Label
    Typography.Display

This is **not** a recommendation that DAHN Issue 698 introduce all of these. The current DAHN vertical slice should introduce only tokens actually required by its initial Visualizers/MDS. The list above is a research candidate for a broader common vocabulary, not a PR checklist.

The naming itself should also remain open to commoning. `Content` is used here because it avoids privileging Fluent's `Foreground`, Carbon's split `Text`/`Icon`, or Material/Salesforce's `OnSurface` idiom. Similarly, `Border` is more broadly understandable than Fluent's `Stroke`, while mappings can preserve those source terms.

---

## 8. Source-vocabulary mappings

A peer mapping layer should preserve the source concepts rather than replacing them. Illustratively:

| Commons concept | Material | Fluent | Spectrum | Carbon | Salesforce |
|---|---|---|---|---|---|
| `Surface` | `surface` | `colorNeutralBackground1` | `background-base-color` | `$background` | `surface-1` |
| `Surface.Container` | `surfaceContainer` family | neutral background hierarchy | layered/background aliases | `$layer-01` family | `surface-container-1` family |
| `Content.Primary` | `onSurface` | `colorNeutralForeground1` | `neutral-content-color-default` | `$text-primary`; `$icon-primary` | high-emphasis `on-surface-*` |
| `Content.Secondary` | `onSurfaceVariant` | `colorNeutralForeground2/3` | neutral subdued content | `$text-secondary`; `$icon-secondary` | lower-emphasis `on-surface-*` |
| `Border` | `outline` | `colorNeutralStroke1` | semantic border family | `$border-*` | `border-*` |
| `Accent` | `primary` | Brand aliases | `accent` | `$interactive` / brand | `accent-*` |
| `Focus.Indicator` | focus treatment derived from system/component roles | focus stroke treatment | `focus-indicator-color` | `$focus` | semantic focus treatment |
| `Status.Error` | `error` | `Danger*` | `negative` | `$support-error` | `error-*` |
| `Status.Success` | — | `Success*` | `positive` | `$support-success` | `success-*` |
| `Status.Warning` | — | `Warning*` | `notice` | `$support-warning` | `warning-*` |
| `Status.Info` | — | information semantics | `informative` | `$support-info` | `info-*` |

These cells should **not** all be encoded as `exactMatch`. The table says "this is the closest source concept/family," not "these are extensionally identical concepts."

Examples of mapping judgments likely to survive closer review:

- `Content.Primary` ↔ Fluent `colorNeutralForeground1`: plausible exact or very-close match.
- `Content.Primary` ↔ Carbon `$text-primary`: likely **narrowMatch** from the commons concept if `Content` intentionally includes both text and icons.
- `Status.Error` ↔ Spectrum `negative`: likely **closeMatch**, because Spectrum's negative semantic category includes more than literal errors.
- `Status.Warning` ↔ Spectrum `notice`: likely **closeMatch**, not exact.
- `Accent` ↔ Material `primary`: likely close, because Material primary is broader than only interactive accent treatment.

The mapping graph is therefore part of the research product, not cleanup metadata.

---

## 9. Selector semantics: do not equate semantic similarity with substitutability

For ordinary ontology navigation, a `closeMatch` is useful. For DAHN Visualizer selection, automatically treating every close match as satisfying a required DesignToken would be unsafe.

Suppose:

    Visualizer requires Commons.Status.Error
    MDS guarantees Spectrum.Negative
    Spectrum.Negative closeMatch Commons.Status.Error

The concepts are clearly related, but Spectrum's `negative` category can include error, alert, rejected, and failed semantics. Whether that is a safe substitution for a Visualizer's specific error treatment is an MDS contract decision, not something the Selector should infer from lexical or ontological proximity alone.[17]

A safer architecture is:

    NativeGuaranteedTokens(MDS)
        + explicitly substitutable mappings/adapters
        = EffectiveGuaranteedTokens(MDS)

    Selectable(V, MDS)
        iff RequiredTokens(V) subset-of EffectiveGuaranteedTokens(MDS)

Default automatic closure should be limited to mappings carrying a strong substitutability assertion—conceptually analogous to `exactMatch`, or an even more domain-specific `satisfiesPresentationRole` relationship. `closeMatch`, broader/narrower, and related mappings should remain available to humans/agents for discovery and bridge authoring without silently affecting Selector eligibility.

This preserves the distinction between:

- **ontological mapping**: how meanings relate;
- **presentation-contract mapping**: whether one token may safely satisfy another in a particular MDS context.

---

## 10. Aliases still have an important role

Fluent aliases and DTCG references remain useful, but at a different layer.

They are well suited to expressing bindings such as:

    Commons.Content.Primary -> Fluent.colorNeutralForeground1

when an MDS author has deliberately adopted that mapping and wants the target value to resolve through the Fluent token. In that case the alias/value reference is the executable binding.

But the semantic commons should separately retain the mapping assertion and provenance describing *why* these concepts are considered equivalent or substitutable. Otherwise value resolution erases the distinction between exact equivalence, contextual equivalence, and approximate correspondence.

In MAP terms, this argues for keeping the semantic relationship first-class even when a Theme or MDS realization also uses an alias-like resolution mechanism.

---

## 11. Why this is a strong ontological-commoning case study

The process closely resembles the research methodology used by W3C Open UI. Open UI explicitly starts with design-system surveys, identifies recurring concepts, normalizes terminology, and then develops proposals. Its Design Systems Analysis guidance says it uses existing design systems as evidence for "cataloging emergent UI standards," and its process calls for reviewing concepts across systems and identifying common ones.[25][26]

The DesignToken case extends that methodology from component semantics into presentation semantics and adds an executable payoff:

    better semantic mappings
        -> larger trustworthy MDS guarantee closure
        -> more independently authored Visualizers become eligible
        -> greater composability

The shared vocabulary can therefore become common through use rather than decree. MAP/DAHN may propose a vocabulary, Material may retain Material's vocabulary, Fluent may retain Fluent's, and communities may adopt whichever concepts are useful. Cross-mappings make convergence beneficial without making convergence mandatory.

The commons vocabulary is a peer. It becomes influential only to the degree that participants adopt it directly or publish trusted mappings to it.

---

## 12. Recommendations for DAHN

### Near term: Issue 698 / current vertical slice

Keep the current PR narrow.

- Retain `DesignToken` as the DTCG-aligned generic concept.
- Use DTCG-aligned token Type terminology where DAHN introduces value types.
- Introduce only the semantic tokens actually required by the initial Visualizers and MDS.
- Prefer names that fall within the high-confidence concept families above (`Surface`, `Content`, `Border`, `Accent`, `Focus`) when they fit the actual requirement.
- Do not add the whole candidate commons to make the schema appear complete.
- Do not add cross-vocabulary mapping machinery unless the vertical slice actually needs it.

### Next design/research increment

Create a first-class **DesignToken Concept Scheme / Vocabulary** model and a mapping model, informed by SKOS semantics but expressed in MAP-native terms.

At minimum, preserve distinctions equivalent to:

    ExactMatch
    CloseMatch
    BroaderMatch
    NarrowerMatch
    RelatedMatch

Then decide separately which mapping assertions are strong enough to produce a `SatisfiesDesignToken` / guarantee bridge usable by the Selector.

### Candidate commons process

Treat the vocabulary above as a **proposal generated from evidence**, not a finalized MAP vocabulary. For each candidate token:

1. write a precise definition independent of any source system;
2. cite the source concepts that motivated it;
3. classify each source mapping by semantic strength;
4. record disagreements and unmapped nuances;
5. test whether independently authored Visualizers can depend on the concept without implicitly assuming one source design system;
6. accept the concept into the commons only if the semantic abstraction reduces translation cost without erasing meaningful distinctions.

This is effectively an Open UI-style design-system analysis applied to token semantics.[25]

---

## 13. Bottom line

There **is** a meaningful de facto consensus to common from. It is strongest at the level of a semantic grammar rather than a finished token catalog.

The clearest shared core is:

    Surface
    Surface.Container
    Content.Primary
    Content.Secondary
    Border
    Accent
    Focus.Indicator

plus orthogonal interaction-state semantics:

    Hover
    Pressed
    Selected
    Disabled

and a widely recurring, though slightly less universal, feedback family:

    Status.Error
    Status.Success
    Status.Warning
    Status.Info

Typography also supports a plausible parallel commons around Body, Heading, Label, and Display.

Spacing, radius, shadow/elevation, and motion should remain outside the semantic commons for now: the systems agree on tokenizing them but not yet on shared semantic role vocabularies.

The more important architectural result is that **the commons need not be canonical to be useful**. A MAP vocabulary can be one peer concept scheme among many. Explicit mappings preserve the independent source ontologies. Adoption creates gravity. And carefully governed substitutability mappings turn ontological commoning into executable DAHN interoperability.

---

## Sources

1. Microsoft Fluent 2, “Design tokens.” https://fluent2.microsoft.design/design-tokens
2. Material Web, “Color.” https://github.com/material-components/material-web/blob/main/docs/theming/color.md
3. Adobe Spectrum Web Components, “Styles / Design tokens.” https://opensource.adobe.com/spectrum-web-components/tools/styles/
4. IBM Carbon Design System, “Color tokens.” https://carbondesignsystem.com/elements/color/tokens/
5. Salesforce UX, “design-system-2-starter-kit” semantic global styling hook guidance. https://github.com/salesforce-ux/design-system-2-starter-kit/blob/main/.builderrules
6. Design Tokens Community Group, “Design Tokens Format Module 2025.10.” https://www.designtokens.org/TR/2025.10/format/
7. Design Tokens Community Group, “FAQ.” https://www.designtokens.org/faq/
8. W3C, “SKOS Simple Knowledge Organization System Reference,” Recommendation, 2009. https://www.w3.org/TR/skos-reference/
9. Android Developers, “Material 3 ColorScheme.” https://developer.android.com/reference/kotlin/androidx/compose/material3/ColorScheme
10. Android Developers, “Material Design 3 in Compose.” https://developer.android.com/develop/ui/compose/designsystems/material3
11. Material Web, “Theming.” https://github.com/material-components/material-web/blob/main/docs/theming/README.md
12. Material Web, “Typography.” https://github.com/material-components/material-web/blob/main/docs/theming/typography.md
13. Microsoft Fluent 2, “Design tokens.” https://fluent2.microsoft.design/design-tokens
14. Microsoft Fluent 2, “Web Alias Color Tokens.” https://fluent2.microsoft.design/color-tokens
15. Microsoft Fluent 2, “Typography.” https://fluent2.microsoft.design/typography
16. Microsoft Fluent UI, “Design Tokens architecture.” https://github.com/microsoft/fluentui/blob/master/docs/architecture/design-tokens.md
17. Adobe Spectrum, “Color system.” https://spectrum.adobe.com/page/color-system/
18. Adobe Spectrum, “Spacing.” https://spectrum.adobe.com/page/spacing/
19. IBM Carbon Design System, “Typography / Type sets.” https://carbondesignsystem.com/elements/typography/type-sets/
20. IBM Carbon Design System, “Spacing.” https://carbondesignsystem.com/elements/spacing/overview/
21. Salesforce Developers, “Compare SLDS Versions.” https://developer.salesforce.com/docs/platform/lwc/guide/create-components-css-slds1-slds2.html
22. Salesforce Developers, “Preparing your App for the Lightning Design System Color Update.” https://developer.salesforce.com/blogs/2023/06/preparing-your-app-for-the-lightning-design-system-color-update
23. Salesforce Developers, “Interpret Your Results / SLDS Validator.” https://developer.salesforce.com/docs/platform/slds-validator/guide/interpret-your-results.html
24. Salesforce Developers, “LWC Development Tools / Styling hook categories.” https://developer.salesforce.com/docs/platform/lwc/guide/mcp-lwc.html
25. Open UI, “Design Systems Analysis.” https://open-ui.org/design-system-analysis-guide/
26. Open UI, “Getting Involved / How we do Research.” https://open-ui.org/get-involved/
