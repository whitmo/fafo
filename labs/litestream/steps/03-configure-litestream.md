# Configure Litestream

Write a Litestream configuration that replicates the database's WAL to a local directory. In production you'd point this at S3 or another remote store, but local replication works for demonstrating the concept.

```sh
cat > litestream_demo_env/litestream.yml <<'EOF'
dbs:
  - path: litestream_demo_env/demo.db
    replicas:
      - path: litestream_demo_env/wal
EOF
```

Start Litestream in the background. It will continuously watch the database and replicate WAL changes.

```sh
litestream replicate -config litestream_demo_env/litestream.yml &
```

Give it a moment, then verify the replica directory has content:

```sh
ls -la litestream_demo_env/wal/
```
