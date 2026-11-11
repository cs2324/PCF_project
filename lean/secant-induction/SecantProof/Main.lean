import SecantProof.Radial
import SecantProof.Induction
import SecantProof.Secant
import SecantProof.SecantValues
import SecantProof.Horizontal

/-! The abstract strong induction is instantiated with the concrete
polynomial differential operator and ordinary iterated real derivatives.
The final statements have no recurrence hypotheses. -/

noncomputable section
namespace SecantProof

theorem mixed_contraction (k l : ℕ) :
    Radial.T k l = (2 : ℝ) ^ (2 * k + l) * (k.factorial : ℝ) *
      (l.factorial : ℝ) *
        iteratedDeriv (k + l)
          (fun z : ℝ => (Real.cos z)⁻¹ * Real.tan z ^ k) 0 := by
  simpa [Induction.scale, Secant.d, Secant.f] using
    Induction.mixed_induction Radial.T Secant.d
      Radial.T_zero_zero Radial.T_rec Secant.d_zero_zero
      Secant.d_rec Secant.d_vanish k l

theorem radial_contraction (m : ℕ) :
    MvPolynomial.eval (fun _ => (0 : ℝ))
      ((Radial.H^[m]) (Radial.a ^ m)) =
      (2 : ℝ) ^ m * (m.factorial : ℝ) *
        iteratedDeriv m (fun z : ℝ => (Real.cos z)⁻¹) 0 := by
  simpa [Radial.T] using mixed_contraction 0 m

theorem horizontal_contraction (m : ℕ) :
    MvPolynomial.eval (fun _ : Fin 3 => (0 : ℝ))
      ((Horizontal.HH^[m]) (Horizontal.a ^ m)) =
      (2 : ℝ) ^ m * (m.factorial : ℝ) *
        iteratedDeriv m (fun z : ℝ => (Real.cos z)⁻¹) 0 := by
  rw [Horizontal.eval_iterate_area]
  exact radial_contraction m

end SecantProof
