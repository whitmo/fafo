## Context

AI agents often require external knowledge or tools to perform complex tasks. ChromaDB, as a vector database, can serve as a powerful external memory for agents, allowing them to store and retrieve contextual information, code snippets, documentation, or tool descriptions efficiently through semantic search. This demo will illustrate two key use cases: a coding agent utilizing ChromaDB for a knowledge base, and an agent using ChromaDB for skill retrieval.

## Goals / Non-Goals

**Goals:**
- Develop a demo that clearly shows ChromaDB acting as a searchable knowledge base for a simulated coding agent.
- Create a separate demo segment illustrating ChromaDB's role in dynamically retrieving appropriate "skills" or "tools" for an agent based on user queries or internal prompts.
- Demonstrate loading, chunking, embedding, and querying large PDF documents for Retrieval Augmented Generation (RAG) to overcome context window limitations.
- Demonstrate best practices for ChromaDB data integrity and recovery using SQLite in WAL mode with Litestream local replication.
- Ensure the demo is self-contained and easy to run, ideally using Python.
- Provide a simple yet effective dataset for both coding knowledge and agent skills.

**Non-Goals:**
- Building a fully functional, production-ready AI agent.
- Implementing complex natural language understanding (NLU) or generation (NLG) within the agent beyond what's necessary for the demo.
- Integrating with external large language models (LLMs) or sophisticated AI orchestration frameworks (unless simplified and mocked).
- Deep dives into ChromaDB's internal architecture or advanced optimizations.

## Decisions

- **Programming Language:** Python will be used for all demo components due to its strong ecosystem for AI/ML and ChromaDB's native Python client.
- **ChromaDB Setup:** For most demos, an in-memory ChromaDB client will be used for simplicity. However, for the WAL mode and recovery demo, a persistent SQLite backend will be configured.
- **Coding Agent Knowledge Base Demo:**
    - **Data:** A small collection of simple Python code snippets with comments or explanations (e.g., common utility functions, algorithm implementations) will serve as the "knowledge base."
    - **Interaction:** A simulated agent loop will take a "coding problem" (text query), embed it, search ChromaDB for relevant code snippets, and present the results as potential solutions or references.
- **Agent Skill Retrieval Demo:**
    - **Data:** A collection of "skill descriptions" (short text descriptions of hypothetical agent tools, e.g., "send email," "search web," "create file," "analyze sentiment") will be stored in ChromaDB.
    - **Interaction:** A simulated agent will receive a "user request" (text query), embed it, search ChromaDB for the most semantically similar skill description, and indicate which skill the agent would likely invoke.
- **Large PDF RAG Demo:**
    - **Data:** One or more sample large PDF documents.
    - **Processing:** Use a library like `PyPDF2` or `pypdf` for PDF text extraction and `langchain` or custom logic for chunking.
    - **Interaction:** Demonstrate embedding chunks and querying, then showing how retrieved chunks can form part of a prompt to an LLM (simulated).
- **ChromaDB SQLite WAL Mode and Recovery Demo:**
    - **ChromaDB Setup**: Will use a persistent SQLite backend (not in-memory) to demonstrate WAL mode and Litestream.
    - **Data**: Simple ChromaDB collection with some dummy data for persistence demonstration.
    - **Integration**: Will showcase Litestream starting to monitor the ChromaDB SQLite file, performing ChromaDB operations, simulated data loss (deletion of DB file), and then recovering the ChromaDB instance via Litestream restore.
    - **Explanation**: Emphasize WAL mode advantages and Litestream's role in continuous backup and recovery.
- **Embedding Model:** A lightweight, readily available sentence transformer model will be used for generating embeddings for both code/text and skill descriptions.

## Risks / Trade-offs

- **Simulation vs. Realism:** The demo will involve simulated agent behavior, which may not fully convey the complexity of real-world agent interactions. → Mitigation: Clear commentary and explanation within the demo will highlight conceptual applications.
- **Limited Data Scope:** The small datasets for code and skills will naturally limit the breadth of search results. → Mitigation: Emphasize the pattern, which scales with larger datasets.
- **No LLM Integration:** The demo might not explicitly integrate with an LLM for actual agent reasoning. → Trade-off: Keep the focus on ChromaDB's role as memory/tool-lookup; LLM integration can be explained conceptually in the demo.
- **Litestream Dependency:** Users will need Litestream installed for the `chroma-sqlite-wal-recovery-demo`. → Mitigation: Provide clear installation instructions.

## Open Questions

- What specific code snippets would best illustrate the coding agent KB retrieval?
- What are good examples of agent skills to include for the skill retrieval demo?
- Which sample large PDF document(s) would be suitable and publicly accessible for the RAG demo?
- What specific content should be created in the ChromaDB SQLite WAL Recovery demo to best illustrate the recovery process?
