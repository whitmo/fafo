import chromadb
import os

def get_chroma_client(persistent: bool = False, path: str = "./.chroma_db"):
    """
    Initializes and returns a ChromaDB client.

    Args:
        persistent (bool): If True, returns a persistent client storing data at 'path'.
                           If False, returns an in-memory client.
        path (str): The directory path for persistent storage.

    Returns:
        chromadb.Client: An initialized ChromaDB client.
    """
    if persistent:
        # Ensure the directory exists
        os.makedirs(path, exist_ok=True)
        return chromadb.PersistentClient(path=path)
    else:
        return chromadb.Client()

def delete_chroma_data(path: str = "./.chroma_db"):
    """
    Deletes the persistent ChromaDB data directory.
    """
    if os.path.exists(path) and os.path.isdir(path):
        import shutil
        shutil.rmtree(path)
        print(f"Deleted persistent ChromaDB data at: {path}")

if __name__ == "__main__":
    # Example usage: In-memory client
    print("--- In-memory ChromaDB Client Demo ---")
    client_in_memory = get_chroma_client(persistent=False)
    collection_in_memory = client_in_memory.get_or_create_collection(name="my_in_memory_collection")
    collection_in_memory.add(documents=["hello world"], metadatas=[{"source": "test"}], ids=["doc1"])
    results_in_memory = collection_in_memory.query(query_texts=["hello"], n_results=1)
    print(f"In-memory query results: {results_in_memory}")
    client_in_memory.delete_collection(name="my_in_memory_collection") # Clean up in-memory

    # Example usage: Persistent client
    print("
--- Persistent ChromaDB Client Demo ---")
    persistent_path = "./.chroma_db_test"
    client_persistent = get_chroma_client(persistent=True, path=persistent_path)
    collection_persistent = client_persistent.get_or_create_collection(name="my_persistent_collection")
    collection_persistent.add(documents=["persistent data"], metadatas=[{"source": "db"}], ids=["p_doc1"])
    results_persistent = collection_persistent.query(query_texts=["persistent"], n_results=1)
    print(f"Persistent query results: {results_persistent}")
    print(f"Data stored at: {persistent_path}")

    # Clean up persistent data
    delete_chroma_data(persistent_path)
    print(f"Cleaned up persistent data at: {persistent_path}")
