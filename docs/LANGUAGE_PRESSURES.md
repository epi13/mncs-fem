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
