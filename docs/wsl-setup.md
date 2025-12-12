# Running Attendee on WSL (Without Docker)

This guide explains how to run the Attendee project directly on WSL without using Docker.

## Quick Start

```bash
# 1. Run the setup script
./scripts/wsl_setup.sh

# 2. Set up the database
./scripts/setup_db.sh

# 3. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Generate environment file
python init_env.py > .env

# 6. Run database migrations
export DJANGO_SETTINGS_MODULE=attendee.settings.local
python manage.py migrate

# 7. Start all services
./scripts/run_local.sh
```

## Using MinIO Instead of AWS S3 (Optional)

MinIO provides S3-compatible storage locally, saving AWS costs during development.

### Setup MinIO

```bash
# Install MinIO
./scripts/setup_minio.sh

# Start MinIO (in a separate terminal)
./scripts/run_minio.sh
```

### Configure .env for MinIO

Update your `.env` file:

```bash
AWS_ENDPOINT_URL=http://localhost:9000
AWS_ACCESS_KEY_ID=minioadmin
AWS_SECRET_ACCESS_KEY=minioadmin
AWS_RECORDING_STORAGE_BUCKET_NAME=attendee-recordings
```

### Access MinIO Console

- **URL:** http://localhost:9001
- **Username:** minioadmin
- **Password:** minioadmin

## Available Scripts

| Script | Description |
|--------|-------------|
| `scripts/wsl_setup.sh` | Install all system dependencies |
| `scripts/setup_db.sh` | Create PostgreSQL database and user |
| `scripts/start_services.sh` | Start PostgreSQL and Redis |
| `scripts/setup_minio.sh` | Install MinIO for local S3 storage |
| `scripts/run_minio.sh` | Start MinIO server |
| `scripts/run_local.sh` | Start all services (Django + Celery) |
| `scripts/run_server.sh` | Start Django server only |
| `scripts/run_worker.sh` | Start Celery worker only |
| `scripts/run_scheduler.sh` | Start Celery scheduler only |

## Accessing the Application

- **Main application:** http://localhost:8000
- **API documentation:** http://localhost:8000/api/v1/
