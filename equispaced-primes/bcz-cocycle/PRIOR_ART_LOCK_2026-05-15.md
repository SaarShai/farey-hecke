# PRIOR-ART LOCK — Dynamical / per-step-cocycle formulation of the Farey second moment

Adversarial gating audit. 2026-05-15. Auditor: literature prior-art reviewer.
Default posture: claim is NOT novel until the literature clearly shows otherwise.

## 0. Exact claim under audit

> The Farey counting discrepancy `E_Q` (and the Franel–Landau / Mikolás L²
> second moment `W(Q)` / `J(Q)`) is EXACTLY the Birkhoff sum of an explicit
> cocycle `g = 1 − Φ·gap` over the BCZ map (= first-return map of the
> horocycle flow on `SL₂(ℝ)/SL₂(ℤ)`, Athreya–Cheung), and its per-step
> (order `Q−1→Q`, prime-step) increment is the corresponding Birkhoff
> increment.

Conceded prior art (not in scope): the STATIC Farey↔Mertens identities
(`A_Q(m)=Σ_{d|m}d·M(⌊Q/d⌋)`, `Σ M(⌊x/n⌋)=1`) — Cox–Ghosh–Sultanow.

Audited question (sole): is the **dynamical / per-step-cocycle** formulation
of the SECOND MOMENT / discrepancy as a BCZ–Birkhoff sum already in the
field?

---

## 1. Mikolás 1949 (primary) — COULD-NOT-OBTAIN full text; conservative reading

**Source.** M. Mikolás, *Farey series and their connection with the prime
number problem. I*, Acta Sci. Math. (Szeged) **13** (1949/1950), no. 2,
93–117 (Part II: ibid. **14** (1951), 5–21).

**Obtainability.** Szeged repository record located
(`contentas.bibl.u-szeged.hu/Record/acta13662`; full scan at
`acta.bibl.u-szeged.hu/13662`). The record page exposes **only bibliographic
metadata, no abstract / TOC**. The primary mathematical text was **NOT
obtained** in this audit → tagged **COULD-NOT-OBTAIN**, treated
conservatively (= assume Mikolás proves the strongest analytic form).

**What Mikolás proves (per consistent secondary characterization — Codecà–Nair
"Euler products, Farey series and the Riemann hypothesis II"; Cox–Ghosh–
Sultanow §1; Kruse / Dress–Tenenbaum-line discrepancy surveys; Karvonen–
Zhigljavsky 2024).** Mikolás establishes the **mean-square / second moment of
the Farey discrepancy in closed analytic (Fourier–Parseval, cotangent-sum /
bilinear-Mertens) form** — i.e. the identity the handoff uses as
`J(Q) = (1/2π²) Σ_m A_Q(m)²/m² + O(1)` — and proves the summation formula
`Σ_{n≤x} M(⌊x/n⌋) = 1`. This is **purely analytic number theory
(Parseval over the Fourier expansion of the sawtooth / `e(mf)` characters)**.

**Dynamical content: NONE.** No cocycle, Birkhoff sum, horocycle flow, BCZ
map, or ergodic averaging appears (Mikolás 1949 predates the BCZ map by ~50
years and Athreya–Cheung by ~65 years; the homogeneous-dynamics machinery did
not exist). The conservative assumption (Mikolás proves the strongest Parseval
form) **still contains no dynamical/cocycle structure** — it cannot, by date
and by method. Verdict contribution: Mikolás is the ANALYTIC second-moment
result; he does NOT pre-empt the dynamical formulation.

---

## 2. Cox, Ghosh & Sultanow — primary text obtained, read verbatim

### 2.1 arXiv:2105.12352 (2021) — *The Farey Sequence and the Mertens Function*

**Primary obtained** (PDF text-extracted 2026-05-15, 9 pp).

**Abstract, verbatim:**
> "Franel and Landau derived an arithmetic statement involving the Farey
> sequence that is equivalent to the Riemann hypothesis. Since there is a
> relationship between the Mertens function and the Riemann hypothesis, there
> should be a relationship between the Mertens function and the Farey
> sequence. Functions of subsets of the fractions in Farey sequences that are
> analogous to the Mertens function are introduced. Mikolás proved that the
> sum of certain Mertens function values is 1. Results analogous to Mikolás'
> theorem are the defining property of these functions. A relationship
> between the Farey sequence and the Riemann hypothesis other than the
> Franel-Landau theorem is postulated. This conjecture involves a theorem of
> Mertens and the second Chebyshev function."

**Opening, verbatim:**
> "Mikolás [1] proved that Σ_{n=1}^{x} M(⌊x/n⌋) = 1 where M denotes the
> Mertens function. … A more general convolution is Σ_{n≤x} α(n)F(x/n) …
> The function G is denoted by α∘F."

**Keyword census over the full extracted text (verbatim count):**
`BCZ`=0, `horocycle`=0, `Birkhoff`=0, `cocycle`=0, `ergodic`=0,
`second moment`=0, `L2`/`L^2`=0, `discrepancy`=0, `per-step`=0,
`asymptotic`=0; `dynamic`=1 (incidental, non-dynamical-systems use);
`Mikolás`=10, `Franel`=4, `Landau`=3.

**Finding.** Cox–Ghosh–Sultanow 2021 is **purely static Dirichlet-convolution
/ Mertens-identity arithmetic**. **No BCZ map, no horocycle flow, no Birkhoff
sum, no cocycle, no second-moment object, no per-step (order N→N+1)
increment.** Exactly the conceded static prior art — and nothing more. It does
**not** touch the dynamical formulation.

### 2.2 "arXiv:2407.10214 (2024)" — MISATTRIBUTION FOUND IN THE HANDOFF

**Adversarial finding (reported per project anti-novelty-inflation culture):**
The handoff (`START.md` §0; `THEOREM_R` §0.4) cites *"Cox–Ghosh–Sultanow
arXiv:2407.10214 (2024)"*. **arXiv:2407.10214 is NOT a Cox–Ghosh–Sultanow
paper.** Verified at source: arXiv:2407.10214 = **T. Karvonen & A.
Zhigljavsky, *Maximum mean discrepancies of Farey sequences* (2024)**.
Abstract, verbatim:
> "We identify a large class of positive-semidefinite kernels for which a
> certain polynomial rate of convergence of maximum mean discrepancies of
> Farey sequences is equivalent to the Riemann hypothesis. This class
> includes all Matérn kernels of order at least one-half."

Karvonen–Zhigljavsky is a **kernel / RKHS / MMD** paper: **no BCZ, no
horocycle, no Birkhoff sum, no cocycle, no per-step increment** (verified).
Since the handoff explicitly leaves the 2407.10214 citation
`[CITATION-UNVERIFIED, not load-bearing]`, the misattribution does not
threaten theorem (R) — but it must be **corrected in any writeup** (the
project's #1 failure mode is exactly mis-cited references). It does NOT supply
prior art for the dynamical claim.

---

## 3. BCZ-school / homogeneous-dynamics literature — hard adversarial sweep

### 3.1 Athreya & Cheung, IMRN 2014 / arXiv:1206.6597 — primary obtained, read verbatim (THE closest piece of prior art)

**Primary obtained** (PDF text-extracted 2026-05-15, 39 pp).

This is the single most dangerous source: it is the canonical paper that
applies the **Birkhoff ergodic theorem to BCZ-map orbits with explicit
`L¹(Ω,m)` observables** to recover Farey statistics. What it DOES, verbatim:

- Gap distribution as a BCZ/Birkhoff statistic (Hall's distribution),
  Corollary 1.8 & 1.9 (`Q²(γ_{i+1}−γ_i) = (R∘T^{i−1})(1/Q,1)`); moments of
  consecutive denominators via `∫_Ω x^s y^t dm`, Theorem 1.11 eq (1.13)–(1.14)
  (recovering Hall–Tanenbaum). Verbatim:
  > "We can apply our results … to Farey fractions by applying Theorem 1.3 to
  > various functions in L¹(Ω, m). … we obtain results originally due to
  > Hall–Tanenbaum [23]."
  > "This result will follow from the application of the Birkhoff ergodic
  > theorem to the orbit of Λ under the BCZ map, with observable given by the
  > indicator f…"

- **Franel–Landau / RH is raised ONLY as an OPEN QUESTION, not realized as a
  cocycle.** Verbatim (Section 8, "Questions"):
  > "Zagier [36] showed that proving an optimal rate of equidistribution for
  > long periodic trajectories for h_s on SL(2,ℝ)/SL(2,ℤ) … is equivalent to
  > the classical Riemann hypothesis. There is also an equivalent formulation
  > of the Riemann hypothesis in terms of the distribution of the Farey
  > sequence due to Franel–Landau [18]. This leads to **Question. Is there an
  > optimum bound on the error term in Theorem 1.3 that is equivalent to the
  > Riemann hypothesis?**"

**Keyword census over the full extracted text (verbatim count):**
`discrepancy`=0, `second moment`=0, `Mikolás`=0. `Franel`/`Landau`=2 (only
the open-question passage above + the reference list entry [18]).

**Precise delta (load-bearing).** Athreya–Cheung realize **gap-distribution
and denominator-moment** statistics as BCZ/Birkhoff `L¹` averages, and
explicitly **pose** the Franel–Landau/RH error term as an *open question*.
They do **NOT**: (i) write the Farey discrepancy `E_Q(x)` as a Birkhoff sum
of any cocycle; (ii) define the cocycle `g = 1 − Φ·gap`; (iii) treat the
**L² second moment** `J(Q)`/`W(Q)` (the word "discrepancy" / "second moment"
/ "Mikolás" never appears); (iv) do an order `Q−1→Q` per-step increment. The
audited claim is the **specific unfilled slot Athreya–Cheung flagged but did
not occupy**.

### 3.2 Cheung & Quas, arXiv:2403.14976 (2024) — primary obtained

> "Theorem 1. The BCZ map is weak-mixing."

Introduction (verbatim): only "the BCZ map … a tool to study the statistical
properties of Farey sequences, whose relation to Riemann Hypothesis dates
back to Franel and Landau." **No discrepancy, no second moment, no Mikolás,
no cocycle-Birkhoff identity** (verified over full text). Qualitative;
authors state mixing/rigidity open. Not prior art for the claim (consistent
with the handoff's own [CITATION-LOCKED] reading).

### 3.3 Boca & Zaharescu, *Farey fractions and two-dimensional tori*, 2006 survey

Survey themes (verified via publisher record + Athreya–Cheung's citation of
it): spacing statistics of Farey fractions, geometric-probability / linear
flow on the punctured 2-torus, noncommutative tori / almost-Mathieu. This is
**spacing/gap-statistics and the H. Hall conjecture line**, NOT a Birkhoff-sum
realization of the discrepancy **second moment**, and not a per-step cocycle.
(Full text behind Springer auth; the BCZ-school body of work it surveys —
gap distributions, Hall's conjecture — is exactly the gap/spacing direction,
explicitly distinct from the discrepancy-L² direction. Tagged
PARTIAL-ACCESS, conservative reading applied: no contrary evidence, and the
survey's own scope statement excludes the audited object.)

### 3.4 Bonanno et al., *A Poincaré map for the horocycle flow on
PSL(2,ℤ)\ℍ and the Stern–Brocot tree*, arXiv:2207.03755 (pub. 2024)

Abstract (verified): constructs a Poincaré map for the positive horocycle
flow; characterizes periodic orbits, equidistribution, Stern–Brocot tree
organization; corollaries on cusp-excursion depth and **gap distributions**.
**No discrepancy / second-moment Birkhoff sum, no `1−Φ·gap` cocycle, no
per-step increment** (abstract + scope). Same gap-statistics lane as
Athreya–Cheung.

### 3.5 Marklof, *Horospheres and Farey fractions* — primary obtained

**Primary obtained** (PDF text-extracted, 10 pp). Subject: equidistribution
of *multidimensional* Farey fractions on expanding horospheres in `Γ\SL(d,ℝ)`
(Theorem 2, eq (1.10)–(1.13)); application to Frobenius-number / gap
asymptotics. Keyword census: `discrepancy`=0, `second moment`=0, `Mikolás`=0,
`Birkhoff`=0, `cocycle`=0; `Riemann`=1 (an unrelated uniform-continuity
estimate). **Not prior art for the claim.** (Marklof–Strömbergsson Annals
2010, Heersink ETDS 2019 `arXiv:1712.03258`, Lutsko "Farey for thin groups",
Taha "BCZ analogue for Hecke groups", Athreya–Margulis logarithm-law /
arXiv:2403.15160 — all verified by abstract/scope to be **equidistribution,
gap/spacing distribution, or logarithm-law** results; none expresses the
discrepancy L² second moment as a BCZ/horocycle Birkhoff sum, and none does
the order N→N+1 per-step cocycle.)

### 3.6 The one phrase that demanded scrutiny

A search-engine synthesis paraphrased the field as "the Franel–Landau RH
characterization has been reinterpreted in terms of estimates of L¹-averages
of the BCZ cocycle along periodic orbits." Run to ground: this paraphrase is
**not traceable to any primary source asserting it**. The actual primary
texts (Athreya–Cheung §8: open *question*; Cheung–Quas: weak mixing only;
Cheung "Dynamics of BCZ cocycles" ICBS-2024 talk: no abstract obtainable
asserting a discrepancy-second-moment Birkhoff identity) show only the
**L¹/equidistribution (gap)** program and an **open RH question** — *not* an
L² second-moment Birkhoff-sum identity, and *not* a per-step cocycle. Treated
conservatively: even granting an "L¹ BCZ-cocycle reinterpretation of
Franel–Landau" exists in folklore, it is the **L¹ / equidistribution** form,
which is strictly weaker than and distinct from the audited **L² second
moment + explicit `1−Φ·gap` cocycle + prime-step increment** package.

---

## 4. VERDICT

### (A) NOVEL — with a precisely stated, narrow delta.

The **dynamical / per-step-cocycle formulation of the Farey discrepancy and
its L² (Franel–Landau / Mikolás) second moment as the Birkhoff sum of the
explicit BCZ cocycle `g = 1 − Φ·gap`, with the order `Q−1→Q` prime-step
Birkhoff increment**, is **not present in the literature surveyed** (primary
texts read verbatim for Mikolás-secondary, Cox–Ghosh–Sultanow 2105.12352,
Karvonen–Zhigljavsky 2407.10214, Athreya–Cheung 1206.6597, Cheung–Quas
2403.14976, Marklof Farey-horospheres; scope-verified for Boca–Zaharescu
2006, Bonanno 2207.03755, Marklof–Strömbergsson, Heersink, Lutsko, Taha,
Athreya–Margulis).

**What IS in the literature (the prior art that is real):**
1. **Mikolás 1949** — the L² second moment of the Farey discrepancy in
   **analytic Fourier–Parseval / bilinear-Mertens** form (COULD-NOT-OBTAIN
   primary; conservatively granted the strongest analytic form — still
   non-dynamical by date/method).
2. **Cox–Ghosh–Sultanow 2021** — the **static** Farey↔Mertens identities
   (conceded; verbatim-confirmed purely arithmetic).
3. **Athreya–Cheung 2014** — the BCZ map = horocycle first-return; the
   **Birkhoff `L¹` realization of GAP / denominator-moment statistics**; and
   an **explicit OPEN QUESTION** asking whether a BCZ-error-term bound is
   RH-equivalent (Franel–Landau).

### Single closest piece of prior art + exact location + precise delta

**Closest:** **Athreya & Cheung, *A Poincaré section for horocycle flow on
the space of lattices*, IMRN 2014 no. 10, 2643–2690 = arXiv:1206.6597v2**,
**Section 8 ("Questions")** and **§1.5 / Cor. 1.8–1.9, Thm 1.11 eq
(1.13)–(1.14)**.

**Exact delta (what they do vs. the claim):**
- They DO: BCZ-Birkhoff `L¹` averaging for **gap** distribution (Hall) and
  **denominator moments** (Hall–Tanenbaum); they **pose**, as an open
  question (§8), whether an optimal BCZ error term is RH-equivalent, citing
  Franel–Landau [18].
- They do NOT: write `E_Q(x)` as a Birkhoff sum of any cocycle; introduce the
  cocycle `g = 1 − Φ·gap`; address the **L² second moment** `J(Q)`/`W(Q)`
  (the words discrepancy / second moment / Mikolás are absent); perform the
  order `Q−1→Q` prime-step Birkhoff increment.

The audited dictionary is therefore the **specific construction Athreya–Cheung
explicitly flagged as open and did not build**. That is genuine novelty of
*formulation*, not of the underlying analytic content.

### Mandatory novelty-inflation guardrails for any writeup

1. **CLAIMABLE AS NEW:** the *formulation/dictionary* — `E_Q` = Birkhoff sum
   of the explicit cocycle `g = 1 − Φ·gap` over the BCZ map; `J(Q)`/`W(Q)`
   as the roof-weighted second moment of that Birkhoff sum; the prime-step
   `ΔA(m)=−1+p𝟙[p|m]` as the Birkhoff increment from the φ(p) new primitive
   vectors. Frame explicitly as **occupying the open slot named in
   Athreya–Cheung IMRN 2014 §8**.
2. **NOT CLAIMABLE AS NEW (must cite):** (a) the L² second moment itself →
   **Mikolás 1949 / Franel–Landau 1924** (analytic); (b) the static
   Farey↔Mertens identities → **Cox–Ghosh–Sultanow arXiv:2105.12352**;
   (c) the BCZ map = horocycle first-return & `L¹` Birkhoff realization of
   gap/denominator statistics → **Athreya–Cheung IMRN 2014**; (d) weak
   mixing → **Cheung–Quas arXiv:2403.14976**.
3. **MUST FIX before any writeup:** the handoff's citation
   "Cox–Ghosh–Sultanow arXiv:2407.10214" is **WRONG** — 2407.10214 is
   **Karvonen–Zhigljavsky, *Maximum mean discrepancies of Farey sequences***.
   Remove/relabel; do not attribute it to Cox–Ghosh–Sultanow.
4. **Honesty constraint preserved:** novelty is of the *dynamical
   formulation*, NOT a new theorem. The asymptotic constant `C` remains
   REDUCED-WITH-NAMED-INPUT (not proven), per `THEOREM_R_2026-05-15.md`; the
   prior-art status of the *formulation* does not upgrade the proof status of
   `C`.

### Residual uncertainty (stated for conservatism)
Mikolás 1949 primary text COULD-NOT-OBTAIN, and Boca–Zaharescu 2006 survey /
Cheung "Dynamics of BCZ cocycles" 2024 talk are PARTIAL-ACCESS. The
conservative default was applied throughout (grant the strongest analytic /
L¹-equidistribution form to the prior art). Even under that worst case, no
source surveyed expresses the **L² second moment** as the **explicit
`1−Φ·gap` BCZ-cocycle Birkhoff sum with a prime-step increment** — the delta
holds. If a future primary read of Mikolás 1949 or the Boca–Zaharescu survey
reveals a discrepancy-L²-as-Birkhoff identity, this lock must be revisited;
absent that, verdict (A) stands with the narrow, explicitly-bounded delta
above.
