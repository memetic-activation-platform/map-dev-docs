# DAHN Path Inspector Interaction Grammar

**Version:** 0.2

## Status

Draft normative specification for the Path Inspector spatial interaction model.

## Change Log

### v0.2

Refines the interaction grammar around an explicit two-dimensional grid and retained navigation paths.

- Establishes the **2D grid as the stable geometric substrate** of the Path Inspector.
- Establishes that **columns own width**: every cell in a column receives the same width, and horizontal compression or expansion applies to the entire column.
- Establishes that **rows own height**: every cell in a row receives the same height, and vertical compression or expansion applies to the entire row.
- Defines a cell's spatial budget as the intersection of its row height and column width.
- Separates **grid position**, **occurrence identity**, and **semantic Holon identity**.
- Clarifies that grid coordinates may change through row or column insertion without changing occurrence identity or navigation provenance.
- Distinguishes **replaceable leaf occurrences** from occurrences that have become part of a retained navigation path.
- Allows a newly selected child to replace an existing child while that child remains an untraversed leaf.
- Requires an occurrence to be retained once navigation has continued through it.
- Requires selection of an alternative child from an earlier anchor to create an additional occurrence rather than overwrite a retained path.
- Introduces **row and column insertion** as the mechanism for accommodating those additional occurrences while preserving existing navigation provenance.
- Explicitly permits **sparse/empty cells** when necessary to preserve truthful navigation geometry.
- Recasts compression combinations as emergent consequences of row and column allocation rather than separately enumerated Path Inspector states.

The central refinements introduced in v0.2 are:

> **The grid owns geometry; occurrences occupy cells.**

> **Rows own height; columns own width.**

> **Coordinates may move; provenance does not.**

> **Replace an untraversed leaf; insert to preserve a traversed path.**

### v0.1

Initial interaction grammar.

Established:

- occurrence-based retained navigation topology;
- horizontal traversal for structurally singular affordances;
- vertical, collection-mediated traversal for structurally plural affordances;
- stable attachment of descendants to the occurrence that produced them;
- focus-dependent projection;
- independent horizontal and vertical compression;
- distinction between compression and overflow;
- branch-local overflow;
- hidden-lineage discoverability;
- parent-owned external allocation and child-owned internal composition;
- state preservation across compression, overflow, scanning, and maximization;
- explicit distinction between traversal and re-rooting.

## Purpose and Authority

[Continue with the v0.2 grammar, incorporating the grid and retained-path insertion refinements below.]
---

# 1. Grid Vocabulary

## 1.1 Grid

The **grid** is the Path Inspector's stable two-dimensional geometric substrate.

It consists of ordered rows and columns.

The grid is stable in the sense that navigation, focus changes, compression, and occurrence substitution operate through row and column geometry rather than allowing individual cells to acquire incompatible dimensions.

The grid may grow by inserting rows or columns as retained navigation topology requires.

## 1.2 Row

A **row** is a horizontal grid band with one current height.

Every cell in that row receives that height.

Rows may be inserted as navigation topology grows.

## 1.3 Column

A **column** is a vertical grid band with one current width.

Every cell in that column receives that width.

Columns may be inserted as navigation topology grows.

## 1.4 Cell

A **cell** is the intersection of one row and one column.

A cell therefore receives:

    cell.width  = column.width
    cell.height = row.height

A cell may be occupied by an occurrence or may be empty.

An empty cell remains part of the grid and may be necessary to preserve truthful navigation geometry.

## 1.5 Grid Position

Grid positions SHOULD be named by row and column:

    R1C1
    R1C2
    R2C1
    R2C2

These are projection addresses, not semantic identities.

For example:

    occurrence O7
    semantic Holon H42
    currently occupies R2C3

Occurrence identity and semantic Holon identity remain stable even when row or column insertion changes the occurrence's current grid position.

## 1.6 Occurrence

An **occurrence** is a presentation of a semantic Holon at a particular place in the retained navigation topology.

Occurrences occupy cells; they do not define the geometry of those cells.

The same semantic Holon may appear in multiple occurrences with different navigation provenance.

---

# 2. Grid Geometry Rules

## 2.1 Column Width Invariant

Every cell in a column MUST receive the same external width.

Therefore an operation that changes the horizontal allocation of an occurrence changes the width of the occurrence's entire column.

It is invalid for:

    R1C2.width != R2C2.width

because both cells belong to C2.

## 2.2 Row Height Invariant

Every cell in a row MUST receive the same external height.

Therefore an operation that changes the vertical allocation of an occurrence changes the height of the occurrence's entire row.

It is invalid for:

    R2C1.height != R2C2.height

because both cells belong to R2.

## 2.3 Cell Budget

The Path Inspector assigns geometry to rows and columns rather than directly to individual occurrences.

The external budget received by an occurrence is derived from the cell it occupies:

    occurrence.width  = containing-column.width
    occurrence.height = containing-row.height

The selected child Visualizer then decides how to realize itself within that budget.

## 2.4 Compression

Horizontal compression is a **column transformation**.

Vertical compression is a **row transformation**.

Therefore:

> **Compressing one cell horizontally compresses its entire column. Compressing one cell vertically compresses its entire row.**

Two-axis compression occurs naturally when an occurrence occupies both a compressed column and a compressed row.

It does not require a separate Path Inspector occurrence state.

## 2.5 Focus and Grid Allocation

Focus may cause the Path Inspector to redistribute row heights and column widths.

For example:

- moving focus right may expand the newly focused column and compress columns to its left;
- moving focus down may expand the newly focused row and compress rows above it.

These are grid-allocation changes.

They do not alter occurrence identity, semantic provenance, or retained navigation topology.

---

# 3. Replaceable Selection Versus Retained Navigation

The Path Inspector distinguishes between:

1. changing a selection that has not yet become part of a traversed navigation path; and
2. selecting an alternative after the current occurrence has acquired retained continuation.

This distinction determines whether an existing cell may be reused or whether the grid must grow.

## 3.1 Replaceable Leaf Occurrence

An occurrence that has not been traversed onward is a **replaceable leaf occurrence** with respect to its source.

Selecting another alternative from the same source may replace that occurrence in its existing grid position.

For example, beginning at:

    R1C1
      H1

selecting one singular relationship from H1 may produce:

    R1C1   R1C2
      H1     H2

If H2 has not been traversed onward, selecting a different singular relationship from H1 may reuse R1C2:

    R1C1   R1C2
      H1     H4

Likewise, selecting different collections within H1 may change the Collection Visualizer shown by H1 without extending the Path Inspector topology.

Selecting different rows from a collection may reuse the corresponding vertical child position while that occurrence remains an unextended leaf.

## 3.2 Traversal Makes the Occurrence Retained

Once navigation continues from an occurrence, that occurrence becomes part of a retained navigation path.

For example:

    R1C1   R1C2   R1C3
      H1  -> H2  -> H3

H2 can no longer be treated merely as H1's currently selected singular target.

It is now the semantic anchor of the retained continuation to H3.

Replacing H2 with another selection from H1 would either:

- destroy the retained H2 -> H3 path; or
- falsely imply that H3 descends from the replacement occurrence.

Neither is valid.

The governing rule is:

> **A selected child may be replaced while it is an unextended leaf. Once navigation has continued through that occurrence, selecting an alternative from the same source creates an additional retained occurrence rather than replacing the traversed occurrence.**

---

# 4. Grid Insertion

## 4.1 Insertion Preserves Retained Paths

When a new occurrence cannot reuse an existing position without displacing a traversed occurrence, the Path Inspector MUST grow the grid.

It does so by inserting the row or column necessary to preserve both:

- the existing retained navigation path; and
- the newly selected continuation.

## 4.2 Horizontal Insertion

Suppose the retained path is:

    C1      C2      C3

    H1  ->  H2  ->  H3

The user returns to H1 and selects a different singular continuation.

Because H2 has already been traversed onward to H3, H2 MUST NOT be replaced.

The Path Inspector inserts a new column immediately after H1's column:

    C1      C2      C3      C4

    H1  ->  H4      H2  ->  H3

The former C2 and C3 have shifted to C3 and C4.

Their occurrences and navigation provenance have not changed.

The newly inserted column may contain empty cells elsewhere in the grid.

## 4.3 Vertical Insertion

The same rule applies to collection-mediated traversal.

If a selected collection member remains an unextended leaf, another member selection may replace it in the existing child position.

Once navigation has continued from that member occurrence, selecting another member from the same source MUST preserve the traversed occurrence and create an additional occurrence.

Where necessary, the Path Inspector inserts a row to provide that occurrence with a distinct grid position while preserving existing provenance.

## 4.4 Insertion Does Not Renumber Identity

Row and column identifiers describe current projection order.

Occurrence identifiers describe retained navigation identity.

Therefore insertion may change an occurrence from:

    R1C2

to:

    R1C3

without changing:

- the occurrence;
- its semantic Holon;
- its parent occurrence;
- the affordance through which it was reached;
- its descendants.

Coordinates are projection addresses, not semantic identifiers.

## 4.5 Sparse Cells

Insertion may create empty cells.

For example, if a new horizontal continuation originates from a lower row:

    before:

        C1      C2

    R1  H1  ->  H2
    R2  H3

a horizontal continuation from H3 may require:

    after:

        C1      C2      C3

    R1  H1      .   ->  H2
    R2  H3  ->  H4

The empty cell R1C2 is intentional.

It prevents geometric compaction from falsely implying that H4 and H2 belong to the same horizontal continuation stage.

> **Empty cells are valid structural elements when necessary to keep the grid truthful to retained navigation provenance.**

---

# 5. Consequences for the Existing Grammar

## 5.1 Replace Independent Occurrence Extents

The current concept that:

> each occurrence has independently selected width and height extents

should be removed.

It should be replaced by:

> **Each column has a current width and each row has a current height. An occurrence receives the width of its containing column and the height of its containing row.**

Expanded, partially compressed, and fully compressed remain useful allocation concepts, but they apply to **rows and columns at the Path Inspector level**, not independently to individual cells.

The child Visualizer remains responsible for deciding how to realize itself within the resulting cell budget.

## 5.2 Replace Cross-Axis Consistency With Grid Consistency

The current cross-axis consistency rule should become a stronger grid invariant.

Instead of:

> the vertical lineage shares the current width of its intersection occurrence; the horizontal lineage shares the current height of its intersection occurrence

the grammar should state:

> **All cells in a column share that column's width. All cells in a row share that row's height.**

This is simpler and applies everywhere, not only at lineage intersections.

## 5.3 Refine Branch Production

The current Branch rule should explicitly distinguish replacement from retained branching:

> **Changing the selected child of an anchor may reuse the existing child position while that child is an unextended leaf. Once that child has been traversed onward, it is retained navigation topology. Selecting another child from the same anchor creates an additional occurrence and causes the Path Inspector to insert whatever row or column is necessary to preserve both continuations.**

## 5.4 Refine Stable Attachment

Stable attachment should explicitly survive grid insertion:

> **A continuation remains attached to the occurrence that produced it regardless of focus changes, row or column compression, or insertion of rows and columns. Grid coordinates may change; navigation provenance does not.**

---

# 6. Revised Core Invariants

The Path Inspector MUST preserve these invariants:

1. The viewport is bounded while navigation topology and its grid projection may grow.
2. The Path Inspector projects retained navigation topology onto a two-dimensional grid.
3. Every column has exactly one current width shared by all cells in that column.
4. Every row has exactly one current height shared by all cells in that row.
5. Every cell receives its external spatial budget from the intersection of its row height and column width.
6. Horizontal compression or expansion transforms a whole column.
7. Vertical compression or expansion transforms a whole row.
8. Single-valued traversal extends horizontal navigation; collection-mediated traversal extends vertical navigation.
9. An unextended child occurrence may be replaced by another selection from the same source.
10. Once navigation continues through an occurrence, that occurrence and its continuation become retained topology.
11. A new alternative from an anchor whose existing child has been traversed creates an additional occurrence rather than replacing the retained occurrence.
12. The Path Inspector inserts rows or columns as necessary to preserve multiple retained continuations.
13. Row or column insertion may change grid coordinates but MUST NOT change occurrence identity or navigation provenance.
14. Empty cells are valid when required to preserve truthful topology.
15. Existing lineage remains stably attached as focus and grid geometry change.
16. Partial compression retains the relevant active scanning context.
17. Full compression preserves topology and recoverability.
18. Overflow remains distinct from compression and hidden lineage remains discoverable.
19. Parents own external child allocation; children compose responsively within the resulting cell budget.
20. Compression, overflow, maximization, insertion, traversal, and re-rooting have distinct semantics.

---

# 7. Resulting Mental Model

The refined grammar can be summarized as:

    retained navigation topology
        ->
    Path Inspector grid
        ->
    ordered rows + ordered columns
        ->
    one height per row + one width per column
        ->
    cell spatial budgets
        ->
    responsive child Visualizers

Navigation changes that remain local and untraversed may reuse a cell.

Navigation changes that would overwrite retained history instead grow the grid:

    replace while leaf
        ->
    traverse onward
        ->
    retain occurrence
        ->
    select alternative
        ->
    insert row or column
        ->
    preserve both paths

This makes the two-dimensional grid the stable geometric grammar while allowing the semantic Holons occupying that geometry to change over time.

The concise governing principles are:

> **The grid owns geometry; occurrences occupy cells.**

> **Rows own height; columns own width.**

> **Coordinates may move; provenance does not.**

> **Replace an untraversed leaf; insert to preserve a traversed path.**