## ADDED Requirements

### Requirement: Chroma Coding Agent Knowledge Base Demo
The demo SHALL showcase ChromaDB serving as a searchable knowledge base for a coding agent.

#### Scenario: Retrieve Code Snippet for Problem
- **WHEN** a coding problem (natural language query) is provided to the simulated agent
- **THEN** the agent SHALL query ChromaDB semantically
- **THEN** relevant code snippets or documentation SHALL be retrieved from ChromaDB, ordered by relevance.
