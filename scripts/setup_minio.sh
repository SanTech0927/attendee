#!/bin/bash
# Set up MinIO for local S3-compatible storage
# Usage: ./scripts/setup_minio.sh

set -e

MINIO_ROOT_USER="${MINIO_ROOT_USER:-minioadmin}"
MINIO_ROOT_PASSWORD="${MINIO_ROOT_PASSWORD:-minioadmin}"
MINIO_DATA_DIR="${MINIO_DATA_DIR:-$HOME/.minio/data}"
MINIO_BUCKET="${MINIO_BUCKET:-attendee-recordings}"

echo "==================================="
echo "MinIO Setup for Attendee"
echo "==================================="
echo ""

# Install MinIO if not present
if ! command -v minio &> /dev/null; then
    echo "Installing MinIO server..."
    wget -q https://dl.min.io/server/minio/release/linux-amd64/minio -O /tmp/minio
    sudo mv /tmp/minio /usr/local/bin/minio
    sudo chmod +x /usr/local/bin/minio
fi

# Install MinIO client if not present
if ! command -v mc &> /dev/null; then
    echo "Installing MinIO client (mc)..."
    wget -q https://dl.min.io/client/mc/release/linux-amd64/mc -O /tmp/mc
    sudo mv /tmp/mc /usr/local/bin/mc
    sudo chmod +x /usr/local/bin/mc
fi

# Create data directory
mkdir -p "$MINIO_DATA_DIR"

echo ""
echo "MinIO installed successfully!"
echo ""
echo "==================================="
echo "MinIO Configuration"
echo "==================================="
echo ""
echo "Add these to your .env file:"
echo ""
echo "  AWS_ENDPOINT_URL=http://localhost:9000"
echo "  AWS_ACCESS_KEY_ID=$MINIO_ROOT_USER"
echo "  AWS_SECRET_ACCESS_KEY=$MINIO_ROOT_PASSWORD"
echo "  AWS_RECORDING_STORAGE_BUCKET_NAME=$MINIO_BUCKET"
echo ""
echo "==================================="
echo "Starting MinIO"
echo "==================================="
echo ""
echo "To start MinIO, run:"
echo "  ./scripts/run_minio.sh"
echo ""
echo "MinIO Console will be available at: http://localhost:9001"
echo "  Username: $MINIO_ROOT_USER"
echo "  Password: $MINIO_ROOT_PASSWORD"
echo ""
