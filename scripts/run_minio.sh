#!/bin/bash
# Run MinIO server
# Usage: ./scripts/run_minio.sh

MINIO_ROOT_USER="${MINIO_ROOT_USER:-minioadmin}"
MINIO_ROOT_PASSWORD="${MINIO_ROOT_PASSWORD:-minioadmin}"
MINIO_DATA_DIR="${MINIO_DATA_DIR:-$HOME/.minio/data}"
MINIO_BUCKET="${MINIO_BUCKET:-attendee-recordings}"

# Create data directory
mkdir -p "$MINIO_DATA_DIR"

echo "Starting MinIO server..."
echo ""
echo "API:     http://localhost:9000"
echo "Console: http://localhost:9001"
echo "User:    $MINIO_ROOT_USER"
echo "Pass:    $MINIO_ROOT_PASSWORD"
echo ""

# Start MinIO in background and wait for it to be ready
MINIO_ROOT_USER=$MINIO_ROOT_USER MINIO_ROOT_PASSWORD=$MINIO_ROOT_PASSWORD \
    minio server "$MINIO_DATA_DIR" --console-address ":9001" &

MINIO_PID=$!

# Wait for MinIO to start
echo "Waiting for MinIO to start..."
sleep 3

# Configure mc client
mc alias set local http://localhost:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD 2>/dev/null || true

# Create bucket if it doesn't exist
if ! mc ls local/$MINIO_BUCKET &>/dev/null; then
    echo "Creating bucket: $MINIO_BUCKET"
    mc mb local/$MINIO_BUCKET
fi

echo ""
echo "MinIO is running! Bucket '$MINIO_BUCKET' is ready."
echo "Press Ctrl+C to stop."
echo ""

# Wait for MinIO process
wait $MINIO_PID
