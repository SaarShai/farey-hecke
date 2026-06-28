# Veech slope-gap bridge — consolidated record (2026-06-27)

**Verdict: DEAD as a source of a new fact.** The transversals *do* correspond (same
horocycle Poincaré section — real but entirely **owned** by ACL 2013 + Taha 2018). The
headline numeric bridge **X(q) = 1/λ³ = the Veech slope-gap hard edge is FALSE**: different
observable, opposite end of the distribution, no λ³-conjugacy. This **reproduces the repo's
prior FALSIFIED record** (bug_id 14, `code/xomega_normalization_proof.py`), it does not
overturn it.

---

## 1. The question

Both objects are Poincaré sections of the horocycle flow on H_q\SL(2,ℝ):

- **OURS:** the Taha G_q-BCZ cross-section (Rosen continued fractions for the Hecke
  triangle group G_q = (2,q,∞), λ = λ_q = 2cos(π/q)), with the gap-**product** observable
  P = a·b (genuine form P_gen = a(a+λb)/λ) and machine-verified support edge
  **X(q) = 1/λ_q³** (onset theorem, q = 5..21 in Lean).
- **VEECH:** the double-(2q+1)-gon translation surface (genus 2, stratum H(2)) whose Veech
  group is exactly H_q (Veech 1989). Its saddle-connection **slope-gap** distribution, the
  q = 5 case = the **golden L** computed by Athreya–Chaika–Lelièvre (ACL) 2013
  (arXiv:1308.4203).

**Bridge to test:** are these the *same* section, and does X(q) = 1/λ³ equal the Veech
slope-gap hard edge? **Cheap anchor:** does ACL's golden-L hard edge equal
X(5) = 1/φ³ ≈ 0.2360680?

---

## 2. Scout-pinned definitions + the q = 5 ACL anchor (web-verified from primary PDFs)

- **Surface / Veech group** (Veech 1989; Massart survey arXiv:2107.11581): double-(2n+1)-gon
  has Veech group = Hecke (2, 2n+1, ∞) = H_q with **q = 2n+1** (odd q). q = 5 ↔ n = 2 ↔
  double pentagon = **golden L**, λ_5 = 2cos(π/5) = φ = 1.6180339887.
  (ACL line 74, verbatim: "Γ = Δ(2,5,∞) … is the Veech group of the golden L.")
- **Section** (ACL Thm 3.1 = Taha Thm 2.2): identical chart g_{a,b} = [[a,b],[0,1/a]] on the
  identical domain, the **G_q-Farey triangle** T_q = {0 < a ≤ 1, 1 − λ_q·a < b ≤ 1}. At q = 5
  Taha's floor 1 − λa and ACL's floor 1 − aφ are the *same set*. Same first-return ("BCZ") map.
- **Roof / return time** (ACL, 3 pieces): Ω_1 R = 1/(a(a+b)); Ω_φ R = 1/(a(φ⁻¹a+b));
  Ω_∞ R = 1/(ab). "R is uniformly bounded below by 1."
- **ACL hard edge** (Remark 2, verbatim): "f(x) = 0 for 0 ≤ x ≤ 1." The slope-gap density's
  left edge of support is **x = 1** (the gap variable = the return time R; **min R = 1**),
  **NOT 0.236**. Tail ~ x⁻².
- **ACL non-differentiability** (Thm 1.1, verbatim): "seven points of non-differentiability,"
  located at {1, φ, φ², 4, φ³, 4φ, φ⁴}.

**Anchor answer:** 0.2360680 ≠ ACL's hard edge of 1. The proposed numeric anchor **FAILS**
as a direct match. The two sections correspond; the two edge *numbers* do not.

---

## 3. What the computation + structural work established

**Tooling** (plain python3 + numpy + mpmath; Sage / surface_dynamics absent and unnecessary —
the section is an explicit elementary piecewise map). Witness files under `code/veech_bridge/`.

### 3a. ACL golden-L (q = 5) reproduction — what is SOLID vs OVERSTATED

**SOLID (independently confirmed this session):**

- **Hard edge = 1.** Method B (our own super-level-area integral G(t) = P(gap ≥ t) over the
  three validated cells) gives G(t) = 1 for t ≤ 1, i.e. f = 0 on [0,1]. Section roof
  min R_q = 1.0 confirmed directly. (`acl_goldenL_validation.json`, `veech_roof_minR.json`)
- **Breakpoint locations** at powers of φ: {1, φ, φ², 4, φ³, 4φ, φ⁴} = {1.0, 1.618, 2.618,
  4.0, 4.236, 6.472, 6.854} — match ACL Thm 1.1.

**OVERSTATED — must be discounted (caught by adversarial audit, confirmed against the JSON):**

- **"7 non-diff points"**: Method A's own kink detector finds **6**, not 7 — t = φ² = 2.618
  reads `is_nondiff: false` (dleft ≈ dright ≈ −0.047). Locations match ACL; the *count* of 7
  was not independently reproduced. (`acl_goldenL_validation.json` lines 27–32, 62.)
- **"Suspension volume 3π²/10 to 1.6e-12"**: **UNSUBSTANTIATED.** No executable code computes
  ∫_Ω R da db. The phrase exists only in code comments and `VALIDATION_SUMMARY.json`. Treat as
  not done.
- **Method A (closed form)**: integrates to **1.073** (7% error), OCR-mangled Appendix-A bars;
  disagrees with Method B by 2–7% at interior points. Method B (geometric) is the only
  authoritative density computation; Method A is fragile.
- **Method C (Monte-Carlo on ACL's return map)**: **BROKEN.** min R ≈ 2e-11, 100% of samples
  below 1 — the OCR'd k-floor / (a',b') map diverges out of Ω. Validates nothing. The
  "three independent ways" and "orbit quantiles agree 2–6%" claims are **not** supported by
  the code (no quantile-vs-section comparison exists in any script).

**Net:** the *pipeline is trusted only for* the hard edge (= 1) and the breakpoint
*locations*. The volume check, the count-of-7, and the MC/quantile cross-checks are not real
and should not be cited as validation. **None of this changes the verdict** — the refutation
rests on exact algebra + owned literature (below), not on the ACL density reproduction.

### 3b. Per-q edge numbers (exact)

| q  | λ = 2cos(π/q)   | OURS: X(q) = 1/λ³ | VEECH: min R_q | match |
|----|-----------------|-------------------|----------------|-------|
| 5  | 1.6180339887    | **0.23606798**    | **1.0** (at corner (1,1)) | mismatch |
| 7  | 1.8019377358    | **0.17091519**    | **1.0**        | mismatch |
| 9  | 1.8793852416    | **0.15064425**    | **1.0**        | mismatch |
| 11 | 1.9189859472    | **0.14150918**    | **1.0**        | mismatch |

`1/X(q) = λ³`: q5 → 4.236068, q7 → 5.850855, q9 → 6.638156, q11 → 7.066679.
(`veech_roof_minR.json`, `bridge_compare.json`)

The **Veech hard edge is q-independent = 1** (universal no-small-gaps edge of
Athreya–Chaika; attained at the section corner (a,b) = (1,1) on the cusp branch). Our
1/λ³ is the cusp-**tip** value (a,b) → (1/λ, 0) of the **reciprocal** product observable.

### 3c. Structural (exact, sympy-checked) — WHY the edges cannot coincide

1. **Different observable.** Edge of P_gen = a(a+λb)/λ vs edge of the return-time R. On the
   cusp (Ω_∞) branch R = 1/(ab) and P = ab, so **R·P = 1** exactly. Reciprocal observables on
   one section — not related by any conjugation.
2. **Opposite ends.** X(q) = 1/λ³ is P at the cusp tip, where R = 1/(ab) → +∞ (the
   **largest-gap / Hall-ray** end). ACL's min R = 1 is the **smallest-gap** ess-inf, at an
   interior corner, not the cusp. So 1/X(q) = λ³ = sup R, the OPPOSITE extreme.
3. **λ³ conjugacy is impossible.** The diagonal D = diag(t, 1/t) matching the Hecke parabolic
   [[1,λ],[0,1]] to ACL's [[1,1],[0,1]] forces λt² = 1; it scales slope-gaps by **λ** (not λ²,
   not λ³). The old "1/λ²" script value and the asserted "λ³" bridge are both wrong: no
   diagonal conjugation produces λ³. The "X·λ³ = 1" alignment in `bridge_compare.json` is just
   the **tautology** X = 1/λ³, not a section-level identity.

### 3d. B(q) ≠ density piece-count — refuted

- B(7) = 3 vs the double-heptagon density's many more non-diff points (Al Assal et al. 2025
  state 13; the count was **not** web-confirmed this session, but B(q) ≠ it under any value).
- B(q) grows ~ (2 arcsin(1/3)/π)·q ≈ **0.216q**; the 2n-gon/heptagon non-diff counts grow
  ~ **2q** (Berman et al. Thm 1.3). Different growth rates ⇒ no correspondence.
- Only alignment is an accidental **3 = 3** at q = 5 (B(5) ≈ 3 vs ACL's 3 roof zones). B(q) is
  a **cluster length** (max run of consecutive sub-threshold P); the piece count is the **zone
  structure of the roof**. Genuinely different objects.

---

## 4. Adversarial verdict (real vs coincidence vs owned)

- **bridge_status: refuted** (confidence 0.86).
- **REAL:** the transversal correspondence (Taha T_q = ACL Ω at q = 5; same Taha section all
  odd q) and min R_q = 1. The exact algebra (R·P = 1, λ-scaling, sup-R vs min-R) is decisive
  **against** the edge identity.
- **COINCIDENCE:** "X·λ³ = 1" = the tautology X = 1/λ³, not a correspondence. Any 0.236-vs-1
  alignment is a manufactured normalization coincidence.
- **OWNED:** *everything real here is classical.* Section = ACL 2013 (q = 5) + Taha 2018
  (all q) + KSW 2021 (general method). min R = 1 no-small-gaps = Athreya–Chaika 2012.
  Veech group of double-(2q+1)-gon = H_q = Veech 1989. Arithmeticity {3,4,6} = Takeuchi 1977.
  X_Ω is normalization-fixed, lives in the trace field ℚ(cos π/q), and detects **nothing**
  beyond Takeuchi's classical λ²∈ℤ (prior PARTIAL verdict,
  `research_notes/Xomega_generalize_2026-06-14.md`).
- **Evidence defects** the adversary caught in the COMPUTE self-report (all confirmed against
  the JSON above): the 1.6e-12 volume cross-check is uncomputed; Method C is broken; the
  "2–6% orbit-quantile" agreement and "7 non-diff points" are not produced by the code. The
  "Pipeline TRUSTED" line in `VALIDATION_SUMMARY.json` is overstated — trust only edge = 1 and
  breakpoint locations.

---

## 5. Theorem to prove next?

**None.** The headline identity is false, so there is no bridge theorem to formalize. The only
true adjacent statements are **already proved elsewhere and not ours**:

- (Taha) the G_q section roof R_q satisfies min R_q = 1 — owned.
- (tautology) 1/X(q) = λ³ = the sup-side cusp value of R_q.

The only formalizable residue is the **negative** one-liner: *on the shared cusp branch
R = 1/P, hence the two support edges are reciprocal-observable extremes (min-R vs sup-R) and
cannot coincide.* That is a one-line exact identity, not a result worth Lean effort. The
"new fact" — X(q) = 1/λ³ as the Veech slope-gap hard edge transported by a transversal
identity — **does not exist**: the transversal identity is real but owned, and the specific
edge identity is false at the observable/end level. This is a **re-derivation** of the known
q = 5 case (ACL) + Taha's all-q machinery, not a new fact.

---

## 6. Witness files (all absolute)

Built this session under `/Users/za/Documents/farey-hecke/code/veech_bridge/`:

- `acl_goldenL.py` — ACL golden-L reproduction (Method A closed form, Method B geometric
  super-level-area integral [authoritative], Method C MC [broken]).
- `veech_slopegap_orbit.py` — direct Hecke-orbit Γ.(1,0) saddle-connection slope gaps.
- `veech_roof_minR.py` — min R_q from the Taha G_q section roof, q = 5,7,9,11 (all = 1).
- `bridge_compare.py` — normalization audit (reciprocal, λ, λ², λ³) vs X(q) = 1/λ³.
- `out/acl_goldenL_validation.json` — Method A finds 6/7 kinks; Method C broken (min R ≈ 2e-11).
- `out/veech_roof_minR.json`, `out/bridge_compare.json`, `out/veech_slopegap_orbit.json`.
- `out/VALIDATION_SUMMARY.json` — **caveat:** overstates (claims 7 points, 1.6e-12 volume,
  2–6% quantiles, "Pipeline TRUSTED"); discount those three claims per §3a/§4.

Prior record (consistent — this run reproduces, does not overturn):

- `/Users/za/Documents/farey-hecke/code/xomega_normalization_proof.py` — bug_id 14, the
  FALSIFIED λ³-conjugacy record.
- `/Users/za/Documents/farey-hecke/research_notes/Xomega_generalize_2026-06-14.md` — PARTIAL
  verdict (mechanism ports; X_Ω is not a new invariant; no arithmeticity detector).
- `/Users/za/Documents/farey-hecke/code/goal1_bcz_hecke_cluster.py`,
  `/Users/za/Documents/farey-hecke/code/goal1_onset_scan.py` — the Taha G_q section + P.

---

## 7. Recommendation

**The Veech bridge is DEAD — do not pursue or formalize.** It is a confirmed clean negative
that reproduces the repo's own prior falsification (bug_id 14): the two cross-sections are the
same horocycle Poincaré transversal (real, but entirely owned by ACL 2013 + Taha 2018 + KSW
2021), while the headline identity "X(q) = 1/λ³ = Veech slope-gap hard edge" is false at the
level of the observable (gap-product P vs return-time R, reciprocal R = 1/P on the cusp branch)
and the end of the distribution (our sup-R / Hall-ray cusp value vs ACL's min-R = 1 hard edge),
with no λ³ diagonal conjugacy to rescue it. The B(q) = piece-count correspondence is likewise
refuted (0.216q vs ~2q growth; only an accidental 3 = 3 at q = 5). The lone genuinely-new
framing — "1/λ³ = 1/sup R_q, a family-uniform largest-gap quantity on the shared section" — is
a relabeling, not an invariant (X_Ω is normalization-fixed, lives in ℚ(cos π/q), detects
nothing beyond Takeuchi's classical λ²∈ℤ). Per the FunSearch doctrine, redirect away from this
owned edge entirely; if anything nearby is still worth a novelty check it is the cluster-ceiling
growth law B(q) ~ 0.216q (a *different* object from the slope-gap piece count, still flagged
"novelty under test"), which must be checked against Berman's 2n-gon non-analyticity linear
bounds before any claim.
