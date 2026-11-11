import Mathlib.Algebra.MvPolynomial.PDeriv
import Mathlib.Algebra.MvPolynomial.CommRing
import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

namespace SecantProof.Radial

noncomputable section

open MvPolynomial

abbrev P := MvPolynomial (Fin 2) ℝ

def r : P := X 0
def a : P := X 1

def H (f : P) : P :=
  4 * r * pderiv 0 (pderiv 0 f) + 4 * pderiv 0 f + r * pderiv 1 (pderiv 1 f)

def T (k l : ℕ) : ℝ :=
  MvPolynomial.eval (fun _ => 0) ((H^[k + l]) (r ^ k * a ^ l))

@[simp] private theorem coord01 : (0 : Fin 2) ≠ 1 := by decide
@[simp] private theorem coord10 : (1 : Fin 2) ≠ 0 := by decide

theorem H_add (f g : P) : H (f + g) = H f + H g := by
  simp only [H, map_add]
  ring

theorem H_C_mul (q : ℝ) (f : P) : H (C q * f) = C q * H f := by
  simp only [H, pderiv_C_mul]
  ring

@[simp] theorem H_zero : H 0 = 0 := by simp [H]

theorem iterate_add (n : ℕ) (f g : P) :
    (H^[n]) (f + g) = (H^[n]) f + (H^[n]) g := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [Function.iterate_succ_apply', ih, H_add]

theorem iterate_C_mul (n : ℕ) (q : ℝ) (f : P) :
    (H^[n]) (C q * f) = C q * (H^[n]) f := by
  induction n with
  | zero => rfl
  | succ n ih =>
    simp only [Function.iterate_succ_apply', ih, H_C_mul]

@[simp] theorem iterate_zero (n : ℕ) : (H^[n]) 0 = 0 := by
  induction n with
  | zero => rfl
  | succ n ih => simp only [Function.iterate_succ_apply', ih, H_zero]

theorem pd0_monomial (k l : ℕ) :
    pderiv 0 (r ^ k * a ^ l) = C (k : ℝ) * r ^ (k - 1) * a ^ l := by
  simp [r, a, pderiv_mul, pderiv_pow, Pi.single_apply]
  ring

theorem pd1_monomial (k l : ℕ) :
    pderiv 1 (r ^ k * a ^ l) = C (l : ℝ) * r ^ k * a ^ (l - 1) := by
  simp [r, a, pderiv_mul, pderiv_pow, Pi.single_apply]
  ring

theorem pd0_twice_monomial (k l : ℕ) :
    pderiv 0 (pderiv 0 (r ^ k * a ^ l)) =
      C ((k : ℝ) * ((k - 1 : ℕ) : ℝ)) * r ^ (k - 2) * a ^ l := by
  rw [pd0_monomial, mul_assoc, pderiv_C_mul, pd0_monomial]
  simp only [Nat.sub_sub, one_add_one_eq_two, map_mul]
  ring

theorem pd1_twice_monomial (k l : ℕ) :
    pderiv 1 (pderiv 1 (r ^ k * a ^ l)) =
      C ((l : ℝ) * ((l - 1 : ℕ) : ℝ)) * r ^ k * a ^ (l - 2) := by
  rw [pd1_monomial, mul_assoc, pderiv_C_mul, pd1_monomial]
  simp only [Nat.sub_sub, one_add_one_eq_two, map_mul]
  ring

theorem H_monomial (k l : ℕ) :
    H (r ^ k * a ^ l) =
      (if k = 0 then 0 else C (4 * (k : ℝ) ^ 2) * r ^ (k - 1) * a ^ l) +
      C ((l : ℝ) * ((l - 1 : ℕ) : ℝ)) * r ^ (k + 1) * a ^ (l - 2) := by
  unfold H
  rw [pd0_twice_monomial, pd0_monomial, pd1_twice_monomial]
  simp only [Nat.sub_sub, one_add_one_eq_two, map_mul, map_pow, map_ofNat,
    map_natCast]
  cases k with
  | zero =>
    simp
    ring
  | succ k =>
    cases k with
    | zero =>
      simp [pow_succ]
      ring
    | succ k =>
      simp [Nat.succ_eq_add_one, pow_succ]
      ring

theorem T_zero_zero : T 0 0 = 1 := by simp [T]

theorem eval_iterate_scaled_monomial (n k l : ℕ) (c : ℝ) :
    MvPolynomial.eval (fun _ => 0) ((H^[n]) (C c * r ^ k * a ^ l)) =
      c * MvPolynomial.eval (fun _ => 0) ((H^[n]) (r ^ k * a ^ l)) := by
  rw [mul_assoc, iterate_C_mul, map_mul, eval_C]

theorem T_rec (k l : ℕ) (h : 0 < k + l) :
    T k l =
      (if k = 0 then 0 else 4 * (k : ℝ) ^ 2 * T (k - 1) l) +
      (if l < 2 then 0 else (l : ℝ) * ((l - 1 : ℕ) : ℝ) * T (k + 1) (l - 2)) := by
  have hn : k + l = (k + l - 1) + 1 := by omega
  change MvPolynomial.eval (fun _ => 0) ((H^[k + l]) (r ^ k * a ^ l)) = _
  rw [hn, Function.iterate_succ_apply, H_monomial, iterate_add, map_add]
  congr 1
  · by_cases hk : k = 0
    · simp [hk]
    · simp only [if_neg hk]
      rw [eval_iterate_scaled_monomial]
      have hdegree : k - 1 + l = k + l - 1 := by omega
      simp only [T, hdegree]
  · by_cases hl : l < 2
    · have hlcases : l = 0 ∨ l = 1 := by omega
      rcases hlcases with rfl | rfl <;> simp
    · simp only [if_neg hl]
      rw [eval_iterate_scaled_monomial]
      have hdegree : k + 1 + (l - 2) = k + l - 1 := by omega
      simp only [T, hdegree]

end

end SecantProof.Radial
