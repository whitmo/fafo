## 1. Project Setup

- [x] 1.1 Create `labs/chroma-agent-integration` project structure (e.g., `src`, `data`, `pdfs` for RAG).
- [x] 1.2 Initialize a Python virtual environment and install `chromadb`, `sentence-transformers`, `pypdf` (or similar PDF parser), and `langchain` (for chunking) dependencies.
- [x] 1.3 Create a `Makefile` in `labs/chroma-agent-integration` with `install-deps`, `run-demo`, and `clean` targets.
- [x] 1.4 Ensure Litestream is installed for the WAL recovery demo.

## 2. ChromaDB Core Initialization and Data Management

- [x] 2.1 Write Python script to initialize a ChromaDB client (in-memory for most, persistent SQLite for WAL demo).
- [x] 2.2 Implement functions to manage ChromaDB collections (create, get, delete).
- [x] 2.3 Implement function to configure and use a suitable embedding function (e.g., from `sentence-transformers`).

## 3. Coding Agent Knowledge Base Demo

- [x] 3.1 Define a small dataset of Python code snippets and their explanations/metadata.
- [x] 3.2 Implement function to add code snippets to a ChromaDB collection.
- [x] 3.3 Implement a simulated agent query flow: take a coding problem, embed it, search ChromaDB, and display relevant code.

## 4. Agent Skill Retrieval Demo

- [x] 4.1 Define a small dataset of agent skill descriptions (e.g., "send email", "search web", "write file").
- [x] 4.2 Implement function to add skill descriptions to a ChromaDB collection.
- [x] 4.3 Implement a simulated agent query flow: take a user request, embed it, search ChromaDB for the most relevant skill, and display the skill.

## 5. Large PDF RAG Demo

- [x] 5.1 Obtain or create a sample large PDF document(s).
- [x] 5.2 Implement a PDF loading and text extraction mechanism using `pypdf`.
- [x] 5.3 Implement text chunking logic (e.g., using `langchain`'s text splitters or custom logic) to create chunks suitable for ChromaDB.
- [x] 5.4 Implement function to embed and add PDF chunks to a ChromaDB collection with metadata (e.g., page number).
- [x] 5.5 Implement a query flow: take a question, retrieve relevant chunks from ChromaDB, and simulate an LLM response using these chunks.

## 6. ChromaDB SQLite WAL Mode and Recovery Demo

- [x] 6.1 Implement a Python script to initialize a ChromaDB client with a persistent SQLite backend (e.g., `chroma.PersistentClient`).
- [x] 6.2 Populate this ChromaDB instance with some test data.
- [x] 6.3 Configure `litestream.yml` to replicate the persistent ChromaDB SQLite file to a local WAL directory.
- [x] 6.4 Implement steps to start Litestream in the background, simulate data loss (delete DB file), and restore using `litestream restore`.
- [x] 6.5 Verify data integrity after restoration by querying the ChromaDB instance.

## 7. Demo Orchestration and Cleanup

- [x] 7.1 Create a main Python script or `showoff` presentation to orchestrate and present all demo segments.
- [x] 7.2 Add clear print statements and explanations within the demo to guide the user.
- [x] 7.3 Implement robust cleanup logic within the Python script/Makefile to remove all created ChromaDB data, WAL directories, and other demo artifacts.
