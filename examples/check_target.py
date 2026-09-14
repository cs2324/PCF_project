"""General PCF recovery with reference-CF validation"""

import sympy as sp
from cf_recovery import SignatureCharacteristicFunction


def check_target(name, terms, reference_cf=None, *, Phi_X, lam, R=4,
                 max_dimension=256):
    """Recover moments 0,...,R and the truncation S_R for a target Z under the supplied PCF.

    terms contains (real coefficient, word) pairs. Words may have different
    lengths. No scalar reference CF is needed for recovery.

    If reference_cf is a SymPy expression, also compare reference moments
    and the degree-R Taylor polynomial; otherwise print recovered results
    without claiming validation. Reference coefficients a_m are converted
    to moments using a_m * m! / i**m.
    max_dimension controls the tensor-matrix size guard, not efficiency.
    Return (polynomial, moments); raise AssertionError on a mismatch.
    """
    target = SignatureCharacteristicFunction(
        Phi_X, terms, max_dimension=max_dimension
    )
    polynomial, moments = target.R_truncation(lam, R)
    if reference_cf is None:
        print(f"\n{name} (computed without a reference CF)")
        print("m | recovered moment")
        for m, recovered in enumerate(moments):
            print(f"{m} | {recovered}")
        print(f"S_{R}(lambda) =", polynomial)
        return polynomial, moments

    # Expand the independent reference through degree R.
    reference_series = sp.series(reference_cf, lam, 0, R + 1).removeO().expand() # remove the O(lam^(R+1)) term and expand
    print(f"\n{name}")
    print("m | recovered moment | reference moment | check")
    for m, recovered in enumerate(moments):
        # Convert the Taylor coefficient to E[Z**m] before comparison.
        expected = sp.simplify(
            reference_series.coeff(lam, m) * sp.factorial(m) / sp.I**m
        )
        if sp.simplify(recovered - expected) != 0:
            raise AssertionError(f"{name}, m={m}: {recovered} != {expected}")
        print(f"{m} | {recovered} | {expected} | PASS")
    # Check the assembled polynomial, including its i**m / m! factors.
    if sp.simplify(polynomial - reference_series) != 0:
        raise AssertionError(f"{name}: Taylor polynomial mismatch")
    print("S_R(lambda) =", polynomial)
    print("Polynomial comparison: PASS")
    return polynomial, moments

