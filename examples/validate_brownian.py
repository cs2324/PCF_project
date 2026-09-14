"""Configure targets and run recovery: python -m examples.validate_brownian.

May edit Phi_X, R, and targets below.
A reference CF is optional, but when
provided it must correspond to the chosen target and process.
"""

import sympy as sp
from cf_recovery import BrownianPCF
from .check_target import check_target


def main():
    """Run each configured target with a shared process and default order 4."""
    T = sp.Symbol("T", nonnegative=True)
    lam = sp.Symbol("lambda", real=True)
    Phi_X = BrownianPCF(path_dim=2, T=T)
    R = 4  # Computes R + 1 moments: mu_0,...,mu_R.
    max_dimension = 256  

    # Add/edit targets here; may omit reference_cf when no closed form is known.
    # An individual target may override R, e.g. "R": 2.
    targets = [
        {
            "name": "S_12",
            "terms": [(1, (1, 2))],
            "reference_cf": 1 / sp.sqrt(sp.cosh(lam * T)),
        },
        {
            "name": "A = (S_12-S_21)/2",
            "terms": [
                (sp.Rational(1, 2), (1, 2)),
                (-sp.Rational(1, 2), (2, 1)),
            ],
            "reference_cf": sp.sech(lam * T / 2),
        },
        {
            "name": "3*S_1 + 2*S_12",
            "terms": [(3, (1,)), (2, (1, 2))],
            "R": 2,
        },
    ]

    for target in targets:
        paras = {"R": R, "max_dimension": max_dimension, **target}
        check_target(Phi_X=Phi_X, lam=lam, **paras)


if __name__ == "__main__":
    main()
