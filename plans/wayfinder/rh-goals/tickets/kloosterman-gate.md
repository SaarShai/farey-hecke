# Kloosterman DiscrepancyStep gate spec + probe

- Type: research
- Mode: AFK
- Status: closed (NO-GO, 2026-08-14)
- Claimed by: frontier (gate spec WRITTEN — KLOOSTERMAN_GATE_SPEC.md); step-1 probe = lane K1 (codex luna); frontier adjudicated
- Blocked by: sample-complexity-t1.md (frontier bandwidth ordering only)
- Source: GOAL3_MAP S1 (sanctioned salvage, breakthrough-picks 2026-07-02); "execute!" wave 2026-08-14

## Question
Write the pre-registered gate (what Kloosterman/Weil variance bound
suffices; what falls short = NO-GO), then: does the bound land, giving the
unconditional DiscrepancyStep theorem?

## Resolution
NO-GO, recorded per the pre-registered binding condition. Step-1 extraction
(lane_i/V_EXTRACTION.md + v_extraction_receipt.json, exact rationals,
probes p = 13, 8501, 92173 all zero-error) found two independent kill
grounds, adjudicated by frontier 2026-08-14:

1. SPEC DEFECT (logged amendment): the pre-registered inequality
   "N + B + C > A" has no source-defined semantics for the FROZEN integral
   observable — the four-term decomposition exists only for the older
   discrete Franel–Landau observable (main.tex:921-954). Direct witness:
   at p=13, ΔW_disc = −663287/249819570 ≠ ΔW_integral = −95083/180180.
   The integral protocol's own step formula is ΔW(p) = (p−1)/(6p)·(A(p−1)−1)
   with NO A,B,C,N split.
2. STRUCTURAL (the binding NO-GO): the only source-backed fluctuation
   object is V_residue(p) = Σ_c M(⌊(p−1)/c⌋)·s(p,c) — a Dedekind-sum
   convolution carrying MERTENS-function weights. The frozen paper itself
   rules the direct Kloosterman completion invalid (main.tex:1056-1064):
   there are no complete S(m,n;c) sums to Weil-bound, and any bound at the
   required level embeds Mertens cancellation, i.e. RH-strength input —
   exactly the pre-registered stop condition ("more than Weil-square-root
   cancellation ... RH-strength input ⇒ NO-GO"). No extensions past the bar.

Consistent with the 2026-06-29 per-step verdict (RH-coupled-unreachable).
NO-GO deliverable per spec: the documented reduction (V_EXTRACTION.md) is
the precise-open-problem material for the D3 note's outlook section.
