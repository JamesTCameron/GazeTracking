# Docker Usage Guide

This document explains how to use the Docker image for GazeTracking.

## Pulling the Image

Once the CI/CD pipeline is set up, you can pull the pre-built image from GitHub Container Registry:

```bash
docker pull ghcr.io/jamestcameron/gazetracking:latest
```

### Available Tags

- `latest` - Latest build from the master branch
- `master` - Latest build from the master branch
- `v*` - Specific version tags (e.g., `v1.0.0`)
- `sha-<commit>` - Specific commit builds

## Running the Container

### Basic Usage

```bash
docker run -it --rm ghcr.io/jamestcameron/gazetracking:latest
```

### With Webcam Access

To use the webcam with the Docker container (requires X11 forwarding on Linux):

```bash
xhost +local:docker
docker run -it --rm \
  --device=/dev/video0 \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ghcr.io/jamestcameron/gazetracking:latest \
  python3 example.py
```

### Interactive Shell

To get an interactive shell inside the container:

```bash
docker run -it --rm ghcr.io/jamestcameron/gazetracking:latest /bin/bash
```

## Building Locally

If you prefer to build the image locally:

```bash
docker build -t gazetracking:local .
```

## CI/CD Pipeline

The Docker image is automatically built and pushed to GitHub Container Registry when:

- Code is pushed to the `master` branch
- A new tag starting with `v` is created (e.g., `v1.0.0`)
- Manually triggered via GitHub Actions

### Multi-Architecture Support

The CI/CD pipeline builds images for both:
- `linux/amd64` (Intel/AMD processors)
- `linux/arm64` (ARM processors, including Apple Silicon)

## Workflow Features

- **Automatic tagging**: Images are tagged based on branch names, semantic versions, and commit SHAs
- **Layer caching**: GitHub Actions cache is used to speed up subsequent builds
- **Pull request builds**: Images are built (but not pushed) for pull requests to verify they build successfully
- **Latest tag**: The `latest` tag is automatically updated when pushing to the default branch

## Configuration

The workflow uses the `GITHUB_TOKEN` automatically provided by GitHub Actions, so no additional secrets need to be configured. The images are automatically pushed to `ghcr.io/jamestcameron/gazetracking`.

## Accessing Private Images

If your repository is private, you'll need to authenticate to pull images:

```bash
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
docker pull ghcr.io/jamestcameron/gazetracking:latest
```
