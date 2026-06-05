# Applications + Core-Math Audit — consolidated findings (2026-06-05)

Session goal: honestly assess the practical-application directions and core math
claims of this research — confirm/falsify early, kill what doesn't survive,
keep only what's verified. Every claim was gated against null/baseline/literature
and, where possible, INDEPENDENTLY recomputed (not trusting prior self-grades).

Detail docs: `SPECTROSCOPY_GATE_RESULTS.md`, `CORE_MATH_VERIFICATION.md`.
Code: `code/gate2_clean_recovery.py`, `code/gate2b_fair_periodogram.py`,
`code/gate3_finite_d.py`, `code/probe_close_pair.py`, `code/verify_core_math.py`,
`code/priority_nesting_probe.py`, `code/final_kill_test.py` (comms probe).

---

## 1. Communications-coordination direction

### 1a. "Silent coordination" / Farey-Prime TDMA  — DEAD as a product
(Artifacts in the Farey NOW tree: SILENT_COORDINATION_APPLICATIONS.md,
PATENT_DRAFT_SILENT_COORDINATION.md, DRONE_SWARM_KILL_TEST.md,
MILITARY_EMCON_TRIPLECHECK.md, DATACENTER_FAREY_REPORT.md, IOT_LORAWAN_*.)
- The project's own kill-tests already showed: "zero-communication" needs global
  agreement on fleet size N (= communication); ~100× worse clock-drift
  sensitivity than uniform TDMA; utilization gain ~5%, not 15-25%.
- Added this session: the monotone-nesting differentiator is **dominated** by two
  trivial alternatives — a uniform big frame (drift-tolerant, grows to a fixed
  cap) and dyadic bisection (near-uniform gaps). Farey gives nothing they lack
  and is worse on min-gap. Kill stands.

### 1b. Priority-nesting sub-lead — ALIVE but MINOR/conditional
(code/priority_nesting_probe.py, code/final_kill_test.py; PRIORITY_NESTING_PROBE.md,
FINAL_KILL_TEST.md in the Farey NOW tree.)
- The one place Farey is NOT dominated: non-disruptive HETEROGENEOUS-priority
  allocation. For heavy-tailed priorities, Stern-Brocot beats dyadic ~2.5-3× on
  proportional-allocation error (~5× worst-case), as a zero-comm, non-disruptive,
  design-free, full-utilization-at-every-size nested palette.
- Bounded niche (4 conjunctive conditions): heavy-tailed priorities + unknown
  final size + full bandwidth wanted at every growth stage + modest N / good
  clocks. Outside it: dominated (uniform/dyadic/WFQ/target-matched oracle).
- Open: not proven optimal among all universal nested palettes; discrete-slot
  model untested. Significance Level 1 at best.

---

## 2. Spectroscopy direction (MUSIC/Prony L-zero recovery) — TOOL KILLED
Full record: `SPECTROSCOPY_GATE_RESULTS.md`.
- **Gate 0 novelty (deep-research, 101 agents): PASS** — inverse algorithmic
  recovery of zeros from prime counts via parametric estimators is unpublished.
  Nearest prior art = spectral DISPLAY (Lan-Yong/Wolf ψ-fluctuation power
  spectrum; Csoka DFT): same signal, peaks at γ, but display not recovery.
- **Gate 1 reproduction: PASS** after debugging. Committed `D_number_field_music.py`
  was broken (spurious peaks, circular γ-scaling). Clean rewrite recovers 5/5
  low zeros of L(s,χ₄) as top-5 peaks in order, <0.3%, non-circular.
- **Gate 2 obviousness: FAIL (decisive).** A fair Hann-windowed periodogram
  recovers the same 5/5 at <0.34% and ties MUSIC at every sample count. For the
  abundant-data number-field case the parametric method buys nothing over the FFT
  display already in the prior art.
- **Gate 3 + close-pair probe: FAIL.** Sub-Rayleigh super-resolution (the only
  regime parametric can win) has no application home (function-field zeros come
  from direct point-counting, also O(d)); and on real arithmetic data a close
  cross-character pair (sep 0.36) is NOT robustly resolved — MUSIC's lone success
  was non-monotone in X (fluke), even with oracle source count.
- **Verdict:** kill as a tool. Residue: a modest theory note (explicit-formula-
  as-line-spectrum + O(d)/Cramér-Rao sample-complexity, confirmed unaddressed in
  literature). Not SOTA-beating.

---

## 3. Core math claims — independent verification
Full record + numbers: `CORE_MATH_VERIFICATION.md` (code/verify_core_math.py).

| Claim | Verdict |
|---|---|
| **K≤4 unconditional non-vanishing** of c_K(s)=Σ_{k=2}^K μ(k)k^{-s} | **VERIFIED CORRECT (minor).** Proof elementary & sound; min on Re=½ = 2^{-½}−3^{-½}=0.12976. Independently **found actual c₅ zeros in the strip** (σ=0.582,γ=9.293; …) → "elementary iff K≤4" boundary confirmed both directions. Lean-formalized. Novelty uncertain (may be folklore). |
| **Avoidance anomaly** (c_K zeros repel ζ zeros 9×–52×) | **REFUTED.** Sample-size artifact (repo's own audit + my reproduction): median\|c_K\|@zeros ≈ @control; ratio only tracks control density. Survivor: 6000/6000 certified c_K≠0 = conditional numerical evidence for DPAC. |
| **Universality + RIP** | **OVERSTATED; cores known.** Prime↔zero duality = Guinand–Weil explicit formula (known); "any Σ1/p=∞ subset detects every zero" is not a theorem (divergence ≠ resonance); Maynard–Tao corollary a non-sequitur. "Large sieve = RIP" is a false conflation — large sieve is one-sided; RIP needs two-sided uniform isometry; correct arithmetic→RIP route is Bourgain et al. (Duke 2011). No proof in repo. |
| **Per-step Franel–Landau / ΔW + 33,000:1** | **One correct minor lemma; grand claim unsupported.** ΔA(N)=(1/3)φ(N)+(1/(6N))Π_{p\|N}(1−p) verified exactly (N=2..30). But one component only; full wobble has no closed form; "known in spirit" (Franel/Landau/Mikolás/Huxley); "33,000:1" not substantiated in source (only timing logs). |

---

## 4. Bottom line
Across comms, spectroscopy, and the core math claims, the same pattern held:
**every flashy/application/tool claim collapsed under gating; what survives is
small, correct, and probably known.**

Verified survivors:
- K≤4 non-vanishing boundary (+ c₅ vanishes in strip) — verified, formalized, minor.
- ΔA(N) closed form — verified, minor, likely known.
- 6000/6000 certified c_K≠0 — conditional numerical evidence for DPAC.
- Priority-nesting result — real, non-dominated in a narrow niche, Significance L1.

Dead/overstated: silent-coordination TDMA; spectroscopy-as-tool; avoidance
anomaly; universality/RIP as stated; the grand ΔW/per-step framing.

Out of scope (unaudited, separate): Koyama replication; the Lean/Hecke proof.
The durable value of this research = verified formal math (pending a Hecke/Lean
build audit) + the gating/kill-test discipline that retired the rest.
