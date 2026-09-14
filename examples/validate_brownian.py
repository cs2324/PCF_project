"""Validate PCF recovery by comparing with the known Brownian reference CFs.

Run from the project root: python -m examples.validate_brownian
All recovered moments come from cf_recovery. Reference CFs are used only
after recovery to check the answers. 
This script checks degrees 0,...,4.
"""

import sympy as sp
from cf_recovery import (
    BrownianPCF, MomentRecovery, SignatureCharacteristicFunction,
)


def check_target(name, terms, reference_cf, Phi_X, lam, R=4):
    """Print and check each recovered moment and the finite CF polynomial.
    

    Parameters
    ----------
    name:  a string for the target, e.g. "S_12" or "A=(S_12-S_21)/2".
    terms:  a list of (coefficient, word) pairs for the target.
    reference_cf:  a SymPy expression for a known scalar characteristic
    function, obtained independently of the PCF recovery algorithm.

    Since phi^(m)(0)=i^m E[Z^m], divide its derivative by i^m, not m!.
    Raise AssertionError with the target/order if an exact check fails.
    """
    target = SignatureCharacteristicFunction(Phi_X, terms)
    polynomial, moments = target.R_truncation(lam, R)
    reference_series = sp.series(reference_cf, lam, 0, R + 1).removeO().expand()
    print(f"\n{name}")
    print("m | recovered moment | reference moment | check")
    for m, recovered in enumerate(moments):
        expected = sp.simplify(
            reference_series.coeff(lam, m) * sp.factorial(m) / sp.I**m
        )
        if sp.simplify(recovered - expected) != 0:
            raise AssertionError(f"{name}, m={m}: {recovered} != {expected}")
        print(f"{m} | {recovered} | {expected} | PASS")
    if sp.simplify(polynomial - reference_series) != 0:
        raise AssertionError(f"{name}: Taylor polynomial mismatch")
    print("P_R(lambda) =", polynomial)
    print("Polynomial comparison: PASS")
    return polynomial, moments


def main():
    """Check S_12, full area L and half area A at symbolic time T."""
    T = sp.Symbol("T", nonnegative=True)
    lam = sp.Symbol("lambda", real=True)
    Phi_X = BrownianPCF(path_dim=2, T=T)
    recovery = MomentRecovery(Phi_X)

    # This cross moment tests the mixed-word part before the combination.
    cross = recovery.mixed_moment([(1, 2), (2, 1)])
    if sp.simplify(cross) != 0:
        raise AssertionError(f"Expected E[S_12 S_21]=0, got {cross}")
    print("E[S_12 S_21] = 0: PASS")

    check_target("S_12", [(1, (1, 2))],
                 1 / sp.sqrt(sp.cosh(lam*T)), Phi_X, lam)
    check_target("L = S_12-S_21", [(1, (1, 2)), (-1, (2, 1))],
                 1 / sp.cosh(lam*T), Phi_X, lam)
    check_target("A = (S_12-S_21)/2", [
        (sp.Rational(1, 2), (1, 2)), (-sp.Rational(1, 2), (2, 1)),
    ], 1 / sp.cosh(lam*T/2), Phi_X, lam)
    print("\nAll Brownian checks passed through moment order 4.")


if __name__ == "__main__":
    main()
