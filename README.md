# gDel3D: GPU-Accelerated 3D Delaunay Triangulation

A refactored, modernized repository of **gDel3D** optimized for recent CUDA architectures (sm_70 through sm_120+ including NVIDIA Blackwell), equipped with high-performance PyTorch C++ CUDA extension bindings.

Original repository: https://github.com/ashwin/gDel3D

## Installation & Python Bindings

### 1. Prerequisites
Ensure you have a modern C++ host compiler, an NVIDIA CUDA Toolchain (e.g., CUDA Toolkit 12.x), and PyTorch with CUDA enabled:

```bash
# Optional: Create a dedicated Conda environment with compatible CUDA compilers
conda create -c conda-forge -n gdel3d python=3.10 gxx_linux-64=13 gcc_linux-64=13 -y
conda activate gdel3d
conda install nvidia::cuda-toolkit==12.8.2 -y

# Install PyTorch with CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

### 2. Install PyTorch CUDA Extension
You can install the Python bindings directly from GitHub without build isolation:
```bash
pip install git+https://github.com/KhoiDOO/gDel3D.git --no-build-isolation
```

Or clone the repository and install locally in editable mode:
```bash
git clone https://github.com/KhoiDOO/gDel3D.git
cd gDel3D
pip install -e . --no-build-isolation
```

### 3. Python Quickstart Example
Once installed, you can directly execute GPU-accelerated 3D Delaunay tetrahedralization on PyTorch tensors:
```python
import torch
import gdel3d_cuda

# Create random 3D points on GPU (float32 or float64)
num_points = 5000
points = (torch.rand(num_points, 3, dtype=torch.float64, device='cuda') * 100.0).contiguous()

# Compute 3D Delaunay tetrahedralization (returns integer tensor of indices)
tets = gdel3d_cuda.tetrahedralize_cuda(points)

print(f"Generated {tets.shape[0]} tetrahedra of shape {tets.shape} on {tets.device}")
```

---

## Standalone C++ Demo Build

CMake is supported to build the native C++ benchmarking demo executable on Linux:

```bash
mkdir build
cd build
cmake ..
make -j
./gflip3d # Run the standalone test & demo binary
```

---

## Algorithm & Attribution

This program constructs the Delaunay Triangulation of a set of arbitrary points in 3D using NVIDIA GPUs. The underlying engine utilizes high-speed incremental insertion and parallel flipping on the GPU, combined with robust CPU star splaying post-processing for degenerate topological cases—delivering exact geometric parity with traditional scientific libraries (such as SciPy / Qhull) at significantly faster processing rates.

### Original Authors
- **Cao Thanh Tung**
- **Ashwin Nanjappa**
- For further internal structural details on input/output definitions, refer to [CommonTypes.h](GDelFlipping/src/gDel3D/CommonTypes.h) and [GpuDelaunay.h](GDelFlipping/src/gDel3D/GpuDelaunay.h).
