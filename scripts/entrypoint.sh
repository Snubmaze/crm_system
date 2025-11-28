#!/bin/sh
set -e

if [ ! -f ".env" ]; then
  echo "Creating .env from .env.example..."
  cp .env.example .env
fi

echo "Running DB seeder..."
python scripts/seed.py

echo "Starting FastAPI..."
uvicorn src.main:app --host 0.0.0.0 --port 8000
