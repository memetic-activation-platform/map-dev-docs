# MAP Commands

The commands section owns the command model, dispatch, command-specific runtime
structures, undo and redo behavior, and command-owned schema concepts.

`MAP Commands Schema-v0.1.0` is a separately loadable package at
`map-holons/schema-src/commands/schema.tdl`. It depends on `MAP Core
Schema-v0.0.7` and `MAP Dance Schema-v0.1.0`; Core contains no Command symbols
or affordance occurrences. Commands owns `CommandType`, concrete core command
descriptors, `AffordsCommand` / `CommandAffordedBy`, command affordance
occurrences, and command payload relationships.

The word `Runtime` used by the command design may name a command-related Rust
structure. It does not make commands the owner of the MAP core runtime.

This directory is the target replacement for `commands-and-runtime/`. Content
will move after it has been classified under the
[document role manifest](../document-role-manifest.md).
