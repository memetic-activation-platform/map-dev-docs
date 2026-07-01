# Bootstrap Function Specification

## Summary

The MAP bootstrap process should introduce no new protocol-level bootstrap commands if the existing command surface is already sufficient.

Instead, bootstrap should be implemented as a TypeScript SDK convenience function that performs a deterministic discovery walk against the participant's I-space using ordinary MAP commands and dances.

This preserves a minimal command surface while allowing richer experiences to emerge through descriptors, dancers, and visualizers.

## Design Principle

Bootstrap is an SDK concern, not a protocol concern.

The runtime provides:

- Primitive commands
- Holon navigation
- Relationship traversal
- Property access
- Dance execution

The SDK composes those primitives into a higher-level bootstrap experience.

## Assumptions

Upon successful connection:

- The participant is connected to an I-space.
- The SDK receives a reference to that I-space.
- The SDK may execute commands and dances against that I-space.

No dedicated bootstrap command is required.

## Proposed SDK Function

    async function bootstrapISpace(): Promise<BootstrapContext>

## Bootstrap Context

The bootstrap function returns a fully initialized context suitable for driving the initial human experience.

Example:

    interface BootstrapContext {
        currentSpace: HolonReference;
        spaceDescriptor: HolonReference;
        availableDancers: HolonReference[];
        defaultVisualizer?: HolonReference;
        spaceManager?: HolonReference;
        roleContext: RoleContext;
    }

## Bootstrap Sequence

### Step 1

Obtain the current I-space reference.

This is supplied by the connection layer.

Example:

    const currentSpace = connection.currentSpace();

### Step 2

Resolve the descriptor of the I-space.

This provides:

- type information
- properties
- relationships
- available dances
- available visualizers

Example:

    const descriptor =
        await sdk.getDescriptor(currentSpace);

### Step 3

Discover dancers.

Using ordinary relationship traversal.

Example:

    const dancers =
        await sdk.getRelated(
            currentSpace,
            "Dancers"
        );

No special command is required.

### Step 4

Locate the Space Manager dancer.

Example:

    const spaceManager =
        dancers.find(
            d => d.typeName === "SpaceManager"
        );

The bootstrap function may optionally treat the Space Manager as the preferred navigation entry point.

### Step 5

Locate the default visualizer.

Possible strategies:

- explicit relationship from I-space
- explicit relationship from descriptor
- visualizer tagged as default
- visualizer preferred by participant

Example:

    const visualizers =
        await sdk.getRelated(
            currentSpace,
            "Visualizers"
        );

### Step 6

Resolve participant role context.

Example:

    const roles =
        await sdk.getRelated(
            currentSpace,
            "Roles"
        );

This determines:

- permissions
- available actions
- visible affordances

### Step 7

Return BootstrapContext.

The experience layer now has everything required to render the initial dashboard.

## Why This Works

The existing command surface already supports graph navigation.

Examples:

- get related holons
- get property values
- execute dance

Bootstrap is therefore just a discovery recipe.

It does not require dedicated protocol support.

## Descriptor-Assisted Discovery

The bootstrap process should immediately begin leveraging descriptors.

Every discovered holon should expose its affordance surface through its descriptor.

For example:

    I-space
        -> Descriptor
            -> Dances
            -> Visualizers
            -> Relationships
            -> Properties

The SDK should use this information to drive experience generation.

## Descriptor-Assisted Dance Building

### Principle

Dance builders should leverage descriptors rather than requiring developers to manually reconstruct available capabilities.

The MAP already knows:

- property names
- relationship names
- dance descriptors
- validation rules
- state models

Builders should expose these automatically.

## Example: Projection Dance

Suppose the SDK encounters:

    ComputeNode.Type

Properties:

- node_name
- endpoint
- status
- capacity

The dance builder can automatically offer:

    project(
        "node_name",
        "endpoint",
        "status",
        "capacity"
    )

without manually specifying valid property names.

The property surface comes directly from the descriptor.

## Example: Get Related Dance

Suppose:

    Ingester.Type

Relationships:

- ComputeNodes
- ActiveJobs
- Owner

The builder can automatically expose:

    getRelated("ComputeNodes")
    getRelated("ActiveJobs")
    getRelated("Owner")

without requiring relationship names to be hardcoded.

The relationship surface comes directly from the descriptor.

## Example: Available Dances

Given:

    ComputeNode

State:

    Active

Descriptor-assisted discovery may expose:

- Pause
- Deactivate
- ViewMetrics

Given:

    ComputeNode

State:

    Paused

Descriptor-assisted discovery may instead expose:

- Resume
- Deactivate
- ViewMetrics

The affordance surface changes dynamically.

## Example: Ingester Dancer

The Ingester dancer owns relationships to ComputeNode holons.

The dance:

    getComputeNodes()

may internally construct a query equivalent to:

    expand(ComputeNodes)

using the descriptor-defined relationship.

The dance author does not manually write traversal logic.

The builder derives it from the descriptor.

Additional dances:

    ingestComputeNode()
    deactivateComputeNode()
    pauseComputeNode()
    getComputeNodeStatus()

can similarly leverage descriptor-assisted query construction.

## Affordance Surface

A key concept emerging from this design is the Affordance Surface.

For any holon in a given context, the affordance surface consists of:

- available properties
- available relationships
- available dances
- available visualizers
- available state transitions
- available actions

These are computed from:

- holon type
- descriptor
- state
- role context
- membrane permissions
- active space
- installed dancers

rather than hardcoded application logic.

## Human Experience Implication

The experience layer becomes progressively self-discovering.

As participants navigate:

- spaces
- dancers
- roles
- relationships
- holons

new affordances become visible.

The UI is assembled dynamically from descriptor knowledge rather than being entirely predefined.

This is a stronger form of HATEOAS:

The system does not merely reveal links.

It reveals capability.