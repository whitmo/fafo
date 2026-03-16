import chromadb
import os
import time
import subprocess
from typing import List, Dict, Any

from src.chroma_client_utils import get_chroma_client, delete_chroma_data
from src.embedding_utils import get_sentence_transformer_ef

COLLECTION_NAME = "wal_recovery_collection"
PERSISTENT_DB_PATH = "./.chroma_wal_db"
LITESTREAM_CONFIG_PATH = "./litestream.yml"
LITESTREAM_WAL_DIR = "./wal"
LITESTREAM_PID_FILE = "./litestream.pid"

def setup_chroma_wal_db(client: chromadb.PersistentClient, ef: Any) -> chromadb.Collection:
    """
    Sets up a ChromaDB collection using a persistent client and populates it with data.
    """
    print(f"
--- Setting up ChromaDB at {PERSISTENT_DB_PATH} ---")
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=ef
    )

    if collection.count() == 0:
        print("Populating collection with initial data...")
        documents = [
            "The quick brown fox jumps over the lazy dog.",
            "Never underestimate the power of a good book.",
            "Artificial intelligence is transforming the world."
        ]
        metadatas = [
            {"source": "sentence", "number": 1},
            {"source": "quote", "number": 2},
            {"source": "AI_news", "number": 3}
        ]
        ids = ["doc1", "doc2", "doc3"]
        collection.add(documents=documents, metadatas=metadatas, ids=ids)
        print(f"Added {collection.count()} documents.")
    else:
        print(f"Collection already contains {collection.count()} documents.")

    return collection

def configure_litestream():
    """
    Creates a litestream.yml configuration file for local replication.
    """
    print(f"
--- Configuring Litestream to monitor {PERSISTENT_DB_PATH}/chroma.sqlite3 ---")
    os.makedirs(LITESTREAM_WAL_DIR, exist_ok=True)
    with open(LITESTREAM_CONFIG_PATH, "w") as f:
        f.write(f"""
replicas:
  - path: {PERSISTENT_DB_PATH}/chroma.sqlite3
    url: file://{LITESTREAM_WAL_DIR}
""")
    print(f"Litestream configuration written to {LITESTREAM_CONFIG_PATH}")

def start_litestream_replication():
    """
    Starts Litestream in the background.
    """
    print("
--- Starting Litestream replication ---")
    if not os.path.exists(LITESTREAM_CONFIG_PATH):
        configure_litestream() # Ensure config exists

    # Check if litestream is installed
    if subprocess.run(["which", "litestream"], capture_output=True).returncode != 0:
        print("Error: Litestream not found. Please install Litestream to run this demo.")
        print("See: https://litestream.io/install/")
        return None

    process = subprocess.Popen(
        ["litestream", "replicate", "-config", LITESTREAM_CONFIG_PATH],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid # Start in a new process group
    )
    with open(LITESTREAM_PID_FILE, "w") as f:
        f.write(str(process.pid))
    print(f"Litestream started with PID {process.pid}")
    time.sleep(2) # Give Litestream a moment to start
    return process

def stop_litestream_replication(process: subprocess.Popen = None):
    """
    Stops the Litestream replication process.
    """
    if process:
        print("
--- Stopping Litestream replication ---")
        try:
            # Use os.killpg to kill the entire process group
            os.killpg(os.getpgid(process.pid), 9) # SIGKILL
            process.wait(timeout=5)
            print(f"Litestream process {process.pid} stopped.")
        except Exception as e:
            print(f"Could not stop Litestream process {process.pid}: {e}")
    if os.path.exists(LITESTREAM_PID_FILE):
        os.remove(LITESTREAM_PID_FILE)
    if os.path.exists(LITESTREAM_CONFIG_PATH):
        os.remove(LITESTREAM_CONFIG_PATH)

def simulate_data_loss():
    """
    Deletes the persistent ChromaDB SQLite file to simulate data loss.
    """
    db_file = os.path.join(PERSISTENT_DB_PATH, "chroma.sqlite3")
    print(f"
--- Simulating data loss: Deleting {db_file} ---")
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Deleted {db_file}")
    else:
        print(f"File {db_file} not found, already deleted or not created.")

def restore_chroma_db():
    """
    Restores the ChromaDB SQLite file from Litestream's local WAL.
    """
    print("
--- Restoring ChromaDB from Litestream WAL ---")
    db_file = os.path.join(PERSISTENT_DB_PATH, "chroma.sqlite3")
    # Ensure parent directory exists for the restored file
    os.makedirs(PERSISTENT_DB_PATH, exist_ok=True)
    command = ["litestream", "restore", "-config", LITESTREAM_CONFIG_PATH, db_file]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        print("Restoration successful.")
    else:
        print(f"Restoration failed: {result.stderr}")
    return result.returncode == 0

def verify_restored_data(client: chromadb.PersistentClient, expected_count: int) -> bool:
    """
    Verifies that the restored ChromaDB instance contains the expected data.
    """
    print("
--- Verifying restored data ---")
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=get_sentence_transformer_ef() # Need ef for get_or_create_collection
    )
    current_count = collection.count()
    print(f"Restored collection '{COLLECTION_NAME}' contains {current_count} documents.")
    if current_count == expected_count:
        print("Data count matches expected count. Restoration verified!")
        return True
    else:
        print(f"Error: Data count mismatch. Expected {expected_count}, got {current_count}.")
        return False

def run_wal_recovery_demo():
    print("Starting ChromaDB WAL Recovery Demo...")
    litestream_process = None
    try:
        # Cleanup any previous runs first
        cleanup_wal_recovery_demo()

        # 1. Setup persistent ChromaDB
        client = get_chroma_client(persistent=True, path=PERSISTENT_DB_PATH)
        ef = get_sentence_transformer_ef()
        collection = setup_chroma_wal_db(client, ef)
        expected_doc_count = collection.count()
        if expected_doc_count == 0:
            print("Demo requires initial data. Exiting.")
            return

        # 2. Configure and start Litestream
        configure_litestream()
        litestream_process = start_litestream_replication()
        if litestream_process is None:
            return # Litestream not installed

        # 3. Add more data while Litestream is running
        print("
--- Adding more data while Litestream replicates ---")
        collection.add(documents=["Additional data point."], metadatas=[{"source": "live"}], ids=["doc4"])
        print(f"Added new document. Collection count: {collection.count()}")
        expected_doc_count = collection.count()
        time.sleep(3) # Give Litestream time to replicate new WAL segment

        # 4. Simulate data loss
        stop_litestream_replication(litestream_process) # Stop Litestream before deleting the file it monitors
        litestream_process = None # Clear ref
        simulate_data_loss()

        # 5. Restore ChromaDB
        if not restore_chroma_db():
            print("Demo failed during restore phase.")
            return

        # 6. Verify restored data
        client_restored = get_chroma_client(persistent=True, path=PERSISTENT_DB_PATH)
        verify_restored_data(client_restored, expected_doc_count)

    except Exception as e:
        print(f"
An error occurred during the demo: {e}")
    finally:
        if litestream_process:
            stop_litestream_replication(litestream_process)
        cleanup_wal_recovery_demo()
        print("
ChromaDB WAL Recovery Demo Finished.")

def cleanup_wal_recovery_demo():
    """
    Cleans up all artifacts from the WAL recovery demo.
    """
    print(f"
--- Cleaning up WAL recovery demo artifacts ---")
    delete_chroma_data(PERSISTENT_DB_PATH)
    if os.path.exists(LITESTREAM_CONFIG_PATH):
        os.remove(LITESTREAM_CONFIG_PATH)
    if os.path.exists(LITESTREAM_WAL_DIR):
        import shutil
        shutil.rmtree(LITESTREAM_WAL_DIR)
    if os.path.exists(LITESTREAM_PID_FILE):
        os.remove(LITESTREAM_PID_FILE)
    print("Cleanup complete.")

if __name__ == "__main__":
    # Change into the project root to ensure relative paths work correctly
    # For standalone execution, it expects to be run from labs/chroma-agent-integration/
    # If run from parent, adjust paths
    original_cwd = os.getcwd()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    os.chdir(project_dir)

    try:
        run_wal_recovery_demo()
    finally:
        os.chdir(original_cwd) # Restore original working directory
