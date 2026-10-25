---
name: docs
description: Use this skill when the user wants to scan through all coding file types (.c, .h, .cpp, .cuh, .cu, .py, and PyBind11 bindings) and add, improve, revise, or standardize docstrings and documentation for every function, class, struct, kernel, host dispatcher, and binding, or uses /docs or [DOCS].
---

# Multi-Language Documentation & Docstring Standard Workflow

When this skill is activated (or the user uses `/docs` or `[DOCS]`), systematically discover, audit, and enhance documentation across every coding file in the workspace.

You MUST write clear, exhaustive, and technically precise docstrings for every function, method, class, struct, CUDA `__global__` / `__device__` kernel, host launcher, and PyBind11 binding across all targeted file extensions:
- **`.py`**: Python Modules, Classes, Functions, Transforms, and Datasets (Google Python Style Guide).
- **`.cu`**: CUDA Kernel Implementations, Launchers, Device Helpers, and Warp Algorithms (Doxygen GPU Standard).
- **`.cuh`**: CUDA Device Headers, Data Layouts, and Shared Kernel Declarations (Doxygen GPU Standard).
- **`.cpp`**: C++ Implementation Files, Host Dispatchers, and PyBind11 Bindings (Doxygen & PyBind11 Standard).
- **`.h` / `.hpp`**: C/C++ Header Files, Public API Declarations, and Struct/Class Definitions (Doxygen Standard).
- **`.c`**: C Source Files and Core Computational Kernels (Doxygen Standard).

---

## Workflow Overview

```
[Phase 1: Universal Codebase Discovery & Inventory]
  ├── Python (.py, .pyi)
  ├── CUDA (.cu, .cuh)
  ├── C++ (.cpp, .hpp)
  └── C (.c, .h)
                        ↓
[Phase 2: Documentation Quality & Coverage Audit]
                        ↓
[Phase 3: Standardized Multi-Language Docstring Authoring]
  ├── Python (.py): Google Python Style Guide
  ├── C / C++ (.c, .h, .cpp, .hpp): Doxygen Standard (API Contracts & Types)
  ├── CUDA (.cu, .cuh): Doxygen GPU Standard (Hardware Bounds, Memory & Concurrency)
  └── PyBind11 (.cpp): Rich Embedded Python Signatures (R"pbdoc(...)pbdoc")
                        ↓
[Phase 4: Zero-Regression & Build Verification]
```

---

## Phase 1: Universal Codebase Discovery & Inventory

1. **Discover All Coding Files by Extension**:
   - Locate and categorize source files across the workspace:
     - **`.py`**: Python source code and stubs (`.py`, `.pyi`).
     - **`.cu`**: Native CUDA kernel implementations and host dispatchers.
     - **`.cuh`**: CUDA device header declarations, inline math routines, and memory layouts.
     - **`.cpp`**: C++ translation units, host algorithms, and PyBind11 binding definitions.
     - **`.h` / `.hpp`**: C and C++ header files and public API declarations.
     - **`.c`**: Pure C source implementations.
2. **Build a Per-File Symbol Index**:
   - List all public and internal classes, structs, functions, CUDA `__global__` and `__device__` kernels, host launch dispatchers, and PyBind11 exposed methods.

---

## Phase 2: Documentation Quality & Coverage Audit

Inspect each file using `view_file` and check for:
- Missing module-level, header-level, class-level, or function-level docstrings.
- Missing parameter explanations (`Args:` or `@param[in]`, `@param[out]`, `@param[in,out]`).
- Missing return type descriptions (`Returns:` or `@return`).
- Undocumented GPU kernel requirements (e.g. expected tensor shape, contiguous memory layout, device type, thread block configuration, shared memory bytes).
- Non-standard formatting (e.g. reStructuredText or Sphinx styles where Google Style is required for Python, or plain C-comments where Doxygen is required for C++/CUDA).

---

## Phase 3: Standardized Multi-Language Docstring Authoring

### 1. Python Docstrings (`.py`) — Google Python Style Guide Standard

All Python files (`.py`, `.pyi`) must strictly adhere to the **Google Python Style Guide**.

#### Key Rules:
- **Module-Level Docstrings**: Begin at the top of every module explaining the module's overall responsibility, domain purpose, public exports, and optional usage examples.
- **Function & Method Docstrings**:
  - Start with a concise single-line summary ending with a period.
  - Leave a blank line before the detailed explanation.
  - **`Args:`**: Document every parameter with `name (type): description`. Mention shapes, dtypes, default values, and coordinate conventions (e.g., `(N, 3)` float32 tensor in normalized $[-1, 1]$ bounds). Do not include `self` or `cls`.
  - **`Returns:`**: Specify `type: description`. For tuples or complex dicts, break down each returned element clearly.
  - **`Yields:`**: Used for generators instead of `Returns:`.
  - **`Raises:`**: List all exceptions explicitly thrown with conditions.
  - **`Example:` / `Examples:`**: Provide doctest-style or snippet examples illustrating typical usage.
- **Class Docstrings**:
  - Provide a class overview.
  - **`Attributes:`**: Document public class attributes with types and descriptions.
  - Document `__init__` consistently.
  - Document properties on their getter methods.

#### Python Google Style Template:
```python
"""Module-level overview describing the geometric algorithm or utility.

Detailed explanation of mathematical foundations, coordinate frames, 
and integration with other modules in the library.

Example:
    Examples can be given using the ``Example`` or ``Examples`` sections::

        from conquer3d.ops import dmc
        verts, faces = dmc(grid_vertices, voxels, sdf)
"""

def function_with_types(
    param1: torch.Tensor,
    param2: float = 0.0,
    *args,
    **kwargs
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Short summary line of what the function accomplishes.

    Extended description detailing the mathematical formulation, 
    level-set projection, or spatial traversal algorithm.

    Args:
        param1 (torch.Tensor): Coordinates tensor of shape `(N, 3)` with dtype 
            `torch.float32` on CUDA device. Must be contiguous.
        param2 (float, optional): Isolevel threshold for surface extraction. 
            Defaults to 0.0.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        Tuple[torch.Tensor, torch.Tensor]:
            - vertices (torch.Tensor): Extracted mesh vertices of shape `(V, 3)`.
            - faces (torch.Tensor): Mesh faces of shape `(F, 3)` for triangles 
              or `(Q, 4)` for pure quads.

    Raises:
        ValueError: If `param1` is not on a CUDA device or is not contiguous.
        RuntimeError: If the GPU kernel fails during execution.

    Example:
        >>> import torch
        >>> from conquer3d.ops import dual_marching_cubes
        >>> verts, faces = dual_marching_cubes(grid_vertices, voxels, sdf)
    """
    pass
```

---

### 2. C / C++ Header & Source Docstrings (`.c`, `.h`, `.cpp`, `.hpp`) — Doxygen Standard

All native C (`.c`, `.h`) and C++ (`.cpp`, `.hpp`, `.h`) files must adhere to the **Doxygen / Javadoc Standard**.

#### Key Rules:
- Use block formatting `/** ... */` above structs, classes, functions, and macros.
- **`@brief`**: Single-sentence summary of the function, class, or struct.
- **`@details`**: In-depth description of the algorithm, mathematical derivation, or coordinate frame conventions.
- **`@tparam`**: Description of template parameters.
- **`@param[in]`**: Explicitly mark read-only input pointers, references, and values with shape and memory expectations.
- **`@param[out]`**: Explicitly mark output pointers or buffers written by the function.
- **`@param[in,out]`**: Explicitly mark in-place mutated buffers.
- **`@return`**: Return value type and semantics.
- **`@note`**: Memory alignment, contiguous layout requirements, or assertion preconditions.

#### C / C++ Doxygen Template:
```cpp
/**
 * @file triangle_mesh.h
 * @brief Half-edge discrete differential geometry and topological analysis for triangle meshes.
 */

/**
 * @brief Evaluates the cotangent Laplace-Beltrami operator at all mesh vertices.
 * 
 * @details Uses Mayer (2003) discrete cotangent weights $\frac{1}{2}(\cot \alpha + \cot \beta)$
 * normalized by mixed Voronoi cell areas.
 * 
 * @param[in]  vertices  Tensor of shape (N, 3) containing float32 vertex coordinates.
 * @param[in]  triangles Tensor of shape (F, 3) containing int32 triangle vertex indices.
 * @param[out] out_lb    Tensor of shape (N, 3) containing computed Laplace-Beltrami vectors.
 * 
 * @return void
 * @note Requires 2-manifold triangle mesh topology without degenerate zero-area faces.
 */
void compute_laplace_beltrami_cotangent(
    const at::Tensor &vertices,
    const at::Tensor &triangles,
    at::Tensor &out_lb
);
```

---

### 3. CUDA Device & Implementation Docstrings (`.cu`, `.cuh`) — Doxygen GPU Standard

All CUDA source files (`.cu`) and CUDA device headers (`.cuh`) must document **hardware execution models, parallelization strategies, and numerical invariants**.

#### Key Rules:
- Document every `__global__` kernel and `__device__` helper function.
- **`@brief`**: Single-sentence purpose of the kernel or device helper.
- **`@details`**: Parallel decomposition strategy (e.g. 1 thread per voxel, 1 warp per primitive), memory access coalescing, or numerical formulation.
- **`@param[in]` / `@param[out]` / `@param[in,out]`**: Explicit pointer types, array sizes, and device global/shared/constant memory space.
- **`@note`**: Launch bounds, grid/block dimension assumptions (e.g., `blockDim.x == 256`, 1D vs 3D grids), dynamic shared memory requirements (`extern __shared__`), and stream associations.
- **`@warning`**: Warp divergence hazards, atomic contention points, register pressure constraints, and numerical $\epsilon$-guards (e.g., division by zero avoidance).

#### CUDA `.cu` / `.cuh` Doxygen Template:
```cpp
/**
 * @file dual_contouring.cu
 * @brief CUDA kernel implementations for GPU-accelerated Dual Contouring.
 */

/**
 * @brief Parallel evaluation of Quadratic Error Function (QEF) and dual vertex positioning.
 * 
 * @details Solves for the optimal cell feature point $v^*$ minimizing $\sum (n_i \cdot (v - p_i))^2$
 * using register-level cyclic Jacobi SVD diagonalization on a 3x3 symmetric matrix.
 * 
 * @param[in]  num_voxels    Total number of active voxel cells in the grid.
 * @param[in]  grid_vertices Pointer to (N, 3) float32 coordinates in device global memory.
 * @param[in]  voxels        Pointer to (M, 8) int32 corner indices per voxel cell.
 * @param[in]  sdf           Pointer to (N,) float32 scalar SDF values on grid vertices.
 * @param[out] out_vertices  Output device buffer for extracted (V, 3) dual vertex coordinates.
 * 
 * @note Launch configuration: 1D grid with 256 threads per block (`threads = 256`).
 * @warning Operates entirely within thread register space; do not increase `MAX_JACOBI_SWEEPS` beyond 6 to prevent register spilling to local memory.
 */
__global__ void dual_contouring_qef_kernel(
    const uint32_t num_voxels,
    const float3 *__restrict__ grid_vertices,
    const uint32_t *__restrict__ voxels,
    const float *__restrict__ sdf,
    float3 *__restrict__ out_vertices
);
```

---

### 4. PyBind11 C++ Bindings (`.cpp`) — Rich Docstring Standard

PyBind11 binding files (`csrc/binds/**/*.cpp` and `csrc/pybind.cpp`) must include rich Python docstrings embedded directly inside binding definitions using `R"pbdoc(...)pbdoc"`.

#### Key Rules:
- Set `m.doc() = "..."` at the top of binding modules.
- Provide raw string docstrings `R"pbdoc(...)pbdoc"` for all `.def(...)` and `.def_static(...)` calls.
- Specify argument names and defaults using `py::arg("name") = default`.
- Document expected tensor shapes, dtypes, and return values matching Python Google Style.

#### PyBind11 Template:
```cpp
m.def(
    "dual_marching_cubes",
    &conquer3d::ops::dual_marching_cubes,
    R"pbdoc(
    Forward pass of Differentiable Dual Marching Cubes (DMC).

    Args:
        grid_vertices (torch.Tensor): (N, 3) float32 corner coordinates on CUDA.
        voxels (torch.Tensor): (M, 8) int32 corner indices.
        sdf (torch.Tensor): (N,) float32 scalar SDF field.
        colors (torch.Tensor, optional): (N, C) float32 color features. Defaults to None.
        iso (float, optional): Isosurface threshold. Defaults to 0.0.
        quad_split (bool, optional): Split into Delaunay triangles. Defaults to True.
        project_iters (int, optional): Newton-Raphson iterations. Defaults to 5.

    Returns:
        Tuple[torch.Tensor, torch.Tensor, Optional[torch.Tensor]]: 
            (extracted_vertices, extracted_faces, extracted_colors)
    )pbdoc",
    py::arg("grid_vertices"),
    py::arg("voxels"),
    py::arg("sdf"),
    py::arg("colors") = py::none(),
    py::arg("iso") = 0.0f,
    py::arg("quad_split") = true,
    py::arg("project_iters") = 5
);
```

---

## Phase 4: Zero-Regression & Build Verification

After adding or updating docstrings:
1. **Preserve Code Logic**: DO NOT modify function implementations, return signatures, variable names, or algorithmic logic.
2. **Preserve Comments & Licenses**: Preserve existing copyright headers, license notices, and author annotations.
3. **Syntax & Stub Check**:
   - Verify Python syntax via Python compilation/linting tools: `python -m py_compile $(find conquer3d -name "*.py")`.
   - If rebuilding C++ extensions, verify `CustomBuildExt` runs and generates updated `_C.pyi` stubs.
