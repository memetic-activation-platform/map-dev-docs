# 🧬 MAP / Holons WASM Build Guidelines

## Overview

This document describes the conventions and constraints for building **WebAssembly (WASM)** targets in the **MAP Holons** codebase — specifically the **guest-side Holochain hApp**.

In this architecture:
- The **`happ/` workspace** builds the Holochain zomes (guest-side logic).
- The **`host/` workspace** builds the native Tauri runtime and clients.
- The **`crates/` directory** holds shared code that must remain **WASM-safe**.
- The **`tests/` workspace** runs native integration tests using **Sweettest**.

The goal is a **hybrid monorepo** that maintains strict build isolation between WASM and native targets while keeping shared code ergonomic and consistent.

---

## 🧱 WASM Workspace Purpose

The `happ/` workspace (formerly `wasm/`) produces the **guest-side build artifacts**:
- `.wasm` binaries for each zome
- `dna.yaml` and `happ.yaml` definitions (in `workdir/`)
- Optional Holochain-specific metadata (integrity, coordinator zomes)

These builds target the Holochain conductor runtime and must conform to **Holochain Guest WASM constraints** (see below).

---

## 📂 Directory Structure

~~~
map-holons/
├── Cargo.toml                  # Unified workspace metadata (for tooling only)
├── crates/                     # Shared dual-target crates (WASM-safe)
│   ├── base_types/
│   ├── core_types/
│   ├── holons_core/
│   ├── holons_prelude/
│   ├── holon_dance_builders/
│   ├── shared_validation/
│   └── ...
│
├── happ/                       # 🧬 Guest-side hApp (Holochain zomes)
│   ├── Cargo.toml              # WASM build target configuration
│   ├── crates/
│   │   └── holons_guest/       # Guest zome logic
│   ├── zomes/
│   │   ├── coordinator/holons/
│   │   └── integrity/holons_integrity/
│   └── workdir/
│       ├── dna.yaml
│       ├── happ.yaml
│       └── web-happ.yaml
│
├── host/                       # 🖥️ Host-side runtime (clients + adapters)
│   ├── tauri-app/              # Rust client orchestrator (Tauri command handlers)
│   ├── crates/                 # Client + adapter crates
│   └── ui/                     # Frontend code (TypeScript)
│
└── tests/                      # 🧪 Integration & sweetests suite
└── sweetests/
~~~

---

## ⚙️ Building the hApp

From the repo root or `happ/` directory:

cargo build --manifest-path happ/Cargo.toml --target wasm32-unknown-unknown --release

This produces `.wasm` binaries for each zome inside:
happ/target/wasm32-unknown-unknown/release/

Use `hc dna pack` and `hc app pack` to package your zomes into DNA/hApp bundles defined in `workdir/`.

---

## ✅ Shared Crate Rules for WASM Safety

Crates under `crates/` may be used by both the **host** and **happ** workspaces, but they must satisfy WASM safety rules.

| Rule | Description | Example |
|------|--------------|----------|
| **No Tokio / async executors** | WASM cannot spawn or block threads | ❌ `tokio::spawn()` |
| **No native I/O** | No filesystem, sockets, or native concurrency | ❌ `std::fs::File`, `std::net` |
| **No `std::thread`** | No threading in guest WASM | ❌ `thread::spawn()` |
| **No `block_on`** | Holochain guest has no async runtime | ❌ `futures::executor::block_on()` |
| **Pure sync functions only** | Guest must be deterministic and single-threaded | ✅ normal `fn` |
| **`async fn` allowed only in traits** | Enables abstraction across host + guest | ✅ trait `async fn` definitions only |
| **`hdk` must be built with `default-features = false`** | Avoid Tokio contamination | ✅ `[dependencies] hdk = { version = "0.5", default-features = false }` |

---

## 🚫 Common Pitfalls

| Pattern | Why It Fails |
|----------|--------------|
| `tokio::spawn` or `spawn_local` | WASM guest has no scheduler or threads |
| `.await` in guest code | No async executor; the future never polls |
| Using HDK with default features | Pulls Tokio and Mio (breaks WASM build) |
| Writing to filesystem | No file access inside guest sandbox |
| Spawning background tasks | Non-deterministic; forbidden by Holochain runtime |

---

## 🧩 Integration with Host Workspace

Although the `happ` and `host` workspaces are isolated for build safety, they **interoperate at runtime**.

### Flow:
1. The `host` workspace builds and runs the Tauri application.
2. It launches a **Holochain Conductor** that loads `.dna` and `.wasm` artifacts from `happ/workdir/`.
3. Guest zomes (compiled to `.wasm`) execute within the conductor sandbox.
4. Communication occurs via the **Conductor API**, using Rust client adapters and `TrustChannel` orchestration.

### Important:
- The `host` never compiles the guest zomes.
- The `happ` never links to native crates or Tokio.
- They interact only via the conductor and well-defined serialization boundaries.

---

## 🔒 Build Isolation Summary

| Target | Workspace | Features | Build Command |
|--------|------------|-----------|----------------|
| **Guest (WASM)** | `happ/` | `default-features = false` | `cargo build --target wasm32-unknown-unknown` |
| **Host (Native)** | `host/` | full features allowed | `cargo build --manifest-path host/Cargo.toml` |
| **Tests** | `tests/` | full features allowed | `cargo test --manifest-path tests/Cargo.toml` |

The root `Cargo.toml` is **metadata-only** and **never built directly**.

---

## 🧠 Quick Reference — Guest vs Host Rules

| Capability | Guest (WASM) | Host (Native) |
|-------------|---------------|----------------|
| Async I/O | ❌ No | ✅ Yes |
| Threads | ❌ No | ✅ Yes |
| Filesystem Access | ❌ No | ✅ Yes |
| Network Access | ❌ No | ✅ Yes |
| `tokio::spawn()` | ❌ No | ✅ Yes |
| `block_on()` | ❌ No | ✅ Yes |
| `async fn` (traits) | ✅ Allowed | ✅ Allowed |
| `async fn` (impls) | ❌ No | ✅ Yes |
| HDK Use | ✅ With `default-features = false` | ✅ With full features |

---

## 🧩 Developer Workflow

1. Build and pack the guest WASM zomes:
    - `npm run build:happ` or `cargo build --manifest-path happ/Cargo.toml --target wasm32-unknown-unknown`
    - `hc app pack happ/workdir`

2. Build and run the host:
    - `npm run tauri:dev` or `cargo tauri dev --manifest-path host/tauri-app/Cargo.toml`

3. The host automatically loads the `happ/workdir/happ.yaml` bundle and initializes the conductor.

4. Integration tests (under `tests/`) run against this conductor instance using Sweettest.

---

## 🧩 Key Design Principle

> The `happ/` workspace is **strictly deterministic, synchronous, and platform-agnostic**.  
> The `host/` workspace provides all **asynchronous orchestration, networking, and persistence**.

---

## ✅ Summary

- The **`happ/` workspace** compiles the Holochain guest WASM (zomes)
- The **`host/` workspace** provides runtime orchestration and UI integration
- Shared crates must be **WASM-safe**
- No async runtime or Tokio in guest code
- The root workspace file is **metadata-only**
- Each workspace maintains its own build isolation and Cargo.lock

This structure guarantees:
- Safe, reproducible builds across WASM and native targets
- Deterministic guest logic
- Flexible, async-capable host orchestration
- Seamless integration within a single monorepo

---

🧠 *Remember:*
> The hApp executes **inside the Holochain conductor sandbox**,  
> not in a browser or async runtime.  
> Every zome function must complete synchronously and deterministically.

## Appendix A — Why This Layout Works

Cargo resolves dependency features globally.  
If a WASM-safe crate and a Tokio-enabled crate live in the same build graph, Cargo unifies their features — breaking the WASM build.  
By separating `happ/` (guest) and `host/` (native) physically, we prevent that contamination while keeping shared crates reusable.

---

## Appendix B — Holochain Guest Execution Rules

Holochain executes guest WASM synchronously:

| Pattern | Allowed? | Notes |
|----------|-----------|-------|
| `async fn` in free functions | ❌ | Guest runtime has no executor |
| `.await` usage | ❌ | Futures never polled |
| `async fn` in traits | ✅ | For abstraction only |
| HDK externs (`#[hdk_extern]`) | ✅ | Must be synchronous |
| Background tasks (`tokio::spawn`) | ❌ | Not supported |
| Multi-threading | ❌ | Deterministic, single-threaded only |

> The Conductor handles async orchestration. The guest is pure logic.

---

## Conclusion

This **host–hApp hybrid workspace** structure is the canonical model for all Holons and MAP projects.
It combines:
- Clean separation between host and guest build targets
- Centralized dependency management
- Reliable cross-platform builds
- IDE-friendly unified workspace metadata

> 🧬 **hApp = guest logic (inside conductor)**  
> 🧑‍💻 **Host = conductor + client orchestration layer**

Together, they form a robust architecture that’s **WASM-safe**, **native-optimized**, and **test-ready**.

---

## Appendix C — Workdir and Bundle Layout

The `workdir/` directory acts as the **bridge between Rust builds and Holochain runtime artifacts**, serving as the staging area for packaging, configuration, and testing.

### 📁 Default Layout (Holons — Single hApp Repo)

In the Holons codebase, the `workdir/` resides at the **repository root**, not inside `happ/`.  
This makes it globally accessible to **host**, **guest**, and **test** environments alike.

~~~text
map-holons/
├── Cargo.toml
├── crates/
├── happ/
│   ├── zomes/
│   ├── crates/
│   └── Cargo.toml
├── host/
│   ├── crates/
│   └── Cargo.toml
├── tests/
│   └── sweetests/
│
├── workdir/                     # 🧩 Holochain hApp packaging + runtime state
│   ├── dna.yaml                 # DNA manifest (declares zomes and wasm paths)
│   ├── happ.yaml                # hApp manifest (declares DNAs and roles)
│   ├── bundles/                 # Built .dna and .happ bundles (hc pack outputs)
│   │   ├── holons.dna
│   │   └── holons.happ
│   ├── conductor-config.yaml    # (Optional) used for local conductor/sweettest
│   ├── storage/                 # (Optional) persisted Holochain DHT data
│   └── temp/                    # (Optional) transient conductor state or logs
~~~

### 🧱 Purpose and Responsibilities

| File / Folder                        | Purpose                                                                                                                                                                                                                        |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `dna.yaml`                           | Defines which zomes (and which `.wasm` builds) are included in the DNA.                                                                                                                                                        |
| `happ.yaml`                          | Defines which DNAs make up the hApp and their roles.                                                                                                                                                                           |
| `bundles/`                           | Output directory for packaged `.dna` and `.happ` bundles.                                                                                                                                                                      |
| `conductor-config.yaml` *(reserved)* | **Reserved for future use.** Will eventually define local conductor runtime configuration (environment path, networking, and installed apps) once the merged Conductora runtime is stabilized. Not currently required or used. |
| `storage/`                           | Persistent DHT data for long-running test conductors or local development.                                                                                                                                                     |
| `temp/`                              | Temporary working directory for transient conductors and ephemeral runs.                                                                                                                                                       |

---

> ⚠️ **Note:**  
> The `conductor-config.yaml` entry is intentionally **not yet part of the active Holons toolchain**.  
> All conductor initialization is currently handled programmatically through the runtime (e.g., `TauriConductorConfig`) or the test harness.  
> This placeholder simply reserves the filename and location so that when configuration-file-based launches are reintroduced later, no structural changes to `workdir/` will be required.

### 🧩 Build and Packaging Flow

1. **Build the zomes (hApp WASM):**
   ~~~bash
   cargo build --manifest-path happ/Cargo.toml --target wasm32-unknown-unknown --release
   ~~~

2. **Package DNA:**
   ~~~bash
   hc dna pack workdir/
   ~~~

3. **Package hApp:**
   ~~~bash
   hc app pack workdir/
   ~~~

4. **Result:**
   ~~~bash
   workdir/bundles/holons.dna
   workdir/bundles/holons.happ
   ~~~

---

### ⚙️ Usage in Tests and Runtime

Both the **`host/` conductor** and the **`tests/sweetests/` harness** load hApps directly from the `workdir/`.

**Example — in Sweetest or conductor launch code:**
```rust
let happ_path = PathBuf::from("workdir/bundles/holons.happ");
let conductor = Conductor::builder()
 .with_happ(happ_path)
 .spawn()
 .await?;