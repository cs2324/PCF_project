"""Represent path characteristic functions Phi_X(M) = E[Dev_M(X)]."""

from abc import ABC, abstractmethod
from numbers import Integral
import sympy as sp

from .linear_map import LinearMap

# ABC means this PCF class is a general interface which can't be used directly. Only concrete subclasses can be called to evaluate Phi_X(M).  A concrete subclass implements the law-dependent rule for evaluating Phi_X(M).
class PathCharacteristicFunction(ABC):
    """
    Represent the path characteristic function of a process X on [0, T].

    For every matrix size N and every linear map

        M: R^d -> u_N,

    the path characteristic function is

        Phi_X(M) = E[Dev_M(X)].

    The process dimension d and time duration T are common data for all
    concrete path characteristic functions.  A subclass implements the
    law-dependent rule for evaluating Phi_X(M).
    """

    def __init__(self, path_dimension, T):
        """
        Store the common parameters: path dimension d of the process X and time duration T.
        
        T may be a nonnegative number or a symbolic SymPy scalar.
        """
        if (
            not isinstance(path_dimension, Integral)
            or isinstance(path_dimension, bool)
            or path_dimension < 1
        ):
            raise ValueError(
                "path_dimension must be a positive integer."
            )

        try:
            T = sp.sympify(T)
        except sp.SympifyError as error:
            raise ValueError(
                "T must be a scalar time duration."
            ) from error

        if (
            isinstance(T, sp.MatrixBase)
            or T.is_real is False
            or T.is_nonnegative is False
        ):
            raise ValueError(
                "T must be a nonnegative real scalar."
            )

        self.path_dimension = path_dimension
        self.T = T

    def _validate_M(self, M):
        """
        Check that M belongs to Hom(R^d, u_N) for some matrix size N.

        This verifies that M is a LinearMap with the same domain dimension
        as X and that all matrices M(e_a) are skew-Hermitian N-by-N
        matrices.

        Raise error or returns the matrix size of M if valid.
            
        """
        if not isinstance(M, LinearMap):
            raise TypeError(
                "M must be a LinearMap."
            )

        if M.domain_dim != self.path_dimension:
            raise ValueError(
                "M.domain_dim must equal the path dimension."
            )

        M_dim = M.matrix_dim

        for M_ea in M.basis_images:
            if not isinstance(M_ea, sp.MatrixBase):
                raise TypeError(
                    "Every basis image M(e_a) must be a SymPy matrix."
                )

            if M_ea.shape != (M_dim, M_dim):
                raise ValueError(
                    "All basis images M(e_a) must be square matrices "
                    "of the same size."
                )

            if M_ea.H != -M_ea:
                raise ValueError(
                    "Every basis image M(e_a) must be "
                    "skew-Hermitian."
                )

        return M_dim

    @abstractmethod
    def __call__(self, M):
        """
        Evaluate Phi_X(M) for a linear map M: R^d -> u_N.

        A concrete subclass must return the N-by-N matrix
        E[Dev_M(X)].
        """


class BrownianPCF(PathCharacteristicFunction):
    """
    Path characteristic function of standard Brownian motion B on [0, T].

    For the development

        dY_s = Y_s M(dB_s),    Y_0 = Id,

    the expected development is

        Phi_B(M)
        = exp[(T / 2) * sum_{a=1}^d M(e_a)^2]

    Thus this class supplies the process-dependent PCF used in
    Step (4) of the recovery algorithm.
    """

    def generator(self, M):
        """
        Return the Brownian expected-development generator(the coefficient of T inside exp)

        For M_a := M(e_a), the generator is

            A_M = (1 / 2) * sum_{a=1}^d M_a^2,

        so that Phi_B(M) = exp(T A_M).
        """
        M_dim = self._validate_M(M)
        A_M = sp.zeros(M_dim)

        for M_ea in M.basis_images:
            A_M += M_ea * M_ea

        return sp.Rational(1, 2) * A_M

    def __call__(self, M):
        """
        Evaluate Phi_B(M) = exp(T A_M).

        Parameters
        ----------
        M: A LinearMap M: R^d -> u_N.

        Returns
        -------
        sympy.Matrix
            The N-by-N matrix E[Dev_M(B)].
        """
        A_M = self.generator(M)
        return (self.T * A_M).exp()