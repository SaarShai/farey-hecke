# Riemann-zeta asset synthesis — 2026-08-14

Full-repo sweep (5 codex gpt-5.6-luna xhigh search agents over research_notes/,
wiki+facts, engine+code, equispaced-primes/, projects/) plus direct audit.
Trigger: the Anthropic article (anthropic.com/research/riemann-zeta) — an
unreleased Claude raised the proven critical-line proportion of zeta zeros from
41.6% to 67.2% via idea fan-out → numerical falsification → adversarial
refereeing → Lean formalization. Same pipeline shape as this repo. Goal: pick 3
aims where this repo's verified bank can produce article-style measurable
partials toward RH. Maps: GOAL1_MAP.md, GOAL2_MAP.md, GOAL3_MAP.md.

## A. Verified capabilities (the bank)

1. **Zeta zeros as certified transfer-operator resonances.**
   det(1−L⁺_s)=0 ⟺ ζ(2s)=0 at q=3 (Mayer/Gauss-map operator). Certified vs
   Odlyzko to ~1e−13; argument-principle winding counts; Newton refinement to
   1e−15. Resonance geometry = arithmeticity signature: q=3 zeros rigid on
   Re=¼ (std 6.5e−14) vs non-arithmetic G_5 scattered cloud (std ~0.04).
   CAUTION: the code (Aletheia engine, zeta_cert_q3.py, zeta_mayer_rosen.py,
   hejhal_g5/g8) is NOT on HEAD or main — only on codex/declusteraudit* side
   branches, commits c779fc6 → 092ae7d → b973d56. Restore before use.
2. **Independent Arb/FLINT critical-line-zero certificate.** Conductor-19
   Dirichlet L, γ ≈ 0.0189563990802261, bracket width 5.9e−84, Hardy sign
   change, PARI-independent. Existence only — no completeness/GRH claim.
   projects/minus1-dominance/spectral_transients_3e14/independent_n19/.
3. **Zero-recovery-from-primes pipeline (MUSIC/Prony + periodogram).**
   Real, non-circular (5/5 Dirichlet zeros <0.3%; 10/10 ζ zeros 0.04–0.5%;
   function-field 0.0°). KILLED as a tool (fair windowed FFT ties it;
   no super-resolution niche — SPECTROSCOPY_GATE_RESULTS.md). Surviving
   residue: explicit-formula-as-line-spectrum reframing + O(d)/Cramér–Rao
   sample-complexity question — 101-agent novelty scan says unaddressed.
4. **Lean-proved exact identities.**
   - Farey Bridge Identity (unconditional): Σ_{f∈F_{p−1}} e^{2πipf} = M(p)+2.
   - Local Perron residue at a simple L-zero (zero-sorry):
     Res_{w=0} K^w/(w L(ρ+w)) = log K/L′(ρ) − L″(ρ)/(2L′(ρ)²).
   - Boundary Euler-product prime-power decomposition at Dirichlet L-zeros
     (proved unconditionally; standalone novelty gate FAIL — support material).
   - K≤4 DPAC ceiling (elementary, proved). General DPAC research-open;
     NOT implied by LI of zeta ordinates.
5. **Prime-step / Mertens bridge (frozen, proof-qualified).**
   E_p−E_{p−1} = ((p−1)/6p)(2−A(p−1)) with A(x)=Σ_{m≤x} M(⌊x/m⌋)/m;
   Σ a(n)/n^s = ζ(s+1)/ζ(s); RH ⟺ A(x)=O(x^{1/2+ε}) (standard, labeled so).
   First negative prime step p=8501 finite-certified. Triangular limit law
   proof-qualified.
6. **Function-field unconditional suite** (Weil RH is a theorem there):
   FF Mertens exponent exactly 1/2; C_FF(q)=(q+1)²; δ_ff = 1.0000 by
   exhaustive enumeration (deg ≤ 22, 387,975 irreducibles) vs
   Rubinstein–Sarnak GRH+LI-conditional 0.9959; L-zero phase recovery 0.0°;
   min-entropy certificates.
7. **Zero data + universality diagnostics.** Odlyzko 2,001,052 zeros + windows
   at 10^12/10^21/10^22; LMFDB Δ zeros; cluster diagnostic confirming ζ in
   GUE class (f(size2) < 0.034%, >2794× below Farey/BCZ structural level).

## B. Live conjectures with evidence (ours)

- NW(Q) → C ≈ 0.679 ± 0.002 (Mertens NW; explicitly not a theorem). CONFLICT
  (found 2026-08-14 import): snapshot note FRANEL_LANDAU_LOWER_BOUND fits the
  same quantity as C_W ≈ 0.16 + 0.24·log log N (slowly divergent). Settle in
  Goal 3 S0.
- Σ_ρ 1/(|ρ|²|ζ′(ρ)|²) = 2/π² (log.md, from Mikolás constant 2/3) — but
  mimo E5 probe got S(N=100)=0.0141 vs expected 0.2014. UPDATE 2026-08-14:
  imported SELBERG_INPUT_DISPROVED records the literature-known RH-conditional
  value ≈ 0.03; E5's 0.0141@100 zeros is consistent with slow convergence to
  ≈0.03, so the 2/π² bridge likely has a normalization error. Goal 3 S0
  confirms and locates it.
- Σ M(n)²/n³ = 1.13616230745460 — possibly-new constant, novelty unverified.
- DPAC: 300–6000 certified nonzero cases, K=5 first open; conjecture-with-
  evidence tier.

## C. Falsified / dead (do not re-chase; see also memory DO-NOT-RE-CHASE)

- Spectroscopy-as-tool (Gates 0–3 + close-pair probe: KILL).
- Pointwise Mertens sign claims (p=92,173; p=237,733; p=243,799 certified
  counterexamples). Universal-dominance of −1 (backwards per Fiorilli–Martin;
  −1 maximizes variance, minimizes bias).
- Universal 1/ζ(2) EC constant (sym² collapse falsified it); c_K global
  asymptotic (off-target zeros oscillate with |K^{ρ'−ρ}|=1, no o(1)).
- 9–52× DPAC "avoidance anomaly" (sample-size artifact).
- Farey spectroscope as ζ-zero detector = circular (already disclaimed).
- spectroscope/README.md headline numbers (434 Lean theorems, R=0.952,
  9000:1): referenced artifacts absent from repo; treat as unaudited.

## D. The "new perspective" (what the user remembered)

Two genuinely-ours reframings:
1. **Zeta zeros as the rigid fiber of a resonance family.** The same certified
   operator that yields ζ zeros at q=3 yields scattered resonance clouds for
   non-arithmetic Hecke groups. "Zeros on a line" is the arithmetic-rigidity
   phenomenon inside a deformation family — RH's geometry seen as the q=3
   special case. (Goal 2.)
2. **The explicit formula as a line spectrum; primes as measurements of
   zeros.** Inverse problem: how much prime data determines the zeros to what
   precision. Information-theoretic, unscooped. (Goal 1.)

## E. Goal triad (each map = separate file)

- GOAL 1 — Sample-complexity theory of zero detection from prime data.
- GOAL 2 — Certified resonance program: ζ zeros + arithmetic-rigidity
  deformation measurements.
- GOAL 3 — Unconditional Farey–Mertens structure: DiscrepancyStep theorem +
  the ζ′(ρ) zero-sum constant.

Niche-doctrine check: each headline is a NEW fact (a bound, a measured
rigidity law, an unconditional theorem/constant), not verification of the
known. DO-NOT-RE-CHASE check: no pivot to per-step significance claims, no
spectral lever, no Veech, no twin primes, no QMC tooling.
