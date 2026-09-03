# Semantic Navigation Agent POC

## Purpose

Explore a tractable agent architecture in which an LLM answers questions over an unfamiliar ontology by incrementally discovering and navigating semantic structure rather than generating a complete graph query up front.

The core pattern is:

> **LLM chooses what to try; deterministic semantic checks determine whether the proposed step is valid.**

The validator is intentionally not a second reasoner. It answers only whether a proposed operation is valid and, if not, why.

---

## Core Agent Loop

The LLM is repeatedly asked:

> Given the user's goal, the semantic context discovered so far, previous results, and any validation errors, what is the single best next operation?

The loop is:

1. Provide the user goal and current semantic context.
2. LLM proposes exactly one operation.
3. Preflight validation checks the proposal.
4. If invalid:
    - do not execute it;
    - return a precise validation error;
    - add that error to context;
    - ask the LLM for the next best operation.
5. If valid:
    - execute it;
    - add the result to context;
    - ask again for the next best operation.
6. Continue until the LLM selects `answer`.

Validation should explain only **why the proposed operation is invalid**, not suggest what to do instead.

Example:

> Relationship `purchases` is not defined for `Customer`.

The LLM is then responsible for reconsidering the graph and choosing another path.

---

# Operation Vocabulary

Keep the operational vocabulary small and fixed while allowing the ontology itself to remain open-ended.

The initial POC operations are:

## `inspect`

Inspect a known semantic object.

This is intentionally generic rather than defining separate operations such as:

- inspect space
- inspect dancer
- inspect schema
- inspect module
- inspect type
- inspect instance

The target determines what kind of information inspection reveals.

Inspection may expose:

- identifying information;
- discovery context;
- properties;
- relationships;
- other semantic affordances.

## `expand_relationship`

Traverse one known relationship from a known holon.

The relationship must already have been exposed by the semantic context for the source object or its type.

The LLM must not invent plausible-sounding relationships.

For example, given:

    Customer -> Order -> LineItem -> Product

the model must not replace this with an imagined:

    Customer -> purchases -> Product

simply because that would make sense linguistically.

## `project`

Retrieve one or more known property values from a holon or collection.

Prefer projecting the useful set of properties together rather than forcing separate operations for every scalar property.

The property names must already be semantically afforded by the target type.

## `answer`

Return the answer when the accumulated graph evidence is sufficient.

The model should not answer from general world knowledge when the intent is to answer from the graph.

---

# Semantic Preflight Validation

Every proposed operation is validated before execution.

The checks should remain simple and descriptor-rooted.

Examples include:

- does the target exist in the known context?
- is the requested relationship afforded by the target's type?
- is the requested property afforded by the target's type?
- is the requested operation structurally valid?

The validator should not attempt to reason about better alternatives.

This maintains a clean division:

- **LLM:** relevance, planning, interpretation, next-step selection
- **validator:** semantic admissibility
- **graph/database:** execution and factual results

This differs from inserting a general OWL-style semantic reasoner into the agent loop. OWL or similar technologies may still have uses elsewhere, but they are not required for this POC pattern.

---

# Progressive Semantic Discovery

The agent should not receive the entire ontology up front.

Instead, it progressively earns semantic context.

A possible mature MAP hierarchy is:

    Space
      -> Dancers
        -> Schemas
          -> Modules
            -> Types
              -> Instances

However, this hierarchy should **not be hard-coded into the agent protocol**.

Instead, introduce the generic concept of a:

## Discovery Context

An `inspect` result may identify a set of semantic objects representing the preferred next scope for orientation.

Examples:

- inspecting a Space might expose Dancers;
- inspecting a Dancer might expose Schemas;
- inspecting a Schema might expose Modules;
- inspecting a Module might expose Types.

The system prompt tells the model that discovery context is the preferred mechanism for progressively narrowing semantic scope.

It remains guidance rather than a hard constraint. Ordinary graph relationships may still provide a better direct route in some situations.

This distinction is useful:

- **discovery context** helps the agent orient and narrow scope;
- **ordinary affordances** expose the semantic relationships and properties of the current object.

The LLM does not have to infer which of dozens of relationships is the intended information architecture.

---

# Neo4j POC Simplification

The current POC runs on Neo4j and does not yet represent Dancers, Schemas, and Modules explicitly.

There is no need to fabricate those structures merely to resemble the eventual MAP architecture.

For the POC, treat the entire ontology as one implicit module.

The initial discovery context can therefore simply be:

> the set of available types, with concise names and descriptions.

This lets the experiment begin at approximately:

    Module -> Types

while preserving the same generic discovery protocol that MAP can later use at additional levels.

An important empirical question for the POC is:

> How large can the initial type discovery context become before another level of semantic segmentation becomes useful?

If dozens or even hundreds of concise types work reliably, additional structure may not yet be necessary.

If the model begins to:

- choose irrelevant helper types;
- confuse neighboring concepts;
- wander through the ontology;
- consume excessive context;
- become inconsistent about where to begin;

then that provides evidence for introducing higher-level modules or other discovery scopes.

---

# Modules as Semantic Scope

MAP's evolving module concept appears well suited to progressive discovery.

A module is not an AI-specific artifact. It is already useful as a software and ontology design boundary:

- a coherent collection of closely related types;
- high internal cohesion;
- relatively loose coupling to other modules;
- types belong to one module;
- modules can evolve and be versioned as units.

That makes modules a natural semantic chunk for an LLM.

Rather than exposing hundreds of fine-grained types immediately, a future implementation can expose:

- module name;
- concise module description;

and let the model inspect the relevant module before seeing its types.

---

# Bootstrap and Conversation Context

At the very beginning of a session, an initial inspection may be performed automatically to establish discovery context.

For example, in mature MAP:

    inspect Space -> available Dancers

For the current Neo4j POC:

    initial discovery -> available Types

After bootstrap, the same generic loop is used for every user turn.

A later conversational prompt may:

- continue from a previously discovered instance;
- inspect another type;
- broaden back toward a larger semantic scope;
- follow a relationship;
- retrieve properties;
- answer immediately.

The LLM should therefore retain freedom to navigate at whatever level the accumulated context supports.

---

# Instance-Level Discovery

Pure top-down schema discovery creates another problem.

If the database contains `Tom Hanks`, requiring the model to descend through:

    Space -> Dancer -> Schema -> Module -> Type -> Properties -> Instances

before learning that Tom Hanks exists is unnecessarily schema-first.

It also increases the chance that the agent follows the wrong branch before grounding the user's concrete referent.

Instance grounding should therefore be **orthogonal to schema discovery**.

Once an appropriate semantic scope or type has been identified, the agent should be able to resolve a user referent directly within that scope.

For example:

    discover Person type
        ->
    find Person matching "Tom Hanks"
        ->
    inspect Tom Hanks
        ->
    navigate his afforded relationships

This suggests adding another primitive:

## `find`

Resolve a user-supplied concept, name, or identifying description to candidate holons within a known semantic scope.

For example:

    find(
      type = Person,
      query = "Tom Hanks"
    )

`find` should be selective. It should not mean enumerating every instance of a type.

Its implementation might use:

- identifying properties;
- display labels;
- indexed properties;
- lexical search;
- other type-specific lookup mechanisms.

The important architectural distinction is:

- **discovery** answers: what kinds of things are relevant?
- **find** answers: which concrete thing does the user mean?
- **inspect** answers: what do we know about this thing?
- **expand** answers: what is connected to it?
- **project** answers: what values do we need?
- **answer** completes the task.

This produces an interleaved process of:

> orientation → grounding → narrowing → traversal

rather than a strictly top-to-bottom ontology walk.

---

# Relationship Cardinality and Selectivity

Semantic validity alone is insufficient for intelligent traversal.

Two relationships may both be valid while having radically different operational consequences.

For example:

    Space --Owns--> Holon

may return essentially every holon in the space.

Expanding it may therefore be semantically valid but strategically terrible.

The LLM should receive enough metadata to estimate the likely cost and usefulness of relationship expansion.

## Schema Cardinality

Traditional semantic cardinality remains useful:

- `0..1`
- `1`
- `0..*`
- `1..*`

But this says relatively little about actual traversal cost.

A relationship with cardinality `0..*` could currently return:

- 2 targets;
- 20 targets;
- 20,000 targets.

## Runtime Selectivity

For agent planning, estimated result size or selectivity is more useful.

A relationship affordance might conceptually include:

    name: owns
    target_type: Holon
    semantic_cardinality: 0..*
    estimated_target_count: 48000
    selectivity: very_low
    description: Holons owned by this space

versus:

    name: placed_orders
    target_type: Order
    semantic_cardinality: 0..*
    estimated_target_count: 14
    selectivity: moderate
    description: Orders placed by this customer

This lets the LLM distinguish:

> **valid to expand**

from:

> **wise to expand now**

The system prompt should encourage the model to prefer relationships likely to narrow the search and avoid very broad expansions unless the user's goal genuinely requires them.

---

# Three Dimensions of an Affordance

The emerging design suggests that relationship and property affordances should expose three distinct kinds of information.

## 1. Semantic Validity

What is actually allowed?

Examples:

- this relationship exists on this type;
- this property exists on this type.

## 2. Semantic Meaning

What does the affordance represent?

Examples:

- relationship description;
- target type;
- property description.

## 3. Navigation Economics

How useful or expensive is following it likely to be?

Examples:

- cardinality;
- estimated target count;
- selectivity;
- perhaps later, retrieval cost or locality.

This third dimension is especially important for keeping an agent from making semantically legal but explosively broad traversals.

---

# System Prompt Principles

The standing agent instructions should establish the following rules.

1. Choose exactly one next operation at a time.
2. Use only semantic objects and affordances actually exposed in context.
3. Never invent types, relationships, properties, or facts.
4. Prefer progressive discovery when additional orientation is needed.
5. Use concrete instance lookup once an appropriate semantic scope is known.
6. Treat validation failures as authoritative semantic information.
7. Do not expect the validator to recommend alternatives.
8. Prefer operations that reduce uncertainty or materially narrow the search.
9. Avoid high-cardinality expansion when a more selective path is available.
10. Answer only when the accumulated graph evidence is sufficient.

The model's operational vocabulary remains fixed even though the domain ontology is open-ended and discovered dynamically.

---

# Emerging POC Operation Set

The discussion began with four core operations:

    inspect
    expand_relationship
    project
    answer

The instance-grounding discussion suggests a likely fifth:

    find

The resulting compact vocabulary is therefore:

| Operation | Purpose |
|---|---|
| `inspect` | Discover information and affordances about a known semantic object |
| `find` | Resolve a concrete user referent within a known semantic scope |
| `expand_relationship` | Traverse one known semantic relationship |
| `project` | Retrieve selected known property values |
| `answer` | Return the final answer from accumulated evidence |

These operations deliberately say nothing about domain-specific types.

They should work unchanged as MAP acquires arbitrary new schemas, modules, types, relationships, and instances.

---

# Architectural Character

The overall architecture is intentionally asymmetrical.

The LLM contributes what it is particularly good at:

- interpreting natural language;
- judging relevance;
- forming hypotheses;
- choosing promising next steps;
- recovering from failed hypotheses.

MAP or the graph substrate contributes what deterministic systems are good at:

- declaring semantic affordances;
- validating operations;
- executing graph traversal;
- retrieving factual values;
- exposing cardinality/selectivity information.

The goal is therefore not to make the LLM know the ontology.

It is to give the LLM a small navigation language through which it can **learn just enough ontology, just in time, to answer the current question**.