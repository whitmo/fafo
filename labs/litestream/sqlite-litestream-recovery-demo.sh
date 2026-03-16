#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status

DEMO_DIR="labs/litestream_demo_env"
DB_FILE="$DEMO_DIR/demo.db"
LITESTREAM_CONFIG="$DEMO_DIR/litestream.yml"
WAL_DIR="$DEMO_DIR/wal"
LITESTREAM_PID_FILE="$DEMO_DIR/litestream.pid"

echo "--- SQLite Litestream Local Recovery Demo ---"

# --- 1. Setup Environment ---
echo "1. Setting up demo environment..."
mkdir -p "$DEMO_DIR"
mkdir -p "$WAL_DIR"
echo "   Created $DEMO_DIR and $WAL_DIR"

# --- 2. SQLite Database Operations ---
echo "2. Creating and populating SQLite database..."
sqlite3 "$DB_FILE" <<EOF
CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
INSERT INTO users (name) VALUES ('Alice');
INSERT INTO users (name) VALUES ('Bob');
.quit
EOF
echo "   Database '$DB_FILE' created and populated."

echo "   Querying initial database:"
sqlite3 "$DB_FILE" "SELECT * FROM users;"
echo ""

# --- 3. Litestream Configuration ---
echo "3. Configuring Litestream for local replication..."
cat > "$LITESTREAM_CONFIG" <<EOF
replicas:
  - path: $DB_FILE
    url: file://$WAL_DIR
EOF
echo "   Litestream configuration '$LITESTREAM_CONFIG' created."

echo "   Starting Litestream in the background..."
# Check if litestream command exists
if ! command -v litestream &> /dev/null
then
    echo "Error: litestream command not found. Please install Litestream."
    echo "       (e.g., brew install litestream on macOS, or see litestream.io)"
    exit 1
fi
litestream replicate -config "$LITESTREAM_CONFIG" &
LITESTREAM_PID=$!
echo "$LITESTREAM_PID" > "$LITESTREAM_PID_FILE"
echo "   Litestream started with PID: $LITESTREAM_PID"
sleep 2 # Give Litestream a moment to start replication

# --- 4. Demo Flow Implementation (Simulation of Data Loss) ---
echo "4. Simulating database loss: Deleting '$DB_FILE'..."
rm "$DB_FILE"
echo "   '$DB_FILE' deleted."
if [ ! -f "$DB_FILE" ]; then
    echo "   Database file confirmed deleted."
else
    echo "   Warning: Database file still exists after deletion attempt."
fi
echo ""

echo "   Attempting to query deleted database (should fail or be empty):"
if sqlite3 "$DB_FILE" "SELECT * FROM users;" &> /dev/null; then
    echo "   Query succeeded (unexpected - database might not have been deleted)."
else
    echo "   Query failed as expected (database is gone)."
fi
echo ""

echo "5. Restoring database from local WAL files..."
# Ensure Litestream is stopped before restoring the database file it manages.
if [ -f "$LITESTREAM_PID_FILE" ]; then
    LITESTREAM_RUNNING_PID=$(cat "$LITESTREAM_PID_FILE")
    echo "   Stopping Litestream process (PID: $LITESTREAM_RUNNING_PID) before restore..."
    kill "$LITESTREAM_RUNNING_PID" || true # Kill the background litestream process
    wait "$LITESTREAM_RUNNING_PID" 2>/dev/null || true # Wait for it to terminate
    rm "$LITESTREAM_PID_FILE"
fi

litestream restore -config "$LITESTREAM_CONFIG" "$DB_FILE"
echo "   Database restored."
echo ""

echo "   Querying restored database:"
sqlite3 "$DB_FILE" "SELECT * FROM users;"
echo ""

# --- 5. Cleanup ---
echo "6. Cleaning up demo environment..."
# Ensure Litestream is stopped before cleaning up
if [ -f "$LITESTREAM_PID_FILE" ]; then
    LITESTREAM_RUNNING_PID=$(cat "$LITESTREAM_PID_FILE")
    echo "   Stopping Litestream process (PID: $LITESTREAM_RUNNING_PID)..."
    kill "$LITESTREAM_RUNNING_PID" || true # Kill the background litestream process
    wait "$LITESTREAM_RUNNING_PID" 2>/dev/null || true # Wait for it to terminate
fi

rm -rf "$DEMO_DIR"
echo "   Cleaned up '$DEMO_DIR'."
echo ""
echo "--- Demo Complete ---"
