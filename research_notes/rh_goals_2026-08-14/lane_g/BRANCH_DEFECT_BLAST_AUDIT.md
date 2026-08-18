# Branch-phase defect blast-radius audit (sol, read-only, 2026-08-17)

Auditor: gpt-5.6-sol codex, read-only sandbox; report persisted verbatim from
the session log (scratchpad sol_branch_audit.log). VERDICT: 0 re-runs needed
for the branch defect; the MAP-queued suspect-audit item is DISCHARGED.
Independent spot-verification by the orchestrator: none beyond reading —
classifications cite file:line evidence throughout.

> **[CORRECTION 2026-08-18 audit-14]** Scope note on this report's own
> numbers. The "Independent checks" section below reports an 850-file scan,
> a `q=12, s=1.1+1.5i` raw-vs-path-integrated comparison, and a fresh
> 50-point `agp_massbalance` re-check with max difference `3.91e-10`. Those
> are **auditor-reported, not independently receipted**: no command, script
> path, interpreter, precision setting, output file or hash is recorded, and
> the header above states the orchestrator did no verification beyond
> reading. The audit's SCOPED CONCLUSION (0 re-runs needed; the MAP-queued
> suspect-audit item discharged; the future-use warning about raw
> `K_q_corrected`) may stand on its cited file:line evidence, but the
> numerical census is not reproducible from this report alone.

## Consumer table

“Rerun” means rerun specifically because of this branch-phase defect.

| File | Classification | Evidence | Rerun |
|---|---|---|---|
| [`agp_phi.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_phi.py:79) | Provider, not a consumer | Raw principal-power kernel lines 79–87; branch-free derivative and defect explanation lines 96–120; `phi_det` hard-codes `1/2+ir` lines 170–191 | No |
| [`agp_validate.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_validate.py:46) | `USES-ON-LINE-ONLY` | All determinant/exact comparisons use real `r0` with the critical-line API, lines 46–93 | No |
| [`agp_b4star.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_b4star.py:50) | `USES-ON-LINE-ONLY` | Calls the exact critical-line log derivative; explicitly no determinant or Teo kernel, lines 17–24 and 50–57 | No |
| [`agp_massbalance.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_massbalance.py:114) | `USES-ON-LINE-ONLY` | `kk(r)` fixes `s=0.5+ir`; local phase ratio only, lines 114–133. Fresh 50-point comparison passed at `3.91e−10` max error | No |
| [`agp_kgrowth.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_kgrowth.py:54) | `POST-FIX` | Directly evaluates branch-free `Re dlogK_ds(0.5+ir,q)`, lines 54–59 | No |
| [`agp_window.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_window.py:138) | `POST-FIX` | Explicitly rejects raw `arg K_q`; integrates `dlogK_ds`, lines 138–173. Arithmetic exact checks are at lines 248–256 | No |
| [`agp_alpha.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_alpha.py:76) | `POST-FIX` | Reads only `agp_kgrowth.json` and `agp_window.json`, lines 76–102 | No |
| [`mirror_u4_corrected.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/mirror_u4_corrected.py:122) | `USES-MAGNITUDE-ONLY` | Every off-line kernel/φ value is reduced with `fabs`, lines 122–166 | No |
| [`q3cont_compare.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/q3cont_compare.py:62) | `USES-MAGNITUDE-ONLY` | Off-line `phi_exact` and `K_q_corrected` enter only through `fabs`, lines 62–81 | No |
| [`q3cont_q4_sigmasweep.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/q3cont_q4_sigmasweep.py:48) | `USES-MAGNITUDE-ONLY` | Whole off-line σ sweep stores `fabs(phi)` and `fabs(K)`, lines 48–69 | No |
| [`rate_measure.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure.py:98) | `POST-FIX` | Reconstructs `log K` by vertical integration of `dlogK_ds`, then forms complex off-line `φ_q`, lines 98–119 | No |
| [`rate_measure_validate.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate.py:30) | `POST-FIX` | Tests corrected complex `φ_q` against exact q=3,4,6 values over the full off-line grid, lines 30–48 | No* |
| [`rate_measure_run.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_run.py:50) and [`rate_measure_data.json`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_data.json:2) | `POST-FIX` | Runner calls corrected `R.phi_q` at `σ=1.1,1.25`, stores complex values and `D`, lines 50–79. Current artifact has 48 rows | No* |
| [`LAW_AGAMMA_PROBE.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_AGAMMA_PROBE.md:173) | `POST-FIX` | Records the discarded raw-argument defect and replacement with `dlogK_ds`, lines 173–186; final arithmetic checks passed, lines 190–210 | No |
| [`LAW_STRIP_AND_MIRROR.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_STRIP_AND_MIRROR.md:3) | `USES-MAGNITUDE-ONLY` | Tasks are explicitly `|φ_q|` and modulus mirror ratios, lines 3–13; code paths use independent continuation and magnitudes, lines 105–117 and 295–316 | No |
| [`LAW_U1_GROWTH.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_U1_GROWTH.md:231) | `USES-MAGNITUDE-ONLY` | Critical-line assembly is a modulus check, lines 231–258; guard receipts are determinant absolute values, lines 712–725 | No |
| [`LAW_U1PHI_PROOF_ROUTE.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_U1PHI_PROOF_ROUTE.md:289) | `USES-MAGNITUDE-ONLY` | Uses independent Eisenstein `φ_q` and exact sine-product `E_q`, lines 289–301; receipts explicitly describe `|φ_q|`/`|φ_qE_q|`, lines 543–550 | No |
| [`LAW_U1PHI_TEST.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_U1PHI_TEST.md:217) | `USES-ON-LINE-ONLY` | Phase experiment uses the determinant proxy only at `Re s=1/2`; no off-line `agp_phi` phase evaluation | No |
| [`LAW_RATE_MEASURE.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_RATE_MEASURE.md:69) | `POST-FIX` | Describes the defect and path-integrated fix, lines 69–99; published `D` values explicitly come from the corrected runner, lines 169–177 | No* |
| [`LAW_R1_COSET_STRUCTURE.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_R1_COSET_STRUCTURE.md:116) | `POST-FIX` | Reference validation uses `rate_measure.phi_q` at `1.5+i·10⁻⁸`, lines 116–123; introduced after the corrected RATE pipeline | No |
| [`LAW_R2_RATE_LEMMA_DRAFT.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_R2_RATE_LEMMA_DRAFT.md:254) | `POST-FIX` | Reads measured `D` from the corrected RATE JSON, lines 254–266 | No |
| [`LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:61) | `POST-FIX` | q=64 completion and slopes explicitly cite the corrected RATE JSON/log, lines 61–71 | No |
| [`LAW_R4_THETA_DEFECT.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_R4_THETA_DEFECT.md:14) | `USES-MAGNITUDE-ONLY` | Reuses only `phi_infty`/`_g_of_s`; it does not consume finite-q `K_q_corrected` phase, lines 14–15 | No |

\*No branch-related rerun. A separate truncation issue remains: [`rate_measure_validate.log`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate.log:18) fails its `N=24` gate at `t=14`, and the `t=7.0665` RATE rows are not converged. Higher-`N` reruns are needed only if those heights are to be promoted—not because of the branch defect.

## Published-number impact

- **Retained published tables/slopes:** unaffected by this defect.
- **RATE complex differences `D(q;s)`:** phase-sensitive, but all were produced through the post-fix path.
- **Strip/U1/mirror numbers:** unaffected because their code uses independent evaluators or magnitudes only.
- **AGP final numbers:** unaffected; branch-free critical-line paths were used and validated.
- **Known-bad diagnostic:** `LAW_AGAMMA_PROBE.md` line 180 prints the discarded pre-fix example `−8.96`. That number is affected, but it is explicitly labeled as the defect symptom and is not consumed by any retained conclusion.
- **Unknowns:** none among direct executable consumers. Citation-only prose mentioning `φ_q` without executing an evaluator was excluded from the consumer set rather than guessed into a classification.
tokens used
207,299
# Read-only blast-radius audit

Verdict: **no retained repo number requires re-running because of the off-critical-line branch-phase defect.**

No pre-fix script that consumed the raw off-line complex phase was found. The only general off-line `agp_phi` consumer is the RATE pipeline, and it was introduced together with the path-integrated correction. Earlier related probes either:

- use independent Eisenstein-series evaluators;
- reduce `φ_q`/`K_q` to magnitudes with `abs`/`fabs`;
- stay on `Re s=1/2`; or
- already use `dlogK_ds`.

No files were written.

## Important implementation detail

The raw [`K_q_corrected`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_phi.py:79) function itself still assembles principal-branch fractional powers. The branch-free derivative is [`dlogK_ds`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_phi.py:96), while the actual off-line path-integrated reconstruction lives in [`rate_measure.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure.py:98).

Therefore, a future direct call to `agp_phi.K_q_corrected(s,q)` that consumes off-line phase would reintroduce the defect.

## Independent checks

- The entire requested tree—850 files—was scanned for imports, calls, subprocess consumers, textual citations, and output dependencies.
- At `q=12`, `s=1.1+1.5i`, raw and path-integrated `K_q` had:
  - relative modulus difference: `0.0`;
  - phase difference: `−2.617993877991495` radians;
  - on-line `|K_q(1/2+1.5i)|−1`: `0.0`.

  This directly confirms phase corruption without magnitude corruption at that sample.
- `agp_massbalance.py` is the one older probe using local raw-`K_q` phase differences. All 50 published `(q,r)` points were freshly compared against `Re dlogK_ds`; maximum absolute difference was `3.91e−10`. Its retained numbers do not require rerunning.

## Consumer table

“Rerun” means rerun specifically because of this branch-phase defect.

| File | Classification | Evidence | Rerun |
|---|---|---|---|
| [`agp_phi.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_phi.py:79) | Provider, not a consumer | Raw principal-power kernel lines 79–87; branch-free derivative and defect explanation lines 96–120; `phi_det` hard-codes `1/2+ir` lines 170–191 | No |
| [`agp_validate.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_validate.py:46) | `USES-ON-LINE-ONLY` | All determinant/exact comparisons use real `r0` with the critical-line API, lines 46–93 | No |
| [`agp_b4star.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_b4star.py:50) | `USES-ON-LINE-ONLY` | Calls the exact critical-line log derivative; explicitly no determinant or Teo kernel, lines 17–24 and 50–57 | No |
| [`agp_massbalance.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_massbalance.py:114) | `USES-ON-LINE-ONLY` | `kk(r)` fixes `s=0.5+ir`; local phase ratio only, lines 114–133. Fresh 50-point comparison passed at `3.91e−10` max error | No |
| [`agp_kgrowth.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_kgrowth.py:54) | `POST-FIX` | Directly evaluates branch-free `Re dlogK_ds(0.5+ir,q)`, lines 54–59 | No |
| [`agp_window.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_window.py:138) | `POST-FIX` | Explicitly rejects raw `arg K_q`; integrates `dlogK_ds`, lines 138–173. Arithmetic exact checks are at lines 248–256 | No |
| [`agp_alpha.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/agp_alpha.py:76) | `POST-FIX` | Reads only `agp_kgrowth.json` and `agp_window.json`, lines 76–102 | No |
| [`mirror_u4_corrected.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/mirror_u4_corrected.py:122) | `USES-MAGNITUDE-ONLY` | Every off-line kernel/φ value is reduced with `fabs`, lines 122–166 | No |
| [`q3cont_compare.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/q3cont_compare.py:62) | `USES-MAGNITUDE-ONLY` | Off-line `phi_exact` and `K_q_corrected` enter only through `fabs`, lines 62–81 | No |
| [`q3cont_q4_sigmasweep.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/q3cont_q4_sigmasweep.py:48) | `USES-MAGNITUDE-ONLY` | Whole off-line σ sweep stores `fabs(phi)` and `fabs(K)`, lines 48–69 | No |
| [`rate_measure.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure.py:98) | `POST-FIX` | Reconstructs `log K` by vertical integration of `dlogK_ds`, then forms complex off-line `φ_q`, lines 98–119 | No |
| [`rate_measure_validate.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate.py:30) | `POST-FIX` | Tests corrected complex `φ_q` against exact q=3,4,6 values over the full off-line grid, lines 30–48 | No* |
| [`rate_measure_run.py`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_run.py:50) and [`rate_measure_data.json`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_data.json:2) | `POST-FIX` | Runner calls corrected `R.phi_q` at `σ=1.1,1.25`, stores complex values and `D`, lines 50–79. Current artifact has 48 rows | No* |
| [`LAW_AGAMMA_PROBE.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_AGAMMA_PROBE.md:173) | `POST-FIX` | Records the discarded raw-argument defect and replacement with `dlogK_ds`, lines 173–186; final arithmetic checks passed, lines 190–210 | No |
| [`LAW_STRIP_AND_MIRROR.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_STRIP_AND_MIRROR.md:3) | `USES-MAGNITUDE-ONLY` | Tasks are explicitly `|φ_q|` and modulus mirror ratios, lines 3–13; code paths use independent continuation and magnitudes, lines 105–117 and 295–316 | No |
| [`LAW_U1_GROWTH.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_U1_GROWTH.md:231) | `USES-MAGNITUDE-ONLY` | Critical-line assembly is a modulus check, lines 231–258; guard receipts are determinant absolute values, lines 712–725 | No |
| [`LAW_U1PHI_PROOF_ROUTE.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_U1PHI_PROOF_ROUTE.md:289) | `USES-MAGNITUDE-ONLY` | Uses independent Eisenstein `φ_q` and exact sine-product `E_q`, lines 289–301; receipts explicitly describe `|φ_q|`/`|φ_qE_q|`, lines 543–550 | No |
| [`LAW_U1PHI_TEST.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_U1PHI_TEST.md:217) | `USES-ON-LINE-ONLY` | Phase experiment uses the determinant proxy only at `Re s=1/2`; no off-line `agp_phi` phase evaluation | No |
| [`LAW_RATE_MEASURE.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_RATE_MEASURE.md:69) | `POST-FIX` | Describes the defect and path-integrated fix, lines 69–99; published `D` values explicitly come from the corrected runner, lines 169–177 | No* |
| [`LAW_R1_COSET_STRUCTURE.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_R1_COSET_STRUCTURE.md:116) | `POST-FIX` | Reference validation uses `rate_measure.phi_q` at `1.5+i·10⁻⁸`, lines 116–123; introduced after the corrected RATE pipeline | No |
| [`LAW_R2_RATE_LEMMA_DRAFT.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_R2_RATE_LEMMA_DRAFT.md:254) | `POST-FIX` | Reads measured `D` from the corrected RATE JSON, lines 254–266 | No |
| [`LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_HEJHAL_CH6S12_CH11S3_EXTRACT.md:61) | `POST-FIX` | q=64 completion and slopes explicitly cite the corrected RATE JSON/log, lines 61–71 | No |
| [`LAW_R4_THETA_DEFECT.md`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/LAW_R4_THETA_DEFECT.md:14) | `USES-MAGNITUDE-ONLY` | Reuses only `phi_infty`/`_g_of_s`; it does not consume finite-q `K_q_corrected` phase, lines 14–15 | No |

\*No branch-related rerun. A separate truncation issue remains: [`rate_measure_validate.log`](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes/rate_measure_validate.log:18) fails its `N=24` gate at `t=14`, and the `t=7.0665` RATE rows are not converged. Higher-`N` reruns are needed only if those heights are to be promoted—not because of the branch defect.

## Published-number impact

- **Retained published tables/slopes:** unaffected by this defect.
- **RATE complex differences `D(q;s)`:** phase-sensitive, but all were produced through the post-fix path.
- **Strip/U1/mirror numbers:** unaffected because their code uses independent evaluators or magnitudes only.
- **AGP final numbers:** unaffected; branch-free critical-line paths were used and validated.
- **Known-bad diagnostic:** `LAW_AGAMMA_PROBE.md` line 180 prints the discarded pre-fix example `−8.96`. That number is affected, but it is explicitly labeled as the defect symptom and is not consumed by any retained conclusion.
- **Unknowns:** none among direct executable consumers. Citation-only prose mentioning `φ_q` without executing an evaluator was excluded from the consumer set rather than guessed into a classification.
