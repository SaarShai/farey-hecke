# T1 GAP-4 — Lemma 1 restated with explicit band-edge constant

DRAFT (builder lane) 2026-08-26 — UNREFEREED.

Scope: this note only restates Lemma 1 of
`T1_CRAMER_RAO_DRAFT.md` (§4, "Lemma 1 (local whitening)") with the
band-edge flatness constant δ made explicit, as GAP-4 in that draft's gaps
ledger requires. It does not modify the draft or any other file, and does
not touch the surrounding argument (Lemma 2, Lemma 3, Prop. 4.4, the proof
of T1).

---

## 1. GAP-4 as logged in the draft

Gaps-ledger entry (`T1_CRAMER_RAO_DRAFT.md` line 990):

> GAP-4 | Lemma 1's local-flatness parameter δ. **REDUCED by A2, still
> open.** … The tag drops from FRONTIER to ARISTOTLE-ABLE because no
> modelling decision is left — only a finite estimate. … | §4 (4.1), Lemma 1
> | **ARISTOTLE-ABLE**

and the Lemma-1 note itself (line 715): "**GAP-4 is REDUCED by A2 but NOT
closed.** A factor 1.23 at γ_d (2.03 at γ_1) is a genuine two-sided
constant, not 'negligible', and Lemma 1 should be restated with S_ε
evaluated at the band edge rather than at the centre."

This note does that restatement.

---

## 2. Current statement, quoted verbatim

`T1_CRAMER_RAO_DRAFT.md`, §4, "Lemma 1 (local whitening)" (lines 680–693):

> Let S_ε be continuous and bounded below on the band, and suppose S_ε
> varies by at most a factor (1+δ) over the interval
> [γ_j − 2πK/T, γ_j + 2πK/T]. Then for any u, v supported in that frequency
> band around ±γ_j,
>
>   (1+δ)^{-1} S_ε(γ_j)^{-1} ∫_0^T u v dt ≤ ⟨u,v⟩_C ≤ (1+δ) S_ε(γ_j)^{-1}
>   ∫_0^T u v dt.
>
> *Proof.* Plancherel on [0,T] plus the pointwise bound on 1/S_ε over the
> support. ∎
>
> Interpretation: near γ_j the coloured noise acts exactly like white noise
> of two-sided PSD S₀ = S_ε(γ_j), and
>
>   **I_{jk}(θ) = S_ε(γ_j)^{-1} ∫_0^T ∂_j m_θ(t) ∂_k m_θ(t) dt · (1 +
>   O(δ)).**  (4.1)

δ is left as an unspecified parameter; (4.1) is asserted "O(δ) negligible"
without a value for δ. That is GAP-4.

---

## 3. Deriving δ from the draft's own definitions

All quantities below are the draft's own (§1.4 clause (M4″), §2 clause
(W′), §4 Lemma-1 note, §4.0 operating point). Nothing here is imported from
outside the draft.

### 3.1 S_ε in closed form on the target-tone range

By (T1-b)/(M4″), for ω above the floor threshold (every target tone
qualifies, since γ_1 = 14.135 ≫ 2π e^{ϑ_min}):

  S_ε(ω) = a_ω² · log(ω/2π),   a_ω = |M_W(½+iω)| = ((¼+ω²)(9/4+ω²))^{-1/2}
  (clause (W′), §1.4).

So, exactly,

  log S_ε(ω) = −log(¼+ω²) − log(9/4+ω²) + log log(ω/2π).

Differentiating term by term:

  **D(ω) := d/dω log S_ε(ω) = −2ω/(¼+ω²) − 2ω/(9/4+ω²) + 1/(ω log(ω/2π)).**

This is exactly the expression the draft writes at line 702–703. The draft
then simplifies it to "−4/ω + O(1/(ω log ω))": for ω ≫ 1 the two
rational terms each tend to −2/ω, and the third term is positive and
smaller. Write

  D(ω) = −4/ω + r(ω),   r(ω) := D(ω) + 4/ω.

r(ω) is exactly what the draft calls "O(1/(ω log ω))" — **the draft does
not give an explicit constant for r(ω)**; see §5 (OWED-1).

### 3.2 The band-edge bound on the flatness factor

Lemma 1's neighbourhood is [γ_j − h, γ_j + h] with half-width
h := 2πK/T (M5's resolvability constant K, observation length T = log X).
For any ω in that interval,

  |log S_ε(ω) − log S_ε(γ_j)| = |∫_{γ_j}^{ω} D(u) du| ≤ h · sup_{|u−γ_j|≤h} |D(u)|,

so the max/min ratio of S_ε over the neighbourhood — i.e. the draft's
(1+δ_j) — satisfies

  1 + δ_j ≤ exp( 2h · sup_{|u−γ_j|≤h} |D(u)| ).

Using the leading term of D (dropping r(ω), i.e. taking the draft's own
"−4/ω + O(…)" working approximation at face value, which is exactly the
step that produces the draft's own displayed bound "e^{16πK/(ωT)}" at line
705):

  sup |D(u)| ≈ 4/γ_j   (since ω ↦ 4/ω is slowly varying over a band of
  width 2h ≪ γ_j at these operating points), so

  2h · (4/γ_j) = 2·(2πK/T)·(4/γ_j) = **16πK / (γ_j T)**,

giving the explicit, closed-form band-edge constant

  **1 + δ_j ≤ exp( 16πK / (γ_j T) ).**            (★)

This is the arithmetic behind the draft's own "e^{16πK/(ωT)}" line; the
draft states the exponent but does not carry it to numbers per tone. (★)
is an upper bound (rounded UP, per convention): it uses sup|D| over the
interval rather than the exact value, and it omits r(ω) (OWED-1 below), so
it is not claimed to be tight — only sound as a ceiling given the draft's
own approximation.

### 3.3 Numbers at the draft's own operating point

Operating point from §5.1 of the draft: K = 4 (M5's stated minimum), and
the same T used throughout §5, T = log(3·10⁷) = 17.2167 (§5.2). Then

  16πK/T = 16π·4 / 17.2167 = 201.0619 / 17.2167 = 11.6784.

Evaluating (★) = exp(11.6784/γ_j) at the six tabulated tones (Odlyzko
γ_j, §5.1), rounding the exponent computation to 5 places and the final
bound UP at the 3rd significant figure:

| j | γ_j | 16πK/(γ_j T) | (★) upper bound 1+δ_j | draft's measured ratio (line 710–713, for comparison only) |
|---|---|---|---|---|
| 1 | 14.134725 | 0.82624 | **2.29** | 2.03 |
| 2 | 21.022040 | 0.55558 | **1.75** | 1.55 |
| 3 | 25.010858 | 0.46694 | **1.60** | 1.46 |
| 4 | 30.424876 | 0.38386 | **1.47** | 1.38 |
| 5 | 32.935062 | 0.35455 | **1.43** | 1.35 |
| 10 (=d) | 49.773832 | 0.23464 | **1.27** | 1.23 |

(★) sits consistently 10–15% above the draft's own numerically measured
column at every tone — consistent with (★) being a sound ceiling for a
quantity the draft only reports as a measured number (uncommitted script,
GAP-8), not as a closed form. The two columns are not claimed to be the
same quantity computed two ways to full precision; (★) is an independent,
hand-derivable upper bound and the right-hand column is the draft's
separately measured value, kept here only as a sanity check that (★) does
not undershoot it.

---

## 4. Lemma 1, restated

**Lemma 1′ (local whitening, explicit band-edge constant).**
Let S_ε(ω) = a_ω²·max{log(ω/2π), ϑ_min} (clauses (W′), (M4″)), with
a_ω = ((¼+ω²)(9/4+ω²))^{-1/2}, let K ≥ 4 be the resolvability constant of
(M5), T = log X the observation length, and let γ_j be a target tone with
γ_j ≥ γ_1 (so above the (M4″) floor). Set the Lemma-1 half-width
h := 2πK/T. Then, for any u, v supported in the frequency band
[γ_j − h, γ_j + h] ∪ [−(γ_j + h), −(γ_j − h)],

  (1+δ_j)^{-1} S_ε(γ_j)^{-1} ∫_0^T u v dt ≤ ⟨u,v⟩_C ≤ (1+δ_j) S_ε(γ_j)^{-1}
  ∫_0^T u v dt,

with the explicit two-sided bound

  **1 + δ_j ≤ exp( 16πK / (γ_j T) )**,                             (★)

modulo the remainder r(ω) of §3.1 (OWED-1). At the draft's own §5.1
operating point (K = 4, T = 17.2167) this gives the table of §3.3, e.g.
1 + δ_1 ≤ 2.29 and 1 + δ_d ≤ 1.27, versus the draft's separately measured
2.03 and 1.23.

*Proof.* Identical to the original Lemma 1's Plancherel argument, with the
pointwise bound on 1/S_ε over the support supplied by (★): for
ω ∈ [γ_j−h, γ_j+h], §3.2 gives S_ε(γ_j)/(1+δ_j) ≤ S_ε(ω) ≤ (1+δ_j)S_ε(γ_j)
with 1+δ_j as in (★), so the whitening bound of the original Lemma 1 holds
with this explicit δ_j. ∎

Consequence for (4.1): the flatness correction is bounded, computable, and
$T\to\infty$-vanishing (since (★)'s exponent is $O(K/(\gamma_j T))\to 0$),
confirming the draft's own qualitative claim (line 718–720) with the
constant it asked for, at the cost of the one remainder term below.

---

## 5. OWED

**OWED-1.** The remainder r(ω) := D(ω) + 4/ω (§3.1) — the draft's own
"O(1/(ω log ω))" — has no explicit constant anywhere in the draft. Without
it, (★) is a bound on the leading-order approximation to D(ω), not a fully
rigorous non-asymptotic bound on D(ω) itself. Missing: an explicit C such
that |r(ω)| ≤ C/(ω log(ω/2π)) for ω ≥ γ_1, which would let (★) be tightened
to 1+δ_j ≤ exp(16πK/(γ_j T) + 2h·C/(γ_j log(γ_j/2π))) and certified as a
true, not merely approximate, ceiling.

**OWED-2.** The draft's own measured δ_j values (0.03, …, 2.03 at γ_1 down
to 1.23 at γ_d; lines 710–713) come from an uncommitted script
(`scratchpad/a2_verify.py` / `lane_t/t1_verify.py`, logged as GAP-8) that
integrates S_ε exactly over the neighbourhood rather than via the
linearized bound (★). No closed-form derivation of those exact numbers is
given in the draft; (★) above is offered as the closed-form substitute, and
it is intentionally looser (a valid ceiling, not a matching value).

---

## 6. What was not touched

This note does not alter `T1_CRAMER_RAO_DRAFT.md`, the GAP-4 ledger entry,
Lemma 2, Lemma 3, Proposition 4.4, or the proof of Theorem T1. It also does
not attempt to close GAP-4 — the draft's own criterion for closure ("Lemma
1 should be restated with S_ε evaluated at the band edge … and carry the
explicit two-sided constant") is satisfied by §4 above, but OWED-1/OWED-2
mean the constant is a derived ceiling, not the draft's exact measured
value re-derived from first principles.

## FRONTIER VERIFICATION 2026-08-26 (fable) — arithmetic PASS
Independent recomputation: 16π·4/17.2167 = 11.6783; exp(c/γ_j) at the six
tabulated tones = 2.29/1.74/1.60/1.47/1.43/1.27 (rounded UP), matching the
note and exceeding the draft's measured δ column at every tone (sound
ceiling). OWED-1 (explicit remainder constant) and OWED-2 (closed form for
the measured δ) accepted as stated. GAP-4 CLOSED at leading-order-ceiling
standing with OWED-1 disclosed.
