"""Small shared validators for exact symbolic calculations."""

from numbers import Integral
import sympy as sp


def integer(value, name, minimum=0):
    """Return an integer >= minimum; reject bool and floats."""
    if isinstance(value, bool) or not isinstance(value, Integral):
        raise ValueError(f"{name} must be an integer >= {minimum}.")
    if value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}.")
    return int(value)


def real_scalar(value, name, nonnegative=False):
    """Require a finite real SymPy scalar with provable assumptions."""
    try:
        value = sp.sympify(value)
    except (sp.SympifyError, TypeError) as error:
        raise ValueError(f"{name} must be a real scalar.") from error
    if not isinstance(value, sp.Expr):
        raise ValueError(f"{name} must be a real scalar.")
    if value.is_real is not True or value.is_finite is not True:
        raise ValueError(f"{name} must be provably finite and real.")
    if nonnegative and value.is_nonnegative is not True:
        raise ValueError(f"{name} must be provably nonnegative.")
    return value
