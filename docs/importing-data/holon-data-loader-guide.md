MAP Holon Data Loader: JSON Import Format – Comprehensive Authoring Guide

This document provides a full guide to writing JSON files for importing data into the MAP Holon Data Loader. It assumes a clean slate—no prior conventions or frameworks—and reflects the most recent design decisions around schema declaration, relationship handling, type descriptors, key rules, and file structure.

⸻

✅ Core Principles
	1.	Everything is a Holon
Every entity in the MAP system is a Holon (including types, schemas, rules, and data instances). All imports describe Holons and their relationships.
	2.	Single Target Space
Each import file loads data into a single HolonSpace. The HolonSpace:
	•	Is either pre-existing (and thus not declared in the file), or
	•	Is created by including its definition in the file.
	3.	Types Are Self-Describing
Each Holon must specify its type, which implicitly replaces the need for a DescribedBy relationship. This improves clarity and reduces redundancy.
	4.	Component Wrapping for Schema Types
Types (especially type descriptors) should be wrapped within the relationships block of their parent Schema using the IsComponentOf relationship. This simplifies type management.
