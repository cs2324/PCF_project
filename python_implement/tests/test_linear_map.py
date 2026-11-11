"""Check generality and independent Levy-area CF validation."""

import sympy as sp
from cf_recovery import (
    PathCharacteristicFunction, LinearMap, BrownianPCF,
    MomentRecovery, SignatureCharacteristicFunction,
)


class StraightLinePCF(PathCharacteristicFunction):
    """A new law implementing only __call__: x(s)=s on [0,1]."""

    def __init__(self):
        super().__init__(1, 1)

    def __call__(self, M):
        self._validate_M(M)
        return M([1]).exp()


def test_new_process_uses_inherited_coefficient_method():
    recovery = MomentRecovery(StraightLinePCF())
    assert recovery.coordinate_moment((1,), 1) == 1
    assert recovery.coordinate_moment((1, 1), 1) == sp.Rational(1, 2)
    assert recovery.mixed_moment([(1,), (1,)]) == 1


def test_levy_area_polynomial_against_independent_cf():
    T = sp.Symbol("T", nonnegative=True)
    lam = sp.Symbol("lambda", real=True)
    Phi = BrownianPCF(2, T)
    # A = (S_12-S_21)/2. The reference appears ONLY in this test.
    area = SignatureCharacteristicFunction(Phi, [
        (sp.Rational(1, 2), (1, 2)),
        (-sp.Rational(1, 2), (2, 1)),
    ])
    polynomial, moments = area.R_truncation(lam, 4)
    reference = sp.series(1 / sp.cosh(lam*T/2), lam, 0, 5).removeO()
    assert sp.expand(polynomial-reference) == 0
    assert moments == [1, 0, T**2/4, 0, 5*T**4/16]
    recovery = MomentRecovery(Phi)
    assert recovery.mixed_moment([(1, 2), (2, 1)]) == 0


def test_pcf_rejects_scalar_images_without_restricting_linear_map():
    L = LinearMap([2])
    assert L([3]) == 6
    import pytest
    with pytest.raises(TypeError):
        BrownianPCF(1, 1)(L)
