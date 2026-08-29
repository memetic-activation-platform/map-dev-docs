# MAP as Associative Memory for LLMs

## Core Hypothesis

The problem may not be that MAP lacks the right retrieval mechanism. The problem may be that we have been asking the LLM to perform a task outside the interaction patterns it has learned particularly well.

Our previous approach effectively asked the model to understand an unfamiliar graph schema and synthesize queries over it. Even when query generation was constrained through structured intents rather than free-form Cypher, the model was still being asked to reason primarily as a graph-query planner.

A potentially better approach is to expose MAP as a **self-describing environment that an LLM can incrementally explore**.

This resembles the way coding agents work with an unfamiliar repository:

1. Orient to the environment.
2. Inspect something potentially relevant.
3. Discover its structure and affordances.
4. Follow a promising relationship.
5. Inspect what was found.
6. Repeat until enough evidence has accumulated to answer the original question.

The LLM does not need prior knowledge of MAP's schemas, holon types, relationships, properties, or dances. It learns the relevant portion of the semantic environment incrementally from MAP's own self-description.

The working hypothesis for the proof of concept is therefore:

> Can an LLM reliably investigate an unfamiliar, dynamically extensible MAP space when given a small set of generic navigation operations and authoritative self-describing projections?

If that works, MAP begins to function as associative memory through **agentic semantic navigation**, rather than primarily through RAG or generated graph queries.

---

# Separation of Responsibilities

The architecture has three distinct responsibilities.

## MAP

MAP remains the authoritative semantic environment.

It owns:

- holons
- holon descriptors
- properties
- relationships
- dances
- homogeneous HolonCollections
- smart references
- projection operations
- relationship navigation
- caching and materialization
- eventual adaptive retrieval through DAHN

MAP does not need to know what question the LLM is trying to answer beyond what is necessary to execute a requested operation.

MAP should not rely on the LLM's interpretation of its ontology. Descriptor projections supplied by MAP remain authoritative.

## The LLM

The LLM performs the semantic reasoning.

Its job is to repeatedly answer a question of approximately this form:

> Given the user's goal, the semantic context already discovered, and the evidence obtained so far, what is the most useful next operation?

The LLM decides:

- what appears relevant
- which domain to explore
- which holon to inspect
- which relationship to follow
- which properties matter
- whether additional evidence is needed
- when sufficient evidence exists to answer the user's question

The LLM does **not** generate Cypher or MAP query algebra.

It selects operations from a constrained set supplied by the agent.

## The Agent

The agent is deliberately schema-agnostic.

It does not contain hard-coded knowledge of:

- Person
- Movie
- Organization
- Agreement
- Directed
- ActedIn
- or any other domain-specific concept

Those can all appear dynamically as dancers are adopted into a MAP space.

The agent instead owns the investigation loop.

It:

- maintains the user's goal
- maintains the working context for the investigation
- obtains MAP projections
- sends relevant descriptors and evidence to the LLM
- requests the LLM's next operation
- validates the structured response
- executes that operation through MAP
- incorporates the result into working context
- detects obvious operational problems such as repeated identical requests
- logs the investigation
- repeats until the model chooses to answer

The agent coordinates the reasoning loop without itself performing the domain reasoning.

---

# Stateless Model Calls and Working Context

Model API calls should be treated as stateless from the architecture's perspective.

Therefore, when we say:

> The model already knows what a Person is.

what we actually mean is:

> The agent has already obtained the authoritative Person descriptor projection and includes the relevant representation of that descriptor in subsequent model contexts.

The descriptor does not need to be fetched from MAP repeatedly.

MAP's existing reference-based architecture and intrinsic caching already address that retrieval problem.

But the semantic information required by the LLM must remain represented in the model's current context.

This suggests that the agent maintains an explicit **investigation context**.

For example:

    Goal:
      What movies did Tom Hanks direct Kevin Bacon in?

    Known domains:
      People
      Movies
      Organizations
      Awards

    Known descriptors:
      Person
      Movie

    Current entities:
      Tom Hanks
      Kevin Bacon

    Evidence discovered:
      ...

    Available operations:
      ...

The descriptor projections themselves should remain authoritative MAP-generated artifacts.

The model may eventually help summarize accumulated investigative evidence, but it should not be asked to redefine or compress authoritative descriptor semantics in ways that could introduce hallucinated ontology.

---

# Descriptor Projections as Cognitive Units

MAP's native retrieval operations can remain fine-grained.

A holon may internally require separate operations to:

- retrieve a property
- navigate `describedBy`
- retrieve a relationship
- follow a related-holon reference
- materialize a target holon

The LLM does not necessarily need to see this fine-grained storage behavior.

The useful question is:

> What constitutes a useful cognitive unit for the LLM?

For an inspected holon, a good initial cognitive unit appears to consist of two things:

1. The instance itself.
2. A projection of its descriptor.

For example, an inspection of Tom Hanks might conceptually yield:

    Instance
      Type: Person
      First name: Tom
      Last name: Hanks
      Other immediately relevant scalar properties: ...

    Person descriptor
      Description:
        Represents a person participating in this domain.

      Properties:
        firstName
        lastName
        birthDate
        ...

      Relationships:
        actedIn
          Person -> Movie
          Movies in which this person acted.

        directed
          Person -> Movie
          Movies directed by this person.

        ...

      Dances:
        ...

This is not intended to recursively materialize the graph.

It exposes enough of the semantic neighborhood for the model to understand:

- what this thing is
- what information it possesses
- what relationships can be traversed
- what actions are available
- what promising next steps exist

That is the important purpose of `inspect`.

---

# Homogeneous Collections

MAP's existing rule that a HolonCollection is homogeneous is useful here.

A collection of 1,000 Person instances does not require 1,000 copies of the Person descriptor.

Conceptually the agent can provide:

    Collection:
      Type: Person

    Descriptor:
      <one Person descriptor projection>

    Elements:
      Tom Hanks
      Kevin Bacon
      Meg Ryan
      ...

This means context growth is more closely related to the number of **concepts encountered** than to the number of **instances encountered**.

That is an important scaling property.

---

# Initial Exploration Operations

The proof of concept should deliberately begin with a very small operation vocabulary.

The model should choose among these operations rather than generating arbitrary queries.

## 1. `discover_domains`

Purpose:

> Orient the model to the conceptual landscape available in the current MAP space.

This solves the bootstrap problem without assuming that global text search is inexpensive or natural for a Holochain DHT.

A domain result might contain:

    People
      People and their interpersonal and domain-specific relationships.

    Movies
      Films, productions, credits, and related entities.

    Awards
      Awards, nominations, recipients, and awarding organizations.

The model can reason over this small semantic table of contents and decide where to begin.

This operation could simply be implemented as a standard MAP query. There is no need initially to create a special caching architecture for it; MAP's existing reference and materialization caching can handle repeated access.

## 2. `inspect`

Purpose:

> Understand a particular holon sufficiently well to decide what to do next.

Input:

    holon reference

Result:

- useful instance properties
- identity and type information
- descriptor projection if not already represented in working context
- relationship definitions
- dance definitions
- potentially lightweight references to immediately relevant neighboring holons

`inspect` should be understood semantically rather than as a fixed physical retrieval operation.

Underneath, MAP may satisfy the inspection through several property and relationship operations.

## 3. `expand_relationship`

Purpose:

> Follow one explicitly available relationship from a holon or homogeneous collection.

Input conceptually includes:

    source
    relationship

For example:

    source: Tom Hanks
    relationship: directed

The result should normally be a homogeneous HolonCollection plus the descriptor of its element type if that descriptor has not yet been included in the investigation context.

## 4. `get_property_values`

Purpose:

> Retrieve one or more property values when the complete inspection projection does not already contain them.

This allows `inspect` to remain useful without necessarily materializing every scalar property.

Input conceptually includes:

    source
    properties

For example:

    source: Movie-123
    properties:
      title
      releaseYear

## 5. `answer`

This is not a MAP operation but should be part of the model's constrained decision vocabulary.

It means:

> The evidence accumulated so far is sufficient to answer the user's goal.

This lets the model explicitly terminate the exploration loop.

The operation can include the proposed answer and references to the evidence on which it relies.

---

# Possible Structured Model Response

The model's next-step response should be constrained to a machine-readable structure.

For example:

    {
      "operation": "expand_relationship",
      "target": "Tom Hanks",
      "relationship": "directed",
      "reason": "The goal asks which movies Tom Hanks directed, so following the directed relationship is the most direct way to obtain candidate movies."
    }

The exact JSON contract can evolve.

The important point is that the model supplies:

- the selected operation
- the target
- required parameters
- a short rationale

The application code owns execution.

The LLM never emits Cypher, traversal syntax, or implementation-specific MAP algebra.

This preserves the useful part of the structured-intent work already done in the Neo4j experiments.

---

# Why Ask for a Rationale?

The brief `reason` is useful during the proof of concept.

The model is the component making the semantic choice, so it is the only component capable of explaining why it selected one available path rather than another.

The rationale should be treated as diagnostic information, not as authoritative evidence.

For example:

    operation:
      expand_relationship

    target:
      Tom Hanks

    relationship:
      directed

    reason:
      The question asks specifically about movies Tom Hanks directed, so this relationship should produce the initial candidate set.

This gives us a trace of the model's navigation strategy.

If the POC fails, we can distinguish several failure classes:

- MAP did not expose necessary information.
- The projection was insufficient.
- The model misunderstood a descriptor.
- The model chose an irrelevant relationship.
- The model had the right information but reasoned incorrectly.
- The model became lost because context accumulated poorly.
- The operation vocabulary was insufficient.

Without the rationale and complete execution trace, those failure modes are much harder to distinguish.

---

# Example Investigation

Consider:

> What movies did Tom Hanks direct Kevin Bacon in?

The actual answer is irrelevant for the architectural example.

The important thing is how the system attempts to discover it without prior schema knowledge.

## Step 0 — User Goal

The agent records:

    Goal:
      What movies did Tom Hanks direct Kevin Bacon in?

At this point neither the agent nor the model is assumed to know the MAP ontology.

## Step 1 — Domain Orientation

The agent executes:

    discover_domains

MAP might return:

    People
      Represents people and relationships involving people.

    Movies
      Represents films, productions, credits, and related information.

    Awards
      Represents awards, nominations, and recipients.

The agent provides the goal and this domain projection to the model.

The model might respond:

    operation:
      inspect_domain

    target:
      People

    reason:
      Both Tom Hanks and Kevin Bacon appear to be people, so the People domain is the most likely entry point.

Whether `inspect_domain` becomes a distinct operation or is simply a variation of `inspect` is an implementation detail worth testing.

## Step 2 — Learn the Relevant Domain

MAP exposes enough of the People domain to reveal a Person holon type and a way to identify or enumerate Person instances.

The model now knows that `Person` exists because MAP told it so, not because Person was programmed into the agent.

The Person descriptor becomes part of the investigation context.

## Step 3 — Locate Tom Hanks

The model selects the appropriate operation available within the People domain to identify Tom Hanks.

Exactly how identification works should follow MAP's actual capabilities rather than forcing full-text search into the architecture.

The result is a Person reference corresponding to Tom Hanks.

## Step 4 — Inspect Tom Hanks

The agent executes:

    inspect(Tom Hanks)

The resulting cognitive projection might include:

    Instance:
      Tom Hanks

    Type:
      Person

    Properties:
      firstName: Tom
      lastName: Hanks

    Available relationships:
      actedIn
      directed
      produced
      ...

Because the Person descriptor is already known to the agent, it need not be retrieved again from MAP.

However, its relevant authoritative projection remains in the model context for the next reasoning call.

## Step 5 — Model Chooses `directed`

The model responds approximately:

    operation:
      expand_relationship

    target:
      Tom Hanks

    relationship:
      directed

    reason:
      We need movies directed by Tom Hanks, so this relationship should produce the candidate movie set.

## Step 6 — MAP Returns a Movie Collection

The expansion returns a homogeneous collection:

    Collection type:
      Movie

    Elements:
      Movie A
      Movie B
      Movie C

If Movie has not previously been encountered, the Movie descriptor projection is introduced once into the working context.

The model now knows the relationships available from Movie.

One of those relationships might represent actors appearing in the movie.

## Step 7 — Determine Kevin Bacon Participation

The model may now choose between several strategies based entirely on the semantic affordances MAP has exposed.

For example, it could expand the actors relationship on each candidate movie.

Or, if the Movie descriptor exposes a more useful operation, it could select that.

The agent does not need to understand which strategy is appropriate.

The model chooses.

MAP executes.

## Step 8 — Answer

Once sufficient evidence has accumulated, the model responds:

    operation:
      answer

    evidence:
      ...

    answer:
      ...

The exploration loop terminates.

---

# The Agent Loop

The initial implementation can be extremely small.

Conceptually:

    goal = user_prompt

    context = {
        goal,
        domains,
        descriptors_seen,
        entities_seen,
        evidence,
        available_operations
    }

    while not complete:
        decision = call_model(context)

        validate(decision)

        if decision.operation == "answer":
            return decision.answer

        result = execute_map_operation(decision)

        log(goal, context, decision, result)

        update_context(context, result)

The semantic intelligence is not inside this loop.

The intelligence comes from the model interpreting authoritative self-describing MAP projections.

---

# Proof-of-Concept Implementation Plan

## Phase 1 — Define the Exploration Contract

Implement only enough protocol to test the hypothesis.

Start with approximately:

- `discover_domains`
- `inspect`
- `expand_relationship`
- `get_property_values`
- `answer`

Potential additions should only be introduced when experiments demonstrate that the existing vocabulary cannot express a required navigation step.

Avoid designing a comprehensive MAP agent API before validating the basic loop.

## Phase 2 — Define Projection Holons

Use MAP's existing projection operation to create standard projections suitable for LLM consumption.

At minimum define projections for:

### Domain orientation

Expose:

- domain name
- domain description
- major holon types or entry points

### Descriptor orientation

Expose:

- type name
- type description
- property names and descriptions
- relationship names
- relationship descriptions
- source and target type information where available
- dances available for the type
- short descriptions of those dances

### Instance inspection

Expose:

- holon identity/reference
- type
- useful scalar properties
- perhaps selected smart-reference information
- enough information to connect the instance to its known descriptor

Do not attempt initially to optimize these projections aggressively.

The POC should favor adequate semantic context over minimal token use.

## Phase 3 — Build the Thin Agent

Implement an agent that knows nothing about the movie ontology.

Its code should contain no literals such as:

- Person
- Movie
- Actor
- Director
- actedIn
- directed

Its only domain knowledge should be the generic operation protocol.

This schema ignorance is an important test condition.

If the POC only works because domain semantics have leaked into the agent implementation, it has not validated the architecture.

## Phase 4 — Use Structured Model Decisions

Require each model reasoning step to return a constrained structure.

For example:

    operation
    target
    parameters
    reason

Validate the structure before executing anything.

Reject unsupported operations rather than attempting to interpret free-form instructions.

This should retain the major advantage discovered during the Cypher experiments: the model chooses intent, while deterministic code performs execution.

## Phase 5 — Maintain Explicit Investigation Context

Maintain at least:

    goal

    discovered domains

    descriptor projections currently required by the investigation

    relevant holon references

    results of prior operations

    concise accumulated evidence

    operations available to the model

The first POC can err on the side of preserving more context.

Context compression should be treated as a later optimization unless context size itself prevents the experiment from working.

## Phase 6 — Instrument Everything

Record every investigative step.

For each step capture:

- original user goal
- context supplied to the model
- descriptors supplied
- model-selected operation
- operation arguments
- model's short reason
- raw MAP result
- projection supplied back to the model
- eventual final answer
- whether the answer was correct

Also record metrics such as:

- number of model reasoning turns
- number of MAP operations
- number of holons materialized
- number of relationships expanded
- descriptors encountered
- token consumption
- repeated or redundant operations
- dead-end explorations

The logs should make the reasoning trajectory observable.

---

# Initial POC Test Suite

Do not begin with difficult MAP-specific use cases.

Use a small ontology whose correct answers are independently obvious.

A movie graph is useful precisely because its semantics are easy for humans to inspect.

Create questions that exercise progressively harder forms of navigation.

## Level 1 — Property Retrieval

Examples:

> What is Tom Hanks's birth year?

Tests:

- entity discovery
- Person descriptor interpretation
- property retrieval

## Level 2 — Single Relationship

Example:

> Which movies did Tom Hanks direct?

Tests:

- entity discovery
- relationship interpretation
- one expansion

## Level 3 — Relationship plus Filtering

Example:

> Which movies featuring Kevin Bacon were directed by Tom Hanks?

Tests:

- relationship traversal
- intersection/filter reasoning
- multiple instances

## Level 4 — Multi-Hop Navigation

Example:

> Which actors appeared in movies directed by Tom Hanks?

Tests:

- multiple descriptors
- chained relationship traversal
- homogeneous collections

## Level 5 — Unfamiliar Schema

After the movie ontology works, introduce a domain whose descriptor terminology the model has never seen before.

Ideally use intentionally unfamiliar type and relationship names whose descriptions provide their meanings.

This is the most important architectural test.

The question becomes:

> Can the model learn enough of a novel ontology from MAP's self-description to navigate it correctly?

A successful result here is much more significant than success on the familiar movie ontology.

---

# What Success Looks Like

The POC does not need to prove efficiency.

It needs to demonstrate a different capability.

The strongest result would be:

> A generic agent with no knowledge of the installed schema can receive an arbitrary goal, orient itself using MAP's self-description, select valid generic navigation operations, progressively discover relevant concepts, and arrive at a correct answer.

We should particularly look for evidence that:

1. The LLM successfully identifies useful domains from descriptions.
2. It correctly interprets previously unknown holon descriptors.
3. It chooses semantically sensible relationships.
4. It can recover after choosing an unproductive path.
5. It does not need generated Cypher or other graph-query syntax.
6. Adding a new dancer does not require modifying the agent.
7. The same exploration protocol works across substantially different domains.

If those conditions hold, we have evidence that MAP can serve as an associative memory environment for an LLM without forcing the LLM to become a MAP-specific query planner.

---

# What Not to Optimize Yet

Several promising ideas should deliberately remain outside the first POC.

## Adaptive inspection projections

DAHN could eventually learn which relationships and properties should automatically accompany an inspection.

For example:

> When agents inspect X, they almost always immediately request Y.

MAP could then materialize Y as part of future X inspections.

That may substantially reduce reasoning turns.

But it is not required to validate the basic navigation hypothesis.

## Cognitive profiles

DAHN may eventually maintain different usage patterns for different consumers.

A human-oriented visualizer might benefit from one projection shape, while an LLM agent benefits from another.

Potential profiles could include:

- human navigation
- general LLM investigation
- analytical agents
- planning agents
- specialized domain agents

This is promising, but should follow proof that the generic exploration loop works.

## Learned decision usefulness

DAHN can eventually distinguish between:

> This relationship is requested frequently.

and:

> Providing this relationship proactively materially improves the next reasoning decision or eliminates a reasoning round trip.

The latter is a stronger criterion.

Useful future metrics could include:

- probability that a relationship is requested after inspection
- probability that its presence changes the next selected operation
- number of model turns eliminated by embedding it
- reduction in failed exploratory branches
- improvement in final-answer accuracy
- token cost versus decision value

Again, these are optimizations after the basic loop has demonstrated value.

## Context compression

The eventual agent will likely need disciplined working-memory management.

But initially, keep authoritative descriptors and relevant evidence readily available.

First prove that the model can navigate correctly when adequately informed.

Then determine how little information it actually needs.

---

# Near-Term Development Sequence

A pragmatic implementation order would be:

1. Define the exact structured contract for the model's `next operation` response.
2. Implement `discover_domains`.
3. Define the standard descriptor projection.
4. Define the standard instance inspection projection.
5. Implement `inspect`.
6. Implement `expand_relationship`.
7. Implement `get_property_values`.
8. Build the minimal schema-agnostic agent loop.
9. Log complete reasoning and execution traces.
10. Create a very small movie ontology test dataset.
11. Run single-hop questions until navigation is reliable.
12. Run multi-hop questions.
13. Examine every failure trace and classify the failure.
14. Modify projections or operations only in response to observed failures.
15. Introduce a deliberately unfamiliar ontology.
16. Test whether the same unmodified agent can navigate it successfully.

That final step is the architectural proof.

---

# The Central Design Principle

The agent should not know the ontology.

The LLM should not know the query language.

MAP should not know the user's reasoning strategy.

Instead:

> MAP describes the world.

> The LLM reasons about the world.

> The agent manages the conversation between them.

The investigation proceeds through repeated small semantic steps:

    orient
      ->
    inspect
      ->
    notice
      ->
    expand
      ->
    inspect
      ->
    reason
      ->
    repeat
      ->
    answer

If this works, the key advance is not a better graph query generator.

It is that MAP has become an **LLM-navigable semantic environment**.

That is the proof of concept worth testing first.