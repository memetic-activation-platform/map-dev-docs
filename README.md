# MAP Developer Documentation

Welcome to the **MAP Developer Documentation** repository. This is the canonical source for technical documentation related to the **_Memetic Activation Platform_**, a holonic, agent-centric system designed for decentralized coordination and cultural evolution. 

The documentation is structured around **distinct technical audiences**, with additional shared conceptual material.

Use the following links to view the three GitHub Pages docs published from this repo.

- MAP Application Developers: 
https://memetic-activation-platform.github.io/map-dev-docs/mapp-dev/
- MAP Core Developers:
https://memetic-activation-platform.github.io/map-dev-docs/core/
- Dynamic Adaptive Holon Navigator (DAHN) Developers
https://memetic-activation-platform.github.io/map-dev-docs/dahn/




## 🧭 Audience-Centric Navigation Philosophy

This documentation follows a **role-based navigation model**, making it easier for developers to quickly find relevant guidance based on their involvement with the platform.

It is organized around three primary technical audiences:

---

### 🧱 **Mapp Developers**

Developers interested in understanding the **purpose and value** of adopting MAP, and the **steps and guidelines** for doing so.

There are two architectural options:

1. **Native MAP Applications:** Applications whose persistent data is stored and managed within MAP **Spaces**, using holonic structures natively.

2. **Integrating Applications:** Existing applications that retain their own persistence architecture but expose a **native API** wrapped in a **holonic adapter**. This adapter translates native data types and actions to/from MAP's holonic representation.

> Both approaches require mapping the application to the **MAP Ontology** for semantic alignment and interoperability.

---

### 🎨 **Visualizer Developers**

Developers interested in the **purpose of MAP**, its **open-ended architecture**, and the **value of contributing visualizers** to the **Visualizer Commons** and seeking specific guidelines on how to contribute.

Documentation in this section provides:

- Guidelines for building and registering visualizers
- Principles behind holonic data visualization
- API and composition standards for visualizer modules

---

### ⚙️ **MAP Core Implementers**


Developers responsible for the **design and implementation of MAP’s core functionality**, including:

- The **holon engine**
- **Space and persistence** infrastructure
- Core **type system** and runtime semantics

This audience maintains the foundational functionality that enable mapp and visualizer development.

---

## 📁 Directory Structure

### `docs/`

Contains all source Markdown files for the site.

#### 🔹 `mapp-dev/`
- **Audience:** Developers building or integrating **MAP Applications (mapps)**
- **Includes:**
    - Overview of mapp development paths
    - Native mapp integration
    - Adapter-based integration
    - Data loading guides

#### 🔹 `visualizers/`
- **Audience:** Developers contributing **visualizer components** to the MAP Visualizer Commons
- **Includes:**
    - Visualizer architectural principles
    - API usage
    - Contribution guidelines

#### 🔹 `core/`
- **Audience:** Developers working on **MAP's core runtime and architecture**
- **Includes:**
    - Holon engine internals
    - Storage and space management
    - Design specs and implementation guides

#### 🔹 `shared/`
- **Audience:** All developer audiences
- **Includes:**
    - Core concepts like holons and the MAP ontology
    - Shared glossary of terms

#### 🔹 `assets/`, `media/`, `overrides/`
- **assets/**: Scripts or JSON data used in the docs (e.g., glossary hover script)
- **media/**: Images and diagrams used throughout the documentation
- **overrides/**: CSS or theme overrides for the Material MkDocs theme

---

## 📚 Building the Docs

To preview the documentation locally:

    pip install mkdocs mkdocs-material
    mkdocs serve

To build the static site:

    mkdocs build

---

## 🛠️ Contributing

We welcome contributions! If you find an error, have suggestions, or want to extend the documentation:

1. Open an issue
2. Fork and submit a pull request
3. Join the discussion in the [MAP community](https://map.foundation/discord)

Please read `CONTRIBUTING.md` before submitting major structural changes.

## 🪪 License

This repository is licensed under the **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** license.

You are free to share and adapt the content as long as you:

- Attribute the MAP project
- Distribute your contributions under the same license

See [`LICENSE.md`](LICENSE.md) for full terms.

