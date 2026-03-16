## ADDED Requirements

### Requirement: SQLite Litestream Local Restore Demo
The system SHALL provide a demo that creates, populates, queries, deletes, and restores an SQLite database using Litestream for local WAL storage.

#### Scenario: Database creation and population
- **WHEN** the demo script is executed
- **THEN** an SQLite database file SHALL be created and populated with sample data.

#### Scenario: Litestream configuration
- **WHEN** the demo script is executed
- **THEN** Litestream SHALL be configured to replicate the SQLite database to a local directory.

#### Scenario: Database querying
- **WHEN** the demo script queries the populated database
- **THEN** the expected data SHALL be returned.

#### Scenario: Database deletion
- **WHEN** the demo script deletes the SQLite database file
- **THEN** the database file SHALL no longer exist.

#### Scenario: Database restoration
- **WHEN** the demo script restores the database using Litestream
- **THEN** the SQLite database file SHALL be re-created with the original data.

#### Scenario: Query restored database
- **WHEN** the demo script queries the restored database
- **THEN** the expected data SHALL be returned.
