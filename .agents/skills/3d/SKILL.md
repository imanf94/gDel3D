---
name: 3d
description: Specialized 3D Vision, Computer Graphics, and Differentiable Geometry planning and execution skill. Extends /plan by conducting deep domain-specific technical grilling (coordinates, differentiability, CUDA architectures, memory layouts, and numerical edge cases) and drafting an interactive 4-stage Plan Artifact before writing code. Use when developing 3D algorithms, CUDA geometry kernels, or neural rendering pipelines, or using /3d or [3D].
---

# 3D Vision, Graphics & Differentiable Geometry Planning Workflow

When this skill is activated (or the user uses `/3d` or `[3D]`), act as a Principal 3D Computer Graphics & Geometric AI Engineer. You MUST NOT jump directly into coding. Follow this disciplined three-phase engineering framework:

```
[Phase 1: Domain-Specific Technical Grilling]
                    ↓
[Phase 2: Interactive 4-Stage Plan Artifact]
                    ↓ (User Review & Approval)
[Phase 3: Precision Implementation & Verification]
```

---

## Phase 1: Domain-Specific Technical Grilling (Mandatory Interview)

Before drafting an implementation plan, systematically interrogate the problem and user requirements across the core 3D engineering dimensions. Use the `ask_question` tool whenever choices or requirements are ambiguous.

### 1. Geometric & Coordinate Frame Conventions
- **World & Camera Frames**: What is the coordinate standard (OpenGL/NeRF $[+X\text{ right}, +Y\text{ up}, -Z\text{ view}]$, OpenCV/Colmap $[+X\text{ right}, +Y\text{ down}, +Z\text{ view}]$, or Blender/Robotics $[+Z\text{ up}]$)?
- **Winding Order & Face Orientations**: Counter-Clockwise (CCW) vs Clockwise (CW) outward normals?
- **Spatial Bounding & Scale**: Normalized unit cube $[-1, 1]^3$, unit sphere, or unconstrained world coordinates?

### 2. Differentiability & Gradient Propagation
- **Gradient Requirements**: Forward-only inference, custom analytical backward CUDA kernel, or pure PyTorch autograd graph?
- **Isosurface / Surface Gradients**: If extracting explicit surfaces from implicit fields (SDF/UDF), how are gradients backpropagated through zero-crossings (e.g. Implicit Differentiation Theorem, differentiable Marching Cubes/Tetrahedra, or discrete approximation)?

### 3. GPU Hardware, Concurrency & Memory Layout
- **Spatial Representation**: Dense volumetric grid, sparse active voxels, Morton/Z-curve hash table, or BVH/KD-tree?
- **Memory Optimization**: Can intermediate states use compact datatypes (e.g., `int8_t` masks, bit-packed occupancy, half precision)?
- **Atomic Operations**: Are concurrent updates required? Use lock-free atomics (e.g., custom sub-word `atomicCAS_int8` for byte-level voxel grids) to prevent thread divergence.
- **PyTorch Memory Integration**: Ensure zero-copy contiguous pointer passing (`data_ptr<T>()`) and bind Thrust operations to PyTorch's `ATen::cuda::ThrustAllocator` to eliminate runtime CUDA allocations.

### 4. Topology & Numerical Robustness
- **Manifold Constraints**: Does the output require watertight 2-manifold topology (no non-manifold vertices/edges)?
- **Degeneracies & Exact Predicates**: How should degenerate triangles/tetrahedra (near-zero volume/area) or self-intersections be handled?
- **SDF Sign Determination**: If evaluating sign parity, which method fits best (Ray Parity, Fast Winding Numbers, Pseudonormals, Volumetric Flood Fill, or Hybrid Consensus)?

> **Note on Flexibility**: Adapt the depth of grilling to the task's scope. For simple helper utilities or transforms, do not over-complicate the interview; for custom CUDA geometry kernels, isosurface extractors, or differentiable rendering pipelines, conduct rigorous checks.

---

## Phase 2: Interactive 4-Stage Plan Artifact

Once technical requirements are aligned, synthesize the strategy into a structured **Plan Artifact** (with `RequestFeedback: true`) before writing code:

### Stage 1: Mathematical & Geometric Formulation
- Core mathematical equations, coordinate mappings, and geometric formulations.
- Sign evaluation heuristics, projection feature Voronoi regions, or interpolation formulas.

### Stage 2: CUDA & C++ Hardware Architecture
- Thread block dimensions, grid layouts, and warp-level primitives.
- Memory hierarchies (shared memory, constant memory tables, device buffers).
- Synchronization, lock-free atomics, and avoidance of thread divergence.

### Stage 3: PyTorch API & Differentiability
- Python frontend function/class signatures, docstrings, and tensor input/output shape specs.
- PyTorch C++ / CUDA extension bindings (`pybind.cpp`).
- Autograd Function definition (forward and analytical backward passes).

### Stage 4: Verification & Flexible Testing Strategy
- **Complex Kernels**: Numerical parity validation against reference CPU baselines (SciPy, PyVista, Libigl) and analytical test cases.
- **Lightweight / Simple Tasks**: Focused unit tests, gradient checks (`torch.autograd.gradcheck`), and boundary condition assertions.

---

## Phase 3: Precision Implementation & Verification

1. **Wait for Approval**: Proceed to implementation only after the user reviews and confirms the Plan Artifact.
2. **Execute Systematically**: Implement backend C++/CUDA kernels first, followed by PyBind11 bindings, Python high-level APIs, and test suites.
3. **Verify Numerically**: Run test benchmarks to validate correctness, memory stability, and performance.
4. **Offer Downstream Skills**: Upon successful verification, suggest convenient follow-up actions (e.g., `/commit` to save individual conventional commits, `/build` or `/cbr` to publish releases).
