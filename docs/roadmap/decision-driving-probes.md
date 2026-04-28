# Decision-Driving Probes (DDPs)

## What is a DDP?

A **Decision-Driving Probe (DDP)** is a tightly scoped, time-bounded investigation designed to **reduce critical architectural uncertainty**.

A DDP is not about building features.  
It is about **testing key assumptions before they become irreversible decisions**.

A good DDP answers questions like:

- “Can this actually work within our constraints?”
- “What must be true for this approach to succeed?”
- “Where will this break if we proceed?”

---

## What a DDP *Is*

- **Focused** — targets a single architectural unknown
- **Bounded** — explicit scope and frozen dependencies
- **Falsifiable** — has clear failure conditions
- **Constraint-producing** — yields requirements, not implementations
- **Disposable** — outputs insight, not production code

---

## What a DDP *Is Not*

- Not feature development
- Not speculative architecture design
- Not open-ended exploration
- Not a prototype intended for reuse
- Not dependent on unstable or undefined subsystems

If a DDP starts producing reusable systems, it has likely gone too far.

---

## The 3-Stage DDP Pattern (Gated)

DDPs are executed as a **three-stage sequence**, where each stage must complete before the next begins.

---

### Stage 1 — Scenario & Constraint Definition

**Goal:** Stabilize the problem before considering solutions.

Define:
- 3–5 **concrete scenarios** the system must support
- Derived **non-negotiable constraints**
- **Nice-to-have constraints**
- Explicit **non-requirements** (what is out of scope)

**Output:**
> A clear statement of what any viable solution must satisfy

---

### Stage 2 — Candidate Identification & Selection

**Goal:** Identify possible approaches, then select only a few to test.

Steps:
- Identify a **broad set of candidate approaches**
- Evaluate them against Stage 1 constraints
- Select **2–3 candidates** for deeper probing

**Output:**
- Candidate list
- Selection rationale
- Explicit exclusions

---

### Stage 3 — Probe Execution

**Goal:** Test selected candidates against the defined scenarios.

Approach:
- Simulate or minimally implement only what is needed
- Walk each candidate through the Stage 1 scenarios
- Identify:
    - where it succeeds
    - where it fails
    - what constraints it violates

**Output:**
- Capability comparison
- Failure modes
- Required invariants
- Clear viability assessment

---

## Key Guardrails

- **Freeze dependencies** before starting (e.g., no reliance on Agreements if undefined)
- **Do not design forward** — extract constraints, don’t build systems
- **Stop at insight** — avoid implementation drift
- **Keep scope small** — 1–2 weeks max

---

## Candidate DDP Topic Areas

The following areas represent major unresolved design questions in the MAP roadmap:

---

### 1. Dynamic Dance Loading & Dispatch
How Dancer behavior is brought into and executed within a local Integration Hub.

---

### 2. Visualizer Loading & Dispatch (Trust-Channel Mediated)
How visualizers are dynamically loaded and governed under trust constraints.

---

### 3. Trust Channel Implementation
Where and how enforcement occurs at membrane boundaries for inbound/outbound flows.

---

### 4. Update Propagation, Semantic Versioning & Merging
How holons evolve, diverge across spaces, and reconcile over time.

---

### 5. Multi-Space Holon Resolution
How holon identity and representation are resolved across multiple spaces.

---

## Strategic Use

DDPs are best applied where:

- The cost of being wrong is high
- The design space is unclear
- Premature commitment would create deep rework

They are especially valuable for **cross-cutting concerns** that affect multiple subsystems.

---

## Bottom Line

DDPs are a way to:

> **Discover the constraints of the system before committing to its design**

Used well, they:
- reduce architectural risk
- prevent premature decisions
- focus effort where it matters most

Used poorly, they become:
- unfocused exploration
- speculative prototyping
- wasted effort

The difference is discipline in scope, framing, and execution.