
cmake_minimum_required(VERSION 3.18)

project(gflip3d LANGUAGES CXX CUDA)

set(CMAKE_BUILD_TYPE Debug) 

# Add the source files
set(SOURCES
GDelFlipping/src/DelaunayChecker.cpp
GDelFlipping/src/Demo.cpp
GDelFlipping/src/InputCreator.cpp
GDelFlipping/src/RandGen.cpp
GDelFlipping/src/gDel3D/GpuDelaunay.cu
GDelFlipping/src/gDel3D/CPU/predicates.cu
GDelFlipping/src/gDel3D/CPU/PredWrapper.cu
GDelFlipping/src/gDel3D/CPU/Splaying.cu
GDelFlipping/src/gDel3D/CPU/Star.cu
GDelFlipping/src/gDel3D/GPU/KerDivision.cu
GDelFlipping/src/gDel3D/GPU/KerPredicates.cu
GDelFlipping/src/gDel3D/GPU/ThrustWrapper.cu
)

# Add the executable
add_executable(${PROJECT_NAME} ${SOURCES})

# Set CUDA properties
set_target_properties(${PROJECT_NAME} PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON
    CUDA_ARCHITECTURES 60 70 80
)

# Include directories if needed
target_include_directories(${PROJECT_NAME} PRIVATE ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES})
