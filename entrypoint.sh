#!/bin/sh

set -e

echo "Running DB initializer..."
python seed.py

echo "Starting FastAPI server..."
uvicorn src.main:app --host 0.0.0.0 --port 8000
