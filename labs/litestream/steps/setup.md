# Setup Environment

Create the demo directory structure. We need a place for the SQLite database and a separate directory where Litestream will store WAL replicas.

```sh
mkdir -p litestream_demo_env/wal

ls -la litestream_demo_env/
```

Create a SQLite database with a simple `users` table and insert some
sample data. Query the database to confirm the data is there:

```sh
sqlite3 litestream_demo_env/demo.db "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT); INSERT INTO users (name) VALUES ('Alice'); INSERT INTO users (name) VALUES ('Bob');"
sqlite3 litestream_demo_env/demo.db "SELECT * FROM users;"
```
