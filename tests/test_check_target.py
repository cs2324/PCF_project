"""Check the general example helper with and without a reference CF."""

import pytest
import sympy as sp
from cf_recovery import PiecewiseLinearPCF
from examples.check_target import check_target


def test_compute_without_reference(capsys):
    lam = sp.Symbol("lambda", real=True)
    polynomial, moments = check_target(
        "straight", [(1, (1,))], Phi_X=PiecewiseLinearPCF([(2,)]),
        lam=lam, R=2,
    )
    assert moments == [1, 2, 4]
    assert polynomial == 1 + 2*sp.I*lam - 2*lam**2
    assert "PASS" not in capsys.readouterr().out


def test_reference_comparison_and_dimension_guard():
    lam = sp.Symbol("lambda", real=True)
    options = dict(name="straight", terms=[(1, (1,))],
                   Phi_X=PiecewiseLinearPCF([(2,)]), lam=lam, R=2)
    assert check_target(reference_cf=sp.exp(2*sp.I*lam), **options)[1] == [1, 2, 4]
    with pytest.raises(AssertionError):
        check_target(reference_cf=sp.exp(sp.I*lam), **options)
    with pytest.raises(ValueError, match="size guard"):
        check_target(max_dimension=3, **options)
