# mncs-fem

Machine-native finite element analysis for MNCS.

`mncs-fem` is a reusable scientific FEA and future multiphysics framework, and a deliberate `mncs-language` pressure project for sparse linear algebra, meshes and topology, element assembly, material models, solver semantics, parallel execution and scientific verification.

## Initial scope

- meshes, elements, topology and geometry
- fields, degrees of freedom and constraints
- element formulations, quadrature and material models
- global matrix/vector assembly
- sparse systems and iterative/direct solver interfaces
- linear structural mechanics as the first validated domain
- convergence studies, patch tests and reference problems
- CPU/GPU execution with explicit numerical contracts

## Repository layout

- `docs/ARCHITECTURE.md`
- `docs/rfcs/0001-foundation.md`
- `docs/LANGUAGE_PRESSURES.md`
- `AGENTS.md`
