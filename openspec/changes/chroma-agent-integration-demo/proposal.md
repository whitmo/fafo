## Why

To demonstrate the practical application of ChromaDB in enhancing AI agents, specifically for coding-related tasks and as a knowledge base for agent skills. This addresses the challenge of providing AI agents with persistent, searchable, and context-aware memory, enabling them to perform more complex and informed actions.

## What Changes

This change will introduce a new demo project, likely within the `labs/chroma-tic` directory, focusing on ChromaDB's integration with AI agents. The demo will:
- Set up ChromaDB to store code snippets, documentation, or function signatures relevant to coding tasks.
- Demonstrate how an AI agent can query ChromaDB for relevant code/information based on a given coding task or problem.
- Showcase ChromaDB storing "agent skills" (e.g., descriptions of tools, functions, or workflows an agent can use) and how an agent can retrieve the most relevant skill for a given prompt or user request.
- Provide examples of how embeddings of code/text are used for semantic search and retrieval within the agent's knowledge base.
- Demonstrate loading, chunking, embedding, and querying large PDF documents for Retrieval Augmented Generation (RAG) to overcome context window limitations.
- Demonstrate best practices for Data Integrity & Recovery with ChromaDB using SQLite in WAL mode, integrated with Litestream for local replication.

## Capabilities

### New Capabilities
- `chroma-coding-agent-kb-demo`: Demonstrates ChromaDB serving as a knowledge base for a coding agent to retrieve relevant code snippets or documentation.
- `chroma-agent-skill-retrieval-demo`: Demonstrates ChromaDB's use in enabling an agent to semantically search and retrieve descriptions of available skills or tools.
- `chroma-large-pdf-rag-demo`: Demonstrates using ChromaDB for RAG with large PDF documents to avoid context window issues.
- `chroma-sqlite-wal-recovery-demo`: Demonstrates ChromaDB with SQLite in WAL mode and local Litestream replication for data integrity and recovery.

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec file.
     Use existing spec names from openspec/specs/. Leave empty if no requirement changes. -->

## Impact

The new demo will provide a practical example of integrating vector databases with AI agents, offering insights into building more capable, context-aware, and performant agents. It will involve Python code interacting with ChromaDB and a simulated or simplified AI agent interaction flow.
