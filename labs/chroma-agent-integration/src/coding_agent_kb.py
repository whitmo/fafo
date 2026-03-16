from typing import List, Dict, Any
from chromadb.api import Client, Collection

from src.chroma_client_utils import get_chroma_client
from src.embedding_utils import get_sentence_transformer_ef
from data.code_snippets import CODE_SNIPPETS_DATA

COLLECTION_NAME = "coding_agent_knowledge_base"

def initialize_coding_kb(client: Client, ef: Any) -> Collection:
    """
    Initializes a ChromaDB collection for the coding agent knowledge base.
    Adds code snippets if the collection is newly created or empty.
    """
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

    if collection.count() == 0:
        print(f"Adding {len(CODE_SNIPPETS_DATA)} code snippets to '{COLLECTION_NAME}' collection...")
        documents = [snippet["document"] for snippet in CODE_SNIPPETS_DATA]
        metadatas = [snippet["metadata"] for snippet in CODE_SNIPPETS_DATA]
        ids = [snippet["id"] for snippet in CODE_SNIPPETS_DATA]

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added {collection.count()} items to '{COLLECTION_NAME}'.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already contains {collection.count()} items.")

    return collection

def query_coding_kb(collection: Collection, query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """
    Queries the coding knowledge base for relevant code snippets.
    """
    print(f"
Searching coding KB for: '{query}'")
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=['documents', 'metadatas', 'distances']
    )
    return results

if __name__ == "__main__":
    # Example usage
    client = get_chroma_client()
    ef = get_sentence_transformer_ef()
    coding_kb_collection = initialize_coding_kb(client, ef)

    # Example query
    query = "function to calculate factorial recursively"
    results = query_coding_kb(coding_kb_collection, query)

    if results and results['documents']:
        print("
--- Retrieved Code Snippets ---")
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i]
            print(f"
Result {i+1} (Distance: {distance:.4f}):")
            print(f"Title: {metadata['title']}")
            print(f"Description: {metadata['description']}")
            print(f"Code:
{doc}")
    else:
        print("No relevant code snippets found.")

    # Clean up
    client.delete_collection(name=COLLECTION_NAME)
    print(f"
Collection '{COLLECTION_NAME}' deleted.")
