# Workspace Strategy: Native, WASM, and Test Workspaces in the Holons Codebase

## Summary

The `map-holons` monorepo is being re-organized into **three separate Cargo workspaces**, each targeting a different runtime environment:

1. 🧬 `wasm/` — WebAssembly (WASM) builds for Holochain zome execution
2. 🖥 `native/` — Native builds (e.g., Tauri clients, local services)
3. 🧪 `test/` — Test runners and fixtures (e.g., `sweetests` integration suite)

This architecture resolves long-standing dependency issues caused by **Cargo's unified feature resolution**, and enforces clear target boundaries to ensure clean, reliable builds.

This document explains:

- Why we’ve split the workspace
- What the unified feature resolution problem is
- How it has undermined prior attempts to solve build incompatibilities
- What the current structure looks like
- Caveats to be aware of

---

## Why Two Workspaces?

### The Core Problem: Tokio and WASM Don't Mix

Many crates in the Holochain ecosystem — including `hdk` and its dependencies — rely on **Tokio**, which in turn pulls in platform-specific dependencies like **Mio**, which do **not** compile to WASM (e.g., `wasm32-unknown-unknown`). Some parts of our application — especially the zome logic intended to run inside WASM — must be WASM-safe and **cannot** link against Tokio or its transitive dependencies.

This leads to a critical conflict: we want our **native client code** (which can use Tokio) and our **zome code** (which must not) to coexist and share common libraries.

### The Hidden Killer: Unified Feature Resolution

Cargo’s **unified feature resolution** means that:

> If any crate in a workspace enables a feature on a dependency, that feature is enabled for **all crates** that depend on that dependency — regardless of whether they actually use that feature or whether the feature is compatible with the build target.

This is **global** across the entire dependency graph **per build**, and **not conditional on the target platform**.

#### Example:

- `holons-client` depends on `hdk` with the default features (includes Tokio).
- `holons-guest` (a zome crate) also depends on `hdk`, but wants to exclude Tokio.
- Cargo sees that some crate needs `hdk[default]`, and therefore compiles `hdk` with **Tokio enabled for all consumers**.
- Even when compiling `holons-guest` for `wasm32-unknown-unknown`, Tokio and Mio are pulled in — and the build fails.

### The Consequence

All attempts to use features, conditional compilation (`#[cfg(...)]`), or careful structuring **fail** because:

> Cargo resolves features **before** considering target architectures, and it does not allow compiling the same dependency with different feature sets in the same build.

This limitation effectively **dooms** all one-workspace solutions to failure when mixing native and wasm targets that require different dependency configurations.

---

## The Solution: Separate Target-Aligned Workspaces

To fully isolate build environments and avoid transitive incompatibility, the repo now maintains three clearly scoped workspaces:

### 🔁 High-Level Layout

```text
map-holons/
├── crates/
│   ├── holons-core/
│   ├── holons-guest/
│   ├── holons-client/
│   ├── holons-tests/
│   └── ...
├── wasm/                  # WASM-only workspace
│   └── Cargo.toml
├── native/                # Native-only workspace
│   └── Cargo.toml
├── test/                  # Test runners
│   └── Cargo.toml
```



## The Solution: Split Workspaces

To work around this, we now maintain **three top-level workspaces**, each with a strict boundary around the types of crates and dependencies it supports.

## Workspace Definition

### 🧩 Workspace Comparison Table

This table summarizes the characteristics, constraints, and crate membership of each workspace in the `map-holons` codebase.

| Category / Crate           | `wasm/` 🧬                        | `native/` 🖥️                | `test/` 🧪                   |
|----------------------------|-----------------------------------|------------------------------|------------------------------|
| **Target Platform**        | `wasm32-unknown-unknown`          | Native (e.g. x86_64 Linux)   | Native                       |
| **Purpose**                | Build zomes & WASM-safe libs      | Build native clients & tools | Run async integration tests  |
| **Runtime Container**      | Holochain Conductor (WASM guest)  | Tauri shell or CLI binary    | Holochain Sweetest framework |
| **Tokio Support**          | 🚫 Not allowed                    | ✅ Full support               | ✅ Full support               |
| **Threading**              | 🚫 Not supported                  | ✅ Allowed                    | ✅ Required by test framework |
| **Zome Code Allowed**      | ✅ Yes                             | ❌ No                         | ❌ No                         |
| **Use of `hdk`**           | ✅ With `default-features = false` | ✅ Full features              | ✅ Full features              |
| **Can use `tokio::spawn`** | ❌ No                              | ✅ Yes                        | ✅ Yes                        |
| **Can use `.block_on()`**  | ❌ No                              | ✅ Yes                        | ✅ Yes                        |
| **Build Target**           | Compile-only                      | Build & run                  | Test-only                    |
| **Executor Runtime**       | Conductor-driven async            | Tokio                        | Tokio                        |
| **Shared Crate Rules**     | Must be WASM-safe                 | May use full native deps     | May use full native deps     |

---

### 🧱 Crate Allocation

| Crate Name                 | `wasm/` 🧬 | `native/` 🖥️ | `test/` 🧪 |
|----------------------------|------------|---------------|------------|
| `holons` (zome)            | ✅          | ❌             | ❌          |
| `holons_integrity` (zome)  | ✅          | ❌             | ❌          |
| `holons-core`              | ✅          | ✅             | ✅          |
| `holons-guest`             | ✅          | ❌             | ❌          |
| `holons-guest-integrity`   | ✅          | ❌             | ❌          |
| `holons-client`            | ❌          | ✅             | ❌          |
| `holons-trust-channel`     | ✅          | ✅             | ❌          |
| `holon-dance-builders`     | ✅          | ✅             | ✅          |
| `type_system/*`            | ✅          | ✅             | ✅          |
| `shared_validation`        | ✅          | ✅             | ✅          |
| `holons-tests` (sweetests) | ❌          | ❌             | ✅          |

---

> ✅ = Included in workspace  
> ❌ = Excluded from workspace  
> ⚠️ Zome crates (`holons`, `holons_integrity`, etc.) are only compiled to `.wasm` and loaded dynamically at runtime

---

## Rationale for Each Crate

| Crate              | Workspace(s) | Notes |
|--------------------|--------------|-------|
| `holons-core`      | Both         | Must remain WASM-safe; no Tokio or MIO dependencies |
| `holons-guest`     | `wasm/`      | Zome logic; uses `hdk` with `default-features = false` to avoid Tokio |
| `holons-client`    | `native/`    | Native Rust client; allowed to use Tokio, MIO, full Holochain stack |
| `holons-tests`     | `native/`    | Test runners; may depend on Tokio and native-only crates |
| `shared`/utils/etc | Varies       | Must be evaluated for WASM safety if used in both workspaces |

---

## Key Developer Practices

- ✅ **Never run `cargo build --workspace` from repo root** — always specify the correct workspace.
- ✅ **Verify WASM compatibility** with:
  ```bash
  cargo check --manifest-path wasm/Cargo.toml --target wasm32-unknown-unknown
  ```
- ✅ Use `default-features = false` for `hdk` in all zome code.
- ❌ Never use `tokio::spawn`, `std::thread::spawn`, or `.block_on` in crates shared with WASM targets.
- ✅ Use `.dev/IDE_SETUP.md` to configure multi-workspace awareness in RustRover or VSCode.

---

# Async Trait Do’s and Don’ts in WASM Containers (Wasm Cheat Sheet)

These guidelines cover the **safe and unsafe ways to use async traits and functions** in crates that compile to `wasm32-unknown-unknown`, such as those intended to run in WASM.

> 🧠 Reminder: In WASM containers, threading is unavailable and blocking is illegal.  
> All async operations in guest WASM code must be non-blocking and are suspended at .await. Execution is resumed by the Holochain Conductor’s async host runtime, which manages guest execution from outside the WASM sandbox.

| Pattern                                  | ✅/❌ | Notes                                      |
|------------------------------------------|-----|--------------------------------------------|
| `async fn` in traits or impls            | ✅   | Non-blocking                               |
| `.await` inside async fn                 | ✅   | Standard usage                             |
| `.block_on(...)`                         | ❌   | Will panic in WASM                         |
| `tokio::spawn(...)` or threads           | ❌   | Not supported in `wasm32-unknown-unknown`  |
| `wasm_bindgen_futures::spawn_local(...)` | ✅   | Use this for running async in sync context |

---

## Test Workspace Design

The `test/` workspace includes:

- ✅ `sweetests`: async test harness using `holochain[sweettest]`
- ✅ Full Tokio runtime
- ❌ No WASM crates or zome logic — to avoid `hdk` cross-contamination

## Conclusion

This three-workspace structure ensures:

- ✅ **Clean separation of concerns**
- ✅ **Reliable build behavior** across WASM and native
- ✅ **Test crates no longer break zome crates**
- ✅ **Tokio stays out of WASM**, but can thrive in native/test code

> 🧠 Cargo's unified feature resolution means "just be careful" isn't enough. This structure is **the only reliable path** to cross-target compatibility in a monorepo setting.

Use this architecture as the default model for all MAP/Holons development going forward.


## Caveats & Developer Notes

- **Never build both workspaces together** (e.g., don’t `cargo build --workspace` from the repo root).
- Be mindful of **feature usage in shared crates** — even indirect dependencies can cause contamination.
- Use `default-features = false` on `hdk` in `holons-guest` to avoid pulling in Tokio.
- If adding a dependency to `holons-core`, always verify that it compiles to `wasm32-unknown-unknown`.
- Consider using `#[cfg(...)]` blocks in shared code to gate platform-specific functionality.

---


### 🔍 Tips

- Consider injecting an `AsyncSpawner` trait if you want to abstract away the use of `spawn_local` vs. `tokio::spawn`.
- Use feature flags to provide different executor backends in `native` vs. `wasm` builds — but only from crates that are *not* shared between workspaces.
- Always verify your WASM crates with:
  ```bash
  cargo check --target wasm32-unknown-unknown
  ```

---

### ✅ Summary

| Pattern                              | Allowed in WASM? | Notes |
|--------------------------------------|------------------|-------|
| `async fn` in traits and impls       | ✅               | Safe — async syntax alone is non-blocking |
| Calling `async fn` from `async fn`   | ✅               | Use `.await` |
| Calling `async fn` from `fn` via `spawn_local` | ✅        | Standard pattern in WASM |
| Calling `async fn` from `fn` without `.await` or `spawn_local` | ❌ | Future won't run |
| Using `.block_on(...)`               | ❌               | Not allowed — no thread to block |
| Spawning threads or tasks            | ❌               | Not supported in WASM without threads |

---

Use this cheat sheet when writing or reviewing shared trait interfaces and service implementations in the WASM workspace — especially within `holons-core` and `holons-guest`.

---

## Conclusion

This dual-workspace setup is a necessary architectural change driven by Cargo’s unified feature resolution model — a subtle, global behavior that invalidates many otherwise reasonable dependency strategies when working across targets like native and WASM.

Now that this is in place, we can:

- Reliably isolate incompatible dependencies
- Share common code across platforms (safely)
- Build cleanly for both native and WASM targets
- Avoid the tail-chasing and brittle patching that have plagued the project for the last year

This architecture should now be considered the **canonical structure** for all MAP/Holons projects targeting both native and WASM runtimes.


---

## Addendum: Testing Strategy and Workspace Allocation

### Overview

Our test infrastructure, including all integration tests, fixtures, and test executors, now lives **exclusively in the native workspace**.  
This decision aligns with both the technical requirements of the `sweettest` framework and the architectural split we’ve established between **native** and **WASM** targets.

### Why Tests Must Run in the Native Workspace

The [`sweettest`](https://docs.rs/sweettest) testing framework—used extensively in our Holochain integration tests—relies on a **multithreaded, asynchronous runtime** provided by **Tokio**. This includes:

- Spawning multiple Holochain conductors concurrently
- Running asynchronous test cases across threads
- Managing native filesystem and networking resources

Because **WASM targets cannot spawn threads** (and `wasm32-unknown-unknown` in particular lacks thread and socket support), any attempt to compile or execute the test framework in a WASM workspace is inherently incompatible.

> ⚠️ Even though the test crates may not directly import Tokio, transitive dependencies from the Holochain HDK and testing harness will always bring it in.

### Symptoms of the Old Setup

In the previous single-workspace model, our test crates were included alongside both native and wasm-targeted code. This led to:

- **Intermittent build failures** — depending on Cargo’s feature resolution order
- **Unpredictable success** — some tests appeared to compile when Tokio features weren’t yet unified into the dependency graph
- **Spurious “it used to work” moments** — caused by Cargo reusing cached build artifacts that hadn’t yet been poisoned by Tokio-enabled dependencies

Now that we understand **unified feature resolution**, it’s clear why these partial fixes failed: once any crate in the workspace enabled Tokio (via the Holochain HDK defaults), *every crate in that build graph inherited it*, including those targeting WASM.

### The Correct Allocation

| Category             | Workspace | Notes |
|----------------------|-----------|-------|
| `holons-tests`       | **native** | Runs Sweettest integration suites and async conductors |
| Test fixtures        | **native** | Depend on Tokio and local Holochain services |
| Shared test helpers  | **native** | May reference HDK with default features |
| `wasm` tests (future) | **wasm** | Only if explicitly built for WASM using `wasm-bindgen-test` |

### Summary

All integration and system-level testing belongs in the **native workspace**.  
The **WASM workspace** remains strictly for buildable, deployable zomes and wasm-safe shared libraries.  
This separation not only eliminates the recurring test-related build conflicts we’ve faced but also formalizes a clean boundary between the **runtime environments** our code targets.

In short:

> 🧩 The native workspace is for *execution* and *testing*.  
> 🧬 The wasm workspace is for *compilation* and *deployment*.

This division finally resolves the historical instability in our test builds and provides a clear, maintainable structure for all future development.


--

## Addendum: Pitfalls, False Hopes, and Ensuring WASM-Safe and Native-Optimized Builds

### ⚠️ Beware! AI Tools will often recommend these as "certain" fixes

Over the course of developing this architecture, we’ve tried nearly every reasonable approach to isolate WASM-incompatible code (e.g., Tokio, Mio, native-only crates) while still enabling a unified build experience. AI tools often profess "perfect understanding" of your situation and suggest one or more of these will "absolutely" fix your problem.

They're wrong!

Unfortunately, many of these attempts **fail silently or inconsistently** due to how Cargo handles **unified feature resolution**.

Below is a breakdown of common strategies we explored — and why each one ultimately **fails** under unified feature resolution.

---

### ❌ Conditional Compilation with `#[cfg(target_arch = "wasm32")]`

**Why it’s tempting**: You can write platform-specific code paths like:

```rust
#[cfg(target_arch = "wasm32")]
fn spawn() { /* wasm-specific impl */ }

#[cfg(not(target_arch = "wasm32"))]
fn spawn() { tokio::spawn(...) }
```

**Why it fails**:  
Even if the Tokio-specific code path is never compiled on the wasm target, **Cargo still resolves and compiles all dependencies globally**.

If Tokio is anywhere in the feature graph, it (and all its dependencies like Mio) will be pulled in — even if they're not used in the wasm build.

> 💥 *The mere presence of the dependency poisons the build for wasm.*

---

### ❌ Feature Flags to “Turn Off” Native Code

**Why it’s tempting**: You can isolate native dependencies like so:

```toml
[features]
default = ["native"]
native = ["tokio"]

[dependencies]
tokio = { version = "...", optional = true }
```

Then write code like:

```rust
#[cfg(feature = "native")]
use tokio::spawn;
```

**Why it fails**:  
Even if `holons-guest` disables the `native` feature, **if any other crate in the workspace enables it**, **Cargo will resolve `tokio` into the global dependency graph** — for *every crate* that depends on that shared crate.

This happens **regardless of the target**, which means you can’t have one crate built with `tokio` and another without it — if they both depend on the same shared crate (`holons-core`, for example).

---

### ❌ Crate-Type Tweaks: Switching from `rlib` to `cdylib`, etc.

**Why it’s tempting**: You might try to influence linking or compilation behavior by changing crate types:

```toml
[lib]
crate-type = ["cdylib"]
```

**Why it fails**:  
This only affects how the final artifact is *linked* — not which dependencies Cargo resolves or compiles.  
Cargo still builds the full dependency graph **before** target-specific logic kicks in.

---

### ❌ Using `#[cfg(test)]` to Contain Test-Only Dependencies

**Why it’s tempting**: You may hope test dependencies are only compiled in test mode.

**Why it fails**:  
If tests live in a crate that’s part of the workspace (like `holons_test``), then any test-only dependencies are still resolved in the workspace feature graph.

Also, if `cargo test` runs from the top level and includes wasm-targeted crates, they still inherit the **unified dependency graph** — potentially pulling in Tokio or test harnesses that are native-only.

---

## ✅ Ensuring WASM Safety: What to Watch for in Crate Definitions

When designing crates for inclusion in the `wasm/` workspace, here’s what to verify:

### 📋 Checklist for WASM Compatibility

- ✅ No direct or indirect dependency on:
    - `tokio`, `mio`, `parking_lot`, `std::net`, `std::thread`, `std::time::Instant`
- ✅ `hdk` used with `default-features = false`:
  ```toml
  [dependencies.hdk]
  version = "0.3"
  default-features = false
  features = ["macros"]  # only what’s strictly needed
  ```
- ✅ Crate contains **no panic, spawn, or blocking** operations that assume threading or system IO.
- ✅ All timeouts or async operations use WASM-safe crates like:
    - `wasm-timer`
    - `futures::StreamExt` with delay
- ✅ Compilation passes for:
  ```bash
  cargo check --target wasm32-unknown-unknown
  ```

### 🧪 Optional: Use a WASM-specific test crate

If you want to test wasm code directly, use `wasm-bindgen-test` in a separate crate that only builds for WASM. These tests must run in a JS environment (e.g. via headless browser or Node).

---

## ⚡ Goals for Native Workspace: Maximize Async Capability

The native workspace (`native/`) can use full multithreaded async runtimes. When targeting native builds:

- ✅ Enable full `tokio` and Holochain HDK defaults.
- ✅ Allow integration with:
    - `sweettest`
    - `holochain_client`
    - `libsqlite3`, filesystem, local sockets, etc.
- ✅ Use `#[tokio::test]` or `#[test]` with multi-conductor orchestration.

Note that `holons-core`, being shared, cannot assume multithreading — but native-specific crates like `holons-client` and `holons-tests` can freely use `tokio::spawn`, `JoinSet`, etc.

---

## 🧠 Conclusion

Understanding **why** the common partial fixes fail is just as important as applying the correct solution.  
Most of these attempts — `cfg`s, feature flags, crate types, and test scoping — are invalidated by **Cargo's global, target-agnostic, unified feature resolution**.

This reinforces our architectural boundary:

> **Two separate workspaces is not a workaround — it’s the only reliable strategy.**

This separation guarantees:
- Predictable builds
- No accidental Tokio leaks into WASM code
- Full async runtime support in native clients and tests

Our development workflow and repo structure should now be fully aligned with these constraints.