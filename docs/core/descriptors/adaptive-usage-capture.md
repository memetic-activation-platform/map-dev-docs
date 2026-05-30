# Adaptive Visualization Usage, Personalization, and Collective Visual Defaults

## Summary

MAP and DAHN visualization behavior is inherently adaptive.

Visualization is not treated as a fixed rendering layer attached statically to a type. Instead, visualization behavior emerges from:

- local personalization
- repeated interaction patterns
- salience signaling gestures
- affinity signaling through navigation and embedding
- contextual usage patterns
- collective aggregation within shared spaces

This document captures a conceptual model for:

- personalized visualization state
- visualization usage metrics
- salience and affinity signaling
- adaptive visual defaults
- collective visualization evolution
- sovereignty-preserving aggregation

This pattern is closely related to descriptor usage and schema evolution, but it concerns visualization behavior rather than schema structure.

---

# 1. Core Principle

Visualization in MAP is not purely declarative.

It is adaptive, contextual, and socially shaped.

The same holon type may be visualized differently:

- by different agents
- in different spaces
- in different execution contexts
- for different purposes
- at different levels of detail
- with different salience priorities

Visualization therefore becomes:

> a living behavioral layer over the ontology.

---

# 2. Personalization as First-Class State

## Core idea

Each agent may personalize how holons are visualized.

This includes choices such as:

- which visualizer to use for a holon type
- which value visualizer to use for a property type
- which collection visualizer to use
- which relationships are expanded by default
- which properties are hidden
- which properties are emphasized
- which sections are collapsed
- ordering and layout decisions
- embedding preferences
- preferred navigation paths
- preferred detail levels

These choices are not incidental UI state.

They are durable expressions of local salience and meaning.

## Personalization persistence

The system therefore needs a place to persist visualization choices so that future interactions can reuse them.

For example:

> When an agent revisits a holon type, the system should bias toward previously preferred visual arrangements.

This implies some form of:

- `VisualizerUsage`
- `VisualizationPreference`
- `VisualizationContext`
- `VisualizerSelection`
- `VisualizationProfile`

or related concepts.

---

# 3. Visualization Gestures as Semantic Signals

## Core idea

Visualization interactions are not merely interface events.

They are semantic signals.

They communicate:

- salience
- affinity
- attention
- importance
- workflow relevance
- conceptual grouping
- contextual usefulness

This means interaction telemetry is not simply analytics data. It becomes part of the adaptive intelligence layer of the MAP.

---

# 4. Salience Signals

## Property salience

Gestures such as:

- moving properties upward in a layout
- pinning properties
- expanding properties
- repeatedly accessing properties
- revealing hidden properties
- suppressing properties
- resizing visual emphasis

all act as salience indicators.

These suggest:

> This property is important in this context.

Possible derived metrics:

- property display frequency
- property expansion frequency
- property reorder frequency
- average visual prominence
- hide frequency
- reveal frequency
- interaction dwell time
- edit frequency
- sort priority frequency

## Relationship salience

Relationship navigation is also a salience signal.

For example:

- repeatedly traversing a relationship
- expanding a relationship inline
- pinning a relationship view
- embedding target holons
- visualizing relationship collections

suggests that:

> This relationship is operationally important.

Possible derived metrics:

- traversal frequency
- inline expansion frequency
- embed frequency
- relationship dwell time
- relationship reuse frequency
- relationship persistence frequency

---

# 5. Affinity Signals

## Relationship affinity

Frequent traversal between two holon types suggests affinity.

For example:

> When viewing holons of type T1, users frequently navigate relationship R to holons of type T2.

This indicates:

- conceptual association
- workflow coupling
- operational relevance
- cognitive adjacency

Affinity is stronger than simple salience.

Salience means:

> This element matters.

Affinity means:

> These elements meaningfully belong together.

## Embedding as affinity signaling

Embedding gestures are especially strong affinity indicators.

For example:

- embedding a target holon inside another holon's visualization
- repeatedly visualizing two holon types together
- preserving side-by-side layouts
- nesting collections within parent views

suggests:

> These structures are cognitively and operationally coupled.

Embedding therefore acts as a strong affinity signal between:

- holon types
- relationship types
- property groups
- visualization contexts

---

# 6. Visualization Usage Records

## Core idea

Just as descriptor usage captures schema interaction patterns, visualization usage records capture visualization interaction patterns.

These records become the natural place to accumulate:

- personalization state
- salience metrics
- affinity metrics
- layout preferences
- visualization context usage
- adaptive rendering signals

Possible concepts:

- `VisualizerUsage`
- `VisualizationUsage`
- `VisualizationPreference`
- `VisualizationAffinity`
- `VisualizationContextUsage`

The exact decomposition remains open.

---

# 7. Suggested Conceptual Model

## VisualizationUsage

Captures how a holon type or descriptor is visualized within a particular context.

Because this usage relationship is intentionally descriptor-agnostic, the
visualized descriptor target should use the v2.0 generic descriptor root rather
than the removed `TypeDescriptor` node.

Possible properties:

| Property | Purpose |
| --- | --- |
| `viewer_ref` | Agent or viewer |
| `space_ref` | Space where usage occurred |
| `descriptor_ref` | Descriptor being visualized |
| `visualizer_ref` | Visualizer selected |
| `usage_count` | Number of uses |
| `last_used_at` | Most recent use |
| `context_signature` | Contextual usage key |
| `salience_profile` | Derived salience vector |
| `affinity_profile` | Derived affinity vector |

Possible relationships:

| Relationship | Target |
| --- | --- |
| `UsesVisualizer` | `Visualizer` |
| `VisualizesDescriptor` | `DescriptorRoot` |
| `HasPropertyVisualizationMetric` | `PropertyVisualizationMetric` |
| `HasRelationshipVisualizationMetric` | `RelationshipVisualizationMetric` |
| `HasEmbeddingAffinityMetric` | `EmbeddingAffinityMetric` |

---

# 8. Property Visualization Metrics

## Purpose

Captures visualization-specific interaction patterns for properties.

Possible metrics:

| Metric | Meaning |
| --- | --- |
| display frequency | How often property is shown |
| hide frequency | How often property is hidden |
| reorder frequency | How often property is repositioned |
| expansion frequency | How often expanded |
| edit frequency | How often edited |
| pin frequency | How often pinned |
| visual prominence score | Aggregate salience score |
| contextual relevance score | Relevance in specific contexts |

These metrics become signals for:

- default layouts
- adaptive forms
- progressive disclosure
- intelligent summarization
- compact vs expanded rendering
- context-aware visualization

---

# 9. Relationship Visualization Metrics

## Purpose

Captures visualization and navigation patterns involving relationships.

Possible metrics:

| Metric                     | Meaning                                       |
|----------------------------|-----------------------------------------------|
| traversal frequency        | How often traversed                           |
| inline expansion frequency | How often expanded inline                     |
| embed frequency            | How often targets embedded                    |
| co-navigation frequency    | Frequently traversed with other relationships |
| persistence frequency      | How often kept open                           |
| affinity score             | Strength of association                       |

These metrics support:

- adaptive navigation
- predictive expansion
- graph visualization weighting
- context-aware relationship ordering
- embedded visualization suggestions

---

# 10. Visualization Affinity

## Core idea

Visualization affinity reflects the tendency for structures to be experienced together.

This may arise from:

- repeated co-visualization
- repeated embedding
- repeated navigation
- repeated simultaneous expansion
- repeated contextual grouping

Possible affinity relationships:

| Source | Relationship | Target |
| --- | --- | --- |
| `HolonType` | `HasVisualizationAffinity` | `HolonType` |
| `RelationshipType` | `HasVisualizationAffinity` | `RelationshipType` |
| `PropertyDescriptor` | `HasVisualizationAffinity` | `PropertyDescriptor` |

These affinities can later influence:

- layout recommendations
- graph clustering
- embedded views
- adaptive dashboards
- contextual summarization
- predictive navigation

---

# 11. Contextual Visualization

## Visualization is context-sensitive

Visualization preferences likely depend on more than:

- holon type
- visualizer type

Additional contextual factors may eventually matter:

- current workflow
- active dance
- device form factor
- interaction mode
- urgency
- collaboration state
- role
- trust context
- cognitive load
- current task
- time horizon
- editing vs browsing mode

The architecture should therefore avoid assuming that visualization preference is globally fixed.

A likely pattern is:

> visualization preference = descriptor + context signature

The exact structure of the context signature remains open.

---

# 12. Personalization vs Collective Defaults

## Personalization

Each agent should retain sovereignty over personal visualization choices.

This includes:

- visualizer selection
- property ordering
- hidden fields
- preferred expansions
- preferred layouts
- embedding preferences
- interaction density
- navigation preferences

These choices directly shape the local experience.

## Collective influence

At the same time:

> Personalization choices may contribute signals toward collective defaults.

This creates a feedback loop:

1. Individuals personalize views.
2. Personalizations generate salience and affinity metrics.
3. Metrics aggregate within a community context.
4. Shared defaults emerge.
5. Individuals may still override them locally.

This allows the system to evolve adaptive defaults without imposing rigid centralized behavior.

---

# 13. Sovereignty and Aggregation

## Important concern

Agents or spaces may not want raw interaction telemetry sent to a centralized stewarding space.

This is important for:

- sovereignty
- privacy
- autonomy
- cultural differentiation
- political independence
- trust

Therefore:

> Visualization aggregation should likely be community-scoped rather than globally centralized.

## Community-scoped aggregation

Instead of sending metrics to the stewarding space for a descriptor, usage aggregation may occur within:

- intentional communities
- bioregional spaces
- communities of practice
- organizational spaces
- affinity groups
- collaborative networks

This produces:

> community-adapted defaults rather than universal defaults.

This feels significantly more MAP-aligned than globally centralized UI optimization.

## Consequence

Different communities may evolve:

- different default visualizers
- different salience assumptions
- different relationship emphases
- different embedding conventions
- different navigation defaults
- different cognitive maps

without fragmenting the underlying ontology.

---

# 14. Relationship to Descriptor Usage

Visualization usage is related to descriptor usage, but they should remain distinct.

Descriptor usage concerns:

- schema interaction
- retrieval behavior
- hydration behavior
- traversal behavior
- runtime optimization

Visualization usage concerns:

- perception
- cognition
- salience
- layout
- interaction
- presentation
- embedding
- navigation experience

The two systems may inform each other, but they are not the same.

For example:

- frequently traversed relationships may suggest visualization affinity
- frequently displayed properties may influence prefetch policy
- visualization salience may inform retrieval salience
- retrieval metrics may inform adaptive rendering

But the conceptual separation remains useful.

---

# 15. Possible Architectural Layers

## Layer 1 — Personal Visualization State

Local durable preferences:

- visualizer choices
- layout choices
- hidden/revealed state
- ordering
- embedding choices

## Layer 2 — Visualization Usage Metrics

Behavioral telemetry:

- salience
- affinity
- traversal patterns
- interaction patterns
- co-visualization patterns

## Layer 3 — Community Aggregation

Community-level adaptation:

- shared defaults
- common layouts
- common embeddings
- common expansions
- common navigation patterns

## Layer 4 — Adaptive Visualization Engine

Runtime adaptation:

- predictive expansion
- contextual rendering
- progressive disclosure
- adaptive dashboards
- recommendation systems
- personalized defaults

---

# 16. Conceptual Framing

The deeper pattern emerging here is:

> Visualization is not merely presentation.  
> Visualization behavior is a form of collective sensemaking.

Or:

> Salience is expressed through interaction.

Or:

> Repeated visualization gestures become votes about meaning.

Or:

> Personalization becomes collective adaptation without sacrificing sovereignty.

This gives MAP and DAHN a path toward:

- deeply adaptive interfaces
- context-aware rendering
- sovereignty-preserving personalization
- community-shaped defaults
- semantically meaningful interaction metrics
- evolving cognitive landscapes
- participatory interface evolution

without collapsing into centralized behavioral optimization.
