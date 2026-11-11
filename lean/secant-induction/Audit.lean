import SecantProof

/-! Audit the public theorems and show the complete final signatures. -/

#eval Lean.versionString
#eval Lean.githash

#check @SecantProof.mixed_contraction
#check @SecantProof.radial_contraction
#check @SecantProof.horizontal_contraction

#print axioms SecantProof.Radial.H_add
#print axioms SecantProof.Radial.H_C_mul
#print axioms SecantProof.Radial.H_zero
#print axioms SecantProof.Radial.iterate_add
#print axioms SecantProof.Radial.iterate_C_mul
#print axioms SecantProof.Radial.iterate_zero
#print axioms SecantProof.Radial.pd0_monomial
#print axioms SecantProof.Radial.pd1_monomial
#print axioms SecantProof.Radial.pd0_twice_monomial
#print axioms SecantProof.Radial.pd1_twice_monomial
#print axioms SecantProof.Radial.H_monomial
#print axioms SecantProof.Radial.T_zero_zero
#print axioms SecantProof.Radial.eval_iterate_scaled_monomial
#print axioms SecantProof.Radial.T_rec
#print axioms SecantProof.Induction.scale_left
#print axioms SecantProof.Induction.scale_right
#print axioms SecantProof.Induction.mixed_induction
#print axioms SecantProof.Secant.d_zero_zero
#print axioms SecantProof.Secant.f_zero
#print axioms SecantProof.Secant.d_zero_succ
#print axioms SecantProof.Secant.d_secant
#print axioms SecantProof.Secant.f_zero_hasDerivAt
#print axioms SecantProof.Secant.f_succ_hasDerivAt
#print axioms SecantProof.Secant.f_contDiffAt
#print axioms SecantProof.Secant.d_rec_zero
#print axioms SecantProof.Secant.d_rec_succ
#print axioms SecantProof.Secant.d_rec
#print axioms SecantProof.Secant.d_vanish
#print axioms SecantProof.Secant.d_eq_zero_of_odd
#print axioms SecantProof.Secant.d_odd_zero
#print axioms SecantProof.Secant.d_diagonal
#print axioms SecantProof.Secant.d_two_zero
#print axioms SecantProof.Secant.d_four_zero
#print axioms SecantProof.Secant.d_six_zero
#print axioms SecantProof.Horizontal.pderiv_commute
#print axioms SecantProof.Horizontal.HH_expansion
#print axioms SecantProof.Horizontal.embed_X_zero
#print axioms SecantProof.Horizontal.embed_X_one
#print axioms SecantProof.Horizontal.embed_r
#print axioms SecantProof.Horizontal.embed_a
#print axioms SecantProof.Horizontal.embed_C
#print axioms SecantProof.Horizontal.pderiv_embed
#print axioms SecantProof.Horizontal.pderiv_zero_embed
#print axioms SecantProof.Horizontal.pderiv_one_embed
#print axioms SecantProof.Horizontal.pderiv_two_embed
#print axioms SecantProof.Horizontal.HH_embed
#print axioms SecantProof.Horizontal.iterate_HH_embed
#print axioms SecantProof.Horizontal.eval_zero_embed
#print axioms SecantProof.Horizontal.eval_iterate_area_general
#print axioms SecantProof.Horizontal.eval_iterate_area
#print axioms SecantProof.Horizontal.eval_iterate_area_eq_T
#print axioms SecantProof.mixed_contraction
#print axioms SecantProof.radial_contraction
#print axioms SecantProof.horizontal_contraction
