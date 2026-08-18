# V27 dispatch note — M1 word-level refutation + N4 counting

Dispatched 2026-08-17. Project `0103cfab-38d0-4f6c-85cd-bbe662392f96`,
task `b495c784-1a96-4e2f-a520-0b1c67ee15a5`. File: `RateCoreII.lean`
(6 sorry'd theorems). Local syntax pre-check PASSED before submission
(`lake env lean RateCoreII.lean` against the v26 .lake cache: 6
declaration-uses-sorry warnings, exit 0) — closes the v26 workflow gap.

## Content

1. `c_depth_three`: c_λ([n,m]) = λ(nmλ²−1) — hand-derived, numerically
   verified at λ = 2cos(π/7), λ = 2 (this session).
2. `wordLimitMap_not_injective_depth_three`: REFUTATION TARGET for the v26
   axiom `wordLimitMap_injective_on_matched` at K = 3 (witness [1,2] vs
   [2,1] — same c at every Hecke λ). [CORRECTION 2026-08-18 audit-1: this
   dispatch note previously said "machine-certified REFUTATION"; wrong tense
   — at dispatch time all 6 theorems are live sorrys. Status: hand-derived
   and numerically checked (3 λ values); syntax-checked dispatch; harvest
   and independent sorry-free rebuild PENDING. Nothing in this file is
   machine-verified until the harvest note says so.] Consequence IF
   certified: M1 must be stated at the coset/invariant level, not the word
   level; the v26 axiom (used by nothing) would be refuted-as-stated. Note
   the collision is for the c-ONLY word proxy: the lower-right entries
   differ (d = −nλ vs −mλ), so the R1 invariant (c, d mod c) may still
   separate these as cosets — see the R2 [CORRECTION v27] block.
3. `c_depth_three_injective_in_product`: the repaired depth-3 statement —
   the surviving invariant is the product n·m.
4. `two_smul_wordMatrix_two_integral` + `c_two_even`: λ=2 integrality
   backbone (2·wordMatrix integral; c-values even integers) — the bridge
   toward Hejhal Vol.2 Ch.11 §3 Lemma 3.1's integer pairs.
5. `theta_coset_count`: #{d : 0 ≤ d < 2c, gcd(c,d)=1, c+d odd} = φ(2c) —
   the N4 multiplicity constant, now sourced to the printed Lemma 3.1
   (received from Koyama 2026-08-17).

## Ledger

Nothing here claims the (RATE) lemma. M1-general remains OPEN — this
dispatch is expected to REFUTE its v26 word-level formulation and pin the
correct invariant; the coset-level M1 (the real gap) still needs a
normal-form/geodesic argument. Harvest on completion; watcher armed.
