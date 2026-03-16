## Why

To create a comprehensive and interactive demonstration of ChromaDB's core features, making it easier for users to understand its capabilities, especially for fulltext and regex search, document storage, embeddings, vector search, metadata filtering, and multi-modal retrieval. This demo will serve as a learning tool and a quick reference for developers exploring vector databases.

## What Changes

This change will introduce a new "showoff" style demo within the `labs/chroma-tic` project. The demo will:
- Initialize and configure a ChromaDB instance.
- Demonstrate adding documents and metadata to a collection.
- Showcase the generation and storage of embeddings.
- Implement fulltext search functionality.
- Implement regex search functionality.
- Perform vector search queries.
- Apply metadata filtering during searches.
- Illustrate multi-modal retrieval (conceptually, as the actual multi-modal model integration might be beyond a simple showoff demo, or provide placeholders for it).

## Capabilities

### New Capabilities
- `chroma-fulltext-search-demo`: Demonstrates fulltext search.
- `chroma-regex-search-demo`: Demonstrates regex search.
- `chroma-document-storage-demo`: Demonstrates document storage and retrieval.
- `chroma-embeddings-demo`: Demonstrates embedding generation and storage.
- `chroma-vector-search-demo`: Demonstrates vector similarity search.
- `chroma-metadata-filtering-demo`: Demonstrates filtering results based on metadata.
- `chroma-multi-modal-retrieval-demo`: Demonstrates (conceptually or with placeholders) multi-modal retrieval.

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec file.
     Use existing spec names from openspec/specs/. Leave empty if no requirement changes. -->

## Impact

The new demo will be located in `labs/chroma-tic`. It will provide a clear, executable, and interactive example of ChromaDB's functionalities, primarily benefiting developers and users learning about ChromaDB.
