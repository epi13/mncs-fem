# Agent and contributor contract

- Prefer `mncs-language` for implementation.
- State mesh assumptions, element order, units, material law, boundary conditions, solver tolerance and precision explicitly.
- A solver returning a value is not evidence of correctness; use patch tests, analytic/manufactured solutions and convergence studies.
- Keep discretization, assembly and solver responsibilities distinct.
- Do not weaken tolerances or mesh-quality checks merely to obtain passing tests.
- Record language/compiler/runtime pressure in `docs/LANGUAGE_PRESSURES.md` with minimal reproducers where possible.
- CPU/GPU acceleration must preserve the declared scientific contract.
