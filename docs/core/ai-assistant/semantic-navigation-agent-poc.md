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

- inspect space (future)
- inspect dancer (future)
- inspect schema
- inspect module (future)
- inspect holon type
- inspect instance (future?)

The target determines what kind of information inspection reveals.

Inspection may expose:

- identifying information;
- discovery context;
- properties;
- relationships;
- other semantic affordances.

## `find_instances`

Find instances of a known type that satisfy a selective set of predicates.

This operation provides the bridge from type-level semantic discovery to instance-level grounding without requiring broad enumeration.

For example:

    find_instances(
      type = Person,
      predicates = [
        Person.name Equals "Tom Hanks"
      ]
    )

`find_instances` should not mean:

    get all instances of Person
        ->
    filter them afterward

Instead, the predicates are part of the operation itself and constrain the candidate population before results are returned.

The requested type must already be known in semantic context, and every predicate must be valid for that type.

A predicate list is optional at the operation level, but the agent should generally avoid unconstrained `find_instances` calls for types with large instance populations. The purpose of the operation is selective instance discovery, not population enumeration.

## `expand_relationship`

Traverse one known relationship from a known holon.

The relationship must already have been exposed by the semantic context for the source object or its type.

The LLM must not invent plausible-sounding relationships.

For example, given:

    Customer -> Order -> LineItem -> Product

the model must not replace this with an imagined:

    Customer -> purchases -> Product

simply because that would make sense linguistically.

An expansion may optionally include predicates constraining the target instances returned by the relationship.

For example:

    expand_relationship(
      source = Customer123,
      relationship = placed_orders,
      predicates = [
        Order.status Equals "Open"
      ]
    )

Predicates on an expansion apply to the **target instances of the relationship**, not to the source holon or the relationship itself.

This allows the graph substrate to constrain results before materializing a potentially large collection.

## `project`

Retrieve one or more known property values from a holon or collection.

Prefer projecting the useful set of properties together rather than forcing separate operations for every scalar property.

The property names must already be semantically afforded by the target type.

## `answer`

Return the answer when the accumulated graph evidence is sufficient.

The model should not answer from general world knowledge when the intent is to answer from the graph.

---

# Predicates

Selective instance discovery and traversal require a small, explicit predicate model.

A predicate consists of:

    Predicate
      type
      property
      operation
      match_value

For example:

    type: Person
    property: name
    operation: Equals
    match_value: "Tom Hanks"

The fields have the following semantics:

- `type` identifies the type whose instances are being constrained;
- `property` identifies a property defined for that type;
- `operation` identifies the comparison or string-match operation to perform;
- `match_value` supplies the value against which the property is compared.

Predicates are intentionally descriptor-rooted.

A predicate is valid only if:

- the type is valid in the current operation context;
- the property is defined for that type;
- the operation is valid for the property's value type;
- the match value is valid for the property's value type and operation.

Although an enclosing operation may make the predicate type derivable, retaining `type` explicitly makes the predicate self-describing and independently validatable.

For example, in:

    find_instances(
      type = Person,
      predicates = [...]
    )

the validator can confirm that every predicate also declares `Person`.

Similarly, for:

    expand_relationship(
      source = TomHanks,
      relationship = acted_in,
      predicates = [...]
    )

the relationship descriptor establishes `Movie` as the target type, and every predicate must declare `Movie`.

---

## Predicate Operations

The POC should begin with a deliberately small set of predicate operations.

For string-valued properties:

    Equals
    StartsWith
    EndsWith
    Contains

For ordered values such as numbers or dates:

    Equals
    LessThan
    LessThanOrEqual
    GreaterThan
    GreaterThanOrEqual

For boolean-valued properties:

    Equals

Additional operations can be introduced later if justified by concrete navigation needs.

The goal is not to expose OpenCypher's expression language to the LLM.

It is to provide a small, deterministic selection vocabulary whose legality can be derived from semantic descriptors.

For example, if the model proposes:

    type: Person
    property: birth_date
    operation: Contains
    match_value: "1956"

and `birth_date` is a Date-valued property, preflight validation should reject the predicate because `Contains` is not a valid operation for that property's value type.

---

## Predicate Lists

Operations may accept zero or more predicates.

A predicate list is interpreted as an implicit logical conjunction.

For example:

    [
      P1,
      P2,
      P3
    ]

means:

    P1 AND P2 AND P3

For the initial POC:

- predicates may be ANDed together;
- `OR` is not supported;
- `NOT` is not supported;
- arbitrary nested Boolean expressions are not supported.

This keeps predicate construction, validation, and execution simple while covering the primary requirement: progressively narrowing a candidate population.

For example:

    find_instances(
      type = Movie,
      predicates = [
        Movie.year GreaterThanOrEqual 1990,
        Movie.title Contains "Apollo"
      ]
    )

means:

    Movie.year >= 1990
    AND
    Movie.title contains "Apollo"

Predicates therefore provide selection semantics without introducing a general-purpose query language.

---

# Semantic Preflight Validation

Every proposed operation is validated before execution.

The checks should remain simple and descriptor-rooted.

Examples include:

- does the target exist in the known context?
- is the requested type known?
- is the requested relationship afforded by the target's type?
- is the requested property afforded by the relevant type?
- is the predicate operation valid for the property's value type?
- is the predicate match value valid for the property's value type?
- for `find_instances`, do all predicates apply to the requested type?
- for `expand_relationship`, do all predicates apply to the relationship's target type?
- is the requested operation structurally valid?

The validator should not attempt to reason about better alternatives.

This maintains a clean division:

- **LLM:** relevance, planning, interpretation, predicate construction, next-step selection
- **validator:** semantic admissibility
- **graph/database:** execution and factual results

This differs from inserting a general OWL-style semantic reasoner into the agent loop. OWL or similar technologies may still have uses elsewhere, but they are not required for this POC pattern.

The validator should remain intentionally literal.

For example:

> Property `name` is not defined for type `Order`.

or:

> Predicate operation `Contains` is not valid for property `created_at`, whose value type is DateTime.

or:

> Predicate type `Product` does not match relationship target type `Order`.

The validator does not then propose a different property, operation, type, or path.

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
- find another instance using predicates;
- follow a relationship;
- constrain a relationship expansion using predicates;
- retrieve properties;
- answer immediately.

The LLM should therefore retain freedom to navigate at whatever level the accumulated context supports.

---

# Instance-Level Discovery

Pure top-down schema discovery creates another problem.

If the database contains `Tom Hanks`, requiring the model to descend through:

    Space -> Dancer -> Schema -> Module -> Type -> Instances

and then enumerate the instances of `Person` before locating Tom Hanks would be both inefficient and unnecessarily schema-first.

The agent instead needs a selective transition from a known type to candidate instances.

Once an appropriate type has been identified and its relevant properties discovered, the agent can construct predicates over those properties.

For example:

    discover Person type
        ->
    inspect Person
        ->
    discover Person.name
        ->
    find_instances(
      type = Person,
      predicates = [
        Person.name Equals "Tom Hanks"
      ]
    )
        ->
    Tom Hanks
        ->
    inspect Tom Hanks
        ->
    navigate his afforded relationships

Instance grounding is therefore related to, but not simply another layer of, hierarchical discovery.

The important architectural distinction is:

- **discovery context** answers: what kinds of things are relevant?
- **find_instances** answers: which instances of this known type satisfy these known constraints?
- **inspect** answers: what do we know about this thing?
- **expand_relationship** answers: what is connected to it, optionally constrained?
- **project** answers: what values do we need?
- **answer** completes the task.

This produces an interleaved process of:

> orientation → selective grounding → traversal → further narrowing

rather than a strictly top-to-bottom ontology walk.

---

## Instance Anchors

`find_instances` is primarily useful for establishing an instance anchor without enumerating an entire population.

Once an anchor is known, ordinary graph traversal may provide a more natural and selective route to additional instances.

For example:

    find_instances(
      type = Person,
      predicates = [
        Person.name Equals "Tom Hanks"
      ]
    )
        ->
    Tom Hanks
        ->
    expand_relationship(
      source = TomHanks,
      relationship = acted_in
    )
        ->
    Movies

The agent does not need to repeatedly perform type-wide searches if a relationship from an existing anchor can more naturally constrain the candidate set.

This produces two principal routes to an instance:

    known type
        +
    selective predicates
        ->
    find_instances
        ->
    instance

and:

    known instance
        +
    known relationship
        ->
    expand_relationship
        ->
    related instances

The first establishes anchors.

The second exploits graph structure from those anchors.

---

# Selective Expansion

Predicates are useful not only for initial instance discovery but also for controlling traversal fan-out.

Consider:

    Customer --placed_orders--> Order

A customer may have hundreds or thousands of historical orders.

The agent may only need open orders:

    expand_relationship(
      source = Customer123,
      relationship = placed_orders,
      predicates = [
        Order.status Equals "Open"
      ]
    )

The alternative:

    expand all placed_orders
        ->
    retrieve hundreds of Orders
        ->
    filter afterward

needlessly materializes irrelevant graph state.

Predicate-constrained expansion establishes the principle:

> **When the agent already knows a useful constraint, apply it before materializing the target collection.**

This principle is particularly important for relationships with high target cardinality.

It also preserves a useful distinction between traversal and selection:

- the relationship determines **where the agent may navigate**;
- the predicates determine **which target instances should be returned**.

For example:

    Tom Hanks
        ->
    acted_in
        ->
    Movie

establishes the valid traversal.

Adding:

    Movie.release_year GreaterThanOrEqual 2000

does not alter the relationship semantics. It constrains the resulting target collection.

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

Predicate-constrained expansion gives the model an additional option.

A relationship that would otherwise be broad may become selective when target predicates can be applied:

    valid relationship
        +
    high target cardinality
        +
    useful target predicate
        ->
    selective expansion

This is preferable to:

    broad expansion
        ->
    large intermediate collection
        ->
    post hoc filtering

---

# Avoiding Population Enumeration

The POC should explicitly avoid using broad population enumeration as a normal instance-discovery mechanism.

In particular, the agent should not ordinarily need operations equivalent to:

    get all holons

or:

    get all instances of Person

merely to locate a specific instance.

Instead, the preferred pattern is:

    discover relevant type
        ->
    discover relevant properties
        ->
    construct selective predicates
        ->
    find_instances
        ->
    establish anchor
        ->
    navigate relationships

Similarly, once an instance anchor exists, the agent should prefer selective relationship traversal over returning every possible target and filtering afterward.

This does not mean broad enumeration can never exist elsewhere in MAP.

It means broad enumeration is not the normal semantic-navigation mechanism for locating concrete referents or answering selective questions.

---

# Three Dimensions of an Affordance

The emerging design suggests that relationship and property affordances should expose three distinct kinds of information.

## 1. Semantic Validity

What is actually allowed?

Examples:

- this relationship exists on this type;
- this property exists on this type;
- this predicate operation is valid for this property's value type.

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

Predicates complement navigation economics by allowing the model to turn some otherwise broad retrievals into selective ones.

---

# Predicate Discovery and Agent Knowledge

The agent should not invent predicates any more than it should invent relationships.

A predicate can only be constructed from semantic information that has already been exposed.

For example, before proposing:

    Person.name Equals "Tom Hanks"

the agent must know that:

- `Person` is a known type;
- `name` is a property of `Person`;
- `name` has a value type for which `Equals` is valid.

Similarly, before proposing:

    Movie.release_year GreaterThanOrEqual 1990

the agent must know that:

- `Movie` is the target type under consideration;
- `release_year` is a valid property of `Movie`;
- its value type supports ordering.

This preserves the same fundamental discipline applied to relationship navigation:

> **Discover the affordance before using the affordance.**

The model may infer that a user phrase such as "after 1990" is likely expressible as a comparison, but it may not assume that the relevant type actually contains a suitable property until that property has been discovered.

---

# Predicate Semantics Versus Query Generation

The introduction of predicates should not turn the agent protocol into a thin wrapper around OpenCypher.

The agent does not construct:

- `MATCH` clauses;
- arbitrary `WHERE` expressions;
- variable-length graph patterns;
- Boolean expression trees;
- joins;
- subqueries;
- query plans.

Instead, it operates through a small semantic navigation language.

For example:

    inspect
    find_instances
    expand_relationship
    project
    answer

with reusable predicates of the form:

    type
    property
    operation
    match_value

The graph substrate remains free to implement those operations using OpenCypher, native MAP mechanisms, indexes, caches, or other execution strategies.

The agent-facing semantics do not depend on that implementation choice.

This preserves the original architectural goal:

> The LLM should choose semantically meaningful next steps, not synthesize the graph query language used by the underlying storage engine.

---

# Future Search Semantics

The initial predicate model deliberately focuses on deterministic property matching.

For example:

    Equals
    StartsWith
    EndsWith
    Contains
    GreaterThan
    LessThan

This should not be conflated with broader information-retrieval capabilities such as:

- full-text keyword search;
- fuzzy matching;
- stemming;
- synonym expansion;
- semantic similarity;
- embedding-based search;
- relevance ranking.

Those capabilities may eventually prove useful for instance grounding, especially when user language does not exactly match stored property values.

However, they should be introduced explicitly rather than hidden behind an underspecified `find(query)` operation.

Possible future approaches include:

- additional well-defined predicate operations;
- type-specific resolution dances;
- a distinct search capability;
- ranked candidate resolution.

The POC should first establish whether descriptor-rooted predicates provide sufficient instance grounding for the target scenarios.

---

# System Prompt Principles

The standing agent instructions should establish the following rules.

1. Choose exactly one next operation at a time.
2. Use only semantic objects and affordances actually exposed in context.
3. Never invent types, relationships, properties, predicate operations, or facts.
4. Prefer progressive discovery when additional orientation is needed.
5. Use `find_instances` when an appropriate type is known and selective property constraints can identify candidate instances.
6. Construct predicates only from properties and operations semantically afforded by the relevant type.
7. Treat multiple predicates in a predicate list as logical `AND`.
8. Do not invent `OR`, `NOT`, or nested predicate expressions.
9. Use predicates on relationship expansion when they can materially narrow the target collection.
10. Treat validation failures as authoritative semantic information.
11. Do not expect the validator to recommend alternatives.
12. Prefer operations that reduce uncertainty or materially narrow the search.
13. Avoid high-cardinality unfiltered expansion when a more selective operation is available.
14. Avoid broad type-instance enumeration merely to locate a concrete referent.
15. Answer only when the accumulated graph evidence is sufficient.

The model's operational vocabulary remains fixed even though the domain ontology is open-ended and discovered dynamically.

---

# POC Operation Set

The compact POC vocabulary is:

| Operation | Purpose |
|---|---|
| `inspect` | Discover information and affordances about a known semantic object |
| `find_instances` | Find instances of a known type satisfying validated predicates |
| `expand_relationship` | Traverse one known semantic relationship, optionally constraining target instances with predicates |
| `project` | Retrieve selected known property values |
| `answer` | Return the final answer from accumulated evidence |

Predicates are not themselves an operation.

They are a reusable constraint structure accepted by operations that select collections of instances:

    find_instances(
      type,
      predicates[]
    )

    expand_relationship(
      source,
      relationship,
      predicates[]
    )

This keeps selection semantics orthogonal to navigation semantics.

`find_instances` selects from the population of a known type.

`expand_relationship` selects from the population reachable through a known relationship.

In both cases, predicates provide the same reusable mechanism for narrowing candidate instances.

These operations deliberately say nothing about domain-specific types.

They should work unchanged as MAP acquires arbitrary new schemas, modules, types, relationships, and instances.

---

# Example: Resolving and Navigating from an Instance

Suppose the user asks:

> What movies did Tom Hanks appear in after 2000?

The agent might proceed approximately as follows.

Initial discovery context exposes:

    Person
    Movie
    ...

The agent inspects `Person`.

The resulting descriptor exposes:

    properties:
      name: String

    relationships:
      acted_in -> Movie

The agent can now propose:

    find_instances(
      type = Person,
      predicates = [
        Person.name Equals "Tom Hanks"
      ]
    )

Assume this returns the Tom Hanks instance.

The agent inspects the relevant `Movie` type or otherwise has its descriptor available and discovers:

    release_year: Integer

It can then propose:

    expand_relationship(
      source = TomHanks,
      relationship = acted_in,
      predicates = [
        Movie.release_year GreaterThan 2000
      ]
    )

The graph substrate performs the constrained expansion.

The model may then project the useful properties:

    project(
      target = returned Movies,
      properties = [
        title,
        release_year
      ]
    )

and finally:

    answer

At no point does the model need to:

- retrieve every `Person`;
- retrieve every `Movie`;
- generate OpenCypher;
- invent a relationship;
- materialize all of Tom Hanks's movies before applying a known year constraint.

---

# Example: Multiple Predicates

Suppose the user asks:

> Which open orders over $500 has this customer placed?

Assume the customer instance is already known.

The `placed_orders` relationship targets `Order`, whose descriptor exposes:

    status: String
    total: Decimal

The model can propose:

    expand_relationship(
      source = Customer123,
      relationship = placed_orders,
      predicates = [
        Order.status Equals "Open",
        Order.total GreaterThan 500
      ]
    )

The predicate list means:

    Order.status = "Open"
    AND
    Order.total > 500

The model does not need a general Boolean query language to express this common narrowing operation.

---

# Architectural Character

The overall architecture is intentionally asymmetrical.

The LLM contributes what it is particularly good at:

- interpreting natural language;
- judging relevance;
- forming hypotheses;
- choosing promising next steps;
- constructing selective predicates from discovered semantic affordances;
- recovering from failed hypotheses.

MAP or the graph substrate contributes what deterministic systems are good at:

- declaring semantic affordances;
- validating operations and predicates;
- executing graph traversal;
- applying selection constraints;
- retrieving factual values;
- exposing cardinality and selectivity information.

The goal is therefore not to make the LLM know the ontology or generate a general-purpose graph query.

It is to give the LLM a small navigation language through which it can **learn just enough ontology, construct just enough selection criteria, and navigate just enough graph structure to answer the current question**.