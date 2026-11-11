import SecantProof.Secant
import Lean.Elab.Tactic.Omega
import Mathlib.Tactic.NormNum

namespace SecantProof.Secant

/-!
The parity argument uses only the proved derivative recurrence and initial
values, and is applied below to the analytic secant derivatives `d`.
-/

private theorem recurrence_odd_vanish
    (a : ℕ → ℕ → ℝ)
    (hzero : ∀ k, a 0 (k + 1) = 0)
    (hrec : ∀ n k, a (n + 1) k =
      (if k = 0 then 0 else (k : ℝ) * a n (k - 1)) +
        ((k + 1 : ℕ) : ℝ) * a n (k + 1)) :
    ∀ n k, (n + k) % 2 = 1 → a n k = 0 := by
  intro n
  induction n with
  | zero =>
      intro k hodd
      cases k with
      | zero => omega
      | succ k => exact hzero k
  | succ n ih =>
      intro k hodd
      rw [hrec n k]
      have hplus : a n (k + 1) = 0 := ih (k + 1) (by omega)
      rw [hplus, mul_zero, add_zero]
      by_cases hk : k = 0
      · simp [hk]
      · rw [if_neg hk, ih (k - 1) (by omega), mul_zero]

private theorem recurrence_small_values
    (a : ℕ → ℕ → ℝ)
    (hbase : a 0 0 = 1)
    (hzero : ∀ k, a 0 (k + 1) = 0)
    (hrec : ∀ n k, a (n + 1) k =
      (if k = 0 then 0 else (k : ℝ) * a n (k - 1)) +
        ((k + 1 : ℕ) : ℝ) * a n (k + 1)) :
    a 2 0 = 1 ∧ a 4 0 = 5 ∧ a 6 0 = 61 := by
  constructor
  · norm_num [hrec, hbase, hzero]
  constructor
  · norm_num [hrec, hbase, hzero]
  · norm_num [hrec, hbase, hzero]

/-- Analytic secant-tangent derivatives vanish when their total parity is odd. -/
theorem d_eq_zero_of_odd (n k : ℕ) (hodd : (n + k) % 2 = 1) :
    d n k = 0 :=
  recurrence_odd_vanish d d_zero_succ d_rec n k hodd

/-- Every odd derivative of the analytic secant function vanishes at zero. -/
theorem d_odd_zero (n : ℕ) : d (2 * n + 1) 0 = 0 := by
  apply d_eq_zero_of_odd
  omega

/-- The leading Taylor coefficient of `sec z * tan z ^ n` is one. -/
theorem d_diagonal (n : ℕ) : d n n = (n.factorial : ℝ) := by
  induction n with
  | zero => simpa using d_zero_zero
  | succ n ih =>
      rw [d_rec_succ, ih, d_vanish n (n + 2) (by omega)]
      simp [Nat.factorial_succ]

/-- The first positive secant number. -/
theorem d_two_zero : d 2 0 = 1 := by
  exact (recurrence_small_values d d_zero_zero d_zero_succ d_rec).1

/-- The second positive secant number. -/
theorem d_four_zero : d 4 0 = 5 := by
  exact (recurrence_small_values d d_zero_zero d_zero_succ d_rec).2.1

/-- The third positive secant number. -/
theorem d_six_zero : d 6 0 = 61 := by
  exact (recurrence_small_values d d_zero_zero d_zero_succ d_rec).2.2

end SecantProof.Secant
