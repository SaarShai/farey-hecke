# Spectroscopy redirect — kill-gate results (2026-06-05)

Target: MUSIC/Prony line-spectral recovery of L-function zeros from prime-count
bias (the higher-ceiling spectroscopy thread). Gated to confirm/falsify early.

Code (farey-hecke/projects/mimo-mini-project/code/):
  gate2_clean_recovery.py, gate2b_fair_periodogram.py, gate3_finite_d.py

## Gate 0 — Novelty (deep-research, 101 agents, 25 claims verified 3-0)
PASS (medium confidence). No prior art does inverse algorithmic recovery of
zeros from prime counts via parametric estimators. Strongest near-miss =
spectral-DISPLAY cluster (Lan–Yong/Wolf power spectrum of ψ(x)−x, Physica A
2006; Csoka DFT of von Mangoldt, 2015/2017): SAME signal, peaks visible at γ,
but display not algorithmic recovery. Q6 (O(d) sample-complexity / Cramér–Rao
for zeros-from-counts) entirely unaddressed in literature.
KEY CONSEQUENCE: the threat is not "already done" but "OBVIOUS given the
displays." Novelty survives only if parametric BEATS the display.

## Gate 1 — Reproduction
Committed D_number_field_music.py: FAILS as-written (top-3 MUSIC peaks γ≈60,48,103
are spurious; γ-axis scaling ambiguous/circular; only 100 samples).
Clean rewrite (gate2_clean_recovery.py, γ-axis fixed a priori via steering
e^{iγ·dn·m}, ground truth fixed before run): PASS. MUSIC recovers 5/5 low zeros
of L(s,χ_4) as the top-5 dominant peaks IN ORDER, all <0.3% error, X=3e7,
400 samples. Null (shuffled residues) does not reproduce → real structure.
=> The METHOD reproduces cleanly; the committed script was just buggy.

## Gate 2 — Obviousness (the crux): parametric vs FAIR periodogram
DECISIVE NEGATIVE. A properly windowed (Hann), detrended, zero-padded Fourier
periodogram recovers the SAME 5/5 zeros at <0.34% error, in correct order, and
TIES MUSIC at every sample count in a sweep (both: 2/3 at N=60, 3/3 from N≥80).
=> For number-field low zeros (the case with abundant data + real external
value, e.g. LMFDB), the parametric method has NO advantage over the FFT display
that already exists in the prior-art near-miss cluster. K2 (obviousness) TRIGGERED.

## Gate 3 — Sample-starved super-resolution (the only regime parametric can win)
Finite-degree (function-field) case: explicit formula is an EXACT finite sum of
K exponentials, so parametric methods can in principle resolve below the Fourier
limit from ~2K samples. Synthetic test (gate3_finite_d.py) was numerically
INCONCLUSIVE at the tiny N required (Hilbert/Hann edge artifacts dominate).
But this regime has NO application home anyway: function-field zeros are obtained
exactly from the first ~d point-counts by the STANDARD method (direct L-poly /
Frobenius), which is also O(d), exact, and simpler (E7 already noted "direct is
vastly superior"). A super-resolution win here would be dominated by direct
computation.

## VERDICT
- As a COMPUTATIONAL TOOL for the community: KILL. No regime found where it
  beats the existing alternative — windowed-FFT display (number field) or direct
  point-counting (function field). The Gate-0 novelty is novelty of FRAMING,
  undercut by the Gate-2 fair-periodogram tie.
- The number-field MUSIC recovery is real and reproduces non-circularly — it
  just isn't BETTER than a windowed FFT.
- Surviving residue (theory, not tool): the explicit-formula-as-line-spectrum
  reframing + the O(d) / Cramér–Rao sample-complexity statement (Q6), which is
  genuinely unaddressed in the literature. Possible modest expository / Exp.Math
  note. Not a SOTA-beating tool.

## Last probe — close-pair super-resolution on REAL data (probe_close_pair.py)
The one untested axis: can parametric resolve a close zero pair from LESS data
than a fair windowed FFT, under real arithmetic noise? Test pair: low zeros
γ=6.8007 (L_{-11}) & 7.1607 (L_{-19}), sep=0.36, combined real prime-bias signal,
MUSIC given ORACLE source count K, X swept to 1.5e8.
RESULT: KILL.
  - FFT: never resolves the pair (X up to 1.5e8).
  - MUSIC: resolves ONLY at X=3e7, then FAILS at 6e7, 1e8, 1.5e8 — NON-MONOTONE.
  - A real super-resolution threshold is monotone in X; the lone success is a
    coincidental noise-peak alignment, not recovery. Even with oracle K.
  - The sub-Rayleigh edge evaporates under real arithmetic fluctuation, as the
    super-resolution-under-noise literature predicts.
=> No surviving tool niche on any tested axis.

## FINAL STATUS
Spectroscopy-as-tool: comprehensively killed across Gates 0-3 + close-pair probe.
Only residue: the explicit-formula-as-line-spectrum reframing + O(d)/Cramér-Rao
sample-complexity statement (Gate 0 confirmed unaddressed in literature) — a
modest expository/theory note at best, and even its "few-measurements" selling
point is real only in the noiseless function-field case, which direct
point-counting already dominates. Pattern matches the comms outcome: elegant,
genuinely novel framing, dominated on the axis that matters.
