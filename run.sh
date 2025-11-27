#!/bin/bash

set -e

IMAGE_NAME="lead-service"
CONTAINER_NAME="lead-service-container"
PORT=8000

echo "=== Stopping old container (if exists) ==="
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true

echo "=== Building Docker image ==="
docker build --no-cache -t $IMAGE_NAME .

echo "=== Running container ==="
docker run -d \
    --name $CONTAINER_NAME \
    -p ${PORT}:8000 \
    $IMAGE_NAME

echo "=== Container started ==="
echo "→ http://localhost:${PORT}"
