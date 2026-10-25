/**
 * @file pybind_ext.cu
 * @brief PyTorch C++ CUDA extension bindings for gDel3D GPU 3D Delaunay Tetrahedralization.
 */

#include <torch/extension.h>
#include <vector>
#include <cstring>
#include "GpuDelaunay.h"

/**
 * @brief Computes 3D Delaunay tetrahedralization for a set of 3D points.
 * 
 * @details Converts input PyTorch tensor coordinates into gDel3D point structures,
 * dispatches the parallel GPU Delaunay point insertion and flipping engine,
 * and filters out infinite bounding vertices and inactive (dead) tetrahedra.
 * 
 * @param[in] points Tensor of shape (N, 3) with float32 or float64 dtype.
 * @return torch::Tensor Output tensor of shape (M, 4) with int64 dtype containing valid tetrahedra indices.
 */
torch::Tensor tetrahedralize_cuda(const torch::Tensor& points) {
    TORCH_CHECK(points.dim() == 2 && points.size(1) == 3, "points must be an N x 3 tensor");
    TORCH_CHECK(points.size(0) >= 4, "Need at least 4 points for tetrahedralization");
    
    torch::Tensor points_contig = points.is_cuda() ? points.contiguous().cpu() : points.contiguous();
    int num_points = points_contig.size(0);
    
    Point3HVec pointVec;
    pointVec.resize(num_points);
    
    if (points_contig.dtype() == torch::kFloat32) {
        const float* pts_ptr = points_contig.data_ptr<float>();
        for (int i = 0; i < num_points; ++i) {
            pointVec[i]._p[0] = static_cast<RealType>(pts_ptr[i * 3 + 0]);
            pointVec[i]._p[1] = static_cast<RealType>(pts_ptr[i * 3 + 1]);
            pointVec[i]._p[2] = static_cast<RealType>(pts_ptr[i * 3 + 2]);
        }
    } else if (points_contig.dtype() == torch::kFloat64) {
        const double* pts_ptr = points_contig.data_ptr<double>();
        for (int i = 0; i < num_points; ++i) {
            pointVec[i]._p[0] = static_cast<RealType>(pts_ptr[i * 3 + 0]);
            pointVec[i]._p[1] = static_cast<RealType>(pts_ptr[i * 3 + 1]);
            pointVec[i]._p[2] = static_cast<RealType>(pts_ptr[i * 3 + 2]);
        }
    } else {
        TORCH_CHECK(false, "points must be float32 or float64");
    }
    
    std::vector<int64_t> valid_tets;
    {
        GDelOutput output;
        GDelParams params;
        GpuDel gpuDel(params);
        gpuDel.compute(pointVec, &output);
        
        int num_raw_tets = output.tetVec.size();
        for (int i = 0; i < num_raw_tets; ++i) {
            const Tet& tet = output.tetVec[i];
            if (isTetAlive(output.tetInfoVec[i]) &&
                tet._v[0] < num_points && tet._v[1] < num_points && 
                tet._v[2] < num_points && tet._v[3] < num_points) {
                valid_tets.push_back(static_cast<int64_t>(tet._v[0]));
                valid_tets.push_back(static_cast<int64_t>(tet._v[1]));
                valid_tets.push_back(static_cast<int64_t>(tet._v[2]));
                valid_tets.push_back(static_cast<int64_t>(tet._v[3]));
            }
        }
    }
    
    int num_tets = valid_tets.size() / 4;
    torch::Tensor result = torch::empty({num_tets, 4}, torch::dtype(torch::kInt64).device(torch::kCPU));
    if (num_tets > 0) {
        std::memcpy(result.data_ptr<int64_t>(), valid_tets.data(), valid_tets.size() * sizeof(int64_t));
    }
    return result.to(points.device());
}

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    m.doc() = "PyTorch CUDA extension bindings for gDel3D GPU 3D Delaunay Tetrahedralization.";

    m.def(
        "tetrahedralize_cuda",
        &tetrahedralize_cuda,
        R"pbdoc(
        Compute exact 3D Delaunay tetrahedralization on GPU using gDel3D.

        Given a 2D tensor of 3D point coordinates, computes the 3D Delaunay 
        tetrahedralization using GPU-accelerated point insertion, bistellar 
        flipping, and host CPU star splaying post-processing for topological 
        degeneracies.

        Args:
            points (torch.Tensor): Coordinates tensor of shape `(N, 3)` with 
                dtype `torch.float32` or `torch.float64` on CPU or CUDA device. 
                Must contain at least 4 non-coplanar points.

        Returns:
            torch.Tensor: Tetrahedra vertex indices tensor of shape `(M, 4)` 
                with dtype `torch.int64` on the same device as input points. 
                Each row `[v0, v1, v2, v3]` represents a valid Delaunay 3D 
                tetrahedron indexing into the input `points` tensor.

        Raises:
            ValueError: If `points` is not a 2D tensor of shape `(N, 3)` or 
                has fewer than 4 points, or has unsupported dtype.

        Example:
            >>> import torch
            >>> import gdel3d_cuda
            >>> pts = torch.rand(1000, 3, dtype=torch.float64, device='cuda') * 10.0
            >>> tets = gdel3d_cuda.tetrahedralize_cuda(pts)
            >>> print(tets.shape)  # torch.Size([M, 4])
        )pbdoc",
        py::arg("points")
    );
}
