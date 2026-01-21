# Agent, I-Space, and Computing Node Onboarding

This document describes the technical process by which a new user onboards into the Memetic Activation Platform (MAP), with emphasis on the relationship between **I-Space**, **computing nodes**, **agents**, and the identity/authority structures binding them together.

---

## 1. Key Concepts

### I-Space
- An **I-Space** is a user’s personal agent-space within Planetary Space.
- It is a **Holochain agent space** (flattened inheritance: `I-Space ⊂ Holochain Space`).
- Conceptually represents the user’s:
    - **Personal computing cloud**
    - **Personal data cloud**
    - **Core identity**
- Acts as the parent membrane for all of the user’s sub-agents (e.g. computing devices).

### Computing Node
- A **computing node** is a user’s device (laptop, desktop, tablet, etc.) running the MAP software.
- Each computing node is instantiated as a **Holochain agent** within the user’s I-Space.
- Provisioned with applications (“the Gift” = Nine core apps).
- Executes MAP applications and participates in the user’s **personal services layer**.

### Sovereign Data Sphere
- The user’s **personal data cloud**, formed by the aggregation of application-specific DHTs.
- Conceptualized as a concentric layer surrounding core identity in the I-Space diagram.
- Data is distributed across the user’s computing nodes.

### Core Identity
- The user’s personal identity within Planetary Space.
- Materialized via a cryptographic keypair (or complement of keypairs) created at onboarding.
- Distributed across the user’s computing nodes, but logically represented as a singular identity.

---

## 2. Onboarding Flow

### Step 1. Invitation & Gift
- User downloads MAP (free, open-source software).
- On first run, the MAP presents the user with an **invitation to join Planetary Space**.
- The “gift” is disclosed gradually:
    1. Free installation.
    2. Presentation of invitation.
    3. Acceptance generates I-Space and identity.

### Step 2. Identity Creation
- Upon acceptance:
    - The MAP requests Holochain to generate:
        - A **core identity keypair** for the user.
        - A **sub-agent keypair** for the initial computing node.
- Result: both **user identity** and **computing node identity** are established in Planetary Space.

### Step 3. Sub-Agent Relationship
- The computing node is recorded as a **sub-agent of the user’s I-Space**.
- A **membership agreement** is created:
    - Grants the user full stewardship/admin privileges over the computing node.
    - Establishes mutual recognition (key exchange).
    - Agreement is inherently **mutual** (signed by both parties).

### Step 4. Activation
- The computing node is provisioned with the Nine core applications.
- Applications run **inside computing nodes**, not directly in the I-Space.
- The I-Space view displays:
    - Core Identity (center).
    - Sovereign Data Sphere (personal cloud).
    - Sub-agents (computing nodes) around the ring.

---

## 3. Temporal Sequence: Protocol vs. Conceptual

There is a subtle but important distinction between how onboarding must occur at the **protocol level (Holochain mechanics)** versus how it is best understood at the **conceptual level (MAP narrative)**.

### Protocol Sequence (Holochain View)
1. **Compute node identity is generated first.**
    - A device cannot participate in a DHT without an agent keypair.
2. **I-Space (personal identity) is generated.**
    - A keypair is created for the human’s core identity.
3. **Agreement is recorded between the two.**
    - Membership establishes the compute node as a sub-agent of the I-Space.

### Conceptual Sequence (MAP View)
1. **I-Space exists first as the enclosing membrane.**
    - Represents the person’s personal cloud and identity.
2. **Computing node is ingested into the I-Space.**
    - The I-Space “absorbs” the node into its membrane, making it a sub-agent.
3. **Agreement is mutual but is understood as the I-Space granting stewardship authority to the person over the node.**

### Reconciliation
- **Protocol necessity:** Device keys come first (Holochain requirement).
- **Conceptual truth:** The I-Space envelops its computing nodes (MAP metaphor).
- **Documentation implication:** Both sequences are valid; developers must follow the protocol, storytellers should communicate the conceptual.

---

## 4. Open Questions

1. **Key Generation for Hardware**
    - How exactly are compute node identities derived?
    - Is device hardware entropy/identifier hashed into the keypair?
    - Best practice for bootstrapping Holochain agent keys to hardware?

2. **Sequential Dependencies**
    - Does Holochain strictly enforce “node-first then I-Space,” or can the appearance be reversed through orchestration?
    - What does this mean for cross-device identity joining?

---

## 5. Storytelling Alignment

For **non-technical onboarding presentations**:

- Start from the **user experience**:
    - Download gift → Accept invitation → Receive I-Space.
- Emphasize **simplicity**:
    - “Your personal cloud”
    - “Your devices become part of it”
- Reveal **computing nodes** and **applications** only as necessary.
- Avoid algebraic notation (letters like A, B, C) — use relatable examples (Laptop, Phone, Tablet).

---