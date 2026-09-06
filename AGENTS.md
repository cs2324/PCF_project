# Instructions for Codex

## Project goal and current boundary

This repository implements recovery of characteristic functions of signature
coordinates from the unitary path characteristic function (PCF). Read
`README.md` before changing code.

The maintained package is `pcf_recovery/`. `general_cf.ipynb`, when present,
is an earlier prototype and is not the source of truth. The package is
currently complete through the `PathCharacteristicFunction`/`BrownianPCF`
query layer. The next planned module is coordinate moment recovery from
Proposition 1.

## Mathematical invariants

- Use the right-multiplicative convention `dY = Y M(dX)`. A
  left-multiplicative convention changes word order.
- Word letters are numbered `1, ..., d`; Python matrix indices are numbered
  `0, ..., k`.
- Keep the paper's notation: `M`, `M_I`, `m`, `M_dim`, `lifted_dim`, and
  `M_I^[m]` in prose and docstrings.
- The picker is
  `M_I(e_a) = sum_{r: i_r=a} (E_{r-1,r} - E_{r,r-1})`.
- The tensor lift is the sum of single-factor actions. Never replace it by
  `M(e_a)` tensor-powered $m$ times.
- With `k = len(I)` and `D = (k + 1)**m`, moment recovery uses degree `k*m`
  and entry `(0, D - 1)`:
  `mu_m = [t^(k*m)] Phi_X(t M_I^[m])[0, D - 1]`.
- A truncated moment series is not automatically the full characteristic
  function. State the analytic or exponential-integrability assumption when
  claiming equality with the infinite series.
- Brownian formulas use Stratonovich/geometric development. Brownian paths are
  not bounded-variation paths.
- PDE and known Brownian closed forms are independent validation targets. Do
  not use them to derive or reverse-engineer coefficients that the PCF method
  is intended to recover.
- State the Lévy-area convention explicitly: `pi_12 - pi_21` versus half of
  that quantity.

## Coding conventions

- Use SymPy matrices and exact arithmetic in `pcf_recovery/` and `tests/`. Do
  not introduce NumPy merely because the notebook prototype uses it.
- Pass matrix-valued maps through `LinearMap`; do not regress to bare lists of
  matrices in new package APIs.
- Preserve the current word-picker module filename. Some branches use
  `M_I.py`; others use `single_wordpicker.py`. Do not rename it without
  updating imports and tests deliberately.
- Keep process-specific PCF evaluation separate from general moment
  extraction.
- Public functions need meaningful docstrings stating purpose, inputs,
  outputs, dimensions, basis ordering, and the mathematical formula used.
- Distinguish path dimension `d`, word length `k`, moment order `m`, matrix
  dimension `M_dim`, and lifted dimension `lifted_dim`.
- Avoid unrelated refactors. Inspect the actual files and tests before editing
  because the user's local branch may be newer than an archived copy.

## Working style

- The user is learning both the mathematics and the code. For each new layer,
  first explain its mathematical input and output and how it maps to the
  existing classes. Then propose the minimal API and tests before implementing.
- Make one logical layer at a time. Do not jump from moment extraction to
  mixed linear combinations or optimisation in one change.
- Separate statements proved by the paper, Brownian-specific facts, current
  code behavior, and proposed extensions.
- If an exact theorem or equation is needed and its text is not in the
  repository, ask for or inspect the relevant PDF instead of guessing.

## Verification

From the repository root, run:

```bash
python -m pip install -r requirements.txt
python -m pytest tests -q
```

The archived PCF-layer snapshot has 49 passing tests. After edits:

- ensure pytest collects tests rather than reporting `no tests ran`;
- add tests for identities, dimensions, repeated letters, boundary cases, and
  invalid inputs;
- run the whole suite, not only the new test file;
- report the exact command and result;
- review the diff for stale API names and NumPy/SymPy mixing.

Do not call a mathematical layer complete merely because code executes.
Completion requires a formula-level test against a hand-computable case and,
when available, an independent Brownian benchmark.
