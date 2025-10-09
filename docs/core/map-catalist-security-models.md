# Proposal: Migrating from Catalist’s Fine-Grained Security to MAP’s Group-Oriented Model

## 1. Core Dimensions of Security

Both Catalist and MAP need to address the same underlying dimensions:
- **Who** (agents/people/groups)
- **What Data** (holons, attributes, views) 
- **What Actions** (verbs/Dances)
- **Entitlements vs. Permissions** (purchased rights vs. delegated rights)

Catalist encodes these as fine-grained decisions at the level of individuals and attributes. MAP lifts them into higher-order groupings:

| Dimension        | Catalist (fine-grain)          | MAP (group-oriented)                       |
|------------------|--------------------------------|--------------------------------------------|
| **Who**          | Each person has direct grants  | People belong to **Groups**                |
| **Actions**      | Each verb toggled per person   | Actions grouped into **Roles**             |
| **Entitlements** | Tied to specific individuals   | Entitled actions bundled into **Products** |
| **Data**         | Attributes assigned per person | Attributes bundled into **Views**          |

---

## 2. Simplifying the Decision Surface

Instead of N×M×K×L micro-decisions (people × attributes × actions × contexts), MAP collapses the surface area:

- **Grant = (Group, Role, View)**
    - *Which group has which role over which view?*
- **Entitlements = (Product → Role associations)**
    - *Purchasing a product expands the action set for associated roles.*

This makes permissioning a **macro-level governance decision** rather than an endless stream of micro-decisions.

---

## 3. Change Management and Migration Path

- **Step 1: Define canonical Groups, Roles, Products, Views**  
  Translate existing Catalist entitlements/permissions into these higher-order bundles.
- **Step 2: Map existing fine-grained grants into group memberships**  
  (e.g., “Frank has access to X, Y, Z” → Frank is in Group A, which carries Role B over View C).
- **Step 3: Retire individual grants in favor of group membership operations**  
  Adding/removing people from groups now handles churn events (onboarding, offboarding, role shifts).

---

## 4. Alignment with MAP Security Model

This approach fits cleanly with MAP’s core security principles:

- **Membrane-based boundaries** — Groups correspond to AgentSpace membranes 
- **Consent-based access** — Views and Products are exposed only via explicit Agreements 
- **Sovereign custody** — All data lives in private Data Groves, shared only through Information Access Agreements 
- **Role-based actions** — Roles map directly to permitted Dances within the Uniform API 

---

## 5. Benefits

- **Reduces cognitive load** for administrators and members.
- **Improves resilience** by making permissions more transparent and auditable.
- **Supports migration**: existing fine-grained Catalist grants can be bulk-mapped into initial groups/roles/views without losing fidelity.
- **Future-proof**: easily maps into MAP’s holistic model of Promises, Agreements, and Vital Capital flows 

```mermaid
flowchart LR
  subgraph Inputs[Normalized Inputs]
    SM[SpaceMembership (user ∈ Group@Space)]
    RP[RolePolicy (Group → can_*)]
    PUB[Publish/Unpublish (Thing ↔ Space)]
    OWN[Home Transfer]
    ENT[Entitlement (Plan@Space)]
    ASG[EntitlementAssignment (seat)]
    PF[Plan/Feature/Action mapping]
    TREF[ThingEntitlementRef (Thing ↔ Entitlement)]
    AS[Audience Set (Space:is_audience_set)]
  end

  subgraph Compiler[Backend "Compiler" Workflows]
    P1[Recompute eff_perm_* for impacted Things]
    E1[Recompute eff_ent_* for impacted Things]
    I1[(Optional) Write eff_allowed_* = ∩]
  end

  subgraph Outputs[Thing Runtime Lists]
    EPV[eff_perm_view]
    EPA[eff_perm_annotate]
    EPE[eff_perm_edit]
    EPM[eff_perm_manage]
    EEV[eff_ent_view]
    EEA[eff_ent_annotate]
    EEE[eff_ent_edit]
    EAL[(optional) eff_allowed_*]
  end

  SM --> P1
  RP --> P1
  PUB --> P1
  OWN --> P1
  ENT --> E1
  ASG --> E1
  PF --> E1
  TREF --> E1
  AS --> P1

  P1 --> EPV & EPA & EPE & EPM
  E1 --> EEV & EEA & EEE
  I1 --> EAL

  style EPM fill:#ffd8bf,stroke:#c44,color:#222
  style AS fill:#eef,stroke:#88a,color:#222
```
 