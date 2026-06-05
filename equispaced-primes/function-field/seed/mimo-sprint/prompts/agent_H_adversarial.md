---
agent: H
day: 2
purpose: Red-team D2/D3 written claims for inflation patterns, citation fabrication, novelty-boundary overreach
---

# Agent H — Adversarial red-team of D2/D3 claims

## Context — and the patterns we're hunting for

This project has a documented history of catching inflated claims **before they shipped externally**. Three priors:

(1) **"9×–52× avoidance margin"** in DPAC PR #3716 — REFUTED as a sample-size artifact. The original framing claimed a strong statistical separation; deeper analysis showed the margin was driven by N, not by the underlying signal. See `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_dpac_status.md`.

(2) **"Annals 170 Soundararajan"** citation — FABRICATED. The actual citation is Crelle 631, not Annals 170. See `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_d3_binfty_citation_lock.md`. The pattern: an inflated-confidence write-up referenced a citation that did not exist, with a plausible-sounding journal/volume/year.

(3) **"Static Farey ↔ Mertens = novel"** — REFUTED. Cox–Ghosh–Sultanow arXiv:2105.12352 (2021) already had it. The novel piece is *dynamical / per-step BCZ-cocycle*. See `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_farey_prior_art.md`.

Your job is to find any analog of (1), (2), or (3) in the D2/D3 sprint outputs before they ship.

## Your task

Review the following materials:

- `projects/ak-bias-followups/SESSION.md` (existing D2/D3 write-up)
- `projects/ak-bias-followups/mimo-sprint/results/agent_A_sieve_xcheck.json` (cross-impl)
- `projects/ak-bias-followups/mimo-sprint/results/agent_B_asymptotic.json` (correction)
- `projects/ak-bias-followups/mimo-sprint/results/agent_C_lvalue_cert.json` (m(σ)=0 cert)
- `projects/ak-bias-followups/mimo-sprint/results/agent_D_deltaff_null.json` (null check)
- `projects/ak-bias-followups/mimo-sprint/results/agent_E_s3_sweep.json` (D3 sweep)
- `projects/ak-bias-followups/mimo-sprint/results/agent_F_mrho_artin.json` (D3 Artin)
- (Day-1 close write-up draft, located at `projects/ak-bias-followups/mimo-sprint/results/d2_numerics_draft.md`)

Scan for:

**A. δ_ff finite-N artifact (cross-ref Agent D).** If Agent D reports `P(δ_ff = 1 | null, N=22) ≥ 0.05`, the δ_ff = 1.0000 framing must be downgraded in the write-up. Check: is the downgrade actually applied, or did the draft preserve "δ_ff = 1.0000" as a headline?

**B. Citation pattern.** Every external citation in the D2/D3 outputs and SESSION.md gets independently verified. For each:
   - Confirm journal + volume + year + page match.
   - Specifically check: AK ref [18] (Kaneko–Koyama–Kurokawa "Toward DRH for GL_n") — verify exact title/journal/year.
   - Specifically check: any reference to "Annals" volumes by Soundararajan (per prior, this is the fabrication smell).
   - Specifically check: "Akatsuka 2013/2017" (Kodai 40, not 2013) — see `project_d3_binfty_citation_lock`.

**C. Novelty boundary.** D2's positioning vs prior art:
   - Is the (q=2, M=T³) +0.50449 number presented as novel? AK §3.4 is the *theorem*; what's novel here is the *unconditional verification* + δ_ff numerics. Confirm framing isn't "we proved AK Thm 3.4" (false).
   - D3 reversal: claimed in AK Example 2.1 already? Confirm framing isn't claiming the reversal as new.
   - δ_ff = 1.0000: is this presented as proving the function-field RS density is 1? If Agent D's null is consistent with 1, the *unconditional* part of the claim is empty.

**D. Inflation language sweep.** Scan for: "first unconditional", "proves", "establishes", "rigorous", "breakthrough". For each, verify the supporting math actually backs the strength of the verb.

## Output format

```json
{
  "findings": [
    {
      "id": "H-001",
      "category": "delta_ff_artifact" | "citation" | "novelty_boundary" | "inflation_language",
      "severity": "BLOCKER" | "MAJOR" | "MINOR",
      "location": "<file:line or section>",
      "claim": "<quoted text>",
      "issue": "<one sentence>",
      "recommended_fix": "<one sentence>"
    }
  ],
  "blockers": [<ids of BLOCKER findings>],
  "overall_verdict": "CLEAN" | "NEEDS_REVISION" | "BLOCKED",
  "sign_off": true | false
}
```

## Norms

- Be ruthless. False positives are cheap; false negatives ship inflated claims that get refuted later.
- Cross-reference the three memory files cited above. They are the project's anti-inflation record; new findings should resemble them.
- If everything is clean, say so with a clear sign-off. Don't manufacture findings.
- A finding can be MAJOR/MINOR even if not a BLOCKER. Only BLOCKER stops the ship.
