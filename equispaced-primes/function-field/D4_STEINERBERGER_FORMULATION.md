# D4 — Steinerberger greedy-discrepancy connection (the last untouched forward lead)

Status: FORMULATION + gated plan. Autonomous run 2026-05-16, after D3 complete.
Priority: lower than Koyama joint paper and the D1 N·W→C note; executed because
it is the last self-contained, non-blocked forward lead and Aistleitner (the
domain expert) explicitly volunteered it. Char-0 (Steinerberger is [0,1]
sequences), NOT function field.

## Provenance (why this is legitimate, not manufactured)

`correspondence/AISTLEITNER.md`: Aistleitner pointed at Steinerberger
arXiv:1902.03269 ("greedy step-by-step construction of low-discrepancy
sequences ... between classical and experimental mathematics") as related to
the project's per-step ΔW(p) object. The project's own forward-verdict memory
lists this as the explicit #2 forward lead, never executed. The user asked to
continue; D3 is complete; this is the honest next item.

## The precise question

Project facts (established, in-repo):
- Sign Theorem [PROVEN, Lean-verified]: at a prime step, the forced Farey
  insertion of the φ(p)=p−1 new points {k/p : 1≤k≤p−1} changes the L² Farey
  discrepancy W(N)=∫₀¹E_N(x)²dx by ΔW(p)=W(p)−W(p−1), whose sign is governed
  by the Mertens value M(p) (primes with M(p)≤−3 ⇒ ΔW(p)>0, discrepancy
  *increases*).
- Founding lens: the Farey insertion is *forced/arithmetic/non-adaptive* —
  a prime inserts ALL p−1 equispaced points {k/p}, with zero freedom.

Steinerberger: builds sequences *greedily*, each new point chosen to MINIMIZE
a discrepancy energy E (functional TBD from the primary read, agent
ad2b8b9837c37b8b2). Greedy ⇒ each step is discrepancy-*minimizing*.

> **Central question.** Is `ΔW(p)>0` precisely a *greediness failure*: the gap
> between the **forced** arithmetic Farey insertion of the p−1 points {k/p}
> and the **greedy-optimal** insertion of p−1 points under Steinerberger's
> energy E — with the **Mertens function M(p) as the exact obstruction**?
>
> Formally: define the deficiency D(p) := ΔW_Farey(p) − ΔW_greedy(p) ≥ 0
> (Farey is forced, so cannot beat greedy). Question: is D(p) (or ΔW_Farey(p)
> itself) governed by M(p)? Best case: D(p) = (explicit Mertens term) + lower
> order, giving the Sign Theorem a home inside Steinerberger's greedy-energy
> program.

If true: a genuine reframing — the Sign Theorem becomes "the Farey
construction is the canonical *anti-greedy* (forced) low-discrepancy process,
and its greediness deficit is the Mertens function." That is the kind of
cross-program bridge the per-step lens was supposed to provide. If false /
only a loose analogy: honest negative, recorded, D4 closed dictionary-tier.

## Gated plan (D3-style kill-gates)

- [~] **G-S1 [literature, running]** Steinerberger 1902.03269 primary read
  (agent ad2b8b9837c37b8b2): exact greedy energy functional E, exact theorem,
  the kernel, whether any Farey/arithmetic instance exists. **Do NOT build the
  probe until E is known** (avoid strawman benchmark = inflation risk).
- [ ] **G-S2 [formulate]** Once E known: write the exact correspondence
  {Farey forced insertion ↔ greedy step under E}; is E an L² energy
  commensurate with W(N)=∫E_N²? If E is a different (non-L²) energy, state the
  precise mismatch and whether the comparison is even well-posed.
- [ ] **G-S3 [numerical probe]** Compute ΔW_Farey(p) (exact) and the
  greedy-optimal ΔW_greedy(p) under the ACTUAL E for primes p≤~50; test
  whether D(p) tracks M(p) / 1[M(p)≤−3]. Kill-gate: no Mertens signal in the
  greedy deficiency ⇒ loose analogy ⇒ honest negative, close D4.
- [ ] **G-S4 [verdict]** Genuine bridge (Sign Theorem ⊂ Steinerberger
  program, deficiency = Mertens) vs loose analogy. Adversarial check vs
  prior art (any Steinerberger/Farey link in the literature). Honest scope:
  even the best case is an Experimental-Math-grade reframing, NOT RH-depth and
  NOT a char-0 advance — calibrate, do not inflate.

## VERDICT (2026-05-16) — REFUTED, cleanly, by the primary read + classical facts

G-S1 primary read (agent ad2b8b9837c37b8b2, Steinerberger 1902.03269
"Dynamically Defined Sequences with Small Discrepancy", 2019):

- Steinerberger's greedy energy is the **logarithmic pairwise kernel**
  `x_N = argmin Σ_{k<N}[1 − log(2 sin π|x−x_k|)]` — a log-energy repulsion,
  **NOT** the L² discrepancy `W(N)=∫E_N²` the Sign Theorem is about. The two
  functionals are structurally different. No Farey/Mertens/prime content in
  the paper.

Decisive classical facts (derive-then-verify; these are CLASSICAL, not new —
labelled so explicitly):
1. `Π_{k=1}^{p−1} 2 sin(π k/p) = p` (cyclotomic identity; `Π_{k=1}^{n−1}
   2 sin(πk/n)=n`). [PROVEN, classical]
2. The `n`-th roots of unity (equispaced points) are the **unique global
   minimizer** of the circle logarithmic energy `−Σ_{j≠k} log|x_j−x_k|`
   (equivalently they maximize `Π|x_j−x_k|`; Fejér / Fekete points of the
   circle). [PROVEN, classical]
3. A prime `p` inserts **exactly** the equispaced block `{k/p}` (the founding
   lens). [PROVEN, in-repo]

⇒ Under Steinerberger's *actual* (logarithmic) energy, the prime Farey block
is **energy-OPTIMAL** (it is the log-energy minimizing configuration), the
**opposite** of a "greediness failure". The Sign-Theorem fact `ΔW(p)>0` lives
in a **different** functional (L² `∫E²`) and does NOT translate into a
Steinerberger-greediness deficit.

**The central hypothesis is REFUTED (and reversed).** No numerical probe is
run: it would be a strawman against the wrong functional (an inflation risk
the project explicitly warns against). G-S2/G-S3/G-S4 are closed by this
analytic refutation.

**Salvageable honest residue (minor, explicitly CLASSICAL — not a
contribution):** the founding lens intersects a classical extremal fact —
prime Farey blocks are the logarithmic-energy-optimal insertions, with exact
value via the cyclotomic identity `Π 2 sin(πk/p)=p`. This is a true, tidy
observation but it is Fejér/cyclotomic classical, and it *contradicts* (rather
than supports) the Sign-Theorem-as-greediness-failure framing. Record as a
one-line aside at most; do not inflate into a "Steinerberger bridge".

**D4 status: CLOSED — honest NEGATIVE.** The last untouched forward lead does
not pan out; reason precisely identified (wrong functional; primes are
log-energy-optimal, not failures). Cost: one primary read + classical facts,
~10 min — the gated method killing a dead lead cheaply, as designed.

## Honest priors

- Most likely outcome (base rate, given the project's honest map): a
  suggestive analogy that does NOT close to a theorem — Steinerberger's energy
  is probably a specific RKHS/Fourier diaphony, and the Farey forced insertion
  is unlikely to be its exact greedy critical set. Expected verdict: honest
  negative or "analogy only", Experimental-Math footnote at best.
- Upside case (lower probability): D(p) numerically tracks M(p) cleanly ⇒ a
  genuine, citable reframing of the Sign Theorem. Worth the cheap probe.
- Either way: this is dictionary/Exp-Math tier, strictly below the Koyama
  paper and the D1 note in the project's priority order. Recorded so the user
  can decide; nothing sent.
