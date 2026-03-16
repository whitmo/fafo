from typing import List, Dict, Any
from chromadb.api import Client, Collection

from src.chroma_client_utils import get_chroma_client
from src.embedding_utils import get_sentence_transformer_ef
from data.agent_skills import AGENT_SKILLS_DATA

COLLECTION_NAME = "agent_skills_knowledge_base"

def initialize_agent_skills_kb(client: Client, ef: Any) -> Collection:
    """
    Initializes a ChromaDB collection for agent skill descriptions.
    Adds skill descriptions if the collection is newly created or empty.
    """
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

    if collection.count() == 0:
        print(f"Adding {len(AGENT_SKILLS_DATA)} agent skills to '{COLLECTION_NAME}' collection...")
        documents = [skill["document"] for skill in AGENT_SKILLS_DATA]
        metadatas = [skill["metadata"] for skill in AGENT_SKILLS_DATA]
        ids = [skill["id"] for skill in AGENT_SKILLS_DATA]

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added {collection.count()} items to '{COLLECTION_NAME}'.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already contains {collection.count()} items.")

    return collection

def retrieve_agent_skill(collection: Collection, query: str, n_results: int = 1) -> List[Dict[str, Any]]:
    """
    Retrieves the most relevant agent skill(s) based on a query.
    """
    print(f"
Searching agent skills KB for: '{query}'")
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
    skills_kb_collection = initialize_agent_skills_kb(client, ef)

    # Example queries
    queries = [
        "I need to send a quick message to John.",
        "How do I look up information on the internet?",
        "Create a new document with some text."
    ]

    for query in queries:
        results = retrieve_agent_skill(skills_kb_collection, query)

        if results and results['documents']:
            print(f"
--- Relevant Skill for '{query}' ---")
            for i, doc in enumerate(results['documents'][0]):
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]
                print(f"Skill (Distance: {distance:.4f}):")
                print(f"  Name: {metadata['name']}")
                print(f"  Description: {metadata['description']}")
                print(f"  Usage: {metadata['usage']}")
                print(f"  Document: {doc}")
        else:
            print(f"No relevant skill found for '{query}'.")

    # Clean up
    client.delete_collection(name=COLLECTION_NAME)
    print(f"
Collection '{COLLECTION_NAME}' deleted.")
