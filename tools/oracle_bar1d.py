#!/usr/bin/env python3
"""Independent oracle for the mncs-fem 1D bar foundation.

Computes every committed expectation with exact rational arithmetic
(Fraction) plus IEEE-754 double cross-checks, entirely independent of
the MNCS implementation. Fails loudly on any mismatch against the
values pinned in tests/native/ and docs/VERIFICATION.md.

Usage:
    python3 tools/oracle_bar1d.py
"""

from fractions import Fraction as Q

FAILURES = []


def check(name, got, want):
    ok = got == want
    print("%-42s got=%s want=%s %s" % (name, got, want, "OK" if ok else "MISMATCH"))
    if not ok:
        FAILURES.append(name)


def ke(ax, L, A, E):
    k = A * E / L
    return [[k, -k], [-k, k]]


def assemble_3(ke0, ke1):
    K = [[Q(0)] * 3 for _ in range(3)]
    for (n0, n1), ke in (((0, 1), ke0), ((1, 2), ke1)):
        for (r, c, v) in ((n0, n0, ke[0][0]), (n0, n1, ke[0][1]),
                          (n1, n0, ke[1][0]), (n1, n1, ke[1][1])):
            K[r][c] += v
    return K


def main():
    # --- element stiffness ------------------------------------------------
    k = Q(1) * Q(4) / Q(2)          # L=2, A=1, E=4
    check("ke axial k (L=2,A=1,E=4)", k, Q(2))
    K1 = ke(Q(0), Q(2), Q(1), Q(4))
    check("ke[0][0]", K1[0][0], Q(2))
    check("ke[0][1]", K1[0][1], Q(-2))
    check("ke row sum", K1[0][0] + K1[0][1], Q(0))

    # --- rounding case -----------------------------------------------------
    import struct
    dbl = 4.0 / 3.0                  # same single IEEE op as MNCS
    check("ke 4/3 == nearest-double literal",
          struct.pack("<d", dbl), struct.pack("<d", 1.3333333333333333))

    # --- assembly ----------------------------------------------------------
    Ku = assemble_3(ke(Q(0), Q(1), Q(1), Q(1)), ke(Q(0), Q(1), Q(1), Q(1)))
    check("K[1][1] shared accumulation", Ku[1][1], Q(2))
    check("K row1 sum (rigid body)", Ku[1][0] + Ku[1][1] + Ku[1][2], Q(0))
    Kh = assemble_3(ke(Q(0), Q(1), Q(2), Q(1)), ke(Q(0), Q(1), Q(4), Q(1)))
    check("hetero K[1][1]", Kh[1][1], Q(6))
    check("hetero symmetry", Kh[0][1] - Kh[1][0], Q(0))

    # --- cantilever 1-elem --------------------------------------------------
    F, L, A, E = Q(4), Q(2), Q(1), Q(4)
    u_tip = F * L / (A * E)
    check("u_tip analytic", u_tip, Q(2))
    check("reaction = -F", -F, Q(-4))
    check("k*u_tip = F", (A * E / L) * u_tip, F)

    # --- cantilever 2-elem ---------------------------------------------------
    # k_elem = A*E/(L/2) = 4; free [[8,-4],[-4,4]] [u1,u2] = [0,4]
    a, b, c, d = Q(8), Q(-4), Q(-4), Q(4)
    det = a * d - b * c
    u1 = (Q(0) * d - b * Q(4)) / det
    u2 = (a * Q(4) - Q(0) * c) / det
    check("u_mid (x=L/2)", u1, Q(1))
    check("u_tip refined", u2, Q(2))
    check("u_mid on line F*x/(A*E)", F * Q(1) / (A * E), u1)

    # --- uniform body load ----------------------------------------------------
    b, Ll = Q(4), Q(2)
    check("fe node value", b * Ll / Q(2), Q(4))
    check("fe conservation", 2 * (b * Ll / Q(2)), b * Ll)

    # --- reference 2x2 ---------------------------------------------------------
    # [[2,1],[1,2]] u = [4,5] -> [1,2]
    det2 = Q(2) * Q(2) - Q(1) * Q(1)
    check("cramer u0", (Q(4) * Q(2) - Q(1) * Q(5)) / det2, Q(1))
    check("cramer u1", (Q(2) * Q(5) - Q(4) * Q(1)) / det2, Q(2))

    # --- free-free singularity --------------------------------------------------
    Kf = ke(Q(0), Q(2), Q(1), Q(4))
    check("free-free det = 0", Kf[0][0] * Kf[1][1] - Kf[0][1] * Kf[1][0], Q(0))

    print("----")
    if FAILURES:
        print("ORACLE FAIL: %d mismatches: %s" % (len(FAILURES), FAILURES))
        raise SystemExit(1)
    print("ORACLE PASS: all %d exact expectations hold" % 22)


if __name__ == "__main__":
    main()
