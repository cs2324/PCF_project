# Verification result

**The general deterministic identities in the two-page note are
Lean-verified.** This includes every natural order, the strengthened
mixed-monomial formula, the actual secant derivatives, and the horizontal
operator reduction.

## Checked final statements

The final theorem signatures have only the parameters shown below. They
contain no assumed recurrence, unproved operator identity, or assumed
secant-number formula.

| Theorem | Parameters | Result |
| --- | --- | --- |
| `SecantProof.mixed_contraction` | `k l : ℕ` | The general mixed-monomial identity, equation (3) in the PDF |
| `SecantProof.radial_contraction` | `m : ℕ` | The radial contraction equals `2^m * m!` times the ordinary `m`th derivative of secant at zero |
| `SecantProof.horizontal_contraction` | `m : ℕ` | The same formula for the horizontal operator on three-variable polynomials |

The Lean source represents the secant function explicitly as
`(Real.cos z)⁻¹`, the reciprocal of cosine.

## Correspondence with the PDF

| PDF content | Definitions or checked results |
| --- | --- |
| Radial operator, equation (1) | `Radial.H` on `MvPolynomial (Fin 2) ℝ` |
| Derivatives and contractions, equation (2) | `Secant.d`, `Radial.T` |
| General theorem, equation (3) | `mixed_contraction` |
| Secant-number corollary, equation (4) | `radial_contraction`, `Secant.d_secant` |
| Monomial action, equation (5) | `Radial.H_monomial` |
| Contraction recurrence, equation (6) | `Radial.T_rec` |
| Derivative recurrence, equation (7) | `Secant.d_rec`, proved by local differentiation |
| Vanishing below the diagonal, equation (8) | `Secant.d_vanish` |
| Leading derivative `d(k,k)=k!` | `Secant.d_diagonal` |
| Strong induction and boundary cases | `Induction.mixed_induction`, instantiated in `Main.lean` |
| Odd secant numbers and initial values | `Secant.d_odd_zero`, `d_zero_zero`, `d_two_zero`, `d_four_zero`, `d_six_zero` |
| Horizontal operator expansion | `Horizontal.HH_expansion` |
| Radial substitution and its iterates | `Horizontal.HH_embed`, `Horizontal.iterate_HH_embed` |
| Final horizontal contraction | `horizontal_contraction` |

The Lean proof of the vanishing result uses induction on the proved
derivative recurrence. The PDF instead explains the same result from the
Taylor expansion. This change of proof does not change the statement.

## Actual checker execution

All six proof modules, the umbrella module, and the audit were checked in
dependency order with the official, unmodified Lean 4.19.0 frontend and
kernel, through the explicit-installation-path adapter included here.
All returned exit code 0. The proof modules produced no warnings or errors.

`check-output.txt` records the actual output, all final theorem signatures,
and SHA-256 hashes of the checked Lean sources. The audit covers all
54 public theorem declarations, including the three final theorems.
Their transitive axiom dependencies are contained in:

```
propext
Classical.choice
Quot.sound
```

There is no `sorryAx` or added mathematical axiom. The source contains no
admitted proof and no `native_decide` use. Abstract recurrence hypotheses
in intermediate lemmas are discharged by proved facts before any final
theorem is stated.

Versions:

- Lean: `4.19.0`
- Lean Git commit: `6caaee842e9495688c1567e78c0e68dbb96942aa`
- Mathlib Git commit: `c44e0c8ee63ca166450922a373c7409c5d26b00b`

The normal `lake build` command was not executed in this workspace because
the launcher could not discover its installation path. The public Lean
frontend API was used instead. This directory explains that adapter;
standard reproduction commands are in the main README.

The PDF's historical sentence saying that the induction was not yet
formalized is superseded by these checks. The separate tensor-matrix
reduction, which the PDF explicitly excludes, is not asserted here.
