import SecantProof.Radial
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FinCases

noncomputable section

namespace SecantProof

namespace Horizontal
open MvPolynomial

abbrev Q := MvPolynomial (Fin 3) ℝ
def x : Q := X 0
def y : Q := X 1
def a : Q := X 2

def W1 (f : Q) : Q := pderiv 0 f - y * pderiv 2 f
def W2 (f : Q) : Q := pderiv 1 f + x * pderiv 2 f
def HH (f : Q) : Q := W1 (W1 f) + W2 (W2 f)

/-- Formal partial derivatives commute on every polynomial. -/
theorem pderiv_commute (i j : Fin 3) (p : Q) :
    pderiv i (pderiv j p) = pderiv j (pderiv i p) := by
  induction p using MvPolynomial.induction_on with
  | C c => simp [pderiv_C]
  | add p q hp hq => simp only [map_add, hp, hq]
  | mul_X p k hp =>
    by_cases hki : k = i <;> by_cases hkj : k = j <;>
      simp_all [pderiv_mul, pderiv_X, Pi.single_apply] <;> ring

/-- Cartesian expansion of the sum of squares of the two horizontal fields. -/
theorem HH_expansion (p : Q) :
    HH p = pderiv 0 (pderiv 0 p) + pderiv 1 (pderiv 1 p) +
      2 * (x * pderiv 1 (pderiv 2 p) - y * pderiv 0 (pderiv 2 p)) +
      (x ^ 2 + y ^ 2) * pderiv 2 (pderiv 2 p) := by
  have h20 := pderiv_commute 2 0 p
  have h21 := pderiv_commute 2 1 p
  simp [HH, W1, W2, pderiv_mul, x, y, Pi.single_apply, h20, h21]
  ring

def embed : Radial.P →ₐ[ℝ] Q :=
  aeval (fun i : Fin 2 => if i = 0 then x ^ 2 + y ^ 2 else a)

@[simp] theorem embed_X_zero : embed (X 0) = x ^ 2 + y ^ 2 := by simp [embed]
@[simp] theorem embed_X_one : embed (X 1) = a := by simp [embed]
@[simp] theorem embed_r : embed Radial.r = x ^ 2 + y ^ 2 := embed_X_zero
@[simp] theorem embed_a : embed Radial.a = a := embed_X_one
@[simp] theorem embed_C (c : ℝ) : embed (C c) = C c := by simp [embed]

theorem pderiv_embed (i : Fin 3) (p : Radial.P) :
    pderiv i (embed p) =
      pderiv i (x ^ 2 + y ^ 2) * embed (pderiv 0 p) +
        pderiv i a * embed (pderiv 1 p) := by
  induction p using MvPolynomial.induction_on with
  | C c => simp [pderiv_C]
  | add p q hp hq => simp only [map_add, hp, hq]; ring
  | mul_X p j hp =>
    fin_cases j <;>
      simp [pderiv_mul, hp, pderiv_X, Pi.single_apply] <;> ring

theorem pderiv_zero_embed (p : Radial.P) :
    pderiv 0 (embed p) = 2 * x * embed (pderiv 0 p) := by
  rw [pderiv_embed]
  simp [x, y, a, pderiv_pow, Pi.single_apply]

theorem pderiv_one_embed (p : Radial.P) :
    pderiv 1 (embed p) = 2 * y * embed (pderiv 0 p) := by
  rw [pderiv_embed]
  simp [x, y, a, pderiv_pow, Pi.single_apply]

theorem pderiv_two_embed (p : Radial.P) :
    pderiv 2 (embed p) = embed (pderiv 1 p) := by
  rw [pderiv_embed]
  simp [x, y, a, pderiv_pow, Pi.single_apply]

/-- Exact radial intertwining for every polynomial, not just monomials. -/
theorem HH_embed (p : Radial.P) : HH (embed p) = embed (Radial.H p) := by
  have h0 : pderiv 0 (2 : Q) = 0 := (pderiv 0).map_natCast 2
  have h1 : pderiv 1 (2 : Q) = 0 := (pderiv 1).map_natCast 2
  have h4 : embed (4 : Radial.P) = 4 := map_natCast embed 4
  simp [HH, W1, W2, Radial.H, pderiv_mul, pderiv_embed,
    pderiv_pow, x, y, a, Pi.single_apply, h0, h1, h4]
  ring

/-- Iterating the horizontal operator preserves the radial embedding. -/
theorem iterate_HH_embed (n : ℕ) (p : Radial.P) :
    (HH^[n]) (embed p) = embed ((Radial.H^[n]) p) := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [Function.iterate_succ_apply', ih, HH_embed, Function.iterate_succ_apply']

/-- The embedding sends the spatial origin to the radial origin. -/
theorem eval_zero_embed (p : Radial.P) :
    eval (fun _ : Fin 3 => (0 : ℝ)) (embed p) =
      eval (fun _ : Fin 2 => (0 : ℝ)) p := by
  induction p using MvPolynomial.induction_on with
  | C c => simp
  | add p q hp hq => simp only [map_add, hp, hq]
  | mul_X p j hp =>
    fin_cases j <;> simp [x, y, a]

/-- Origin values of the area-polynomial iterates reduce to radial iterates. -/
theorem eval_iterate_area_general (n m : ℕ) :
    eval (fun _ : Fin 3 => (0 : ℝ)) ((HH^[n]) (a ^ m)) =
      eval (fun _ : Fin 2 => (0 : ℝ)) ((Radial.H^[n]) (Radial.a ^ m)) := by
  have he : embed (Radial.a ^ m) = a ^ m := by simp
  rw [← he, iterate_HH_embed, eval_zero_embed]

theorem eval_iterate_area (m : ℕ) :
    eval (fun _ : Fin 3 => (0 : ℝ)) ((HH^[m]) (a ^ m)) =
      eval (fun _ : Fin 2 => (0 : ℝ)) ((Radial.H^[m]) (Radial.a ^ m)) :=
  eval_iterate_area_general m m

/-- The horizontal contraction is exactly the radial scalar `T 0 m`. -/
theorem eval_iterate_area_eq_T (m : ℕ) :
    eval (fun _ : Fin 3 => (0 : ℝ)) ((HH^[m]) (a ^ m)) = Radial.T 0 m := by
  rw [eval_iterate_area]
  simp [Radial.T]

end Horizontal
end SecantProof
