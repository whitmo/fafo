## Why

To demonstrate the resilience and disaster recovery capabilities of a SQLite database when paired with Litestream for continuous backup and restoration, particularly in a local development environment. This demo will illustrate how data can be restored efficiently after accidental deletion, addressing a common concern with local data persistence for SQLite.

## What Changes

This change will introduce a new demo script or application that performs the following sequence:
- SQLite database creation and schema definition.
- Litestream configuration for local WAL (Write-Ahead Log) storage.
- Data insertion and querying.
- Simulation of data loss (database file deletion).
- Restoration of the database using Litestream.

## Capabilities

### New Capabilities
- `sqlite-litestream-local-restore`: Demonstrates the local restoration of an SQLite database using Litestream WAL files.

### Modified Capabilities
<!-- Existing capabilities whose REQUIREMENTS are changing (not just implementation).
     Only list here if spec-level behavior changes. Each needs a delta spec file.
     Use existing spec names from openspec/specs/. Leave empty if no requirement changes. -->

## Impact

The demo will primarily impact developer tooling and example code. It will provide a clear, executable example of Litestream's functionality, which can be integrated into documentation or used for educational purposes.
