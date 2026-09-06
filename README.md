# General homogeneous coordinate-signature recovery from PCF

This code implements the algebraic recovery scheme for

$$
Z_\ell(X)
=
\sum_{|w|=N} c_w\,\pi_w(S(X)),
\qquad
\varphi_\ell(\lambda)
=
\mathbb E[e^{i\lambda Z_\ell(X)}].
$$

The coefficients must be real and all words must currently have the same
length $N$. Thus the implemented scope is **any finite real linear
combination of coordinate signatures at one homogeneous level**. A mixture such
as $\pi_1+\pi_{12}$ needs an additional homogenisation construction and is
deliberately rejected rather than handled incorrectly.

## The product-first idea

The development expansion is

$$
\mathrm{Dev}_{tM}(x)
=
I
+
\sum_{r\ge 1} t^r
\sum_{a_1,\ldots,a_r}
\pi_{a_1\cdots a_r}(S(x))
M(e_{a_1})\cdots M(e_{a_r}).
$$

Therefore the correct design target is the **whole product coefficient**

$$
\langle
u_0,
M(e_{i_1})\cdots M(e_{i_N})v_N
\rangle
=
c_{i_1\cdots i_N},
$$

not the isolated action of one matrix $M(e_a)$. `build_picker` starts from
the required coefficients $c_w$ and constructs matrices satisfying this
identity. This is the precise interpretation of “first consider the total
effect of the product $B_1B_2\cdots$”.

For a single word $I=(i_1,\ldots,i_N)$, the states are the prefix chain
$\emptyset,i_1,i_1i_2,\ldots,I$. For a linear combination, common prefixes
are shared and all degree-$N$ coefficients are stored in one terminal map.
The matrices are $B_a=D_a-D_a^*$, hence skew-Hermitian.

## From one coordinate combination to all its moments

If the base picker acts on $H$, the literal inductive lift is

$$
M_{\ell,m}(e_a)
=
M_{\ell,m-1}(e_a)\otimes I_H
+
I_{H^{\otimes(m-1)}}\otimes M_\ell(e_a).
$$

This is available with `representation="tensor"`. Its dimension is
$(\dim H)^m$.

Because the selected vectors are $u_0^{\otimes m}$ and
$v_N^{\otimes m}$, only the symmetric tensor space is needed. The default
`representation="symmetric"` computes the restriction to $\mathrm{Sym}^m H$,
whose dimension is

$$
\binom{\dim H+m-1}{m}.
$$

Both versions satisfy

$$
\mathbb E[Z_\ell(X)^m]
=
\frac{1}{(Nm)!}
\left.
\frac{d^{Nm}}{dt^{Nm}}
\right|_{t=0}
\langle
u_0^{\otimes m},
\Phi_X(tM_{\ell,m})v_N^{\otimes m}
\rangle.
$$

The tests verify that the full tensor recursion and its symmetric compression
give the same Brownian moments.

## Main functions

- `build_picker(coefficients, alphabet_size=None)`
  - input: `{word_tuple: real_coefficient}`;
  - output: sparse skew-Hermitian matrices `M(e_a)` and the selected indices.
- `verify_picker(picker)`
  - checks the product identity for every word of length $N$.
- `build_moment_query(picker, m, representation="symmetric")`
  - output: the lifted matrices, selected entry and derivative order $Nm$.
- `standard_brownian_moment(...)`
  - evaluates that query using the standard Brownian PCF
    $\Phi_B(tM)=\exp\{Tt^2\sum_a M(e_a)^2/2\}$.
- `characteristic_taylor(moments, lambdas)`
  - evaluates a truncated moment series; it is not claimed to converge for all
    real $\lambda$.
- `jacobi_characteristic(moments, lambdas, order=R)`
  - constructs a finite Jacobi approximation from $2R$ moments. Exact
    all-real recovery requires the scalar moment problem to be determinate and
    the limit $R\to\infty$.

## Examples

For $Z=\pi_{12}(S(B))$:

```python
from pcf_recovery import build_picker, standard_brownian_moments

picker = build_picker({(1, 2): 1.0}, alphabet_size=2)
moments = standard_brownian_moments(picker, maximum_order=6, time=1.0)
print(moments)
# [1, 0, 1/2, 0, 7/4, 0, 139/8] up to floating-point formatting
```

For the half-normalised Lévy area
$A_T=(\pi_{12}-\pi_{21})/2$:

```python
picker = build_picker(
    {(1, 2): 0.5, (2, 1): -0.5},
    alphabet_size=2,
)
moments = standard_brownian_moments(
    picker,
    maximum_order=6,
    time=1.0,
)
```

Run the demonstration and tests from this directory:

```bash
python example_brownian.py
python -m unittest -v test_pcf_recovery.py
```

The only runtime dependencies are NumPy and SciPy; they are listed in
`requirements.txt`. The package can also be imported from the parent directory:

```python
from pcf_recovery import build_picker
```

## What the Brownian check proves

For $I=(1,2)$, the PCF code recovers

$$
\mu_0=1,
\qquad
\mu_2=\frac{T^2}{2},
\qquad
\mu_4=\frac{7T^4}{4},
\qquad
\mu_6=\frac{139T^6}{8},
$$

with odd moments zero. These are exactly the Taylor coefficients implied by

$$
\varphi_{12}(\lambda)
=
\bigl(\cosh(\lambda T)\bigr)^{-1/2}.
$$

This is a PCF/expected-signature check of the explicit formula, independent of
the conditional-Gaussian/PDE derivation. It verifies every computed Taylor
coefficient, but finitely many coefficients alone are not a proof of the
closed form. A full alternative proof would need an all-order recurrence or a
separate identification theorem.
