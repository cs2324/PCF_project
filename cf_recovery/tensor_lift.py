"""Construct tensor lifts M_I^[m] of matrix-valued linear maps."""

from numbers import Integral
import sympy as sp
from .linear_map import LinearMap


def mat_tensor_product(factors):
    """
    Compute A_1 tensor ... tensor A_m in the given factor order.
    """
    factors = tuple(factors)

    if len(factors) == 0:
        raise ValueError(
            "At least one Kronecker factor is required."
        )

    result = factors[0]

    for factor in factors[1:]:
        result = sp.kronecker_product(result, factor)

    return result


def tensor_lift(M, m):
    """
    Construct the order-m tensor lift of a matrix-valued linear map.

    For LinearMap M: R^d -> Mat_N(C), write M_a:=M(e_a), and the lifted map M^[m] is defined by

        M^[m](e_a) = sum_{q=1}^m I^(tensor(q-1)) tensor M_a tensor I^(tensor(m-q)).

    The output is a LinearMap M_I^[m]: R^d -> Mat_{N^m}(C).

    Dimensions: M_dim is the size of the square basis-image matrices of M, 
    and lifted_dim = M_dim^m is the size of the square basis-image matrices of M^[m].
    """
    if not isinstance(M, LinearMap):
        raise TypeError(
            "The input linear map M must be a LinearMap."
        )

    if (
        not isinstance(m, Integral)
        or isinstance(m, bool)
        or m < 1
    ):
        raise ValueError(
            "order m must be a positive integer."
        )

    M_dim = M.matrix_dim
    lifted_dim = M_dim ** m
    Id = sp.eye(M_dim)
    lifted_basis_images = []

    # M_a = M(e_a) for a = 1, ..., d, where d = M.domain_dim.
    # M^{[m]}(e_a)=\sum_{q=1}^{m} {Id}^{\otimes(q-1)} \otimes M_a \otimes {Id}^{\otimes(m-q)}.
    for M_a in M.basis_images:
        lifted_image = sp.zeros(lifted_dim)

        # Iterate over the m tensor factors, inserting M_a in each position.
        for factor_position in range(m):
            factors = [
                M_a if position == factor_position else Id
                for position in range(m)
            ]

            lifted_image += mat_tensor_product(factors)

        lifted_basis_images.append(lifted_image)

    return LinearMap(lifted_basis_images)