#!/bin/bash

# GazeTracking Docker Launcher
# This script runs the gaze tracking application in a Docker container
# with webcam and X11 display access (no sudo required)

IMAGE_NAME=gaze-tracking

# Build image if it doesn't exist
if [ "$(docker images -q ${IMAGE_NAME})" == "" ]; then
    echo "Building Docker image..."
    docker build -t ${IMAGE_NAME} .
fi

# Allow Docker to access X11 display
xhost +local:docker

# Run the gaze tracking application
echo "Starting gaze tracking..."
docker run --rm \
  --device /dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  --env="QT_X11_NO_MITSHM=1" \
  ${IMAGE_NAME} \
  python3 example.py
