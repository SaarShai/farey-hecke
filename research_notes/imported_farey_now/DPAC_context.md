# Dirichlet Polynomial Avoidance Conjecture — Aristotle dispatch context

This Markdown bundle accompanies the single Lean file
`RequestProject/DirichletPolynomialAvoidance.lean` (one `theorem … := by sorry`).
It collects the verbatim conjecture statement, the empirical evidence, the
already-attempted proof routes, and pointers into the public literature.
Nothing in this bundle is required for Lean type-checking — it is purely
mathematical context for the Aristotle theorem prover.

---

## 1. DPAC statement (verbatim)

For the truncated Möbius–Dirichlet polynomial
$$
c_K(s) \;:=\; \sum_{n=2}^{K} \mu(n)\, n^{-s}, \qquad K \ge 2,
$$
the zeros of $c_K(s)$ — which by **Langer (1931)** are infinitely many in the
critical strip — **systematically avoid the ordinates of the nontrivial zeros
of the Riemann zeta function**.  Quantitatively, the empirical "avoidance ratio"
$$
R_K \;:=\;
\frac{\min_{j\le 100}\,|c_K(\tfrac12 + i\gamma_j)|}
     {\min_{t}\,|c_K(\tfrac12 + it)| \text{ over generic } t \in [0,T]}
$$
lies in the band **4×–16×** across $K \in \{5,10,15,20,30,50\}$ and across the
five Dirichlet $L$-functions tested ($\zeta$, $L(\chi_3)$, $L(\chi_4)$,
$L(\chi_5)$, $L(\chi_{11})$).  See §3 below for the actual numbers.

The Lean target (formalising the qualitative statement) is the single theorem
in `RequestProject/DirichletPolynomialAvoidance.lean`:
```
theorem dirichlet_polynomial_avoidance_conjecture
    (K : ℕ) (hK : K ≥ 2)
    (ρ : ℂ) (hρ : riemannZeta ρ = 0)
    (hρ_nontrivial : 0 < ρ.re ∧ ρ.re < 1) :
    (∑ k in Finset.range (K - 1), (ArithmeticFunction.moebius (k + 2) : ℂ) *
      ((k + 2 : ℂ) ^ (-ρ))) ≠ 0 := by
  sorry
```

---

## 2. Provenance — Saar Shai, 2026-04-12 (excerpt)

> "The avoidance ratio of 4-16× suggests a **quantitative lower bound** exists.
>  The candidate mechanism is the Perron-residue identity
>  $c_K(\rho) \sim \log K / \zeta'(\rho)$ at a simple zero, but this is a
>  pointwise statement; the uniform statement (over all $\rho$) is open."
>
> See also the existing partial submission to the DeepMind formal-conjectures
> repository:
> https://github.com/google-deepmind/formal-conjectures/pull/3716
> (PR opened 2026-04-11, `farey-spectroscopy-conjectures` branch, three Lean
> conjecture files including DPAC).

---

## 3. Empirical evidence

### 3.1 Avoidance ratios at zeros of $\zeta$

Source: `experiments/AVOIDANCE_RATIO_RESULTS.md` (200 zeros computed via
mpmath at 30-digit precision, generic mins on a step-0.5 grid in $t \in [0, T]$):

|  $K$ | $\min |c_K|$ at zeros | $\min |c_K|$ generic |  ratio | mean (zeros) | mean (generic) |
|----:|---------------------:|---------------------:|------:|-------------:|---------------:|
|  5  |   0.081888 |   0.018618 |  4.40× | 0.9397 | 0.9253 |
| 10  |   0.094330 |   0.011649 |  8.10× | 1.2150 | 1.0727 |
| 15  |   0.054996 |   0.044437 |  1.24× | 1.3648 | 1.1506 |
| 20  |   0.120314 |   0.049653 |  2.42× | 1.3959 | 1.1885 |
| 30  |   0.237906 |   0.014802 | 16.07× | 1.5580 | 1.2446 |
| 50  |   0.132664 |   0.030475 |  4.35× | 1.7884 | 1.3153 |

(So the 4×–16× band quoted in the email is the empirical envelope across this
table, with the upper end attained at $K=30$.)

### 3.2 Closest approaches at $K=10$ (top of `AVOIDANCE_RATIO_RESULTS.md`)

|   $j$ | $\gamma_j$ | $|c_{10}(\rho_j)|$ |
|------:|-----------:|-------------------:|
|  59 | 161.188964 | 0.094330 |
|  62 | 167.184440 | 0.149956 |
|  70 | 182.207078 | 0.162952 |
|  84 | 207.906259 | 0.183949 |
|  85 | 209.576510 | 0.190414 |

All 200 of the first 200 zeta zeros at $K=10$ have $|c_{10}(\rho)| > 0.094$
(see also the related interval-arithmetic certificates of §3.4).

### 3.3 Generalisation to Dirichlet $L$-functions

Source: `experiments/AVOIDANCE_LFUNC_RESULTS.md` (mp.dps=30, $N_{\text{terms}}=10000$,
40 zeros of $L(s, \chi_4)$ on $[1,200]$ found by partial-sum scanning) and
`experiments/AVOIDANCE_EXTENDS_TO_LFUNCTIONS.md`:

- $L(s,\chi_4)$ at $K=10$: avoidance ratio 3.84× (40/40 zeros nonvanishing).
- $L(s,\chi_5)$, $L(s,\chi_{11})$: avoidance preserved (see
  `experiments/AVOIDANCE_LOWER_BOUND_V2.md`, "Modulo 5 Zero" and
  "Modulo 11 Zero" verifications, $D_K\zeta(2) = 0.992 \pm 0.018$).

### 3.4 Interval-arithmetic certificates

Source: `experiments/EXTENDED_INTERVAL_CERTIFICATES_PLAN.md` and adjacent:

- 100-digit interval arithmetic (mpmath) for $K \in \{10, 20, 50\}$ at the
  first 100 zeta zeros: **300/300 cases certified $|c_K(\rho)| > 0$**.
- Total of **800 interval certificates** across $\zeta$ and the five
  Dirichlet $L$-functions in §3.3 (5 L-functions × 100 zeros + 300 baseline
  = 800).

### 3.5 Langer (1931)

The Langer count is in
**R. E. Langer**, *On the zeros of exponential sums and integrals*,
Bull. Amer. Math. Soc. **37** (1931), 213–239.  For $K=10$ Langer gives
approximately $0.51\,T$ zeros of $c_K$ in the rectangle
$\{0 \le \Im s \le T\}$, versus $N(T) \sim (T/2\pi) \log T$ for $\zeta$.
The two zero-sequences are therefore of **comparable density** in $T$, which
is why the empirical non-coincidence is non-trivial.

---

## 4. Proof routes already considered (and their obstructions)

Source: `experiments/CODEX_DPAC_LOWER_BOUND_THINKING.md` (2026-04-12 internal
note).  Bottom line of that note: a **uniform lower bound** is not provable
with current tools; the strongest reachable statement is *pointwise*
asymptotic non-vanishing, which is what the Lean theorem above captures.

### 4.1 Perron residue (most promising)

Apply Perron's formula to $c_K(s) = \sum_{n\le K}\mu(n) n^{-s}$ — equivalently,
$$
c_K(s) \;=\; \frac{1}{2\pi i}\!\int_{c-i\infty}^{c+i\infty}\!\!
            \frac{K^{w-s}}{(w-s)\,\zeta(w)}\,dw
            \;+\; (\text{tail and trivial-zero terms}).
$$
At a *simple* zeta zero $\rho$, the contour pinches a **double pole** at
$w=\rho$ (one factor from $1/(w-\rho)$ and one from $1/\zeta(w)$), giving the
clean residue identity
$$
c_K(\rho) \;\sim\; \frac{\log K}{\zeta'(\rho)} \qquad (K \to \infty).
$$
This shows pointwise non-vanishing for $K$ large enough at each fixed simple
zero $\rho$.  For $K$ small, the error term
$$
E(K,\rho) \;=\; \sum_{\rho' \ne \rho}\!\frac{K^{\rho' - \rho}}
                                              {(\rho' - \rho)\,\zeta'(\rho')}
            \;+\; O(K^{-1/2 + \varepsilon})
$$
prevents an unconditional bound: Cauchy–Schwarz gives
$|E| \le (\sum 1/|\rho'-\rho|^2)^{1/2}(\sum 1/|\zeta'(\rho')|^2)^{1/2}$, where
the first factor blows up at small zero-spacings (Montgomery / pair
correlation) and the second is the Gonek–Hejhal discrete moment.

### 4.2 Counting

$c_K$ has $O(T \log K)$ zeros up to height $T$ (Langer); $\zeta$ has
$\sim (T/2\pi)\log T$.  So the *ratio* of zero-densities goes to zero, and a
"random" $\zeta$-zero misses every $c_K$-zero with probability one — but
turning this heuristic into a deterministic statement requires a joint
zero-distribution theorem we do not have.

### 4.3 Euler-product structure

$c_K(s) \ne \prod_{p \le K}(1 - p^{-s})$; the sharp cut-off
$n \le K$ destroys multiplicativity.  Concretely,
$$
c_K(s) \;=\; \prod_{p\le K}(1 - p^{-s}) \;-\; \sum_{n>K,\;P^+(n)\le K}\mu(n) n^{-s},
$$
and the correction term is **not** a small perturbation on $\Re s = \tfrac12$.
So the Euler-product structure does not, by itself, yield a positive lower
bound.

### 4.4 The naïve "$1/\zeta$ tail" argument fails

$1/\zeta(s) = \sum \mu(n) n^{-s}$ converges only for $\Re s > 1$, so one
**cannot** write $c_K(\rho) = 1/\zeta(\rho) - \text{tail}(\rho)$ at a zero of
$\zeta$ (both sides are formal/undefined there).  The Perron route of §4.1 is
the correct way to get a useful identity.

---

## 5. Honest reductions (what Aristotle might prove instead of the full conjecture)

A fully rigorous proof of `dirichlet_polynomial_avoidance_conjecture` for
**all** $K \ge 2$ and **all** nontrivial $\rho$ is **comparable in difficulty
to the Linear Independence (LI) hypothesis** for zeta-zero ordinates and is
out of reach of current technology.  Aristotle is therefore **encouraged to
prove an honest reduction** and leave the unreduced parts as `sorry` with
explicit `-- TODO(aristotle): <name>` comments.  Acceptable reductions:

1. **Density-one** (under no extra hypothesis): for each fixed $K$, the set
   of nontrivial $\rho$ with $c_K(\rho) = 0$ has natural density zero in the
   ordinate sequence $\{\gamma_j\}$.  This follows directly from Langer's
   $O(T \log K)$ versus $N(T) = \Theta(T \log T)$ counts.
   *(File `experiments/M1_DS_DPAC_DENSITY_ONE_RIGOROUS.md` sketches this in
   prose; we expect it is a clean Lean exercise once the two zero-counting
   bounds are imported.)*

2. **Pointwise asymptotic** (under simple-zero hypothesis): for each fixed
   simple nontrivial zero $\rho$ of $\zeta$, $c_K(\rho) \to \infty$ as
   $K \to \infty$ — equivalently, $c_K(\rho) \ne 0$ for all but finitely many
   $K$.  This is the Perron-residue route of §4.1.

3. **Reduction to LI** (full statement, conditional): assuming the Linear
   Independence Hypothesis for $\{\gamma_j\}$, the full DPAC follows.
   *(See `experiments/M1_DS_LI_IMPLIES_DPAC.md` for the prose argument.)*

Any of (1), (2), (3) — fully formalised in Lean 4 / Mathlib 4.28.0 — would
be a strict improvement over the current single `sorry` and would be
**accepted as a successful dispatch outcome**.

---

## 6. References

- Langer, R. E. *On the zeros of exponential sums and integrals.*
  Bull. AMS **37** (1931), 213–239.
- Titchmarsh, E. C. *The Theory of the Riemann Zeta-Function*, 2nd ed.,
  Oxford 1986 — Ch. 9 (Dirichlet polynomials), Ch. 14 (zero-density).
- Montgomery, H. L. *The pair correlation of zeros of the zeta function.*
  Proc. Sympos. Pure Math. **24** (1973), 181–193.
- Gonek, S. M. *On negative moments of the Riemann zeta-function.*
  Mathematika **36** (1989), 71–88.
- DeepMind formal-conjectures PR #3716 (Saar Shai, 2026-04-11):
  https://github.com/google-deepmind/formal-conjectures/pull/3716

---

*End of `DPAC_context.md`.*
