"""Ordered matrix tensor products and mixed tensorlift and tensor lifts of word-picker maps."""

from math import prod
import sympy as sp
from .linear_map import LinearMap
from .validation import integer


def mat_tensor_product(factors):
    """
    Return the ordered Kronecker product

        A_1 tensor A_2 tensor ... tensor A_m.

    The order of the factors is preserved.

    Parameters
    ----------
    factors :
        Nonempty sequence of SymPy matrices.

    Returns
    -------
    sympy.Matrix
        The Kronecker product of the matrices in the given order.
    """
    factors = tuple(factors)

    if not factors:
        raise ValueError(
            "At least one tensor factor is required."
        )

    if any(not isinstance(A, sp.MatrixBase) for A in factors):
        raise TypeError(
            "Tensor factors must be SymPy matrices."
        )

    result = factors[0]

    for A in factors[1:]:
        result = sp.kronecker_product(result, A)

    return result


def mixed_tensor_lift(word_maps, max_dimension=256):
    """
    Construct the mixed tensor lift of word-picker maps
    M_{I_1}, ..., M_{I_m}.

    This is a generalisation of the tensor-power construction for a single word.

    Suppose

        M_{I_q}: R^d -> Mat_{N_q}(C),
        q = 1, ..., m.
    
    For each standard basis vector e_a,
    construct the linear map

        M_mixed(e_a)
        =
        sum_{q=1}^m
        Id_{N_1} tensor ... tensor M_{I_q}(e_a)
        tensor ... tensor Id_{N_m}.

    Thus the q-th summand acts by M_{I_q}(e_a) on the q-th tensor
    factor and by the identity on every other tensor factor.

    The output acts on

        C^{N_1} tensor ... tensor C^{N_m},

    so its basis-image matrices have dimension

        N_1 * ... * N_m.

    In the project this construction is used for mixed products of
    signature coordinates, for example

        pi_{I_1}(S(X)) ... pi_{I_m}(S(X)),

    which arise when taking powers of a linear combination of signature
    coordinates.

    Notes
    -----
    The paper explicitly defines only the same-word case
    M_I^[m].  This function is its mixed-word generalisation.

    Parameters
    ----------
    word_maps :
        Nonempty sequence of matrix-valued LinearMap objects
        M_{I_1}, ..., M_{I_m}. All maps must have the same domain
        dimension, but their matrix dimensions may be different.

    max_dimension : int or None, default=256
        Maximum allowed dimension of the lifted basis-image matrices.
        The check is performed before the matrices are allocated.
        If None, no size guard is applied.

    Returns
    -------
    LinearMap
        The mixed lifted map
        R^d -> Mat_{N_1 ... N_m}(C).
    """
    word_maps = tuple(word_maps)

    if not word_maps:
        raise TypeError(
            "word_maps must be a nonempty sequence of LinearMap objects."
        )

    if any(not isinstance(M_I, LinearMap) for M_I in word_maps):
        raise TypeError(
            "word_maps must be a nonempty sequence of LinearMap objects."
        )

    path_dim = word_maps[0].domain_dim

    if any(
        M_I.domain_dim != path_dim
        for M_I in word_maps
    ):
        raise ValueError(
            "All word-picker maps must have the same domain."
        )

    matrix_dimensions = [
        M_I.matrix_dim
        for M_I in word_maps
    ]

    lifted_dimension = prod(matrix_dimensions)

    if max_dimension is not None:
        integer(max_dimension, "max_dimension", 1)

        if lifted_dimension > max_dimension:
            raise ValueError(
                f"Lifted dimension {lifted_dimension} "
                "exceeds size guard."
            )

    identities = [
        sp.eye(matrix_dimension)
        for matrix_dimension in matrix_dimensions
    ]

    lifted_basis_images = []

    # Construct M_mixed(e_a) for each basis vector e_a of R^d.
    for a in range(path_dim):
        lifted_image = sp.zeros(lifted_dimension)

        # Add the contribution in which M_{I_q}(e_a)
        # acts on tensor factor q.
        for q, M_I_q in enumerate(word_maps):
            factors = list(identities)

            # LinearMap stores M_{I_q}(e_a) as basis_images[a].
            factors[q] = M_I_q.basis_images[a]

            lifted_image += mat_tensor_product(factors)

        lifted_basis_images.append(lifted_image)

    return LinearMap(lifted_basis_images)


def tensor_lift(M_I, m, max_dimension=256):
    """
    Construct the tensor-lifted word-picker M_I^[m]: R^d -> u((k+1)^m)

        M_I^[m](e_a)
        =
        sum_{q=1}^m
        Id^(tensor(q-1))
        tensor M_I(e_a)
        tensor Id^(tensor(m-q)), a = 1, ..., d.

    The lifted map acts on H_m = (C^(k+1))^(tensor m).

    Since M_I(e_a) is stored as M_I.basis_images[a], this function
    constructs the above sum separately for every basis vector e_a.

    The lift is used to recover the m-th moment of the signature
    coordinate pi_I(S(X)) from PCF.

    Parameters
    ----------
    M_I : LinearMap
        The word-picker associated with a fixed word I. If |I| = k,
        its basis images are (k+1)-by-(k+1) matrices.

    m : int
        Positive integer giving the moment order and the number of
        tensor factors.

    max_dimension : int or None, default=256
        Maximum allowed matrix dimension of M_I^[m].
        If None, no size guard is applied.

    Returns
    -------
    LinearMap
        The tensor-lifted map M_I^[m].

    Notes
    -----
    This is the same-word special case of mixed_tensor_lift:

        tensor_lift(M_I, m) = mixed_tensor_lift([M_I, ..., M_I]).

    """
    if not isinstance(M_I, LinearMap):
        raise TypeError(
            "M_I must be a LinearMap."
        )

    integer(m, "m", 1)

    return mixed_tensor_lift(
        [M_I] * m,
        max_dimension=max_dimension,
    )