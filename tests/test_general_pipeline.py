"""Unit tests for maps, pickers, tensor products and input contracts."""

import pytest
import sympy as sp
from cf_recovery import (
    LinearMap, M_I, E, B,
    tensor_lift, mixed_tensor_lift, mat_tensor_product,
)


def test_linear_map_and_scaling():
    M = LinearMap([sp.eye(2), sp.zeros(2)])
    assert M.domain_dim == M.matrix_dim == 2
    assert M([3, 4]) == 3 * sp.eye(2)
    assert M.scaled(2)([3, 4]) == 6 * sp.eye(2)
    assert M([3, 4]) == 3 * sp.eye(2)
    with pytest.raises(ValueError):
        M([1])


def test_picker_word_order_and_repeated_letters():
    M = M_I((1, 2), 2)
    assert isinstance(M, LinearMap)
    A, C = M.basis_images
    assert (A * C)[0, 2] == 1
    assert (C * A)[0, 2] == 0
    assert all(A.H == -A for A in M.basis_images)
    repeated = M_I((1, 1, 2), 3)
    assert repeated.basis_images[0] == B(1, 3) + B(2, 3)
    assert repeated.basis_images[2] == sp.zeros(4)
    assert E(0, 1, 2)[0, 1] == 1


@pytest.mark.parametrize("word", [(), (0,), (3,), (True,), (1.5,)])
def test_invalid_word(word):
    with pytest.raises(ValueError):
        M_I(word, 2)


@pytest.mark.parametrize("m", [0, -1, True, 1.5])
def test_invalid_tensor_order(m):
    with pytest.raises(ValueError):
        tensor_lift(M_I((1,), 1), m)


def test_tensor_identity_and_dimensions():
    M = M_I((1, 2), 2)
    assert tensor_lift(M, 1).basis_images == M.basis_images
    lift = tensor_lift(M, 2)
    assert lift.domain_dim == 2 and lift.matrix_dim == 9
    for A, L in zip(M.basis_images, lift.basis_images):
        expected = (sp.kronecker_product(A, sp.eye(3))
                    + sp.kronecker_product(sp.eye(3), A))
        assert L == expected
    assert all(A.H == -A for A in lift.basis_images)
    with pytest.raises(ValueError, match="size guard"):
        tensor_lift(M, 6)


def test_mixed_dimensions_and_factor_order():
    A, C = M_I((1,), 2), M_I((1, 2), 2)
    M = mixed_tensor_lift([A, C])
    assert M.matrix_dim == 6
    assert mat_tensor_product([A.basis_images[0], C.basis_images[0]]) == (
        sp.kronecker_product(A.basis_images[0], C.basis_images[0]))
    with pytest.raises(ValueError):
        mat_tensor_product([])
    with pytest.raises(ValueError):
        mixed_tensor_lift([A, M_I((1,), 1)])
