# MAP Client Security Implementation Plan

**Version:** 0.8

**Date:** 2026-11-16

**Status:** Independent CS1 boundary protections, state-aware packaged Welcome and the deny-only initial admission contract are implemented. App-private macOS custody and non-mutating transition preparation are implemented provisionally; signed-package assurance and live cutover remain outstanding. Constitution and authorized reopening remain disabled pending the CS2–CS4 enablement gates. Verification scope and limitations are recorded below; no complete CS-L1 or production-readiness claim.

## 1. Authority and delivery boundary

The [Client Security design specification](map-client-security-design-spec.md) owns semantics. This plan delivers reusable security capabilities independently of Agent Spaces. AS2 consumes the bounded initial local capability; it does not implement a general security framework. Completing the entire future security roadmap is not an AS2 dependency.

## 2. CS-L1 — Initial local trust and authorization

CS-L1 is tracked by [map-holons #872](https://github.com/evomimic/map-holons/issues/872) and consumed by [AS2 #870](https://github.com/evomimic/map-holons/issues/870). The implementation units below subdivide delivery; they are not newly created GitHub issues.

### Reconciled CS-L1 implementation units — proposal for review, 2026-11-16

CS-L1 is the bounded security milestone. CS1–CS5 name its supported-configuration, Welcome-admission, credential-custody, binding/retirement and assurance contract areas; they are not five completed deliveries or automatically five PRs. The following units assign reviewable outcomes and explicit AS2 consumers. The [AS2 unit/first-constitution contract](../agent-spaces/agent-spaces-impl-plan.md#reconciled-implementation-units--proposal-for-review-2026-11-16) defines lifecycle outcomes; this plan supplies mechanisms and security evidence, not a competing onboarding flow.

| Unit | Security delivery and AS2 consumer | Exit evidence / current allocation |
| --- | --- | --- |
| CS-L1.1 — Supported packaged execution boundary (CS1) | Fixed supported profile, packaged Welcome isolation, native-host/conductor ingress restrictions and a closed inventory of privileged entrypoints. Consumed by AS2-P and all later units. | Show actual permitted and denied interfaces, wrong-window/content/local-caller isolation, no frontend reusable authority, no startup restoration of forbidden interfaces and compatible retained-state behavior. `c9316ce3` supplies substantial mechanism implementation/basic tests; packaged terminal foundation evidence is now established by AS2-P, while complete supported-profile security assurance remains open. |
| CS-L1.2 — Scoped constitution admission and credential custody (CS2/CS3) | Verified explicit packaged Welcome request path, internally resolved installation/Space/operation scope, protected backend credential custody and a documented admitted-request contract. Consumed by AS2-C. | Approved initiation can reach the narrowly authorized backend operation under eligible controlled preconditions; unauthorized/forged/out-of-scope requests fail. Custody and retained-credential access are demonstrated on the supported configuration. Current working-tree status/admission code is deny-only: it establishes no usable constitution credential or allowed acquisition. No production constitution path is enabled before AS2-C/CS-L1.3 are ready. |
| CS-L1.3 — Constitution authority binding and durable retirement (CS4 acquisition portion) | Bind the resulting PersonAgent principal to author/executor authority and retire acquisition-only privileges using the agreed persisted-state/commitment contract. Delivered with AS2-C integration, not as an assumption that CS-L1 is already complete. | Real constitution establishes required authorization effects; repeated/competing/unknown-outcome requests cannot create another association. Interrupted work follows existing remediation/resubmission; restart preserves retirement even though author invocation rights may remain. Missing/inconsistent credentials deny privilege without reissuing acquisition authority. Current code does not deliver this. |
| CS-L1.4 — Authorized lifecycle continuation (CS4 Open/Upgrade portion) | Reconstruct authority for the same acquired AgentSpace and enforce only the reconciled finite operation inventory. Consumed by AS2-O and its explicitly scoped Navigator handoff, then AS2-U's declared transition. | Valid retained credentials support the same principal/context without reacquisition or bootstrap reopening; missing/inconsistent credentials deny. Authorized bounded reads/presentation and the supported version transition work; out-of-scope calls fail. Current discovery/presentation tests are not this evidence. |
| CS-L1.5 — Assurance and handoff (CS5, applied to each unit) | Mechanism-level positive/negative and actual-boundary evidence, supported revisions/configuration and residual limits. Required before enabling each unit's exposed paths; final composition evidence accompanies AS2-C/O/U. | Publish the relevant interface/content/local-caller, credential, replay/retirement and restart results for each enabled path. Unit/configuration tests, a disabled button and unsigned/debug rendering are identified accurately. This is not a later phase that permits unverified security now, nor a requirement to finish every future security feature. |

**No circular completion gate.** AS2-C consumes CS-L1.1/2 and delivers the real domain integration needed to prove CS-L1.3. CS-L1.4 is exercised through AS2-O/U. Mechanism contracts/tests may precede their consumer using controlled fixtures; final security/lifecycle claims require the real integration. Neither #872 nor #870 must be declared complete before that integration can be implemented. Each remains open until its own whole milestone acceptance passes.

**Proposed PR handling.** The next feature PR is AS2-C, whose acceptance requires actual first personal constitution with its necessary security integration. A prerequisite PR for CS-L1.1/2 is legitimate only if its independently useful boundary/custody/admission contract and supported evidence are explicit. Merging a collection of deny-only screens/helpers is not evidence of constitution, complete CS2/CS3 or complete CS-L1. No branch split, new issue, PR creation or merge is performed by this reconciliation.

### Required handoffs before the first-constitution PR

1. **Configuration/ingress:** publish the exact profile, admitted entrypoint(s), inaccessible or equivalently checked alternatives, and tests. Reuse CS1 controls and close remaining demonstrated gaps rather than re-inventorying the whole future security roadmap.
2. **Custody/admission:** settle the concrete protection and restart availability of backend-held authorizing credentials and the narrowly scoped allowed request path in design §8.2. Do not treat the existing empty Lair passphrase or a native signer as the security argument. Approved Welcome can submit personal naming data; it cannot select the sovereign principal, target Space/cell, author key or bootstrap authority. Actual IPC/runtime/zome mappings must precede enablement; the current zero-argument denied command is preparation, not the finished form/API.
3. **Durable binding/retirement:** define the security meaning, minimal representation and authoritative lookup of principal/author/executor binding and retirement, coordinated with AS2's committed IsInteriorOf predicate and shared persistence. Do not prescribe a ConstitutionRecord, generic journal or another completion artifact. Reuse an adequate existing mechanism when established by inspection/evidence.
4. **Shared eligibility and commitment:** consume named relationship/constraint/lineage/key handoffs and acquisition-specific conflict/retry evidence. Security cannot certify authoritative absence from the current inverse collection, enforce history through UI state, or require a new all-or-nothing transaction mechanism.
5. **Integrated evidence:** map the proposed AS2-C acceptance cases to actual tests and entrypoints; prove legitimate constitution, blocked alternate ingress, durable retirement, relevant interruption/resubmission and minimal restart recognition. Full authorized Navigator/Open is a later unit, but retirement must already survive restart in AS2-C.

Custody and durable authority-binding choices remain concrete implementation/security decisions requiring their owning specification contracts before enablement. They do not reopen Local Sovereign Constitution, external recognition, the approved packaged-Welcome trust boundary or the absence of mandatory independent OS confirmation. Ordinary DTO details, presentation text and internal adapter choices may be resolved during implementation within those contracts. General Dancer/delegation engines, cross-device continuity, credential-loss/compromise recovery and general migration remain deferred.

### Operation inventory by delivery unit

The existing minimum inventory below remains the approved baseline. This allocation does not grant additional privileges.

| AS2 consumer | Permitted operation envelope to enumerate and verify | Not yet admitted by this allocation |
| --- | --- | --- |
| AS2-P | Internal first-space/foundation provisioning; read-only lifecycle status and required saved-state verification | General frontend bootstrap commands, arbitrary schema import or sovereign mutation |
| AS2-C | Explicit initial personal constitution; resolution/retry of that same request; scoped constitution-result/identity reads; retirement/restart-recognition checks | Generic mutation/Dance dispatch, operational Navigator, full acquired-space runtime opening, credential recovery |
| AS2-O | Retained-credential Open of the same acquired principal/Space and existing continuity reads; proposed bounded built-in Navigator realization/read operations require an exact approved entrypoint/data-scope list before exposure | Arbitrary browsing, mutation or every action discoverable in the Navigator; displaying an action does not authorize it |
| AS2-U | Only the declared supported versioned transition and its outcome/retry checks | Generic migration, arbitrary schema mutation or expanded administrative authority |

AS2's intended Welcome-to-Navigator handoff requires a targeted reconciliation of its built-in presentation/content reads with this finite inventory. Before AS2-O enablement, enumerate actual Canvas/Home Dancer resolution, content/property/relationship reads and any other required calls, their resource scope and denial behavior; approve the closed list rather than adding a category such as "all Navigator operations". CS-L1.4 implements that bounded authorization. General Dancer/delegation authorization is not pulled into AS2-C or AS2-O by implication.

### Tracking alignment still proposed

Issue #872 exists; earlier plan wording that CS-L1 was only a documentation label is superseded. The issue still uses older full-write-set/physical-atomicity language and must be aligned with the accepted Complete/Rejected/Incomplete and remediation/resubmission contracts, coordinated with #870. Record the new unit/consumer mapping and current partial status rather than marking the milestone complete. No GitHub issue body is changed in this pass; first review the proposed AS2-C PR contract and unit boundaries.

### Contract gate

Apply the approved boundary in design §8.1 and resolve the remaining §8.2 implementation/assurance gates before enabling usable constitution credentials or the bounded privileged paths. Record one supported configuration, its enforcement controls, ingress coverage, backend credential custody, scope/retirement and lifecycle restart checks. Map the finite operation inventory below to concrete AS2 integration tests. Keep security, semantic assessment and commitment decisions separate; AS2's scope and D2 Local Sovereign Constitution remain unchanged.

### Approved local trust boundary

Trust the legitimate packaged application and approved Welcome code, Rust host, embedded conductor and protected signing facilities within an uncompromised OS environment. The OS account is an environmental assumption, not a grant to its other processes. Unrelated WebViews, remote/displayed content, supplied IDs and bootstrap flags remain untrusted. Implement and verify isolation, origin restrictions and command permissions so that displayed content cannot inherit constitution authority. Keep credentials and authorization enforcement in the backend; do not place reusable constitution authority in frontend JavaScript.

Exclude compromise of trusted Welcome code, the native host and OS from the initial assurance claim. Retain exposed-interface, unauthorized-local-caller and untrusted-content attacks in the test scope; do not use the integrity assumption to waive admission/isolation verification. Explicit Welcome initiation and backend request-path verification express the approved human-initiation assurance, not cryptographic proof of identity or intent.

Independent native/OS confirmation is not a CS-L1 prerequisite. Reuse existing facilities; introduce neither independent native confirmation nor a new credential framework unless investigation demonstrates a concrete inability to enforce the approved boundary otherwise. Record such a finding and its bounded implications before changing the implementation contract.

### Repository grounding and implementation

Inspect existing Tauri command/capability configuration, Holochain plugin origin/token/signing behavior, native runtime dispatch, conductor interfaces, guest session restoration and keystore integration on the actual implementation baseline. Candidate surfaces include `host/conductora/capabilities/`, `plugins/tauri-plugin-holochain/`, `src/runtime/dispatch_map_command.rs`, and `happ/crates/holons_guest/src/dances_guest/dance_adapter.rs`. Their existence is not proof of sufficient authorization.

**Inspected baseline — 2026-11-14:** map-holons `36a577c2fa5b6c78419897ecdfcca4e56b32b79b`; `host/Cargo.lock` resolves Holochain 0.7.1 and Tauri 2.12.4. Inspection of Holochain 0.7.1 `holochain_state::source_chain::SourceChain::valid_cap_grant` shows an author-access check before stored remote grants are consulted. Removing a stored grant must not be assumed to disable the author's inherent call rights. The current host issues reusable app tokens, and guest context restoration enables bootstrap mode from wire session state; neither establishes semantic constitution authority. Recheck the actual implementation revision and dependency sources when delivering CS-L1. These are inspection findings, not security-test evidence.

Reuse adequate existing mechanisms. Deliver only:

- Trusted initiation/admission and constitution-specific scope enforcement.
- Credential issuance/custody and replay or equivalent repeated-acquisition protection.
- Durable principal/execution authorization binding and acquisition privilege retirement.
- Authorization for opening/restarting the same acquired AgentSpace and only the minimum operations inventoried below; missing credentials fail closed. No general ordinary-operation or Dancer authorization delivery is implied.
- Integration with shared commitment outcomes and conflicts, without a competing persistence path.

No capability framework, general policy engine, arbitrary Dancer/delegation authorization, WeSpace role system, TrustChannel implementation, external identity service or recovery framework is implied. Any unsupported privileged path exposed by the configuration must be disabled or protected, not admitted through bootstrap authority.

### Minimum operation inventory

`AS2-Local-Lifecycle` names the proposed concrete integration acceptance scenario, not an existing implemented test. Its finite operation inventory is:

| Scenario step | Required authorization scope |
| --- | --- |
| Trusted startup provisions one unclaimed Space and packaged foundation | Existing narrowly scoped internal provisioning; no general UI bootstrap privilege |
| Welcome requests and resolves/retries constitution | Only the eligible installation/Space and complete initial acquisition operation |
| Close, restart and Open the same acquired AgentSpace | Retained-credential verification and reconstruction of its principal/executor context |
| Verify reopened identity/content continuity | Reads of the established Agent/Space identity, Home Space/interior association and retained fixture holons needed by this scenario |
| Exercise the explicitly supported AS2 Upgrade transition, if exposed | Only the versioned transition declared by that AS2 test; enumerate its exact entrypoints before enabling it |

Before implementation, map each step to named IPC/runtime/zome entrypoints and actual AS2 test identifiers. No unrestricted mutation, arbitrary Dance dispatch or unspecified additional local operation is admitted by this table. Tests needing additional authorized operations must explicitly reconcile that finite inventory; shared versioning/validation tests do not automatically expand CS-L1. CS-L1 must also demonstrate denial of unsupported operational Dancers and other reachable out-of-scope privileged paths.

### Acceptance contract

For the explicitly supported configuration, demonstrate:

1. Explicit initiation by approved packaged Welcome reaches the authorized backend path under design §8.1, without requiring independent native/OS confirmation. It is not described as cryptographic proof of human identity or intent.
2. Backend authorization admits only an eligible initial acquisition within the approved operation/installation/Space scope.
3. Unauthorized or alternate reachable paths cannot successfully constitute an AgentSpace; include direct conductor/zome ingress where applicable. Other local processes, unrelated WebViews and untrusted displayed content cannot inherit constitution authority through exposed interfaces, origin/permission gaps or a supplied identity/bootstrap flag. Frontend JavaScript receives no reusable constitution authority.
4. Completed acquisition cannot produce a second successful sovereign association, including when called by a technically authorized author. Idempotent retry may recover the original result. Competing requests and lost-response/retry behavior integrate with shared transaction guarantees; deleting a grant is not sufficient retirement evidence.
5. Durable principal/executor authorization evidence and valid retained credentials support opening the same acquired AgentSpace after restart without reacquisition.
6. Missing or inconsistent authorization evidence/credentials fails closed; acquisition-only privileges cannot become a standing operational bypass.
7. Only the minimum inventoried AS2 operations are supported; other privileged paths remain unavailable or appropriately protected. Broader security capabilities remain deferred.
8. Evidence identifies the verified code/dependency revisions, deployment mode (development versus packaged), the approved trust assumptions/exclusions, in-scope interface/local-caller/content attacks, residual risks and unverified guarantees. Integrity of approved packaged code is an assumption; correct enforcement of content isolation and caller admission must be demonstrated.

Client Security owns mechanism-level security tests; AS2 owns the end-to-end `AS2-Local-Lifecycle` integration; shared Transactions/persistence owns commitment and concurrency guarantees. This acceptance contract does not make CS-L1 alone proof of physical atomicity or full production readiness.

### Evidence and handoff

Own mechanism-level tests for unauthorized/direct callers, forged identities/flags, origin and permission boundaries, credential exposure/replay, operation/Space scope, post-completion privilege reuse, restart and missing credentials. Distinguish packaged from development configurations. Coordinate interruption/response-loss tests with shared persistence ownership.

Publish the supported API/contract and verified revision/configuration, guarantees, residual risks and unverified checks. AS2 runs selected end-to-end scenarios through its real lifecycle. Security assurance must cover the guarantees needed by the supported deployment; broader capability deferrals cannot waive those guarantees. No production-readiness claim follows from plan completion alone.

## 3. Later capabilities

General Dancer authorization, arbitrary delegation, WeSpace roles, universal operation-policy management, adaptive risk/step-up, rotation/revocation, credential recovery, multi-device continuity and interspace security are separately scoped. Their sequencing remains open and must not silently expand CS-L1 or AS2.

## CS1 implementation record — 2026-11-15

### Configuration and ingress disposition

The working implementation targets packaged macOS on Apple Silicon. Tauri packaging declares macOS 14.0 as its minimum; the current verification machine is macOS 26.5.2 arm64. These are distinct from a claim of assurance across supported OS releases. The packaged build uses the custom-protocol feature, an embedded fixed storage configuration and the Tauri resource mapping for the hApp. Release binaries cannot fall back to development privileges. Development overrides are rejected for packaged Welcome.

| Surface | Packaged disposition | Development disposition |
| --- | --- | --- |
| Conductor administration | Existing in-process Holochain admin handler; no admin listener | Existing admin WebSocket workflow retained |
| Dance transport | Native caller fixed to the selected cell and holons::dance; no app listener or frontend token | Existing authenticated app-WebSocket transport retained |
| Generic signing / additional hApp windows | Rejected by the native-only runtime | Existing explicit plugin capabilities retained |
| Generic MAP IPC, legacy map_request and auxiliary client commands | Not registered in packaged handler | Existing handler registered with explicit application-command permissions |
| Welcome | Dedicated fixed local page, narrow capability and backend window/URL check; no materialized modules | Not an authorized constitution surface |
| Constitution | Narrow request command exists but always refuses; no principal or supplied bootstrap flag enables it | No constitution authority supplied |
| Direct node / SmartLink exports and supplied guest bootstrap state | Existing WASM semantics unchanged; no external local conductor interface, generic client dispatch or signing route reaches them in this configuration | Existing development/test paths retained |
| Open / restart | Existing Space discovery and content preservation; no authorized sovereign execution supplied | Existing development behavior retained |
| Upgrade | No semantic AS2 Upgrade enabled | Existing development behavior is not AS2 Upgrade evidence |

Before starting the native-only conductor, its own persisted-state loader checks for saved app listeners and refuses incompatible state before those listeners can reopen. No identity reset, replacement Space, or implicit migration is performed. The absence of an app listener is independent of the author's inherent capability rights; deleting a remote grant is not used as retirement evidence. Startup compares persisted DNA/coordinator definitions with the packaged hApp and refuses mismatches or active remote grants in this initial local-only execution profile. Broader remote execution is not implemented by these checks.

### Verification and remaining gates

Focused tests exercise exact Welcome URL/window admission, narrow command permissions, native provisioning through the existing loader/Commit path, retained Space discovery and persisted-listener rejection. Results must distinguish library/conductor mechanism tests from actual packaged WebView evidence. Full packaged assurance, hostile content/local-caller coverage, credential-store protection and the CS2–CS5 lifecycle remain separately identified checks.

Existing Lair signing is reused; native backend custody does not itself establish protection of the credential store against all local attack surfaces. The existing empty-passphrase setup is not evidence of protected custody. CS3 must establish and verify the actual storage/custody guarantee before constitution is enabled. CS2 supplies backend admission and the eligible installation/Space operation scope; CS4 supplies principal binding, durable retirement and restart authorization. Commit remediation/resubmission semantics remain unchanged.

### Verification results — working tree, macOS 26.5.2 arm64

- `cargo test --manifest-path host/Cargo.toml -p Conductora -p holochain_runtime --lib --locked -- --test-threads=1`: 31 Conductora and 5 embedded-runtime tests passed. The real persistent-conductor case loads the production hApp and full Core bootstrap through the native transport, observes Complete, restarts and discovers the same Space without bootstrap authority. The separate listener case seeds a saved external interface and verifies rejection before it can be restored. These run outside the managed sandbox because Holochain requires network-monitor access.
- The two Welcome admission/capability tests were rerun after narrowing the capability to the exact WebView label; both passed. These are unit/configuration tests, not live-WebView attack tests.
- Production Angular build passed with the matching ARM64 Node runtime outside the managed sandbox. The sandboxed process aborted; no dependency or lockfile workaround was introduced. Existing size/CommonJS warnings remain.
- An unsigned debug macOS app bundle built with `custom-protocol`; its mapped hApp, bootstrap manifest and import resources were verified. It was launched from `/private/tmp`, outside the checkout. A process-level check observed no TCP listeners. This is packaged-asset/debug-build evidence, not a signed release or production-readiness claim.
- Initial UI inspection timed out while first-time loader/validation work was active and dependency warning output was excessive. Welcome creation was moved before background provisioning. The updated unsigned debug bundle was then relaunched from `/private/tmp` with retained state and quieter logging: native inspection observed `tauri://localhost/welcome.html`, the expected unavailable message from the backend status response and the disabled personal-space button. This verifies basic packaged rendering, script execution and the narrow status path; adversarial CSP, hostile-content and alternate-WebView checks remain unverified. The earlier verification process was stopped without deleting or resetting data; its complete first-run configured-import outcome was not established.

No MAP schema, guest Commit or sovereign-state semantics changed. Acquired-space authorization and operational execution remain disabled pending CS2–CS4. Full packaged security assurance, credential-store protection, P2P/remote-grant negative cases and local filesystem attack coverage remain explicit follow-up evidence; no claim of complete CS-L1 follows from these checks.


## State-aware Welcome and initial admission contract — 2026-11-16

The next increment implements read-only lifecycle presentation and the denied initial-constitution admission path. It does not complete CS2/CS3 or enable acquisition. CS1 checkpoint: map-holons `c9316ce3`; corresponding security-document checkpoint: DevDocs `08f86e7`.

### Bounded CS2/CS3 integration contract

| Boundary | Initial implementation contract |
| --- | --- |
| Initiation | The approved packaged Welcome page explicitly invokes `constitute_personal_space`; the command takes no caller-selected principal, Space, author key, operation name or bootstrap argument. No independent native/OS confirmation is required. |
| Admission | Existing exact WebView-label/URL checks and Tauri permissions admit the request path. They do not establish domain eligibility or sufficient credential custody. All currently reachable constitution requests remain denied. |
| Target scope | Rust resolves the saved local Space through the configured native runtime and TransactionContext/Reference Layer. The existing native caller is fixed to the one admitted app/role/cell and `holons::dance`. No target selector is exposed to Welcome. This is initial personal constitution only, not arbitrary Dance authority. |
| Display evidence | `welcome_status` returns a phase, explanatory text, availability and blocking-reason codes. No target identity, author credential, signing capability or execution permit is returned. Process-local observations serve presentation only. |
| Custody and issuance | Reuse the backend's existing Lair/native signing facilities as the technical author. Do not infer constitution authority from that key or issue another bearer credential merely to represent admission. No usable constitution credential/permit is issued in this increment. Existing empty-passphrase Lair setup has not established protected custody; CS3 must supply and verify that guarantee before enabling issuance/exercise. No new credential framework is selected. |
| Eligibility | A saved `IsInteriorOf` observation prevents offering another constitution. An empty current collection is not proof of authoritative absence across source/target lineage evolution, so the status is foundation-present with eligibility unverified, not eligible-unclaimed. Unavailable or ambiguous evidence denies admission. |
| Execution and retirement | Before enabling execution, integrate the complete AS2 acquisition effects, shared validation/commitment, principal binding and durable retirement/retry contracts. The admitted path alone cannot mint usable authority, commit a partial PersonAgent, certify completion or open general operations. |

This slice reads the persisted local Space, the supported Agent Spaces schema/PersonAgent descriptor and its saved `IsInteriorOf` collection through the existing Reference Layer. It never authors the inverse, writes a completion marker, changes TDL, replays imports during Open or establishes a sovereign principal. Multiple observed members are reported as unresolved evidence, not an independent local cardinality validator. A positive observation reports the recorded association, without claiming that lineage traversal, authorized restart or all onboarding effects have been verified.

Packaged Welcome remains visible during initialization, foundation loading and evidence checks. Startup errors remain visible in the restricted page with admission closed. A recorded association produces a returning-installation message and hides constitution; it does not launch Navigator until authorized Open exists. Missing foundation, lookup failure and inconsistent state are blocked without replacement, automatic import replay or reacquisition. Neither foundation presence nor presentation state is a global provisioning-completion artifact.

Existing Complete/Rejected/Incomplete Commit outcomes, retained saved/staged work, diagnostics and remediation/resubmission remain unchanged. Authorization denial occurs before any acquisition mutation; this increment adds no transaction protocol.

### Remaining enablement gates

- Verify protected backend credential custody for the supported packaged configuration; specify how retained credentials are available on ordinary restart and fail closed when missing.
- Deliver authoritative lineage/history lookup and shared eligibility/continuity enforcement, and the complete acquisition orchestration with existing Commit remediation and retry identity.
- Integrate durable principal/executor binding and acquisition privilege retirement. Only then enable the approved Welcome action.
- Enumerate and authorize the bounded operational entrypoints before replacing Welcome with Space Navigator. General Dancer/delegation authorization remains outside CS-L1.

Verification results for this increment are recorded after the implementation checks; packaged live-page evidence is distinct from unit/conductor evidence. No production-readiness claim follows from the admission contract or the deny-only path.

### Verification of the state-aware increment

- Host library suite: 34 passed, including the extended real native-conductor test using the production hApp, ordinary Lair keys and no app/admin WebSocket listeners. It rejects missing Agent Spaces foundation evidence, then observes the saved Space/current inverse after a completed schema import. A fresh runtime after conductor restart adopts the persisted designation as ordinary Open does and observes the same Space/status without import replay. These checks do not establish historical absence or authorized acquired-space reopening.
- Packaged page script: 3 tests passed using the actual shipped HTML/JavaScript. They cover startup polling to foundation-present, hiding constitution for an existing association, and closed admission on status failure with safe text rendering. Pure host classification tests cover unavailable/ambiguous evidence and failure overriding prior observations; no response includes a target ID or credential.
- Web typecheck, Rust formatting and scoped diff checks passed. The unsigned debug macOS/Apple Silicon app bundle with `custom-protocol` built successfully. No signed-release or adversarial-security assurance is claimed.
- Live native inspection observed the updated `tauri://localhost/welcome.html`, backend-provided initial-runtime status and disabled constitution button. Its retained-state startup remained busy in SQLite work before conductor initialization completed. The verification process was stopped with its persistent store intact; terminal foundation/association presentation and completed packaged Open were not established by that run. This is a separately recorded startup verification limit, not authority to reset/reprovision retained state.

### AS2-P consumer verification — 2026-11-16

The rebuilt supported packaged application now reaches terminal `foundation-present` on retained state, with the constitution action disabled. Logs confirm the same startup path adopts the existing Space without bootstrap import replay and checks the 31 fixed configured definitions. This resolves the earlier live terminal-startup evidence limit; it does not establish acquisition eligibility, credential custody, retirement, historical continuity or authorized acquired-space reopening.

The native conductor delay was isolated to repeated gossip-sector database scans and corrected in a bounded native dependency patch, with an additive index migration documented in `map-holons/host/patches/README.md`. A backup preceded retained-store migration. The [AS2-P delivery record](../agent-spaces/agent-spaces-impl-plan.md#as2-p-delivery--bounded-first-space-foundation-2026-11-16) records evidence and the retained shared bootstrap-readiness gap. This does not broaden CS-L1 or resolve its remaining security-assurance gates.

The final AS2-P host suite passed all 35 tests, including real-conductor provisioning/restart and interface-denial assertions; the 3 shipped Welcome-script tests also passed. These are lifecycle/mechanism checks, not a replacement for the outstanding CS-L1 security-assurance gates.


## App-restricted macOS custody implementation — 2026-11-16

**Decision:** app-private data-protection Keychain custody is adopted under design §8.4. It wraps the existing Holochain/Lair facilities rather than adding an identity provider, constitution confirmation or credential framework. CS-L1.2 remains partial; admission is still deny-only and no personal constitution is enabled.

### Implemented boundary and transition preparation

The native runtime supplies an insert-only Keychain provider with explicit data-protection/private-group queries, device-local unlocked-only access and no authentication UI fallback. A compile-time `MAP_KEYCHAIN_ACCESS_GROUP` identifies the provisioned application identifier; runtime/IPC values cannot select it. Current-process signature admission requires an Apple-anchored signature, the expected bundle/application identifier and absence of the debugger entitlement. Secret generation/readback remains native and missing/inaccessible retained custody or incomplete retained installation state fails closed.

The host's non-default `protected-custody` feature selects this provider and rejects development/reset profiles. The default foundation-only engineering profile retains its existing startup behavior and cannot authorize constitution. These profiles must not be confused: an ordinary unsigned `npm start` is not Keychain security evidence. Enabling the feature alone is not an approved production configuration.

The version-bound Lair 0.7.1 and native `holochain_data` adapters prepare replacement encrypted wrappers in memory. They preserve the Lair context key/server seed and the existing conductor SQLCipher key/salt. Preparation neither writes an installation nor creates a Keychain item. The live store has not been migrated. Applying the prepared wrappers remains an explicit pending step requiring exclusive shutdown, recoverable installation of both wrapper files, protected legacy-backup handling and verified signed custody. This is a bounded credential transition, not a change to MAP Commit or a new transaction subsystem.

### Signing/provisioning and remaining evidence

1. Supply the legitimate application signing identity and an authorized provisioning profile for the actual application identifier. Current inventory found no valid visible code-signing identities or profiles on this Mac. Do not invent a Team/App ID prefix or commit private signing material.
2. Build packaged assets with `custom-protocol,protected-custody`, compiling `MAP_KEYCHAIN_ACCESS_GROUP` to the profile-authorized application identifier. Sign the application with matching application-identifier/private Keychain entitlements and embed the authorized profile. Keep the private group stable across upgrades; omit debugger entitlement. Verify final nested signatures, entitlement/profile consistency and the embedded runtime's hardened-runtime/JIT requirements. Notarization and release distribution remain separate assurance work.
3. On a disposable installation, demonstrate legitimate create/retrieve/restart and denial to an unrelated local executable, another signed app, unauthorized group and untrusted WebView/content. Verify locked Keychain, missing item, existing item and interrupted initialization failures without replacement/fallback. Current-process rejection tests alone do not demonstrate Keychain group isolation.
4. Before touching retained user state, complete and exercise the offline recoverable cutover on disposable copies. Verify identical author, Space/descriptor identities and content, and a restart without bootstrap replay. Preserve recovery until the new package opens successfully; protect and explicitly dispose/retain legacy empty-passphrase wrappers rather than silently deleting backups.
5. Only after these checks perform an explicitly authorized live cutover. Continue the remaining CS-L1.2 admission/scope and CS-L1.3 binding/retirement work with AS2-C; custody does not establish their completion.

Mechanism tests use synthetic temporary encrypted Lair/Conductor stores and an in-memory custody provider. Their evidence covers preservation of a signing public key and signature validity, retained encrypted database content/key/salt, old-passphrase rejection, non-mutating preparation, insert-only issuance and missing/denied-state failures. They do not prove legitimate signed-package Keychain retrieval or complete AS2 constitution/restart authorization. All eight native custody tests passed on macOS 26.5.2 arm64, including disposable real encrypted-store preservation and unsigned-process admission rejection. No live Keychain or user-store mutation is part of these tests.


**Host validation:** the native host compiled with `custom-protocol,protected-custody`; all 34 selected host library tests passed. The existing full `native_only_provisioning_retains_identity_without_external_interfaces` bootstrap/restart test was excluded in this run; no new claim of full HolonSpace identity continuity through a live cutover is made. Native workspace formatting and scoped diff checks passed. No web or hApp source changed. Signed-package positive access, unrelated-signed-app denial and the recoverable live-store cutover remain unverified/unimplemented as listed above.


**User startup checkpoint:** `npm start` was reported nominal after this custody increment. This verifies ordinary foundation-only engineering startup; it does not exercise the opt-in protected Keychain profile or perform a live credential transition.
