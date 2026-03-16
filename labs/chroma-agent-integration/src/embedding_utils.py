from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

def get_sentence_transformer_ef(model_name: str = "all-MiniLM-L6-v2"):
    """
    Returns an embedding function using a Sentence Transformer model.

    Args:
        model_name (str): The name of the Sentence Transformer model to use.
                          Defaults to "all-MiniLM-L6-v2".

    Returns:
        chromadb.api.types.EmbeddingFunction: An embedding function compatible with ChromaDB.
    """
    # Initialize the Sentence Transformer model
    _ = SentenceTransformer(model_name) # Load model to ensure it's downloaded if not present

    # Create and return the ChromaDB compatible embedding function
    return embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name)

if __name__ == "__main__":
    # Example usage
    print("--- Sentence Transformer Embedding Function Demo ---")
    ef = get_sentence_transformer_ef()
    texts = ["This is a test sentence.", "Another sentence for embedding."]
    embeddings = ef(texts)
    print(f"Embeddings generated for {len(texts)} texts. First embedding shape: {embeddings[0].shape}")

    # You can also test with a ChromaDB client (requires chromadb_client_utils)
    try:
        from chroma_client_utils import get_chroma_client
        client = get_chroma_client()
        collection = client.get_or_create_collection(name="test_collection_ef", embedding_function=ef)
        collection.add(documents=texts, metadatas=[{"source": "demo"} for _ in texts], ids=[f"doc{i}" for i in range(len(texts))])
        print("Documents added to ChromaDB with embedding function.")
        results = collection.query(query_texts=["test query"], n_results=1)
        print(f"Query results: {results}")
        client.delete_collection(name="test_collection_ef")
    except ImportError:
        print("Skipping ChromaDB client test, 'chroma_client_utils' not found.")
