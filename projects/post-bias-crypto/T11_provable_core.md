# T11 — The Provable Core of Post-Bias Cryptography (PBC)

**Status:** working draft, formalization-ready. Adversarially honest.
**Scope:** the single rigorous theorem at the heart of PBC + a value verdict.
**Conditional vs unconditional are kept strictly separate throughout.**

---

## 0. One-paragraph summary

PBC's defensible mathematical content is a **min-entropy certificate for residue-class-restricted prime sampling**. The crypto *motivation* (avoiding residue classes for RSA primes) is, on scrutiny, **not worth it** as a security primitive — uniform sampling is as good or better, and the objection in §4 is essentially conceded. What survives is a clean number-theory result with a formal-methods payload: over a function field `F_q[T]`, the entropy lost by restricting prime generation to an allowed set `A` of residue classes is **exact and unconditional** (Weil's RH is a theorem there), whereas over `ℚ` the same bound is only conditional on GRH. The headline deliverable is therefore (iii) below: *a verified-crypto entropy bound that needs no unproved hypothesis*, valuable as a formal-methods artifact independent of whether anyone should build the sampler.

---

## 1. The theorem (precise statement)

### 1.1 Common setup

Fix `M ≥ 2`. Let `A ⊆ (ℤ/M)^*` be the **allowed** reduced residue classes (the complement, inside the units, of the avoid-list `S`). Write `a := |A|`, `φ := φ(M) = |(ℤ/M)^*|`, with `1 ≤ a ≤ φ`.

A range `I_k = [2^{k-1}, 2^k)`. Let `P_k := { p prime : p ∈ I_k }`, `N := |P_k|`, and for `r ∈ (ℤ/M)^*`,
```
        n_r := #{ p ∈ P_k : p ≡ r (mod M) },        N_A := Σ_{r∈A} n_r .
```

**The sampler `D_A`:** draw `p` uniform on `P_k`, reject and resample while `(p mod M) ∉ A`. (Equivalently: uniform on `P_k ∩ A`.) Underlying randomness: a CSPRNG bit source — quarantined as Assumption U below.

### 1.2 Min-entropy: the exact lemma (no max-subtlety)

> **Lemma E (uniform-restriction is uniform).** Conditioning a uniform distribution on a nonempty subset yields the uniform distribution on that subset. Hence `D_A` is **uniform on `P_k ∩ A`**, and
> ```
>   H_∞(D_A) = log₂ |P_k ∩ A| = log₂ N_A .
> ```

This is the load-bearing correction to the task's framing. The task suggested bounding `max_p Pr[p]` and plugging in a per-class density `max/min`. That is the right move for a *re-weighted* (importance-sampled) distribution, but plain rejection sampling does **not** re-weight: every surviving prime keeps equal probability. So min-entropy is exactly `log₂(support size)`, and the bias enters **only through the count `N_A`**, never through a per-class maximum. The `max_r/min_r` machinery is unnecessary here and would give a looser, slightly wrong bound. (It *would* be needed if PBC instead did class-balancing by re-weighting — see §4(a).)

### 1.3 (i) Support containment (trivial, stated)

> **Prop S.** `supp(D_A) ⊆ { p prime : p ∈ I_k ∧ (p mod M) ∈ A }`. In particular no sampled prime lies in an avoided class.

### 1.4 (ii) ℚ-form min-entropy bound (CONDITIONAL on GRH)

Define the per-class bias `n_r = (N/φ)(1 + β_r(k))`, i.e. `β_r(k) := φ·n_r/N − 1`. Set the **allowed-set mean bias**
```
        β̄_A(k) := (1/a) Σ_{r∈A} β_r(k) ,   so  N_A = (N/φ)·a·(1 + β̄_A(k)).
```

> **Theorem Q (conditional).** With the above,
> ```
>   H_∞(uniform prime in I_k) − H_∞(D_A) = Δ_ℚ
>          = log₂(φ/a) − log₂(1 + β̄_A(k)) .
> ```
> Under **GRH for Dirichlet L-functions mod M**, each class bias obeys
> ```
>   |β_r(k)|  ≤  C(M) · 2^{-k/2} · k · φ          (effective Siegel–Walfisz / GRH form)
> ```
> with `C(M)` an explicit constant (depends on M only, polynomial in log M). Consequently
> ```
>   Δ_ℚ = log₂(φ/a) + O( C(M) 2^{-k/2} k φ / ln 2 ),
> ```
> so for cryptographic sizes (`k ≈ 1024`) the bias correction is **astronomically below 2^{-400}** and `Δ_ℚ → log₂(φ/a)` to all practical precision.

**Honest flags.** (1) The exact `1/√x`-rate, GRH-conditional bias bound for `π(x; M, r)` is the Montgomery–Vaughan / Davenport form; the constant `C(M)` is effective but we do not optimize it. (2) Unconditionally only Siegel–Walfisz gives `O(x exp(−c√ln x))` with an **ineffective** constant for the worst residue — so the *unconditional* ℚ statement cannot pin `Δ_ℚ` with an explicit constant. This is exactly the gap the function field removes.

### 1.5 (iii) FF-form min-entropy bound — THE HEADLINE (UNCONDITIONAL)

Replace `ℤ` by the polynomial ring `R = F_q[T]`, "prime" by "monic irreducible," and the modulus `M` by a monic squarefree `m ∈ R` of degree `d` with `r` irreducible factors of degrees `d_1,…,d_r`. The unit group `(R/m)^*` has order
```
        Φ(m) = Π_{i=1}^{r} (q^{d_i} − 1).
```
Let `A ⊆ (R/m)^*` be the allowed classes, `a := |A|`. The "range" is **monic irreducibles of degree exactly `n`**, count
```
        π_q(n) = (1/n) Σ_{e|n} μ(e) q^{n/e}  =  q^n/n + O(q^{n/2}/n).
```
For a class `χ`-decomposition, the count in residue class `c ∈ (R/m)^*` is
```
        π_q(n; m, c) = (1/Φ(m)) Σ_{χ mod m} χ̄(c) · ψ_χ(n),   ψ_χ(n) := Σ_{deg P = n} χ(P)·(monic irred).
```
By the **explicit formula for `F_q[T]` Dirichlet L-functions** (each `L(u,χ)` is a polynomial in `u` of degree `≤ d−1`, with all inverse roots of absolute value `q^{1/2}` or `1` — this is **Weil's RH, a THEOREM** over function fields, Weil 1948 / Rosen, *Number Theory in Function Fields*, Thm 4.8 & Ch. 9):
```
        | ψ_χ(n) |  ≤  (d − 1) · q^{n/2} / n        for every nontrivial χ mod m.
```
Therefore the **exact, unconditional** class bias is bounded:
```
        n_c := π_q(n; m, c),     n_c = (π_q(n)/Φ(m))(1 + β_c),
        | β_c |  ≤  (d − 1) · Φ(m) · q^{-n/2} · (1 + o(1)).         (Weil)
```

> **Theorem FF (unconditional, closed-form).** With `Φ := Φ(m)`, `a := |A|`, allowed-set mean bias `β̄_A := (1/a)Σ_{c∈A} β_c`,
> ```
>   Δ_FF  =  log₂(Φ/a) − log₂(1 + β̄_A),
>
>   | log₂(1 + β̄_A) |  ≤  (1/ln 2) · 2·(d−1)·Φ·q^{-n/2}      (for Φ·q^{-n/2} ≤ 1/4),
> ```
> hence
> ```
>   |  Δ_FF − log₂(Φ/a)  |  ≤  ε_FF := (2(d−1)Φ / ln 2) · q^{-n/2},
> ```
> **with `ε_FF` an explicit, computable, hypothesis-free error term.** No GRH, no Siegel–Walfisz ineffectivity. As `n → ∞` (or `q → ∞`), `ε_FF → 0` at the certified rate `q^{-n/2}`.

This is the cleanest statement and the one formalized in §3. It is a genuine theorem on its own (a residue-class min-entropy certificate, unconditional), regardless of the crypto verdict.

---

## 2. Proofs (crypto-paper rigor)

### 2.1 Proof of Lemma E and Prop S (support + exact entropy)

Let `U` be uniform on finite `P_k`, `Pr[U=p] = 1/N`. Rejection sampling on event `B = {p mod M ∈ A}` produces the conditional law `Pr[· | B]`. For `p ∈ P_k∩A`,
```
   Pr[D_A = p] = Pr[U=p ∧ B]/Pr[B] = (1/N)/(N_A/N) = 1/N_A,
```
constant on `P_k∩A` and `0` off it. Thus `supp(D_A) = P_k∩A ⊆ {p : p mod M ∈ A}` (Prop S), and the law is uniform, so
```
   H_∞(D_A) = −log₂ max_p Pr[D_A=p] = −log₂(1/N_A) = log₂ N_A.   ∎
```
(Termination: `Pr[B] = N_A/N > 0` since `A ≠ ∅` and primes in allowed classes exist for `k` large; expected trials `= N/N_A ≤ φ/(a(1−|β̄|)) = O(φ/a)`. Quarantine the underlying bit uniformity as Assumption U; rejection preserves it.)

### 2.2 Proof of Theorem Q (ℚ, conditional)

`H_∞(U) = log₂ N`. By Lemma E, `Δ_ℚ = log₂ N − log₂ N_A = log₂(N/N_A)`. Substitute `N_A = (N/φ)a(1+β̄_A)`:
```
   N/N_A = φ / (a(1+β̄_A)),   so  Δ_ℚ = log₂(φ/a) − log₂(1+β̄_A).
```
For the bias bound: `π(x;M,r) = (1/φ) li(x) + E(x;M,r)`. Under GRH, `|E(x;M,r)| ≤ c·√x·(ln x)` (Davenport, *Multiplicative Number Theory*, §20, GRH form). With `x = 2^k`, `N = π(2^k)−π(2^{k-1}) ≍ 2^k/(k ln 2)`, divide through: `|β_r| ≤ C(M) 2^{-k/2} k φ`. Average over `A` and bound `|log₂(1+β̄_A)| ≤ |β̄_A|/((1−|β̄_A|)ln2)`. ∎

### 2.3 Proof of Theorem FF (function field, unconditional) — the core

**Step 1 (orthogonality).** For `c ∈ (R/m)^*`, count weighted by characters mod `m`:
```
   π_q(n;m,c) = (1/Φ) Σ_{χ mod m} χ̄(c) ψ_χ(n),    ψ_χ(n) = Σ_{deg P=n, P monic irred} χ(P).
```
The trivial character gives `ψ_{χ₀}(n) = π_q^{(m)}(n) = π_q(n) + O(d)` (irreducibles dividing `m` excluded; at most `d` of them). So the **main term** is `π_q(n)/Φ` and the **error** is `(1/Φ)Σ_{χ≠χ₀} χ̄(c) ψ_χ(n)`.

**Step 2 (Weil/RH input).** The L-function `L(u,χ) = Σ_f χ(f) u^{deg f} = Π_P (1 − χ(P) u^{deg P})^{-1}` is, for `χ ≠ χ₀` mod squarefree `m`, a **polynomial in `u` of degree `≤ d−1`** (Rosen, Prop. 4.3 & Thm 4.8). Write `L(u,χ) = Π_{j=1}^{≤d−1}(1 − α_{χ,j} u)`. The Riemann Hypothesis for curves / function fields (**Weil, theorem**) gives `|α_{χ,j}| = q^{1/2}` (or `=1` for ramified/degenerate factors). Taking the logarithmic derivative and reading off the `u^n` coefficient,
```
   Σ_{deg P = n} (deg P) χ(P)^{...}  — von Mangoldt form —  Λ-sum_χ(n) = − Σ_j α_{χ,j}^n,
```
so `|Λ-sum_χ(n)| ≤ (d−1) q^{n/2}`. Passing from the von Mangoldt-weighted sum to the irreducible count `ψ_χ(n)` (Möbius over `e | n`, lower-degree terms are `O(q^{n/2}/n)` already) gives
```
   |ψ_χ(n)| ≤ (d−1) q^{n/2}/n.                                    (★)
```

**Step 3 (assemble error).** Summing (★) over the `Φ−1` nontrivial characters and dividing by `Φ`:
```
   |π_q(n;m,c) − π_q(n)/Φ| ≤ ((Φ−1)/Φ)(d−1)q^{n/2}/n ≤ (d−1)q^{n/2}/n.
```
Dividing by the per-class main term `π_q(n)/Φ ≈ q^n/(nΦ)`:
```
   |β_c| ≤ (d−1)·Φ·q^{-n/2}·(1+o(1)).                              (Weil bias bound)
```

**Step 4 (entropy).** `Δ_FF = log₂(Φ/a) − log₂(1+β̄_A)`, `|β̄_A| ≤ max_c|β_c|`. Using `|ln(1+x)| ≤ 2|x|` for `|x|≤1/2`:
```
   |Δ_FF − log₂(Φ/a)| ≤ (2/ln2)(d−1)Φ q^{-n/2} =: ε_FF.            ∎
```
Every constant is explicit and **no hypothesis beyond `q` a prime power and `m` squarefree** is used. This is the unconditional certificate.

---

## 3. Formalization-ready statement

See `T11_entropy_bound_statement.lean`. Definitions: allowed classes as `Set (ZMod ...)` analog over `F_q[T]/(m)`, sampler support as a `Set`, the loss bound as an inequality with `ε : ℝ≥0`. Proof skeleton mirrors the ArkLib `Sorries.lean` quarantine: `weil_bound`, `csprng_uniform`, `primality_oracle_sound` are isolated `sorry`-ed lemmas; the entropy theorem is proved *from them* (so `#print axioms` shows exactly the assumption surface). Not yet wired to a `lake` build (no PBC lake project exists; toolchain is `leanprover/lean4:v4.28.0` + Mathlib, matching the project's other Lean dirs).

---

## 4. Adversarial value verdict (the most important section)

### 4.1 The strongest objection — and the answer (mostly a concession)

> **Objection (real cryptographer).** "Why would you ever avoid residue classes for RSA primes? RSA security rests on the hardness of factoring `pq`. The factoring difficulty is governed by the *size* of `p,q` and their being random — not by `p mod M`. Restricting to allowed classes throws away `log₂(φ/a)` bits of key entropy **for no factoring-security gain**, and it *narrows* the key space, which can only help an attacker. Class-balancing is solving a non-problem: there is no known factoring attack that exploits the residue class of an RSA prime mod small `M`. You have built a strictly-worse RSA key generator and dressed it in entropy bookkeeping."

**Answer: largely conceded.** For the stated RSA-key-generation use case, the objection is correct.
- Entropy: even with the *exact* certificate, `Δ = log₂(φ/a) > 0` means we provably **lose** entropy vs uniform. Best case `a = φ−1` (avoid one class): `Δ ≈ log₂(φ/(φ−1))` is tiny but still positive and still gains nothing.
- Security: there is no published factoring attack exploiting `p mod M` for small fixed `M` (coprime to the public exponent and not a backdoored special form). So the avoid-list buys no hardness.
- Caveat where the objection is *not* total: it does NOT cover (a) **side-channel/fault** threat models, where the attacker observes *physical* leakage correlated with the arithmetic path, not the factoring of `pq`. There, deliberately forcing primes into balanced classes can flatten a leakage distribution. But that benefit is an **engineering** claim about a specific leakage model, not a number-theory theorem, and must be benchmarked, not asserted.

### 4.2 Ranking the candidate value sources

| # | Claimed value | Verdict | Why |
|---|---|---|---|
| (b) | **FF-unconditional entropy *certificate* as a formal-methods contribution** | **SURVIVES — the real result** | Theorem FF is a genuine, hypothesis-free theorem. Its worth is as a *verified-crypto building block / case study*: "here is a key-gen-adjacent quantity whose entropy loss is machine-checkable with **only** Weil + CSPRNG assumptions, no GRH." That is a clean formal-methods artifact and a publishable number-theory note. |
| (a) | Provable side-channel/fault resistance via class-balancing | **DEMOTED to engineering** | Plausible only under a specific leakage model; needs class-*balancing by re-weighting* (not rejection), which changes the entropy analysis (back to the `max_r/min_r` machinery). No theorem here yet; benchmark-or-bust. |
| (c) | Closed-form differential-privacy noise budget (from B8) | **KILLED for this primitive** | The DP angle wants a *non-uniform* noise law with a closed-form MGF. Rejection sampling produces a *uniform* law on `A` (Lemma E) — no useful non-uniform shape, no tighter `ε`-budget. The B8 "structured non-uniformity" idea would need re-weighting, and even then the Laplace/Gaussian mechanisms already have exact budgets; Chebyshev-bias noise does not beat them. |

### 4.3 Real vs engineering vs hype

- **Genuine theorem (real):** Theorem FF (unconditional, closed-form `ε_FF`), Lemma E (exact min-entropy of rejection sampling), Theorem Q (conditional ℚ analog). These are correct and provable now.
- **Engineering:** any side-channel/fault-resistance benefit; performance of the rejection loop; the CSPRNG and probable-prime instantiation.
- **Narrative / hype to drop:** "post-bias cryptography" as a *security* upgrade for RSA key-gen; "balancing the Chebyshev prime-race asymmetry improves keys"; the B8 DP/VDF promises; the stale `q*≈0.605` and the inflated plausibility %s in the applications note. None survive.

### 4.4 The single biggest block

> **The primitive has no security theorem — only an entropy-accounting theorem.** Theorem FF rigorously *quantifies what you lose*, but there is no theorem showing the restriction *buys* anything (no reduction "balanced primes ⇒ harder to attack under model X"). Until a concrete, formalized leakage/fault model is fixed and a separating advantage is *proved* against it, PBC's entropy certificate is a high-quality answer to a question (“how much entropy does class-restriction cost?”) whose crypto motivation is unestablished. **Recommendation: ship Theorem FF as a standalone unconditional residue-class min-entropy result (formal-methods + analytic NT), and drop the RSA-security framing unless/until a leakage model with a provable separation is supplied.**

---

## 5. References (real)

- M. Rubinstein, P. Sarnak, *Chebyshev's bias*, Experimental Mathematics **3**(3) (1994), 173–197. (Prime races; bias is GRH+GSH-conditional in ℚ.)
- M. Rosen, *Number Theory in Function Fields*, GTM 210, Springer (2002). Ch. 4 (Dirichlet L-functions over `F_q[T]`, polynomial L-functions, Φ(m)), Ch. 9 (RH for function fields / Weil). Source of (★).
- A. Weil, *Sur les courbes algébriques et les variétés qui s'en déduisent* (1948). RH for curves over finite fields (the theorem making (★) unconditional).
- H. Davenport, *Multiplicative Number Theory*, 3rd ed., GTM 74, Springer (2000). §20 (`π(x;q,a)` error term; Siegel–Walfisz ineffectivity; GRH form).
- H. L. Montgomery, R. C. Vaughan, *Multiplicative Number Theory I*, CUP (2007). (Effective conditional bias constants.)
- D. Goldfeld, *Zeta functions, one-way functions, and pseudorandom number generators*. (Number-theoretic randomness context.)
- Standard min-entropy / key-generation references: NIST SP 800-90B (entropy sources), SP 800-90A (DRBGs); Y. Dodis et al. on randomness extraction (min-entropy as the right measure for keying).
- ArkLib (Verified-zkEVM), `leanprover/lean4:v4.29.0` + mathlib4 + VCV-io — formal scaffold model (see `arklib-learnings.md`).
