# Visual Explainer: SQLite & Litestream for Local Recovery

This document provides a conceptual overview of how Litestream enables local recovery for SQLite databases.

## The Problem: SQLite Data Loss

SQLite databases are single files. If this file is accidentally deleted, corrupted, or overwritten, the data is lost. This is a significant risk, especially in local development environments where backups might not be rigorously maintained.

```
+------------+
|  Your App  |
+----|-------+
     |
     v
+----------+
| demo.db  |  (Single SQLite file)
+----------+
     |
     v
   [DELETED!]  <-- Data Loss Event
```

## The Solution: Litestream for Continuous WAL Replication

Litestream is a standalone stream replicator for SQLite. It continuously monitors changes to your SQLite database's Write-Ahead Log (WAL) and replicates them to a configurable destination. In this demo, the destination is a local directory.

### Key Components:

1.  **SQLite Database (`demo.db`):** Your primary data store.
2.  **SQLite Write-Ahead Log (`demo.db-wal`):** Where all changes are initially written before being committed to the main database file. Litestream taps into this.
3.  **Litestream Process:** A background process that reads the WAL and pushes changes to the replica.
4.  **Local WAL Replica (`./wal` directory):** A local directory where Litestream stores copies of the WAL segments.

### The Flow:

1.  **Application Writes Data:** Your application makes changes to `demo.db`. These changes are first written to `demo.db-wal`.

    ```
    +------------+      +----------+      +----------------+
    |  Your App  | ---> | demo.db  | <--- | demo.db-wal    |
    +----|-------+      +----------+      +----------------+
         |                                         ^
         |                                         |
         +-----------------------------------------+
    ```

2.  **Litestream Replicates WAL:** The Litestream process continuously observes `demo.db-wal`. As new changes appear, Litestream copies these WAL segments to the local replica directory.

    ```
    +------------+      +----------+      +----------------+
    |  Your App  | ---> | demo.db  | <--- | demo.db-wal    |
    +----|-------+      +----------+      +----------------+
         |                                         ^
         |                                         |  Litestream
         |                                         |  (Replication)
         v                                         |
    (Writes/Reads)                                 |
                                                   |
    +----------------------------------------------+
    | Local WAL Replica (e.g., ./wal/snapshot.db, ./wal/*.wal)
    +-------------------------------------------------------------+
    ```

3.  **Data Loss Occurs (`demo.db` deleted):** Your primary `demo.db` file is lost.

    ```
    +------------+
    |  Your App  | X  +----------+ (Deleted!)
    +----|-------+    +----------+
         |
    (Cannot Access)

    Meanwhile...
    +-------------------------------------------------------------+
    | Local WAL Replica (e.g., ./wal/snapshot.db, ./wal/*.wal)    |
    |  - Contains full history of changes                        |
    +-------------------------------------------------------------+
    ```

4.  **Restoration with Litestream:** You use the `litestream restore` command. Litestream takes the latest full snapshot from the local replica and then applies all subsequent WAL segments to reconstruct the `demo.db` file to its most recent state.

    ```
    +-------------------------------------------------------------+
    | Local WAL Replica                                           |
    |  (litestream restore command reads from here)               |
    +----|--------------------------------------------------------+
         |
         v (Reconstructs)
    +----------+
    | demo.db  | (Restored!)
    +----------+

    +------------+
    |  Your App  | ---> +----------+
    +------------+      | demo.db  | (Data Recovered!)
                        +----------+
    ```

This process ensures that even if your primary SQLite database file is lost, you can recover it quickly from the locally stored WAL logs, minimizing data loss.
