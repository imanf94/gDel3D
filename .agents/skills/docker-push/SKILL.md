---
name: docker-push
description: Use this skill when the user wants to tag and push the Docker image to Docker Hub, or uses /docker-push or [DOCKER_PUSH].
---

# Docker Push Workflow

Follow these steps exactly:

1. Identify the current version tag of `conquer3d` (e.g., `v0.0.1`).
2. Tag the `conquer3d:latest` and `conquer3d:<version>` images with the `kohido` username:
   - `docker tag conquer3d:latest kohido/conquer3d:latest`
   - `docker tag conquer3d:<version> kohido/conquer3d:<version>`
3. Push both tagged images to Docker Hub:
   - `docker push kohido/conquer3d:latest`
   - `docker push kohido/conquer3d:<version>`
