# The secant contraction identity in Lean

This project formalizes the deterministic argument in the two-page note
**An induction proof of the secant-number contraction identity**.

**Verification passed:** all proof modules and all 54 public theorem axiom
audits completed successfully under Lean 4.19.0. See
`verification/REPORT.md` and `verification/check-output.txt`.

The main statements use the real polynomial operator

```
H = 4 r ∂r² + 4 ∂r + r ∂a²
```

and ordinary real derivatives of `sec(z) = 1 / cos(z)`. In particular, the
secant numbers are not introduced as an arbitrary recursively defined
sequence: their definition uses Mathlib's `iteratedDeriv`.

## Final theorem

`SecantProof.mixed_contraction` proves, for every pair of natural numbers
`k` and `l`,

\[
\left.H^{k+\ell}(r^k a^\ell)\right|_{(0,0)}
=2^{2k+\ell}k!\ell!\,
\left.\frac{d^{k+\ell}}{dz^{k+\ell}}
   \bigl(\sec z\,\tan^kz\bigr)\right|_{z=0}.
\]

`SecantProof.radial_contraction` specializes this to

\[
\left.H^m a^m\right|_{(0,0)}
=2^m m!\left.\frac{d^m}{dz^m}\sec z\right|_{z=0}.
\]

`SecantProof.horizontal_contraction` proves the same formula for the
horizontal operator on polynomials in `x`, `y`, and `a`. All three final
theorems have only natural-number parameters; no additional hypotheses
are required.

## Proof structure

- `SecantProof/Radial.lean` defines `H` on multivariate polynomials over the
  real numbers, proves its general monomial action, and derives the
  contraction recurrence.
- `SecantProof/Induction.lean` proves the strengthened strong induction,
  including the factorial and power-of-two normalization and every
  boundary case.
- `SecantProof/Secant.lean` defines
  `d n k = iteratedDeriv n (fun z => (cos z)⁻¹ * (tan z)^k) 0` and proves
  the recurrence from actual local differentiation near zero. It also
  proves vanishing when `n < k`.
- `SecantProof/SecantValues.lean` proves that the odd secant derivatives
  vanish and checks the displayed values 1, 1, 5 and 61.
- `SecantProof/Horizontal.lean` connects the radial operator to
  `(∂x - y ∂a)² + (∂y + x ∂a)²` under `r = x² + y²`.
- `SecantProof/Main.lean` instantiates the induction with the concrete
  operator and concrete derivatives, yielding the final identities
  without additional recurrence assumptions.

The abstract recurrence hypotheses in `Induction.lean` are intermediate
lemma parameters, discharged by proved theorems in `Main.lean`. They are
not added axioms.

## Reproduction

Lean is pinned to `leanprover/lean4:v4.19.0`, and Mathlib is pinned to commit
`c44e0c8ee63ca166450922a373c7409c5d26b00b` (the v4.19.0 release).

From this directory in a standard Lean/Elan installation:

```sh
lake update
lake exe cache get
lake build
lake env lean Audit.lean
```

The verification report records the checks actually executed for this
artifact. `Audit.lean` lists the axiom dependencies of the principal
claims. Standard Lean foundations (`propext`, `Classical.choice`,
`Quot.sound`) are distinct from admitted proofs or added mathematical
assumptions.

## Scope

The requested two-page note concerns the deterministic polynomial identity.
Its separate tensor-matrix application and any probabilistic application
are outside the note and outside this project's target.

The PDF was written before this formalization. Its final sentence about
the induction not yet being formalized is historical; the verification
report accompanying this project records the subsequent Lean checks.
