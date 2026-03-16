from typing import List, Dict, Any
from chromadb.api import Client, Collection

from src.chroma_client_utils import get_chroma_client
from src.embedding_utils import get_sentence_transformer_ef
from src.pdf_utils import extract_text_from_pdf, chunk_text
import os

COLLECTION_NAME = "pdf_rag_collection"

def initialize_pdf_rag_collection(client: Client, ef: Any, pdf_path: str) -> Collection:
    """
    Initializes a ChromaDB collection for PDF RAG.
    Extracts text, chunks it, and adds to the collection.
    """
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

    if collection.count() == 0:
        print(f"Processing PDF '{pdf_path}' and adding chunks to '{COLLECTION_NAME}'...")
        pages_data = extract_text_from_pdf(pdf_path)
        chunks_data = chunk_text(pages_data)

        if not chunks_data:
            print("No text extracted or chunks generated from PDF. Collection will remain empty.")
            return collection

        documents = [chunk["document"] for chunk in chunks_data]
        metadatas = [chunk["metadata"] for chunk in chunks_data]
        ids = [chunk["id"] for chunk in chunks_data]

        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully added {collection.count()} chunks to '{COLLECTION_NAME}'.")
    else:
        print(f"Collection '{COLLECTION_NAME}' already contains {collection.count()} items.")

    return collection

def query_pdf_rag(collection: Collection, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """
    Queries the PDF RAG collection for relevant chunks.
    """
    print(f"
Querying PDF RAG for: '{query}'")
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

    # Ensure dummy PDF exists for testing
    data_dir = "labs/chroma-agent-integration/data"
    sample_pdf_path = os.path.join(data_dir, "sample_large_document.pdf")
    if not os.path.exists(sample_pdf_path):
        from data.generate_large_pdf import generate_large_pdf
        print(f"Generating dummy PDF for testing: {sample_pdf_path}")
        generate_large_pdf(sample_pdf_path, num_pages=2, text_per_page="This is sample text for the large PDF document. ")

    rag_collection = initialize_pdf_rag_collection(client, ef, sample_pdf_path)

    # Example query
    query = "What is the purpose of this document?"
    results = query_pdf_rag(rag_collection, query)

    if results and results['documents']:
        print("
--- Retrieved PDF Chunks for RAG ---")
        for i, doc in enumerate(results['documents'][0]):
            metadata = results['metadatas'][0][i]
            distance = results['distances'][0][i]
            print(f"
Chunk {i+1} (Distance: {distance:.4f}):")
            print(f"  Source: {metadata['source']}, Page: {metadata['page_number']}")
            print(f"  Content: {doc[:200]}...")
    else:
        print("No relevant chunks found.")

    # Clean up
    client.delete_collection(name=COLLECTION_NAME)
    print(f"
Collection '{COLLECTION_NAME}' deleted.")
