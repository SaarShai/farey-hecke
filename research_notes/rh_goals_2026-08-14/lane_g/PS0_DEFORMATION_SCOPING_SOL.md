# PS-0 — Deformation-family lane: prior-art gate + scoping

**Date:** 2026-08-22/23. **Lane:** NEXT-3 (Phillips–Sarnak deformation family),
step PS-0 as mapped in plans/wayfinder/rh-goals/MAP.md (2026-08-23 06:30Z entry).
**Status: UNREFEREED.** LEDGER RULE binds: nothing below is stronger than its
most-caveated source. Every unproven statement is marked CONJECTURAL or OPEN.

## 0. Verdict of the gate

**NARROW, do not kill.** The 2026-06-20 verdict (Aim 2 DROP) and the 2026-08-16
deformation prior-art catalog stand. The mechanism (Fermi golden rule), the
cusp-form-dissolution side, and non-rigorous numerical pole tracking along
deformations are all **owned by others**. What the sweep did NOT find, in the
banked catalog or in fresh search (2026-08-22): any **interval-certified /
rigorous-numerics localization of scattering resonances along a deformation
path** (character variety or Teichmüller), at any surface. That is the sole
surviving niche. It is an *instrument + certificates* niche, not a
*mechanism* niche; framing it as new mechanism would repeat the Aim-2 error.

## 1. What the prior verdicts already killed (re-read, binding)

- `.worktrees/aletheia-restore/research_notes/DISCOVERY_SYNTHESIS_2026-06-20.md`,
  Aim 2: "Phillips–Sarnak dissolution geometry: DROP (post-hoc / spurious)."
  Frame owned by Phillips–Sarnak 1985/1992/1994, Bruggeman–Pohl, Petridis–
  Risager, and the numerical-resonance paper arXiv:1812.05554. The
  "q-independent attractor band" claim was post-hoc and is dead. Salvage
  allowed there: "a certified resonance Re-value table (data artifact, not a
  theorem)." NEXT-3 must stay inside that salvage clause plus the certified-
  localization gap of §2.
- `LAW_DEFORMATION_PRIOR_ART.md` (2026-08-16, frontier-verified): the
  qualitative large-q Hecke off-line tail is a **Selberg–Hejhal theorem**
  (Hejhal LNM 1001 Vol. 2, Thm 7.11/Cor 7.12; Garbin–Jorgenson 2018 quantify
  it). Must be cited wherever novelty is framed (mandate,
  `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md` correction block item 2).

## 2. Prior-art sweep: who tracks WHAT along deformations

Owned-by-others, by column (resonances vs cusp forms; rigorous vs numerical):

| Work | Family/parameter | Object tracked | Rigor |
|---|---|---|---|
| Phillips–Sarnak, JAMS 5 (1992) 1–32; GAFA 4 (1994) 93–118 | Teichmüller (weight-4 cusp-form directions); character varieties | cusp forms dissolving into resonances; singular set | rigorous, **conditional** (embedded eigenvalue + nonzero coupling) |
| Wolpert, "Spectral limits for hyperbolic surfaces I/II" (Invent. Math. 108 (1992)) and CMP 112 (1987) | Teichmüller / pinching degeneration | spectral measures, Z | rigorous; degeneration continuity, no off-line localization |
| Petridis–Risager, Mathematika 59 (2013) 269–301 | character variety | higher-order dissolution criteria | rigorous, conditional/local |
| Balslev–Venkov, Acta Math. 186 (2001) | Γ₀(N) + character (arithmetic; "Hecke" false friend) | embedded eigenvalues → resonances | rigorous, conditional |
| Farmer–Lemurell, Math. Comp. 74 (2005) 1967–1982 | Teichmüller of Γ₀(5)-type | Maass forms / dissolution | numerical, non-rigorous ("indicate") |
| Avelin, Math. Comp. 76 (2007) 361–384 | Teichmüller of Γ₀(5) | pole motion (Taylor coefficients) | numerical + rigorous local lemma (Lemma 3.1) |
| Fraczek–Mayer, Algebra & Number Theory 6 (2012) 587–610, arXiv:1011.4441; Fraczek, *Selberg Zeta Functions and Transfer Operators*, Springer LNM 2139 (2017) | Γ₀(4) + Selberg's one-parameter character χ_α | **Selberg-zeta zeros = resonances**, tracked in α via transfer operator; λ=−1 sector proved on-line (via Phillips–Sarnak), λ=+1 zeros observed leaving the line | numerical (high-precision, NOT interval-certified) |
| Bruggeman–Fraczek–Mayer, Exp. Math. 22 (2013) 217–242, arXiv:1201.2324 | Γ₀(4) + singular character deformation | curves of resonances, tangency at Re s = 1/2, Thms 1.4/1.5 | **rigorous off-line curve theorem** (arithmetic base) |
| Levitin–Strohmaier, IMRN 2021:6, 4003–4050, arXiv:1812.05554 | conformal perturbations and Teichmüller moves on cusped surfaces | **resonances directly** (scattering matrix from Neumann-to-Dirichlet FEM) | numerical, floating-point; explicitly advertised for tracking resonances in Teichmüller space |
| Borthwick (book 2016, 2nd ed.; Borthwick–Weich etc.) | infinite-area families (Hecke Γ_w, w>2; pants) | resonance-cloud computations | numerical, non-certified |
| Booker–Strömbergsson–Venkatesh, "Effective computation of Maass cusp forms", IMRN 2006; Child, arXiv:2204.11761; Bober et al. arXiv:2201.08760 | fixed arithmetic groups (no deformation) | **certified** cusp-form eigenvalues (on-line) | interval-rigorous — but eigenvalues, not resonances; no family |

**Gap statement (the narrowed goal).** No located work combines all three of:
(i) resonances (off-line scattering poles / Selberg-zeta zeros off Re s = 1/2),
(ii) a continuous deformation family with an arithmetic point, and
(iii) certified (interval/winding-certificate) localization. Our repo already
holds (i)+(iii) at fixed groups (the certify engine, G_5/G_7 winding
certificates; the G_5 off-line resonance theorem 2026-08-15). NEXT-3 adds (ii).
CONJECTURAL until PS-2/PS-4 deliver: that the engine extends to a deformed
family at controlled cost.

## 3. Scoping: what actually deforms

Hecke triangle groups G_q are triangle groups, hence **rigid**: no Teichmüller
deformation; q is discrete and q→∞ is *elliptic degeneration* (cone point →
cusp), not a path. So the "family" must be one of:

1. **Character variety of a fixed group** (unitary characters χ_α). Canonical
   worked example: Γ₀(4) with Selberg's character — the Fraczek–Mayer /
   BFM setting, with a transfer-operator representation of Z(s,χ_α) already in
   print. Arithmetic point α=0 where the scattering matrix is expressible in
   Dirichlet L / ζ data. **Best-instrumented candidate**; also most crowded.
2. **Teichmüller space of a non-rigid surface with an arithmetic point**, e.g.
   once-punctured torus (Teich dim 2) with the Γ' = commutator-subgroup-of-
   PSL(2,Z) point, or Γ(2) (thrice-punctured sphere is again rigid — excluded).
   Punctured torus has genuine moduli AND a hyperbolic arithmetic point; its
   Fricke coordinates give an explicit real-analytic family. No published
   transfer-operator family coding located for the deformed points (OPEN).
3. **Weights / multiplier systems** on a fixed Hecke G_q (real weight r as a
   deformation parameter; Selberg's original context). Keeps our groups, but
   prior art on Eisenstein/scattering in the r-parameter is old and partly
   owned (Selberg, Hejhal Vol. 2 App.; not swept in depth — OPEN item for PS-1).

Option 1 fits PS-1's ledger wording ("punctured-torus / Γ(2)-type surface at
whose τ=0 the scattering matrix is ζ-expressible") loosely; strictly, Γ₀(4)
with χ_α IS the literature's canonical instance and the one where a certified
snapshot is most plausibly computable. Option 2 is more novel but PS-2 cost is
much higher (no donor symbolic coding).

## 4. What our LAW + pins say vs the PS conjecture (precise formulation)

- The PS conjecture (informal, for non-arithmetic cofinite groups): the
  discrete (cusp-form) spectrum is finite/sparse — N_d(T) = o(T²) — with the
  Weyl T² mass carried by the scattering term M(T). **OPEN**; this session's
  PGT-1 referee defect D2 makes our own density-zero claims **CONDITIONAL on
  exactly this**: what is known unconditionally is only the split
  N_d(T) + M(T) ~ (|F_q|/4π)T², with |F_q| = 2π(1/2 − 1/q) (Gauss–Bonnet;
  the earlier π(1/2−1/q) is a corrected factor-2 slip — do not reuse).
- Our LAW/(C) count (`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`,
  CONFIRMED-by-two-referees statement, consumed modulo the unread [Sel90]
  citation — that caveat inherits here): for every finite q≥3 the weighted
  off-line scattering-zero count is (1/2π)T log T + A_qT + O_q(log T). This
  gives **abundance of off-line resonances at every fixed q** but is
  NON-DISCRIMINATING (q=3 arithmetic has it too) and says nothing about
  motion in a family.
- Our certified pins (G_5 off-line resonance theorem, 2026-08-15; G_5/G_7
  resonance tables; q=3 Re=1/4 interval checks) are **static snapshots at
  rigid points**. They neither support nor refute PS; they are the calibration
  endpoints a deformation lane would interpolate between.
- Therefore: nothing we own currently bears on the PS conjecture itself.
  A NEXT-3 result of type PS-4/PS-5 would be the first *certified* exhibit of
  the dissolution/off-line drift phenomenon along a path — evidence-grade for
  PS, not a proof of it. Any claim that it "tests" or "confirms" PS must be
  marked CONJECTURAL framing.

## 5. Proved vs conjectured in the successor literature (summary)

Proved: conditional dissolution criteria (PS 1992 Fermi golden rule; PS 1994
eq. (5.29); Petridis–Risager higher order); off-line resonance curves for the
singular character deformation of Γ₀(4) (BFM 2013 Thms 1.4/1.5); on-line
persistence of the λ=−1 sector of Γ₀(4,χ_α) (Fraczek–Mayer 2012, via PS);
degeneration continuity (Wolpert; Garbin–Jorgenson; Schulze).
Conjectured/numerical only: genericity of dissolution (Farmer–Lemurell,
Avelin); the full λ=+1 sector leaving the line for α≠0 (Fraczek LNM 2139 —
numerics, no certificates); PS conjecture N_d(T)=o(T²) itself (OPEN);
resonance behaviour along general Teichmüller paths (Levitin–Strohmaier —
float numerics).

## 6. Recommended PS-1 (sharpest attackable question)

**Family selection = Γ₀(4) with Selberg's character χ_α (option 1), with the
punctured torus (option 2) as the recorded fallback if novelty pressure
demands distance from Fraczek–Mayer.** Rationale: transfer-operator coding of
Z(s,χ_α) is published (Fraczek–Mayer 2012; Fraczek LNM 2139), so PS-2 becomes
"port a published symbolic coding into engine/certify/ and interval-certify
it" — squarely our demonstrated capability — rather than "invent a coding."
The arithmetic point α=0 is ζ/L-expressible, satisfying the certified-
computable-anchor requirement.

The PS-1 question to write up: *fix the Fraczek λ=+1 zero nearest the banked
heights; state the certified-snapshot target — interval boxes for that
resonance at a finite grid of α values, plus a perturbation bound gluing
adjacent boxes — and check Fraczek's LNM 2139 numerics for the specific zero
and α-range where off-line drift is largest (best signal-to-cost).* Success at
PS-4 then yields: first interval-certified off-line resonance localization
along a deformation path (novel per §2 gap), with BFM 2013 cited as the
rigorous-curve antecedent on the same family and Fraczek's numerics as the
uncertified antecedent — both citations mandatory wherever novelty is framed.

**Explicit novelty ceiling (write it now, before compute):** the phenomenon,
family, mechanism, and non-rigorous tracking are ALL owned (PS, FM, BFM,
Levitin–Strohmaier). Ours would be only the certificates and any effective
constants. If PS-1 finds BFM/Fraczek's rigorous results already cover the
targeted zero's off-line locus (their Thms 1.4/1.5 cover the singular
deformation; check overlap with the regular χ_α sector), narrow again or kill.

## References (new beyond LAW_DEFORMATION_PRIOR_ART.md's list)

- M. Fraczek and D. Mayer, "Symmetries of the transfer operator for Γ₀(N) and
  a character deformation of the Selberg zeta function for Γ₀(4)," Algebra &
  Number Theory 6 (2012), 587–610. DOI 10.2140/ant.2012.6.587;
  arXiv:1011.4441.
- M. S. Fraczek, *Selberg Zeta Functions and Transfer Operators: An
  Experimental Approach to Singular Perturbations*, Springer Lecture Notes in
  Mathematics 2139 (2017). DOI 10.1007/978-3-319-51296-9.
- M. Levitin and A. Strohmaier, "Computations of eigenvalues and resonances on
  perturbed hyperbolic surfaces with cusps," IMRN 2021, no. 6, 4003–4050.
  DOI 10.1093/imrn/rnz157; arXiv:1812.05554.
- A. R. Booker, A. Strömbergsson, A. Venkatesh, "Effective computation of
  Maass cusp forms," IMRN 2006, Art. ID 71281.
- A. Child, "Certification of Maass cusp forms of arbitrary level and
  character," arXiv:2204.11761 (2022).
- J. Bober et al., "Rigorous computation of Maass cusp forms of squarefree
  level," arXiv:2201.08760 (2022).
- S. A. Wolpert, "Spectral limits for hyperbolic surfaces, I & II," Invent.
  Math. 108 (1992), 67–89 and 91–129.
(For Hejhal, Garbin–Jorgenson, PS 1992/1994, Petridis–Risager, BFM 2013,
Avelin, Farmer–Lemurell, Balslev–Venkov, Schulze, Borthwick: full entries in
LAW_DEFORMATION_PRIOR_ART.md — not duplicated here.)

## Caveats ledger (inherits)

- [Sel90] unread — every LAW/(C) consumption above is modulo Kelmer's
  transcription (LAW_SECOND_AUDIT_REFEREE residual).
- Hejhal 7.11/7.12 + Garbin–Jorgenson quantification must accompany any
  novelty framing (standing mandate).
- PGT-1 D2: density-zero / PS-side statements CONDITIONAL on N_d(T)=o(T²).
- Fraczek LNM 2139 theorem-level contents were NOT read in full text this
  pass (contents inferred from the 2012 paper, BFM, and publisher/search
  abstracts); PS-1 must read the book's relevant chapter before committing
  the target zero. Web-search summaries above are secondary until then.
