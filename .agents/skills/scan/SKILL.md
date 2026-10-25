---
name: scan
description: Use this skill when the user wants an exhaustive, deep-dive architectural and technical audit of any codebase, thoroughly reading core implementation files (.cu, .cpp, .py, etc.) to understand its architecture, philosophy, style, and active developments, or uses /scan or [SCAN].
---

# Exhaustive Codebase Deep Scan Workflow

When this skill is activated (or the user uses `/scan` or `[SCAN]`), perform an exhaustive, multi-layered architectural and technical audit of the current working repository. 

Do not settle for high-level directory listings. You MUST systematically discover and actively read the core source files (native backends, acceleration structures, algorithms, data structures, and APIs) using `view_file` and `grep_search`.

---

## 1. Universal Discovery & Architecture Mapping
1. **Repository Layout & Topology**:
   - Use `list_dir` to explore the project structure, sub-packages, modules, and directories.
   - Detect project type, tech stack, and build system (e.g., `setup.py`, `pyproject.toml`, `CMakeLists.txt`, `Cargo.toml`, `package.json`, `Makefile`, etc.).
2. **Dynamic Core File Identification**:
   - Locate and categorize primary implementation files across all layers:
     - **Native & GPU Backends**: `.cu`, `.cuh`, `.cpp`, `.cc`, `.c`, `.h`, `.hpp`, `.rs`
     - **High-Level APIs & Algorithms**: `.py`, `.ts`, `.js`, `.go`, etc.
     - **Build, Config & Bindings**: Extension bindings (e.g. PyBind11, CFFI, FFI), compiler configurations, environment manifests.

---

## 2. Mandatory Deep File Reading (via `view_file`)
Select and deeply inspect the most important core source files in the repository across these technical dimensions:

### A. Core Architecture & Design Philosophy
- **Domain Purpose**: What core problem does this repository solve?
- **Design Principles**: Identify foundational design patterns (e.g., zero-copy memory pipelines, modular abstraction layers, immutable data flows, lock-free concurrency, specialized cache hierarchies).
- **Abstractions & Interfaces**: How do high-level interfaces communicate with low-level compute kernels or backends?

### B. Computational & Algorithmic Mechanics
- **Algorithmic Strategies**: Inspect the exact mathematical, geometric, or algorithmic logic in core files.
- **Data Structures**: Analyze spatial hierarchies, graph representations, tree structures, tensor arrangements, or hash tables.
- **Hardware & Concurrency Patterns**: Inspect parallelism models (e.g., GPU thread/block configurations, warp primitives, lock-free atomics, SIMD vectorization, multi-threading, asynchronous task scheduling).
- **Memory Layout & Efficiency**: Identify memory management strategies (e.g., compact bitmasks, packed representations, cache-aligned buffers, zero-copy pointer passing).

### C. Coding Conventions & Quality Standards
- **Style & Idioms**: Note naming conventions, error handling paradigms, typing discipline, assertion checks, and formatting standards.
- **Extension & Integration Patterns**: How are native extensions compiled, linked, exposed, and tested?

---

## 3. Git Context & Active Developments
- Scan recent commit history and uncommitted changes (`git status`, `git log -n 10 --oneline`, `git diff`) to understand:
  - Recent feature developments and major refactors.
  - Active work in progress, open challenges, or experimental modules.

---

## 4. Comprehensive Audit Report Structure
Synthesize all findings into a structured, insightful technical audit report:

1. **Executive Summary & Repository Mission**: High-level purpose, primary domain, and guiding architectural philosophy.
2. **Directory & Module Architecture Map**: Annotated breakdown of key directories and their responsibilities.
3. **Deep Technical Breakdown of Core Modules**: File-by-file analysis of the primary implementation files read during the scan.
4. **Key Data Structures & Algorithmic Pipelines**: Detailed explanation of the central algorithms, data structures, and acceleration techniques.
5. **Memory, Concurrency & Performance Engineering**: Hardware utilization, concurrency mechanisms, memory footprint optimizations, and efficiency trade-offs.
6. **Codebase Style & Conventions**: Established patterns, error handling, typing, and development practices.
7. **Active Development & Work in Progress**: Recent evolution of the codebase, recent commits, and active focus areas.
