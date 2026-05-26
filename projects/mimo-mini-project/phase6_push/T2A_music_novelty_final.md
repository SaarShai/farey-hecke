---
model: mimo-v2.5-pro
max_tokens: 14000
---

# T2A — MUSIC L-zero pipeline: novelty after all adversarial rounds

## Setup

After multiple rounds of MiMo dispatches:
- AV1 (positive): "after thorough search, no prior work found"
- Z4 (negative): "relabeled Stoica-Nehorai 1989, in Kay §7.6"
- D2 (defender): "math is textbook adaptation, application novel"
- D4 (defender): "ingredients textbook, composition undocumented"

These agree the MATH is standard but disagree about whether the APPLICATION counts.

## Task: settle this once with care

### A. Search for explicit prior work in EACH community

1. **Signal processing literature** (1986-2025): has anyone applied MUSIC/Prony/ESPRIT specifically to:
   - Riemann zeta zeros from prime data?
   - Any L-function zeros?
   - Hint: search keywords like "MUSIC + prime", "ESPRIT + Riemann", "Prony + L-function"

2. **Analytic number theory literature**:
   - Has anyone explicitly framed L-zero recovery as a spectral estimation problem?
   - Odlyzko-Schönhage 1988 uses FFT but not spectral subspace methods
   - Hejhal's Maass form computation: spectral estimation? Or root-finding?

3. **Hilbert-Pólya / quantum chaos community**:
   - Berry-Keating treat zeros as eigenvalues but use Hamiltonian framework
   - Anyone applied subspace methods?

4. **Recent ML/applied math**:
   - Pratt et al. on ML for RH?
   - DeepMind math papers — knot theory yes, L-zeros?
   - PDE/inverse-problem framings?

### B. What would make this PUBLISHABLE per the actual community

Two paths:

**Path 1 (signal processing)**: 
- "Test cases with rigorously known infinite signals" — L-zeros provide that
- Submission target: IEEE Trans. Signal Processing or ICASSP
- Audience cares: novel benchmark for spectral methods
- Specific claim: L-zero data has known pair-correlation structure (GUE), which makes a good test for spectral methods on COLORED signals

**Path 2 (computational number theory)**:
- "Fast first-pass zero estimator for L-families lacking analytic infrastructure"
- Submission target: Math. Comp. or J. Number Theory (computational)
- Audience cares: Sym^k, GL(n) Maass, Rankin-Selberg zeros are hard via classical methods
- Specific claim: O(1) wall-clock zero estimate per L-function family

### C. Who specifically cares?

Real names to identify (if you can):
- Andrew Booker (Maass form computation, lcalc)
- Tim Dokchitser (computeL package)
- David Farmer (LMFDB curation, L-function database)
- Ce Bian / Andreas Strömbergsson (Maass forms)
- Mike Rubinstein (lcalc, L-zero computation)

If we wrote to them: "here's a fast method to estimate L-zeros of Sym^k Δ, here are the values" — would they care? Would it be useful?

### D. The "killer" answer

If you can identify ONE specific person + ONE specific use case where MUSIC pipeline would be valuable:
- "X computes Sym^k Δ zeros via method Y which takes Z hours per L-function. MUSIC gives a first-pass in seconds."

That's the "who cares" answer.

If you cannot identify such a use case, the work is a pedagogical demonstration, not a research contribution.

## What I want

1. Honest verdict on novelty (with specific cited prior work searched)
2. Concrete "who cares" answer (specific names, specific use cases)
3. Realistic publication path with named journal/venue

Be specific or honestly say "I don't know if anyone uses this."
