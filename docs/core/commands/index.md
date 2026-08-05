# MAP Commands

The commands section owns the command model, dispatch, command-specific runtime
structures, undo and redo behavior, and command-owned schema concepts.

The word `Runtime` used by the command design may name a command-related Rust
structure. It does not make commands the owner of the MAP core runtime.

This directory is the target replacement for `commands-and-runtime/`. Content
will move after it has been classified under the
[document role manifest](../document-role-manifest.md).
