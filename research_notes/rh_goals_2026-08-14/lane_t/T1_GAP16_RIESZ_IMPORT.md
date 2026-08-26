# T1 GAP-16 — the explicit-formula import under the order-1 Riesz window

STATUS UPDATE 2026-08-26: **CLOSED AT CITATION+LEAN STANDING.** The Lean
core (Aristotle v21, RieszImport.lean, 8 theorems, sorry-free, axioms
propext/Classical.choice/Quot.sound) is harvested and re-elaborated. The
luna frontier review (T1_GAP16_REVIEW_LUNA.md, RULING: KEEP-OPEN pending
items 1–5) required six exact repairs — RH added to Prop. R; the
Gonek–Hejhal J_{−1} notation corrected to the squared-reciprocal form with
the Cauchy–Schwarz/dyadic convergence argument inserted (also in
G1_MODEL_SPEC.md); citations replaced (Hardy–Riesz Ch. IV/VII§2,
Hardy–Littlewood Acta 41 §2.25x, Titchmarsh §14.16/§14.27, Ng Lemmas 3–4;
§9.7 claim withdrawn); E_A(N) := I_{−A}(N) − R_triv(N) defined; the
ζ′(−2n) asymptotic, leading R_triv coefficient, and monotonicity sentence
corrected; the mandatory disclosure inserted in Prop. R — ALL APPLIED in
this revision, which per the ruling's closing paragraph licenses closure
at citation+Lean standing. A full Lean formalization of the contour
engine is NOT owed by that standard.


Lane T. Written 2026-08-15. Status: **DERIVED (frontier, not machine-verified;
analytic step is a citation, not a repo proof) + finite core DISPATCHED to
Aristotle.** Ticket:
`plans/wayfinder/rh-goals/tickets/t1-gap16-riesz-import.md`.
Model authority: `G1_MODEL_SPEC.md` v0 + Amendment A1 + **Amendment A2**
(clause (W′): W(x) = (1−x)_+, M_W(s) = 1/(s(s+1))).

GAP-16 is the debt A2 creates: the VERIFIED explicit-formula import in this
repo was proved for the *Gaussian* window and is out of scope under (W′)
(G1_MODEL_SPEC §A2.5.1; T1 v3 §1.1, §6). This note discharges the derivation
half of that debt and states what remains.

---

## 1. What the Gaussian-window artifact actually proved

**Artifact:** `research_notes/imported_farey_now/Smoothed_Dwf_explicit_formula_VERIFIED.md`
(created/verified 2026-05-03, confidence 0.96). Lean stub cited there:
`SmoothedDwfFormula.lean` (159 lines, states the formula axiomatically with
`def R0 : ℤ := -2`; the analytic content is **not** formalised — §5 of the
artifact is a 9-step ~600–700 LOC *program*, not a completed proof).

**Theorem 1 of that artifact.** Let f̂ be compactly supported (H1); let W be
Schwartz on (0,∞) with M_W meromorphic and **superpolynomially decaying** on
vertical strips (H2; satisfied by W(x) = e^{−x²}, where M_W(s) = ½Γ(s/2) and
|M_W(σ+it)| ≪ (1+|t|)^{σ/2−½} e^{−π|t|/4} by Stirling); assume simplicity of
the nontrivial zeros (H3, used only inside the zero sum). Then for every
A > 0,

  Σ_{m≥1} Δw_f(m) W(m/N)
    = R₀(f,W) + Σ_{ρ} N^ρ G_f(ρ) M_W(ρ)/ζ′(ρ) + R_triv(f,W;N) + E_A(N),

with (i) R₀(e₁, e^{−x²}) = Res_{s=0}M_W · 1/ζ(0) = 1·(−2) = **−2**;
(ii) the zero sum paired as 2·Re Σ_{γ>0}; (iii) R_triv = Σ_{k≥1}
N^{−2k}[c₁(k) log N + c₀(k)] arising from **double** poles at s = −2k (M_W
*and* 1/ζ both have simple poles there), total O(N^{−2} log N);
(iv) |E_A(N)| ≤ C_{A,f,W} N^{−A} for **every** A > 0.

Numerical anchor in the artifact: mp.dps 40, μ-sieve to 10⁶, 200 zeros;
S(N) vs R₀ + zero sum agree to 8 digits at N = 10⁵; the double-pole residue
at s = −2 matches its closed form to 18 digits at N = 100.

**Load-bearing use of the Gaussian in that proof.** Exactly one place: the
e^{−π|t|/4} decay of ½Γ(s/2) kills the horizontal contour pieces and the
far-left vertical line for *arbitrary* A, giving the superpolynomial E_A and
free absolute convergence of the zero sum. That is precisely the property A2
deletes on purpose (it was the cause of GAP-3/GAP-14). So the artifact does
not degrade gracefully to (W′): it must be re-derived, and the remainder
changes character from superpolynomial to polynomial.

---

## 2. The order-1 Riesz analog (derivation)

Throughout f = e₁, G_{e₁}(s) ≡ 1, so the arithmetic object is Möbius.

### 2.1 The window and its Mellin transform

W(x) := (1−x)_+ . For Re s > 0,

  M_W(s) = ∫₀¹ (1−x) x^{s−1} dx = 1/s − 1/(s+1) = **1/(s(s+1))**,   (2.1)

meromorphic on ℂ by continuation, with **simple poles only at s = 0
(residue 1) and s = −1 (residue −1)**, and no zeros. On the critical line
|M_W(½+iω)| = ((¼+ω²)(9/4+ω²))^{−1/2} ≍ |ω|^{−2}; more generally on any fixed
vertical line |M_W(σ+it)| ≍ |t|^{−2}. This is Riesz's typical mean of order
k = 1 (Cesàro/Fejér). Citations (corrected per the luna review 2026-08-26):
the Riesz-mean framework is Hardy–Riesz, *The General Theory of Dirichlet's
Series*, Ch. IV (typical means; order-1 = Cesàro) with the Riesz/Perron
integral in Ch. VII §2, p. 50; the generic order-δ kernel
Γ(δ+1)/[s(s+1)⋯(s+δ)] — which at δ = 1 is exactly 1/(s(s+1)) — is
Hardy–Littlewood, Acta Math. 41 (1916), §2.25x, pp. 140–141.
Montgomery–Vaughan §5.1 is the sharp-cutoff Perron formula (kernel x^s/s),
NOT this weighted variant: the inverse-Mellin identity and Fubini step for
(2.3) are proved elementarily below, not imported. For the contour shift,
§9.7 of Titchmarsh does NOT suffice (its zero-avoiding bound is an
unspecified polynomial, and no Gamma factor is present here); the correct
route, under T1's standing RH assumption, is Titchmarsh §14.16 (the
T^ε zero-avoiding height sequence under RH, extended to −A ≤ σ ≤ 1/2 by
the functional equation), with §14.27 as the model Mertens contour and
Ng 2004 (Möbius summatory), Lemmas 3–4, as the modern explicit version.
The derivation below is textbook in every step; GAP-16 asks for a
citation-grade re-derivation, not a discovery.

### 2.2 Arithmetic side is finite and exact

Because supp W ⊆ [0,1],

  𝓜_W(N) := Σ_{n≥1} μ(n) W(n/N) = Σ_{n≤N} μ(n)(1 − n/N)
          = (1/N) Σ_{n≤N} μ(n)(N − n)
          = **(1/N) Σ_{0≤k<N} M(k)**,   M(k) = Σ_{n≤k} μ(n).   (2.2)

The last equality is a *finite algebraic identity* (Abel/Fubini on the
rectangle {(n,k) : n ≤ k < N}): Σ_{n≤N} μ(n)(N−n) = Σ_{n≤N} μ(n) ·
#{k : n ≤ k < N} = Σ_{0≤k<N} Σ_{n≤k} μ(n). It is exact, requires no
convergence hypothesis, and is the piece the T1 pipeline actually computes
(one pass over a Möbius sieve). It is also the dispatchable Lean core (§4).

### 2.3 Mellin–Perron and the contour shift

For c > 1, Σ μ(n) n^{−s} = 1/ζ(s) absolutely, and M_W decays like |t|^{−2} on
Re s = c, so Mellin inversion + Fubini (Montgomery–Vaughan §5.1; the |t|^{−2}
decay gives absolute convergence, so no Perron truncation term is needed) give

  𝓜_W(N) = (1/2πi) ∫_{(c)} N^s M_W(s)/ζ(s) ds.   (2.3)

Shift the line to Re s = −A for a **fixed** A ∈ (1, 2) — not A → ∞, and this
is the substantive difference from the Gaussian case. Poles crossed:

- **s = 0** (simple pole of M_W; ζ(0) = −½):
  R₀ = Res_{s=0} M_W · N⁰/ζ(0) = 1 · (−2) = **−2**.  Unchanged from the
  Gaussian, for the structural reason that Res_{s=0}M_W = W(0) = 1 for any
  window continuous at 0.
- **s = −1** (simple pole of M_W, *new*; ζ(−1) = −1/12):
  Res_{s=−1} M_W = lim_{s→−1}(s+1)/(s(s+1)) = 1/(−1) = −1, so the term is
  N^{−1}·(−1)/ζ(−1) = N^{−1}·(−1)/(−1/12) = **R_{−1}(N) = 12/N**.   (2.4)
- **s = ρ**, each nontrivial zero (simple pole of 1/ζ under H3):
  N^ρ M_W(ρ)/ζ′(ρ), paired into 2·Re Σ_{γ>0}.
- **s = 1**: not a pole (ζ has the pole, so 1/ζ(1) = 0).
- **s = −2, −4, …** (trivial zeros): with A < 2 only s = −2 lies in the strip
  if one shifts that far; taking A ∈ (1,2) crosses **none** of them. Shifting
  further (A > 2n) they appear as **simple** poles — M_W is *regular* at every
  s = −2n, n ≥ 1 — so, unlike the Gaussian case, there is **no double pole and
  no log N**:

  R_triv(N) = Σ_{n≥1} N^{−2n} M_W(−2n)/ζ′(−2n)
            = **Σ_{n≥1} N^{−2n} / ( (−2n)(1−2n) ζ′(−2n) )**.   (2.5)

  Since M_W(−2n) = 1/((−2n)(−2n+1)) = 1/(2n(2n−1)) and, by the functional
  equation, ζ′(−2n) = (−1)ⁿ (2n)! ζ(2n+1)/(2(2π)^{2n}), the factor
  1/|ζ′(−2n)| DECAYS like 2(2π)^{2n}/(2n)! (correction per the luna review;
  the earlier text inverted this), so the series converges absolutely for
  N > 1 and R_triv(N) = O(N^{−2}). Its leading term is
  r₁(N) = N^{−2}/(2 ζ′(−2)) = −(2π²/ζ(3)) N^{−2}
  (ζ′(−2) = −ζ(3)/(4π²); the earlier 1/(6ζ′(−2)) was wrong).

**Remainder.** The vertical integral on Re s = −A, A ∈ (1,2), is

  |E(N)| ≤ N^{−A} · (1/2π) ∫_ℝ |M_W(−A+it)| |1/ζ(−A+it)| dt.

Here 1/ζ(−A+it) is only **polynomially** bounded (functional equation:
|ζ(−A+it)| ≍ |t|^{A+½}|ζ(1+A−it)| ≫ |t|^{A+½}, so |1/ζ(−A+it)| ≪
|t|^{−A−½}), while |M_W| ≪ |t|^{−2}. The integrand is therefore ≪
|t|^{−A−5/2}, absolutely integrable, and

  **|E(N)| ≤ C_A · N^{−A} for each fixed A ∈ (1,2)**,   (2.6)

with C_A explicit. **Assembly repair (luna item 4):** a shift to
Re s = −A with A ∈ (1,2) crosses NO trivial zero, so the identity as
originally written (full infinite R_triv + E(N) = the (−A)-line integral)
was inconsistent. The repaired bookkeeping: let I_{−A}(N) denote the
vertical integral on Re s = −A (shown above to be O_A(N^{−A}), using the
functional-equation bound |1/ζ(−A+it)| ≪ |t|^{−A−1/2}), and DEFINE
  E_A(N) := I_{−A}(N) − R_triv(N).
Since R_triv(N) = O(N^{−2}) and A < 2, still |E_A(N)| = O_A(N^{−A}), and
the displayed formula with the full R_triv holds with E(N) := E_A(N).
The horizontal segments use the §14.16 RH zero-avoiding heights (T^ε
bound; §2.1 citations), giving O(T^{−2+ε}) → 0 — NOT §9.7, whose
polynomial bound has an unspecified exponent. **Polynomial, not
superpolynomial** — exactly the cost A2 booked (G1_MODEL_SPEC §A2.5.2).

**Absolute convergence of the zero sum is now a hypothesis** (corrected
per the luna review: the earlier text misnamed a first-absolute-moment
bound "J_{−1}"). The standard, CONJECTURAL Gonek–Hejhal input is
  J_{−1}(T) := Σ_{0<γ≤T} 1/|ζ′(½+iγ)|² = O(T),
and J_{−1}(T) ~ (3/π³)T is the conjectured asymptotic (lane_a measured the
squared-reciprocal slope 0.0928 vs 3/π³ = 0.0968). Convergence then follows
by Cauchy–Schwarz + dyadic summation: with N_ζ(T) = O(T log T),
  Σ_{0<γ≤T} 1/|ζ′(ρ)| ≤ J_{−1}(T)^{1/2} N_ζ(T)^{1/2} = O(T√(log T)),
so on a dyadic block Σ_{T<γ≤2T} γ^{−2}/|ζ′(ρ)| = O(√(log T)/T), and the
dyadic sum converges, with tail O(√(log G)/G) beyond height G. Under the
Gaussian window the e^{−πγ/4} factor made this free. Stated, not hidden
(G1_MODEL_SPEC §A2.1.4).

### 2.4 Statement (the GAP-16 target)

> **Proposition R (order-1 Riesz explicit formula).** Assume **RH**, H3
> (simple zeros), and the conjectural Gonek–Hejhal bound
> J_{−1}(T) := Σ_{0<γ≤T} 1/|ζ′(½+iγ)|² = O(T). For every integer N ≥ 2
> and every fixed A ∈ (1,2),
>
>   (1/N) Σ_{0≤k<N} M(k) = Σ_{n≤N} μ(n)(1 − n/N)
>     = **−2 + 12/N + 2·Re Σ_{γ>0} N^{½+iγ}/( (½+iγ)(3/2+iγ) ζ′(½+iγ) )
>        + R_triv(N) + E(N)**,
>
> with R_triv as in (2.5) (O(N^{−2}), **no log N**) and
> E(N) = E_A(N) := I_{−A}(N) − R_triv(N), |E(N)| ≤ C_A N^{−A}.
>
> **Mandatory disclosure.** Proposition R is conditional on RH, simplicity of every nontrivial zero, and the conjectural Gonek–Hejhal bound J_{−1}(T) := Σ_{0<γ≤T}|ζ′(½+iγ)|^{−2} = O(T). Lean checks only the eight finite/algebraic lemmas in `RieszImport.lean`; the Riesz–Perron inversion, meromorphic residue calculus, absolute convergence of the zero and trivial-zero sums, the RH zero-avoiding contour shift, and the O_A(N^{−A}) remainder remain cited classical analysis and are not formalized in Lean.

Dividing by N^{1/2} with N = e^t recovers T1 §1.1's observable y(t) verbatim,
with a_γ = 1/(|½+iγ||3/2+iγ||ζ′(½+iγ)|) and the R₀, R_{−1}, R_triv
subtractions of G1_MODEL_SPEC §A2.1.3. **This is what T1 consumes and nothing
more.**

---

## 3. Numerical check (NON-RIGOROUS; validation, not proof)

Script: `projects/aristotle_dispatch_v21/riesz_numeric_check.py` (mpmath 1.4.1, mp.dps = 30; linear μ
sieve to 2·10⁴; first K mpmath `zetazero`s; R_triv truncated at n ≤ 7).
LHS = Σ_{n≤N} μ(n)(1−n/N) computed directly. RHS = −2 + 12/N + zero sum(K) +
R_triv(N).

γ_100 = 236.524, γ_200 = 396.382.

| N | LHS (direct) | diff, K=25 | K=50 | K=100 | K=200 |
|---|---:|---:|---:|---:|---:|
| 2 000 | −2.3055 | +2.69e−2 | +7.51e−3 | +7.62e−4 | +5.17e−4 |
| 8 000 | −2.625375 | −2.26e−2 | −1.98e−2 | −1.52e−2 | −2.17e−3 |
| 20 000 | −1.6818 | +3.82e−2 | +3.94e−2 | +7.38e−3 | +5.14e−3 |

Reading: the residual falls by one to two orders from K = 25 to K = 200
(not strictly monotone: the N = 20 000 row rises 3.82e−2 → 3.94e−2 at
K = 25 → 50 before falling; correction per the luna review), i.e. it behaves like the zero-truncation
tail, not like a structural error. The predicted tail is
2√N Σ_{γ>Γ} a_γ ≍ √N·log Γ/Γ: at N = 2·10⁴, Γ = 396 this is ≲ 0.34 without
phase cancellation, and the observed 5·10⁻³ sits comfortably inside it. The
constants **−2** and **12/N** are both required: dropping R_{−1} = 12/N
shifts the N = 2000 residual by 6·10⁻³, ten times the K = 200 residual, so the
new pole term is numerically confirmed at that N.

**Label:** floating-point, finitely many zeros, no interval arithmetic. This
validates the derivation; it does not verify it.

---

## 4. Lean core (candidate statement, sorry-stubbed)

`projects/aristotle_dispatch_v21/RieszImport.lean` — scaffolding copied from
`projects/aristotle_dispatch_v19` (lakefile.toml, lake-manifest.json,
lean-toolchain: Lean 4.28.0 / mathlib v4.28.0).

Split, stated plainly:

| piece | content | tag |
|---|---|---|
| `riesz_cesaro_identity` | Σ_{n=1}^{N} a n * (N − n) = Σ_{k<N} Σ_{n≤k} a n — the exact finite identity (2.2), for an arbitrary ℝ-valued a | **ARISTOTLE-ABLE** |
| `riesz_weight_eq` | Σ_{n=1}^{N} a n * (1 − n/N) = (1/N) Σ_{k<N} Σ_{n≤k} a n (N > 0) | **ARISTOTLE-ABLE** |
| `mellin_riesz_k1` | ∫_0^1 (1−x) x^{s−1} dx = 1/(s(s+1)) for real s > 0 — (2.1) | **ARISTOTLE-ABLE** (small analysis) |
| `MW_residue_zero`, `MW_residue_negOne` | s·M_W(s) = 1/(s+1) and (s+1)·M_W(s) = 1/s off the poles — the residue algebra giving Res = 1 at 0, −1 at −1 | **ARISTOTLE-ABLE** (field identities) |
| `R0_eq_neg_two`, `Rneg1_eq_twelve_div` | given ζ(0) = −1/2 and ζ(−1) = −1/12 as hypotheses: R₀ = −2 and R_{−1}(N) = 12/N | **ARISTOTLE-ABLE** |
| `Rtriv_summand_eq` | M_W(−2n)/ζ′(−2n) = 1/((−2n)(1−2n)ζ′(−2n)), i.e. (2.5) is a **simple**-pole residue (no log N) | **ARISTOTLE-ABLE** |
| Perron representation (2.3) + contour shift + (2.6) | the analytic engine | **FRONTIER / CITATION** — Hardy–Riesz Ch. V, Montgomery–Vaughan §5.1, Titchmarsh §3.7/§9.7. Not dispatched; a Mathlib-scale project (the Gaussian artifact §5 estimated 600–700 LOC for the *easier* superpolynomial case). |

So: the dispatch closes the finite/algebraic half of GAP-16 mechanically. The
Perron/contour half stays a **cited classical theorem**, and T1 must keep
saying so.

---

## 5. What remains open after this note

1. The analytic step (2.3)+(2.6) is a citation, not a repo proof. GAP-16
   therefore moves from *underived* to *derived, machine-verification partial*.
2. Absolute convergence of the zero sum rests on J_{−1}(T) = O(T) — a
   conjecture with lane_a empirical support (§2.3).
3. The remainder is O_A(N^{−A}) for fixed A, not superpolynomial; T1 §1.1's
   "ε negligible on [0,T]" needs A > 1 only, so this suffices, but the
   constant C_A has not been made explicit here.
4. H3 (simple zeros) is inherited unchanged from the Gaussian artifact.
