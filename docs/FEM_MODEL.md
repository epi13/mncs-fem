# FEM model and ownership boundary

## What FEM owns

Finite-element semantics, and only those:

- **Nodes** — `Node1 { id: u64, x: f64 }`. Identity is the `id`.
  Coordinate equality never determines identity: two nodes may share
  `x`, one node joins many elements.
- **Elements** — `BarElement { id: u64, n0: u64, n1: u64 }`.
  Connectivity names global node identities. A local position (0/1)
  is not a global identity; the scatter kernels translate explicitly.
- **Mesh/topology** — fixed-size connectivity arrays plus
  `check_element`/`mesh_ok` validation. Dynamic meshes are out of
  scope until the language supports them (F-004 context).
- **Shape functions** — reference-element interpolation with exact
  algebraic properties (partition of unity, Kronecker, symmetry).
- **Element physics** — `bar_ke`, consistent loads. The formula is
  FEM-owned; the arithmetic is Numeric-owned.
- **Assembly** — explicit local-to-global scatter with additive
  accumulation, deterministic under insertion order.
- **Constraints** — `Dirichlet` sets retained as data; reduction
  keeps the fixed-column coupling (`ff = f - k*u0`), reactions
  recovered as `R = K u - F`.
- **Results** — `Cantilever(Value { u_tip, reaction, k_axial })` and
  structured `BadInput`/`Singular` outcomes. Degenerate models
  (zero length, bad material, unconstrained modes) are data, never
  NaN and never bare "solver failed".

## What FEM does not own

- **Numeric** (`mncs-numerics`): f64 representation, conversions,
  `approx` tolerance policy, sqrt. Consumed, never re-implemented.
- **Math** (`mncs-math`): generic matrices, exact integer/rational
  solvers, sparse i64 kernels. The 1D slice needs nothing beyond
  Numeric; future 2D work should consume Math dense kernels where
  they fit rather than duplicate them.
- **Geometry** (`mncs-geometry`): point/vector/transform semantics.
  The 1D slice carries its own scalar coordinate (a 1D point needs
  no 2D primitive); 2D+ elements must consume Geometry, not wrap it.
- **Data** (`mncs-data`): no mesh serialization or model storage in
  FEM. Persisted evidence lives in the canonical Store path, not in
  FEM formats.
- **Solvers**: generic f64 linear-system solving belongs in Math
  (or a canonical numerical component), not in FEM. `solveref1d`
  is an explicitly marked reference bridge, not a solver home.

## Deliberately out of scope

Material-model frameworks, every PDE, nonlinear mechanics, CFD,
multiphysics, contact, optimization, shells/solids, parallel
assembly, CUDA kernels. The architecture layers reserve space for
them (`docs/ARCHITECTURE.md`); the foundation slice proves the
semantic structure first.

## Historical note

The repository bootstrapped with architecture docs only (no host FEM
code, no prior consumers anywhere in the family). There was no legacy
implementation to port or remove: the foundation above is the first
and only canonical implementation, built directly against the current
language and the modernized Numeric/Test libraries.
