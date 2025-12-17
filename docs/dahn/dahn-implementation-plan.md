# **DAHN MVP Implementation Plan (TypeDescriptors-First)**
### *A pragmatic path to bringing the MAP’s human experience to life.*

This plan integrates the **TypeDescriptors-first approach** into the broader MVP roadmap,  
ensuring early visible results, architectural integrity, and rapid momentum.

---

# ---------------------------------
# **PHASE 0 — Foundational Runtime (Weeks 1–2)**
### *Lay the SEA substrate DAHN will run on.*

## **0.1. SEA Runtime Foundations**
- Implement the base semantic contract for visualizers
- Implement the Canvas abstraction (minimal API)
- Implement the Visualizer interface (framework-independent Web Components)
- Implement the Theme system (token-based)
- Implement Selector Function interface (stub only)

## **0.2. Uniform API Integration**
- MAP SDK access to holons
- Rust ↔ TypeScript serialization of holon references
- Read-only traversal of properties + relationships

## **0.3. Dynamic Loader**
- Runtime loading of Web Components
- Hot reload for development
- No frontend framework lock-in

**Outcome:**  
DAHN can load holons and render them using dynamically loaded components.

---

# ---------------------------------
# **PHASE 1 — Minimal Canvas, Minimal Theme, Initial Visualizers + TypeDescriptors (Weeks 3–6)**
### *Deliver the first full end-to-end experience loop using the MAP’s Type System itself.*

---

## **1.1. MVP Canvas: “DAHN-2D Minimal Canvas”**
Capabilities:
- Flow layout, scroll, basic panels
- Responsive design (mobile → desktop)
- Basic keyboard navigation
- Single container region for visualizers
- Theme attachment

Limitations:
- No complex docking or multi-pane layouts
- No transitions or animations
- No multi-modal affordances

---

## **1.2. MVP Theme**
- Light + dark modes
- Working color palette
- Typography scale
- Spacing tokens
- Starter icon set

---

## **1.3. Three Core Visualizers**
These render **any holon**, including TypeDescriptors.

### **1.3.1. Property Sheet Visualizer**
- Displays scalar properties
- Basic formatting and layout
- Collapse/expand long values

### **1.3.2. Relationship List Visualizer**
- Groups relationships by type
- Navigation to related holons
- Count + compact preview

### **1.3.3. Action Menu Visualizer**
- Lists available dances
- Simple buttons

---

## **1.4. Selector Function (Static v0)**
- Hardcoded affinity
- Always selects MVP visualizers
- No salience or personalization yet

---

## **1.5. Milestone Zero — Render the Type System (FIRST DEMO)**
Using the Canvas, Theme, and Visualizers:

- Open **TypeDescriptor: HolonType**
- View its properties
- View its relationships
- Navigate to MetaHolonType
- Navigate to its PropertyDescriptors
- Navigate to ValueTypes
- Switch visualizers
- Switch themes
- Navigate to another TypeDescriptor

**Outcome:**  
The MAP becomes *visible*.  
DAHN can render and navigate the living schema.

---

# ---------------------------------
# **PHASE 2 — Personalization (Salience + Affinity) + Theme Switching (Weeks 7–12)**
### *Make DAHN adaptive and person-centric.*

## **2.1. Salience Gestures**
- Drag-to-reorder fields in Property Sheet
- Persist personal salience preferences
- Reorder fields accordingly

## **2.2. Affinity Gestures**
- Person selects alternate visualizer
- DAHN records personal affinity
- Applies personal affinities on load

## **2.3. Selector Function v1**
- Combines static defaults + personal preferences
- Uses salience and affinity for selection
- Still no community aggregation

## **2.4. Theme Switching**
- Add multiple themes (4–6)
- Person chooses preferred theme
- Applied globally across Canvas + Visualizers
- Preferences persisted

**Demo:**  
Personalized DAHN that remembers you.

---

# ---------------------------------
# **PHASE 3 — Schema Editing (TypeDescriptors) + Visualizer Commons (Weeks 12–18)**
### *DAHN becomes a self-evolving system and opens to external contributors.*

---

## **3.1. Edit TypeDescriptors**
### **Scalar edits:**
- display_name
- description
- is_abstract_type
- instance_type_kind

### **Property edits:**
- add property
- remove property
- change value type
- change cardinality
- reorder property definitions

### **Relationship edits:**
- add relationship
- remove relationship
- set cardinality
- set definitional flag
- choose target type

### **Extends**
- modify inheritance tree

---

## **3.2. Create New TypeDescriptors**
- Provide UI to create a new TypeDescriptor
- Add fields + relationships
- New types appear instantly in DAHN
- No code changes necessary

**Demo:**  
Define “PublicationType” → DAHN renders it automatically.

---

## **3.3. Visualizer Commons v0**
- Directory + loader for external visualizers
- Web Component starter kit
- Developer guide: “Build a DAHN visualizer in 20 minutes”

**Demo:**  
Load first external visualizer (e.g., card-based TypeDescriptor viewer).

---

## **3.4. Selector Function v2 (Community-aware stub)**
- Accepts community affinity/salience data (static for now)
- Demonstrates shifting defaults

**Outcome:**  
DAHN becomes extensible and begins to feel alive.

---

# ---------------------------------
# **PHASE 4 — Canvas Evolution + Adaptive Controls (Weeks 18–26)**
### *DAHN becomes multi-modal, more expressive, and more adaptive.*

---

## **4.1. Enhanced 2D Canvas**
- Multi-panel layout
- Breadcrumb navigation
- Split view
- Improved responsiveness
- Simple animations

## **4.2. Additional Canvases**
- Navigation-focused Canvas
- Card-centric Canvas
- “Reading Mode” Canvas
- (Optional) Spatial Canvas prototype

Different canvases unlock different experiential modalities.

---

## **4.3. Adaptive Controls (Explore ↔ Exploit)**
Introduce sliders that tune DAHN’s behavior:

- Personal vs. Collective weighting
- Trending vs. All-time
- Mature vs. Experimental visualizers
- Randomness tolerance

---

## **4.4. Selector Function v3 (Adaptive)**
Now considers:

- personal affinity
- aggregate affinity
- trending
- maturity
- randomness
- salience patterns

**Demo:**  
DAHN actively adapts to the person and the ecosystem.

---

# ---------------------------------
# **PHASE 5 — Localization + Accessibility + Device Variants (Weeks 26–36)**
### *Make DAHN globally inclusive and widely usable.*

---

## **5.1. Localization Foundations**
- Translation files
- Locale-aware formatting
- Right-to-left (RTL) Canvas variant

## **5.2. Accessibility Foundations**
- Semantic roles for all visualizers
- Keyboard-only navigation
- Screen reader compatibility
- High-contrast theme
- Reduced-motion mode

## **5.3. Mobile / Tablet Optimization**
- Touch gestures for salience
- Contextual action menus
- Compact layout profiles

**Outcome:**  
DAHN becomes globally viable.

---

# ---------------------------------
# **PHASE 6 — DAHN Alpha Release**
### *The experience layer of the MAP is fully alive.*

DAHN now supports:

- rendering **any** holon
- exploring the **full Type System**
- schema editing + creation
- multiple canvases
- theming
- personalization
- adaptive selection
- contributed visualizers
- accessibility & localization
- multi-device operation
- full MAP navigation
- executing dances

**Alpha Demo:**  
Walk an entire MAP journey:
1. Open your Agent holon
2. Explore your LifeCode
3. Navigate We-Spaces
4. View relational flows
5. Switch canvases
6. Switch visualizers
7. Personalize fields
8. Invoke a dance
9. Observe adaptive selection
10. Return to TypeDescriptors and evolve the schema itself

This is the moment the MAP becomes **visible**, **navigable**, and **alive**.

---

# ---------------------------------
# **Guiding Principles Throughout**

1. **Minimum complexity, maximum leverage.**
2. **Framework-free visualizers (Web Components only).**
3. **Everything is a holon; everything comes through the Uniform API.**
4. **Personal coherence before app coherence.**
5. **Ecosystem extensibility from day one.**
6. **Declarative semantics → dynamic experience.**

---

# **In Summary**

The DAHN MVP roadmap delivers:

- the first dynamic semantic UI engine
- the first visual MAP experience
- a self-hosting schema editor
- a community-extensible visualizer ecosystem
- the birth of a regenerative experience architecture
- global inclusivity
- adaptive intelligence
- a living interface for a living civilization

This is the path to a DAHN that works, grows, adapts, and inspires —  
the path to finally **walking the MAP**.