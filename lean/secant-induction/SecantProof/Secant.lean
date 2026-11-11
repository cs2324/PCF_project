import Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas
import Mathlib.Analysis.SpecialFunctions.Trigonometric.ArctanDeriv
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Convert
import Lean.Elab.Tactic.Omega

/-!
# Derivatives of the actual analytic secant function

The array below is defined using `iteratedDeriv`, not by a combinatorial
recurrence. Its recurrence is proved by differentiating the real functions
`(cos z)⁻¹ * (tan z)^k` on a neighborhood of zero.
-/

namespace SecantProof.Secant

open Filter
open scoped Topology

noncomputable def f (k : ℕ) (z : ℝ) : ℝ :=
  (Real.cos z)⁻¹ * Real.tan z ^ k

noncomputable def d (n k : ℕ) : ℝ := iteratedDeriv n (f k) 0

theorem f_zero : f 0 = (fun z : ℝ => (Real.cos z)⁻¹) := by
  funext z
  simp [f]

theorem d_zero_zero : d 0 0 = 1 := by simp [d, f]

theorem d_zero_succ (k : ℕ) : d 0 (k + 1) = 0 := by simp [d, f]

theorem d_secant (n : ℕ) :
    d n 0 = iteratedDeriv n (fun z : ℝ => (Real.cos z)⁻¹) 0 := by
  rw [d, f_zero]

private theorem secant_hasDerivAt {z : ℝ} (hz : Real.cos z ≠ 0) :
    HasDerivAt (fun t : ℝ => (Real.cos t)⁻¹)
      ((Real.cos z)⁻¹ * Real.tan z) z := by
  convert (Real.hasDerivAt_cos z).inv hz using 1
  simp [Real.tan_eq_sin_div_cos, div_eq_mul_inv, pow_two]
  ring

private theorem tan_hasDerivAt {z : ℝ} (hz : Real.cos z ≠ 0) :
    HasDerivAt Real.tan (1 + Real.tan z ^ 2) z := by
  convert Real.hasDerivAt_tan hz using 1
  rw [one_div, ← Real.inv_one_add_tan_sq hz, inv_inv]

theorem f_zero_hasDerivAt {z : ℝ} (hz : Real.cos z ≠ 0) :
    HasDerivAt (f 0) (f 1 z) z := by
  rw [f_zero]
  simpa [f] using secant_hasDerivAt hz

theorem f_succ_hasDerivAt (k : ℕ) {z : ℝ} (hz : Real.cos z ≠ 0) :
    HasDerivAt (f (k + 1))
      (((k + 1 : ℕ) : ℝ) * f k z + ((k + 2 : ℕ) : ℝ) * f (k + 2) z) z := by
  convert (secant_hasDerivAt hz).mul ((tan_hasDerivAt hz).pow (k + 1)) using 1
  simp only [f, Nat.add_sub_cancel, Nat.cast_add, Nat.cast_one,
    Nat.cast_ofNat, pow_succ]
  ring

theorem f_contDiffAt (k n : ℕ) : ContDiffAt ℝ n (f k) 0 := by
  have hz : Real.cos (0 : ℝ) ≠ 0 := by simp
  exact (Real.contDiff_cos.contDiffAt.inv hz).mul
    ((Real.contDiffAt_tan.mpr hz).pow k)

private theorem iteratedDeriv_eventuallyEq {g h : ℝ → ℝ}
    (n : ℕ) (heq : g =ᶠ[𝓝 (0 : ℝ)] h) :
    iteratedDeriv n g =ᶠ[𝓝 (0 : ℝ)] iteratedDeriv n h := by
  induction n with
  | zero => simpa using heq
  | succ n ih => simpa only [iteratedDeriv_succ] using ih.deriv

private theorem cos_eventually_ne_zero :
    ∀ᶠ z : ℝ in 𝓝 0, Real.cos z ≠ 0 :=
  Real.continuous_cos.continuousAt.eventually_ne (by simp)

theorem d_rec_zero (n : ℕ) : d (n + 1) 0 = d n 1 := by
  have heq : deriv (f 0) =ᶠ[𝓝 (0 : ℝ)] f 1 := by
    filter_upwards [cos_eventually_ne_zero] with z hz
    exact (f_zero_hasDerivAt hz).deriv
  simpa only [d, iteratedDeriv_succ'] using
    (iteratedDeriv_eventuallyEq n heq).self_of_nhds

theorem d_rec_succ (n k : ℕ) :
    d (n + 1) (k + 1) =
      ((k + 1 : ℕ) : ℝ) * d n k + ((k + 2 : ℕ) : ℝ) * d n (k + 2) := by
  have heq : deriv (f (k + 1)) =ᶠ[𝓝 (0 : ℝ)]
      (fun z => ((k + 1 : ℕ) : ℝ) * f k z + ((k + 2 : ℕ) : ℝ) * f (k + 2) z) := by
    filter_upwards [cos_eventually_ne_zero] with z hz
    exact (f_succ_hasDerivAt k hz).deriv
  change iteratedDeriv (n + 1) (f (k + 1)) 0 = _
  rw [iteratedDeriv_succ', (iteratedDeriv_eventuallyEq n heq).self_of_nhds]
  change iteratedDeriv n
    ((fun z => ((k + 1 : ℕ) : ℝ) * f k z) +
     (fun z => ((k + 2 : ℕ) : ℝ) * f (k + 2) z)) 0 = _
  have h1 : ContDiffAt ℝ n (fun z => ((k + 1 : ℕ) : ℝ) * f k z) 0 :=
    contDiffAt_const.mul (f_contDiffAt k n)
  have h2 : ContDiffAt ℝ n (fun z => ((k + 2 : ℕ) : ℝ) * f (k + 2) z) 0 :=
    contDiffAt_const.mul (f_contDiffAt (k + 2) n)
  rw [iteratedDeriv_add h1 h2,
    iteratedDeriv_const_mul (f_contDiffAt k n),
    iteratedDeriv_const_mul (f_contDiffAt (k + 2) n)]
  rfl

theorem d_rec (n k : ℕ) :
    d (n + 1) k = (if k = 0 then 0 else (k : ℝ) * d n (k - 1)) +
      ((k + 1 : ℕ) : ℝ) * d n (k + 1) := by
  cases k with
  | zero => simpa using d_rec_zero n
  | succ k => simpa [Nat.succ_eq_add_one, add_assoc] using d_rec_succ n k

theorem d_vanish (n k : ℕ) (h : n < k) : d n k = 0 := by
  induction n generalizing k with
  | zero =>
      cases k with
      | zero => omega
      | succ k => exact d_zero_succ k
  | succ n ih =>
      have hk : k ≠ 0 := by omega
      rw [d_rec, if_neg hk, ih (k - 1) (by omega), ih (k + 1) (by omega)]
      simp

end SecantProof.Secant
