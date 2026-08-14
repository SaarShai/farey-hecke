# GOAL 2 — Certified resonance program: ζ zeros and arithmetic rigidity

Preliminary map, 2026-08-14. Status: DRAFT — no work started.
Absorbs breakthrough Pick B (certified G_5/G_7 spectra, unscooped per
2026-07-02 scout) and the resonance-geometry arithmeticity signature.

## Aim

Turn the certified transfer-operator route to zeta zeros into (a) a
first-of-kind certified resonance atlas across the Hecke family and (b) a
quantitative **rigidity law**: how the perfect Re=¼ line of ζ-zero resonances
at q=3 breaks into a scattered cloud as arithmeticity is broken. RH's
geometry ("zeros on a line") studied as the rigid fiber of a deformation
family, with certified numbers.

## Why this is RH-relevant

For the modular surface, det(1−L⁺_s)=0 ⟺ ζ(2s)=0: RH is literally
"resonances confined to Re=¼." The family view asks WHAT enforces the
confinement — arithmetic rigidity — and measures its breakdown. This is a
new-perspective contribution of the kind the article gestures at: not a proof
attempt, but new structure/data around the critical-line phenomenon, feeding
Phillips–Sarnak deformation theory. The certified zero-localization route is
also Riemann–Siegel-independent verification technology.

## What we already hold (verified)

- q=3 VALIDATION (rigorous, adversarially reviewed): det(1−L⁺_s) vanishes
  exactly at s=¼+iγ_n/2 for γ_1..γ_8 (|det|→1e−7, Newton 1e−15, winding
  counts 1/2/3, certified vs Odlyzko). Re-scatter std 6.5e−14.
- G_5 even-sector resonances: ~9 N-stable, machine-precision; 3 reproduced by
  independent collocation (4.1e−9, 1.4e−7, table-precision). G_7 reproduced
  (2.2e−4/2.6e−4). Certified band counts. Essential gap 0.015.
- G_5 odd Maass spectrum cross-validated (Hejhal point-matching, 5 sig figs);
  q=3 anchor interval-certified 6/6 (Arb 280-bit).
- Arithmeticity signature: line (q=3) vs cloud (G_5), 12 orders of magnitude
  in Re-std on the same engine.
- MMS convention pinned from source (research_notes/MMS_0912.2236_EXTRACTION).
- **RESTORE REQUIRED:** engine + scripts only on codex/declusteraudit*
  branches (c779fc6, 092ae7d, 9011338, b973d56); engine/ dir on HEAD is
  empty. Step 0 is recovery + re-verification.

## Headline NEW facts targeted

1. **First certified resonance atlas for non-arithmetic Hecke groups**
   (G_5, G_7, G_8 even sector + odd Maass tables), interval-certified — no
   such tables exist (latest prior computations 2007/2013; scout 2026-07-02:
   unscooped).
2. **Rigidity law:** quantified arithmetic-vs-non-arithmetic resonance
   geometry with controls (arithmetic q=4, 6 must ALSO give rigid lines;
   non-arith q=5, 7, 8 clouds) — promoting the 2-surface illustration to a
   family-level statement: resonance-geometry is an arithmeticity
   discriminant. Certified Re-scatter statistics per q.
3. **Certified ζ-zero localization via Fredholm determinant** with a
   completeness argument (winding = interior count in boxes) — a certified,
   explicitly Riemann–Siegel-free confirmation route for low zeros; document
   as method, not as the headline (verification-flavored on its own).
4. Stretch: perturbation velocity at q=3 — d(scatter)/d(deformation) via the
   character/Teichmüller-style deformation available to the operator (Avelin/
   Phillips–Sarnak numerics exist for eigenvalue destruction; certified
   resonance-cloud velocity would be new).

## Stage ladder with falsification gates

- **S0 (1–2 d).** Restore the stack: cherry-pick/branch from b973d56 (+ the
  53eeb53/4c42ca0 collocation cross-checks), rebuild, re-run the q=3 anchor
  and G_5 table, diff against recorded values. GATE: exact reproduction of
  the recorded certificates, else stop and debug provenance.
- **S1 (1–2 wk).** Controls: arithmetic q=4 and q=6 even-sector resonance
  geometry. GATE: if q=4/6 do NOT show rigid lines, the arithmeticity-
  signature interpretation is falsified → re-scope to the atlas alone.
- **S2 (2–3 wk).** G_8 completion + certified band counts for all computed
  surfaces; assemble the atlas paper skeleton (Exp.Math / Math.Comp / LMS
  JCM per Pick B).
- **S3 (2 wk).** Rigidity statistics: certified Re-scatter per q, line-fit
  residuals, essential-gap table. Adversarial referee pass (the honesty
  caveats from 2026-06-20 stay in: scattering resonances, not "dissolved
  cusp forms located").
- **S4 (open).** CAP cross-check (pseudospectral Ruelle 2507.09021) — the
  known multi-week lever; deformation-velocity stretch goal.

## Kill criteria / risks

- S0 reproduction failure (bit-rot, dependency drift) — budget real time.
- S1 control failure kills the signature claim (keep atlas as fallback).
- Scoop re-check before S2 submission (last scout 2026-07-02).
- Niche-trap honesty: this lane is niche spectral geometry; its RH value is
  the perspective + certified technology, and the paper must say exactly
  that. Do not re-inflate to "progress on RH" in text.
- Dim-tail heuristic in the cert engine (validated, not a-priori-proved) —
  disclose; CAP cross-check is the eventual discharge.
- Scope boundary vs Goal 3 (imported MAYER_SPECTRAL_PROOF.md, 2026-08-14):
  the transfer-operator route does NOT currently yield prime-step/Mertens
  monotonicity statements — that attempt is recorded as speculative and
  unverified. Goal 2 claims stay spectral-side (resonances, rigidity,
  certified tables); no Mertens/Farey-discrepancy corollaries.

## First 3 actions

1. `git worktree add` a restore branch at b973d56; rebuild; re-run
   zeta_cert_q3.py anchor; diff vs recorded 6/6 certificates.
2. Re-verify G_5 even-sector table + collocation cross-check outputs.
3. Draft the q=4/q=6 control run spec (operator sign conventions from the
   MMS extraction note).
