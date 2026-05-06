#!/bin/bash

IMAGE_NAME="ros2_lidar_simulation"

echo "Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

echo "Running Docker container from image: $IMAGE_NAME"
docker run --rm $IMAGE_NAME