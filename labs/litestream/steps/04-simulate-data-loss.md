# Simulate Data Loss and Restore

Now simulate a disaster — delete the database file entirely.

```sh
rm litestream_demo_env/demo.db
```

Try to query the (now missing) database. This should fail:

```sh
sqlite3 litestream_demo_env/demo.db "SELECT * FROM users;" 2>&1 || echo "Database is gone!"
```

Stop the Litestream background process first, then use `litestream restore` to rebuild the database from the WAL replica.

```sh
pkill -f "litestream replicate" || true
```

Restore the database from the local replica:

```sh
litestream restore -config litestream_demo_env/litestream.yml litestream_demo_env/demo.db
```

Query the restored database — the data should be back:

```sh
sqlite3 litestream_demo_env/demo.db "SELECT * FROM users;"
```
