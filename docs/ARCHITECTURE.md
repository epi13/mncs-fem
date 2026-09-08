# Architecture

## Layers

1. **Mesh/topology** — nodes, elements, connectivity, geometry and regions.
2. **Fields/DOFs** — field definitions, indexing, constraints and boundary conditions.
3. **Element physics** — shape functions, quadrature, constitutive/material models and local residual/stiffness kernels.
4. **Assembly** — sparse pattern construction, local-to-global mapping and global vectors/matrices.
5. **Solvers** — linear/nonlinear systems, preconditioners, convergence and failure evidence.
6. **Verification** — patch tests, analytic/manufactured cases, residual checks and mesh-convergence studies.
7. **Acceleration/adapters** — SIMD, threaded and CUDA paths plus integration with other scientific MNCS systems.

## First milestones

1. Mesh and DOF foundation.
2. Simple 1D/2D linear elements and quadrature.
3. Sparse assembly and boundary constraints.
4. Linear structural solve with reference cases.
5. Convergence/patch-test suite.
6. Parallel and CUDA pressure campaigns.
