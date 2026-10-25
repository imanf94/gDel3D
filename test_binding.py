import torch
import numpy as np
import scipy.spatial
import time
import sys

try:
    import gdel3d_cuda
except Exception as e:
    print(f"ERROR: gdel3d_cuda failed to import: {e}")
    sys.exit(1)

def test_delaunay(num_points=1000, seed=42):
    print(f"\n--- Testing 3D Delaunay on {num_points} points (seed={seed}) ---")
    np.random.seed(seed)
    torch.manual_seed(seed)
    
    # Generate random points in 3D sphere/box
    points_np = np.random.rand(num_points, 3).astype(np.float64) * 10.0
    points_tensor = torch.from_numpy(points_np).cuda()
    
    # 1. Run CUDA gDel3D
    torch.cuda.synchronize()
    t0 = time.time()
    tets_cuda = gdel3d_cuda.tetrahedralize_cuda(points_tensor)
    torch.cuda.synchronize()
    t_cuda = time.time() - t0
    
    tets_cuda_np = tets_cuda.cpu().numpy()
    print(f"[CUDA] Generated {len(tets_cuda_np)} tetrahedra in {t_cuda*1000:.2f} ms")
    
    # 2. Run SciPy CPU
    t0 = time.time()
    delaunay_scipy = scipy.spatial.Delaunay(points_np)
    t_scipy = time.time() - t0
    tets_scipy = delaunay_scipy.simplices
    print(f"[SciPy] Generated {len(tets_scipy)} tetrahedra in {t_scipy*1000:.2f} ms")
    
    # 3. Verify exact match
    if len(tets_cuda_np) != len(tets_scipy):
        print(f"WARNING: Tetrahedra count mismatch! CUDA: {len(tets_cuda_np)} vs SciPy: {len(tets_scipy)}")
        return False
        
    # Sort vertex indices internally for each tetrahedra
    sorted_cuda = np.sort(tets_cuda_np, axis=1)
    sorted_scipy = np.sort(tets_scipy, axis=1)
    
    # Sort tetrahedra rows lexicographically to align order
    sorted_cuda = sorted_cuda[np.lexsort(sorted_cuda.T)]
    sorted_scipy = sorted_scipy[np.lexsort(sorted_scipy.T)]
    
    is_identical = np.array_equal(sorted_cuda, sorted_scipy)
    if is_identical:
        print("SUCCESS: CUDA results are 100% IDENTICAL to scipy.spatial.Delaunay!")
    else:
        diff_count = np.sum(np.any(sorted_cuda != sorted_scipy, axis=1))
        print(f"FAILURE: {diff_count} out of {len(tets_scipy)} tetrahedra differ between CUDA and SciPy!")
        
    return is_identical

if __name__ == "__main__":
    all_passed = True
    for N in [100, 500, 1000, 2000, 5000, 10000]:
        if not test_delaunay(num_points=N, seed=42):
            all_passed = False
            
    if all_passed:
        print("\n=== ALL DELAUNAY BENCHMARK TESTS PASSED SUCCESSFULLY! ===")
        sys.exit(0)
    else:
        print("\n=== SOME TESTS FAILED! ===")
        sys.exit(1)
