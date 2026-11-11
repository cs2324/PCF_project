"""Check general maps and the optional square-matrix interface.

Place this file in tests/ and run from the project root:
    python -m pytest tests/test_linear_map.py -q
"""

import pytest
import sympy as sp

from cf_recovery.linear_map import LinearMap


def test_scalar_valued_map():
    L = LinearMap([2, -1])
    assert L.domain_dim == 2
    assert L([3, 4]) == 2
    assert L([0, 0]) == 0


def test_vector_valued_map():
    L = LinearMap([sp.Matrix([1, 2]), sp.Matrix([3, 4])])
    assert L([2, -1]) == sp.Matrix([-1, 0])


def test_linearity_and_scaling():
    L = LinearMap([sp.Matrix([1, 2]), sp.Matrix([3, 4])])
    x, y = sp.Matrix([2, 1]), sp.Matrix([-1, 3])
    a, b = sp.symbols("a b", real=True)
    assert (L(a * x + b * y) - a * L(x) - b * L(y)).applyfunc(sp.expand) == sp.zeros(2, 1)
    scaled = L.scaled(a)
    assert scaled(x) == a * L(x)
    assert L(x) == sp.Matrix([5, 8])


def test_general_matrices_need_not_be_skew_hermitian():
    L = LinearMap([sp.eye(2), sp.Matrix([[1, 2], [3, 4]])])
    assert L.matrix_dim == 2
    assert L([1, 0]) == sp.eye(2)


@pytest.mark.parametrize("images, error", [
    ([1, 2], TypeError),
    ([sp.eye(2), 1], TypeError),
    ([sp.zeros(2, 3)], ValueError),
    ([sp.eye(2), sp.zeros(2, 3)], ValueError),
    ([sp.eye(2), sp.eye(3)], ValueError),
    ([sp.zeros(0, 0)], ValueError),
])
def test_matrix_dim_rejects_invalid_matrix_inputs(images, error):
    L = LinearMap(images)
    with pytest.raises(error):
        _ = L.matrix_dim


def test_empty_basis_and_wrong_input_dimension():
    with pytest.raises(ValueError):
        LinearMap([])
    with pytest.raises(ValueError):
        LinearMap([1, 2])([1])
