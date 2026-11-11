import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.Factorial.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Lean.Elab.Tactic.Omega

/-! Strong induction for the mixed-monomial contraction. The abstract
recurrences used here are proved for the concrete operators and ordinary
derivatives in the accompanying modules and instantiated in Main. -/

noncomputable section
namespace SecantProof.Induction

def scale (k l : ℕ) : ℝ :=
  (2 : ℝ) ^ (2 * k + l) * (k.factorial : ℝ) * (l.factorial : ℝ)

theorem scale_left (k l : ℕ) (hk : 0 < k) :
    4 * (k : ℝ) ^ 2 * scale (k - 1) l = scale k l * (k : ℝ) := by
  obtain ⟨j, rfl⟩ := Nat.exists_eq_succ_of_ne_zero (Nat.ne_of_gt hk)
  simp only [Nat.succ_sub_one, scale, Nat.factorial_succ, Nat.cast_mul,
    Nat.cast_add, Nat.cast_one, Nat.cast_succ]
  have he : 2 * (j + 1) + l = (2 * j + l) + 2 := by omega
  rw [he, pow_add]
  ring

theorem scale_right (k l : ℕ) (hl : 2 ≤ l) :
    (l : ℝ) * ((l - 1 : ℕ) : ℝ) * scale (k + 1) (l - 2) =
      scale k l * ((k + 1 : ℕ) : ℝ) := by
  obtain ⟨j, rfl⟩ := Nat.exists_eq_add_of_le hl
  have he : 2 * (k + 1) + (2 + j - 2) = 2 * k + (2 + j) := by omega
  have hs : 2 + j - 1 = j + 1 := by omega
  simp only [scale, he, hs]
  have ht : 2 + j - 2 = j := by omega
  rw [ht]
  have hf : (2 + j).factorial = (j + 2) * (j + 1) * j.factorial := by
    rw [show 2 + j = j + 1 + 1 by omega]
    simp only [Nat.factorial_succ]
    ring
  rw [hf, Nat.factorial_succ]
  push_cast
  ring

theorem mixed_induction
    (T d : ℕ → ℕ → ℝ) -- T_{k,l} and d_{n,k}
    (hT0 : T 0 0 = 1)
    (hTrec : ∀ k l, 0 < k + l →
      T k l = (if k = 0 then 0 else 4 * (k : ℝ) ^ 2 * T (k - 1) l) +
        (if l < 2 then 0 else (l : ℝ) * ((l - 1 : ℕ) : ℝ) * T (k + 1) (l - 2)))
    (hd0 : d 0 0 = 1)
    (hdrec : ∀ n k, d (n + 1) k =
      (if k = 0 then 0 else (k : ℝ) * d n (k - 1)) +
        ((k + 1 : ℕ) : ℝ) * d n (k + 1))
    (hdvanish : ∀ n k, n < k → d n k = 0)
    (k l : ℕ) : T k l = scale k l * d (k + l) k := by
  have main : ∀ N k l : ℕ, k + l = N → T k l = scale k l * d N k := by
    intro N
    induction N using Nat.strong_induction_on with
    | h N ih =>
      intro k l he
      by_cases hN : N = 0
      · have hk : k = 0 := by omega
        have hl : l = 0 := by omega
        subst k
        subst l
        subst N
        simp [hT0, hd0, scale]
      have hpos : 0 < k + l := by omega
      have hfirst :
          (if k = 0 then 0 else 4 * (k : ℝ) ^ 2 * T (k - 1) l) =
          scale k l * (if k = 0 then 0 else (k : ℝ) * d (N - 1) (k - 1)) := by
        by_cases hk : k = 0
        · simp [hk]
        simp only [if_neg hk]
        have hi : (k - 1) + l < N := by omega
        have hj : (k - 1) + l = N - 1 := by omega
        rw [ih ((k - 1) + l) hi (k - 1) l rfl, hj]
        calc
          4 * (k : ℝ) ^ 2 * (scale (k - 1) l * d (N - 1) (k - 1)) =
              (4 * (k : ℝ) ^ 2 * scale (k - 1) l) * d (N - 1) (k - 1) := by ring
          _ = (scale k l * (k : ℝ)) * d (N - 1) (k - 1) := by
              rw [scale_left k l (by omega)]
          _ = scale k l * ((k : ℝ) * d (N - 1) (k - 1)) := by ring
      have hsecond :
          (if l < 2 then 0 else (l : ℝ) * ((l - 1 : ℕ) : ℝ) * T (k + 1) (l - 2)) =
          scale k l * (((k + 1 : ℕ) : ℝ) * d (N - 1) (k + 1)) := by
        by_cases hl : l < 2
        · have hv : d (N - 1) (k + 1) = 0 := hdvanish _ _ (by omega)
          simp [hl, hv]
        simp only [if_neg hl]
        have hi : (k + 1) + (l - 2) < N := by omega
        have hj : (k + 1) + (l - 2) = N - 1 := by omega
        rw [ih ((k + 1) + (l - 2)) hi (k + 1) (l - 2) rfl, hj]
        calc
          (l : ℝ) * ((l - 1 : ℕ) : ℝ) *
              (scale (k + 1) (l - 2) * d (N - 1) (k + 1)) =
              ((l : ℝ) * ((l - 1 : ℕ) : ℝ) * scale (k + 1) (l - 2)) *
                d (N - 1) (k + 1) := by ring
          _ = (scale k l * ((k + 1 : ℕ) : ℝ)) * d (N - 1) (k + 1) := by
              rw [scale_right k l (by omega)]
          _ = scale k l * (((k + 1 : ℕ) : ℝ) * d (N - 1) (k + 1)) := by ring
      have hd := hdrec (N - 1) k
      rw [show N - 1 + 1 = N by omega] at hd
      rw [hTrec k l hpos, hfirst, hsecond, ← mul_add, ← hd]
  exact main (k + l) k l rfl

end SecantProof.Induction
