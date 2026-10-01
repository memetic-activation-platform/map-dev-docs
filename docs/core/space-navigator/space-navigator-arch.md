# DAHN Architecture Has Moved

The canonical specification is now [DAHN Architecture](../hx/dahn-arch.md).
Shared composition and runtime mechanisms are defined in the
[DAHN Design Specification](../hx/dahn-design-spec.md). This page contains
navigation only and has no normative authority.

## Previous section links

<a id="dahn-space-navigator-architecture-specification-v04"></a>
[DAHN Space Navigator Architecture Specification v0.4](../hx/dahn-arch.md#status)

<a id="status"></a>
[Status](../hx/dahn-arch.md#status)

<a id="purpose"></a>
[Purpose](../hx/dahn-arch.md#purpose)

<a id="1-relationship-to-the-space-navigator-document-set"></a>
[1. Relationship to the Space Navigator Document Set](../hx/dahn-arch.md#1-relationship-to-the-specification-family)

<a id="2-dahn"></a>
[2. DAHN](../hx/dahn-arch.md#2-dahn)

<a id="21-dynamic"></a>
[2.1 Dynamic](../hx/dahn-arch.md#21-dynamic)

<a id="22-adaptive"></a>
[2.2 Adaptive](../hx/dahn-arch.md#22-adaptive)

<a id="3-existing-map-deployment-architecture"></a>
[3. Existing MAP Deployment Architecture](../hx/dahn-arch.md#3-existing-map-deployment-architecture)

<a id="4-primary-responsibility-boundary"></a>
[4. Primary Responsibility Boundary](../hx/dahn-arch.md#4-primary-responsibility-boundary)

<a id="5-rust-responsibilities"></a>
[5. Rust Responsibilities](../hx/dahn-arch.md#5-rust-responsibilities)

<a id="6-typescript-responsibilities"></a>
[6. TypeScript Responsibilities](../hx/dahn-arch.md#6-typescript-responsibilities)

<a id="7-map-state-versus-experience-state"></a>
[7. MAP State Versus Experience State](../hx/dahn-arch.md#7-map-state-versus-experience-state)

<a id="71-map-state"></a>
[7.1 MAP State](../hx/dahn-arch.md#71-map-state)

<a id="72-experience-state"></a>
[7.2 Experience State](../hx/dahn-arch.md#72-experience-state)

<a id="8-ipc-boundary"></a>
[8. IPC Boundary](../hx/dahn-arch.md#8-ipc-boundary)

<a id="9-visualizers-are-holons"></a>
[9. Visualizers Are Holons](../hx/dahn-arch.md#9-visualizers-are-holons)

<a id="91-visualizer-holon-types"></a>
[9.1 Visualizer Holon Types](../hx/dahn-arch.md#91-visualizer-holon-types)

<a id="92-semantic-identity-and-executable-realization"></a>
[9.2 Semantic Identity and Executable Realization](../hx/dahn-arch.md#92-semantic-identity-and-executable-realization)

<a id="10-generic-versus-specialized-visualizers"></a>
[10. Generic Versus Specialized Visualizers](../hx/dahn-arch.md#10-generic-versus-specialized-visualizers)

<a id="101-static-core-visualizers"></a>
[10.1 Static Core Visualizers](../hx/dahn-arch.md#101-static-core-visualizers)

<a id="11-visualizer-commons"></a>
[11. Visualizer Commons](../hx/dahn-arch.md#11-visualizer-commons)

<a id="12-accessible-visualizer-population"></a>
[12. Accessible Visualizer Population](../hx/dahn-arch.md#12-accessible-visualizer-population)

<a id="13-visualizer-discovery"></a>
[13. Visualizer Discovery](../hx/dahn-arch.md#13-visualizer-discovery)

<a id="14-minimal-dahn-visualizer-schema"></a>
[14. Minimal DAHN Visualizer Schema](../hx/dahn-arch.md#14-minimal-dahn-visualizer-schema)

<a id="141-applicability"></a>
[14.1 Applicability](../hx/dahn-arch.md#141-applicability)

<a id="142-capabilities"></a>
[14.2 Capabilities](../hx/dahn-arch.md#142-capabilities)

<a id="143-version-and-evolution-domains"></a>
[14.3 Version and Evolution Domains](../hx/dahn-arch.md#143-version-and-evolution-domains)

<a id="15-dahn-selector-function"></a>
[15. DAHN Selector Function](../hx/dahn-arch.md#15-dahn-visualizer-selection-service)

<a id="16-selector-inputs"></a>
[16. Selector Inputs](../hx/dahn-arch.md#16-selector-inputs)

<a id="17-explore-versus-exploit"></a>
[17. Explore Versus Exploit](../hx/dahn-arch.md#17-explore-versus-exploit)

<a id="171-exploit-oriented-selection"></a>
[17.1 Exploit-Oriented Selection](../hx/dahn-arch.md#171-exploit-oriented-selection)

<a id="172-explore-oriented-selection"></a>
[17.2 Explore-Oriented Selection](../hx/dahn-arch.md#172-explore-oriented-selection)

<a id="18-adaptive-salience"></a>
[18. Adaptive Salience](../hx/dahn-arch.md#18-adaptive-salience)

<a id="19-personal-and-collective-adaptation"></a>
[19. Personal and Collective Adaptation](../hx/dahn-arch.md#19-personal-and-collective-adaptation)

<a id="191-personal-adaptation"></a>
[19.1 Personal Adaptation](../hx/dahn-arch.md#191-personal-adaptation)

<a id="192-collective-adaptation"></a>
[19.2 Collective Adaptation](../hx/dahn-arch.md#192-collective-adaptation)

<a id="20-gesture-handling-boundary"></a>
[20. Gesture Handling Boundary](../hx/dahn-arch.md#20-gesture-handling-boundary)

<a id="21-adaptive-presentation-context"></a>
[21. Adaptive Presentation Context](../hx/dahn-arch.md#21-adaptive-presentation-context)

<a id="22-visualizer-selection-result"></a>
[22. Visualizer Selection Result](../hx/dahn-arch.md#22-visualizer-selection-result)

<a id="221-visualizer-materialization"></a>
[22.1 Visualizer Materialization](../hx/dahn-arch.md#221-visualizer-materialization)

<a id="23-visualizer-acquisition-and-execution"></a>
[23. Visualizer Acquisition and Execution](../hx/dahn-arch.md#23-visualizer-acquisition-and-execution)

<a id="24-visualizer-runtime"></a>
[24. Visualizer Runtime](../hx/dahn-arch.md#24-visualizer-runtime)

<a id="25-trust-and-compatibility"></a>
[25. Trust and Compatibility](../hx/dahn-arch.md#25-trust-and-compatibility)

<a id="26-recursive-visual-composition"></a>
[26. Recursive Visual Composition](../hx/dahn-arch.md#26-recursive-visual-composition)

<a id="27-parent-owned-placement"></a>
[27. Parent-Owned Placement](../hx/dahn-arch.md#27-parent-owned-placement)

<a id="28-layout-budgets"></a>
[28. Layout Budgets](../hx/dahn-arch.md#28-layout-budgets)

<a id="29-visualizer-layout-capabilities"></a>
[29. Visualizer Layout Capabilities](../hx/dahn-arch.md#29-visualizer-layout-capabilities)

<a id="30-selection-versus-layout"></a>
[30. Selection Versus Layout](../hx/dahn-arch.md#30-selection-versus-layout)

<a id="31-responsive-composition"></a>
[31. Responsive Composition](../hx/dahn-arch.md#31-responsive-composition)

<a id="32-theme-architecture"></a>
[32. Theme Architecture](../hx/dahn-arch.md#32-theme-architecture)

<a id="33-theme-versus-semantic-layout"></a>
[33. Theme Versus Semantic Layout](../hx/dahn-arch.md#33-theme-versus-semantic-layout)

<a id="34-action-architecture"></a>
[34. Action Architecture](../hx/dahn-arch.md#34-action-architecture)

<a id="35-action-sources"></a>
[35. Action Sources](../hx/dahn-arch.md#35-action-sources)

<a id="351-holon-semantic-actions"></a>
[35.1 Holon-Semantic Actions](../hx/dahn-arch.md#351-holon-semantic-actions)

<a id="352-collection-actions"></a>
[35.2 Collection Actions](../hx/dahn-arch.md#352-collection-actions)

<a id="353-visualizer-actions"></a>
[35.3 Visualizer Actions](../hx/dahn-arch.md#353-visualizer-actions)

<a id="354-canvas-actions-and-dancer-transaction-actions"></a>
[35.4 Canvas Actions and Dancer Transaction Actions](../hx/dahn-arch.md#354-canvas-actions-and-dancer-transaction-actions)

<a id="36-action-visualizers"></a>
[36. Action Visualizers](../hx/dahn-arch.md#36-action-visualizers)

<a id="37-dancer-and-canvas-interaction-surfaces"></a>
[37. Dancer and Canvas Interaction Surfaces](../hx/dahn-arch.md#37-dancer-and-canvas-interaction-surfaces)

<a id="38-action-personalization"></a>
[38. Action Personalization](../hx/dahn-arch.md#38-action-personalization)

<a id="39-visualizer-occurrence"></a>
[39. Visualizer Occurrence](../hx/dahn-arch.md#39-visualizer-occurrence)

<a id="40-holon-identity-versus-occurrence-identity"></a>
[40. Holon Identity Versus Occurrence Identity](../hx/dahn-arch.md#40-holon-identity-versus-occurrence-identity)

<a id="41-dahn-interaction-events"></a>
[41. DAHN Interaction Events](../hx/dahn-arch.md#41-dahn-interaction-events)

<a id="42-dahn-events-versus-map-commands"></a>
[42. DAHN Events Versus MAP Commands](../hx/dahn-arch.md#42-dahn-events-versus-map-commands)

<a id="43-progressive-semantic-retrieval"></a>
[43. Progressive Semantic Retrieval](../hx/dahn-arch.md#43-progressive-semantic-retrieval)

<a id="44-effective-descriptor-boundary"></a>
[44. Effective Descriptor Boundary](../hx/dahn-arch.md#44-effective-descriptor-boundary)

<a id="45-property-and-value-visualizers"></a>
[45. Property and Value Visualizers](../hx/dahn-arch.md#45-propertymap-and-value-visualizers)

<a id="46-collection-visualizers"></a>
[46. Collection Visualizers](../hx/dahn-arch.md#46-collection-visualizers)

<a id="47-read-and-edit-architecture"></a>
[47. Read and Edit Architecture](../hx/dahn-arch.md#47-read-and-edit-architecture)

<a id="48-staged-state-ownership"></a>
[48. Staged State Ownership](../hx/dahn-arch.md#48-staged-state-ownership)

<a id="49-semantic-editing-ownership"></a>
[49. Semantic Editing Ownership](../hx/dahn-arch.md#49-semantic-editing-ownership)

<a id="50-multi-holon-transaction-scope"></a>
[50. Multi-Holon Transaction Scope](../hx/dahn-arch.md#50-multi-holon-transaction-scope)

<a id="51-commit-ownership"></a>
[51. Commit Ownership](../hx/dahn-arch.md#51-commit-ownership)

<a id="52-commit-flow"></a>
[52. Commit Flow](../hx/dahn-arch.md#52-commit-flow)

<a id="53-create-edit-and-clone"></a>
[53. Create, Edit, and Clone](../hx/dahn-arch.md#53-create-edit-and-clone)

<a id="edit"></a>
[Edit](../hx/dahn-arch.md#edit)

<a id="clone"></a>
[Clone](../hx/dahn-arch.md#clone)

<a id="create"></a>
[Create](../hx/dahn-arch.md#create)

<a id="54-delete"></a>
[54. Delete](../hx/dahn-arch.md#54-delete)

<a id="55-transaction-snapshots"></a>
[55. Transaction Snapshots](../hx/dahn-arch.md#55-transaction-snapshots)

<a id="56-ux-undo-boundaries"></a>
[56. UX Undo Boundaries](../hx/dahn-arch.md#56-ux-undo-boundaries)

<a id="57-undo"></a>
[57. Undo](../hx/dahn-arch.md#57-undo)

<a id="58-redo"></a>
[58. Redo](../hx/dahn-arch.md#58-redo)

<a id="59-transaction-status"></a>
[59. Transaction Status](../hx/dahn-arch.md#59-transaction-status)

<a id="60-continuous-snapshotting-versus-undo-semantics"></a>
[60. Continuous Snapshotting Versus Undo Semantics](../hx/dahn-arch.md#60-continuous-snapshotting-versus-undo-semantics)

<a id="61-adaptive-gestures-and-transaction-gestures-are-distinct"></a>
[61. Adaptive Gestures and Transaction Gestures Are Distinct](../hx/dahn-arch.md#61-adaptive-gestures-and-transaction-gestures-are-distinct)

<a id="62-dahn-map-adapter"></a>
[62. DAHN MAP Adapter](../hx/dahn-arch.md#62-dahn-map-adapter)

<a id="63-asynchrony"></a>
[63. Asynchrony](../hx/dahn-arch.md#63-asynchrony)

<a id="64-error-boundaries"></a>
[64. Error Boundaries](../hx/dahn-arch.md#64-error-boundaries)

<a id="65-presentation-refresh-after-semantic-change"></a>
[65. Presentation Refresh After Semantic Change](../hx/dahn-arch.md#65-presentation-refresh-after-semantic-change)

<a id="66-multiple-occurrences-of-the-same-holon"></a>
[66. Multiple Occurrences of the Same Holon](../hx/dahn-arch.md#66-multiple-occurrences-of-the-same-holon)

<a id="67-space-navigator-as-an-architectural-proof"></a>
[67. Space Navigator as an Architectural Proof](../hx/dahn-arch.md#67-space-navigator-as-an-architectural-proof)

<a id="68-initial-architectural-modules"></a>
[68. Initial Architectural Modules](../hx/dahn-arch.md#68-initial-architectural-modules)

<a id="69-architectural-testing-boundaries"></a>
[69. Architectural Testing Boundaries](../hx/dahn-arch.md#69-architectural-testing-boundaries)

<a id="691-rust-map-tests"></a>
[69.1 Rust / MAP Tests](../hx/dahn-docs-refactor-impl-plan.md#691-rust-map-tests)

<a id="692-dahn-adapter-tests"></a>
[69.2 DAHN Adapter Tests](../hx/dahn-docs-refactor-impl-plan.md#692-dahn-adapter-tests)

<a id="693-visualizer-runtime-tests"></a>
[69.3 Visualizer Runtime Tests](../hx/dahn-docs-refactor-impl-plan.md#693-visualizer-runtime-tests)

<a id="694-visualizer-tests"></a>
[69.4 Visualizer Tests](../hx/dahn-docs-refactor-impl-plan.md#694-visualizer-tests)

<a id="695-dancer-top-level-visualizer-tests"></a>
[69.5 Dancer Top-Level Visualizer Tests](../hx/dahn-docs-refactor-impl-plan.md#695-dancer-top-level-visualizer-tests)

<a id="696-adaptive-interaction-tests"></a>
[69.6 Adaptive Interaction Tests](../hx/dahn-docs-refactor-impl-plan.md#696-adaptive-interaction-tests)

<a id="70-architecture-that-should-not-be-over-generalized-initially"></a>
[70. Architecture That Should Not Be Over-Generalized Initially](../hx/dahn-arch.md#70-architecture-that-should-not-be-over-generalized-initially)

<a id="71-core-architectural-invariants"></a>
[71. Core Architectural Invariants](../hx/dahn-arch.md#71-core-architectural-invariants)

<a id="711-rust-owns-semantic-truth"></a>
[71.1 Rust Owns Semantic Truth](../hx/dahn-arch.md#711-rust-owns-semantic-truth)

<a id="712-typescript-owns-experience-realization"></a>
[71.2 TypeScript Owns Experience Realization](../hx/dahn-arch.md#712-typescript-owns-experience-realization)

<a id="713-rust-owns-the-dahn-selector"></a>
[71.3 Rust Owns the DAHN Selector](../hx/dahn-arch.md#713-rust-owns-the-dahn-selector)

<a id="714-visualizer-discovery-is-federated"></a>
[71.4 Visualizer Discovery Is Federated](../hx/dahn-arch.md#714-visualizer-discovery-is-federated)

<a id="715-visualizers-are-holons"></a>
[71.5 Visualizers Are Holons](../hx/dahn-arch.md#715-visualizers-are-holons)

<a id="716-visualizer-selection-and-execution-are-separate"></a>
[71.6 Visualizer Selection and Execution Are Separate](../hx/dahn-arch.md#716-visualizer-selection-and-execution-are-separate)

<a id="717-generic-fallbacks-preserve-usability"></a>
[71.7 Generic Fallbacks Preserve Usability](../hx/dahn-arch.md#717-generic-fallbacks-preserve-usability)

<a id="718-parent-owns-child-placement"></a>
[71.8 Parent Owns Child Placement](../hx/dahn-arch.md#718-parent-owns-child-placement)

<a id="719-layout-is-hierarchical"></a>
[71.9 Layout Is Hierarchical](../hx/dahn-arch.md#719-layout-is-hierarchical)

<a id="7110-themes-are-external"></a>
[71.10 Themes Are External](../hx/dahn-arch.md#7110-themes-are-external)

<a id="7111-read-and-edit-share-the-same-visual-structure"></a>
[71.11 Read and Edit Share the Same Visual Structure](../hx/dahn-arch.md#7111-read-and-edit-share-the-same-visual-structure)

<a id="7112-staged-state-remains-in-rust"></a>
[71.12 Staged State Remains in Rust](../hx/dahn-arch.md#7112-staged-state-remains-in-rust)

<a id="7113-transactions-may-span-multiple-holons"></a>
[71.13 Transactions May Span Multiple Holons](../hx/dahn-arch.md#7113-transactions-may-span-multiple-holons)

<a id="7114-undo-and-redo-are-transaction-scoped"></a>
[71.14 Undo and Redo Are Transaction-Scoped](../hx/dahn-arch.md#7114-undo-and-redo-are-transaction-scoped)

<a id="7115-subject-visualizer-and-occurrence-are-distinct"></a>
[71.15 Subject, Visualizer, and Occurrence Are Distinct](../hx/dahn-arch.md#7115-subject-visualizer-and-occurrence-are-distinct)

<a id="7116-adaptive-preferences-refer-to-visualizer-holons"></a>
[71.16 Adaptive Preferences Refer to Visualizer Holons](../hx/dahn-arch.md#7116-adaptive-preferences-refer-to-visualizer-holons)

<a id="7117-user-gestures-may-become-adaptive-signals"></a>
[71.17 User Gestures May Become Adaptive Signals](../hx/dahn-arch.md#7117-user-gestures-may-become-adaptive-signals)

<a id="7118-action-scope-determines-ownership"></a>
[71.18 Action Scope Determines Ownership](../hx/dahn-arch.md#7118-action-scope-determines-ownership)

<a id="7119-architecture-defines-contracts-not-space-navigator-ux"></a>
[71.19 Architecture Defines Contracts, Not Space Navigator UX](../hx/dahn-arch.md#7119-architecture-defines-contracts-not-space-navigator-ux)

<a id="72-architectural-summary"></a>
[72. Architectural Summary](../hx/dahn-arch.md#72-architectural-summary)

<a id="721-map-semantic-and-adaptive-layer-rust"></a>
[72.1 MAP Semantic and Adaptive Layer — Rust](../hx/dahn-arch.md#721-map-semantic-and-adaptive-layer-rust)

<a id="722-dahn-experience-layer-typescript"></a>
[72.2 DAHN Experience Layer — TypeScript](../hx/dahn-arch.md#722-dahn-experience-layer-typescript)

<a id="723-visualizer-ecosystem-federated-map-agent-spaces"></a>
[72.3 Visualizer Ecosystem — Federated MAP Agent Spaces](../hx/dahn-arch.md#723-visualizer-ecosystem-federated-map-agent-spaces)

<a id="724-canvas-hosted-dancer-experiences"></a>
[72.4 Canvas-Hosted Dancer Experiences](../hx/dahn-arch.md#724-canvas-hosted-dancer-experiences)
