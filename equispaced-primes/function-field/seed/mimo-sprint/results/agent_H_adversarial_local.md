# Agent H — adversarial red-team of D2/D3 outputs

Reviewed materials:
- `results/d2_numerics_draft.md` (Day 1 close)
- `results/agent_B_asymptotic_local.md`
- `results/agent_D_deltaff_null_local.json`
- `results/agent_F_mrho_artin_local.md`
- `results/agent_G_D2_stub.lean`
- `results/agent_E_s3_1e9.log`, `results/agent_E_d4_1e9.log`
- `projects/ak-bias-followups/SESSION.md` (existing)

Lens: catch patterns analogous to the documented inflations in
- `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_dpac_status.md` (9×–52× margin → killed)
- `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_d3_binfty_citation_lock.md` (Annals 170 → fabricated)
- `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_farey_prior_art.md` (static Farey ↔ Mertens already published).

## Findings

### H-001 — `cherry_picking` — MAJOR — **already fixed in d2_numerics_draft.md**

**Original SESSION.md table** reported only A=1 for (q=2, M=T³): C=+0.50449, 0.45% rel err. Three other classes existed but went unreported. A=5 (also QR) measured +0.4452 (10.9% err). Pattern: selecting the most flattering of several measurements without disclosing the spread.

**Status**: caught by local re-run of compute.py (Agent A). The draft now reports all 4 classes + the QR-coset average (+0.4748 = Ex 3.6 exactly) + the analytic order-4-char split formula explaining the spread.

**Sign-off**: this finding is **resolved** in the draft. No further action.

### H-002 — `delta_ff_finite_N_artifact` — BLOCKER (resolved) — δ_ff=1.0000 framing

**Original SESSION.md framing**: "δ_ff = 1.0000 over n ≤ 22 (the unconditional analogue of R-S's GRH+LI-conditional 0.9959)". This phrasing claims an *asymptotic* result (R-S's 0.9959 is asymptotic).

**Locally verified** by null simulator (200k trials): P(δ_ff(N=22) = 1 | LI null, conjugate-constrained zeros) = **0.0414**. Under the symmetric null, the asymptotic δ* = 1/2 exactly (no asymptotic bias).

So δ_ff = 1.0000 at N=22 is (a) marginal evidence (P ≈ 4%, just below 5%); (b) NOT analogous to R-S's asymptotic 0.9959. The phrasing systematically conflates finite-N observation with asymptotic claim.

**Pattern recognition**: this is **the same shape** as the DPAC "9×–52× margin" — a clean number at small sample size that doesn't survive null analysis.

**Status**: downgraded in draft. The new framing is: "δ_ff = 1.0000 at N = 22 is marginally inconsistent with the LI null (P ≈ 4%); the asymptotic δ* = 1/2 by symmetry, so this is not an analog of R-S's 0.9959".

**Sign-off**: **resolved**. The draft no longer carries the inflated framing. Recommend the *original SESSION.md table also be updated* with the correction note, so future readers don't grab the old phrasing.

### H-003 — `citation_check_KKK` — MINOR

**Claim**: "unconditional in char(K) > 0 by Kaneko–Koyama–Kurokawa" (AK ref [18], cited in AK p.238 line 361).

**Verification needed**: confirm the existence and exact venue of the Kaneko–Koyama–Kurokawa paper. The paper is titled "Toward the Deep Riemann Hypothesis for GL_n" or similar; per `project_d3_binfty_citation_lock.md`, ALL citations should be verified before paper submission. 

I have not independently verified this citation here (no web access in the sandbox). 

**Recommended fix**: before any external draft of D2 ships, confirm Kaneko–Koyama–Kurokawa exact citation: journal, volume, year, page, title. The `project_d3_binfty_citation_lock` "Annals 170 Soundararajan" precedent shows confident-sounding citations can be wholly fabricated; this one needs to be checked. Flag as a **must-verify** before submission.

### H-004 — `frohlich_queyrut_citation` — MINOR

Agent F cites Fröhlich–Queyrut, "On the functional equation of the Artin L-function for characters of real representations", *Invent. Math.* 20 (1973), 125–138. I have used this citation from memory of the standard root-number literature, but it is unverified in the sandbox.

**Recommended fix**: spot-check title, journal, volume, year, pages on MathSciNet or ZbMATH before paper ships. The Fröhlich–Queyrut paper does exist; the danger is misremembering year/volume (the volume number 20 vs 17 etc. matters for citation integrity).

### H-005 — `novelty_boundary_D2` — CLEAN

**Claim**: "The novel piece is the *function-field unconditional* verification of AK Thm 3.4 with explicit per-class L-value certificates and a finite-window explanation of the LSQ-slope spread."

**Cross-check against prior art lens**:
- AK Thm 3.4 itself is **not** claimed as novel — it's stated as the theorem being verified.
- Cox–Ghosh–Sultanow (static Farey ↔ Mertens) is in a different direction (Farey sequence, not Chebyshev bias in function fields). Not in conflict.
- The "unconditional finite-data" framing parallels but does not duplicate AC §8 (which concerns the dynamical Farey-cocycle setup). Different theorem family.

**Sign-off**: **clean**. The novelty boundary is appropriately stated and survives prior-art scrutiny.

### H-006 — `novelty_boundary_D3` — CLEAN

**Claim**: D3 paired Q_8 fields give "AK Example 2.1 bias-direction reversal".

**Cross-check**: AK Example 2.1 itself is in the original AK paper — the *theorem-prediction* of reversal is theirs. What we add is a *concrete pair* of LMFDB fields (8.8.12230590464.1 vs 8.0.12230590464.1) where the reversal is observed numerically (10⁹ sweep) and supported by independent Artin/root-number analysis (Agent F).

**Risk**: if AK §2 already names this exact pair of LMFDB fields, our contribution shrinks to the numerics. **Recommended fix**: before paper ships, check whether AK §2 includes this specific pair or just states the existence-of-pairs in the abstract. (I do not have AK in the sandbox to check.)

### H-007 — `d4_field_class_residuals_asymmetric` — MINOR

In `agent_E_d4_1e9.log`, the σ=s and σ=rs residuals at X=10⁸ are +1.0521 and −0.8742 respectively. AK Thm 2.2 (ii) predicts both have the same M(σ) = −1/2 leading-loglog-X coefficient, but allows different (class-specific) constant terms c(σ).

The data is **consistent with AK Thm 2.2 (ii)** — the residuals are bounded (not growing with log log X across X ∈ [10⁶, 10⁸]). The class-specific c(σ) difference between s and rs is allowed by the theorem.

**Worth noting in the paper**: if anyone reads the d_4 logs naïvely, they might misinterpret the residual asymmetry as a violation. A one-sentence note in the paper would prevent that reading.

**Status**: minor framing recommendation. Not a blocker.

### H-008 — `inflation_language_sweep` — CLEAN

Scanned `d2_numerics_draft.md` and supporting files for inflation language: "first", "proves", "establishes", "rigorous", "breakthrough".

- "first" — appears once in the (now-revised) summary table referring to "first honest draft"; OK (not a claim about results).
- "proves" — not present in result claims.
- "establishes" — not present.
- "rigorous" — not present.
- "breakthrough" — not present.
- "unconditional" — used appropriately (the theorem is unconditional over function fields).

**Sign-off**: **clean**.

### H-009 — `lean_stub_not_compiled` — MINOR

`agent_G_D2_stub.lean` is a target statement, body=sorry. It is NOT verified to type-check against the actual mathlib pin in `primes-equispaced/`. The `m_sigma_zero_at_T3_A1` placeholder is `Prop := True` — uninformative.

**Recommended fix**: when this stub is moved to actual development in a follow-up sprint, the `m_sigma_zero_at_T3_A1` proposition needs a substantive definition (referencing nonvanishing of L-functions). Don't claim "the stub is in Lean4" without a `lake build` pass.

### H-010 — `mimo_sprint_methodology_disclosure` — STRENGTH

The draft explicitly discloses that MiMo agents failed to produce output and that the work was completed locally. This is unusually candid for a sprint write-up and prevents future readers from over-attributing capability to the MiMo platform. **Keep this disclosure** in any externally-facing version.

## Overall verdict

**Status of D2 §Numerics draft**: post-honesty-pass, the draft is materially **stronger** than the SESSION.md original because each headline number is either (a) replaced by a coset-averaged number with structural justification (the cherry-picked +0.50449 → QR-average +0.4748 + order-4 explanation), or (b) appropriately downgraded with a null-analysis context (δ_ff = 1.0000 → marginal evidence at N=22).

No BLOCKER findings remain unresolved. Two MINOR findings (H-003, H-004) are citation spot-checks that must be done before any external ship. One MINOR finding (H-006) requires confirming AK §2 does not pre-empt the specific LMFDB-field-pair attribution.

**Sign-off**: CLEAN (subject to pre-ship citation verification).

```json
{
  "findings": [
    {"id": "H-001", "category": "cherry_picking", "severity": "MAJOR", "status": "RESOLVED_in_draft", "details": "SESSION.md reported only A=1 of 4 classes. Re-run reveals 4-class spread. Draft revised."},
    {"id": "H-002", "category": "delta_ff_artifact", "severity": "BLOCKER", "status": "RESOLVED_in_draft", "details": "delta_ff=1.0000 at N=22 had P(=1|null) approx 4 percent. Framing replaced."},
    {"id": "H-003", "category": "citation", "severity": "MINOR", "status": "OPEN_MUST_VERIFY", "details": "Kaneko-Koyama-Kurokawa exact citation unverified in sandbox."},
    {"id": "H-004", "category": "citation", "severity": "MINOR", "status": "OPEN_MUST_VERIFY", "details": "Frohlich-Queyrut Invent.Math.20 (1973) cited from memory."},
    {"id": "H-005", "category": "novelty_boundary", "severity": "OK", "status": "CLEAN", "details": "D2 novelty stated appropriately."},
    {"id": "H-006", "category": "novelty_boundary", "severity": "MINOR", "status": "OPEN_CHECK_AK_S2", "details": "Confirm AK §2 doesnt name this exact LMFDB pair."},
    {"id": "H-007", "category": "framing", "severity": "MINOR", "status": "RECOMMENDATION", "details": "Add note to paper that d_4 s/rs class-specific c constants are allowed by AK Thm 2.2 (ii)."},
    {"id": "H-008", "category": "inflation_language", "severity": "OK", "status": "CLEAN", "details": "No inflated verbs in result claims."},
    {"id": "H-009", "category": "lean_stub", "severity": "MINOR", "status": "OPEN_DEFERRED", "details": "Stub not lake-build verified; placeholder m_sigma proposition is True."},
    {"id": "H-010", "category": "methodology_disclosure", "severity": "STRENGTH", "status": "PRESERVE", "details": "MiMo failure mode explicitly disclosed; keep in external version."}
  ],
  "blockers": [],
  "must_verify_before_ship": ["H-003", "H-004", "H-006"],
  "overall_verdict": "CLEAN",
  "sign_off": true
}
```
