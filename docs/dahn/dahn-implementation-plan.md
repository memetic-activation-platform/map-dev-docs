# **DAHN MVP Implementation Plan (TypeDescriptors-First)**
### *A pragmatic path to bringing the MAP’s human experience to life.*

This plan integrates the **TypeDescriptors-first approach** into the broader MVP roadmap,  
ensuring early visible results, architectural integrity, and rapid momentum.

Because **all MAP TypeDescriptors are themselves Holons**, this roadmap deliberately demonstrates universal holon rendering and editing early — using the Type System as the most structurally rich exemplar.

>NOTE: All timeframe estimates are preliminary, highly-speculative and ignore resource dependencies

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

## **1.5. Milestone Zero — Universal Holon Rendering (FIRST DEMO)**
*Demonstrated via the MAP Type System*

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

Because TypeDescriptors are Holons, this milestone proves that **DAHN can render any MAP Holon**, not just schemas.

**Outcome:**  
The MAP becomes *visible*.  
DAHN can render and navigate the living schema — and any other holon.

---

# ---------------------------------
# **PHASE 2 — Holon Editing (Universal, Minimal, Safe) (Weeks 7–10)**
### *From observation to participation.*

This phase introduces **editing of holons as holons**.  
TypeDescriptors are the first and most visible beneficiaries, not a special case.

---

## **2.1. Generic Holon Editing Infrastructure**
- Inline editing for scalar properties
- Validation via MAP type rules
- Save / revert / error feedback
- Trusted-space assumption (no permissions model yet)

Applies to:

- TypeDescriptors
- Agents
- MemePools
- Spaces
- Any editable MAP holon

---

## **2.2. Relationship Editing (Minimal v0)**
- Add relationship
- Remove relationship
- Choose target holon
- Cardinality enforcement

No graph refactoring UI yet — correctness first.

---

## **2.3. TypeDescriptor Editing (First-Class Demonstration)**
Supported edits:

- display_name
- description
- is_abstract_type
- instance_type_kind
- property order

This demonstrates that the MAP can **edit its own schema from within itself**.

---

## **2.4. Create New Holons (TypeDescriptors First)**
- Create a new TypeDescriptor holon
- Define properties + relationships
- New types render immediately
- No code changes required

**Demo:**  
Create `PublicationType` → DAHN renders it → edit it → navigate it.

**Outcome:**  
DAHN becomes participatory.  
The MAP is no longer just visible — it is *malleable*.

---

# ---------------------------------
# **PHASE 3 — Personalization (Salience + Affinity) + Theme Switching (Weeks 11–16)**
### *Now the system adapts to the person.*

---

## **3.1. Salience Gestures**
- Drag-to-reorder fields in Property Sheet
- Persist personal salience preferences
- Reorder fields accordingly

## **3.2. Affinity Gestures**
- Person selects alternate visualizer
- DAHN records personal affinity
- Applies personal affinities on load

## **3.3. Selector Function v1**
- Combines static defaults + personal preferences
- Uses salience and affinity for selection
- Still no community aggregation

## **3.4. Theme Switching**
- Add multiple themes (4–6)
- Person chooses preferred theme
- Applied globally across Canvas + Visualizers
- Preferences persisted

**Demo:**  
A DAHN that remembers not just what exists — but how *you* engage with it.

---

# ---------------------------------
# **PHASE 4 — Visualizer Commons + Community Signals (Weeks 16–22)**
### *DAHN opens to the ecosystem.*

---

## **4.1. Visualizer Commons v0**
- Directory + loader for external visualizers
- Web Component starter kit
- Developer guide: “Build a DAHN visualizer in 20 minutes”

**Demo:**  
Load first external visualizer (e.g., card-based TypeDescriptor viewer).

---

## **4.2. Selector Function v2 (Community-aware stub)**
- Accepts community affinity/salience data (static for now)
- Demonstrates shifting defaults

**Outcome:**  
DAHN becomes extensible and begins to feel alive.

---

# ---------------------------------
# **PHASE 5 — Canvas Evolution + Adaptive Controls (Weeks 22–30)**
### *DAHN becomes multi-modal, more expressive, and more adaptive.*

---

## **5.1. Enhanced 2D Canvas**
- Multi-panel layout
- Breadcrumb navigation
- Split view
- Improved responsiveness
- Simple animations

## **5.2. Additional Canvases**
- Navigation-focused Canvas
- Card-centric Canvas
- “Reading Mode” Canvas
- (Optional) Spatial Canvas prototype

Different canvases unlock different experiential modalities.

---

## **5.3. Adaptive Controls (Explore ↔ Exploit)**
Introduce sliders that tune DAHN’s behavior:

- Personal vs. Collective weighting
- Trending vs. All-time
- Mature vs. Experimental visualizers
- Randomness tolerance

---

## **5.4. Selector Function v3 (Adaptive)**
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
# **PHASE 6 — DAHN Alpha Release**
### *The experience layer of the MAP is fully alive.*

DAHN now supports:

- rendering **any** holon
- viewing and editing **any** MAP holon (including the schema itself)
- exploring the **full Type System**
- holon creation
- multiple canvases
- theming
- personalization
- adaptive selection
- contributed visualizers
- multi-device operation
- full MAP navigation
- executing dances

**Alpha Demo — Walk the MAP:**

1. Open your Agent holon
2. Explore your LifeCode
3. Navigate We-Spaces
4. View relational flows
5. Switch canvases
6. Switch visualizers
7. Edit a holon
8. Personalize fields
9. Invoke a dance
10. Observe adaptive selection
11. Return to TypeDescriptors and evolve the schema from within the experience

This is the moment the MAP becomes **visible**, **navigable**, **malleable**, and **alive**.

---

# ---------------------------------
# **PHASE 7 — Localization + Accessibility + Device Variants (Weeks 30–40)**
### *Make DAHN globally inclusive and widely usable.*

---

## **7.1. Localization Foundations**
- Translation files
- Locale-aware formatting
- Right-to-left (RTL) Canvas variant

## **7.2. Accessibility Foundations**
- Semantic roles for all visualizers
- Keyboard-only navigation
- Screen reader compatibility
- High-contrast theme
- Reduced-motion mode

## **7.3. Mobile / Tablet Optimization**
- Touch gestures for salience
- Contextual action menus
- Compact layout profiles

**Outcome:**  
DAHN becomes globally viable.

---

# ---------------------------------
# **Guiding Principles Throughout**

1. **Minimum complexity, maximum leverage**
2. **Framework-free visualizers (Web Components only)**
3. **Everything is a holon; everything comes through the Uniform API**
4. **Participation before personalization**
5. **Personal coherence before app coherence**
6. **Ecosystem extensibility from day one**
7. **Declarative semantics → dynamic experience**

---

# **In Summary**

The DAHN MVP roadmap delivers:

- the first dynamic semantic UI engine
- the first visual MAP experience
- universal holon rendering and editing
- a self-hosting, self-evolving schema
- a community-extensible visualizer ecosystem
- adaptive, person-centric intelligence
- a living interface for a living civilization

This is the path to a DAHN that works, grows, adapts, and inspires —  
the path to finally **walking the MAP**.