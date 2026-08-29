# DAHN Space Navigator — Initial Design Concept

## Overview

The **Space Navigator** is an initial DAHN Canvas for exploring a MAP Space through its holons, relationships, properties, and dances.

Its purpose is not simply to display individual holons. It provides a spatial navigation model in which users can progressively explore the structure of a Space while preserving the context and provenance of how they arrived at each holon.

The design is built primarily from two reusable visual primitives:

- **Node Visualizer** — visualizes a single holon.
- **Collection Visualizer** — visualizes a homogeneous multi-valued collection.

The choice of visual treatment is based on the semantics declared by descriptors, especially cardinality and result shape, rather than on the number of values that happen to exist at runtime.

---

## Core Principle: Structure Comes From Definitions

DAHN should determine the structural presentation of an affordance from its descriptor.

For relationships, the relationship descriptor declares cardinality.

Therefore:

- A relationship whose maximum cardinality is `1` is structurally single-valued.
- A relationship whose maximum cardinality is `many` is structurally multi-valued.

This remains true regardless of current population.

For example:

- A many-valued relationship with zero targets is still presented as a collection affordance.
- A many-valued relationship with one target is still presented as a collection affordance.
- A single-valued relationship with no current target is still structurally a single-valued affordance.

The same principle applies to dances.

Dances are themselves holons, and their responses are described. DAHN can therefore determine the shape and cardinality of a dance result from the dance definition before the dance is invoked.

The visual structure of the Node Visualizer can consequently be derived substantially from the effective descriptors before any values or relationship targets are retrieved.

Runtime data populates that structure; it does not determine the structure.

---

# Collection Visualizer

## Purpose

The **Collection Visualizer** renders any homogeneous multi-valued result.

The initial implementation can be a table.

The Collection Visualizer is deliberately independent of the provenance of the collection. The same visualizer can be used for:

1. a value-array property;
2. the targets of a multi-valued relationship;
3. a multi-valued dance result.

The important semantic fact is that all three are homogeneous collections.

## Initial Table Representation

The table would contain:

- one row per collection element;
- one column per exposed property for collections of holons;
- column headings;
- filtering and sorting affordances associated with columns;
- an overarching collection header containing information and actions pertaining to the collection as a whole.

For a homogeneous array of scalar values, the Collection Visualizer would ordinarily contain a single value column whose type is the array's declared value type.

For a collection of holons, each row represents one holon and the columns represent properties exposed for that collection.

## Collection Visualizer as an Abstraction

The Collection Visualizer should not be equated permanently with a table.

A table is simply the first concrete collection visualization.

Other Collection Visualizers might later include:

- cards;
- graph views;
- timelines;
- maps;
- galleries;
- domain-specific visualizations.

This establishes a general DAHN principle:

> Result shape determines the applicable class of visualizer; provenance does not.

---

# Node Visualizer

## Purpose

The **Node Visualizer** renders a single holon together with the affordances available from that holon.

It acts as the primary unit of exploration within the Space Navigator.

A Node Visualizer consists conceptually of several regions.

---

## Title Bar

The title bar identifies the holon being viewed and may provide relevant contextual information.

Its purpose is to preserve clear identity as multiple Node Visualizers accumulate on the Canvas.

---

## Action Bar

The Action Bar exposes the dances currently available to the user for the displayed holon.

These are the **effective available dances**, including:

- dances defined directly by the holon's type;
- inherited dances;
- only those dances currently permitted to the user based on role, authorization, or other applicable policy.

The Action Bar may initially use buttons, menus, or a combination of the two.

---

## Main Viewing Pane

The main viewing pane presents the scalar and single-valued aspects of the holon.

This includes scalar properties displayed as name/value pairs.

Conceptually, this is the part of the visualizer concerned with things that resolve to a single value or single target rather than a collection.

Single-valued relationships and single-valued dance results may therefore also be represented in or adjacent to this pane.

---

# Single-Valued Affordances

## Single-Valued Relationships

A relationship whose descriptor declares maximum cardinality `1` is presented as a single-valued navigation affordance.

Selecting that relationship can open a sidebar to the right of the current Node Visualizer.

That sidebar contains another Node Visualizer for the relationship target.

The original holon remains visible and retains its context.

## Single-Valued Dance Results

A dance whose response descriptor indicates a single holon result can use the same visual treatment.

After invocation, its result can be shown in a Node Visualizer opening to the right.

Although relationships and dance results have different lifecycles, they converge on the same visual navigation grammar once their result shape is known.

---

# Multi-Valued Affordances

The lower portion of the Node Visualizer contains a set of tabs representing the holon's multi-valued affordances.

A tab may represent:

- a value-array property;
- a multi-valued relationship;
- a multi-valued dance result.

Selecting a tab opens the corresponding Collection Visualizer beneath the Node Visualizer.

This lets the user inspect a collection without losing the current holon as context.

The currently selected holon therefore remains the semantic focus while its plural affordances can be explored immediately beneath it.

---

# Spatial Navigation Model

The Space Navigator uses two spatial dimensions to encode two fundamentally different kinds of navigation.

## Horizontal Navigation: Follow One

Single-valued navigation extends the Canvas horizontally.

If the user follows:

- a single-valued relationship; or
- a single-valued dance result,

the resulting Node Visualizer opens to the right.

That Node Visualizer can itself expose further single-valued relationships or results, allowing navigation to continue horizontally.

It can also expose collections, permitting a subsequent vertical traversal.

Conceptually:

    Holon A  ->  Holon B  ->  Holon C

The horizontal dimension therefore represents traversal where there is one semantic target to follow.

---

## Vertical Navigation: Choose Among Many

Multi-valued navigation extends the Canvas vertically.

The user first opens a collection tab.

That exposes the Collection Visualizer beneath the current Node Visualizer.

Each row in the collection represents an available element.

Double-clicking a row selects one of those elements for deeper inspection.

A new Node Visualizer is then opened beneath the Collection Visualizer.

Conceptually:

    Holon A
       |
       +-- Collection
              |
              +-- Selected Holon B

The vertical dimension therefore represents navigation that involves choosing an element from a plurality.

---

# Navigation Invariant

This produces a simple spatial grammar:

> **Single-valued traversal extends horizontally.**

> **Multi-valued traversal extends vertically through a Collection Visualizer.**

The geometry of the Canvas therefore communicates semantic structure.

Horizontal motion means:

> Follow this one thing.

Vertical motion means:

> Explore these many things, then choose one.

This convention is grounded in MAP cardinality semantics rather than being an arbitrary layout choice.

---

# Recursive Exploration

Every Node Visualizer is itself fully navigable.

A Node Visualizer reached horizontally can:

- open another Node Visualizer to its right through a single-valued affordance;
- expose one of its collections beneath itself;
- descend through that collection into another Node Visualizer.

Similarly, a Node Visualizer reached vertically can continue either horizontally or vertically.

The result is a potentially two-dimensional exploration path through the Space.

For example:

    Space
      |
      +-- Types
             |
             +-- Person Type  ->  Schema
                    |
                    +-- Properties
                           |
                           +-- first_name  ->  Value Type

Every holon shown in this structure is an active Node Visualizer rather than merely a breadcrumb or diagram node.

Every collection through which the user navigated can remain an active Collection Visualizer.

---

# Preserving Context and Provenance

A central objective of the Space Navigator is to avoid conventional page-replacement navigation.

Navigating to another holon should not erase the context from which the user arrived.

Instead, prior Node Visualizers and Collection Visualizers remain on the Canvas.

This creates a persistent spatial representation of the traversal path.

The Canvas therefore preserves not just:

> I came from Holon A.

It can preserve:

> I came from Holon A through its Properties collection, selected this row, and arrived at Holon B.

That is much richer provenance than a conventional breadcrumb trail.

---

# Collapsing Prior Context

Persistent traversal can consume substantial screen space, so Node Visualizers need a lightweight collapsed state.

A prior Node Visualizer can collapse into a compact bar while remaining part of the Canvas.

This bar preserves:

- the identity of the holon;
- its position in the traversal path;
- the ability to restore or revisit that context.

Collapsing is therefore not merely a layout optimization.

It is a navigation primitive.

A collapsed node remains a durable marker of provenance.

The user can expand it again and potentially choose a different branch without reconstructing the earlier path.

---

# Partial Collapse During Collection Exploration

When a user opens a collection and begins inspecting rows, it may not be desirable to collapse the originating Node Visualizer completely.

A useful intermediate behavior would be to collapse the larger property and sidebar areas while preserving:

- the originating holon's compact identity;
- the selected collection tab;
- the Collection Visualizer itself.

This permits the user to move quickly among different rows of the collection.

For example, the user could double-click one row, inspect its holon, then double-click another row without having to navigate backward or reopen the collection.

The collection remains the immediate exploration context.

---

# Effective Visual Structure

A Node Visualizer can therefore be thought of roughly as:

    +------------------------------------------------------+
    | TITLE BAR                                            |
    +------------------------------------------------------+
    | ACTION BAR                                           |
    +------------------------------------------+-----------+
    |                                          |           |
    | MAIN VIEWING PANE                        | RIGHT     |
    |                                          | SIDEBAR   |
    | scalar property        value             |           |
    | scalar property        value             | Node      |
    |                                          | Visualizer|
    | single relationship    ->                |           |
    | single dance result    ->                |           |
    |                                          |           |
    +------------------------------------------+-----------+
    | [Array] [Relationship] [Dance Result] ...            |
    +------------------------------------------------------+
    | COLLECTION VISUALIZER                                |
    |                                                      |
    | Collection header                                    |
    |                                                      |
    | Column A        Column B        Column C              |
    | ---------------------------------------------------  |
    | row             row             row                   |
    | row             row             row                   |
    |                                                      |
    +------------------------------------------------------+

A selected row may then introduce another Node Visualizer beneath this structure.

---

# Visual Grammar

The initial Space Navigator can be understood in terms of a small visual grammar.

| Semantic Shape | Initial Presentation |
| --- | --- |
| Scalar property | Name/value field |
| Value array | Collection tab + Collection Visualizer |
| Single-valued relationship | Single-target affordance + right-side Node Visualizer |
| Multi-valued relationship | Collection tab + Collection Visualizer |
| Single-holon dance result | Right-side Node Visualizer |
| Holon-collection dance result | Collection tab + Collection Visualizer |

The visual treatment is determined primarily by declared result shape and cardinality.

---

# Architectural Implication

The effective descriptor of a holon tells DAHN what affordances exist.

Those descriptors provide sufficient structural information to determine much of the Node Visualizer before runtime data is retrieved.

In simplified form:

    Effective descriptor
        |
        +-- scalar properties
        |      -> fields
        |
        +-- value arrays
        |      -> collection tabs
        |
        +-- max-cardinality-1 relationships
        |      -> horizontal navigation affordances
        |
        +-- max-cardinality-many relationships
        |      -> collection tabs
        |
        +-- dances
               |
               +-- single-valued response
               |      -> horizontal result presentation
               |
               +-- multi-valued response
                      -> collection result presentation

This creates a generic visualization system capable of presenting previously unknown holon types without requiring domain-specific screens.

---

# Space Navigator as a DAHN Canvas

The **Space Navigator** is the Canvas that composes these visualizers into an interactive exploration environment.

It should remain conceptually distinct from DAHN itself.

DAHN may eventually support many different Canvases optimized for different modes of interaction.

The Space Navigator is one opinionated Canvas whose primary purpose is:

> To provide a persistent, spatial, descriptor-driven way to navigate a MAP Space through its holons and their affordances.

Its defining characteristics are:

- descriptor-driven structure;
- reusable Node and Collection Visualizers;
- horizontal traversal for singular references;
- vertical traversal for plural collections;
- recursive exploration in both dimensions;
- persistent spatial context;
- collapsible prior states;
- preservation of traversal provenance.

The result is not simply a browser for holons.

It is a spatial representation of the user's evolving path through a Space.