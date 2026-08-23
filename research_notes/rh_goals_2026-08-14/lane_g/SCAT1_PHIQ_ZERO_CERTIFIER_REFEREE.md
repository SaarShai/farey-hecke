# SCAT-1 Cold Referee Report — installed verbatim

Installation note (orchestrator, 2026-08-23 06:52Z): the referee seat is
read-only; this report is installed verbatim from the referee's inline
return. Verdict: PROMOTABLE-WITH-CORRECTIONS. Corrections applied as the
dated append-only §8 block in SCAT1_PHIQ_ZERO_CERTIFIER_SOL.md.

---

## Verdict: **PROMOTABLE-WITH-CORRECTIONS**

No blocking mathematical error. Prop. 2.1 (both proofs), Lemma 3.1 (all three steps, including the conjugation/reflection bookkeeping), and the box reflection are **correct** and I reproduced every numeric receipt in §2.2 and §3.4 bit-for-bit. The defects are rounding-direction errors in a certificate context, three false planning numerics in §5.1b/§5.2, an overstated equivalence in §5.1, and disclosure/LEDGER-RULE violations.

File: `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/SCAT1_PHIQ_ZERO_CERTIFIER_SOL.md`

---

## What CONFIRMS

**Claim 1 — Phase-1 infeasibility: CONFIRMED.**
- q=3 residue anchor exact: `Res_{s=1}φ_3 = √π Γ(½)/Γ(1)·(½)/ζ(2) = 0.954929658551372`; `3/π = 0.954929658551372`. Matches the note's 12 digits.
- Constant cross-check the note does *not* run, and it works: for PSL(2,Z), `D_3 = ζ(2s−1)/ζ(2s)`, `d(c)=φ(c)`, `Σ_{c≤X}φ(c) ~ 3X²/π²`, and `A_pred = 1/(π·vol) = 1/(π·π/3) = 3/π² = 0.303963550927013`. Exact agreement — proof (b)'s constant is right.
- Area check: Δ(2,q,∞) has area `2π(1−½−1/q) = π(1−2/q)` ✓ (q=3 → π/3).
- Landau step: the contradiction argument is valid *without* Landau (a Dirichlet series is holomorphic in its half-plane of convergence; uniqueness of continuation kills the pole). Landau is invoked superfluously.
- §2.2 table reproduced from `law_probes/r1_coset_enum_complete_X50.json` — every N(X), slope, A_pred, A_meas, rel-dev and all three σ-partial-sum rows match to the printed digit (q=5 slope 1.9909, q=8 1.9080, q=12 2.0650, θ 1.9541; A_meas 0.1712/0.1320/0.1272/0.1052).

**Claim 2 — Lemma 3.1: CONFIRMED, and the brief's premise is the trap.** The brief says the functional equation gives a zero "at `1−s̄`". It does not. From `φ(s)φ(1−s)=1` and a pole of order m at `s*`, put `w=1−s`, so `s−s* = −(w−(1−s*))`: `φ(w) = C^{−1}(−1)^m (w−ρ)^m(1+o(1))` with `ρ = 1−s*`. The note's `ρ := 1−s*` is **correct**; `1−s̄*` is the *conjugate* zero, obtained separately via A3 — which the note also states correctly. Steps (i)/(iii) are correctly hypothesised (the note itself flags in S1(iv) that `Re s* > 0` should be written explicitly — agreed, and it is not in the Lemma's hypothesis list as written).

**Claim 3 — the reflected box: interval arithmetic CONFIRMED, margin rounding REFUTED.** See defect 1.

**§3.4 numerics — CONFIRMED.** All seven `|sin|` values reproduce (e.g. `|sin(π(ρ+0)/2)| = 4273.532083`, `|sin(π(ρ+1)/2)| = 4273.532066` — the note's identical printed `4273.5321` is correct rounding, not a copy-paste).

---

## Defect list

**1. [MAJOR] Both §3.2 "rounded DOWN" quantities are rounded UP — they overstate the certificate.**
Exact values from the parent box `0.4538951800749447 ± 1e-6`:
```
margin  (Re ρ − 1/2) = 0.0461038199250553   note prints "rounded DOWN: 0.04610381993"
                                            true round-DOWN  = 0.04610381992
dist to Re=1         = 0.4538941800749447   note prints "rounded DOWN: 0.4538941801"
                                            true round-DOWN  = 0.4538941800
```
Both are round-to-nearest, i.e. UP. This is precisely the erratum the parent already carries (`THEOREM_G5_OFFLINE_ASSEMBLY.md:197-199`: *"a previous quote 3.43787e-8 rounded up, overstating"*). The 7-digit form `≥ 0.0461038` in CLAIM 3.2 and §0 is fine; the 10/11-digit forms are not. Missed because the author derived them by printing, not by directed rounding.

**2. [MAJOR] §5.1b/§5.2: the fallback-candidate separations are false for two of three.**
```
pin        ΔRe vs 0.4538952   box widths (2e-6)   >0.015?   >1e4 bw?   |t|
0.4105437     0.0433514            21676           yes        yes      7.820
0.4470830     0.0068122             3406            NO         NO     12.080
0.4690553     0.0151601             7580           yes         NO     12.786
```
(sources: `KS_GATE_REPORT.md:4,6,7`). The note asserts all three are "separated from the flagship by `> 0.015`, i.e. `> 10⁴` box widths." Both bounds fail for `0.4470830`; the `>10⁴ box widths` claim also fails for `0.4690553` on the natural full-width reading. Separately, §5.2 calls them "milder … closer in `|t|` to the flagship": two of three have `|t| = 12.08, 12.79`, i.e. **farther** than `s_2`'s 10.56 — and by the note's own B2 logic, rising `|t|` is a degrader. The stated fallback rationale is therefore backwards for the two candidates it most relies on.

**3. [MAJOR] §5.1's "the two open items are the same item" is an implication, not an equivalence.**
`NO_VERTICAL_LINE_COROLLARY.md` item 4 asks for two certified pins at distinct real parts to exclude an *arbitrary* vertical line for `Λ°`. NOGO-OPEN-1 needs two `φ_5` zeros with `1/2 < Re ρ < 1`. The transfer works only if **both** pins are nonreal, off-line, **and in `0 < Re s < 1/2`** — a pin certified on/at `Re = 1/2` would close the vertical-line item while reflecting to `Re ρ = 1/2`, outside NOGO-OPEN-1's open interval. The reverse direction (NOGO closure ⇒ vertical-line closure) additionally needs Lemma 3.1 run backwards (φ-zero at ρ ⇒ φ-pole at `1−ρ` ⇒ Z-zero), which is never written. Verdict: **not airtight** as an equivalence; correct as a one-way implication under an extra hypothesis. (The one leg I checked and that *does* hold: `φ_q ∈ 𝔐(A)` for all finite `q ≥ 3` is banked as `NOGO_METATHEOREM_SOL.md:249` Lemma 3.2.)

**4. [MAJOR] "Adds no dependency the declared G_5 theorem does not already carry" is true-but-misleading, and understates by one item.**
`THEOREM_G5_OFFLINE_ASSEMBLY.md` link 7 is *interpretive*: the parent's theorem statement ("`Z_S` has a zero `s*` with |Re−…|≤1e-6") is rigorous **without** link 7, which only labels `s*` a resonance. Claim 3.2 is *entirely* load-bearing on it. Promoting a downstream interpretation citation to a load-bearing hypothesis is a real change in dependency posture, not a null one. Additionally, link 7 asserts no **multiplicity** matching, which Lemma 3.1's "order `m`" does require (the existence conclusion does not, so this is confined to the Lemma's strength). Also, link 7 says "resolvent/scattering matrix"; Lemma 3.1 needs the scalar `φ` specifically.

**5. [MAJOR] B7 convention gate disclosed in exactly one place, quoted in four.** The brief requires B7 wherever box endpoints appear. It appears only in §5.1b. It is **absent** at: §0 V2 (`Re ρ ≥ 0.5461038`, line 33), the CLAIM 3.2 box (§3.2, lines 250-254), the §6 ledger row (`Certified φ_5 zero at Re ρ ≥ 0.5461038`, line 463), and the §5.1 blocker (`0.4538952`, line 355). Source confirmed: `SECOND_PIN_PREP.md:174-177` — *"An independent reimplementation placed a G_5 pin at 0.4332 vs 0.4539 — the even-sector convention gate is not closed."*

**6. [MAJOR] LEDGER-RULE: "certified" / "already in the bank" against a CONJECTURAL claim.** The **title** says "a certified zero of the scattering determinant φ_q itself"; §0 V2 says the artifact is "**ALREADY IN THE BANK**" and NOGO remark 2 is "too pessimistic"; the §6 ledger row reads "**Certified** `φ_5` zero … **CLAIM 3.2 — UNREFEREED / CONJECTURAL**" — self-contradictory in one cell. The most-caveated available phrasing is the §4 table's honest "Superseded, **conditionally**". §0 and the title must match §4, not lead it.

**7. [MINOR] `Re s ≤ 1` divergence is overstated on the boundary line.** Prop. 2.1's "diverges at every `s` with `Re s ≤ 1`" holds for `Re s < 1` and for real `s = 1`; a generalized Dirichlet series with `σ_c = 1` may converge at `1+it`, `t ≠ 0`. Immaterial to the target strip, but it is a stated proposition.

**8. [MINOR] Blocker misattribution in §5.1b.** The bullet labelled "B2 (hard)" folds in the `4.5e-6` not-freezable finding, which is **B1** in `SECOND_PIN_PREP.md:146` ("Box not yet freezable"); B2 is the constants degradation (`:152`). The §6 ledger then names only "B2 and B7", losing B1 as a distinct blocker.

**9. [MINOR] §3.4's "Independent of §3.3" is false.** Route 2's step "`Z(ρ) ≠ 0`: in `Re s > 1/2` the only `Z`-zeros are the real small-eigenvalue parameters in `(1/2,1]`" is itself a statement about the `Z_Γ` divisor — the same classical theorem family as §3.3. Route 2 is a *different slice* of the same citation, not an independent check.

**10. [MINOR] Unsourced/mispathed citation.** `BOX_TO_THEOREM_UPGRADE_PLAN.md` is cited twice with no lane; it lives in **lane_f**, not lane_g, and is absent from §1 "What was read". Its content checks out: q=7 margin `2.4128527e-6` at N=256 confirmed against `lane_f/F7_R3B_ASSEMBLY_RECEIPT.json:537` (`2.41285276269068356797…e-6`), and the q=8 "finite-sampled polygon winding only" characterization is verbatim correct (`:120-124,136`).

**11. [MINOR] Mandated prior-art citation omitted at the novelty claim.** `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:461-465` (2026-08-20 repair 2) mandates: *"Hejhal LNM 1001, Theorem 7.11 and Corollary 7.12 … prove zeros/poles of `φ_N` in any prescribed rectangle touching the critical line for all sufficiently large N. … Must be cited wherever novelty is framed."* §4's "Superseded" row frames novelty and does not cite it (q=5 is not covered by "large N", so the claim survives — but the disclosure is mandatory).

**12. [MINOR] Parent box half-width, receipt vs. declaration.** `W_ENVELOPE_CERT_RECEIPT.json:135-138` records `re_interval`/`im_interval` as `±1.01e-6`, while the declared theorem and `BOX_TO_THEOREM_UPGRADE_PLAN.md:128` say `1e-6`. The note inherits `1e-6`, matching the declaration. If the operative certified box is `±1.01e-6`, the margin drops to `0.0461028…` and every §3.2 endpoint shifts in the 6th decimal. **WHY the two differ is unknown to me** — flagging rather than resolving; it should be reconciled before any paper-level quotation.

---

## Required corrections before promotion
Fix 1 (re-round DOWN), 2 (recompute or delete the fallback separations), 3 (restate as one-way implication with the `Re < 1/2` hypothesis), 4 (state that link 7 moves from interpretive to load-bearing, and that multiplicity is an added input), 5 (B7 at all four sites), 6 (title + §0 to match §4). Then the note is promotable at exactly the status it claims for itself: **CONJECTURAL, conditional on the §3.3 `TODO-VERIFY`** — which remains genuinely undischarged and correctly flagged.
