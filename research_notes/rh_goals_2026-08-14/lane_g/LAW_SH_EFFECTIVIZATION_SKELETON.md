# LAW (SH) — Selberg–Hejhal Thm 7.11: what is reconstructible without the Hejhal text

**Date:** 2026-08-16. **Lane G.** Task: reconstruct the Selberg–Hejhal proof mechanism from
accessible sources and name exactly what must be made quantitative for an effective `Q₀`.
**Constraint honoured:** Hejhal, *The Selberg Trace Formula for PSL(2,R)*, Vol. 2, LNM 1001 (1983),
§7 / p. 579 was **not** consulted (blocked HITL library item). Everything below comes from open or
secondary sources, plus repo files. No git was run.

**Status convention (as in T2/U1/U2b):** `EXPLICIT` = constant is written down or immediately
computable. `EFFECTIVIZABLE` = the argument is quantitative in shape; constants exist but nobody
has written them. `UNKNOWN` = the source gives no constant and the proof is not accessible.
`RECONSTRUCTED` = **not** in any source read here; inferred by me and flagged as such.

---

## 0. Verdict up front

> **(a) The statement is now pinned exactly, from an open source.** Garbin–Jorgenson quote
> Hejhal's Thm 7.11 / Cor 7.12 verbatim. It is *not* "each non-arithmetic `G_q` has an off-line
> resonance". It is a **family / accumulation** statement: for every `t₀ ∈ R` and `0 < δ < 1`, the
> rectangle `[½, ½+δ] × [t₀−δ, t₀+δ]` contains **zeros** of `φ_N`, and `[½−δ, ½] × [t₀−δ, t₀+δ]`
> contains **poles**, *once `N` is sufficiently large*. "Sufficiently large" is the whole
> ineffectivity, and it is per-`(t₀, δ)`.
>
> **(b) No accessible source reveals Hejhal's proof.** Garbin–Jorgenson state the theorem, say it
> comes from Selberg's Göttingen lectures part 2, and note Hejhal promised a Vol. 3 that never
> appeared. They **quantify a neighbouring statement** (accumulation *rate* of the poles, their
> Thm 5.7) but do not reproduce Hejhal's argument. The mechanism in §2 below is therefore
> `RECONSTRUCTED`, not sourced.
>
> **(c) The repo's (T2′) route is already the effective form of Hejhal's mechanism.** Both run the
> same limit: elliptic degeneration `G_q → G_∞ = ⟨S, z↦z+2⟩ = Γ_θ` as the order-`q` elliptic point
> opens into a cusp, plus convergence of the scattering determinant `φ_q → φ_θ`, plus a
> zero/pole-transport step. `LAW_T2_DETERMINANT.md` §3 (Vitali+Hurwitz) is Hejhal's normal-families
> step with a *named* transport radius. So the effectivization does not need a new idea — it needs
> **one missing estimate**, §5.
>
> **(d) The single blocker (this route):** an **effective, `q`-explicit modulus of convergence on a
> fixed disc around `s_∞ = ρ₁/2`** — i.e. proved constants in `sup_{∂D}|Z_{G_q} − Z_{Γ_θ}| ≤ C q^{−2}`
> at `Re s ≈ ¼`, not just at `Re s > 1`. That is repo obligation **U5**, and it is gated by **U1**
> (the `q`-uniform order-2 growth bound). Call the gated form **U1-eff**.
>
> **(e) A genuine bypass exists** that never touches `Z_{G_q}` or U1 — the winding/positivity route
> (§3, route B). Its blocker is different and is *measurable with machinery the repo already has*.
> That is the recommended next lane (§7).

---

## 1. Sources found, and what each actually contains

| # | Source | Access | What it actually contains |
|---|---|---|---|
| S1 | Garbin–Jorgenson, *Spectral asymptotics on sequences of elliptically degenerating Riemann surfaces*, arXiv:1603.01494 = **L'Enseign. Math. 64 (2018) 161–206** | **open, full text read** | **The verbatim statement of Hejhal Thm 7.11 / Cor 7.12** (intro, = p.162 of the journal version); the identification of the limit object (`φ_N`, the 1×1 scattering determinant of the cusp at ∞); Thm 5.7 = the **quantitative accumulation rate** `N_{M_q,0}(T) = c₀(T)·log Q + O((log Q)^{3/4})`; Prop 5.2 giving `G_{M_q,0}(T) = (2C√(T−¼)/π)·log Q + O(1)`, `0 < C < 1` **unspecified**; Example 5.8 applying it to `G_N`. **Does not reproduce Hejhal's proof of 7.11.** |
| S2 | Garbin–Jorgenson, *Heat kernel asymptotics on sequences of elliptically degenerating Riemann surfaces*, arXiv:1603.01495 (Kodai Math. J. 43 (2020) 84–128) | open, not read in full | Companion paper; supplies the regularized heat-trace bounds that S1's Thm 5.1 consumes. This is where any effectivization of S1's `O(f(q))` would have to start. |
| S3 | Hejhal, *Regular b-groups, degenerating Riemann surfaces, and spectral theory*, Memoirs AMS 88 (1990) no. 437 | not accessed (paywalled) | Per S1, the degeneration machinery for Eisenstein series / scattering determinants. **Most likely home of a reusable convergence proof** — and it is *not* the blocked Vol. 2. Worth an access attempt. |
| S4 | Jorgenson–Lundelius / Huntley–Jorgenson–Lundelius (HJL 97) | open | S1 quotes their Lemma 5.3 (itself from He 83 p.160): the **positivity/lower bound** `−(φ′/φ)(½+ir) − Σ_k (1−s_k)/((s_k−½)²+r²) ≥ 2 log q_M > 0`. This is the load-bearing inequality of route B and it *is* explicit. |
| S5 | Fedosova, *Spectral and dynamical invariants of Hecke triangle groups via transfer operators*, arXiv:2509.17936 (2025) | open, abstract-level only | Current transfer-operator treatment of Hecke-triangle resonances / off-line zeros of `Z_w(s)`. Relevant as prior-art and possibly as a source of `q`-uniform operator bounds; **not** a source for Hejhal's mechanism. Flagged for a prior-art read. |
| S6 | Phillips–Sarnak; *Dissolving cusp forms: higher-order Fermi golden rules* (arXiv:1003.2820) | open | The *deformation* mechanism (embedded eigenvalue → resonance under a Teichmüller deformation, Fermi golden rule). **Different mechanism** from Thm 7.11: it needs a moving cusp form and a non-vanishing first-order term; `G_q` is a discrete family, not a deformation with a fixed cusp form. Do not conflate. |
| S7 | Hejhal, *Eigenvalues of the Laplacian for Hecke Triangle Groups*, Memoirs AMS 97 (1992) no. 469 | not accessed | Numerical; would supply data, not the mechanism. |

**Verbatim, S1 intro (the pin):** Hejhal proves "*a statement that he attributes to A. Selberg,
concerning the behavior of the zeros and poles of the scattering determinant*" for `G_N`, "*with
zeros accumulating to the right of the critical line and the poles to the left of it*"; the quoted
rectangle statement is as in §0(a). S1 adds that the result "*appears in the ending remarks of
Selberg's Göttingen lectures part 2*".

**Honest negative.** Google-Scholar-style citer sweeps for a *proof sketch* of 7.11 returned
nothing: the theorem is cited (S1, and the degeneration literature) but never re-proved. The
mechanism below is a reconstruction from what the statement + S1's Thm 5.7 + S4's Lemma force.

---

## 2. Route A — degeneration + transport (`RECONSTRUCTED`; the repo's route)

This is the shape Hejhal's proof almost certainly has, because S1 says Hejhal proved
"*the Eisenstein series and the scattering determinants converge through degeneration*".

- **A1.** As `q → ∞`, `λ_q = 2cos(π/q) ↑ 2`; the order-`q` cone point opens into a cusp and
  `G_q → G_∞ = ⟨S, z↦z+2⟩ = Γ_θ` (two cusps in the limit). Geometric, `EXPLICIT`
  (`2 − λ_q = π²/q² + O(q⁻⁴)`, repo `LAW_T2_DETERMINANT.md` §3.4).
- **A2.** `φ_q → φ_∞` locally uniformly on compacta of the strip, away from limit poles.
  `UNKNOWN` rate — this is the ineffectivity. (S1 asserts Hejhal has this; S3 is the likely proof.)
- **A3.** The limit `φ_∞ = φ_θ` has poles strictly left of `Re s = ½`, and — this is the point —
  **its poles are dense in height**, since `φ_θ` is built from `ζ` (repo `LAW_ANCHOR_T1_THETA.md`:
  `det Φ_θ` has an **order-2 pole at `s_∞ = ρ₁/2`**, `Re = ¼`; the full pole set is `{ρ/2}`).
- **A4.** **Transport.** Hurwitz/Rouché on a disc `D(s_∞, r)`: if
  `sup_{∂D} |φ_q − φ_θ| < min_{∂D} |φ_θ|` (resp. the `Z` version), the pole/zero count inside is the
  same for `q` and for the limit ⇒ `G_q` has a pole in `D(s_∞, r)`, hence `Re < ½ − (⅛ − r)`.
  `EFFECTIVIZABLE` **given A2 with a rate**. This is exactly repo obligation **U5**.
- **A5.** Hejhal's `[½−δ,½]×[t₀−δ,t₀+δ]` *at every `t₀`* then follows because the limit poles
  `{ρ/2}` are dense in height and can be pushed arbitrarily close to the line only by taking `δ`
  small and `N` large — the ineffectivity in `N` is inherited entirely from A2 and from how close
  to `Re = ½` one insists on landing.

**Consequence for us:** the repo route is strictly *stronger* than Hejhal's conclusion where it
works — it lands the pole at depth `≈ ¼` (deep), not merely inside a thin `δ`-strip — and it needs
only the **single** limit pole `s_∞ = ρ₁/2`, whose residue the repo already has numerically
(`−0.14943 − 0.39398i`).

---

## 3. Route B — winding / positivity (`RECONSTRUCTED`; the bypass)

This route uses only `φ_q` and the trace formula. It never needs `Z_{G_q}` growth, hence never
needs U1.

- **B1. Counting identity** (S1 eq. (5.2), from the Selberg trace formula, `EXPLICIT`):
  `N_{M,w}(T) = Σ_{λ_n ≤ T}(T−λ_n)^w − (1/4π)∫ (T−¼−r²)^w (φ′/φ)(½+ir) dr + Γ-term + Tr Φ(½)-term + area term.`
  The only `q`-divergent object here is the **winding term** `W_q(T) := −(1/4π)∫ (φ′_q/φ_q)(½+ir)dr`.
- **B2. Discrete part stays bounded.** `N_{M_q,w}(T) − G_{M_q,w}(T) → N_{M_∞,w}(T)` (S1 Thm 5.1,
  Cor 5.5); small eigenvalues converge. `EFFECTIVIZABLE` via S2's heat-kernel bounds; constants
  `UNKNOWN` as published.
- **B3. Divergence with rate** (S1 Prop 5.2(c), Thm 5.7):
  `G_{M_q,0}(T) = (2C√(T−¼)/π)·log Q + O(1)`, `Q = ∏ q_γ` (`= q` for `G_q`), `0 < C < 1`;
  `N_{M_q,0}(T) = c₀(T) log Q + O((log Q)^{3/4})`.
  So **the winding mass in a fixed window grows like `log q`.** Leading order `EXPLICIT up to C`;
  `C` `UNKNOWN` (it is a mean-value-theorem point), `O(1)` and `O((log Q)^{3/4})` `UNKNOWN`
  (S1 credits "calculations pointed out by Dennis Hejhal").
- **B4. Positivity** (S4 = HJL 97 Lemma 5.3, from He 83 p.160, `EXPLICIT`):
  `−(φ′/φ)(½+ir) − Σ_{k=1}^{N}(1−s_k)/((s_k−½)²+r²) ≥ 2 log q_M > 0.`
  Structurally, `−(φ′/φ)(½+ir)` is a sum of **Poisson kernels of the poles**:
  each pole `s_k = β_k + it_k`, `β_k < ½`, contributes `2(½−β_k)/((½−β_k)² + (r−t_k)²) ≥ 0`.
  (`RECONSTRUCTED` at the level of the Hadamard/inner-function factorization of `φ`; standard for a
  fixed group, `q`-uniform constants `UNKNOWN`.)
- **B5. Localization (the pigeonhole).** Fix the window `|r − t₀| ≤ δ`. Split the mass:
  (i) poles **inside** the `δ`-box; (ii) **shallow** poles (`½−β ≤ δ`) far in height — Poisson tail
  `≤ 2δ/(t−t₀)²`, summable against any polynomial pole-density; (iii) **deep** poles (`½−β ≥ δ`) —
  each contributes at most `2/δ` per unit height. To conclude that the `log q` mass of B3 sits in
  (i), one needs an upper bound on (ii)+(iii) that is `o(log q)`.
- **B6. Conclusion.** ≥ 1 pole in `[½−δ,½]×[t₀−δ,t₀+δ]` once `c₀(T)log q` exceeds that bound —
  and the threshold is **explicit** as soon as B3's constants and B5's upper bound are.

**Why this is attractive:** it reaches Hejhal's exact conclusion, it uses only quantities the repo
already computes (winding numbers!), and its blocker is a *counting upper bound*, historically much
easier than a growth theorem.

---

## 4. Constants table

| Step | Quantity | Status | Value / where |
|---|---|---|---|
| A1 | `2 − λ_q = π²/q² + O(q⁻⁴)` | `EXPLICIT` | repo T2 §3.4 |
| A2 | rate of `φ_q → φ_θ` (or `Z_{G_q} → Z_{Γ_θ}`) near `Re s = ¼` | **`UNKNOWN`** | Hejhal/S3; repo has it only **MEASURED** (`q^{−2}`, fits `−2.10/−2.15/−2.18`, T2 §4) and only for `Re s > 1` (U2a `PROVED`) |
| A3 | `s_∞ = ρ₁/2`, order-2 pole, residue `−0.14943 − 0.39398i` | `EXPLICIT` (numeric) | `LAW_ANCHOR_T1_THETA.md` (T1) |
| A3′ | `det Φ_θ` pole ⇒ `Z_{Γ_θ}` zero of order 2 | **`GAP`** | repo **U3**, still open — blocks A-route independently |
| A4 | `min_{∂D(s_∞,r)}|Z_{Γ_θ}|` | `EFFECTIVIZABLE` (closed form from (DET)+U3) | repo U5/U6 |
| A4 | `q`-uniform Hadamard bound `|Z_{G_q}(s)| ≤ A e^{B(1+|s|)²}` | **`GAP`** — the crux | repo **U1**; area `|F_q| = π(1−2/q) ≤ π` `PROVED`; Euler-product half needs U2b |
| A4-support | `sys(G_q) = 2 arccosh λ_q ≥ 2.1226` | `PROVED` | `LAW_U2B_CLOSURE.md` (a) |
| A4-support | `sup_{q≥5} Σ e^{−σℓ}/(1−e^{−ℓ}) ≤ 0.4861` for `σ ≥ 3.5`; convergence floor `σ₀ = 3.05` | `PROVED` | `LAW_U2B_CLOSURE.md` (b) |
| A4-support | `|Z| ≤ 1.6259` | `PROVED` | `LAW_U2B_CLOSURE.md` |
| B1 | trace-formula counting identity | `EXPLICIT` | S1 (5.2) |
| B3 | `c₀(T) = 2C√(T−¼)/π`, `0 < C < 1` | leading order `EXPLICIT`, **`C` `UNKNOWN`** | S1 Prop 5.2(c) |
| B3 | `O(1)` in `G_{M_q,0}`, `O((log Q)^{3/4})` in Thm 5.7 | **`UNKNOWN`** | S1 Thm 5.7 (unpublished Hejhal calculations) |
| B4 | `−(φ′/φ)(½+ir) − Σ_k ⋯ ≥ 2 log q_{M_q} > 0` | `EXPLICIT` | S4 Lemma 5.3 / He 83 p.160 |
| B5 | `#{poles: Re s ≤ ½−δ, |Im s − t₀| ≤ 1}`, `q`-uniform upper bound | **`UNKNOWN`** — route-B blocker | nothing in repo or sources |
| B5 | shallow-pole height-density (Weyl upper bound, `q`-uniform) | `EFFECTIVIZABLE` | area `≤ π` gives `N_q(T)+M_q(T) ~ (|F_q|/4π)T²`, `PROVED` shape (T2 U1 row) |

---

## 5. The single named blocker

> ### **U1-eff — a `q`-explicit sup-norm comparison at `Re s ≈ ¼`.**
> Everything else on route A is in hand or cheap. What is missing is a **proved** bound
> `sup_{s ∈ ∂D(s_∞, r)} |Z_{G_q}(s) − Z_{Γ_θ}(s)| ≤ C q^{−2}` (any explicit decaying `C q^{−α}`
> suffices) **with `C` written down**. The repo has this comparison `PROVED` only on `Re s > 1`
> (U2a, word-level) and `MEASURED` at `q^{−2}` elsewhere. Carrying `Re s > 1` down to `Re s = ¼`
> is precisely what the `q`-uniform order-2 growth bound **U1** is for (Hadamard + Phragmén–Lindelöf
> in the strip). **U1 with explicit `A, B` ⇒ explicit `Q₀` via U5.** Nothing else on route A is
> `UNKNOWN` except U3, which is textbook-shaped.

This is the exact analogue of the old crux, moved: the frozen U1-φ (Eisenstein `φ_q` decay) route
demanded a *decay exponent* `> 2σ₀ − 1 > 5.1`; U1-eff demands only a *growth* bound plus a decay
rate `q^{−α}` for **some** `α > 0` on a **single fixed disc**. That is a strictly weaker ask, and
the measured `q^{−2}` says the truth is comfortably inside it.

**Route B's blocker, for the record:** a `q`-uniform upper bound on the **deep**-resonance count
`#{s : Re s ≤ ½−δ, |Im s − t₀| ≤ 1}`, growing `o(log q)`. Unknown in the literature read here, but
— unlike U1-eff — **directly measurable** with the repo's existing argument-principle winding
certificates.

---

## 6. What this note does **not** claim

- It does **not** claim to know Hejhal's proof. §2 and §3 are labelled `RECONSTRUCTED`.
- It does **not** claim Thm 7.11 implies "every non-arithmetic `G_q` has an off-line resonance".
  For a *fixed* cofinite group every pole of `φ` already lies in `Re s < ½` (unitarity on the line
  + `φ(s)φ(1−s) = 1`); the content of 7.11 is **localization and accumulation in `N`**, not
  existence. **The parent's framing should be checked against this** — the flagship theorem's
  novelty must rest on *depth* (`Re ≈ ¼`) and on *certification for a named `q`*, not on the bare
  existence of an off-line pole.
- It does **not** claim S1's Thm 5.7 constants are recoverable without S2 and the unpublished
  Hejhal calculations it cites.

---

## 7. Recommended next lane

**Ranked, cheapest first.**

1. **B-measure (recommended, ~1 lane, agent-able).** Use the existing Aletheia certify engine
   (argument-principle winding certificates, already validated for `q = 3, 5, 7`) to **measure the
   deep-pole count** `#{Re s ≤ ½−δ, |Im s − t₀| ≤ 1}` for `q = 5…21`, `δ ∈ {0.05, 0.1, 0.25}`, at a
   few `t₀`, alongside the winding mass `W_q`. Two outcomes, both valuable: (i) deep count is
   bounded/slow ⇒ **route B closes with an explicit `Q₀` and U1 is bypassed entirely**;
   (ii) it grows `≳ log q` ⇒ route B is dead, publish the negative, and all funding goes to U1-eff.
   This is the highest information-per-unit-cost item on the board.
2. **U3 (Aristotle-able finite piece).** Scattering-pole ⇒ Selberg-zero transport for `Γ_θ` via the
   functional equation `Z(1−s) = Z(s)Ψ(s)φ(s)`. Blocks route A completely, is textbook-shaped, and
   is already flagged "run first" in `LAW_T2_DETERMINANT.md` §6. Unchanged recommendation.
3. **S3 access attempt.** Hejhal, Memoirs AMS 88 (1990) no. 437 is a *different* item from the
   blocked Vol. 2 and is the likely home of a reusable `φ_q → φ_∞` convergence proof. If its
   argument is quantitative, A2 may fall out with modest work. Low cost, worth one HITL request.
4. **U1-eff itself.** The real work; frontier + Aristotle in pieces, per T2 §6. Do not start before
   1–3 report.

**Not recommended:** re-reading Phillips–Sarnak / Fermi-golden-rule material for this purpose (S6).
It is a deformation mechanism with a fixed cusp form and does not apply to the discrete `G_q` family.

---

**Sources (URLs):** arXiv:1603.01494 (Garbin–Jorgenson, L'Enseign. Math. 64 (2018) 161–206);
arXiv:1603.01495; arXiv:2509.17936 (Fedosova 2025); arXiv:1003.2820 (dissolving cusp forms);
AMS Memoirs 88/437 and 97/469 (Hejhal, not accessed).
