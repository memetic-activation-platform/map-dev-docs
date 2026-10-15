# Data Loader native source verification

This records implementation evidence for [the Data Loader design](data-loader-design-spec.md)
and DL-05 / map-holons #779. Supported desktops are macOS and Linux.

## Backend capability matrix

The implementation uses RFD 0.17.2, Cocoa NSOpenPanel on macOS and the XDG
Desktop Portal backend on Linux (with the library's Zenity fallback). API/source
inspection establishes the following capabilities; it does not establish that
native interaction has passed on a particular desktop.

| Capability | macOS | Linux |
| --- | --- | --- |
| Multiple files | Exposed by backend | Exposed by backend |
| Directory with recursive host discovery | Exposed by backend | Exposed by backend |
| Multiple directories | Exposed by backend | Exposed by backend |
| Mixed files/directories in one selection | Exposed by macOS-only API | Not exposed; interim separate-choice modes |
| Cancellation | Optional selection result | Optional selection result |
| Native smoke verification | Unverified: automation timed out on macOS 26.5.2 arm64 | Pending; Linux desktop unavailable in current environment |

Evidence: [RFD 0.17.2 file dialog source](https://docs.rs/rfd/0.17.2/src/rfd/file_dialog.rs.html)
and [backend/runtime requirements](https://docs.rs/rfd/0.17.2/rfd/).
Linux deployment needs a working desktop portal backend and Zenity as documented
by RFD. Record distribution, desktop environment, session type (X11/Wayland), and
portal backend/version when testing. Do not claim all Linux desktops have been
verified from a single environment.

The RFD API returns an optional selection rather than a structured native error.
Some backend failures can therefore look like dismissal. MAP reports command
failures and discovery/read errors separately, but cannot recover information
that the native library discarded. This limitation remains explicit.

## Executable verification

From map-holons, enter `nix develop`, then run:

```sh
cargo run --manifest-path host/Cargo.toml -p Conductora --example source_picker -- mixed
cargo run --manifest-path host/Cargo.toml -p Conductora --example source_picker -- files
cargo run --manifest-path host/Cargo.toml -p Conductora --example source_picker -- directories
```

Use `mixed` on macOS; Linux rejects it with an explicit unsupported-mode error.
The harness invokes the same picker/discovery implementation as Conductora's
`select_loader_sources` command. It prints retained content as well as paths:
use test fixtures, not sensitive documents, when capturing its output.

Verify files, nested directories, multiple directories, overlapping selections,
and same-basename JSON files. Cancel the picker and check `status: cancelled`.
Confirm an empty directory and check `status: selected` with an empty source list.
Repeat native checks on both platforms. The harness creates no MAP transaction.

Automated coverage lives in Conductora's `source_ingress::discovery` tests and
`host/ui/src/app/services/loader-source.test.ts`. Existing runtime test
`preparation_builds_isolated_transient_graphs_without_execution` verifies separate
`/one/import.json` and `/two/import.json` bundle provenance through preparation.

## Validation recorded

On macOS 26.5.2 arm64, the host source-discovery tests passed (5), the existing
preparation provenance regression passed (1), and the web suite passed (299,
1 skipped), including six source-adapter tests. `npm run check` and
`npm run fmt:check` passed. The native example compiled and was launched, but the
computer-use service timed out before selection/cancellation could be verified.
The test process was stopped; launching alone is not a native smoke-test pass.
Linux compilation and native interaction have not been verified in this environment.

## Remaining scope

Production ActionVisualizer integration and review UI remain DL-07 and DL-06.
Linux mode-free mixed selection is tracked by
[map-holons #780](https://github.com/evomimic/map-holons/issues/780); an interim separate-choice picker does not complete that goal.
Native smoke evidence must be recorded before claiming platform verification is
complete. #779 remains subject to those verification criteria.
