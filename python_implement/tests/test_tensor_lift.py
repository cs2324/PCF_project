"""Tests for tensor lifts of the single-word picker M_I."""

import pytest
import sympy as sp

from cf_recovery import (
    M_I,
    mat_tensor_product,
    tensor_lift,
)


def test_mat_tensor_product_preserves_factor_order():
    """
    Check that mat_tensor_product([A_1, A_2]) equals
    A_1 tensor A_2 in the stated factor order.
    """
    A_1 = sp.Matrix([
        [1, 2],
        [3, 4],
    ])

    A_2 = sp.Matrix([
        [0, 5],
        [6, 7],
    ])

    expected = sp.Matrix([
        [0, 5, 0, 10],
        [6, 7, 12, 14],
        [0, 15, 0, 20],
        [18, 21, 24, 28],
    ])

    assert mat_tensor_product([A_1, A_2]) == expected


def test_order_two_tensor_lift_on_basis_vectors():
    """
    Verify the paper's defining identity for m=2:

        M^[2](e_a) = M(e_a) tensor Id + Id tensor M(e_a).
    """
    M = M_I(
        word=(1, 2),
        path_dim=2,
    )

    m = 2
    M_dim = M.matrix_dim
    Id = sp.eye(M_dim)
    M_lifted_2 = tensor_lift(M_I=M, m=m)

    for M_ea, M_lifted_ea in zip(
        M.basis_images,
        M_lifted_2.basis_images,
    ):
        expected = (
            sp.kronecker_product(M_ea, Id)
            + sp.kronecker_product(Id, M_ea)
        )

        assert M_lifted_ea == expected

    assert M_lifted_2.domain_dim == M.domain_dim
    assert M_lifted_2.matrix_dim == M_dim ** m


def test_order_one_tensor_lift_is_original_map():
    """
    Check the trivial case M^[1](e_a) = M(e_a).
    """
    M = M_I(
        word=(1, 2),
        path_dim=2,
    )

    M_lifted_1 = tensor_lift(M_I=M, m=1)

    assert M_lifted_1.domain_dim == M.domain_dim
    assert M_lifted_1.matrix_dim == M.matrix_dim
    assert M_lifted_1.basis_images == M.basis_images


def test_lifted_matrix_dimension_is_M_dim_to_power_m():
    """
    Check that M^[m](e_a) has size M_dim^m by M_dim^m.

    For I=(1,2), M_dim=3.  With m=3, every lifted basis
    image must therefore have size 27 by 27.
    """
    M = M_I(
        word=(1, 2),
        path_dim=2,
    )

    m = 3
    M_lifted_3 = tensor_lift(M_I=M, m=m)
    lifted_dim = M.matrix_dim ** m

    assert M_lifted_3.matrix_dim == lifted_dim

    for M_lifted_ea in M_lifted_3.basis_images:
        assert M_lifted_ea.shape == (
            lifted_dim,
            lifted_dim,
        )


def test_tensor_lift_preserves_skew_hermitian_property():
    """
    Check that M^[m](e_a) is skew-Hermitian whenever M(e_a) is.

    Each summand in the tensor-lift definition contains one
    skew-Hermitian factor and identity matrices in all other factors.
    """
    M = M_I(
        word=(1, 2),
        path_dim=2,
    )

    M_lifted_2 = tensor_lift(M_I=M, m=2)

    for M_lifted_ea in M_lifted_2.basis_images:
        assert M_lifted_ea.H == -M_lifted_ea


def test_tensor_lift_evaluation_for_general_x():
    """
    Verify the complete linear-map identity

        M^[2](x) = M(x) tensor Id + Id tensor M(x)

    for a non-basis input x.
    """
    M = M_I(
        word=(1, 2),
        path_dim=2,
    )

    M_dim = M.matrix_dim
    Id = sp.eye(M_dim)
    M_lifted_2 = tensor_lift(M_I=M, m=2)

    x = [2, 3]
    M_x = M(x)

    expected = (
        sp.kronecker_product(M_x, Id)
        + sp.kronecker_product(Id, M_x)
    )

    assert M_lifted_2(x) == expected


def test_tensor_lift_recovers_shuffle_multiplicities():
    """
    Check the endpoint coefficients associated with

        (12) shuffle (12) = 4(1122) + 2(1212).

    For m=2 and |I|=2, the endpoint matrix entry is (0, 8),
    corresponding to the transition from (0,0) to (2,2).
    """
    M = M_I(
        word=(1, 2),
        path_dim=2,
    )

    M_lifted_2 = tensor_lift(M_I=M, m=2)
    M_lifted_e1 = M_lifted_2.basis_images[0]
    M_lifted_e2 = M_lifted_2.basis_images[1]

    product_1122 = (
        M_lifted_e1
        * M_lifted_e1
        * M_lifted_e2
        * M_lifted_e2
    )

    product_1212 = (
        M_lifted_e1
        * M_lifted_e2
        * M_lifted_e1
        * M_lifted_e2
    )

    assert product_1122[0, 8] == 4
    assert product_1212[0, 8] == 2


@pytest.mark.parametrize(
    "invalid_m",
    [
        0,
        -1,
        1.5,
        True,
    ],
)
def test_tensor_lift_rejects_invalid_orders(invalid_m):
    """
    Check that m must be a positive integer and not a Boolean.
    """
    M = M_I(
        word=(1, 2),
        path_dim=2,
    )

    with pytest.raises(ValueError):
        tensor_lift(
            M_I=M,
            m=invalid_m,
        )


def test_tensor_lift_requires_a_linear_map():
    """
    Check that tensor_lift rejects a list of matrices in place of M.
    """
    M = M_I(
        word=(1, 2),
        path_dim=2,
    )

    with pytest.raises(TypeError):
        tensor_lift(
            M=list(M.basis_images),
            m=2,
        )


def test_mat_tensor_product_rejects_empty_factor_list():
    """
    Check that a tensor product with no matrix factors is rejected.
    """
    with pytest.raises(ValueError):
        mat_tensor_product([])