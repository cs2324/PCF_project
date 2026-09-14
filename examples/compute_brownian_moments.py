"""Run the recovery process for S_12 and Levy area: python -m examples.compute_brownian_moments."""

import sympy as sp
from cf_recovery import BrownianPCF, MomentRecovery, SignatureCharacteristicFunction


def main():
    """Print PCF-derived moments and polynomials."""
    # 1. Choose the process law and symbolic parameters.
    T = sp.Symbol("T", nonnegative=True)
    lam = sp.Symbol("lambda", real=True)
    Phi_X = BrownianPCF(path_dim=2, T=T)
    recovery = MomentRecovery(Phi_X)
    print("E[S_12 S_21] =", recovery.mixed_moment([(1, 2), (2, 1)]))

    # 2. Describe each scalar target using (coefficient, word) pairs.
    targets = [
        ("S_12", [(1, (1, 2))]),
        ("A = (S_12-S_21)/2", [
            (sp.Rational(1, 2), (1, 2)),
            (-sp.Rational(1, 2), (2, 1)),
        ]),
    ]

    for name, terms in targets:
        # 3. Recover moments and the function value of the truncation of the required characteristic function.
        target = SignatureCharacteristicFunction(Phi_X, terms)
        polynomial, moments = target.R_truncation(lam, R=4)
        print(name)
        print("  moments [0..4]:", moments)
        print("  Truncation up to order 4:", polynomial)


if __name__ == "__main__":
    main()
