"""Finite moment polynomials for real linear combinations of coordinates."""

from itertools import combinations_with_replacement
from collections import Counter
from math import factorial
import sympy as sp
from .moment_recovery import MomentRecovery
from .single_wordpicker import validate_word
from .validation import integer, real_scalar


class SignatureCharacteristicFunction:
    """Target Z=sum_j c_j*pi_{I_j}(S(X)), with real coefficients.

    terms=[(coefficient, word), ...]; words can have different lengths.
    moment(m) returns E[Z^m]. 
    R_truncation returns (polynomial, moments),
    NOT a promise of a globally convergent CF approximation.
    An empty terms list represents Z=0.
    """

    def __init__(self, Phi_X, terms, max_dimension=256):
        self.recovery = MomentRecovery(Phi_X, max_dimension)
        collected = {} # collect coefficients for repeated words
        for term in terms:
            if not isinstance(term, (tuple, list)) or len(term) != 2:
                raise ValueError("Each term must be (coefficient, word).")
            c, I = term
            c = real_scalar(c, "coefficient")
            I = validate_word(I, Phi_X.path_dim)
            collected[I] = collected.get(I, 0) + c
        self.terms = tuple((sp.simplify(c), I)
                           for I, c in collected.items()
                           if sp.simplify(c) != 0)

    def moment(self, m):
        """Expand Z^m, grouping scalar products by their multiplicities.

        An index j selected n_j times contributes m!/product_j(n_j!)
        times product_j(c_j^n_j) times its mixed moment.
        Return E[Z^m] as a SymPy scalar. The empty product (m=0) returns 1.
        """
        m = integer(m, "m")
        if m == 0:
            return sp.Integer(1)
        total = sp.Integer(0)

        for indices in combinations_with_replacement(range(len(self.terms)), m):
            counts = Counter(indices) # count how many times each term index is selected, as dictionary {index: count}
            multiplicity = factorial(m)
            for count in counts.values():
                multiplicity //= factorial(count)
            coefficient = sp.Integer(multiplicity) #this is the number of permutations under this selection of indices, which is m!/(n_1! n_2! ... n_k!) where n_j is the number of times index j appears in indices

            words = []
            for j in indices:
                c, I = self.terms[j]
                coefficient *= c
                words.append(I)
            total += coefficient * self.recovery.mixed_moment(words)
        return sp.simplify(total)

    def R_truncation(self, lambda_value, R):
        """Return the finite truncation of the required characteristic
        function value: S_R = sum_(m=0)^R (i*lambda)^m*mu_m/m!, 
        and first R+1 moments [mu_0,...,mu_R].
        """
        R = integer(R, "R")
        lam = real_scalar(lambda_value, "lambda")
        moments = [self.moment(m) for m in range(R + 1)]
        polynomial = sum((sp.I * lam)**m * mu / sp.factorial(m)
                         for m, mu in enumerate(moments))
        return sp.expand(polynomial), moments

    def bounded_variation_tail(self, lambda_value, R, L):
        """Conditional error bound if given total l1-variation V_1(X)<=L a.s.

        Q=sum_j |c_j| L^|I_j|/|I_j|!. Return exp(|lambda|Q) minus
        its degree-R partial sum. The caller must justify V_1(X)<=L;
        this method is NOT a Brownian remainder bound.
        """
        R = integer(R, "R")
        lam = real_scalar(lambda_value, "lambda")
        L = real_scalar(L, "L", nonnegative=True)
        Q = sum(abs(c) * L**len(I) / sp.factorial(len(I))
                for c, I in self.terms)
        x = abs(lam) * Q
        return sp.simplify(sp.exp(x) - sum(x**m / sp.factorial(m)
                                          for m in range(R + 1)))
