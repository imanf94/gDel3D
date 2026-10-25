import os
import sys
from setuptools import setup, find_packages
import torch.utils.cpp_extension
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

src_dir = "GDelFlipping/src/gDel3D"

sources = [
    "bindings/pybind_ext.cu",
    f"{src_dir}/GpuDelaunay.cu",
    f"{src_dir}/CPU/predicates.cu",
    f"{src_dir}/CPU/PredWrapper.cu",
    f"{src_dir}/CPU/Splaying.cu",
    f"{src_dir}/CPU/Star.cu",
    f"{src_dir}/GPU/KerDivision.cu",
    f"{src_dir}/GPU/KerPredicates.cu",
    f"{src_dir}/GPU/ThrustWrapper.cu",
]

# Sanitize TORCH_CUDA_ARCH_LIST to strip unsupported/invalid archs like '10.1'
arch_list_env = os.environ.get("TORCH_CUDA_ARCH_LIST", "")
if arch_list_env:
    cleaned_archs = [a.strip() for a in arch_list_env.split(";") if a.strip() and a.strip() != "10.1"]
    if cleaned_archs:
        os.environ["TORCH_CUDA_ARCH_LIST"] = ";".join(cleaned_archs)
    else:
        os.environ["TORCH_CUDA_ARCH_LIST"] = "12.0"

conda_prefix = os.environ.get("CONDA_PREFIX", sys.prefix)
conda_gcc = os.path.join(conda_prefix, "bin", "x86_64-conda-linux-gnu-gcc")

nvcc_args = [
    "-O3",
    "-DNDEBUG",
    "-allow-unsupported-compiler",
    "-w",
    "-D__CUDA_NO_HALF_OPERATORS__",
    "-D__CUDA_NO_HALF_CONVERSIONS__",
    "-D__CUDA_NO_BFLOAT16_CONVERSIONS__",
    "-D__CUDA_NO_HALF2_OPERATORS__",
    "--expt-relaxed-constexpr",
    "-std=c++17",
    "-DTHRUST_DISABLE_ABI_NAMESPACE",
    "-DTHRUST_IGNORE_ABI_NAMESPACE_ERROR",
]
if os.path.exists(conda_gcc):
    nvcc_args.extend(["-ccbin", conda_gcc])

# Auto-detect Blackwell architecture (compute capability 12.0)
import torch
if torch.cuda.is_available():
    cap = torch.cuda.get_device_capability(0)
    if cap == (12, 0):
        nvcc_args.append("-gencode=arch=compute_120,code=sm_120")

cxx_args = [
    "-O3",
    "-DNDEBUG",
    "-std=c++17",
    "-DTHRUST_DISABLE_ABI_NAMESPACE",
    "-DTHRUST_IGNORE_ABI_NAMESPACE_ERROR",
]

cuda_include_dirs = torch.utils.cpp_extension.include_paths(device_type="cuda")
additional_includes = [
    os.path.abspath("GDelFlipping/src/gDel3D"),
    os.path.abspath("GDelFlipping/src/gDel3D/CPU"),
    os.path.abspath("GDelFlipping/src/gDel3D/GPU"),
    os.path.join(conda_prefix, "targets", "x86_64-linux", "include"),
    os.path.join(conda_prefix, "include"),
    os.path.join(conda_prefix, "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages", "nvidia", "cuda_runtime", "include"),
]
additional_includes = [p for p in additional_includes if os.path.exists(p)]
all_includes = list(set(cuda_include_dirs + additional_includes))

setup(
    name="gdel3d_cuda",
    version="0.2.0",
    description="Python binding for gDel3D GPU 3D Delaunay Tetrahedralization",
    author="KhoiDOO & Antigravity",
    packages=find_packages(),
    ext_modules=[
        CUDAExtension(
            name="gdel3d_cuda",
            sources=sources,
            include_dirs=all_includes,
            extra_compile_args={
                "cxx": cxx_args,
                "nvcc": nvcc_args,
            },
        )
    ],
    cmdclass={
        "build_ext": BuildExtension
    },
)
