---
name: docker
description: Use this skill when the user wants to build and test the conquer3d Docker image, or uses /docker or [DOCKER].
---

# Docker Build Workflow

Follow these steps exactly:

1. Check the current tags of the `conquer3d` image using `docker images`.
2. If no tag exists, set the initial tag to `conquer3d:v0.0.0`. If tags exist, determine the latest version and increment the patch version (e.g., from `v0.0.0` to `v0.0.1`).
3. Run `docker build -t conquer3d:<new_version> -t conquer3d:latest .`
4. After building, verify the installation inside the container by running:
   ```bash
   docker run --rm --gpus all conquer3d:latest bash -c "nvidia-smi && python -c 'import torch, conquer3d; print(\"CUDA Available:\", torch.cuda.is_available()); print(\"Conquer3D Version:\", conquer3d.__version__)'"
   ```
