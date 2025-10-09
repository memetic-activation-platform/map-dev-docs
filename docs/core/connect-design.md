# MAP Connect Dashboards: Early Design Sketches

🚧 *Draft for discussion — not final. Intended to seed design conversations among MAP Core developers.*

---

## 1. Connect Dashboard (Offer-Centric)

The **primary dashboard** shows aggregate data on my Offers and inbound Offers.  
It surfaces both **state counts** and **actionable prompts**.

### Lifecycle Flow
- **Drafts** — Offers not yet placed in a Space (parked, not visible).
- **Active Offers** — visible in a Space, subdivided by matching state:
    - **Under-constrained** → too many matches; suggests *requirements to add*.
    - **Over-constrained** → too few/none; suggests *requirements to relax*.
    - **Waiting for My Responses** → unknowns I must answer.
    - **Waiting on Others** → unknowns others must answer.
    - **Healthy Fit** → matches in desired range but below Agreement threshold.
- **Agreement Phase** → matches ≥ Agreement Phase Threshold; ready to reveal identity and negotiate.
- **Agreed / Closed** → historical Offers (archived for reference).

### Dashboard Interactions
- **Click a header** (e.g. “Over-constrained”):
    - Reveals **Top 3 prompts** relevant to that state.
        - For “Over-constrained”: top 3 requirements to consider relaxing.
        - For “Waiting for My Responses”: top missing promises I’m asked to make.
- **Click a number** (e.g. “7 Over-constrained Offers”):
    - Opens a **Collection View** of Offer Cards in that state.
    - From there, I can drill into any card’s **Feedback Panel**.

---

## 2. Collection View

Displays a grid or list of **Offer Cards**.

**Offer Card Preview**
- Title & context (e.g. Service Offer, Join Offer, Space).
- Status chips: ✕ Mismatches | ? Unknowns | ◔ Possibles | ✅ Matches.
- Click → opens **Feedback Panel**.

---

## 3. Feedback Panel (Card Drill-Down)

When I drill into a specific Offer Card:

- **Status Strip**
    - Counts for ✕ mismatches, ? unknowns, ◔ possibles, ✅ matches.

- **Unlocking Promises (ranked)**
    - Promises I could make to unlock the most matches.
    - Each shows projected gain (e.g. “Add Value: Regeneration → +8 matches”).
    - Actions: *Answer*, *Learn More* (link to Meme Pool definition).

- **Blocking Requirements (ranked)**
    - Requirements I imposed that are over-constraining.
    - Each shows projected gain if relaxed (e.g. “Relax Age ≥ 18 to 16 → +3 matches”).
    - Actions: *Adjust / Relax*.

- **Next Actions**
    - Propose Agreement (if matches are in range).
    - Reveal Identity / Open Negotiation (Agreement Phase).
    - Withdraw Offer.

- **Notifications (Sense)**
    - Toggle: *“Notify me when this Offer reaches Agreement Phase / gains new matches / gets blocked.”*

---

## 4. Resonance Engine Dashboard (Promise-Centric)

A **complementary dashboard** for *sense-making into a Space*.  
Instead of Offers, it organizes around **Promises themselves**.

### What it surfaces
- **Top Resonant Promises** — promises most frequently included in offers in this space.
- **Aspirational Gaps** — promises often *required* in offers but rarely present in members’ LifeCodes.
- **Cultural Climate Heatmap** — % of members aligned with key promises (values, principles).
- **Growth Prompts** — promises I’m being nudged to consider adding to my LifeCode to unlock more connections.

### Why it matters
- Lets individuals **see where they resonate** with the culture of a space.
- Lets spaces **see where alignment is strong or thin**, and adapt over time.
- Complements the Offer-centric dashboard by showing the **memetic layer** of connection.

---

## 5. Design Notes

- **States** are mutually exclusive and clear: Draft → Active (with sub-status) → Agreement Phase → Closed.
- **Top 3 prompts** ensure dashboards surface *actionable insights*, not just numbers.
- **Cross-cutting pivots**: Clicking any Promise or Requirement shows both its definition (link to Meme Pool) and the collection of Offers it affects.
- **Threshold awareness**: Agreement Phase Threshold is explicit; exceeding it unlocks negotiation tools.
- **Privacy posture**: Spaces see only alignment signals; only I see my private answers.

---

👉 *Next steps:*
- Align on **visual language** (chips, icons, color coding).
- Decide whether the **Resonance Engine Dashboard** is part of Connect or a separate DAHN module.
- Prototype the funnel dashboard + feedback flows in low-fidelity wireframes.  