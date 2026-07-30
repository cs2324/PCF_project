import pytest
import sympy as sp

from cf_recovery import E, B, M_I


def test_elementary_matrix():
    """
    Check E_{0,1}.
    """
    expected = sp.Matrix([
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 0],
    ])

    assert E(0, 1, 3) == expected


def test_B_1():
    """
    Check B_1 = E_{0,1} - E_{1,0}.
    """
    expected = sp.Matrix([
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 0],
    ])

    assert B(
        position=1,
        word_length=2,
    ) == expected


def test_picker_for_word_12():
    """
    Check M_I for I = (1, 2).
    """
    picker = M_I(
        word=(1, 2),
        path_dimension=2,
    )

    expected_M_e1 = sp.Matrix([
        [0, 1, 0],
        [-1, 0, 0],
        [0, 0, 0],
    ])

    expected_M_e2 = sp.Matrix([
        [0, 0, 0],
        [0, 0, 1],
        [0, -1, 0],
    ])

    assert picker.domain_dim == 2
    assert picker.matrix_dim == 3

    assert picker.basis_images[0] == expected_M_e1
    assert picker.basis_images[1] == expected_M_e2


def test_picker_detects_word_order():
    """
    Check that the product detects the order (1, 2).
    """
    picker = M_I(
        word=(1, 2),
        path_dimension=2,
    )

    M_e1 = picker.basis_images[0]
    M_e2 = picker.basis_images[1]

    # For SymPy matrices, * denotes matrix multiplication.
    forward_product = M_e1 * M_e2
    reverse_product = M_e2 * M_e1

    assert forward_product[0, 2] == 1
    assert reverse_product[0, 2] == 0


def test_repeated_letters():
    """
    For I = (1, 1, 2),

        M_I(e_1) = B_1 + B_2,
        M_I(e_2) = B_3.
    """
    picker = M_I(
        word=(1, 1, 2),
        path_dimension=2,
    )

    expected_M_e1 = sp.Matrix([
        [0, 1, 0, 0],
        [-1, 0, 1, 0],
        [0, -1, 0, 0],
        [0, 0, 0, 0],
    ])

    expected_M_e2 = sp.Matrix([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, -1, 0],
    ])

    assert picker.basis_images[0] == expected_M_e1
    assert picker.basis_images[1] == expected_M_e2


def test_unused_direction_maps_to_zero():
    """
    For I = (1, 2) in R^3, M_I(e_3) is zero.
    """
    picker = M_I(
        word=(1, 2),
        path_dimension=3,
    )

    assert picker.domain_dim == 3
    assert picker.basis_images[2] == sp.zeros(3)


def test_basis_images_are_skew_hermitian():
    """
    Check A^* = -A for every basis image.
    """
    picker = M_I(
        word=(1, 1, 2),
        path_dimension=2,
    )

    for image in picker.basis_images:
        # image.H is the conjugate transpose.
        assert image.H == -image


def test_linear_map_evaluation():
    """
    Check M(x) = x_1 M(e_1) + x_2 M(e_2).
    """
    picker = M_I(
        word=(1, 2),
        path_dimension=2,
    )

    expected = (
        2 * picker.basis_images[0]
        + 3 * picker.basis_images[1]
    )

    # LinearMap defines __call__, so use picker(x).
    assert picker([2, 3]) == expected


@pytest.mark.parametrize(
    "invalid_word",
    [
        (),
        (1, 3),
        (0, 1),
        (True, 2),
        (1.5, 2),
    ],
)
def test_invalid_words_are_rejected(invalid_word):
    with pytest.raises(ValueError):
        M_I(
            word=invalid_word,
            path_dimension=2,
        )


@pytest.mark.parametrize(
    "invalid_dimension",
    [
        0,
        -1,
        1.5,
        True,
    ],
)
def test_invalid_path_dimensions_are_rejected(
    invalid_dimension,
):
    with pytest.raises(ValueError):
        M_I(
            word=(1,),
            path_dimension=invalid_dimension,
        )