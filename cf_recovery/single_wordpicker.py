"""Construct the single-word picker M_I."""

from numbers import Integral
import sympy as sp
from .linear_map import LinearMap


def E(i, j, matrix_dimension):
    """
    Return the elementary matrix E_{i,j}.
    """
    matrix = sp.zeros(matrix_dimension)
    matrix[i, j] = 1
    return matrix


def B(position, word_length):
    """
    Construct B_r = E_{r-1,r} - E_{r,r-1}
    on C^(k+1), where r = position and k = word_length.
    """
    matrix_dimension = word_length + 1

    return (
        E(position - 1, position, matrix_dimension)
        - E(position, position - 1, matrix_dimension)
    )


def M_I(word, path_dimension):
    """
    Construct the single-word picker

        M_I: R^d -> u(k+1),

    defined by

        M_I(e_a) = sum_{r: i_r=a} B_r.
    """
    # Validate the inputs.
    if (
        not isinstance(path_dimension, Integral)
        or isinstance(path_dimension, bool)
        or path_dimension < 1
    ):
        raise ValueError(
            "path_dimension must be a positive integer."
        )

    word = tuple(word)
    word_length = len(word)

    if word_length == 0:
        raise ValueError("The word must be nonempty.")

    for letter in word:
        if (
            not isinstance(letter, Integral)
            or isinstance(letter, bool)
            or not 1 <= letter <= path_dimension
        ):
            raise ValueError(
                "Every letter must be an integer between "
                "1 and path_dimension."
            )

    basis_images = []

    # Construct M_a = M_I(e_a) separately for a = 1, ..., d.
    for a in range(1, path_dimension + 1):
        img_e_a = sp.zeros(word_length + 1)

        for position, letter in enumerate(word, start=1):
            if letter == a:
                img_e_a += B(position, word_length)

        basis_images.append(img_e_a)

    return LinearMap(basis_images)