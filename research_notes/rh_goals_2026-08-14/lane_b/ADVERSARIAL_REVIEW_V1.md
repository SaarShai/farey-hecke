# Adversarial review V1 (frontier-verifier, 2026-08-14) — persisted verbatim by orchestrator

I could not find a DONE MEANS block in the brief, but the four claims C1–C4 are individually gradeable, so I graded them rather than returning NOT-VERIFIABLE. I did **not** write `ADVERSARIAL_REVIEW_V1.md`: my lane is read-only on the work product and does not write report files. Findings are below; the parent can persist them verbatim.

## Verdicts

| Claim | Evidence I produced myself | Verdict |
|---|---|---|
| C1 "line vs cloud is an arithmeticity signature across the Hecke family" | see §1 | **REFUTED as stated** (survives as a much weaker statement, §1.7) |
| C2 "q=4/6 confirm the law" | see §2 | **REFUTED as independent evidence**; valid only as an engine positive control |
| C3 "an RH proof must use arithmetic structure; our lab shows it geometrically" | see §3 | **OVERREACH → SOUND-WITH-REPHRASING** (phrasing given) |
| C4 "G_5 off-line resonance is a provable target" | see §4 | **SOUND-WITH-REPHRASING**, but three unclosed gates, one of them not on the plan at all |

---

## 1. C1 — the "law" is one arithmetic commensurability class vs one or two non-arithmetic surfaces, measured with non-comparable protocols

**1.1 "Four surfaces" is arithmetically wrong and the count that matters is 2.** The arithmetic Hecke triangle groups q=3,4,6 are `Γ_0(1)`, `Γ_0(2)+`, `Γ_0(3)+` — all in *one* commensurability class (the modular one). They do not carry three independent scattering theories; they carry the same ζ. `EXECUTION_LOG.md:84` says "Four arithmetic surfaces on the line" — only three arithmetic surfaces were computed, and evidentially they are one point.

**1.2 The q=3 "control" and the G_5 measurement are different code paths.** `code/zeta_resonance_g5.py:126-133`: `cert_det` dispatches q=5 to `Zc.build_reduced_matrix_ball` (eq.34, κ=3, dim 3N) and q=3 to a locally hand-written scalar builder `build_reduced_matrix_ball_q3` (eq.33, κ=1, dim N). Only the Hurwitz/series/det *primitives* are shared. The q=3 control therefore cannot rule out an operator-construction error in the q=5 branch. Same defect in Lane B: `controls_q4q6/run_q4q6_controls.py:136-146` runs the gate through `Q3.cert_det_complex_mid` (q=3 builder) and the actual controls through `EVEN.cert_det_complex_mid` (`zeta_cert_rosen_even`, eq.32) — the gate validates neither the operator nor the geometry under test. And `zeta_cert_rosen_even.py:60-62` states its own scope: *"no q != 8 claims (the builder is general even q but only q=8 is anchor-validated)."* Lane B used it at q=4 and q=6 with no anchor.

**1.3 The one genuinely independent re-implementation disagreed by the size of the whole effect.** `projects/g5-crosscheck/results_sonnet.json`: from target (0.45390, 5.76354) it converged to (0.43318, 5.67575), `|det|=2.1e-10`, M-stable at M=14 and M=22; second target off by 0.074. `abs_diff_from_target = 0.0902` — larger than the entire reported G_5 cloud range (0.0855). The repo's own addendum (commit `94bc6eb`) attributes this to an *inferred* even-sector convention and calls 2-of-3 concordance a pass, but the concordant third (`results_fable.json`, 4.1e-9 / 1.4e-7) mirrors the certified engine's partition points, centers, radii and tail formula — it is a re-discretization of the same derivation, not an independent convention. The repo's own lesson line: *"the even-sector convention is the fragile step."*

**1.4 The `re_std` statistic is window-dependent and every surface used a different window.**
- q=3: **no scan at all** — `run_resonance_geometry.py:44-50` Newton-seeds directly at `s = 1/4 + iγ_n/2` for the first 8 Riemann zeros and keeps only pins with `|det| < 1e-6`. `re_std = 6.5e-14` measures how well 8 *known* ζ zeros satisfy Re=1/4; it is not a search result.
- G_5: `RE = linspace(0.30, 0.49, 8)`, `IM = [3,17]` — the band **excludes Re=1/4 entirely**.
- G_7: `run_resonance_g7.py:128` `RE = linspace(0.12, 0.48, 10)`.
- q=4/6: `RE = linspace(0.10, 0.49, 16)`.
A statistic computed over four different Re windows is not a family-comparable quantity, and the claimed "12 orders of magnitude on the same engine" compares a Newton residual against a physical spread.

**1.5 The G_5 sample is also inconsistent with the repo's own earlier G_5 harvest.** `code/out/resonance_v2.json` `g5_even_localization[9]` holds a G_5 even pin at **Re = 0.24302842**, Im = 10.5603, N-stable at N=16/22/28 (0.24303292 / 0.24302842 / 0.24302842) and **winding = 1** — one of only five winding-certified G_5 coordinates. It is omitted from the 8-pin geometry set and from `FAMILY_SWEEP_G7G8.md`, because the geometry run's band starts at 0.30. The omitted point is the one nearest the arithmetic line.

**1.6 Confounds I tested and could NOT sustain (report these as defended):**
- *Truncation artifact.* I re-pinned three G_5 coordinates at N=22/28/36/44: Re stable to 8 decimals (`0.45389518` at all four N; `0.48527431→0.48527432`). The cloud is not a dimension-truncation artifact.
- *Newton trapped at its seed / engine cannot produce a line from an off-line seed.* I ran the control the authors never ran — a q=3 surface over the G_5 band `Re∈[0.30,0.49] × Im∈[3,17]` at N=14, then Newton from the 8 deepest cells. Seeds at Re=0.300/0.347/0.395 all migrated to `Re = 0.250000`, `|det| ≈ 7.6e-16`. The q=3 code path does not fabricate off-line pins and does find the line from off-line seeds.
- *The ζ zeros are an artifact of the Hurwitz-tail construction.* Decisive negative control, also never run: I evaluated the **same even-q builder** at non-arithmetic q=8 and q=10 at `s = 1/4 + iγ_n/2`. Results `|det| = 2.13, 12.83, 5.67` (q=8) and `1.29, 11.54, 5.54` (q=10) versus `1.4e-11 / 3.7e-8 / 3.8e-6` at q=4 and `6.3e-10 / 2.2e-6` at q=6. The ζ-zero response is arithmetic-specific, not a construction artifact. **This is the strongest single piece of evidence the project has and it is not in any of the reviewed documents.**

**1.7 What survives.** Not a law across the family. What survives is: *in a fixed Im window and a fixed sector, the certified MMS determinant vanishes at s=ρ/2 for the arithmetic members and at no point of that window for two non-arithmetic members, whose zeros instead occupy a 2-D region.* That is a single arithmetic/non-arithmetic contrast, replicated on two non-arithmetic surfaces (G_5, G_7), with G_8 empty (`FAMILY_SWEEP_G7G8.md`: G_8 has zero eligible even-sector coordinates — all G_8 artifacts are odd-sector on-line data).

---

## 2. C2 — q=4/6 are a positive control, not evidence

**2.1 They re-detect the identical object.** q=4 pins: Im = 7.0673625708673464, 10.511019819386503, 12.50542878996472. q=3 pins: 7.067362570867347, 10.511019819385778, 12.505428790072845. Agreement to 1e-10–1e-15. These are γ_1,γ_2,γ_3 over 2. Because G_4 ≅ Γ_0(2)+ and G_6 ≅ Γ_0(3)+ are commensurable with the modular group, their one-cusp scattering determinants are again built from ζ(2s); resonances at s=ρ/2 are *predicted*, not discovered. Four surfaces are **two** data points, and the arithmetic one is the same ζ counted three times.

**2.2 Their off-line null result is partly protocol-induced.** `run_q4q6_controls.py:285-296` adds a 3×3 surface-local-minimum filter (123 raw seeds → 3 for q=4; 42 → 2 for q=6) and explicitly skips boundary rows `a == 0` and `a == len-1`. With `RE = linspace(0.10,0.49,16)` (spacing 0.026) the Re=0.49 row is excluded, so a basin centred above ≈0.477 cannot be reported. G_5's flagship pin sits at 0.4853, inside that blind zone. The G_5 run, by contrast, Newton-pinned *every* below-threshold cell (51 seeds). The arithmetic arm is less sensitive than the non-arithmetic arm exactly where the non-arithmetic cloud concentrates.

**2.3 The project's own newest document already contradicts the execution log.** `FAMILY_SWEEP_G7G8.md` grades q=4 and q=6 **INSUFFICIENT-DATA** (n=3 and n=2, below the four-point gate), while `EXECUTION_LOG.md:79-87` says "SIGNATURE SURVIVES — LINE, LINE … headline upgrades to arithmeticity law + atlas". The execution log has not been retracted. A referee who reads both will treat the upgrade as unsupported by the authors' own gate.

**2.4 Consequence for the preregistered blind test.** `BLIND_TEST_PROTOCOL.md` §5 makes `n < 4 → UNCLASSIFIABLE` and §6 makes UNCLASSIFIABLE a failed classification with no replacement draw. Run today, all 12 arithmetic draws (q=4: n=3, q=6: n=2) fail, so §7's success criterion is unreachable **by construction**. Separately, the engine is deterministic: 24 draws from a 6-value pool produce byte-identical records for repeated q, which both leaks the grouping to the blind classifier and means the effective sample is 6 surfaces (3 of them one commensurability class), not 24.

---

## 3. C3 — epistemic grade: established *lore*, and the evidence offered is circular

Grade: **not established, not "supported heuristic" in the form written — overreach.** Two independent reasons:

1. **The arithmetic half of the claimed law is RH.** For the modular surface the resonance set in Re<1/2 is exactly {ρ/2}. "Arithmetic ⇒ resonances on a vertical line" is *logically equivalent* to RH for those zeros; the measurement `re_std=6.5e-14` is a re-verification of Odlyzko's data. Arguing from it that "an RH proof must use arithmetic structure" assumes the conclusion in the premise.
2. **Arithmeticity is not isolated as the causal variable.** The contrast confounds arithmeticity with (a) commensurability with a congruence group, (b) existence of Hecke operators, (c) a scattering determinant expressible as a ratio of Dirichlet series with Euler product. Nothing in the data separates these. And the non-arithmetic side is not a failed RH-analogue — there is no L-function there at all, so no analogue statement was tested and refuted.

**Maximally defensible phrasing for the paper:**

> For the Hecke triangle family the Mayer–Mühlenbruch–Strömberg transfer operator gives a single computable model in which resonance locations can be compared across surfaces at fixed sector, precision and search window. For the arithmetic members q=3,4,6 — which are commensurable with the modular group — the resonances we locate in Im s ∈ [3,17] are numerically the points s=ρ/2 with ζ(ρ)=0; their alignment on Re s = 1/4 is therefore the Riemann Hypothesis for those zeros, not an independent regularity of the family. For the non-arithmetic members q=5 and q=7 we locate resonances that do not align on any vertical line, in agreement with the Phillips–Sarnak picture. We claim neither a new law nor an inference about what a proof of RH must contain. What is new is a certified, uniform computational family in which the alignment mechanism is present exactly for the arithmetic members, together with the first interval-quality off-line resonance data for non-arithmetic Hecke surfaces.

Delete every occurrence of "an RH proof must use arithmetic structure". If a motivational sentence is wanted, the defensible version is historical, not evidential: "the absence of an Euler product is the standard heuristic explanation for the failure of purely analytic approaches; our family makes that contrast computable."

---

## 4. C4 — strongest technical objection: the determinant is not the Selberg zeta

The plan (`THEOREM_G5_OFFLINE_PLAN.md`) names one missing ingredient (the dimension-tail bound). There are **three**, and the one it omits is the most dangerous.

**4.1 (Omitted from the plan) The K_s divisor.** MMS's own theorem, verbatim in `research_notes/MMS_0912.2236_EXTRACTION.txt:19,35`, is
`Z_S(s) = det(1−L_s)/det(1−K_s) = det[(1−L_{s,+})(1−L_{s,−})]/det(1−K_s)`.
A zero of `det(1−L_{s,+})` is a zero of Z_S **only if** `det(1−K_s) ≠ 0` there; K_s exists precisely to cancel an over-counted orbit and has, in MMS's words, "regularly spaced zeros of its Fredholm determinant in the complex s-plane". The only statement about K_s anywhere in the repo is `code/zeta_mayer_rosen.py:60-62`: "does NOT contribute zeros **on the critical line near the Maass values**" — an on-line statement, while every headline claim here is off-line. `grep` finds no K_s evaluation, no K_s zero set, and no K_s section in the MMS extraction. As written, the flagship theorem would prove a zero of a *particular Fredholm determinant*, not a scattering resonance of G_5. (Mitigating: the eight G_5 Im values show no arithmetic progression, so blanket K_s contamination is unlikely — but "unlikely" is not a certificate, and a single contaminated pin is fatal if it is the theorem's pin.)

**4.2 The convention pin is a load-bearing, unclosed item.** §1.3 above: the theorem asserts `Re(s*) ∈ [0.4539 − δ, 0.4539 + δ]` while an independent inference of the same even-sector convention places the nearby zero at 0.4332. Until the sign/block convention is verified line-by-line against MMS eq.(32)/(34) — the repo's own recorded lesson — the theorem's numeric content is convention-dependent. Note also the standing label correction (`zeta_mayer_rosen.py:68-72`, memory `g5-maass-spectrum-validated`): the ± sectors are the λ-CF Markov-partition reflection, **not** Maass even/odd parity, so the words "even sector" in the target statement need replacing with "P-symmetric (mms+) sector".

**4.3 The tail heuristic is not merely unproven — it is visibly non-monotone.** In `q4q6_winding_receipt.json`, pin `q4_pin_1`: the centre sample gives ratios 0.0478/0.0467/0.0460 and `tail_radius = 1.5e-15`; the corner (−1,−1) gives ratios **0.5618 → 0.5940 → 0.6047 (increasing)** and `tail_radius = 2.36e-9`, six orders of magnitude larger. `dim_tail_from_matrix` takes the max of the last three observed ratios and extrapolates it to all higher dimensions (`zeta_cert_q3.py:208-243`, `zeta_cert_rosen_q5.py:415-452`, caps 0.75 / 0.85). At that corner the observed ratios trend *toward* the cap, so the extrapolated max is not conservative even within the computed window. This is a concrete counterexample to the "geometric-contraction regime" premise, and it is the premise the proven-tail-bound work item must replace. Margins are thin: `q4_pin_2` has `tail_fix = 3.17e-6` against a contour lower bound of `2.37e-4` and a winding ball of `[0.53, 1.50]`.

**4.4 What the theorem would actually be worth.** "Re(s*) ≠ 1/4" is close to vacuous — nobody expects a non-arithmetic surface to have resonances at 1/4. The valuable statement is *first rigorous localization of a scattering resonance of a non-arithmetic finite-area hyperbolic surface*, with the essential-gap consequence (`Re(s*) ≤ 1/2 − 0.0147`) as the structural content. Reframe the target accordingly.

---

## Single most dangerous weakness

**The headline generalizes from one commensurability class, and every quantity that is supposed to demonstrate the generalization was measured under a different protocol for each surface.** q=3 was seeded at the answer and never searched; G_5 was searched in a band that excludes the arithmetic line and excludes a winding-certified G_5 pin at Re=0.243; G_7 in a third band; q=4/6 in a fourth, with an extra local-minimum filter that is blind exactly where the G_5 cloud lives. A referee needs one paragraph to establish that `re_std` is not a comparable quantity across the rows of the family table — and that is the table the paper is built on. The internal contradiction between `EXECUTION_LOG.md` ("LINE, LINE, upgrade to law") and `FAMILY_SWEEP_G7G8.md` ("INSUFFICIENT-DATA, INSUFFICIENT-DATA") makes it findable in one minute.

## Three highest-value hardening actions

1. **One protocol, one window, every surface — then recompute the table.** Fix `Re ∈ [0.10, 0.49] × Im ∈ [3, 17]`, N_surface, threshold rule and seed rule (no boundary-row exclusion, no 3×3 filter on one arm only), and re-run q=3, 4, 6, 5, 7, 8 identically, including a genuine *search* for q=3 rather than ζ-zero seeding. Report per-surface `re_std` only from that sweep, and restore the omitted G_5 pin at Re=0.24303 (winding=1) or state in print why an eligible winding-certified coordinate is excluded. This is the cheapest action that converts the family table from non-comparable to comparable, and it is what §1.4/§2.2 above would otherwise sink.
2. **Promote the non-arithmetic ζ null control into the paper, and close the K_s gate.** The q=8/q=10 result in §1.6 (|det| = O(1) at s=ρ/2 for non-arithmetic even q, versus 1e-11 at q=4) is stronger evidence than the q=4/q=6 "LINE" rows and costs seconds to reproduce — it is the control that makes the arithmetic response non-trivial. In the same pass, extract MMS Section `secK` / Prop. 2, compute the K_s zero set for q=5, and certify `det(1−K_{s}) ≠ 0` inside every winding box before any resonance is claimed.
3. **Replace the tail heuristic with the Jenkinson–Pollicott bound *and* re-derive the even-sector convention from MMS eq.(32)/(34) independently, before the theorem's Re-value is written down.** The corner ratios at `q4_pin_1` show the current test can pass while the true ratio is rising; the sonnet/fable divergence shows the theorem's number is convention-sensitive at 0.02–0.09. Both must close before `Re(s*) ∈ [0.4539 ± δ]` is a defensible statement. While that is open, restate the theorem as "a resonance with `Re(s*) ≤ 1/2 − δ_gap`" rather than pinning a decimal.

## Documentation defects to fix regardless

- `EXECUTION_LOG.md:79-87` "Four arithmetic surfaces on the line" — only three exist and were computed; and the verdict is contradicted by `FAMILY_SWEEP_G7G8.md`. Retract or reconcile in place.
- `lane_b/CERTIFIED_VS_HEURISTIC.md` and `lane_b/DISTRIBUTION_OPTIONS.md` are now **stale**: both say the q=4/q=6 winding upgrade is pending, but `Q4Q6_WINDING_CERTIFICATES.md` + `q4q6_winding_receipt.json` report 5/5 CERTIFIED (heuristic tail entered = True on all five). Everything else I spot-checked in `CERTIFIED_VS_HEURISTIC.md` reproduced exactly against source — it is the most reliable document in the set and should be the template for the paper's verification section.
- `00_SYNTHESIS.md:149` and `GOAL2_MAP.md:274` quote G_5 `std ~0.04`; the restored artifact gives 0.029986. The 0.04 figure belongs to the June 9-pin set. Pick one and say which sample it is over.
- `lane_b/RESTORE_LOG.md:646-649` "pinned coordinates identical to the 2026-06-20 list" is true only for the 8 geometry pins; the 2026-06-20 record lists ~9 G_5 resonances including 0.243+10.560i. Qualify it.

Key files: `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_resonance_g5.py`, `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_even.py`, `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/controls_q4q6/run_q4q6_controls.py`, `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/run_resonance_geometry.py`, `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/out/resonance_v2.json`, `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/projects/g5-crosscheck/results_sonnet.json`, `/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/research_notes/MMS_0912.2236_EXTRACTION.txt`, `/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_b/FAMILY_SWEEP_G7G8.md`. My probe scripts are in `/private/tmp/claude-501/-Users-za-Documents-farey-hecke/ddf80682-2387-475e-af1f-e0edb8ef7d8a/scratchpad/` (`probe.py`, `q3scan.py`, `g5N.py`, `q810.py`) — all read-only against the worktree.