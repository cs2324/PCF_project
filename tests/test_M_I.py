import numpy as np

from cf_recovery import E, B, M_I


# ---------------------------------------------------------
# Test 1: elementary matrix E_{0,1}
# ---------------------------------------------------------

expected_E_01 = np.array([
    [0, 1, 0],
    [0, 0, 0],
    [0, 0, 0],
], dtype=complex)

assert np.allclose(
    E(0, 1, 3),
    expected_E_01,
)


# ---------------------------------------------------------
# Test 2: B_1 = E_{0,1} - E_{1,0}
# ---------------------------------------------------------

expected_B_1 = np.array([
    [0, 1, 0],
    [-1, 0, 0],
    [0, 0, 0],
], dtype=complex)

assert np.allclose(
    B(position=1, word_length=2),
    expected_B_1,
)


# ---------------------------------------------------------
# Test 3: single-word picker for I = (1, 2)
# ---------------------------------------------------------

picker_12 = M_I(
    word=(1, 2),
    path_dimension=2,
)

expected_M_e1 = np.array([
    [0, 1, 0],
    [-1, 0, 0],
    [0, 0, 0],
], dtype=complex)

expected_M_e2 = np.array([
    [0, 0, 0],
    [0, 0, 1],
    [0, -1, 0],
], dtype=complex)

assert picker_12.domain_dim == 2
assert picker_12.matrix_dim == 3

assert np.allclose(
    picker_12.basis_images[0],
    expected_M_e1,
)

assert np.allclose(
    picker_12.basis_images[1],
    expected_M_e2,
)


# ---------------------------------------------------------
# Test 4: the product detects the word order
#
# [M_I(e_1) M_I(e_2)]_{0,2} = 1,
# [M_I(e_2) M_I(e_1)]_{0,2} = 0.
# ---------------------------------------------------------

forward_product = (
    picker_12.basis_images[0]
    @ picker_12.basis_images[1]
)

reverse_product = (
    picker_12.basis_images[1]
    @ picker_12.basis_images[0]
)

assert np.isclose(
    forward_product[0, 2],
    1,
)

assert np.isclose(
    reverse_product[0, 2],
    0,
)


# ---------------------------------------------------------
# Test 5: repeated letters, I = (1, 1, 2)
#
# M_I(e_1) = B_1 + B_2,
# M_I(e_2) = B_3.
# ---------------------------------------------------------

picker_112 = M_I(
    word=(1, 1, 2),
    path_dimension=2,
)

expected_repeated_e1 = np.array([
    [0, 1, 0, 0],
    [-1, 0, 1, 0],
    [0, -1, 0, 0],
    [0, 0, 0, 0],
], dtype=complex)

expected_repeated_e2 = np.array([
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 1],
    [0, 0, -1, 0],
], dtype=complex)

assert np.allclose(
    picker_112.basis_images[0],
    expected_repeated_e1,
)

assert np.allclose(
    picker_112.basis_images[1],
    expected_repeated_e2,
)


# ---------------------------------------------------------
# Test 6: unused direction is sent to the zero matrix
# ---------------------------------------------------------

picker_in_dimension_3 = M_I(
    word=(1, 2),
    path_dimension=3,
)

assert picker_in_dimension_3.domain_dim == 3

assert np.allclose(
    picker_in_dimension_3.basis_images[2],
    np.zeros((3, 3), dtype=complex),
)


# ---------------------------------------------------------
# Test 7: all basis images are skew-Hermitian
#
# A* = conjugate(A).T = -A.
# ---------------------------------------------------------

for image in picker_112.basis_images:
    assert np.allclose(
        image.conjugate().T,
        -image,
    )


# ---------------------------------------------------------
# Test 8: invalid words are rejected
# ---------------------------------------------------------

try:
    M_I(
        word=(),
        path_dimension=2,
    )
except ValueError:
    pass
else:
    raise AssertionError(
        "An empty word should raise ValueError."
    )

try:
    M_I(
        word=(1, 3),
        path_dimension=2,
    )
except ValueError:
    pass
else:
    raise AssertionError(
        "A letter outside {1, ..., d} should raise ValueError."
    )


print("Single-word picker tests passed.")