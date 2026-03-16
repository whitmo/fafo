## Context

The demo aims to showcase Litestream's local restoration capabilities for an SQLite database. This involves setting up Litestream to monitor an SQLite database, simulating data loss, and then restoring the database from the locally stored WAL files. The demo needs to be self-contained and easy to understand.

## Goals / Non-Goals

**Goals:**
- Create a runnable script or simple application demonstrating SQLite database creation, population, querying, deletion, and Litestream-based restoration.
- Ensure the Litestream configuration is for local WAL storage.
- Provide clear steps for execution and verification.

**Non-Goals:**
- Implementing complex database schemas or application logic beyond the scope of the demo.
- Configuring Litestream with remote storage backends (e.g., S3, WebDAV) - focus is solely on local restoration.
- Production-grade error handling or performance optimization.

## Decisions

- **Language/Scripting:** Use a Bash script for simplicity and direct execution of command-line tools (sqlite3, litestream, rm). This avoids introducing additional language dependencies for a simple demo.
- **SQLite Database Operations:** Utilize the `sqlite3` command-line tool for creating the database, defining schema, inserting data, and querying. This is native to SQLite and common.
- **Litestream Configuration:** Create a `litestream.yml` file to configure Litestream to replicate the SQLite database to a local directory. This provides explicit configuration and is the standard way to use Litestream.
- **Simulation of Data Loss:** Employ the `rm` command to delete the SQLite database file to simulate data loss.
- **Restoration:** Use Litestream's `restore` command to restore the database from the local WAL directory.

## Risks / Trade-offs

- **Dependency on Litestream:** Users need to have Litestream installed. → Mitigation: Document Litestream installation as a prerequisite in the tasks.
- **Local-only restoration:** The demo explicitly focuses on local restoration, which might not fully represent Litestream's cloud capabilities. → Trade-off accepted for demo simplicity and focused scope.

## Open Questions

- None at this time.
