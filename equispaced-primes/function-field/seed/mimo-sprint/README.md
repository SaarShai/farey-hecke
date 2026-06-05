# MiMo 2-Day Sprint — D2 ship + D3 companion

**Target**: ship D2 (function-field unconditional Chebyshev bias) as the lead deliverable; D3 (paired Q_8 same-disc opposite-m_ρ) as companion note. See `../SESSION.md` for direction context.

**Why MiMo**: RLVR-trained on math with verified rewards. Sweet spot = symbolic asymptotic derivation, cross-implementing the same numerical experiment, step-by-step proof checking, Lean4 lemma drafting. Used here as parallel math-workhorse; Claude orchestrates + audits novelty boundary + writes up.

## Layout

- `prompts/agent_A_*.md` … `agent_H_*.md` — self-contained dispatchable prompts (8 agents)
- `results/` — agent JSON outputs land here
- `dispatcher/dispatch.py` — driver that POSTs each prompt to MiMo and saves response
- `dispatcher/MIMO_API.md` — endpoint + auth notes (filled in once user provides key)

## Schedule

| Day | Agents | Output |
|---|---|---|
| 1 | A (sieve cross-impl), B (next-order correction), C (L-cert), D (δ_ff null) | D2 §Numerics draft |
| 2 | E (S_3 to 10⁹), F (m_ρ Artin), G (Lean stub), H (adversarial) | D2 paper draft + D3 note + Lean stub + log entry |

## Gates

- Agent A's cross-impl must confirm the (q=2, M=T³, A=1) +0.50449 number ±1e-6 before that line ships.
- Agent D's null check must clear the δ_ff=1.0000 claim, or that claim is downgraded to "consistent with null at n≤22".
- Agent H must sign off "clean" or flag ≥1 blocker. Flagged blockers gate ship.

## Honesty norms

This sprint inherits the project's anti-inflation discipline. See:
- `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_farey_honest_map.md`
- `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_dpac_status.md` (9×–52× margin → killed pattern)
- `~/.claude/projects/-Users-za-Documents-Farey-NOW/memory/project_d3_binfty_citation_lock.md` (Annals 170 → fabricated; check before any citation)

Better to ship a smaller honest claim than a bigger inflated one.
