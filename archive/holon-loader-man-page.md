# HOLON-LOADER(1) — Manual Page

## NAME
**holon-loader** — JSON Holon Loader for MAP / Conductora environments

## SYNOPSIS
**holon-loader** <command> [*options*] <path …>

## DESCRIPTION
`holon-loader` parses, validates, resolves, and commits JSON Holons into a
target HolonSpace using an embedded Conductora runtime.

Input paths may be JSON files or directories. Directories are scanned
recursively for `*.json`. Processing order is deterministic (lexicographic).

**Validation schema**: The loader uses a **built-in, fixed JSON Schema** that
matches the parser. Callers do **not** supply schema files.

## COMMANDS
**load**
: Parse, validate, resolve, and commit holons into the target HolonSpace.
Supports dry-run.

**validate**
: Parse and validate holons without committing. Produces a validation report.

**version**
: Print version and build information, including the loader’s **schema version**.

## OPTIONS

### General
`-v`
: Increase verbosity. **Repeatable** (e.g. `-vvv`). Each additional `-v` raises the log level, capped at the maximum (debug).

`-q`
: Quiet mode; only errors are printed. Overrides any `-v` flags.

`--format` *text|json*
: **Output format** for results and reports.  
- `text` — human-readable summaries (default).  
- `json` — machine-readable structured output (for scripting and integration).  
*Affects only output; inputs are always JSON files.*

### Target HolonSpace
One of the following must be provided:

`--space-id` *hash*
: Exact HolonSpace ID (ActionHash).

`--space-key` *Type:Key*
: Resolve HolonSpace by type and key (e.g., `Space:PlanetProject.Core`).

`--create-space` *name*
: Create a new HolonSpace with the given name if it does not exist.

`--space-config` *path*
: Path to **space.json** describing the space to create.  
*Current schema: `{ "name": "<string>", "description": "<string>" }`.*

Resolution precedence:
1. `--space-id`
2. `--space-key`
3. `--create-space` (with optional `--space-config`)  
   Else → error: *“No HolonSpace specified.”*

### Loader Behavior
`-n`, `--dry-run`
: Do everything except commit.

`--deny-externals`
: Forbid references to external spaces (default).

`--allow-externals`
: Allow references to external spaces via proxy map.

`--proxy-map` *path*
: Proxy map file used when `--allow-externals` is enabled.

`--fail-fast`
: Abort on first validation error.

`--max-errors` *n*
: Maximum number of errors to collect before aborting (default: 50).

## INPUTS
- One or more file or directory paths.
- Files: processed if they end with `.json`.
- Directories: scanned recursively for `*.json`.
- Non-JSON files are ignored.
- Mixed paths allowed; final list is the deterministic union.

## FILES
**\*.json**
: Holon import files. Each file must contain one or more Holon definitions in the MAP JSON import format.

**space.json**
: Optional configuration file for `--space-config` when creating a HolonSpace. **Currently supports only**:  
- `name` (string)  
- `description` (string)

*(No external schema files are used; validation relies on the loader’s fixed internal schema.)*

## EXAMPLES
Validate all JSON files under `./imports`:

```
holon-loader validate ./imports --space-id id:uhCk123…
```

Load with dry-run and verbose output:

```
holon-loader load ./set -n -vv \
  --space-key Space:PlanetProject.Core
```

Create a new space and load into it (space.json with name/description):

```
holon-loader load ./data \
  --create-space Catalist.Sandbox \
  --space-config ./space.json
```

Emit machine-readable JSON:

```
holon-loader validate ./imports --format json --space-id id:uhCk123…
```

## EXIT STATUS
`0` — success  
`1` — validation error  
`2` — reference resolution error  
`3` — commit error  
`4` — configuration or environment error

## SEE ALSO
**holochain(1)**, **hc(1)**, MAP documentation.

## NOTES
- Input order is stable and deterministic.
- HolonSpace currently supports only `name` and `description`.
- When future HolonSpace policy is introduced, it will take precedence over CLI flags.