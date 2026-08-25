This is the home page for initial MAP prototype's Use Case Model. The intent is to start with a small prototype that represents a _vertical slice_ of MAP functionality and can serve as a base for expansion.

This prototype is our starting point for proving the DAHN model: that views are constructed at runtime via the Selector Function, and composed from modular visualizers. We’re not just building a Human Interface — we’re demonstrating the viability of DAHN’s decentralized, adaptive interface architecture, starting with a real flow.

From the beginning, we want to:
* Instantiate all major visualizer types (Canvas, Node, Property, Action)
* Select visualizers dynamically at runtime based on holon metadata
* Drive selection via an initial DAHN Selector Function, even if it’s basic
* Demonstrate how visualizer selection and personalization can evolve without centralized UI design


### Basic Capabilities

* Standalone (i.e., Canvas-level) Actions
    * Create (an empty) Holon
    * View Existing Holons
    * Select/View Holon with Edit Option
* Holon-Level Actions:
    * View and Select Actions for a Holon (adjacent possible dances)
    * View Details (i.e., view the properties of a holon)
    * Edit holon's properties
    * View Relationships (see the relationship_names of all outbound relationships from this holon)

* Relationship-Level Actions:
    * Show related holons (extend the graph to include all holons related to the source holon via this relationship)
    * Filter related holons -- interactively define a filter for a relationship's collection and apply the filter to the graph
    * Add (target) holons to a relationship


## Use Case Model Diagram

The use cases in scope for the P0 prototype are shown in the following diagram.

![image](https://github.com/evomimic/map-holons/assets/17620758/b2185e25-8876-4071-bcf9-983fdd03e271)

The blue circles convey the implementation sequence.

* [View MAP Home Page](https://github.com/evomimic/map-holons/wiki/UC:-View-MAP-Home-Page)
* [Create Holon](https://github.com/evomimic/map-holons/wiki/UC:-Create-Holon)
* [Edit Holon Properties](https://github.com/evomimic/map-holons/wiki/UC:-Edit-Holon-Properties)
* [View Holons Graph](https://github.com/evomimic/map-holons/wiki/UC:-View-Holons-Graph)
* [View / Update Holon](https://github.com/evomimic/map-holons/wiki/UC:-View---Update-Holon)
* [Query Holon Relationships](https://github.com/evomimic/map-holons/wiki/UC:-Query-Holon-Relationships)





