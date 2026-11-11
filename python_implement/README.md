# Scalar characteristic-function recovery from PCF

Given a process PCF `Phi_X` and a finite collection of real coefficients and
nonempty words, this package recovers mixed moments from the PCF and constructs
a finite Taylor polynomial for the characteristic function of

```math
Z=\sum_{j=1}^r c_j\pi_{I_j}(S(X)),\qquad
\mu_m=\mathbb E[Z^m],\qquad
S_R(\lambda)=\sum_{m=0}^R\frac{(i\lambda)^m}{m!}\mu_m.
```

The package is named **`cf_recovery`**. It uses SymPy for exact symbolic
calculations and pytest for tests. The implementation combines single-word
pickers, mixed tensor lifts, and multinomial expansion. Words may have different
lengths, so targets such as `S_1 + S_12` are supported.

## 1. Project layout and installation

The project root contains `README.md`, `requirements.txt`, and the following
files and directories:

| Path | Purpose |
|---|---|
| `cf_recovery/` | Reusable mathematical modules and package exports in `__init__.py` |
| `examples/compute_brownian_moments.py` | Compute moments and polynomials through the general interface, without reference CFs |
| `examples/validate_brownian.py` | Compare recovered results with independent Brownian and area CFs; print individual PASS results |
| `tests/` | Input validation, algebraic identities, and end-to-end pytest checks |
| `docs/characteristic_function_walkthrough.md` | Detailed walkthrough of `characteristic_function.py` (in Chinese) |
| `AGENTS.md` | Interface, mathematical, and validation requirements for Codex |

**Run commands from the project root containing `cf_recovery/`, rather than
from inside `cf_recovery/`.** Relative imports such as `.moment_recovery` are
package imports.

### Windows PowerShell

With Python 3.12 already installed:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest tests -q
.\.venv\Scripts\python.exe -m examples.compute_brownian_moments
.\.venv\Scripts\python.exe -m examples.validate_brownian
```

### Existing Python environment

```bash
python -m pip install -r requirements.txt
python -m pytest tests -q
python -m examples.compute_brownian_moments
python -m examples.validate_brownian
```

On Linux or macOS, create a virtual environment with `python3 -m venv .venv`,
then use `.venv/bin/python` for the pip, pytest, and example commands above.
The implementation was tested on Linux; the Windows commands have not been
executed on a Windows machine in this workspace.

## 2. Recovery pipeline

1. `SignatureCharacteristicFunction(Phi_X, terms)` stores the target random variable.
2. `.moment(m)` uses multinomial expansion to identify the required mixed moments.
3. `MomentRecovery.mixed_moment(words)` constructs one `M_I` for each word.
4. `mixed_tensor_lift(maps)` combines these maps.
5. Query `Phi_X.taylor_coefficient(M, K, 0, D-1)`, where
   `K=sum(len(I) for I in words)` and `D=product(len(I)+1 for I in words)`.
6. Sum the mixed moments with their scalar coefficients and multiplicities to obtain `E[Z**m]`.
7. `.R_truncation(lam, R)` returns `(polynomial, [mu_0,...,mu_R])`.

`taylor_coefficient` already returns the derivative divided by `K!`; do not
divide by `K!` again. The `m!` in the scalar CF expansion is a separate
normalization.

## 3. Why different word lengths are supported

For selected words $W_1,\ldots,W_m$, the mixed tensor lift satisfies the
development tensor-product identity. Each picker's selected entry has no terms
below degree $|W_q|$, and its coefficient at that degree is $S_{W_q}(X)$.
The product therefore has no terms below $K=\sum_q|W_q|$, and its degree-$K$
coefficient is $\prod_q S_{W_q}(X)$.

Under conditions allowing expectation and the relevant derivative to be
interchanged,

```math
\mathbb E\!\left[\prod_{q=1}^m S_{W_q}(X)\right]
=[t^K]\Phi_X(tM_{\mathrm{mixed}})_{0,D-1},\qquad
D=\prod_q(|W_q|+1).
```

Thus this mixed-moment construction does not require equal word lengths.
A separate implementation based on a homogeneous picker may impose a
single-level restriction, but that restriction does not apply here.

## 4. Define and evaluate a target

```python
import sympy as sp
from cf_recovery import BrownianPCF, MomentRecovery, SignatureCharacteristicFunction

T = sp.Symbol('T', nonnegative=True)
lam = sp.Symbol('lambda', real=True)
Phi_X = BrownianPCF(path_dim=2, T=T)
recovery = MomentRecovery(Phi_X)

mu2 = recovery.coordinate_moment((1, 2), 2)  # T**2/2
cross = recovery.mixed_moment([(1, 2), (2, 1)])  # 0

# S_12
coordinate = SignatureCharacteristicFunction(Phi_X, [(1, (1, 2))])
P12, moments12 = coordinate.R_truncation(lam, R=4)

# Half-normalized Levy area A = (S_12-S_21)/2
area = SignatureCharacteristicFunction(Phi_X, [
    (sp.Rational(1, 2), (1, 2)),
    (-sp.Rational(1, 2), (2, 1)),
])
PA, momentsA = area.R_truncation(lam, R=4)
print(PA)
print(momentsA)
# 5*T**4*lambda**4/384 - T**2*lambda**2/8 + 1
# [1, 0, T**2/4, 0, 5*T**4/16]

# Evaluate the polynomial already computed:
print(PA.subs({T: 1, lam: sp.Rational(1, 2)}).evalf())

# A combination of different signature levels:
mixed_level = SignatureCharacteristicFunction(Phi_X, [(3, (1,)), (2, (1, 2))])
print(mixed_level.moment(2))  # 9*T + 2*T**2
```

To follow execution, read the modules in this order:
`examples` -> `characteristic_function` -> `moment_recovery` ->
`single_wordpicker` / `tensor_lift` -> `pcf`.
`LinearMap` and `validation` provide the shared foundations. A detailed
walkthrough is available in `docs/characteristic_function_walkthrough.md`.

## 5. Brownian and Levy-area validation

`examples.validate_brownian` computes results along two independent routes:

- **Recovery:** terms -> mixed lifts -> Brownian PCF coefficients -> moments -> $S_R$.
- **Reference:** an independent scalar CF -> expansion at $\lambda=0$ -> reference moments and polynomial.

Since $\varphi^{(m)}(0)=i^m\mu_m$, the coefficient of $\lambda^m$ in the
reference polynomial must be multiplied by $m!/i^m$ to obtain a moment.
Reference formulas are used only to check recovered results, never to generate
the recovery coefficients.

For standard Brownian motion started at zero, using the Stratonovich signature,
the validation checks moment orders 0 through 4:

| Target | Independent reference CF | Moments: mu_0, mu_1, mu_2, mu_3, mu_4 |
|---|---|---|
| S_12 | (cosh(lambda*T))^(-1/2) | 1, 0, T^2/2, 0, 7*T^4/4 |
| L = S_12-S_21 | 1/cosh(lambda*T) | 1, 0, T^2, 0, 5*T^4 |
| A = L/2 | 1/cosh(lambda*T/2) | 1, 0, T^2/4, 0, 5*T^4/16 |

These are the project's independent Brownian and Levy-area benchmarks.
Matching finitely many coefficients does not prove the full closed forms.
The validation script prints PASS for each moment and polynomial comparison,
and raises `AssertionError` on a mismatch.

The tests also include deterministic paths and a new PCF subclass implementing
only `__call__`, checking that the recovery interface is not Brownian-specific.

## 6. API and input conventions

| Object | Input and output |
|---|---|
| `LinearMap` | Basis images representing a general map L: R^d -> V; square-matrix checks occur only when `matrix_dim` is accessed |
| `M_I(word, path_dim)` | A nonempty word -> the paper's single-word matrix picker |
| `tensor_lift(M, m)` | One map -> its order-m tensor lift |
| `mixed_tensor_lift(maps)` | Maps with a common domain and possibly different matrix sizes -> a mixed lift |
| `PathCharacteristicFunction` | `__call__(M)` returns Phi_X(M); `taylor_coefficient` returns a normalized scalar derivative |
| `BrownianPCF` | Phi_B(M) = exp(T*A_M), A_M = sum_a M(e_a)^2/2; coefficients are computed exactly from this exponential series |
| `MomentRecovery` | `coordinate_moment` and `mixed_moment` |
| `SignatureCharacteristicFunction` | `moment`, `R_truncation`, and a conditional BV tail bound |

The process-dimension attribute is **`path_dim`** throughout the package.
Use `Phi_X.path_dim` to access it.

Declare symbolic assumptions explicitly: `T` is nonnegative, and `lambda` and
coefficients are real. To use another process, supply its PCF subclass. If its
`__call__` supports symbolic real scaling, it can inherit the base coefficient
method; otherwise, it should implement its own coefficient method.

## 7. Scope, limitations, and troubleshooting

- This is a dense symbolic mixed-lift implementation. Symmetric compression and low-rank solvers are not implemented.
- Each lifted matrix has a default dimension limit of 256. For length-two words, moment order 4 requires dimension 81, while order 6 requires dimension 729 and is rejected by default. A sixth-order example from a different implementation cannot be copied unchanged.
- Raising `max_dimension` changes the guard but does not remove the computational cost of dense tensor calculations.
- A finite polynomial is not guaranteed to approximate the complete CF at every real argument. Finitely many recovered moments are not a closed-form proof.
- Conditions for interchanging coefficients or derivatives with expectation must be justified for the process law; tests do not establish those conditions automatically.
- `bounded_variation_tail` requires a deterministic almost-sure bound V_1(X) <= L. It is not a Brownian remainder bound.
- NumPy/SciPy Jacobi solvers, shared-prefix pickers, and homogenization constructions are not included.
- `ModuleNotFoundError: cf_recovery`: run `python -m examples.compute_brownian_moments` from the project root.
- A missing `cf_recovery.validation` module usually means `validation.py` was omitted when copying the package.
- Run package examples using the `-m` commands above rather than launching individual package modules directly.

To merge this package into an existing repository, copy the relevant files from
`cf_recovery/`, `examples/`, and `tests/`, together with `README.md`. Preserve
existing notebooks, references, and additional tests, then run the complete
local test suite. This deliverable does not directly modify your computer's
repository.

## 8. Compute, validate, and inspect tests

Use `python -m examples.compute_brownian_moments` to compute results. This is
an ordinary client of `cf_recovery`: choose the process, set `terms`, call
`R_truncation`, and print the returned objects. No scalar reference CF
is needed. The former `examples/demo.py` has been renamed to this file.

Use `python -m examples.validate_brownian` to check those results against known
scalar CFs. It compares finite Taylor coefficients, not equality of the finite
polynomial and the full CF at every argument. Moment and polynomial comparisons
are equivalent coefficient checks; the second comparison is useful for checking
assembly and normalization, not an independent all-order proof.

Use `python -m pytest tests -v` to see each collected test case by name. To run
only the half-area CF test:

```bash
python -m pytest tests/test_general_pipeline.py::test_levy_area_polynomial_against_independent_cf -v
```

| Test file | Main checks |
|---|---|
| `test_linear_map.py` | Scalar/vector/matrix outputs, linearity, scaling, and optional matrix validation |
| `test_core.py` | Picker word order and repeated letters, same-map lift identity, unequal-size mixed lift identity, invalid inputs and dimension guard |
| `test_recovery.py` | PCF inputs, symbolic fallback versus Brownian coefficient shortcut, derivative degree/factorial, Brownian moments, area conventions, deterministic paths, mixed levels and cancellation |
| `test_general_pipeline.py` | A new process using the inherited coefficient method, half-area polynomial versus reference CF, and PCF-specific input restrictions |

The BV-tail test uses a deterministic straight path of total variation 2; it
must not be interpreted as applying a BV error bound to Brownian motion.
