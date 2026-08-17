# V25 dispatch — what is NOT sent to Lean

Source: `research_notes/rh_goals_2026-08-14/lane_g/LAW_U3_TRANSPORT.md`
(the U3 obligation of `LAW_T2_DETERMINANT.md` §5.2), plus
`LAW_SH_EFFECTIVIZATION_SKELETON.md` §7 item 2, which names U3 as the
"Aristotle-able finite piece … textbook-shaped".

`U3Transport.lean` contains **only the algebraic implication chain**: order-of-
vanishing arithmetic for meromorphic germs, run against the Selberg functional
equation. Every analytic fact the chain consumes is carried as an explicit
hypothesis of the theorem that uses it. The following are therefore *skipped* —
they remain `CITATION` / `PROVED-on-paper` in the lane notes and are not claimed
by any Lean statement here.

## S1 — the Selberg functional equation `Z(1-s) = κ(s) Z(s)` itself

`CITATION(Teo, LMP 110 (2020) 61–82, Prop. 2.5 / Thm 2.2; arXiv:1901.07898v2)`,
for cofinite hyperbolic orbifolds with cusps **and** ramification points, with

```
kappa(s) = (-1)^{A/2} e^{C(2s-1)} phi(s)
           * prod_j prod_k [ sin(pi(s+k)/m_j) ]^{(m_j-2k-1)/m_j}
           * [ (2pi)^{2s-1} Gamma_2(s)^2 Gamma(1-s) / (Gamma_2(1-s)^2 Gamma(s)) ]^{|X|/2pi}
           * [ Gamma(3/2-s) / Gamma(s+1/2) ]^n .
```

Mathlib has no Selberg zeta function, no scattering matrix, no Barnes double
gamma `Γ₂`, and no trace formula. The equation enters the Lean file as the
hypothesis `hFE`, stated as an eventual equality on a punctured neighbourhood of
`s₀` (faithful to the branch choices in the fractional powers of `κ`).

## S2 — Lemma U3-B: the concrete factors of `κ` are units off `ℝ`

Proved factor by factor in `LAW_U3_TRANSPORT.md` §2.6 (the `sin`-powers, the
Barnes/`Γ` bracket and the parabolic `Γ`-ratio all have **real** divisors).
Formalizing it would need `Γ₂` and a branch-of-fractional-power theory. In Lean
it is the pair of hypotheses `hc : AnalyticAt ℂ c s₀`, `hc0 : c s₀ ≠ 0` on the
collected non-`φ` factor `c`. The *algebraic* consequence — a unit factor does
not move the order — **is** proved (`meromorphicOrderAt_eq_of_unit_factor`).

## S3 — Lemma U3-A: `Z_Γ` is holomorphic and zero-free on `Re s > 1/2`, `Im s ≠ 0`

Read off the 7-item divisor list of
`CITATION(Friedman–Jorgenson–Smajlović, LMP 111 (2021) art. 15, §2.5)`, or from
the absolutely convergent Euler product plus reality of the exceptional-eigenvalue
zeros. Needs the spectral theory of the Laplacian on `Γ\H`; absent from Mathlib.
Carried in Lean as `hZfree : meromorphicOrderAt Z (1 - s₀) = 0`.

## S4 — the identity `det Φ_θ = g² E`, `g = Λ(2s-1)/Λ(2s)`

`LAW_ANCHOR_T1_THETA.md` (DET), `PROVED` in the note by an explicit Eisenstein
computation for `Γ_θ`. The Lean file takes the *shape* `(Λ(2s-1)/Λ(2s))² · E`
as given and only computes its divisor. `E`'s zero/pole locations (`Re s = 1`
and `Re s = 0`, so `E` is a unit at `Re s = 1/4` and `Re s = 3/4`) enter as
`hE : AnalyticAt ℂ E s₀`, `hE0 : E s₀ ≠ 0`.

## S5 — the analytic facts about `Λ` and `ζ`

That `Λ(2s)` vanishes to order `m(ρ)` exactly at `2s = ρ`; that `Λ` is zero-free
off the critical strip; that `Λ`'s only poles are at `0, 1`; that `ρ₁` is a
*simple* zero `CITATION(van de Lune–te Riele–Winter; Odlyzko)`; and
`Re ρ < 1` (de la Vallée Poussin). None is asserted in Lean. The order of `Λ` at
the two argument points is a hypothesis (`hden_ord`, `hnum_ord`, `hnum0`,
`hden0`). Only the arithmetic consequence of `Re ρ₁ = 1/2` — the identity
`1 - conj(ρ/2) = (1+ρ)/2` — is proved (`conj_reflect_of_re_half`).

## S6 — the Hurwitz / Vitali step of `(T2′)` and everything `q`-uniform

`LAW_T2_DETERMINANT.md` §3.2, and obligations U1, U2b, U5. Out of scope: U3 is
consumed **once, at the anchor `Γ_θ`**, and the `q`-side is produced by Hurwitz,
not by this transport (`LAW_U3_TRANSPORT.md` §4). Nothing here touches U1.

## S7 — the outstanding library checks V1–V3

`LAW_U3_TRANSPORT.md` §6: Hejhal LNM 1001 vol. II Ch. X Thm 5.3 p. 498 (V1),
Venkov 1990 p. 49 (V2), Teo journal numbering + branch convention (V3). These
are human library errands, not formalizable, and none of them blocks the
algebraic chain sent here.
