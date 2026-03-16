## 1. Setup Environment

- [x] 1.1 Ensure Litestream is installed and accessible in the PATH.
- [x] 1.2 Create a dedicated directory for the demo files (database, WAL, script, config).

## 2. SQLite Database Operations

- [x] 2.1 Create an SQLite database file (`demo.db`).
- [x] 2.2 Define a simple table schema (e.g., `CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);`).
- [x] 2.3 Populate the table with sample data (e.g., `INSERT INTO users (name) VALUES ('Alice'), ('Bob');`).
- [x] 2.4 Implement a query to retrieve data from the table to verify population.

## 3. Litestream Configuration

- [x] 3.1 Create a `litestream.yml` configuration file.
- [x] 3.2 Configure Litestream to replicate `demo.db` to a local directory (e.g., `replicas: - url: file:///path/to/local/wal/dir`).
- [x] 3.3 Start Litestream in the background to monitor the database.

## 4. Demo Flow Implementation

- [x] 4.1 Write a shell script (`run_demo.sh`) to orchestrate the steps.
- [x] 4.2 Include steps to create and populate the database.
- [x] 4.3 Include a step to query the database.
- [x] 4.4 Simulate data loss by deleting `demo.db`.
- [x] 4.5 Implement the Litestream restore command to recover `demo.db`.
- [x] 4.6 Include a final query after restoration to verify data integrity.

## 5. Cleanup

- [x] 5.1 Add commands to the script or a separate cleanup script to remove `demo.db`, `litestream.yml`, and the local WAL directory.
