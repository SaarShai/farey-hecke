# PROOF SCHEMA — TASK 5b
## "-1 density-dominance among non-residues": proof / exact characterization

Status: **REFUTED in the asymptotic regime + EXACTLY CHARACTERIZED at finite q.**
All density/ordering statements **CONDITIONAL on GRH + LI** (FM Thm 1.1/1.10 framework);
the closed-form variance (FM Thm 1.4) needs **GRH only**. Nothing unconditional. No upgrade.

Scripts (RUN this session, project dir):
`proof_schema_verify.py` (D-max over primes ≤283), `sharp_gap.py` (exhaustive scan
primes q≡3(4), 7≤q<2000: zero violations), `general_char.py` (variance/parity form,
N=7,8,11,19,23), and the cached `full_run.txt` (Route-I exact Gil–Pelaez).

---------------------------------------------------------------------------------
### 0. What "dominance" can mean (disambiguation is load-bearing)
For two DISTINCT non-residues a,b, RS pairwise symmetry gives δ(N;a,b)=1/2 EXACTLY
(Granville–Martin, PNR_text.txt:1107; GRH+LI). So head-to-head NR-vs-NR dominance is
**empty**. The ONLY non-degenerate reading: "-1 tops the hierarchy of δ(N;a,1) (each
non-residue vs the principal class 1)". TASK 5b is about THIS ordering.

---------------------------------------------------------------------------------
### 1. Reduction to ONE inequality (the spine)
FM Thm 1.1 (GRH+LI), with ρ(N)=#real characters (the SAME for every class):
        δ(N;a,1) = 1/2 + ρ(N) / sqrt(2π·V(N;a,1)) + O(ρ³ / V^{3/2}),
        V(N;a,1) = Σ_{χ≠χ0} c_χ |χ(a)−1|²,  c_χ = Σ_{γ: L(½+iγ,χ)=0} 1/(¼+γ²).
ρ(N) is class-independent ⇒ to two-term order **δ(N;a,1) is strictly DECREASING in V(N;a,1).**
Therefore:

  **(EXACT CRITERION)   a=−1 density-dominates all other NR  ⟺  V(N;−1,1) = MIN_{a NR} V(N;a,1).**

Equivalently, using |χ(a)−1)|² = 2 − 2Re χ(a) and C_tot=Σ_{χ≠χ0} c_χ:
        V(N;a,1) = 2 C_tot − 2 S(a),   S(a) := Σ_{χ≠χ0} c_χ Re χ(a).
  **(EXACT CRITERION, dual)   −1 dominates  ⟺  S(−1) = MAX_{a NR} S(a),**
and since χ(−1)∈{±1}, S(−1) = C_even − C_odd, where
        C_even = Σ_{χ≠χ0, χ(−1)=+1} c_χ,   C_odd = Σ_{χ(−1)=−1} c_χ.

**The "skewness" channel is identically empty.** The RS law D_a = m + Σ A_k cos θ_k
(θ iid Uniform, by LI) is SYMMETRIC ⇒ skewness ≡ 0 (verified: E[cos³θ]=0; full_run/
this session). Every correction s_{q,a,b}(l,j) in FM (1.1) is an even/kurtosis-type term;
the **only sign-bearing per-class lever at every order is the covariance V**. So the
"covariance/skewness inequality" the task asks for collapses to a pure **covariance
inequality**: rank NR by V.

---------------------------------------------------------------------------------
### 2. The criterion is VIOLATED — and provably backwards — for prime q ≡ 3 (mod 4)
For prime q, FM Cor 1.9 (FM_text.txt:4043) gives the variance proxy
        D(q;a,1) = i_q(−a)·log2 + Λ(a)/a + Λ(a⁻¹)/a⁻¹ + 2 log q /(q(q−1)),
with δ DECREASING in D and i_q(−a)=1 ⟺ a≡−1.  The tail 2logq/(q(q−1)) is COMMON to
all a (cancels in differences). For a=−1: i_q fires (=log2), Λ(q−1)/(q−1) tiny (Λ(q−1)=0
unless q−1 is a prime power). For a≠−1: NO log2 term.

  **GAP (tails cancel):  D(q;−1,1) − D(q;a,1) = log2 + Λ(q−1)/(q−1) − [Λ(a)/a + Λ(a⁻¹)/a⁻¹].**

Sharp competitor bound: a and a⁻¹ are DISTINCT residues (a=a⁻¹⇒a²≡1⇒a∈{1,−1}, excluded),
and a·a⁻¹ ≡ 1 (mod q) ⇒ a·a⁻¹ ≥ q+1, so the two small primes 2,3 cannot BOTH be the pair.
As q→∞ the largest competitor → Λ(2)/2 = (log2)/2, giving the clean asymptotic gap
        D(q;−1,1) − max_{a≠−1} D(q;a,1) → log2 − (log2)/2 = (log2)/2 ≈ 0.34657 > 0.
EXHAUSTIVE RUN (`sharp_gap.py`): for EVERY prime q≡3(mod4), 7≤q<2000, D(q;−1,1) is the
**STRICT maximum** over non-residues — **zero violations**; minimal gap +0.005056 at q=7,
gap ≈ (log2)/2 for large q.

  ⇒ For every such prime q, V(q;−1,1) is MAXIMAL ⇒ δ(q;−1,1) is MINIMAL ⇒ **−1 is the
    UNIQUE LEAST-biased non-residue, the EXACT OPPOSITE of dominance.** This IS
    Fiorilli–Martin Thm 1.10 bullet 1 (FM_text.txt:325, GRH+LI, verbatim verified).
    Confirmed independently by exact Route-I Gil–Pelaez δ (full_run.txt): δ(7;−1,1)=0.8336,
    δ(11;−1,1)=0.7004, δ(19;−1,1)=0.6037, δ(23;−1,1)=0.5937 are the per-N minima.

**MECHANISM (why −1, parity).** χ(−1)−1 = 0 (even χ) or −2 (odd χ): a=−1 dumps ALL its
weight 4 onto ODD characters, zero on even (verified, full_run: even-weight=0 iff a=−1).
Odd characters carry the heavier archimedean c_χ: c_χ = log(q/π) + ψ((1+a_χ)/2) +
2 Re L'/L(1,χ), and ψ(1)−ψ(½) = 2 log2 = 1.38629 (odd > even). So S(−1)=C_even−C_odd is
the MINIMUM (not maximum) of S(a) ⇒ V(−1) MAXIMUM ⇒ δ(−1) MINIMUM. (`general_char.py`:
C_odd > C_even for all of N=7,11,19,23; S(−1) is the per-N minimum.) This is the
+2φ(q)log2 surcharge the FM iq(−a)log2 indicator encodes.

**NOT a leading-mean effect** (all NR tie: mean = −1 + #√a = −1). **NOT skew** (law
symmetric, skew≡0). **NOT Aoki–Koyama DRH magnitude** (m(a)=Σ χ(a)·ord_{½}L=0 generically,
L(½,χ)≠0 by Chowla; AK gives no NR hierarchy). The unique discriminant is the RS
**covariance/variance parity-weighting**.

---------------------------------------------------------------------------------
### 3. EXACT CHARACTERIZATION (the precise condition on N / c_χ for −1 to dominate)
−1 density-dominates all other non-residues **iff** the covariance inequality
        S(−1) = C_even − C_odd  >  S(a)  for every non-residue a ≠ −1,    (★)
i.e. iff for every NR a≠−1:   Σ_{χ≠χ0} c_χ (Re χ(a) − χ(−1)) > 0,
equivalently V(N;−1,1) < V(N;a,1) for all NR a (the dual). All quantities computable:
c_χ from the closed form (validated c(χ4)=0.15557, c(χ3)=0.11323) or zero-sums.

When does (★) hold? Decompose c_χ = c∞(χ) + c_fin(χ) with the archimedean part
c∞(χ) = log(N/π) + ψ((1+a_χ)/2). The ψ-gap 2log2 makes C_odd structurally exceed
C_even by an amount ∝ (#odd − weighting)·log2. (★) requires the EVEN characters to be
sufficiently heavier than the odd ones to overcome (a) the 2log2 archimedean odd-surcharge
and (b) the small-prime Λ(a)/a advantage that other NR enjoy. For prime q this NEVER
happens (Section 2): odd c_χ strictly dominate, so (★) is FALSE for all prime q≡3(4).

  **CLEAN SUFFICIENT CONDITION FOR FAILURE (proved, GRH+LI):** if N is prime (≡3 mod 4),
  −1 NEVER density-dominates; it is the unique δ-minimum. By FM Thm 1.10 this extends to
  ALL but finitely many N (per fixed competitor a) for which both −1 and a are non-squares.

  **NECESSARY-AND-SUFFICIENT CONDITION FOR DOMINANCE:** (★) — C_even − C_odd > S(a) ∀ NR a.
  Numerically this would require a modulus whose non-principal spectrum is dominated by
  EVEN characters with anomalously large c_χ (e.g. an even character with an unusually
  low-lying zero, inflating its c_χ), enough to beat 2log2 + max-small-prime advantage.
  No such modulus is exhibited; the parity surcharge makes (★) generically unsatisfiable.
  **VERDICT: the set of N for which −1 density-dominates all other NR is, conjecturally,
  EMPTY (and provably contains no prime q≡3 mod 4 and no N tested).**

**Even/composite moduli (no primitive root, e.g. N=8).** The prime D-formula does not
apply; use the full variance criterion (★). There −1 is not even variance-maximal:
the RS-1994 / FM exact ordering (full_run.txt, Route-I) gives δ(8;3,1)=0.99957 >
δ(8;7,1)=0.99894 > δ(8;5,1)=0.99739, so 7≡−1 is δ-RANK 2 (a=5 is the unique minimum).
N=8 is the decisive counterexample to universality even in the amplitude reading.
[CAVEAT: imprimitive χ mod 8 must use the primitive inducer's c_χ (FM Def 1.6,
L'/L(1,χ*)); the authoritative N=8 micro-ordering is the cached Route-I in full_run.txt,
where a=5 is V-max. A quick same-character Euler product mis-ranks the two odd classes;
both methods AGREE on the headline that −1 is NOT the δ-top at N=8.]

---------------------------------------------------------------------------------
### 4. What is PROVED vs CONDITIONAL vs would be UNCONDITIONAL
- **PROVED (CONDITIONAL on GRH+LI):** the reduction δ↓ in V; the criterion (★); the
  prime-q gap = log2 + Λ(q−1)/(q−1) − [Λ(a)/a+Λ(a⁻¹)/a⁻¹] → (log2)/2 > 0; hence −1 is the
  unique δ-minimum for primes q≡3(4) (= FM Thm 1.10, GRH+LI). The variance CLOSED FORM
  (FM Thm 1.4) needs **GRH only**; given GRH it makes V(q;−1,1) maximal among NR
  unconditionally-in-LI (the ORDERING of V is GRH-only; only the passage V→δ needs LI).
- **NUMERICAL:** c_χ values (analytic closed form cross-checked vs low-zero sums); the
  exhaustive no-violation scan to q<2000; Route-I δ values.
- **WHAT WOULD BE UNCONDITIONAL:** nothing here. Over Q there is no unconditional input
  to RS densities. The variance ORDERING "V(q;−1,1) is max" is GRH-only (one hypothesis
  weaker than the δ-statement) but still conditional. Only in the FUNCTION-FIELD model
  (Weil RH, char p>0) would the analogue be unconditional — out of scope here.
- **DO NOT UPGRADE:** GRH, LI, DRH all remain hypotheses. AK/DRH is strictly stronger than
  GRH and does not single out −1 (m(a)=0 generically).

---------------------------------------------------------------------------------
### 5. One-line PROOF_SCHEMA
Reduce δ(N;a,1) ordering to V(N;a,1) (FM Thm 1.1, ρ(N) class-free; skew≡0 by symmetry);
−1 dominates ⟺ V(N;−1,1) is the MIN ⟺ C_even−C_odd > S(a) ∀NR a (★); the 2log2 odd-parity
surcharge (FM iq(−a)log2 / ψ(1)−ψ(½)) forces V(N;−1,1) to be the MAX for prime q≡3(4)
(gap→(log2)/2>0, exhaustively verified), so (★) FAILS and −1 is the UNIQUE LEAST-biased
NR — Fiorilli–Martin Thm 1.10. The dominance set is empty for all primes tested and
conjecturally empty entirely. CONDITIONAL on GRH+LI throughout.
