# mncs-fem

<!-- MNCS:generated:begin -->
## Project entry

Machine-native finite element analysis for MNCS: nodes, DOFs, mesh topology, elements, shape functions, assembly, constraints, and FEM result structures, expressed natively in mncs-language.

```bash
python3 scripts/run_tests.py
```

Declared capabilities (declarations do not establish execution health):

- `finite-elements/0.1` — mncs-library (experimental)

Semantic sources and ownership: `.mncs/projections.json`.
<!-- MNCS:generated:end -->

Machine-native finite element analysis for MNCS.

`mncs-fem` is the canonical FEM implementation: one architecture, no
`fem-v2`/`native-fem` forks, no frozen partial versions. It owns
**finite-element semantics** — nodes, DOFs, mesh topology, elements,
shape functions, materials interfaces, loads, constraints, assembly,
and FEM result structures — expressed natively in `mncs-language`
(Profile 0.18). It is also a deliberate language pressure project for
sparse linear algebra, connectivity ownership, generic numerics,
indexed gather/scatter, and scientific verification.

## Ownership boundary

| Concern | Owner | FEM relationship |
|---|---|---|
| Scalar representation, conversion, precision, `approx` discipline | `mncs-numerics` | Consumed (`scalar_float.approx`); never duplicated |
| Generic math: dense matrices, exact solvers, sparse i64 kernels | `mncs-math` | Consumed where applicable; FEM adds no private math |
| Points/vectors/transforms | `mncs-geometry` | Not a dependency of the 1D slice; 2D+ elements will consume it |
| Structured data / serialization | `mncs-data` | Not a dependency; no model storage in FEM |
| Test declarations, assertions, runner policy | `mncs-test` | Consumed via `mncs test`; no private harness |
| Generic f64 linear-system solving | **nobody yet (pressure F-001)** | FEM uses marked reference kernels only |
| Nodes, DOFs, elements, mesh, shapes, assembly, constraints, results | **`mncs-fem`** | Canonical home |

## Current capability (foundation slice)

1D linear axial-bar path, fully native except the final small-dense
solve (explicit reference boundary):

- `src/fem/mesh1d.mncs` — `Node1`/`BarElement` identity, connectivity
  validation (`ElemCheck`), absolute length, guarded uniform builder.
- `src/fem/shape1d.mncs` — reference-element shapes, derivatives,
  domain check, interpolation, partition residual.
- `src/fem/bar1d.mncs` — `BarMaterial`, validation, guarded
  `ke = (A*E/L)[[1,-1],[-1,1]]`, consistent uniform-load vector.
- `src/fem/assembly1d.mncs` — Nat-generic scatter/assembly/loads over
  `[[f64; N]; N]`, row-sum observer.
- `src/fem/constraints1d.mncs` — `Dirichlet` sets, membership/lookup,
  fix0 reduction (2- and 3-node), reaction recovery.
- `src/fem/solveref1d.mncs` — **REFERENCE (non-canonical)** 1x1/2x2
  Cramer solves with structured `Singular`; pending generic Math f64
  solver (F-001).
- `src/fem/model1d.mncs` — end-to-end fixed-free bar under tip load
  (1- and 2-element), displacement + reaction outcomes.

## Verification

49 native `mncs test` declarations across 7 suites
(`scripts/run_tests.py`), every value exact `==` on dyadic inputs with
explicit `approx` only where rounding genuinely occurs (L = 3,
interior xi = 0.3). Independent exact-rational oracle:
`tools/oracle_bar1d.py` (22 checks, Fraction-based, no shared code).
See `docs/VERIFICATION.md` and `evidence/fem-capabilities.json`.

## Solver boundary (read carefully)

`native FEM formulation/assembly → REFERENCE small-dense solve
(solveref1d, non-canonical) → native verification`. FEM is not claimed
MNCS-native end-to-end until F-001 (generic f64 solver) lands in Math.

## Adding a new element

1. Create `src/fem/<name>.mncs` (`module mncs.fem.<name>.v1`; the file
   path must mirror the module segments).
2. Validate all inputs into data outcomes (no traps for bad models).
3. Reuse `mesh1d` identity/connectivity and `assembly1d` scatter.
4. Add a native suite under `tests/native/` + runner entry, with
   known-answer, symmetry, rigid-body, and degenerate cases plus an
   oracle cross-check.

## Layout

- `src/fem/` — the library (`.mncs` only, no host semantics)
- `tests/native/` — in-language contracts via `mncs test`
- `scripts/run_tests.py` — canonical runner with revision-bound JSON evidence
- `tools/oracle_bar1d.py` — independent exact-arithmetic oracle
- `docs/ARCHITECTURE.md` — layers and milestones (standing plan)
- `docs/FEM_MODEL.md` — ownership boundary and canonical model
- `docs/VERIFICATION.md` — analytic/reference evidence
- `docs/LANGUAGE_PRESSURES.md` — pressure ledger with reproducers
- `docs/rfcs/0001-foundation.md` — foundation principles
- `evidence/fem-capabilities.json` — machine-readable capability record
