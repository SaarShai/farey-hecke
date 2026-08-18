# Hejhal LNM 1001 Vol. 2, §7 — full extraction (source received from Koyama, 2026-08-17)

Source: scan pp. 568–600, banked at
`../lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf`
(sha256 b0f9a7001b10f5e0eae5e5aca85124c0a233256aa0e08b5c0f04720185a2b1e9).
Provenance: sent by Prof. Koyama 2026-08-17 in reply to the lane_p literature
request (Ask 1). This closes restart lever 1 of the 2026-08-17 pause point.

Ask 2 answer (verbatim effect): Koyama is NOT aware of any public circulation
of Hejhal's unpublished calculations cited by Garbin–Jorgenson Thm 5.7 —
"private notes or uncirculated preprints." **B3 explicit-constants recovery via
literature: CLOSED-NEGATIVE.** Any B3 constants must be re-derived, not looked
up.

---

## 1. What the scan contains

- p. 568–569: end of §6; §7 opens. Hecke group G_N = ⟨E, S^λ⟩, λ = 2cos(π/N),
  N ≥ 3, **N = ∞ allowed and G_∞ = theta group** (p. 569: "G_∞ corresponds to
  the theta group"). Conjugated model 𝒢_N = a(1/√λ) G_N a(√λ), generators Q_N, S;
  fundamental region 𝒟_N = {|x| < 1/2, |z| > 1/λ}. Eisenstein series E_N(z;s),
  scattering coefficient φ_N(s) with the Dirichlet-series formula (7.5):
  φ_N(s) = √π · Γ(s−1/2)/Γ(s) · Σ_{W∞∈[S]\𝒢_N/[S], c(W∞)≠0} |c|^{−2s}, Re s > 1.
- Lemma 7.1 (interior regularity): f(z;s) eigenfunction in z, holomorphic in s,
  |f| ≤ 1 ⇒ first derivatives bounded by geometry-only constants.
- Lemma 7.2: Σ_{T∈𝒢_N} (Im Tz)^{1+ε}/[1+|Tz|]^{2+2ε} ≤ C(ε), **C(ε) does NOT
  depend on N**.
- Lemma 7.3: 0 ≤ φ_N(1+ε) ≤ C₁(ε) (N ≥ 4, uses λ ≥ √2).
- Lemma 7.4: Im T(z) ≤ C₂(ε) for T ∈ 𝒢_N, c(T) ≠ 0, Im z ≥ ε; and |c(W∞)| has
  a positive lower bound independent of N.
- Lemma 7.5: |E_N(z;s) − y^s| ≤ C₅(ε)^σ for σ ≥ 1+ε, with the explicit chain
  C₄ = max[C(ε), C₃(ε)], C₅ = [1+C₄]³.
- Prop 7.6: E_N ⇒ E_∞ and φ_N ⇒ φ_∞ on compacta of H × {Re s > 1}
  (normal-families argument; the geometric input is 𝒟_∞ = ∪ 𝒟_N).
- Lemma 7.7: |φ_N(s)| ≤ C₆(ε) for 1/2 ≤ σ ≤ 3/2, |t| ≥ ε (uniform in N).
- **Prop 7.8: φ_N ⇒ φ_∞ on compacta of ℛ₁ = {Re s > 1/2} slit along [1/2,1]**
  (Vitali, from 7.6 + 7.7).
- Lemma 7.9: Green's-function log-integral bound with constant C₇ on the
  rectangle [0,1]×[−1,1] (note 88 refines the conformal-map step).
- Lemma 7.10: subharmonicity: ∬_{|z|<1} ln⁺|f| ≤ M ⇒ ln⁺|f(re^{iθ})| ≤
  2M/(1−r)² (fully explicit proof).
- **Theorem 7.11** (p. 577): given t₀ ∈ ℝ, 0 < δ < 1, the rectangle
  [1/2, 1/2+δ]×[t₀−δ, t₀+δ] contains ZEROS of φ_N(s) whenever N is
  sufficiently large (N < ∞).
- **Corollary 7.12** (p. 579): [1/2−δ, 1/2)×[t₀−δ, t₀+δ] contains POLES of
  φ_N(s) for N sufficiently large. "Proof. Trivial." (reflection φφ̄ ≡ 1).
  Attributed: "This result corresponds to Selberg[2, page 91 line 5]."
- Notes for Chapter Eleven (pp. 580–600), including: note 7 (three methods for
  λ₁ > 1/4 on PSL(2,ℤ): L₂ / triangle-minimax (Selberg 1951, rediscovered by
  Buser) / Maass method, with Selberg's Lemma 1A and its full proof); notes
  8–11 (λ₁ > 2.21 for PSL(2,ℤ) by the Maass–Siegel Bessel device; Weyl minimax
  upper bounds ρ₁ ≤ 9.76877 etc.); note 77 (λ₁ > 1/4 for Γ̂(N), 2 ≤ N ≤ 5,
  the N=5 case via the degree-1,3,3,4,5 representations of Γ̂(1)/Γ̂(5) with
  the explicit L_j table); **note 86: λ₁ > 1/4 for Hecke groups** (via note 8's
  triangle-group argument, p. 583); note 90: "See also: Venkov[7,8]" for 7.12.

This is the "positivity material" GJ-school papers cite: the λ₁ > 1/4
statements live in the chapter notes (7, 8, 77, 86), not in a "p. 160" — the
draft letter's page guess was wrong, Koyama sent the right thing.

## 2. The proof skeleton of Thm 7.11 (what we came for)

Contradiction structure, with every step tagged E (effective as printed) or
I (ineffective as printed):

1. [E] Assume φ_N ≠ 0 on R_δ = [1/2,1/2+δ]×[t₀±δ] along a subsequence 𝒮.
2. [E] |φ_N(1/2+it)| ≡ 1 (unitarity) + Schwarz reflection: φ_N extends to
   [1/2−δ, 1/2+δ]×[t₀±δ] with the functional identity (7.22)
   φ_N(1/2−h+it)·conj(φ_N(1/2+h+it̄)) ≡ 1.
3. [I] Prop 7.8 + **Hurwitz**: φ_∞ ≠ 0 on (1/2,1/2+δ)×(t₀±δ), hence
   inf_{N∈𝒮} |φ_N(1/2+δ/2+it₀)| > 0.   ← ineffective: no rate, no explicit inf.
4. [E] Lemma 7.9 applied to φ_N/C₆: sup over the segment of
   ∫ ln|C₆/φ_N| dt = O(1); with (7.22) this gives the two-sided area bound
   (7.23) ∬_B |ln|φ_N|| dσdt = O(1) on B = [1/2−δ/10, 1/2+δ/10]×[t₀±δ/2].
5. [E] Lemma 7.10: φ_N(s) = O(1) for |s−1/2−it₀| ≤ δ/15.
6. [I] **Vitali** (second use): φ_N ⇒ φ_∞ on |s−1/2−it₀| ≤ δ/20, so
   |φ_∞(1/2+it)| ≡ 1 on |t−t₀| ≤ δ/20.
7. [E] Contradiction with **equation (3.1)** — the explicit theta-group
   scattering coefficient (φ_∞ has poles at half the nontrivial zeta zeros;
   |φ_∞| ≢ 1 on any critical-line segment).

Ineffectivity is CONFINED to steps 3 and 6 — both are exactly "normal
families/Vitali convergence without a rate," and both would become effective
given one quantitative input:

> **(RATE)** an explicit bound |φ_N(s) − φ_∞(s)| ≤ ε(N) → 0 on a fixed
> compact of {Re s ≥ 1+ε} (or of the slit plane ℛ₁).

On Re s ≥ 1+ε both functions are the SAME shape of Dirichlet series (7.5) over
double cosets, and Hejhal's own footnote to Prop 7.6 says the mechanism is
geometric convergence 𝒟_∞ = ∪𝒟_N — cusp-neighborhood group elements match for
λ(N) close to 2 up to explicitly controllable tails (Lemmas 7.2–7.4 supply
N-uniform majorants, so dominated-convergence has an explicit modulus if one
tracks which c-values move). Steps 4–5 then transport the rate from Re s ≥ 1+ε
into the critical strip exactly as printed (7.9/7.10 constants explicit), and
step 7's contradiction becomes a computable defect: near a zeta zero ρ,
|φ_∞| deviates from 1 at an explicit rate, so |φ_N − φ_∞| < that deviation
forces a zero of φ_N. Output: an EXPLICIT N₀(δ, t₀) — i.e. effective onset.

## 3. Consequences for the LAW program

- **Architecture confirmed**: Thm 7.11/Cor 7.12 gives off-line
  scattering poles for all N ≥ N₀(δ,t₀) — with N₀ ineffective as printed.
  Our program = make N₀ explicit (the (RATE) lemma above) + certified finite
  base for q < N₀ (G₅ done, G₇ assembled, q=8..12 sweep mechanical). The two
  halves meet in the middle: this is now a CONCRETE two-sided pincer with one
  named missing lemma, not a search over routes.
- **λ=2 boundary**: Hejhal's device lives exactly at our λ=2 phase boundary
  (N→∞ = theta group; the contradiction (3.1) IS the ρ/2 Riemann-zero pole
  structure). The Fedosova-side obstruction we proved does not touch this
  route: (RATE) needs only Dirichlet-series comparison in Re s > 1, where
  Lemma 7.2's C(ε) is already N-independent.
- **Selberg attribution**: Cor 7.12 "corresponds to Selberg[2, p. 91 line 5]"
  — the GJ attribution chain is confirmed at the source; also Venkov[7,8]
  (note 90) is a new secondary lead we did not have.
- **Positivity**: λ₁ > 1/4 for ALL Hecke groups is note 86 (via the
  triangle-group Maass-method argument of note 8) — replaces our secondary-
  source citation; the v25/U3 hypotheses that referenced "Hejhal positivity"
  can now cite note 86 + note 8 directly.
- **B3**: dead as a literature item (Ask 2 negative). If B3 constants are ever
  needed, note 77's explicit L_j-table method (representation-theoretic
  Bessel bounds) is the closest reproducible template in print.

## 4. Next-step decomposition of (RATE) — the effectivization lane

R1. Enumerate the double-coset c-values of 𝒢_N vs 𝒢_∞ up to height H:
    identify the N-stable prefix (elements whose c is λ-polynomial and
    converges) and the tail; certify tail majorant from Lemma 7.2's proof
    (chapter 6 prop 5.1 with 𝒴 = {|z−2i| < 10⁻⁶}) — constants explicit.
R2. Explicit ε(N) on Re s = 1+ε: |φ_N − φ_∞| ≤ (prefix drift, mean-value in λ)
    + (two tails). Numerical sanity check against our even/odd builders at
    q = 5..21 before proving anything (we can MEASURE φ_N − φ_∞).
R3. Transport: redo steps 4–5 with (7.22) keeping all constants (C₆, C₇,
    2M/(1−r)²) explicit; produce the strip modulus.
R4. Defect at (3.1): explicit lower bound for 1 − |φ_∞(1/2+it)| deviation near
    t = γ₁/2 (first zeta zero), from the completed-zeta formula for the
    theta-group φ_∞.
R5. Assemble N₀(δ, t₀) at t₀ = γ₁/2; compare against certified base range.

Status: extraction complete; R1–R5 not started. LEDGER RULE applies: nothing
above claims a proved rate — §2's (RATE) sketch is a plan, not a lemma.

> **[SUPERSESSION 2026-08-18 audit-17]** "R1–R5 not started" was true on
> 2026-08-17 when this extraction was written. It is now stale: R1
> (`LAW_R1_COSET_STRUCTURE.md`), R2 (`LAW_R2_RATE_LEMMA_DRAFT.md`), R4
> (`LAW_R4_THETA_DEFECT.md`) and the M2 sub-gap
> (`LAW_M2_TAIL_MAJORANT_DRAFT.md`) all have work banked; see
> `plans/wayfinder/rh-goals/MAP.md`. R3 (transport) and R5 (assembly) remain
> not started. The LEDGER RULE above still binds — none of that work claims a
> proved rate, and all of it carries the 2026-08-18 referee corrections
> (`RATE_NOTEGRAPH_REFEREE_AUDIT.md`). Historical line retained, not
> rewritten.

## 5. Addendum 2026-08-17: Vol. 2 table of contents (second Koyama mail)

Koyama also sent the Vol. 2 ToC. Precise locations of the remaining literature
dependencies (not yet in hand; owner-gated follow-up targets):

- Ch. 11 §3 "The theta group", pp. 524–532 — contains eq. (3.1), the explicit
  φ_∞ that Thm 7.11's contradiction targets. Our φ_∞ (LAW_ANCHOR_T1_THETA) is
  independently derived; a cross-check vs Hejhal's printed (3.1) would harden
  R4. Priority: MEDIUM (R4 already numerically self-consistent).
- Ch. 6 §12 "Apriori bounds for φ(s), E(z;s;χ), φ_m(s)", pp. 149–166 — source
  of the 155(12.2) derivation behind Lemma 7.7's C₆ (gap M2's constant chain).
  Priority: HIGH if M2/R3 stall on making C₆ explicit.
- Appendix E "Some Estimates Related to Kloosterman Sums", pp. 665–710 —
  possible backup route for tail majorants (gap N3/M2). Priority: LOW.
- Ch. 6 §11 pp. 108–149 (analytic continuation of Eisenstein series) and ch. 6
  prop 5.1 (p. 27 "A useful estimate" — Lemma 7.2's proof template).

If a follow-up request is ever approved, ask for pp. 149–166 + 524–532 only.
