# COLD REFEREE — assembled preprint, 2026-08-26 (frontier-verifier seat, installed verbatim)

Verdict: **PROMOTABLE-WITH-CORRECTIONS**. All corrections D-1..D-13 applied
to main.tex 2026-08-26 same-day (see git log); D-14 is a process note.
Bib repairs: Luo–Sarnak → Publ. IHES 81 (1995) PGT paper; Garbin–Jorgenson
cite REMOVED (unverifiable); Grothendieck = La théorie de Fredholm (gloss
fixed); Hardy 1914 + Takeuchi 1977 bibitems added.

## Per-check table

| # | Check | Verdict |
|---|---|---|
| 1a | Decimal intervals, pins s1/s2 — character-identical, 1−ρ re-derived | PASS |
| 1b | ρ1/ρ2 boxes + Im signs vs NOGO draft — character-identical, ρ_i=1−s_i | PASS |
| 1c | Separation 0.04334944458020843 re-derived by hand; Lean rational matches | PASS |
| 1d | Theorem statements vs sources | PASS except D-1 |
| 1e | Multiplicity/simplicity quantifier | FAIL (D-1) — FIXED |
| 2a | Standing sentence coverage (absent from abstract) | FAIL (D-2) — FIXED |
| 2b | MMS q=5 heading caveat verbatim | PASS |
| 2c | FJS p.4 k-caveat verbatim | PASS (D-6 fixed) |
| 2d | RH-conditionality disclosures | PASS |
| 3 | Overclaim scan (composable RH overclaim) | FAIL (D-3) — FIXED |
| 4 | FIG-1 caption/range | FAIL (D-4, D-5, D-7) — FIXED |
| 5 | Compile (tectonic, 15pp) | PASS |
| 6 | Bib orphans (none) | PASS except D-8/9/10 — FIXED |
| — | q8 §8 numbers re-derived from receipts | PASS |

## Defect list (as returned; status after repair in brackets)

BLOCKING
1. D-1 · §3b lead-in · "winding = 1 so each zero is simple" asserted of Z_S zeros; certificates give winding 1 for det(1−L_{s,+}) only, Z_S multiplicity ≥ that of + factor; internally contradicted by the Corollary proof. [FIXED in tex + skeleton]
2. D-4 · Fig. 1 caption ended "Not yet rendered" on a rendered figure. [FIXED]
3. D-5 · stale FIG-TODO block; stated range "0.22–0.33" rounds INWARD (receipt min 0.21881057); mandated 0.2188–0.3273 absent. [FIXED: block deleted, outward range in caption]

MAJOR
4. D-2 · abstract said "unconditionally" with the Standing block (part of the statement) stripped. [FIXED: computer-assisted/citation clause added]
5. D-3 · composable RH overclaim: "RH is literally P_line(3/4) for φ₃" + "A ⊬ P_line(c) ∀c" compose to "RH not provable" for a hostile reader; not-claimed list not updated for Met III. [FIXED: explicit bullet added]
6. D-8 · GarbinJorgenson2018 bibitem empty (authors only), cited live. [FIXED: cite + item removed with comment]
7. D-9 · LuoSarnak1995 bibitem was the Number-variance CMP paper, not the PGT error-term source. [FIXED: Publ. IHES 81 (1995)]
8. D-10 · Grothendieck "Résumé" ambiguity, load-bearing Thm 8. [FIXED: La théorie de Fredholm, Bull. SMF 84 (1956); gloss corrected]

MINOR
9. D-6 · PGT remark cites FJS without k-caveat pointer. [FIXED: cross-reference added]
10. D-7 · four arc histograms coincide to plotting precision — caption claimed per-arc structure the plot cannot show. [FIXED: coincidence stated in caption]
11. D-11 · drafting scaffolding typeset as body prose (abstract ledger notes; Bombieri paragraph discussing a citation the paper does not make). [FIXED: both removed]
12. D-12 · Metatheorem III Standing pointed at an unnamed internal note. [FIXED: caveats stated inline, pointing at the in-paper ledger + §machineverif]
13. D-13 · \item[3.] manual label. [FIXED]
14. D-14 · process note: mandated compile rewrote main.pdf (equivalent content). [Noted]

Also: Hardy 1914 and Takeuchi name-dropped without references. [FIXED: bibitems added]

## Non-defects confirmed
All eight interval endpoints, Im intervals, separation constant, Lean rational character-exact; no conjugation error; banned 0.5894543 transposition absent; §8 q=8 numbers reproduce exactly from receipts; cite/bibitem sets equal; blindness corollary, non-discriminating-q=3 repair, four audit weakenings, not-read declarations all present.
