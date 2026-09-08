# RFC 0001: Finite-element foundation

Status: Draft

## Principles

- Discretization, units, element order and boundary conditions are explicit inputs to the scientific result.
- Constraint application has defined semantics and does not rely on hidden mutation.
- Solver results expose residuals, tolerances, convergence state and iteration evidence.
- Mesh refinement and convergence studies are first-class verification tools.
- Parallel assembly/reductions preserve the declared reproducibility mode.
- Physical acceleration may change layout and scheduling but not the mathematical contract.

## Pressure objectives

Sparse matrix/vector types, graph connectivity ownership, compile-time/local element shapes, generic scalar types, quadrature kernels, indexing safety, parallel assembly, deterministic reductions, memory-layout control, iterative solver abstractions, SIMD/CUDA kernels and structured convergence failures.
