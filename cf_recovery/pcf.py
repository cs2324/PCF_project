"""Represent PCF: Phi_X(M) = E[Dev_M(X)]."""

from abc import ABC, abstractmethod
import sympy as sp
from .linear_map import LinearMap
from .validation import integer, real_scalar


class PathCharacteristicFunction(ABC):
    """
    Represent the path characteristic function of a process X on [0, T].

    For every matrix size N and every linear map M: R^d -> u_N,
    the PCF is Phi_X(M) = E[Dev_M(X)].

    The process dimension d and time duration T are common data for all
    concrete path characteristic functions. A subclass implements the
    law-dependent rule for evaluating Phi_X(M).

    For continuous bounded-variation paths, development is defined by
    dY_s = Y_s M(dX_s), Y_0 = Id, and Dev_M(X) = Y_T, as in the paper.
    A stochastic subclass must specify its integration convention.

    __call__ returns the whole PCF matrix. 
    taylor_coefficient returns one normalized derivative at zero, whenever that derivative exists.
    Existence of the PCF alone does not imply existence of all derivatives.
    """

    def __init__(self, path_dim, T):
        """Store the path dimension d and time duration T.

        path_dim must be a positive integer, excluding bool.
        T must be a finite nonnegative real scalar. 
        For symbolic time, use sp.Symbol("T", nonnegative=True); unknown assumptions are
        rejected. The shared validators implement these checks.
        """
        self.path_dim = integer(path_dim, "path_dim", 1)
        self.T = real_scalar(T, "T", nonnegative=True)

    def _validate_M(self, M):
        """Check M belongs to Hom(R^d, u_N), and return the matrix size N.

        Check the domain dimension, SymPy matrix types, common nonempty
        square shape, and M(e_a).H = -M(e_a). Symbolic identities are
        simplified entrywise; an identity not established by simplify
        is rejected. These restrictions belong to PCF, not LinearMap.
        """
        if not isinstance(M, LinearMap):
            raise TypeError("M must be a LinearMap.")
        if M.domain_dim != self.path_dim:
            raise ValueError("PCF and map dimensions disagree.")
        if any(not isinstance(A, sp.MatrixBase) for A in M.basis_images):
            raise TypeError("PCF basis images must be SymPy matrices.")
        N = M.matrix_dim
        for A in M.basis_images:
            if A.shape != (N, N):
                raise ValueError("All basis images must be N-by-N matrices.")
            if any(sp.simplify(x) != 0 for x in A.H + A):
                raise ValueError("PCF basis images must be provably skew-Hermitian.")
        return N

    def _validate_query(self, M, n, row, col):
        """Validate M and a coefficient query; return its matrix size N.

        n is a nonnegative integer. row and col are zero-based integers
        in {0,...,N-1}. Boolean values are not valid degrees or indices.
        """
        N = self._validate_M(M)
        integer(n, "degree")
        integer(row, "row")
        integer(col, "col")
        if row >= N or col >= N:
            raise ValueError("PCF entry out of range.")
        return N

    @abstractmethod
    def __call__(self, M):
        """Return the N-by-N matrix Phi_X(M) = E[Dev_M(X)].

        A concrete subclass implements the law-dependent evaluation and
        should call _validate_M before computing the development.
        """

    def taylor_coefficient(self, M, n, row, col):
        """Return [t^n] Phi_X(tM)[row, col] by symbolic differentiation.

        Parameters
        ----------
        M : LinearMap
            Map R^d -> u_N, independent of the internal scaling variable.
        n : int
            Nonnegative polynomial degree (not necessarily moment order).
        row, col : int
            Zero-based matrix entry indices.

        Returns
        -------
        SymPy expression
            The n-th derivative at zero divided by n!. The subclass
            must accept symbolic real scaling in __call__, or override
            this method with its own coefficient computation.

        Notes
        -----
        The scaling parameter t is real, so tM remains skew-Hermitian.
        This computes (1/n!) * d^n/dt^n Phi_X(tM)[row,col] at t=0.
        MomentRecovery sets n=|I|m (or the sum of mixed word lengths).
        """
        N = self._validate_query(M, n, row, col)
        # Dummy avoids collisions with user-supplied symbolic parameters.
        t = sp.Dummy("t", real=True)
        result = self(M.scaled(t))
        if not isinstance(result, sp.MatrixBase) or result.shape != (N, N):
            raise ValueError("PCF must return an N-by-N SymPy matrix.")
        derivative = sp.diff(result[row, col], t, n).subs(t, 0)
        return sp.simplify(derivative / sp.factorial(n))


class BrownianPCF(PathCharacteristicFunction):
    """
    Path characteristic function of standard Brownian motion B on [0, T].

    B starts at zero and has independent standard components. For the
    Stratonovich development

        dY_s = sum_a Y_s M(e_a) o dB_s^a,    Y_0 = Id,

    the expected development is

        Phi_B(M) = exp[(T / 2) * sum_a M(e_a)^2].
    """

    def generator(self, M):
        """Return the Brownian expected-development generator A_M.

        For M_a := M(e_a), compute the N-by-N matrix

            A_M = (1 / 2) * sum_a M_a^2,

        so Phi_B(M) = exp(T A_M). Products are matrix products and
        1/2 is represented exactly. M must map R^d into u_N.
        """
        N = self._validate_M(M)
        A_M = sp.zeros(N)
        for M_a in M.basis_images:
            A_M += M_a * M_a
        return sp.Rational(1, 2) * A_M

    def __call__(self, M):
        """Evaluate Phi_B(M) = exp(T A_M).

        Parameters
        ----------
        M : LinearMap M: R^d -> u_N.

        Returns
        -------
        SymPy matrix: the N*N matrix E[Dev_M(B)], using matrix exponential.
        """
        return (self.T * self.generator(M)).exp()

    def taylor_coefficient(self, M, n, row, col):
        """Return [t^n] Phi_B(tM)[row, col] directly from the Brownian PCF.

        Parameters and the normalized-scalar return convention are the
        same as in PathCharacteristicFunction.taylor_coefficient.

        Since A_(tM) = t^2 A_M, Phi_B(tM) = exp(T*t^2*A_M).
        Odd coefficients vanish. For n=2*r the coefficient is

            T^r * (A_M^r)[row,col] / r!.

        Compute A_M^r e_col by r matrix-vector products. This is the
        same coefficient as symbolic differentiation, without computing
        a full matrix exponential. No reference scalar CF is used.
        """
        N = self._validate_query(M, n, row, col)
        if n % 2:
            return sp.Integer(0)
        if n == 0:
            return sp.Integer(row == col)
        r = n // 2
        A_M = self.generator(M)
        vector = sp.zeros(N, 1)
        vector[col] = 1
        for _ in range(r):
            vector = A_M * vector
        return sp.simplify(self.T**r * vector[row] / sp.factorial(r))


class PiecewiseLinearPCF(PathCharacteristicFunction):
    """PCF for one deterministic piecewise-linear path (a Dirac law).

    increments is a nonempty sequence of d-vectors, one per segment.
    Its development is exp(M(dx_1))*...*exp(M(dx_s)), in that order.
    T labels the interval; increasing reparameterization does not alter
    the development. At T=0 only zero increments are allowed.
    """

    def __init__(self, increments, T=1):
        increments = tuple(tuple(dx) for dx in increments)
        if not increments or not increments[0]:
            raise ValueError("Supply at least one nonempty increment.")
        d = len(increments[0])
        if any(len(dx) != d for dx in increments):
            raise ValueError("All increments must have length d.")
        self.increments = tuple(
            tuple(real_scalar(x, "increment") for x in dx)
            for dx in increments
        )
        super().__init__(d, T)
        if self.T == 0 and any(x != 0 for dx in self.increments for x in dx):
            raise ValueError("Nonzero increments require positive duration.")
        if self.T != 0 and self.T.is_positive is not True:
            raise ValueError("For a nonzero duration require T > 0 explicitly.")

    def __call__(self, M):
        N = self._validate_M(M)
        result = sp.eye(N)
        for dx in self.increments:
            result = result * M(dx).exp()
        return result

    def taylor_coefficient(self, M, n, row, col):
        """Multiply truncated exponential series using convolution.

        Segment coefficient of degree j is M(dx)^j/j!.
        Truncation through n is exact for the requested degree n.
        """
        N = self._validate_query(M, n, row, col)
        coefficients = [sp.eye(N)] + [sp.zeros(N) for _ in range(n)]
        for dx in self.increments:
            A = M(dx)
            segment = [sp.eye(N)]
            for j in range(1, n + 1):
                segment.append(segment[-1] * A / j)
            new = []
            for degree in range(n + 1):
                value = sp.zeros(N)
                for j in range(degree + 1):
                    value += coefficients[j] * segment[degree - j]
                new.append(value)
            coefficients = new
        return sp.simplify(coefficients[n][row, col])
