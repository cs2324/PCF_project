"""Law-independent moment extraction from PCF coefficient queries."""

import sympy as sp
from .pcf import PathCharacteristicFunction
from .single_wordpicker import M_I, validate_word
from .tensor_lift import mixed_tensor_lift
from .validation import integer


class MomentRecovery:
    """Recover coordinate/mixed moments using one PCF object.

    For words I_1,...,I_m, the endpoint coefficient has degree
    K=sum_j len(I_j), matrix dimension D=product_j(len(I_j)+1).
    Query [t^K] Phi_X(t M_mixed)[0,D-1]. 
    Mathematical validity requires the coefficient/expectation exchange
    for the supplied law; the code cannot certify that assumption.
    """

    def __init__(self, Phi_X, max_dimension=256):
        if not isinstance(Phi_X, PathCharacteristicFunction):
            raise TypeError("Phi_X must implement PathCharacteristicFunction.")
        if max_dimension is not None:
            integer(max_dimension, "max_dimension", 1)
        self.Phi_X = Phi_X
        self.max_dimension = max_dimension

    def mixed_moment(self, words):
        """Return E[product_j pi_{I_j}(S(X))] as a SymPy scalar.

        words is a sequence of nonempty words, possibly of different
        lengths. Repeating a word gives a power of that coordinate.
        The empty sequence represents the empty product and returns 1.
        The PCF coefficient is already normalized: do not need to divide by K!.
        """
        words = tuple(tuple(I) for I in words)
        if not words:
            return sp.Integer(1)
        maps = [M_I(I, self.Phi_X.path_dim) for I in words]
        M = mixed_tensor_lift(maps, self.max_dimension)
        K = sum(len(I) for I in words)
        D = M.matrix_dim
        return self.Phi_X.taylor_coefficient(M, K, 0, D - 1)

    def coordinate_moment(self, word, m):
        """Return E[pi_I(S(X))^m], including m=0; validate I first."""
        m = integer(m, "m")
        word = validate_word(word, self.Phi_X.path_dim)
        return self.mixed_moment([word] * m)
