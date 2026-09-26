# MNCS language pressure ledger

Record workload, observed behavior, required semantic, reproducer, owner, workaround and closure verification.

## Initial pressure targets

- sparse matrix and sparse-pattern abstractions
- compact graph/connectivity ownership
- efficient local fixed-size matrices/vectors
- compile-time element dimension/order parameters
- generic scalar/precision types without performance collapse
- indexed gather/scatter operations
- safe parallel sparse assembly
- deterministic reductions/accumulation modes
- SoA/AoS and alignment control
- iterative solver interfaces and structured convergence states
- CUDA-compatible element kernels and sparse operations
- compiler diagnostics for shape/index/type mismatches

No scientific pressure item is closed solely because a benchmark runs; it must satisfy its verification case.

## Campaign findings (2026-09-26, 1D bar foundation)

- **F-001 (BLOCKING for native end-to-end solve): missing generic f64
  linear solver.** `mncs.math.linalg` solves exact integer/rational
  systems only (Cramer/Bareiss, concrete shapes);
  `mncs.numerics.mat_float_build` constructs matvec/matmul but no
  factorization or solve. FEM needs `K u = f` over f64. Workaround:
  `src/fem/solveref1d.mncs` closed-form 1x1/2x2 Cramer, explicitly
  marked REFERENCE/non-canonical. Owner should be Math (or the
  canonical numerical component), not FEM. Reproducer: any `K u = f`
  over f64 has no canonical callee today.
- **F-002 (non-blocking): no array fill for symbolic bounds.**
  Kernels thread a `seed` exemplar supplying the result shape, fully
  overwritten lane by lane (same honest pattern as numerics P-003).
  Observed in `assembly1d` (`seed: [[f64; N]; N]`).
- **F-003 (non-blocking): `iterate x over arr` binds the index, not
  the element.** Projecting a record field on the loop variable fails
  (MNE161 "field projection requires a value of a declared record
  type"); canonical code spells `arr[e].field`. Minimal case:
  `iterate e over elems { next k = f(elems[e].n0, ...) }` elaborates
  while `e.n0` does not.
- **F-004 (non-blocking): sequence literal as a generic-fn argument
  needs a let-binding.** `scatter_elem(seed, 0, 1, [0.0, 0.0, 0.0,
  0.0])` fails (MNE183 "sequence literals require an exact or
  bounded-view sequence expected type"); binding
  `let zke: [f64; 4] = [...]` first elaborates. Pinned by the
  `zero_stiffness_scatter_is_identity` test shape.
- **F-005 (non-blocking): `as` binds tighter than `-`.**
  `(n - 1 as f64)` parses as `n - (1 as f64)` (MNE119 u64 vs f64);
  `((n - 1) as f64)` is required. Observed in `mesh1d.uniform_node_x`.
- **F-006 (non-blocking): module file path must mirror module
  segments, diagnosed only at the importer.** `src/fem/solve_ref1d.mncs`
  declaring `module mncs.fem.solveref1d.v1` surfaces as MNE173
  "imported module unavailable" on the importing file with no span
  pointing at the misnamed file. Renamed to `solveref1d.mncs`.
- **F-007 (non-blocking, architectural): no generic home for sparse
  f64 assembly.** `mncs.math.sparse` is i64-only, 4x4, cap-8 lanes;
  FEM uses dense storage for these bounded meshes and records the
  ownership question (Math vs Data vs dedicated numerics) rather than
  burying a solver-quality sparse system inside FEM.

Deferred (not yet pressure, decided): generic quadrature ownership —
the linear bar integrates exactly, so no quadrature is embedded; when
higher-order elements need it, its home (Math vs FEM-selected rule)
must be decided explicitly. Unit/dimension typing: distinctions
(length/area/modulus/force/displacement) are documented per function
but not type-enforced; no genuine need demonstrated yet at this
scale — not filed as pressure.
