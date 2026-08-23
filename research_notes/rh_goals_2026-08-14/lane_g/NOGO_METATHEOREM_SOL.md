# NOGO — a metatheorem: what the generic scattering axioms cannot decide

**Date:** 2026-08-23 (file clock `2026-08-23T05:26Z`; the MAP entry that
commissioned this lane is stamped `2026-08-23 07:15Z` — the MAP stamp is the
authority for lane provenance, the file clock for this artifact).
**Lane:** G / NOGO. **Steps:** NOGO-1, NOGO-2, NOGO-3.
**Status: UNREFEREED. No cold referee has read this note.** Section 3's
Metatheorem is derived here; Sections 5–6 mark every item that is
`OPEN`, `CONDITIONAL`, or `CONJECTURAL`.
**Append-only. Nothing outside this file was written. No commit, no push.**

**LEDGER RULE in force.** Nothing below is stated more strongly than its
most-caveated source. In particular the whole note inherits the residual
dependency of the LAW: the complex-analytic engine `[Sel90, Lemmas 1, 2]`
has **not been read** by the author of the LAW, by either of its two
referees, or by the author of this note
(`LAW_SECOND_AUDIT_REFEREE.md:46`). Every occurrence of "PROVED" below
therefore means *proved modulo that one unread citation*, which is the
same standing the promoted LAW carries.

---

## 0. Verdict up front, including one correction to the brief

> ### **The commissioned statement of on-line rigidity is the wrong statement, and the correction changes the shape of the result.**
>
> The brief proposed
> `P = "all zeros of φ in the right half-strip lie on Re s = 1/2"`, described
> as "for q=3 equivalent to RH for ζ". **That is false.** For `q = 3`,
> `φ_3(s) = Λ(2s−1)/Λ(2s)`, whose zeros in `Re s > 1/2` sit at
> `s = (1+ρ)/2` for `ρ` a nontrivial zero of `ζ`. Under RH they lie on
> `Re s = 3/4`. So `P` is not equivalent to RH; **`P` is refuted by RH**,
> and is in fact unconditionally false (§3.2, §4). The RH-equivalent
> statement in this family is
> `P_line(3/4) = "every nonreal zero of φ in 1/2 < Re s < 1 has Re s = 3/4"`
> (Proposition 4.1: `P_line(3/4) ⟺ RH`, exactly, unconditionally).
>
> ### With that correction, the honest picture is a three-line trichotomy.
>
> | statement | relation to the axiom set `A` | status |
> |---|---|---|
> | `P_naive` — no zeros at all in `Re s > 1/2` (the brief's `P`) | **`A ⊨ ¬P_naive`** — `A` *entails the negation* | **PROVED** (§3.3), modulo Sel90 |
> | `¬P_line(3/4)` — the RH-analogue fails | **`A ⊭ ¬P_line`** — `A` cannot refute on-line rigidity | **PROVED CONDITIONAL ON RH** (§3.4); witness `φ_3` |
> | `P_line(3/4)` — the RH-analogue holds | **`A ⊭ P_line`?** | **OPEN** (§5.1) — no countermodel is in the bank |
>
> ### The slogan the lane was asked to make rigorous survives only in its first row.
> "Proof strategies for on-line rigidity that use only the generic analytic
> machinery are doomed" is **a theorem** for the naive reading of on-line
> rigidity, and it is doomed in the strongest possible sense: `A` proves the
> opposite. For the RH-analogue reading it is **not yet a theorem**; §5.1
> writes down exactly the witness that would make it one.
>
> ### `A` is arithmeticity-blind, and that is the transferable content.
> Every axiom in `A` is satisfied by the arithmetic `q ∈ {3,4,6}` and by
> every non-arithmetic `q` with identical receipts (§2). No consequence of
> `A` can separate them. This is the formal version of the second audit's
> warning that the LAW carries **zero** arithmeticity information
> (`LAW_SECOND_AUDIT_REFEREE.md:27,59`).

---

## 1. NOGO-1 — the axiom set `A`

### 1.0 Scope check on `LAW_MINIMAL_HYPOTHESES.md` (as the brief instructed)

`LAW_MINIMAL_HYPOTHESES.md` is **not** the right source and was not used as
one. Its subject is the Vitali/Hurwitz *tail* argument on Selberg zeta
functions — `Z_{G_q} → Z_{Γ_θ}`, the domain `Ω̃`, the corridor, `U1-min`
(`LAW_MINIMAL_HYPOTHESES.md:1-40`). That is the deformation/large-`q` route,
a different object (`Z`, not `φ`) and a different theorem. Confirmed by
`SCAT_EVAL_Q_SOL.md`, which states that "the **large-q tail route** does not
logically need `φ_q` at all."

`A` is therefore extracted directly from the promoted LAW proof chain:
`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md` §§2–5 plus its 2026-08-19
promotion block, cross-read against the per-attack hypothesis inventory in
`LAW_SECOND_AUDIT_REFEREE.md` and against the hypothesis quarantine
`H3`/`H4`/`H5` in `projects/aristotle_dispatch_v33/LawSkeletonI.lean`.

### 1.1 The structures

A **Hecke-type scattering pair** is a pair `M = (φ, 𝒟)` where `φ` is
meromorphic on `ℂ` and `𝒟 = (d(n), g_n)_{n≥1}` is its Dirichlet data. The
axioms below are conditions on `M`. Write `𝔐(A)` for the class of all pairs
satisfying every axiom. **Nothing in the language of `A` mentions `q`, a
group, a surface, arithmeticity, or `ζ`.** That omission is the entire
point: `A` is exactly the "generic analytic machinery" of the slogan.

### 1.2 The axioms

**A0 (SCALAR, ONE CHANNEL, `κ = 1`).** `φ` is a `1×1` determinant: the
degree of singularity is `1`, so `det Φ = Φ` and the archimedean factor
below carries exponent `κ = 1`.

**A1 (MEROMORPHY AND RIGHT-HALF-PLANE REGULARITY).** `φ` is meromorphic on
`ℂ` of order at most `2`, and holomorphic in `Re s > 1/2` apart from
finitely many poles.

**A2 (FUNCTIONAL EQUATION).** `φ(s) φ(1−s) = 1`.

**A3 (REALITY).** `φ(s̄) = conj φ(s)`; equivalently `d(n) ∈ ℝ` for all `n`.

**A4 (GENERALIZED DIRICHLET SERIES WITH THE HEJHAL ARCHIMEDEAN FACTOR).**
For `Re s > 1`,
```
φ(s) = √π · Γ(s − 1/2)/Γ(s) · Σ_{n≥1} d(n) g_n^{−2s},
0 < g_1 < g_2 < … → ∞  (discrete),  d(1) ≠ 0,
```
the series absolutely convergent in `Re s > 1`. **A4⁺** (used only where
flagged): `d(n) > 0`, so the series sits inside Selberg's original
positive-coefficient hypothesis class.

Consequence used downstream — the **normalization** `(N)`/`(NF)`: with
`λ_n = (g_n/g_1)²`, `a_n = d(n)/d(1)`, `L*(s) = 1 + Σ_{n≥2} a_n λ_n^{−s}`,
```
φ(s) = √π Γ(s−1/2)/Γ(s) · d(1) g_1^{−2s} · L*(s),
L*(s) = 1 + O(e^{−c·Re s})  as Re s → +∞.
```
The prefactors are zero-free and pole-free in `Re s > 1/2`, so `φ` and `L*`
have the same divisor there.

**A5 (RIGHT-DIVISOR FINITENESS AND STRIP CONFINEMENT).** In `Re s > 1/2`:
finitely many *real* zeros `ρ_i > 1/2` (with multiplicity); finitely many
poles `σ_j ∈ (1/2, 1]`; and every zero lies in a vertical strip, i.e.
`sup{Re ρ : φ(ρ) = 0, Re ρ > 1/2} < ∞`.

**A6 (VERTICAL POLYNOMIAL BOUND).** For every `ε > 0` there is `C(ε) < ∞`
with `|φ(σ + it)| ≤ C(ε)` for `1/2 ≤ σ ≤ 3/2` and `|t| ≥ ε`.

**A7 (CRITICAL-LINE MODULUS).** `|φ(1/2 + it)| = 1` for real `t`;
equivalently, in the `(N)` normalization,
```
|L*(1/2 + it)| = a · |Γ(1/2+it)/Γ(it)|,   a = g_1 / (√π |d(1)|).
```
(`A7` follows from `A2 + A3`; it is listed separately because the LAW
consumes the **exact modulus**, identity `(G)`, not merely unitarity.)

### 1.3 Why this list and no more

Three independent cross-checks that `A` is what the LAW actually eats.

1. **Kelmer's hypothesis list.** The only object the LAW imports from
   Kelmer is Prop. 4.4's hypothesis list — `(4.13)` right-edge decay,
   `(4.14)` vertical growth, `(4.15)` critical-line modulus — which at
   `d = 2, κ = 1` are exactly `A4`'s consequence, `A6`, and `A7`
   (`LAW_SECOND_AUDIT_REFEREE.md:18`). Kelmer's *global* torsion-free
   standing hypothesis is **not** imported: the LAW supplies `(4.14)` from
   Hejhal 7.7 instead, "strictly more conservative, and … exactly the step
   where torsion-freeness could have entered. The substitution is
   legitimate" (same line).
2. **The Lean quarantine.** `LawSkeletonI.lean` isolates the analytic
   imports as three named hypotheses: `H3 = hgrowth` (the Jensen rectangle
   composed with the critical-line integral — i.e. `A1,A4,A5,A6,A7` fed
   through Sel90), `H4 = hreal_finite` (`A5`), `H5 = hpole` (`A2`).
   `LawSkeletonI.lean:31-32,160-162,182-183,210-213`. Nothing else about
   `φ` appears in the formalization.
3. **The LAW's own §6 inventory** lists precisely: continuation, functional
   equation, generalized Dirichlet series, finite real right exceptions
   (`A1,A2,A4,A5`), the strip bound (`A6`), one cusp (`A0`), and the
   Jensen/Selberg template (not a property of `φ`).
   `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:338-347`.

**Not in `A`, deliberately:** any Euler product; any multiplicativity or
Ramanujan bound; any group, surface, or spectral input beyond `A0`; any
`q`-uniformity; any effective first height; any arithmeticity. `A` contains
**only** properties shared by the arithmetic and non-arithmetic scattering
determinants — which is what makes §3 a no-go and not a theorem about
non-arithmetic groups.

---

## 2. NOGO-2 — per-axiom receipts, both sides

Notation for the arithmetic side: `q = 3`, `G_3 = PSL(2,ℤ)`,
`Λ(w) = π^{−w/2} Γ(w/2) ζ(w)`, and
```
φ_3(s) = √π · Γ(s−1/2) ζ(2s−1) / (Γ(s) ζ(2s)) = Λ(2s−1)/Λ(2s),
L*_3(s) = ζ(2s−1)/ζ(2s).
```
The identity `√π Γ(s−1/2)ζ(2s−1)/(Γ(s)ζ(2s)) = Λ(2s−1)/Λ(2s)` is one line
of algebra: `π^{−(2s−1)/2}/π^{−s} = π^{1/2}` and `Γ((2s−1)/2) = Γ(s−1/2)`,
`Γ(2s/2) = Γ(s)`.

**Sourcing of `φ_3` itself.** The closed form is classical (Kubota; Iwaniec,
*Spectral Methods of Automorphic Forms*, 2nd ed., §3.4 — **NOT READ by this
author**, cited as standard). It is receipted *inside our own bank*, twice
and independently: Kelmer Remark 0.2 as quoted in
`LAW_SECOND_AUDIT_REFEREE.md:26` — *"for Γ = SL₂(ℤ) the scattering
determinant … poles are located at the zeroes of ζ(1−2s)"* — and the same
line's own instantiation *"`L*₃ = ζ(2s−1)/ζ(2s)`, zeros at `s = (1+ρ_ζ)/2`
with `β = 3/4`, poles at `Re = 1/4`"*, numerically verified there against
the `A7` modulus **to `1e−31`** at `t = 0.5, 1, 3, 7.5, 14.13, 50, 137`, and
against the counting law `(C)` to residual `0.34–0.73` for `T = 100…1600`.

| axiom | arithmetic `q = 3` — receipt | non-arithmetic `q ∉ {3,4,6}` — receipt | verdict |
|---|---|---|---|
| **A0** scalar, one cusp, `κ=1` | `G_3` has one cusp; trivial character ⇒ degree of singularity `k = 1`. Same source as the right column (`q = 3` is `N = 3` in Hejhal §7 and MMS). | MMS p. 29 verbatim *"all the Hecke triangle groups have only one cusp"*; `k = c = 1`, `Φ` is `1×1`. `LAW_SECOND_AUDIT_REFEREE.md:22`; `LAW_..._SOL.md:56,96-99` | **PASS** both |
| **A1** meromorphy, order ≤2, finite right poles | `Λ` entire of order 1 except simple poles at `w ∈ {0,1}`; `s ↦ Λ(2s−1)/Λ(2s)` is meromorphic of order 1 in `s`, hence order ≤ 2. Poles in `Re s > 1/2`: `Λ(2s)=0 ⇒ Re s = β/2 < 1/2` (none); `Λ(2s−1)` pole at `s = 1`. So exactly one pole, `σ_1 = 1` — the value the audit uses. `LAW_SECOND_AUDIT_REFEREE.md:20` | FJS §2.4 citing Venkov Thm 3.5 p. 59: *"meromorphic of order at most two … holomorphic for Re(s) > 1/2, except for a finite number of poles"*. `LAW_..._SOL.md:104-113,190-192`; FJS printed in **orbifold** generality with elliptic classes present, `LAW_SECOND_AUDIT_REFEREE.md:16` | **PASS** both |
| **A2** `φ(s)φ(1−s)=1` | Immediate from `Λ(w) = Λ(1−w)`: `φ_3(1−s) = Λ(1−2s)/Λ(2−2s) = Λ(2s)/Λ(2s−1) = 1/φ_3(s)`. | FJS §2.4 `(F)`. `LAW_..._SOL.md:108,192`; `LAW_SECOND_AUDIT_REFEREE.md:16` | **PASS** both |
| **A3** reality | `ζ`, `Γ`, `π^{−w/2}` are real-analytic ⇒ `Λ(w̄) = conj Λ(w)` ⇒ `φ_3(s̄) = conj φ_3(s)`. | FJS footnote 1: `d(n) ∈ ℝ`. `LAW_..._SOL.md:132,194`; `LAW_SECOND_AUDIT_REFEREE.md:16,24` | **PASS** both |
| **A4** Dirichlet series, Hejhal archimedean factor, discrete `g_n`, `d(1)≠0` | `q = 3` is `N = 3` in Hejhal (7.5), which is printed for all finite `N ≥ 3`; the resulting series is `Σ d(n) g_n^{−2s} = ζ(2s−1)/ζ(2s)` with `g_n = n` (integer `c`-values for `PSL(2,ℤ)`), `d(1) = 1 ≠ 0`, discrete. Consistency check: `L*_3 = ζ(2s−1)/ζ(2s) = 1 + O(2^{−Re s})` — the `(N)` right-edge form. | Hejhal (7.5), PDF p. 569 image reproduced by the cold referee: `φ_N(s) = √π Γ(s−½)/Γ(s) Σ_{W∞∈[S]\𝒢_N/[S], c≠0} |c|^{−2s}, Re s > 1`. `LAW_SECOND_AUDIT_REFEREE.md:13`; `LAW_..._SOL.md:117-131`. **Discreteness was the sharpest attack and it failed**: `ℤ[λ_q]` is dense in `ℝ` for `q = 5,7,…`, yet exact `ℤ[λ]` enumeration for `G_5` (1700 elements) gives only **7** distinct `|c|` in `(0,6)`, min gap `0.382`, `g_1 = 1`; float sweep `q = 3,4,5,6,7,8,9,11,17` gives 6–8 values below 6, min gap `0.088`–`1.0`, `g_1 = 1` throughout. `LAW_SECOND_AUDIT_REFEREE.md:23` | **PASS** both. See §5.3 for the one caveat. |
| **A4⁺** positive coefficients | `d(n) = ` number of `c`-classes with `\|c\| = n`, a positive integer. | *"at κ=1 the Hejhal (7.5) coefficients are positive integers, inside Selberg's original positive-coefficient hypothesis class."* `LAW_..._SOL.md:459-460`; `LAW_SECOND_AUDIT_REFEREE.md:32`. Also Hejhal Lemma 7.3, `0 ≤ φ_N(1+ε) ≤ C₁(ε)` (`LAW_HEJHAL_S7_EXTRACT.md`, `N ≥ 4`). | **PASS** both |
| **A5** finite real right zeros, finite right poles, strip confinement | Zeros of `φ_3` in `Re s > 1/2` are exactly `s = (1+ρ)/2`, `ρ` nontrivial; all **nonreal** (ζ has no real nontrivial zeros) and all with `Re s ∈ (1/2, 1)` — so *zero* real right zeros and strip confinement with the explicit bound `1`. One pole, `σ_1 = 1`. | FJS six-item divisor list: *"Finitely many real zeros of the form ρ_i > 1/2, with multiplicity"*, *"Finitely many poles σ_i in (1/2,1]"*. `LAW_..._SOL.md:195-198`. Strip confinement: Kelmer Thm 3 preamble, *"Zeros in Re s>(d−1)/2 lie in a vertical strip … the note leaves this implicit; it is needed"*, `LAW_SECOND_AUDIT_REFEREE.md:19` | **PASS** both; right column carries the *implicit-step* flag of the cold audit. |
| **A6** `\|φ(σ+it)\| ≤ C(ε)` on `1/2 ≤ σ ≤ 3/2`, `\|t\| ≥ ε` | **Same source, same statement.** Hejhal Lemma 7.7 is printed for finite `N`, and `q = 3` is `N = 3`. Cold referee, PDF p. 574 image: *"LEMMA 7.7. For each ε>0 there exists C₆(ε) such that (7.15) \|φ_N(s)\| ≤ C₆(ε) whenever ½≤σ≤3/2 and \|t\|≥ε."* with proof line *"Repeat the derivation of 155(12.2) with B=10 when N < ∞"* — *"The finite-N case is the printed case."* `LAW_SECOND_AUDIT_REFEREE.md:14` | Identical: Hejhal Lemma 7.7 is uniform in `N` (`LAW_HEJHAL_S7_EXTRACT.md`, §1 inventory). `LAW_..._SOL.md:159-164,184-186` | **PASS** both, from one shared source |
| **A7** `\|φ(1/2+it)\| = 1`, exact modulus `(G)` | Hejhal p. 577 printed: *"Recall that \|φ_N(½+it)\| ≡ 1 for t ∈ ℝ"*; verified numerically `\|φ₃(½+it)\| = 1.000000000000000` at `t = 1, 3.7, 20`; and the `L*` modulus `(1/√π)√(t tanh πt)` matched **to 1e−31**. `LAW_SECOND_AUDIT_REFEREE.md:24,26` | Same Hejhal line (uniform in `N`) plus `A2 + A3`. `LAW_..._SOL.md:150-157,247-262` | **PASS** both |

**Result of NOGO-2: no axiom failed on either side.** Every row is `PASS`
for the arithmetic `q = 3` and for every finite `q ≥ 3` including the
non-arithmetic ones, and — the crucial structural fact — **in six of the
nine rows the two columns are the same citation**, because Hejhal §7, FJS,
and MMS are all printed for all finite `q ≥ 3` at once. `A` was not
assembled by intersecting two separately-verified lists; it is a single list
whose sources never distinguish the cases.

Conditional / flagged rows are collected in §5.3. **`q = 4` and `q = 6`**
(the other arithmetic members) inherit every right-column receipt verbatim,
since all of Hejhal §7, FJS, and MMS quantify over all finite `q ≥ 3`; they
are not treated separately and no closed form for `φ_4, φ_6` is used or
needed.

---

## 3. NOGO-3 — the metatheorem

### 3.1 Logical setting

We argue **semantically**, which is the only form the claim needs and the
only form it can honestly carry. `𝔐(A)` is the class of Hecke-type
scattering pairs satisfying `A0`–`A7`. For a statement `S` about such a
pair, write

* `A ⊨ S` ("`A` entails `S`") for: every `M ∈ 𝔐(A)` satisfies `S`;
* `A ⊭ S` for: some `M ∈ 𝔐(A)` fails `S` — a **countermodel**.

By soundness, if `A ⊭ S` then there is no valid derivation of `S` from `A`
in any proof system, since a derivation from `A` alone is a derivation valid
in every member of `𝔐(A)`. That is the whole logical content of a no-go of
this kind, and it is the reason a single countermodel settles the matter.

The two candidate on-line rigidity statements:

```
P_naive :  φ has no zero ρ with Re ρ > 1/2 and Im ρ ≠ 0.
P_line(c):  every zero ρ of φ with 1/2 < Re ρ < 1 and Im ρ ≠ 0 has Re ρ = c.
```

### 3.2 Lemma (breadth of `𝔐(A)`)

`φ_q ∈ 𝔐(A)` for every finite integer `q ≥ 3`, arithmetic and
non-arithmetic alike.

*Proof.* §2, row by row. ∎ *(Status: PROVED, at the caveat level of §5.3.)*

### 3.3 Metatheorem I — the naive on-line rigidity statement is refuted, not merely undecided

> **METATHEOREM I.** `A ⊨ ¬P_naive`. Explicitly: every `M ∈ 𝔐(A)` has
> infinitely many zeros `ρ` with `Re ρ > 1/2` and `Im ρ ≠ 0`, and hence
> (by `A2`) infinitely many multiplicity-matched poles `1 − ρ` with
> `Re(1−ρ) < 1/2`, `Im(1−ρ) ≠ 0`.
>
> **Consequence (the no-go).** There is no valid derivation of `P_naive`
> from `A`. Not because `A` is too weak to reach it, but because `A`
> proves its negation. Any argument that appears to derive on-line
> rigidity in the sense of `P_naive` from the functional equation,
> critical-line unitarity, meromorphic continuation, a generalized
> Dirichlet series, and polynomial vertical growth **contains an error**,
> and the error can be exhibited: apply the argument to `φ_5`.

*Proof.* This is the promoted LAW, read as a statement about `𝔐(A)`
rather than about Hecke orbifolds. Inspect its proof and observe that every
input is an axiom of `A`:

* `(NF)` and the right-edge estimate `L*(s) = 1 + O(e^{−c·Re s})` — `A4`
  (`LAW_..._SOL.md:139-146`).
* The Jensen/Littlewood rectangle `(J)` with the `+` pole term — `A1`, `A5`
  for the finitely many poles `σ_j`, `A6` for the horizontal edges, `A4`
  for the right edge sent to `+∞`, plus the purely complex-analytic
  `[Sel90, Lemmas 1,2]` template (`LAW_..._SOL.md:206-229`). The `+` sign
  is not a convention: with `−` the numerics at `q = 3` are off by exactly
  `T` (`LAW_SECOND_AUDIT_REFEREE.md:20`).
* The critical-line integral `(I)` with leading coefficient `1/(4π)` —
  `A7`'s exact modulus `(G)` plus `|Γ(½+it)/Γ(it)|² = |t| tanh(π|t|)`
  (`LAW_..._SOL.md:245-283`).
* The divergence step — `A5` (finitely many *real* right zeros contribute
  `O(T)`) against the promotion block's
  `F(½,T) = (1/4π)T² log T + O(T²)`, which diverges faster
  (`LAW_..._SOL.md:415-423`).
* Strictness: a zero with `Re ρ = 1/2` carries Jensen weight
  `(Re ρ − 1/2) = 0`, so a divergent weighted sum forces `Re ρ > 1/2`
  strictly; independently, `A2 + A3 + A7` forbid any divisor on the line at
  all, since `ord φ(s) + ord φ(1−s) = 2m = 0`
  (`LAW_SECOND_AUDIT_REFEREE.md:24`, "airtight").
* Nonreality: `A5` bounds the real contribution by `O(T)`, below the
  `(1/4π)T² log T` main term (`LAW_SECOND_AUDIT_REFEREE.md:25`).
* Reflection: `A2` turns an order-`m` zero at `ρ` into an order-`m` pole at
  `1 − ρ` (`LAW_..._SOL.md:326-334`).

No step consumes a group, a surface, arithmeticity, an Euler product, or
`q`. The argument is therefore a derivation from `A`, and its conclusion
holds in every member of `𝔐(A)`. ∎

*Status: PROVED, at the standing of the promoted LAW — i.e. **CONFIRMED by
two independent cold audits, conditional on the unread `[Sel90, Lemmas
1,2]`***
(`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:399-439`;
`LAW_SECOND_AUDIT_REFEREE.md:48-61`). The combinatorial finish is
additionally **machine-verified conditional on `H3`–`H5`** (Aristotle v33,
`LawSkeletonI.lean`; MAP 2026-08-23 06:55Z). No scattering-theoretic content
is machine-verified.

**Two independent confirmations that Metatheorem I is not an artifact of the
non-arithmetic side.**
(i) The cold audit instantiated the entire chain at `q = 3` and found it
holds *on the nose* (`LAW_SECOND_AUDIT_REFEREE.md:26`).
(ii) Kelmer Remark 0.2 records the same phenomenon classically for
`SL₂(ℤ)`: a **positive proportion** of scattering poles on `Re s = 1/4`
(ibid.). `P_naive` fails for the modular surface as a matter of classical
fact.

### 3.4 Metatheorem II — `A` also cannot refute the RH-analogue

> **METATHEOREM II (CONDITIONAL ON RH).** Assume RH. Then
> `A ⊭ ¬P_line(3/4)`: the pair `φ_3 ∈ 𝔐(A)` satisfies `P_line(3/4)`.
> Hence there is no valid derivation from `A` of the failure of on-line
> rigidity in its RH-analogue form.

*Proof.* `φ_3 ∈ 𝔐(A)` by §3.2. By Proposition 4.1 below,
`P_line(3/4)` holds for `φ_3` if and only if RH. ∎

*Status: PROVED, CONDITIONAL ON RH.* The conditionality is unavoidable and
is not a defect of the method: an unconditional witness for
`A ⊭ ¬P_line` would be an unconditional example of a scattering
determinant with all its right-strip zeros on one line, which for `φ_3`
**is** RH.

Combining I and II: within the axiom set `A`, the naive rigidity statement
is decided (negatively) and the RH-analogue is — conditional on RH —
**not refutable**. Whether it is *provable* from `A` is §5.1, and it is
open.

### 3.5 Corollary — arithmeticity-blindness

> **COROLLARY.** Let `S` be any statement about a Hecke-type scattering
> pair with `A ⊨ S`. Then `S` holds for `φ_q` for **every** finite
> `q ≥ 3`. Consequently no consequence of `A` distinguishes arithmetic
> `q ∈ {3,4,6}` from non-arithmetic `q`, and no `A`-only argument can serve
> as an arithmeticity criterion.

*Proof.* §3.2 plus the definition of `⊨`. ∎

This is the formal form of the second audit's downstream-misuse finding:
the LAW's "in particular, nonarithmetic" clause *"carries **zero**
arithmeticity information"* and *"must never be used as an arithmeticity
signature"* (`LAW_SECOND_AUDIT_REFEREE.md:27,59`; the same ledger rule is
written into `LawSkeletonI.lean:52-55`).

---

## 4. The RH calibration

### 4.1 Proposition (exact equivalence)

> **PROPOSITION 4.1.** `P_line(3/4)` holds for `φ_3` **if and only if** the
> Riemann Hypothesis holds. Moreover `P_naive` **fails** for `φ_3`
> unconditionally.

*Proof.* `φ_3(s) = Λ(2s−1)/Λ(2s)` (§2). `Λ` is entire of order 1 except for
simple poles at `w = 0, 1`, its zero set is exactly the set of nontrivial
zeros of `ζ`, and `Λ(w) = Λ(1−w)`.

*Zeros in `Re s > 1/2`.* `Λ(2s−1) = 0 ⟺ 2s−1 = ρ` nontrivial `⟺ s = (1+ρ)/2`,
giving `Re s = (1+β)/2 ∈ (1/2, 1)` since `0 < β < 1`. Poles of the
denominator `Λ(2s)` in `Re s > 1/2` would need `2s ∈ {0,1}`, i.e.
`s ∈ {0, 1/2}` — neither is in the open region — so no cancellation occurs
there. Zeros of `Λ(2s)` lie at `Re s = β/2 < 1/2` and contribute poles, not
zeros, and not in `Re s > 1/2`. Hence

```
{zeros of φ_3 in Re s > 1/2} = { (1+ρ)/2 : ζ(ρ)=0 nontrivial },
```
a bijection preserving multiplicity, all of them nonreal and all with
`1/2 < Re s < 1`.

*Consequences.* (a) The set is nonempty (indeed infinite), so `P_naive`
fails for `φ_3` unconditionally — no RH needed, only the existence of a
nontrivial zero of `ζ`. (b) `Re((1+ρ)/2) = 3/4 ⟺ β = 1/2`. Therefore every
such zero has `Re s = 3/4` iff every nontrivial zero of `ζ` has real part
`1/2`, i.e. iff RH. ∎

*Status: PROVED here, unconditionally, from the classical closed form of
`φ_3` — which is itself a **NOT-READ standard citation** (Iwaniec §3.4)
corroborated twice inside our bank (`LAW_SECOND_AUDIT_REFEREE.md:26`).*

### 4.2 The scattering-pole reading

By `A2`, the poles of `φ_3` in `Re s < 1/2` are the reflections `1 − s` of
the zeros above, i.e. `s = (1−ρ)/2` with `Re s = (1−β)/2`. So
`P_line(3/4)` for zeros `⟺` all nonreal scattering poles of the modular
orbifold lie on `Re s = 1/4` `⟺` RH. This is the classical
Faddeev–Pavlov / Lax–Phillips reading of RH as a statement about the
resonances of the modular surface, and it is exactly what Kelmer's Remark
0.2 is describing when it locates a positive proportion of poles on
`Re s = 1/4` (`LAW_SECOND_AUDIT_REFEREE.md:26`).
**Faddeev–Pavlov and Lax–Phillips are NOT-READ citations here**; the
equivalence proved in §4.1 does not depend on them and is self-contained
given the closed form.

### 4.3 Why this matters for the lane

The brief's `P` conflates two different lines. The functional equation
`φ(s)φ(1−s) = 1` reflects about `Re s = 1/2`, so `Re s = 1/2` is the
*symmetry* line of `φ`. But the zeros of the underlying `ζ` are pushed to
`Re s = 3/4` by the `w = 2s−1` substitution, so the *rigidity* line is
`3/4`. Any future statement of the no-go must keep these apart. Writing
"on-line rigidity" without saying **which** line is the mistake this note
exists to catch.

---

## 5. Scope, limitations, and everything that is not proved

**This paragraph is the load-bearing one; it is written to be quoted
verbatim and must not be paraphrased into something stronger.**

> **SCOPE.** Metatheorem I says: *the axiom set `A` — meromorphic
> continuation of order at most two, the functional equation
> `φ(s)φ(1−s) = 1`, reality, a generalized Dirichlet series with the
> Hejhal archimedean factor and `κ = 1`, finiteness of the real right
> divisor with strip confinement, a polynomial vertical bound, and the
> exact critical-line modulus — entails that infinitely many zeros lie
> strictly to the right of `Re s = 1/2`.* Therefore any proof schema whose
> only inputs are the members of `A`, and which is claimed valid for every
> structure satisfying `A`, cannot establish that all such zeros lie on
> `Re s = 1/2`; a schema that appears to do so is refuted by any `φ_q`,
> `q ≥ 3`.
>
> **IT DOES NOT SAY that there is no proof of the Riemann Hypothesis
> without an Euler product, and it does not say that the RH-analogue in
> this family is unprovable, undecidable, or independent of anything.** It
> is a statement about one explicitly listed set of hypotheses and about
> proof schemas that quantify over all its models. A proof about `ζ` — or
> about `φ_3` — is entitled to use inputs outside `A`: the Euler product,
> multiplicativity, the Hadamard factorization with its explicit zero
> density, subconvexity, moments, the explicit formula with prime powers,
> the `q = 3` Fourier expansion, or any other `ζ`-specific structure. Such
> a proof is untouched by anything here. Metatheorem I constrains only the
> *generic* route, and only in the naive `Re s = 1/2` reading.
>
> **THE RH-ANALOGUE READING IS NOT SETTLED HERE.** For
> `P_line(3/4)` — the statement that is genuinely equivalent to RH at
> `q = 3` (Proposition 4.1) — this note proves only one direction, and that
> one conditionally: assuming RH, `A` cannot *refute* it (Metatheorem II).
> Whether `A` can *prove* it is **OPEN**; see §5.1. Nobody may read
> Metatheorem I as evidence that the RH-analogue is out of reach of generic
> methods. It is evidence that one particular naive formulation of it is
> false.
>
> **NO ARITHMETICITY CONTENT.** Corollary 3.5 is a blindness statement, not
> a dichotomy. Nothing here distinguishes arithmetic from non-arithmetic
> `q`, and nothing here may be cited as an arithmeticity criterion.
>
> **DEPENDENCY.** Everything rests on the promoted LAW, whose one
> undischarged citation — `[Sel90, Lemmas 1, 2]`, reached only through
> Kelmer's transcription of `(4.20)` — has not been read by the LAW's
> author, by either of its referees, or by this author. Numerical
> corroboration at `q = 3` is not proof. Declare it in any downstream use.

### 5.1 The precise open problem

> **OPEN (NOGO-OPEN-1).** Exhibit `M = (φ, 𝒟) ∈ 𝔐(A)` and two nonreal
> zeros `ρ₁, ρ₂` of `φ` with `1/2 < Re ρ_i < 1` and `Re ρ₁ ≠ Re ρ₂`.
> Any such `M` gives `A ⊭ P_line(c)` **for every `c` simultaneously**, and
> upgrades the slogan "generic machinery cannot prove on-line rigidity"
> from a claim about `P_naive` to a claim about the genuine RH-analogue.

Three remarks on why this is not available today.

1. **The `G_5` off-line pin does not supply it.** `THEOREM_G5_OFFLINE_ASSEMBLY.md`
   and `NO_VERTICAL_LINE_COROLLARY.md` certify a zero `s*` of the **Selberg
   zeta** `Z_{G_5}` at `Re s* ≤ 0.4538962 < 1/2` — a *different function*,
   and on the *wrong side* of the line for `P_line`. That note itself says
   the single-line refutation needs *"two certified pins at distinct real
   parts"* and *"that remains open"* (`NO_VERTICAL_LINE_COROLLARY.md:58-60`),
   and that until then *"the G_5 zeros lie on no single vertical line"
   stays EMPIRICAL* (ibid.:132-133).
2. **We have no certified zero of any `φ_q` for non-arithmetic `q`.**
   `SCAT_EVAL_Q_SOL.md` records `SCAT-EVAL_q` as **OPEN**: there is no
   theorem-valid scalar `φ_q` zero-minus-pole certifier in the bank, only
   the Selberg-zeta bypass.
3. **A synthetic countermodel is a genuine construction problem.** `A2`
   holds automatically for any `φ(s) = Λ_D(2s−1)/Λ_D(2s)` built from a
   completed function with `Λ_D(w) = Λ_D(1−w)`, so a Davenport–Heilbronn-
   type function with off-line zeros is the natural candidate. But `A4`'s
   Hejhal archimedean factor with `κ = 1`, `A4⁺` positivity, `A5`, `A6`
   and the *exact* modulus `A7` are all further constraints, and none of
   them has been checked for any such function. **Nothing in this note
   asserts that such an `M` exists.** Listing the candidate is a research
   pointer, not a result. Marked **CONJECTURAL / UNATTEMPTED**.

### 5.2 A related open question worth separating

Hejhal **Theorem 7.11 / Corollary 7.12** (pp. 577–579) prove that for `N`
sufficiently large, every rectangle `[½, ½+δ] × [t₀−δ, t₀+δ]` contains
zeros of `φ_N` — arbitrarily close to the line, at any prescribed height
(`LAW_HEJHAL_S7_EXTRACT.md`; `LAW_SECOND_AUDIT_REFEREE.md:34`). This is a
printed partial antecedent of the LAW, weaker in `q`-range and stronger in
localization. It is **not** a countermodel to `P_line`: it places zeros
near `Re s = ½`, but "near" is not "at two separated real parts", and it is
asymptotic in `N`. It must nonetheless be cited wherever novelty is framed.

### 5.3 Flagged rows from the NOGO-2 table

No axiom **failed** on either side. Four rows carry inherited flags, none
of which is a failure:

1. **A5 / strip confinement, non-arithmetic side — IMPLICIT STEP.** The
   LAW note does not state it; the cold referee supplied it from Kelmer's
   Thm 3 preamble and flagged it as *"one implicit step named"*
   (`LAW_SECOND_AUDIT_REFEREE.md:19`). Not a gap in the mathematics, a gap
   in the write-up. On the arithmetic side it is explicit and trivial
   (`Re s < 1`).
2. **A4 / discreteness, non-arithmetic side — REFUTED ATTACK, NOT A
   THEOREM.** `0 < g_1 < g_2 < …` is printed in FJS Thm 2.1 for the general
   orbifold and is therefore source-established; the audit's exact `ℤ[λ_5]`
   enumeration and the `q ≤ 17` float sweep are *corroboration* of a
   printed statement, not the source of it. Recorded because `ℤ[λ_q]` being
   dense in `ℝ` makes this the least obvious axiom in the list.
3. **A1 / order ≤ 2 and A6 — the whole chain rests on Hejhal §7 and FJS,
   both consumed through `pdftotext` extractions that the second audit
   relabelled as TRANSCRIPTIONS, not verbatim command output**
   (`LAW_SECOND_AUDIT_REFEREE.md:40`; `LAW_..._SOL.md:474-478`). The cold
   referee independently re-extracted and reproduced the line numbers and
   inspected the page images, which is why these rows are `PASS` rather
   than flagged; but nothing here is a machine-checked quotation.
4. **The Hejhal (7.2)–(7.5) conjugation.** Hejhal states (7.5) for the
   conjugated group `𝒢̃_N = a(1/√λ) G_N a(√λ)` with cusp width 1 and
   `ϰ ≡ 1`, not for `G_N` as the LAW note writes. The repair is that the
   normalization changes `φ` only by the zero-free factor `c^{1−2s}`, which
   preserves both the divisor and `φ(s)φ(1−s) = 1`
   (`LAW_SECOND_AUDIT_REFEREE.md:15`, "GAP (cosmetic, repaired here)").
   `A` is stated for the conjugated normalization; nothing in §3 is
   sensitive to it.

### 5.4 Mandatory citation repairs inherited from the second audit

Any paper-level use of this note must carry all four
(`LAW_SECOND_AUDIT_REFEREE.md:54-57`): cite **Selberg 1990** as the source
of the `d = 2` counting theorem and state that it was not read; cite
**Hejhal Thm 7.11 / Cor. 7.12** as the printed partial antecedent; fix the
**Venkov** citation to *Trudy Mat. Inst. Steklov* **153 (1981)**, Thm 3.5
p. 59, not the 1979 Uspekhi survey; relabel the paraphrased receipt blocks.
Additionally: **do not consume `A_q`, `B_q`, or `C_q` from Kelmer** — his
printed `B_Γ` carries a spurious `log π` and his `A_Γ` assembly formula is
wrong (ibid.:38). None of these constants is used anywhere in this note.

---

## 6. Candidate paper section (draft)

> ### `§n.` A no-go for generic proofs of on-line rigidity
>
> The scattering determinant of a finite-area hyperbolic orbifold with one
> cusp carries a standard analytic package: meromorphic continuation of
> order at most two, the functional equation `φ(s)φ(1−s) = 1`, reality,
> a generalized Dirichlet series `φ(s) = √π (Γ(s−½)/Γ(s)) Σ d(n) g_n^{−2s}`
> convergent in `Re s > 1` with positive coefficients and discrete
> exponents, finitely many real zeros and poles to the right of the
> critical line, a polynomial bound on vertical lines, and the
> critical-line identity `|φ(½+it)| = 1`. Call this package `A`. It is
> shared, with identical citations, by the arithmetic Hecke triangle
> groups `q ∈ {3,4,6}` and by every non-arithmetic `G_q`: every input is
> printed in Hejhal §7, Friedman–Jorgenson–Smajlović, and
> Mayer–Mühlenbruch–Strömberg for all finite `q ≥ 3` at once.
>
> Theorem A of this paper shows that `A` alone forces infinitely many
> zeros strictly to the right of `Re s = ½`. Read as a statement about the
> class of all structures satisfying `A`, this has an immediate
> methodological consequence.
>
> **Theorem (no-go).** *There is no derivation, from `A` alone, of the
> statement that `φ` has no zeros off the line `Re s = ½` in the right
> half-plane. Any such derivation would contradict Theorem A, and is
> refuted by every `φ_q`, `q ≥ 3`, arithmetic and non-arithmetic alike.*
>
> The interest of the statement lies in the breadth of `A`, and the
> statement must be read with two cautions.
>
> First, the line matters. For `q = 3` one has the classical closed form
> `φ_3(s) = Λ(2s−1)/Λ(2s)`, `Λ(w) = π^{−w/2}Γ(w/2)ζ(w)`, whose zeros in
> `Re s > ½` are exactly `s = (1+ρ)/2` for `ρ` a nontrivial zero of `ζ`.
> The Riemann Hypothesis is therefore *not* the assertion that these zeros
> lie on the symmetry line `Re s = ½` — that assertion is false — but that
> they lie on `Re s = ¾`, equivalently that all nonreal scattering poles of
> the modular orbifold lie on `Re s = ¼`. The no-go above concerns the
> symmetry line, and does not bear on the rigidity line.
>
> Second, the no-go constrains proof schemas, not proofs. It says that an
> argument valid for every structure satisfying `A` cannot conclude on-line
> rigidity in the symmetry-line sense. It says nothing about arguments that
> use structure absent from `A` — an Euler product, multiplicativity, the
> explicit formula, or any other feature specific to `ζ`. In particular it
> is not a statement about the provability of the Riemann Hypothesis.
>
> What `A` *cannot* do is separate the arithmetic members of the family
> from the non-arithmetic ones: since every axiom holds in both cases with
> the same citation, every consequence of `A` holds throughout the family.
> The off-line phenomenon of Theorem A is accordingly not an arithmeticity
> invariant, and we record explicitly that it must not be used as one:
> for `Γ = SL₂(ℤ)` a positive proportion of the scattering poles already
> lie off the symmetry line, on `Re s = ¼`.
>
> Whether `A` can decide the rigidity-line statement remains open. We can
> say only that it cannot refute it: assuming the Riemann Hypothesis,
> `φ_3` is a structure satisfying `A` in which all right-strip zeros lie on
> a single vertical line. A structure satisfying `A` with right-strip zeros
> at two distinct real parts would settle the remaining direction; we know
> of none.

---

## 7. Provenance

Files read in full: `LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md`,
`LAW_SECOND_AUDIT_REFEREE.md`, `NO_VERTICAL_LINE_COROLLARY.md`,
`projects/aristotle_dispatch_v33/LawSkeletonI.lean`. Read in part:
`LAW_MINIMAL_HYPOTHESES.md` (§0–§1, scope check only),
`LAW_HEJHAL_S7_EXTRACT.md` (§1 inventory), `SCAT_EVAL_Q_SOL.md` (§1–§2),
`LAW_MIRROR_Q3_DISCRIMINATOR.md` (§0, not used),
`plans/wayfinder/rh-goals/MAP.md` (2026-08-23 entries).

Not read, and cited as such: Selberg 1990; Venkov 1981; Iwaniec, *Spectral
Methods*, §3.4; Faddeev–Pavlov; Lax–Phillips; Davenport–Heilbronn.

No numerics were run for this note. Every number quoted is a transcription
from the cited in-repo line, not a fresh measurement.

**Lane label: UNREFEREED. READY FOR COLD REFEREE (NOGO-4).** Attack order:
(i) the claim in §1.3 that `A` is *exhaustive* of what the LAW consumes —
find an input the list omits; (ii) Proposition 4.1's divisor bookkeeping at
`s = ½` and `s = 1`; (iii) whether `A6` for `q = 3` really is the printed
`N = 3` case of Hejhal 7.7; (iv) whether Metatheorem I's "no step consumes
`q`" survives a line-by-line re-read of the LAW's §4.

---

## Section 8 — Correction block (2026-08-23, from NOGO_METATHEOREM_REFEREE.md)

**Append-only.** Nothing above this line was altered. This block applies all
thirteen corrections D1–D13 of the cold referee report
`research_notes/rh_goals_2026-08-14/lane_g/NOGO_METATHEOREM_REFEREE.md`
(dated 2026-08-22, gate **PROMOTABLE-with-corrections**). Where the referee
prescribes exact language, that language is quoted and adopted. Where a
correction contradicts text in §§0–7, **this block governs**.

The referee refuted no claim of the note. Proposition 4.1 is **CONFIRMED
unconditionally**, re-derived and verified numerically to 20+ digits. The two
attacks most likely to land — positivity via Selberg's class, and the
`c^{1−2s}` conjugation repair — both **fail**; `A4⁺` is genuinely not
load-bearing for Metatheorem I, because Kelmer (4.10)–(4.12) carries *"real
but not necessarily positive"* coefficients and positivity enters only in his
Lemma 4.6, which the LAW does not consume.

### D1 (SEVERE) — the entailment is `A ∧ H_Sel90 ⊨ ¬P_naive`, not `A ⊨ ¬P_naive`

**Corrected statement of Metatheorem I.** Everywhere §0 (table row 1), §3.3,
§5 SCOPE, and §6 write `A ⊨ ¬P_naive`, read instead

```
A ∧ H_Sel90  ⊨  ¬P_naive,
```

where `H_Sel90` denotes the (unread) hypothesis list of `[Sel90, Lemmas 1,2]`.

**The risk, in the referee's words.** The Jensen identity `(J)` is Kelmer
`(4.20)`, justified verbatim by *"By Proposition 4.4, `L*(s)` satisfies all the
assumptions needed for `[Sel90, Lemma 1,2]`."* The note's LEDGER RULE treats
this as a *truth* risk ("proved modulo one unread citation"). It is also, and
more damagingly for a **metatheorem**, a *hypothesis-containment* risk: the
claim `A ⊨ ¬P_naive` requires that every hypothesis of Sel90 Lemmas 1,2 is
derivable from `A0–A7`. What is actually verified is only that Kelmer's Prop
4.4 conclusions `(4.13)–(4.15)` follow from `A` (the referee confirms they do,
at `d=2, κ=1`), and that Kelmer *asserts* Prop 4.4 suffices for Sel90. Nobody
has checked Sel90's hypothesis list against Prop 4.4's conclusions. For a
theorem about `φ_q` this is a normal citation dependency; for a **no-go
quantifying over all models of an explicit axiom list**, an unread hypothesis
list is a direct threat to the axiom list's exhaustiveness.

**Consequence for §1.3.** `A` is exhaustive of what the LAW consumes **modulo
the unread hypothesis list of `[Sel90, Lemmas 1,2]`**. The exhaustiveness claim
of §1.3 **cannot be closed until Sel90 is read.** Per the referee's standing
ambiguity: the note is graded against the weaker, checkable claim "no step
*visible in the transcribed chain* consumes anything outside `A`", which it
satisfies; the stronger claim, which is what a no-go metatheorem needs, remains
**OPEN**, and belongs in the SCOPE box, not a footnote.

**Cross-reference (added 2026-08-23, conditional only).** A sibling lane note,
`research_notes/rh_goals_2026-08-14/lane_g/SEL90_BYPASS_JENSEN_REDERIVATION_SOL.md`
(**UNREFEREED**), rederives `(J)` in exactly the form the chain consumes, with
no appeal to Selberg 1990. **IF** that note survives a cold referee, D1's
residual shrinks from `H_Sel90` to the bypass's own inputs (including its own
declared residual `GAP-1`, which the bypass states does not block the imported
form `H3`). This is stated **conditionally only**: the bypass is unrefereed, it
discharges nothing today, and no claim in this file may be strengthened on it.

### D2 — `A5`'s pole clause restated

`A5` as printed (*"finitely many poles `σ_j ∈ (1/2,1]`"*) does not exclude a
non-real pole in `Re s > 1/2`, but `(J)`'s pole term `T Σ_{σ_j > α}(σ_j − α)`
requires every right pole to be real. **`A5`'s pole clause is hereby restated
as:**

> **every pole of `φ` in `Re s > 1/2` is real and lies in `(1/2,1]`, and there
> are finitely many.**

This is what both source columns actually deliver (Kelmer Prop 4.4: *"holomorphic
in `Re s > (d−1)/2` except for finitely many poles in `((d−1)/2, d−1]`"*), so
the fix costs nothing. The zero and strip-confinement clauses of `A5` are
unchanged.

### D3 — Hejhal Lemma 7.3 is an `N ≥ 4` citation

In the §2 `A4⁺` row, the Hejhal Lemma 7.3 citation is printed for **`N ≥ 4`**
(it uses `λ ≥ √2`, and `λ_q = 2cos(π/q) ≥ √2 ⟺ q ≥ 4`). It therefore does
**not** cover `q = 3`. **`q = 3` is covered by the direct argument** that
`d(n) = ϕ_Euler(n)` is a positive integer count. The non-arithmetic `q ≥ 5` all
lie inside `N ≥ 4`. No fact changes; the row must not be presented as a
whole-family receipt.

### D4 — shared-citation count corrected to five

§2's closing paragraph reads "in six of the nine rows the two columns are the
same citation". **The correct count is five:** `A0, A4, A4⁺, A6, A7`. The rows
`A1, A2, A3, A5` carry distinct arithmetic-side derivations from `Λ`. (Under the
alternative reading "the generic citation also covers `q=3`" the count is 9. No
reading yields 6.) The structural point of the paragraph is unaffected.

### D5 — `d(n)` identified for `q = 3`

In the §2 `A4` row, the arithmetic column's Dirichlet data is explicitly

```
d(n) = ϕ_Euler(n),   g_n = n,   d(1) = 1,
Σ_{n≥1} ϕ_Euler(n) n^{−s} = ζ(s−1)/ζ(s),
```

so that `Σ d(n) g_n^{−2s} = ζ(2s−1)/ζ(2s) = L*_3(s)`; discrete, absolutely
convergent for `Re s > 1`, `d(1) ≠ 0`, and `d(n) > 0`. This makes the arithmetic
column a genuinely independent receipt rather than a restatement.

### D6 — strip confinement added as an input; §5.3 flag 1 downgraded

(a) **Added to Metatheorem I's input list** (§3.3 bullets): **strip confinement**
(`A5`) is consumed at the divergence step, where `β` must be bounded to convert
"unbounded weighted sum" into "infinitely many zeros".

(b) **§5.3 flag 1 is downgraded** from "implicit step supplied by the referee"
to an **"immediate corollary of `A4`"**: by `(4.12)` / the `(NF)` right-edge
estimate, `|L* − 1| < 1` for `Re s` large, so `L*` has no zeros there. Strip
confinement is therefore not an independent assumption. This is a
*strengthening* of the note.

### D7 — "unavoidable" weakened

§3.4's status paragraph ("The conditionality is unavoidable") is corrected to
**"unavoidable for this witness"**. The note gives no argument that no other
`M ∈ 𝔐(A)` has unconditionally-collinear right-strip zeros.

### D8 — the trichotomy is mis-calibrated; corrected table

Two rows are added, both immediate from `φ_3 ∈ 𝔐(A)` plus Prop 4.1:

(a) **`A ⊨ P_line(3/4)` is RH-HARD.** Since `φ_3 ∈ 𝔐(A)`, `A ⊨ P_line(3/4)`
implies `φ_3 ⊨ P_line(3/4)` implies RH by Prop 4.1. The third row is therefore
not "open" in the ordinary sense — it is **RH-hard**, and the note's own Prop
4.1 supplies the reduction **in one line**.

(b) **An unconditional statement the note missed.** `φ_3` alone shows that `A`
**fails to decide `P_line(3/4)` in at least one direction**, unconditionally:
if RH holds then `A ⊭ ¬P_line(3/4)`; if RH fails then `A ⊭ P_line(3/4)`.

**Corrected trichotomy table** (supersedes the §0 table):

| statement | relation to the axiom set `A` | status |
|---|---|---|
| `P_naive` (§3.1 definition) — no nonreal zero with `Re ρ > 1/2` | **`A ∧ H_Sel90 ⊨ ¬P_naive`** — `A` (plus the unread Sel90 hypothesis list) *entails the negation* | **PROVED** (§3.3), modulo `H_Sel90` (D1) |
| `¬P_line(3/4)` — the RH-analogue fails | **`A ⊭ ¬P_line(3/4)`** — `A` cannot refute on-line rigidity | **PROVED CONDITIONAL ON RH** (§3.4); witness `φ_3`; conditionality unavoidable *for this witness* (D7) |
| `P_line(3/4)` — the RH-analogue holds | **`A ⊨ P_line(3/4)`?** | **OPEN and RH-HARD** — a positive answer proves RH via `φ_3` + Prop 4.1, in one line (D8a) |
| decidability of `P_line(3/4)` by `A` | **`A` fails to decide `P_line(3/4)` in at least one direction** | **PROVED UNCONDITIONALLY** — RH ⇒ `A ⊭ ¬P_line(3/4)`; ¬RH ⇒ `A ⊭ P_line(3/4)` (D8b) |

This is the note's best unclaimed result and its most important honesty
calibration.

### D9 — the §6 arithmeticity gloss corrected

§6's sentence *"What `A` cannot do is separate the arithmetic members of the
family from the non-arithmetic ones"* is **REFUTED as written**. Corrected
gloss: **"no *consequence of `A`* separates them."**

Added sentence, mandatory in any redraft: *the Dirichlet data itself is **not**
arithmeticity-blind* — the structures are pairs `M = (φ, 𝒟)` with
`𝒟 = (d(n), g_n)` in the language, and the `g_n` are the `|c|`-values, which lie
in `ℤ[λ_q]` and therefore encode `q`. An argument that inspects the Dirichlet
data — still "generic analytic machinery" by any ordinary reading — is **not**
covered by Corollary 3.5.

### D10 — `P_naive` fixed to the §3.1 definition everywhere

The note defines `P_naive` three incompatible ways (§0 "no zeros **at all** in
`Re s > 1/2`"; §3.1; §6 "no zeros off the line `Re s = ½` in the right
half-plane"). **The canonical definition, to be used everywhere, is §3.1's:**

```
P_naive :  φ has no zero ρ with Re ρ > 1/2 and Im ρ ≠ 0.
```

`A5` explicitly permits finitely many real right zeros, so the §0 and §6
readings are non-derivable from `A` for a second and trivial reason, which
weakens rather than strengthens the result. This is load-bearing for a note
whose whole thesis is "say which statement you mean".

### D11 — the exhibition is `φ_3`, not `φ_5`

§3.3's Consequence ("the error can be exhibited: apply the argument to `φ_5`")
is corrected to: **apply it to `φ_3`, where the failure is classical fact.**
§5.1 remark 2 states there is no theorem-valid `φ_q` zero certifier for
non-arithmetic `q`, so `φ_5` is not exhibitable.

### D12 — header dependency set expanded

The §0 LEDGER RULE header names Sel90 alone. Corrected: the residual dependency
is **"one unread *engine* citation plus the not-read/transcribed source set
enumerated in §2 and §5.3"**, namely:

* `[Sel90, Lemmas 1,2]` — the unread complex-analytic **engine** citation,
  reached only through Kelmer's transcription of `(4.20)`;
* Iwaniec, *Spectral Methods of Automorphic Forms*, 2nd ed., §3.4 — declared
  **NOT READ** (§2), source of the classical `φ_3` closed form;
* Venkov, *Trudy Mat. Inst. Steklov* **153 (1981)**, Thm 3.5 p. 59 — reached
  **only through FJS**, never at source;
* Hejhal §7 and FJS — consumed through **`pdftotext` transcriptions**, relabelled
  by the second audit as transcriptions and **not verbatim command output**
  (§5.3 flag 3); the `A1` (order ≤ 2) and `A6` chains rest entirely on these.

§5 DEPENDENCY was honest; the header was not, and the header is what gets
quoted.

### D13 — machine-verification pointer corrected

§3.3's status line and §7 provenance cite
`projects/aristotle_dispatch_v33/LawSkeletonI.lean`. That is the **dispatch
skeleton**: 16 `sorry` occurrences, header *"Everything below with a `sorry`
body is CONJECTURAL at the Lean level. This file machine-verifies nothing."*
**The claim is true; the pointer was to the file that refutes it.** The correct
citation for the machine-verified artifact is

```
projects/aristotle_dispatch_v33/aristotle_dispatch_v33_aristotle/LawSkeletonI.lean
```

— the returned, sorry-free artifact (3 `sorry` hits, all in prose; status line
*"No `sorry` bodies remain"*), with the independent local re-compile recorded at
MAP 2026-08-23 06:55Z. **The §1.3 claim-2 line references to the dispatch file
at `:31-32,160-162,182-183,210-213` are correct and stay**; `H1`/`H2` are
definitional per `DISPATCH.md:71-72`, so "the analytic imports are `H3`–`H5`" is
accurate.

---

**Post-correction status: PROMOTABLE-with-corrections applied; promotion to
CONFIRMED-conditional (on H_Sel90 containment) awaits re-referee sign-off;
paper-section draft NOT usable until re-drafted per D9/D10/D11.**

## Section 9 — D1 addendum and genericity statement (2026-08-23, from NOGO_METATHEOREM_REREFEREE.md, S-1/S-2/S-3)

**S-1 (staleness repair).** Section 8's D1 cross-reference described the
SEL90 bypass as UNREFEREED; that was true at write time and is now
superseded. The bypass was cold-refereed
(SEL90_BYPASS_JENSEN_REDERIVATION_REFEREE.md, commit 0408361, gate
PROMOTABLE-with-corrections), corrections D-1..D-3 applied, and
DISPATCH.md §11 relabels S5/H3 to PROVED (consumed form, per-q).

**S-2 (genericity / transfer statement — the paragraph licensing the
upgrade).** The bypass derivation is written for L*_q, q ≥ 3, but every
step of §§3.1–3.8 cites only the interface facts (D)/(NF), (E), (F),
(G)/(U), (P), (Rl) together with ambient classical analysis (Littlewood/
Titchmarsh 9.9, Stirling, subharmonicity, Carathéodory extension,
Schwarz reflection, Fubini, dominated convergence); §4 is a q=3
numerical check only and carries no proof weight. Each interface fact
is a consequence of the corrected axiom list: (D)/(NF) = A4 (+A3);
(E) = A4 (strict 0 < g₁ < g₂); (F) = A2 + A1 + A5 in its D2-corrected
form (the reality-of-right-poles clause is used essentially — under the
pre-D2 A5 this input exceeded A); (G)/(U) = A7 + the Γ-identity
|Γ(½+it)/Γ(it)|² = t·tanh(πt); (P) = A6 + Stirling + A4's absolute
convergence for σ ≥ 3/2; (Rl) = A3; Σ(σ_j−½) = O(1), monotonicity of
F, and strip confinement = A5/A4. Hence the derivation transfers
verbatim to an arbitrary M ∈ 𝔐(A), and Metatheorem I holds in the
upgraded form

> **A ⊨ ¬P_naive** (P_naive in the §3.1/D10 form),

no longer conditional on H_Sel90. Residuals printed alongside, none a
hypothesis on φ: (J) is consumed in the (J)-avg/H3 form only; GAP-1
((J)-sharp) and GAP-2 ((C)/(DIF)) still rest on Selberg 1990 and are
absent from the conclusion chain's signature (verified against
LawSkeletonI.lean by the bypass referee, rows 2/15/16). This paragraph
implements the re-referee's condition for certifying the A ⊨ sentence
(NOGO_METATHEOREM_REREFEREE.md, Duty 2 and S-2); the containment audit
it banks is the re-referee's own table, reproduced there.

**S-3 (nomenclature).** The §8 "corrected trichotomy table" has four
rows; it is henceforth the **decision table** of the metatheorem.

**Post-addendum status:** Metatheorem I stands PROMOTED in the form
A ⊨ ¬P_naive; Metatheorem II PROMOTED (conditional on RH, witness φ₃,
conditionality unavoidable for this witness); D8a OPEN and RH-HARD;
D8b PROVED unconditionally. The §6 paper draft remains unusable until
redrafted per D9/D10/D11.
