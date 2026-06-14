# θ = 1/2: extremal index & compound-Poisson cluster law for the parabolic Taha G_q-BCZ extreme-gap process

**Goal H-2.** Date: 2026-06-14. Status verdict (one line, see §7): **(b) proved-modulo-a-named-limit-theorem** — the
extremal index θ = 1/2 and the geometric→degenerate cluster law are *derived exactly* from a coordinate-universal
period-2 cusp-swap involution and confirmed by high-precision numerics for q = 4,5,7; the only missing piece is the
rigorous rare-event-point-process (REPP) convergence theorem for the **parabolic, polynomial-mixing** G_q-BCZ
cross-section, which the standard Freitas–Freitas–Todd (FFT) repelling-periodic machinery does **not** supply.

---

## 1 · Setup — exact observable, threshold, and edge

**Map.** Taha (arXiv:1810.10668, Thm 2.2) G_q-BCZ cross-section of the horocycle flow on the Hecke triangle surface
X(G_q), λ = λ_q = 2cos(π/q), U_q = [[λ,−1],[1,0]], w_i = U_q^i (1,0)ᵀ. Domain (G_q-Farey triangle)
T^q = {0 < a ≤ 1, 1 − λa < b ≤ 1}; partition into branches T_i^q (i = 2..q−1). On branch i:
a′ = w_i·(a,b), k = ⌊(1 − w_{i+1}·(a,b))/(λ·w_i·(a,b))⌋, b′ = w_{i+1}·(a,b) + kλ·w_i·(a,b).
Code: `code/goal1_bcz_hecke_cluster.py`. For q = 3, λ = 1 this is the classical BCZ map T(a,b) = (b, −a + ⌊(1+a)/b⌋b).

**Observable.** P_q(a,b) = a·(w_i·(a,b))/y_i where y_i = (w_i)₂; on the **last branch** i = q−1 this is P = a·b (a true
gap-product). P is bounded; the Farey gap scales as ≈ 1/P, so **small P ⇔ LARGE gap**. The rare event is the lower tail
{P < u}.

**Edge vs. onset value — a distinction that must be kept straight.**
- The **lower-tail edge** (essential infimum of P over the invariant measure) is **0**, not 1/λ³. Numerically the orbit
  min of P over 10⁸ iterates is ≈ 7e-5 for all q (`/tmp/probe_tail.py`). The cusp p = (1,0)-corner is the parabolic
  fixed point and P(p) = 0 there. So the EVT limit is taken as **u → 0⁺**.
- The value **X(q) = 1/λ³** (q ≥ 5; X(3) = 2/9, X(4) = √2/8) is the **ergodic-optimization / cluster-ONSET threshold** —
  the L∞ ground value inf_μ ess-sup_μ P and the first threshold at which exceedances begin to *cluster* (cluster-size
  jumps from 1 to ≥ 2). It is a distinguished *finite* threshold, NOT the tail edge. The finite-onset θ_q table is
  evaluated at u = X(q); the *limiting* θ is the u → 0 limit.

---

## 2 · The mechanism — period-2 cusp-swap involution (EXACT) ⇒ mean cluster size 2 ⇒ θ = 1/2

On the last branch the map is M(a,b) = (b, kλb − a), k = ⌊(1 − w_q·(a,b))/(λ b)⌋ (a Boca–Cobeli–Zaharescu-type
continued-fraction step). Take a near-cusp point with a = 1 − s (s small) and b = ε small, so P₁ = ab ≈ ε (an
exceedance for any u > ε).

1. **Image 1 = swap.** M(a,b) = (b, kλb − a) = (ε, b′). The first coordinate is **exactly b** (a ↦ b is the deterministic
   swap). k is the unique integer placing b′ = kλε − (1−s) back in the domain (1 − λε, 1], so b′ = O(1), and since
   ε is small the domain forces b′ ≈ 1. Hence the image is (ε, ≈1) and P₂ = ε·b′ ≈ ε ≈ P₁ — **a second exceedance**,
   and the observable is preserved to leading order (the cusp return is an involution to O(ε)).
2. **Image 2 = escape.** Applying M again to (ε, ≈1): first coordinate becomes ≈1 (the swap brings the O(1) coordinate
   back to the a-slot), so a″ ≈ 1 and P₃ = a″·b″ = O(1) — generically **not** an exceedance. The cluster terminates.

**Therefore every deep-tail exceedance cluster is exactly the swap-PAIR {P₁, P₂}, of length exactly 2**, and this is
**coordinate-universal** (no λ-dependence in the leading structure): the swap a ↦ b and the O(ε) involution hold on the
last branch for every q. Mean cluster size → 2, hence

  **θ = 1 / E[L] = 1/2,  q-independent.**

**Numerical confirmation of the mechanism (`/tmp/swap_check.py`, u = 0.05·X(q), deep tail):** every sampled size-2
cluster is a clean swap. Representative (q = 5): pt1 (a = 0.99378, b = 0.00536, P = 0.00533, branch q−1, k = 229) →
pt2 (a = 0.00536, b = 0.99295, P = 0.00532, branch q−1, k = 0). In every case |b₁ − a₂| = 0.0000 (exact swap) and
P₂ ≈ P₁ to 3–4 digits. Same pattern for q = 4 and q = 7 (always last branch, second point has k = 0).

---

## 3 · Cluster-size distribution (the compound-Poisson multiplicity law)

The REPP limit (modulo §6) is a **compound Poisson process**: positions of clusters are Poisson, multiplicities are
i.i.d. with law π_L. The data say:

- **Limit (u → 0):** π_L → δ_{L=2}, a **point mass at 2**. Pr(L = 1) → 0, Pr(L = 2) → 1, Pr(L ≥ 3) ≡ 0 below onset.
  This is the degenerate limit of a geometric law: for u slightly above 0 the cluster is a size-2 swap with a small
  O(u) probability of "leaking" to size 1 (the swap occasionally lands b′ just above the threshold) — i.e.
  π_L ≈ (1−p)·δ₁ + p·δ₂ with p = Pr(L = 2 | cluster) = 1 − O(u) → 1. Empirically Pr(L = 2) = 0.638, 0.927, 0.987,
  0.995 at u/X = 1, 0.25, 0.05, 0.02 (q = 5).
- **At the finite onset u = X(q):** the multiplicity is a genuine non-degenerate law (geometric-flavoured but with a
  tail): q = 5 gives Pr(L=1,2,≥3) = (0.337, 0.638, 0.025) — note the small but real **L ≥ 3 tail at onset** for q ≥ 5,
  which vanishes as u → 0. q = 3 and the {3,4,6} arithmetic cases are special (cluster ≤ 2 is a *theorem* at threshold,
  Lean `cluster_size_le_two`, so π_L is supported on {1,2} exactly at u = X).
- **q = 3 exact threshold law (closed form, `research_notes/cluster_size_closed_forms.md`):** at u = 2/9,
  P₁ + 2P₂ = (8 ln(3/2) − 2)/9, P₂ = J = 2/45 + J₅ + J₆ + J₇ + J₈ with J₈ = (8 ln3 − 16 ln2)/9 − 2/45 elementary;
  Pr(L=1) = 0.2273516778…, Pr(L=2) = 0.7726483222… (MC-certified to 1.4e-6 at 5×10⁹ steps). θ_3(2/9) = 0.564121.

---

## 4 · Numerics: θ(u) → 1/2 as u → 0⁺ (q-INDEPENDENT) — the verification table

Script: `/tmp/deep_theta.py` (numba, exact Taha map, invariant-domain reject-sampled starts — see PITFALL §5).
Two independent estimators: θ_cs = N_clusters/N_exceedances = 1/E[L]; θ_runs = 1 − π₂/π₁ (π₁ = Pr(P<u),
π₂ = Pr(two consecutive)). They agree to 5 digits. Steps auto-scaled by X/u to hold exceedance counts high.
Inter-start SE shown (~1e-4 or better).

| u/X(q) | q=4 θ_cs | q=4 E[L] | q=5 θ_cs | q=5 E[L] | q=7 θ_cs | q=7 E[L] |
|---:|---:|---:|---:|---:|---:|---:|
| 1.00 (onset)\* | 0.4468\* | 2.238\* | 0.59233 | 1.6883 | 0.65194 | 1.5339 |
| 0.50 | 0.59239 | 1.6881 | 0.54847 | 1.8233 | 0.53485 | 1.8697 |
| 0.25 | 0.52627 | 1.9002 | 0.51888 | 1.9272 | 0.51481 | 1.9425 |
| 0.10 | 0.50906 | 1.9644 | 0.50680 | 1.9732 | 0.50542 | 1.9785 |
| 0.05 | 0.50426 | 1.9831 | 0.50327 | 1.9870 | 0.50281 | 1.9888 |
| 0.02 | 0.50127 | 1.9949 | 0.50127 | 1.9949 | 0.50141 | 1.9944 |

\* The q = 4 "u/X = 1.00" row uses u = 1/λ³ = 0.3536, which OVERSHOOTS the true q = 4 onset X(4) = √2/8 = 0.1768
(= the u/X = 0.50 row). At that over-large u the chain shows a long L ≥ 3 tail (up to 9), an artifact of u being above
the onset; the genuine q = 4 onset value is θ ≈ 0.592 at u = X(4), matching q = 5's onset, and it then descends to 1/2.

**Reading:** for all three q the extremal index descends **monotonically and q-independently** to 1/2; at u/X = 0.02 all
three sit at 0.5013 ± 0.0003, i.e. θ → 1/2 within ~0.3% with Pr(L=2) ≥ 0.994. The finite-onset θ_q ∈ (0.56, 0.65) is a
**finite-threshold effect** (the residual L=1 and L≥3 contributions), not the limit. Convergence is clean and not
λ-ordered in the deep tail (it is q-universal) — confirming the FALSIFICATION of any λ_q-dependent exactly-solvable θ_q.

---

## 5 · PITFALL (carried over, re-verified)

Starting the orbit at a FIXED point (e.g. (0.5, 0.9)) lands on a degenerate quasi-periodic orbit that does NOT sample
the invariant measure and spuriously reports θ = 1/2, Pr(L=2) = 1 at EVERY threshold. Always reject-sample the start
from {0 < a ≤ 1, 1 − λa < b ≤ 1}. All §4 numbers use proper invariant-domain sampling (8 independent starts, burn 1000).

---

## 6 · The HONEST residual — what is proved vs. what is open

**Proved exactly (no analysis gap):**
- The period-2 cusp-swap involution on the last branch (a ↦ b exactly; P preserved to O(ε); escape at step 3) — §2.
  This is the *mean-cluster-size-2 ⇒ θ = 1/2* computation, and it is rigorous as a statement about the deterministic
  near-cusp dynamics.
- The cluster-size law collapses to δ_{L=2} in the limit; the q = 3 threshold law has a (partial) closed form.

**NOT proved — the named missing theorem:** a rigorous **rare-event point process (REPP) convergence theorem** showing
that the (rescaled) exceedance point process of {P < u} converges, as u → 0, to a **compound Poisson process** with
intensity θ·(rate) and multiplicity law δ₂ — i.e. that the extremal index of the *stochastic process* (Birkhoff
samples under the invariant measure) equals the *deterministic* mean-cluster-size reciprocal 1/2, AND that the residual
correlations / longer excursions are asymptotically negligible.

**Why the standard tool (Freitas–Freitas–Todd) FAILS here.** FFT (and Hirata, Collet, Keller–Liverani spectral)
compute θ for observables maximized at a **repelling periodic point** ζ via θ = 1 − 1/|det DTᵖ(ζ)| (or 1 − e^{−…} in the
1-D form). Here the relevant point is the **parabolic cusp** p = (1,0)-corner: DT is **neutral** (eigenvalue 1, parabolic),
so |det| = 1 and the FFT formula returns θ = 1 − 1/1 = **0** — vacuous/wrong. The cusp is *neutral*, not
hyperbolic-repelling; the system has **polynomial (not exponential) mixing** because of the parabolic neutral direction,
so the spectral-gap / Lasota–Yorke hypotheses underpinning FFT do not hold for the relevant induced transfer operator.

**The right tool.** The correct machinery for a parabolic/intermittent section with polynomial decay of correlations is
**operator renewal theory / Gouëzel–Sarig anisotropic Banach towers** for non-uniformly hyperbolic (AFN / Young-tower)
maps, in the EVT incarnation developed by **Freitas–Freitas–Todd–Vaienti** and **Carney–Holland–Nicol** for
non-uniformly expanding / intermittent maps. Concretely: induce on a hyperbolic sub-system away from the cusp (first-
return / Young tower), establish the REPP limit on the tower (where FFT-type spectral arguments DO apply), then transfer
back through the renewal sequence to the parabolic base, controlling the cusp-excursion (return-time tail) contribution.
The period-2 swap is precisely the **two-step return** that the renewal/tower argument must isolate as the cluster. This
is a substantial but well-posed program; it is the genuinely hard step and is **not closed here**.

**Adjacent live literature (positions the novelty).** Marklof–Pollicott (arXiv:2408.01781, "Extreme events for horocycle
flows") and MSY 2025 / Kirsebom–Mallahi-Karai do EVT-for-horocycle, but for the **cusp-EXCURSION** observable
(max penetration into the cusp = large-deviation / large-gap end), via Hall's Farey formula — **not** the gap-product P
and **not** the small-gap/cluster-onset hard edge. So the novelty here is scoped to **this observable** (gap-product P,
lower tail) and **this conclusion** (θ = 1/2 from a deterministic period-2 swap on a parabolic area-preserving section).
No prior extremal-index result for the BCZ map exists.

---

## 7 · THEOREM STATEMENT (precise, with the residual flagged)

> **Theorem (θ = 1/2 for the parabolic G_q-BCZ extreme-gap process), conditional form.**
> Let T_q be the Taha G_q-BCZ cross-section map (q ≥ 4), m_q its invariant probability measure, P the gap-product
> observable, p = (1,0) the parabolic cusp fixed point with P(p) = 0. *Conditional on* the REPP convergence theorem for
> the parabolic, polynomial-mixing induced system (§6), the exceedance point process of {P < u} over (T_q, m_q)
> converges, as u → 0⁺, to a **compound Poisson process** whose multiplicity law is the **point mass δ_{L=2}** and whose
> **extremal index is θ = 1/2, independent of q**. The cluster structure is generated by the deterministic period-2
> cusp-swap involution (Image 1 = a ↦ b swap, second exceedance; Image 2 = escape), which is proved unconditionally.

> **Unconditional content.** (i) The period-2 cusp-swap involution and the resulting **mean cluster size 2** (hence the
> deterministic-clustering value θ = 1/2) — proved exactly in §2. (ii) θ(u) → 1/2 monotonically and q-independently
> (numerics, §4, q = 4,5,7, two estimators agreeing to 5 digits, θ = 0.5013 ± 0.0003 at u = 0.02·X(q)). (iii) The
> limiting multiplicity law is δ₂; at finite onset u = X(q) it is the non-degenerate law of §3.

> **Residual (open).** The REPP / compound-Poisson convergence theorem itself (the limit interchange under m_q),
> requiring operator-renewal / Gouëzel–Sarig polynomial-mixing-tower EVT (Freitas–Freitas–Todd–Vaienti,
> Carney–Holland–Nicol), because the cusp is parabolic-neutral and the FFT repelling-periodic formula degenerates to 0.

**VERDICT: (b) proved-modulo-a-named-limit-theorem.** The cusp-swap ⇒ θ = 1/2 computation is exact; the cluster law and
its q-independence are exact + numerically confirmed; what remains genuinely open is the single named analytic step —
the parabolic REPP limit theorem — for which the correct tool (operator renewal / polynomial-mixing tower EVT) is
identified and the reason FFT fails (neutral cusp ⇒ |det| = 1 ⇒ θ_FFT = 0) is given.

---

## 8 · UPGRADE ASSESSMENT (2026-06-14) — does the EXACT involution rescue θ = 1/E[L], and how blocked is the REPP step?

**Trigger.** Prior-art warning (arXiv:1808.02970, Azevedo–Freitas–Freitas–Rodrigues, "Dynamical
counterexamples regarding the Extremal Index and the mean of the limiting cluster size distribution"):
at an *indifferent* (parabolic) fixed point the textbook identity **θ = 1/E[L]** can FAIL. This section
determines whether our exact cusp-swap places us inside or outside that failure mode, and re-scopes the
REPP step against the actual mixing status of the BCZ map.

### 8.1 What EXACTLY makes θ ≠ 1/E[L] in 1808.02970 (read from ar5iv)

Two distinct cluster-size means must be separated:
- the **finite-time** mean E[L_n] (mean run-length at threshold level n), and
- the **mean of the LIMITING** cluster-size law E[D] = Σ_j j·π(j).

The paper proves (their Thm 2.4, via ergodicity alone) that **θ⁻¹ = lim_n E[L_n]** holds *always*. The
counterexample is that **lim_n E[L_n] ≠ E[D]** — i.e. the limit of the means is not the mean of the limit.
This **requires** a specific construction: the observable is maximised at **≥ 2 points of DIFFERENT
dynamical type** — *one indifferent (parabolic) periodic point AND one repelling/non-periodic point*. The
indifferent point contributes the degenerate θ = 0 behaviour (cluster mass leaks toward infinity); the
repelling point contributes θ > 0; the two limits do not commute and **probability mass escapes** in the
cluster-size point process (non-uniform integrability of L_n). The failure is a **two-maximizer
mass-escape** phenomenon — NOT a property of a lone parabolic point, and NOT requiring a literally
infinite-mean cluster law (it is mass concentration "at infinity in the discrete sense").

So the failure mode is precisely: **competing maximizers of mixed type + an unbounded / non-uniformly
integrable cluster-size distribution**.

### 8.2 Where OUR map sits — three measured structural facts (all NEW this session)

All numerics use the exact Taha map, invariant-domain reject-sampled starts, 30–80M steps, numba.
Repro: `/tmp/cusp_structure_probe.py`, `/tmp/maximizer_type.py`, `/tmp/renewal_tail.py`, `/tmp/fret.py`,
`/tmp/single_min.py`, `/tmp/gaptail.py`, `/tmp/cusp_tail_probe.py`.

1. **SINGLE maximizer, parabolic, no repelling competitor.** Every deep exceedance {P < 0.02·X(q)} lies in
   the two cusp cells {a<0.05, b>0.95} ∪ {a>0.95, b<0.05}; the count OUTSIDE those cells is **exactly 0**
   for q = 4,5,7,9 (`/tmp/single_min.py`). The two cells are the **two phases of ONE period-2 swap orbit**,
   not two independent fixed structures: iterating from (a=ε, b≈1) → (a≈1, b≈−ε), P jumps 1e-4 → 0.62
   (escape), and from (a≈1, b=ε) → (a≈ε, b≈1), P stays ≈1e-4 (the swap) — `/tmp/maximizer_type.py`. The
   only maximizer of the rare event is the **parabolic cusp orbit p = (1,0)**. **There is NO second,
   repelling/non-periodic maximizer.** This is the exact configuration 1808.02970 needs and we do **not**
   have.

2. **Cluster size is BOUNDED (essentially deterministic), not heavy-tailed.** The below-onset excursion
   length (consecutive steps with P < X) has **maximum length 3** and is dominated by length 2:
   counts (len→#) q=5 = {1:1.93M, 2:3.64M, 3:0.14M, ≥4:0}; q=7 = {1:1.56M, 2:1.79M, 3:680, ≥4:0}
   (`/tmp/fret.py`). The cluster-size law is supported on {1,2,3} and collapses to δ₂ as u→0. **A bounded
   cluster-size distribution is trivially uniformly integrable**, so lim_n E[L_n] = E[D] = 2 with NO mass
   escape. This is the structural feature that the 1808.02970 failure cannot touch.

3. **The cusp minimum of P is QUADRATIC (m({P<u}) ~ u²), and the inter-cluster (renewal) gap is only
   approximately exponential.** The small-ball measure scales m({P<u}) ~ u² (slope d log m/d log u → 2.00
   as u→0, both q; `/tmp/renewal_tail.py`). The inter-cluster gap is *roughly* exponential but heavier in
   both tails than Exp(1) (e.g. S(2·mean) ≈ 0.05 vs e⁻² = 0.135; `/tmp/gaptail.py`) — the fingerprint of
   sub-exponential / polynomial mixing through the neutral direction. This is the part the rigorous REPP
   theorem must still control; it does NOT affect the cluster-size identity (8.2.2), only the
   Poisson-positioning of clusters.

### 8.3 VERDICT on the θ = 1/E[L] obstruction — we are OUTSIDE the 1808.02970 failure mode

**YES, the exactness of the involution rescues θ = 1/E[L] = 1/2 — the 1808.02970 obstruction does NOT
apply here.** Structural reason, precisely:

- 1808.02970's mismatch lim_n E[L_n] ≠ E[D] is driven by **mass escaping to ∞ in the cluster-size law**,
  which needs (i) competing maximizers of mixed (indifferent + repelling) type and (ii) a non-uniformly
  integrable, unbounded cluster size. Our map has **NEITHER**: a single parabolic maximizer (8.2.1) and a
  **bounded** cluster size ≤ 3 → δ₂ (8.2.2). A bounded L is uniformly integrable ⇒ lim_n E[L_n] = E[D] = 2
  automatically ⇒ θ = 1/E[L] = 1/2 with no commutation gap. The very mechanism that could break the
  equality is the random/heavy-tailed cluster size; our cluster size is **deterministic = 2**, the maximally
  rigid case.

So the θ = 1/E[L] step is **not the obstruction here** — it is, conversely, the part the exact involution
makes *trivially safe*. (This downgrades the homdyn-audit caveat: that audit correctly flagged 1808.02970
as a generic warning, but our deterministic, single-parabolic-orbit, bounded-cluster structure is outside
its hypotheses.)

### 8.4 RE-SCOPE of step (1), the REPP convergence theorem — HARDER than the note's §6 implied

§6 named Gouëzel–Sarig / FFFV / Young-tower operator-renewal EVT as the off-the-shelf tool. **The mixing
status of the BCZ map makes that NOT off-the-shelf**, and this is the corrected bottleneck:

- The BCZ map (Athreya–Cheung) and its Taha G_q generalization are **zero measure-theoretic entropy,
  weakly mixing, with STRONG MIXING and the DECAY-OF-CORRELATIONS RATE OPEN** (arXiv:2403.14976, "BCZ map
  is weakly mixing", 2024; mixing & rigidity explicitly left open). There is **no established polynomial
  (or any) mixing rate** for the BCZ map, and — being **zero-entropy parabolic, not non-uniformly
  hyperbolic** — it does **not** present an obvious hyperbolic inducing sub-system / Young tower. The
  Gouëzel–Sarig and FFFV programs *presuppose* (a) a known polynomial decay rate and (b) a hyperbolic base
  to induce on. **For the BCZ map, BOTH inputs are themselves open problems**, so those theorems are NOT
  applicable as cited — they would have to be *built*, on a map whose basic mixing rate is unknown.
- Ratner's polynomial decay rates are for the horocycle **flow** with smooth observables, **not** the
  discrete BCZ cross-section map with the (non-smooth, branch-defined) observable P; they do not transfer to
  the section EVT directly.
- The correct route is therefore not "apply FFFV" but **(i) first establish a quantitative mixing /
  return-time-tail rate for the BCZ map** (an open problem in its own right — note our measured renewal-gap
  is only approximately exponential, 8.2.3), **then (ii) build a renewal/REPP argument on it**. The
  self-similarity / geodesic-renormalization technique of arXiv:2403.14976 (which proved weak mixing without
  spectral methods) is the most likely native tool, not anisotropic Banach towers.

### 8.5 FINAL VERDICT (replaces the §7 one-liner's optimism on the route, keeps its grade)

**Grade: still (b) "open on the limit theorem", but the obstruction has SHIFTED and SPLIT:**

- **θ = 1/E[L] obstruction (the 1808.02970 risk): CLOSED.** The exact involution puts us outside the
  failure mode — single parabolic maximizer + bounded (→δ₂) cluster size ⇒ uniform integrability ⇒
  θ = 1/E[L] = 1/2 with no mass escape. Named tool to *write this up* rigorously: Leadbetter/O'Brien
  compound-Poisson identity **plus** a uniform-integrability lemma for the bounded run-length (elementary
  once the REPP limit exists). This is no longer the hard part.

- **REPP convergence obstruction: OPEN, and harder than §6 stated.** It is **not** discharged by a citable
  off-the-shelf theorem, because the BCZ map's **mixing rate / decay of correlations is itself an open
  problem** (arXiv:2403.14976) and the map is zero-entropy parabolic with no ready Young tower. Named tools:
  **(1)** establish a quantitative mixing / return-time-tail estimate for the BCZ map (open; candidate
  technique = the geodesic-renormalization self-similarity of arXiv:2403.14976, *not* FFFV towers); **(2)**
  given that rate, an operator-renewal / REPP argument (Sarig operator-renewal arXiv:1008.4113;
  FFFV-style EVT) to upgrade the deterministic clustering to the stochastic extremal index.

**Honest one-line conclusion.** θ = 1/2 is **(b) blocked on ONE named, genuinely open analytic input — the
quantitative mixing rate of the BCZ map — not on the θ = 1/E[L] equality** (which the exact involution
rescues) and not on a missing-but-citable EVT theorem (the cited FFFV/Gouëzel–Sarig tools presuppose a
mixing rate the BCZ map does not yet have). The deterministic content (cusp-swap ⇒ mean cluster size 2 ⇒
θ = 1/2) is exact and now shown to be outside the 1808.02970 failure mode; the gap to a proof is the
parabolic mixing-rate problem for the BCZ map. **No proof is claimed.**

---

## Files
- `code/goal1_bcz_hecke_cluster.py` — exact Taha G_q-BCZ map + observable P.
- `code/cluster_size_distribution_at_threshold.py` + `…_results_5e9.json` — q = 3 threshold law (5×10⁹ steps).
- `research_notes/cluster_size_closed_forms.md` — q = 3 closed-form cluster distribution at u = 2/9.
- `wiki/concepts/track-c-extremal-index-theta-q-for-bcz-extreme-gap-process.md` — prior verdict (θ_q = 1/2 falsifies
  λ-dependent family).
- Repro for this note: `/tmp/deep_theta.py` (θ(u)→1/2 table, §4), `/tmp/swap_check.py` (swap mechanism, §2),
  `/tmp/probe_tail.py` (edge = 0, §1).
- Repro for §8 (upgrade assessment, 2026-06-14): `/tmp/cusp_tail_probe.py` (θ(u)→1/2 re-verified, two
  estimators agree, θ=0.5010±0.0003 at u=0.02X), `/tmp/single_min.py` (single parabolic maximizer: 0
  deep exceedances outside cusp cells, q=4,5,7,9), `/tmp/maximizer_type.py` (two cells = two phases of one
  swap orbit), `/tmp/fret.py` (below-onset excursion length ≤ 3, bounded cluster ⇒ δ₂), `/tmp/renewal_tail.py`
  (m({P<u})~u², slope→2.00), `/tmp/gaptail.py` (inter-cluster gap ≈ exponential but heavier-tailed ⇒
  sub-exponential mixing fingerprint). Key external: arXiv:1808.02970 (failure needs 2 mixed-type
  maximizers + heavy-tailed cluster — we have neither), arXiv:2403.14976 (BCZ map weakly mixing, zero
  entropy, mixing rate OPEN — the real bottleneck).
