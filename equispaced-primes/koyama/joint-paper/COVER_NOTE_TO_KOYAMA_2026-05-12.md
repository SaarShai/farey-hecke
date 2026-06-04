**Subject:** First draft of the Technical/Computational section — two scope questions before LaTeX

---

Dear Shin-ya,

Thank you for your 2026-05-12 note. I'm honoured by the co-authorship
offer and ready to push toward submission.

Attached is a first draft of the Technical/Computational
section (§X. Methodology, formalization, and numerical evidence),
together with two appendices — Appendix A (pen-and-paper proof of
the corrected $B_\infty$ identity, Theorem X.4.1) and Appendix B
(proof of the $c_K$ leading + subleading identity, Theorem X.4.2,
with the Laurent-algebra for the local Perron double-pole residue
in §B.2) — and a per-`sorry` inventory for the Lean 4 lake
project.

The draft is organised around the four pillars you described as
the core:

1. The `e^{-γ}` correction of the asymptotic target (Aoki–Koyama 2023);
2. The corrected `B_∞` identity and the local Perron residue
   `C₁ = -L''(ρ)/(2 L'(ρ)²)`, both established unconditionally;
3. The three primary open challenges that organise the program
   forward — the shifted Perron leading remainder (SP-L), the
   Dirichlet Polynomial Avoidance Conjecture (DPAC) for general
   $K$, and GL(2) reciprocal-derivative control; three further
   EC-side questions appear in a "Further questions" block at the
   end of §X.7;
4. The rigorous Phase-1 replication of your Dominance-of-`-1`
   residue-count tables at `x = 1.3 · 10^{13}`.

Two scope confirmations before I begin LaTeX conversion:

**1. "Verification at `10^{13}`" — Phase-1 only.** Our `10^{13}`-scale
evidence is the Phase-1 Dominance-of-`-1` replication (two
implementations agreeing on every `π(x; q, a)` count at
`x = 1.3 · 10^{13}` for `N ∈ {7, 8, 11, 19, 23}`; identity (3.1)
verified across 495 cells; bundle sent 2026-05-04). The analytic
identities (`B_∞` residuals, `C_1` subleading, the `|D_K| · ζ(2)`
drift toward `e^{-γ}`) are verified at `K = 2·10^{6}`–`10^{7}` with
50-decimal precision across mpmath / PARI 2.17.3 / Arb 250-bit, and
the manuscript keeps the two scales rigorously separate. Please
confirm this matches your framing.

**2. "Double-verification" — two stacks per claim.** §X.2 uses two
notions: (i) for the analytic identities, the same quantity computed
by mpmath, PARI/GP 2.17.3, and Arb 250-bit via python-flint,
agreeing to all displayed digits at `K = 2·10^{6}` and to
`≈ 10^{-5}` at `K = 10^{7}`; (ii) for the Phase-1 counts, two
independent prime-enumeration implementations (`primesieve` plus a
hand-rolled C segmented sieve), with a second hardware path
agreeing through `1.3 · 10^{12}`. Let me know if you had a different
sense in mind (e.g. Lean ↔ numerical cross-check, or two independent
symbolic derivations of the identity itself).

**Phase-1 cell discrepancies pending your review.** Per your
2026-05-12 note, you offered to resolve the table discrepancies.
I re-checked `nontriv.pdf` Tables 3–7 against our counts; the
values quoted as yours below all match your published tables
exactly, so the discrepancy is genuine count-vs-count and not a
transcription artefact on our side. Substantive cells at
$x = 1.3 \cdot 10^{13}$:

- **Table 5, $N = 11$, $a = 10$**: our $11{,}503$ vs your
  $71{,}711$. **This is the load-bearing one** — the qualitative
  dominance signal for $N = 11$ at this checkpoint depends
  entirely on it: with your $71{,}711$, $-1$ ranks 2nd of 5
  non-residues (top group); with our $11{,}503$, $-1$ ranks 3rd
  of 5 (outside the top-2 group).
- **Table 6, $N = 19$, $a = 13$**: our $24{,}559$ vs your
  $55{,}581$. Substantive.
- **Table 6, $N = 19$, $a = 18$**: our $54{,}192$ vs your
  $57{,}192$. Single-digit at the leading position; could be a
  3 vs 4 typo.
- **Table 3, $N = 7$, $a = 6$**: our $26{,}129$ vs your
  $26{,}179$ ($\Delta = 50$).
- **Table 7, $N = 23$, $a = 19$**: our $79{,}327$ vs your
  $79{,}227$ ($\Delta = 100$, just the hundreds digit).
- **Table 4, $N = 8$, small-$x$ rows**: all 11 small-$x$ rows
  disagree; one of our $x = 10^{12}$ row's values exact-matches
  one of your supposed $x = 1.3\cdot 10^{12}$ entries, which
  suggests an $x$-label error in that table draft.

Headline qualitative result, aligned with your *nontriv.pdf* p. 19
discussion: $-1$-dominance is **cleanly observed for $N = 8$** at
$x = 1.3 \cdot 10^{13}$ ($-1 = 7$ strictly largest); for $N = 19$,
$-1$ is 3rd of 9 non-residues in both our and your data (top
group, not strict); for $N = 11$, the picture turns on the
Table-5 $a = 10$ cell above; for $N = 7$ and $N = 23$ we agree
with your analysis that the predicted bias is not yet cleanly
observed at this scale and is attributable to exceptionally
low-lying first zeros (your $N = 19$ illustrative estimate
places the next sine-wave peak around
$x = e^{33.4} \approx 3.2 \cdot 10^{14}$).

I'll fold whatever you confirm into §X.5.1 before LaTeX conversion.

**Other status notes.**

* The Lean 4 formalisation inventory compiles cleanly under
  `leanprover/lean4:v4.28.0` + Mathlib `8f9d9cff…`. **Two `sorry`s
  across nine files** remain, both being the DPAC headline
  conjecture itself (LI-class). **Seven files are fully proved
  (0 `sorry`)**:
  - **`LocalPerronResidue.lean`** — Lemma X.3.1, machine-verified
    end-to-end (unconditional).
  - **`CorrectedBInfty.lean`** — **Theorem X.4.1 (the paper's
    headline algebraic identity), Lean-verified conditional on a
    single named `Filter.Tendsto` hypothesis** asserting that the
    partial prime-power tail $T_K(\chi,\rho)$ converges to the
    four-component right-hand side. The pen-and-paper proof in
    Appendix A establishes exactly that convergence from Akatsuka
    2013 eq. (2.5) + log-Euler-product expansion + the imprimitive
    Euler-factor identity + geometric-series tails; given the
    convergence, the Lean proof is three lines
    (`Classical.epsilon_spec` + `tendsto_nhds_unique`).
  - **`DPAC_closure_attempt.lean`** — proves DPAC unconditionally
    for $K \in \{2, 3, 4\}$, reformulates the general case as
    `FiniteLogRatioLI`, and records the precise obstruction
    certificate (Pólya 1913 discreteness + a single open avoidance
    statement at $\zeta$-zero ordinates). General-$K$ DPAC remains
    open, comparable to the Linear Independence Hypothesis.
  - **`MertensSpectroscopeUniversality.lean`** — universality
    statement (Tendsto … atTop atTop) Lean-verified conditional on
    an explicit-formula-derived asymptotic hypothesis (Soundararajan
    2009 Theorem 1 input).
  - **`FareyBridgeIdentity.lean`** — Farey-exponential-sum =
    $M(p) + 2$ identity Lean-verified conditional on the
    Ramanujan-sum decomposition input (Hardy–Wright Theorem 304).
  - **`SmoothedDwfFormula_full.lean`** — boundary-residue $R_0 = -2$
    chain (17 algebraic-glue lemmas) closed unconditionally; the
    two analytic prerequisites (`mellin_decay`, `inv_zeta_polynomial_growth`)
    are stated as explicit hypotheses on the consuming theorems,
    both Mathlib v4.28.0 gaps.

  The two remaining sorries are both the DPAC headline conjecture
  itself, which is diagnostically comparable to the Linear
  Independence Hypothesis for $\zeta$-zero ordinates (a famous
  open problem in number theory). The full inventory is in
  `LEAN_SORRY_STATUS.md`.
* The three primary open challenges in §X.7 (Q:Perron, Q:DPAC,
  Q:EC-recip) are each stated with the precise input that would
  close them; three further EC-side questions (conductor-confound,
  Sym² normalisation, EC-NDC) appear in the "Further questions"
  block at the end of §X.7.
* On the GL(1) halo route, my honest assessment is that a naïve
  transfer of the GL(2) halo theorem yields only `K^{1/2+ε}`, which
  does not reach `o(log K)`. I have written this up as a negative
  finding in `HALO_GL1_SKETCH_2026-05-12.md`; it does not block the
  manuscript but I wanted you to see it before deciding whether to
  include SP-L as an open challenge or attempt a deeper route.

I am happy to start LaTeX conversion as soon as the two scope
questions above are settled. The author-order and journal target
are open placeholders; I defer both to you.

With thanks and best wishes,

Saar
