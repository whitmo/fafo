## ADDED Requirements

### Requirement: Chroma Large PDF RAG Demo
The demo SHALL demonstrate loading, chunking, embedding, and querying large PDF documents for Retrieval Augmented Generation (RAG) to overcome context window limitations.

#### Scenario: RAG with Large PDF
- **WHEN** one or more large PDF documents are loaded and processed (chunked and embedded) into ChromaDB
- **WHEN** a question is posed regarding the content of these PDFs
- **THEN** the system SHALL retrieve relevant text chunks from ChromaDB
- **THEN** these chunks SHALL be used to augment a simulated LLM prompt, demonstrating context window management.
