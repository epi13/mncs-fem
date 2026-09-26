# Scientific verification

All expectations below are pinned by native `mncs test` suites
(`scripts/run_tests.py`, 49 declarations, 7/7 suites PASS) and
cross-checked by the independent exact-rational oracle
(`tools/oracle_bar1d.py`, 22/22 checks, `Fraction`-based, zero shared
code with the MNCS implementation). Dyadic cases assert exact `==`;
`approx` appears only where IEEE rounding genuinely occurs.

## Element-level known answers

- `ke` for L=2, A=1, E=4 is exactly `[2,-2,-2,2]` (oracle: exact).
- `ke` for L=3, A=1, E=4 is `4/3` correctly rounded once
  (bit-identical to the nearest-double literal; test uses tight
  `approx`, oracle confirms the bits).
- Uniform body load b=4 over L=2 gives `fe = [4,4]` with exact
  conservation `fe0 + fe1 == b*L`.

## Structural properties

- **Symmetry**: `ke01 == ke10`; preserved through heterogeneous
  assembly (k=2 + k=4 elements).
- **Rigid-body freedom**: element and assembled row sums are exactly
  zero; `ke * [1,1] == [0,0]`.
- **Partition of unity**: `N0 + N1 - 1 == 0` at dyadic xi; explicit
  tolerance only at xi = 0.3.
- **Kronecker/interpolation**: nodal recovery exact; midpoint of
  (3, 7) is exactly 5.
- **Symmetry**: `N0(xi) == N1(-xi)`; derivatives `∓1/2` sum to zero.

## Assembly properties

- Shared-node accumulation: series unit elements give
  `K[1][1] == 2`; hetero (2, 4) gives `6`.
- Insertion-order independence pinned (forward vs reversed).
- Zero-ke scatter is additive identity (no overwrite).
- Load scatter accumulates at shared nodes beside point loads.

## Constraints and equilibrium

- `is_constrained`/`prescribed_or` hit exactly the named DOFs.
- fix0 reduction carries the fixed column: settlement u0=1 shifts
  `ff` from 4 to 6 (constraints are loads, not deletions).
- Reactions: R0 = -4 under tip load 4; `R + F == 0` exactly, 2- and
  3-node.

## Analytical solutions (the vertical slice)

Fixed-free bar, F=4, L=2, A=1, E=4:

| Quantity | Closed form | Model output |
|---|---|---|
| u_tip (1 elem) | F·L/(A·E) = 2 | 2.0 exact |
| reaction | −F = −4 | −4.0 exact |
| u_tip (2 elem) | 2 | 2.0 exact |
| u_mid (2 elem) | F·(L/2)/(A·E) = 1 | 1.0 exact |

The analytic comparator `F*L/(A*E)` is spelled independently inside
each test, never shared code with the model.

## Refinement behavior

Linear elements reproduce the linear field exactly, so 1→2 element
refinement leaves the tip unchanged and lands the midpoint on the
analytic line. This is the correct linear-exactness expectation — not
a convergence-rate claim. True mesh-convergence studies (with
nonlinear fields or higher-order elements) are future work once the
element family grows.

## Degenerate / singular models (all structured, none trapping)

Zero/negative length → `BadLength`/`BadInput`; non-positive area or
modulus → `BadMaterial`/`BadInput`; out-of-range connectivity →
`NodeOutOfRange`; self-connected → `SelfConnected`; bad builder
indices → `BadIndex`; free-free stiffness → `Singular` (unconstrained
rigid-body mode preserved with FEM meaning for Debug).

## Floating-point discipline

Exact `==` where binary64 algebra on the chosen inputs is exact
(dyadic values, correctly-rounded single ops); `approx(abs, rel)`
with stated tolerances only for the two genuinely rounding cases.
No universal epsilon anywhere.

## What is NOT claimed

No patch test beyond the linear bar (the linear field is reproduced
exactly, which subsumes the 1D patch test trivially); no convergence
rates; no 2D/3D, dynamics, or nonlinear verification. The evidence
record (`evidence/fem-capabilities.json`) states exactly this.
