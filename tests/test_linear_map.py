import pytest
import sympy as sp

from cf_recovery import LinearMap


def test_vector_valued_map():
    e1 = sp.Matrix([1, 0])
    e2 = sp.Matrix([0, 1])

    linear_map = LinearMap([e1, e2])

    assert linear_map.domain_dim == 2
    assert linear_map([2, 3]) == sp.Matrix([2, 3])


def test_matrix_valued_map():
    A1 = sp.Matrix([
        [0, 1],
        [-1, 0]
    ])

    A2 = sp.zeros(2)

    linear_map = LinearMap([A1, A2])

    expected = sp.Matrix([
        [0, 2],
        [-2, 0]
    ])

    assert linear_map([2, 3]) == expected


def test_scaled_map():
    e1 = sp.Matrix([1, 0])
    e2 = sp.Matrix([0, 1])

    linear_map = LinearMap([e1, e2])
    scaled_map = linear_map.scaled(5)

    assert scaled_map([2, 3]) == 5 * linear_map([2, 3])


def test_empty_basis_images():
    with pytest.raises(
        ValueError,
        match="At least one basis image is required"
    ):
        LinearMap([])


def test_wrong_input_dimension():
    e1 = sp.Matrix([1, 0])
    e2 = sp.Matrix([0, 1])

    linear_map = LinearMap([e1, e2])

    with pytest.raises(
        ValueError,
        match="Expected an input of dimension 2"
    ):
        linear_map([1, 2, 3])