# **Dynamic Experience Composition in the Semantic Experience Architecture (SEA)**
### *How DAHN Generates Coherent Experience at Runtime*

DAHN (Dynamic, Adaptive, Holon Navigator) is the experience engine of the MAP.  
Its essential task is to generate human experience **dynamically** and **adaptively**—  
not from pre-designed screens, but from **meaning**, **context**, and **personal preference**.

This is not a conventional UI problem.  
It is a *meta-interface* problem:  
the orchestration of micro-design decisions that HX designers normally make **before** software ships.

In SEA, those decisions are made **at runtime**.

---

# **I. The Core Challenge: Runtime Experience Composition**

DAHN must generate coherent experience using four classes of unknowns:

1. **Unknown holons**  
   New types, new properties, new relationships, new behaviors—introduced continuously by MAP participants.

2. **Unknown behaviors**  
   Holons may expose new dances and new affordances the system has never seen before.

3. **Unknown visualizers**  
   The Visualizer Commons is open-ended: anyone may contribute new representations.

4. **Unknown personal and collective preferences**  
   People express preferences through natural gestures—dragging, reordering, choosing visualizers—and DAHN learns from these.

Conventional apps hardcode choices like layout, grouping, and affordances.  
DAHN must **infer** them at runtime.

---

# **II. DAHN Architecture 2.0 (High-Level)**

~~~
          ┌────────────────────────────────────────────────────────┐
          │                     Human Person                        │
          └────────────────────────────────────────────────────────┘
                               ▲             ▲
                               │  Preferences│  Themes
                               │             │
     ┌─────────────────────────┴───────┬─────┴───────────────────────────┐
     │                         DAHN Runtime                               │
     │     (Dynamic Experience Composition Engine of the MAP)             │
     └─────────────────────────┬───────┴───────────────────────────┬─────┘
                               │                                   │
                               ▼                                   ▼
                ┌──────────────────────────┐       ┌──────────────────────────┐
                │          Canvas          │       │     Selector Function     │
                │   (Experience Space)     │       │ (Chooses Visualizers &    │
                │                          │       │  Embedding Strategies)     │
                └──────────────────────────┘       └──────────────────────────┘
                               │                                   ▲
                               │                                   │
                               ▼                                   │
                ┌──────────────────────────┐       │  Inputs:                
                │  Meta Design System      │       │   • holon type        
                │    (Semantic Roles)      │       │   • device/context      
                └──────────────────────────┘       │   • salience/affinity        
                               │                   │   • collective trends
                               │                   │   • visualizer availability
                               ▼                   │
                ┌──────────────────────────┐       │
                │          Themes          │       │
                │   (Personal Look & Feel) │       │
                └──────────────────────────┘       │
                               │                   │
                               ▼                   │
                ┌──────────────────────────┐       │
                │       Visualizers        │◄──────┘
                │   (Pluggable UI Modules) │
                └──────────────────────────┘
                               ▲
                               │
                               ▼
                ┌──────────────────────────┐
                │      MAP Uniform API     │
                │   (Holon Access Layer)   │
                └──────────────────────────┘
                               ▲
                               │
                               ▼
                ┌──────────────────────────┐
                │          Holons          │
                │   (Meaning & Behavior)   │
                └──────────────────────────┘

~~~

---

# **III. The Three Anchors of SEA**

## **1. The Meta Design System (MDS)**
A semantic grammar describing roles like PrimaryAction, BodyText, Surface, Emphasis, and Flow.  
All visualizers bind to these shared roles, ensuring coherence across modalities.

## **2. The Canvas**
The experiential container that handles layout, density, device adaptation, visualizer mounting, and interaction semantics.

## **3. Visualizers**
Pluggable UI modules (framework-free Web Components) contributed by the community; each expresses holons in its own representational style.

Together, these provide **meaning → composition → expression**.

---

# **IV. Affinity and Salience: How DAHN Learns**

DAHN learns from interaction.  
People shape their experience through natural gestures—dragging, expanding, choosing, navigating.  
DAHN interprets these gestures in terms of two universal signals:

### **Salience**
“How important is this *to me*?”  
Affects ordering, visibility, expansion, and density.

### **Affinity**
“How closely do these things belong together?”  
DAHN tracks three types:

1. **Preference Affinity** – choosing among alternatives (e.g., visualizers, themes).
2. **Cohesion Affinity** – grouping elements that naturally belong together (e.g., Undo/Redo, address fields).
3. **Semantic Affinity** – the strength of a relationship between holons (e.g., embed vs. navigate).

Affinity is **not stored in RelationshipDescriptors**.  
It *references* them, allowing personal, space-level, and system-wide variation.

---

# **V. Embedding vs. Navigation: Semantic Affinity in Action**

Every holon is simple—scalar properties with no nested structure.  
Complexity emerges from relationships.

DAHN uses **semantic affinity** to decide:

- Should one holon be **embedded** inside another?
- Should it appear as a **collapsible section**?
- Should it be shown as an **inline preview**?
- Should it require **navigating** to a separate view?

RelationshipDescriptors define semantics.  
Affinity defines *contextual weight*, allowing different communities and individuals to develop different structural expectations.

---

# **VI. The Selector Function: DAHN’s Adaptive Intelligence**

The selector function chooses **how** to express a holon:

- which visualizer to use
- whether to embed or navigate
- which visual grouping to use
- how personal and collective preferences should be weighted
- whether stability or novelty is preferred

It uses:

- device characteristics
- Canvas layout
- personal salience and affinity
- collective preference patterns
- trending or all-time popularity
- visualizer maturity
- randomness (when desired)
- semantic meaning from holon descriptors

This function enables DAHN to  
**adapt to the person, the holon, the moment, and the community.**

---

# **VII. Adaptive Controls (Explore vs. Exploit)**

People differ in their desire for predictability or novelty.  
DAHN optionally exposes controls that allow a person to tune:

- **Personal vs. collective weighting**
- **Trending vs. all-time patterns**
- **Maturity vs. cutting-edge visualizers**
- **Randomness in selection**

![img.png](../media/adaptive-controls.png)


These sliders express the person’s mode:

- **Exploit mode:** “Be predictable, stable, efficient.”
- **Explore mode:** “Show me what’s new, trending, emerging.”

Defaults may be driven by collective behavior,  
but personal preferences always take precedence.

---

# **VIII. The Role of the Canvas in Adaptation**

The Canvas is where adaptivity becomes visible. It:

- adjusts layout across form factors
- manages density based on available space
- clusters high-affinity elements
- handles expansion/collapse behavior
- applies embedding rules
- propagates themes
- integrates selector decisions into a coherent visual flow

The Canvas establishes **coherence that follows the person**,  
not the app.

---

# **IX. Why DAHN Is Novel**

DAHN is the first system that:

- generates experience directly from holon semantics
- adapts continuously to personal and collective preferences
- learns through natural gestures
- separates semantic grammar (MDS) from experience composition (Canvas)
- supports unlimited visual styles through Web Component visualizers
- treats UI as a **commons**, not a proprietary asset
- unifies experience across every MAP application and holon
- composes experience dynamically—never pre-baked
- evolves with the MAP as it evolves

This is why SEA is not a UI framework.  
It is a **meaning-driven, adaptive, generative interface architecture**.

---

# **X. Summary**

DAHN dynamically composes experience using:

- **meaning** (holons)
- **personality** (salience & affinity)
- **community** (aggregate patterns)
- **semantics** (MDS roles)
- **space** (Canvas)
- **expression** (visualizers)
- **adaptation** (selector function)

The result is an interface that:

- follows the person
- evolves with the community
- reflects semantic reality
- adapts across contexts
- remains coherent
- grows as the MAP grows

DAHN turns holonic meaning into lived human experience— not through predefined screens, but through **dynamic, adaptive, semantic composition**.