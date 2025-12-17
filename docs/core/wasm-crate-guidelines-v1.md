# Workspace Strategy: Native, WASM, and Test Build Targets in the Holons Codebase

# NOTE: This doc is outdated

This document describes our initial attempt at build isolation. [Issue #337](https://github.com/evomimic/map-holons/issues/337) implements an improved strategy. 

## Summary

The `map-holons` monorepo is structured around **three distinct Cargo packages**, each targeting a different runtime environment:

1. 🧬 `wasm/` — WebAssembly (WASM) builds for Holochain zome execution
2. 🖥 `native/` — Native builds (e.g., Tauri clients, local services)
3. 🧪 `test/` — Test runners and fixtures (e.g., `sweetests` integration suite)

These packages are not unified into a single Cargo workspace build. Instead, each is responsible for declaring and managing its own dependency graph, allowing for **clean separation of feature sets and build targets**.

We **retain a root-level `Cargo.toml` workspace file**, but only for:

- ✅ IDE and tool awareness across packages (e.g., RustRover, `cargo metadata`)
- ✅ A single-source-of-truth for dependency versions
- ⚠️ **Not** used to build or manage features across packages
- ⚠️ **Never** used with `cargo build --workspace`

Dependency versions from the root file are pushed to each leaf package using a Python script.

This architecture solves longstanding issues with Cargo’s **unified feature resolution**, and ensures builds remain clean, reproducible, and platform-safe across WASM and native targets.

---

## Why Not Use a Unified Workspace?

### The Core Problem: Tokio and WASM Don't Mix

Many crates in the Holochain ecosystem — including `hdk` and its dependencies — rely on **Tokio**, which in turn pulls in platform-specific dependencies like **Mio**, which do **not** compile to WASM (`wasm32-unknown-unknown`). Zome code, which runs inside a Holochain WebAssembly guest, must be **WASM-safe** and **must not** link against Tokio or its transitive dependencies.

This leads to a critical conflict: we want our **native code** (which can use Tokio) and our **zome code** (which must not) to coexist and share some logic.

### The Hidden Killer: Cargo’s Unified Feature Resolution

Cargo’s feature resolution is **global per build**, meaning:

> If any crate in the build graph enables a feature on a dependency, that feature is enabled for **all crates** using that dependency — even if it breaks the target platform.

This is **not conditional on platform**, and **not scoped to the consuming crate**.

#### Example:

- `holons-client` (native) depends on `hdk` with default features (includes Tokio).
- `holons-guest` (WASM) wants to depend on `hdk` with `default-features = false`.
- Because these share a workspace, Cargo resolves `hdk` with all features enabled.
- Even when building only `holons-guest` for WASM, Tokio and Mio are pulled in — and the build fails.

> ⚠️ Conditional compilation like `#[cfg(target_arch = "wasm32")]` does **not** prevent Cargo from including incompatible dependencies.

### Conclusion: Workspace Builds Are Inherently Unsafe for Mixed Targets

No amount of feature-flag gymnastics, conditional `cfg`, or dependency wrangling can make a single Cargo workspace build safely for both native and WASM — **not when using Holochain**.

---

## The Solution: Per-Target Packages + Metadata-Only Workspace

Instead of relying on a single Cargo workspace with conditional features, we use **three top-level packages**:

1. `workspaces/wasm/`
2. `workspaces/native/`
3. `workspaces/test/`

Each of these defines:

- Its own `Cargo.toml`
- Its own `[dependencies]` and `[features]`
- A dummy `lib.rs` if necessary to satisfy Cargo

These packages reference shared internal crates via **path dependencies**, ensuring they only compile with the appropriate features enabled for their target.

At the top level, we include a `Cargo.toml` workspace file, but it is:

- **Never used for building**
- Used **only by IDEs and tooling**
- Treated as a central list of shared dependency versions

A small Python script propagates version values from the root file into the leaf packages. This ensures consistency without invoking Cargo’s problematic workspace resolution behavior.

---

### 🚫 What We Explicitly Avoid

- ❌ `cargo build --workspace`
- ❌ `[workspace.dependencies]` used for feature propagation
- ❌ Workspace-level test or build orchestration
- ❌ Conditional features in shared crates intended for WASM

---

## 🔁 Repo Layout

```text
map-holons/
├── Cargo.toml               # 🧠 Metadata-only workspace (for IDEs/tools)
├── workspaces/
│   ├── wasm/                # 🧬 WASM-targeted build package
│   │   └── Cargo.toml
│   ├── native/              # 🖥️ Native-targeted build package
│   │   └── Cargo.toml
│   └── test/                # 🧪 Test-only build package
│       └── Cargo.toml
├── crates/                  # Shared crates used across 2+ targets
│   ├── holons-core/
│   ├── holons-guest/
│   ├── holons-client/
│   ├── holon-dance-builders/
│   ├── shared_validation/
│   └── ...
├── zomes/                   # Zome crates (WASM only)
│   ├── coordinator/holons/
│   └── integrity/holons_integrity/
├── tests/                   # 🧪 Integration test crates (native)
│   └── sweetests/
└── .dev/                    # Dev tooling configs (e.g., IDE_SETUP.md)
```

---

## Benefits of This Model

- ✅ Each build target has complete control over features and dependencies
- ✅ No target contamination via workspace resolution
- ✅ WASM builds stay clean — no Tokio, no native IO
- ✅ Native clients and test harnesses can use full async/threading
- ✅ IDEs still understand the full repo structure
- ✅ Centralized version declarations without workspace-induced poison

---

## TL;DR

> This is **not** a multi-workspace monorepo.  
> This is a **multi-package build graph** with one metadata-only workspace at the top for tooling only.

Never build the root. Always build from one of:

- `workspaces/wasm/`
- `workspaces/native/`
- `workspaces/test/`

These are the only valid entry points.

## Workspace Definition

### 🧩 Workspace Comparison Table

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

## Async & WASM Safety Guidelines

> For full details on Rust's WASM limitations **vs.** Holochain's additional constraints, see:
> - 📎 Appendix A: General WASM Constraints
> - 📎 Appendix B: Holochain Guest WASM Constraints

In short, in our **Holochain Guest WASM code** (which includes `holons_core`):

- ✅ `async fn` is allowed in **trait definitions** (for cross-platform abstraction)
- ❌ `async fn` is **not allowed in implementations** (trait impls or free functions)
- ❌ `.await` is **not allowed anywhere**
- ❌ Spawning tasks (`tokio::spawn`, `spawn_local`) or blocking (`block_on`, `thread::sleep`) is **never allowed**

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
  npm run build:wasm
  ```
  or
  ```bash
  cargo check --manifest-path wasm/Cargo.toml --target wasm32-unknown-unknown

  ```
- ✅ Use `default-features = false` for `hdk` in all zome code. 
- ✅ Use `.dev/IDE_SETUP.md` to configure multi-workspace awareness in RustRover or VSCode.



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

# 📎 Appendum: Holochain Guest WASM Constraints

Holochain Conductor executes zome code inside a strict, **synchronously invoked WebAssembly guest**. This sandboxed runtime has **no async executor**, no threads, and no way to suspend/resume futures. Execution must be **deterministic, synchronous, and single-threaded**.

This makes Holochain WASM guests significantly more constrained than general `wasm32-unknown-unknown` environments.

---

## ❌ Key Restrictions

| Pattern                              | Allowed in Holochain Guest? | Notes |
|--------------------------------------|------------------------------|-------|
| `async fn` in free functions         | ❌ No                        | Guest has no executor; async fns do not run |
| `.await` anywhere                    | ❌ No                        | Cannot suspend/resume; future never polled |
| `async fn` in trait definitions      | ✅ Yes                       | Allowed for cross-platform abstraction only |
| `async fn` in trait implementations  | ❌ No                        | Guest cannot poll the returned future |
| `tokio::spawn`, threads, `block_on`  | ❌ No                        | No threads, no background execution |
| `spawn_local`, JS-style async        | ❌ No                        | Not supported in Conductor environment |
| `#[hdk_extern]` functions            | ✅ Yes                       | Must be `fn`, return `ExternResult<T>` synchronously |
| HDK functions like `create_entry()`  | ✅ Yes                       | Appear async, but are made sync via host plumbing |

---

## 🧠 Why This Matters

Rust allows writing `async fn` and `.await`, even for WASM targets — but **Holochain does not execute guest code like a browser**.

The Conductor:

- Calls exported zome functions synchronously
- Does not embed an executor inside the guest
- Cannot poll or await a guest future
- Requires all logic to complete in a single call stack

Thus, any `.await` or `async fn` inside guest code is effectively a **no-op** — or worse, will cause logic to silently fail at runtime.

---

## ✅ Correct Structure for Zome Functions

You must write all guest code as **plain synchronous functions**.

```rust
#[hdk_extern]
fn my_zome_fn(input: MyData) -> ExternResult<HeaderHash> {
    create_entry(input) // ✅ this is sync (HDK abstracts over async)
}
```

Do **not** do this:

```rust
#[hdk_extern]
async fn bad_zome_fn(input: MyData) -> ExternResult<HeaderHash> {
    // ❌ async zome handlers are not supported
    let result = create_entry(input).await; // ❌ no .await allowed
    result
}
```

Even helper functions cannot be async:

```rust
async fn helper() -> ExternResult<()> {
    // ❌ this .await will never be executed
    let _ = get(some_hash).await?;
    Ok(())
}
```

---

## ✅ Trait-Based Abstractions (With Caution)

If you're building shared interfaces for use **both in native and guest contexts**, it's fine to use `async fn` in trait **definitions**, as long as:

- ✅ Guest implementations **are synchronous**
- ✅ Guest code **does not call trait methods directly as async**
- ❌ Do **not** `.await` anything in the implementation

```rust
// ✅ Trait definition is allowed
pub trait MyAction {
    fn do_work(&self) -> ExternResult<()>;
}

// ✅ Guest impl must be sync
impl MyAction for MyType {
    fn do_work(&self) -> ExternResult<()> {
        // no async calls
        Ok(())
    }
}
```

You **can** use `async fn` in trait definitions to support native contexts — just be careful not to call `.await` in guest implementations.

---

## ✅ Summary Table

| Use Case                                   | Allowed? | Strategy                                                  |
|--------------------------------------------|----------|-----------------------------------------------------------|
| `async fn` in shared trait definition      | ✅        | OK for abstraction                                        |
| `async fn` in trait impl in guest          | ❌        | Must use sync impl                                        |
| `.await` in any guest code                 | ❌        | Will fail or silently not run                             |
| HDK functions (e.g. `get`, `create_entry`) | ✅        | Synchronous interface in guest                            |
| Background work or task spawning           | ❌        | Not possible in guest                                     |
| Running async logic                        | ✅        | Only in **host** code (e.g., native client, test harness) |

---

## 🛠 Refactoring Tip

If you need to write shared logic that includes async operations:

- ✅ Implement as `async fn` in shared crate
- ✅ In native workspace: use `.await` normally
- ❌ In guest: wrap or stub it out, or move the logic into host orchestration

Use `cfg` or trait-based boundaries if needed to isolate guest vs. host implementations.

---

## Final Note

Holochain's guest model is **not just a subset of WASM** — it's a specialized, deterministic, sync-only execution environment orchestrated by the host. Many "normal" Rust async patterns **will compile but break** in guest context.

Treat zome logic as **purely synchronous**, and handle all async orchestration **outside the guest**, in the Conductor or in native/test code.