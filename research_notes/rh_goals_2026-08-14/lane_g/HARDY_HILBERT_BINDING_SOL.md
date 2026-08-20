# q=8 Hardy/Hilbert operator, basis and norm binding

Date: 2026-08-20. Branch `codex/prime-step-review-economic-validation`.

## Status

**REDUCED — NOT PROVED, NOT OPEN.**

Six of the eight sub-lemmas below are **PROVED** here, one of them
(**B6a**, enlarged-disc weight holomorphy) closing a piece that the repo had
recorded as open. Two sub-lemmas (**B2**, the eq.(32) source identification;
**B8**, the Banach/Hilbert determinant equality) are **REDUCED** to named
printed results plus a short, explicit residual list. Nothing here promotes a
q=8 determinant, Fredholm, Selberg, resonance, winding, or LAW claim. Nothing
here flips `full_tail_certified`.

**No file outside this one was created or modified.** `git status --porcelain`
on `lane_f/` and on `lane_g/l_out/` is empty at the end of this work. Nothing
was committed or pushed. No PDF was downloaded (see residual **R-B2-1**).

House rounding: upper bounds rounded **UP**, lower bounds and margins rounded
**DOWN**. Everything not marked PROVED is **CONJECTURAL**.

---

## 1. The gate, stated verbatim

The gate is phrased in six places. All six are quoted exactly.

**(G-a)** `lane_f/Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_SOL.md:108` (in
"Remaining OPEN gates"):

> 2. Exact q=8 MMS-to-Hardy/Hilbert operator, basis, and norm binding.

**(G-b)** `lane_f/Q8_SCHUR_CONTINUOUS_CONTOUR_REFEREE.md:388`:

> 2. Exact MMS-to-Hardy/Hilbert operator identification and basis/norm binding.

**(G-c)** `lane_f/Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_REFEREE.md:205`:

> 2. Exact q=8 MMS-to-Hardy/Hilbert operator, basis, and norm binding.

**(G-d)** `lane_g/L_OUT_RECEIPT_SOL.md:9-11`:

> Everything below is a computation on the pinned q=8 F1024 receipts. The
> separately-OPEN **"Exact q=8 MMS-to-Hardy/Hilbert operator, basis and norm
> binding"** is *not* claimed, not addressed, and every number here is
> conditional on it.

**(G-e)** `lane_g/SCHUR_SUBSTITUTION_DERIVATION_SOL.md:315-322`, which is the
**most caveated** phrasing because it alone names the specific mathematical
content the downstream inequalities consume:

> * **H0 — orthonormality of `{e_{j,k}}`.** Everything above uses (N4)
>   (`P_N` an orthogonal projection) and the identification
>   `sum_m |X[m,k]|^2 = ||X e_k||_2^2`. Both hold iff the `e_{j,k}` basis is
>   orthonormal for the Hilbert structure in which `||.||_1`, `||.||_HS` are
>   taken. `Q8_OUTPUT_TAIL_SOL.md:100-101` declares this ("Hardy/Hilbert norm in
>   the gate means precisely this"), and the adjudication records that the
>   **"Exact q=8 MMS-to-Hardy/Hilbert operator, basis and norm binding" remains
>   separately OPEN** (`L_OUT_CONDITION4_ADJUDICATION.md:361-367`).

**(G-f)** `lane_g/Q8_OUTPUT_TAIL_SOL.md:76-101`, which supplies the concrete
objects the gate is about:

> ```text
> H  =  H^2(D(c_1,r_1)) (+) H^2(D(c_2,r_2)) (+) H^2(D(c_3,r_3)),
> ```
>
> each summand the Hardy space of the disc with orthonormal basis
>
> ```text
> e_{i,m}(z) = ((z - c_i)/r_i)^m ,    m = 0, 1, 2, ...
> ```
>
> […] The relevant norms are the Hilbert-Schmidt norm of `H` in this basis and the
> trace norm; "Hardy/Hilbert norm" in the gate means precisely this.

### 1.1 Reconciliation, and the statement worked against

(G-a)–(G-d) are the same sentence. (G-e) and (G-f) are strictly stronger: they
name orthonormality, the projection property of `P_N`, and the two norms.
**Per the ledger rule, everything below is proved against the (G-e)+(G-f)
reading**, which is the most demanding one:

> **Gate (HH).** Let `H = ⨁_{i=1}^{3} H²(D(c_i,r_i))` with the discs of
> §2.1 and `e_{i,m}(z) = ((z−c_i)/r_i)^m`. Prove:
> **(i)** `{e_{i,m}}` is an orthonormal basis of `H`, so `P_N` (truncation at
> `m<N`) is an orthogonal projection and `Σ_m |X[m,k]|² = ‖X e_k‖₂²`;
> **(ii)** the matrix the q=8 checker builds in that basis is exactly the
> matrix of the MMS even-q eq.(32) reduced transfer operator `L_s` for `G_8`,
> occurrence for occurrence, branch for branch, weight for weight;
> **(iii)** the sup-norm quantities the R2/W/L-OUT tail certificates bound
> (boundary sups `b_k`, enlarged-contour sups `M_k(θ)`) **dominate** the
> Hilbert-space column norms `‖L_s e_{j,k}‖_H` those certificates are used as;
> **(iv)** `s ↦ L_s^H` is trace-class-valued and holomorphic on the region the
> winding/determinant argument uses, and its Fredholm determinant equals the
> MMS Banach determinant there.

Clause (iv) is what makes the gate load-bearing rather than notational: the
winding argument counts zeros of `det(1−L_s)`, and the finite-section
certificates control `det(I−M_N(s))`. Without (iii)+(iv) the two are unrelated
objects.

---

## 2. The q=8 objects

### 2.1 Geometry (F1024 pin)

Pinned receipt `lane_f/f8_receipts/Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json`,
SHA-256 `5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c`,
records `q=8`, `even_q=true`, `h_q=3`, `kappa=3`, `precision_bits=384`,
`M=512`, `lambda_exact_form="sqrt(2 + sqrt(2))"`.

λ₈ = 2cos(π/8) = √(2+√2). With the finite λ-CF value
`[a_1,…,a_r]_λ := x_0`, `x_r = 0`, `x_{t−1} = −1/(a_t λ + x_t)`, the four
partition points of `[−λ/2, 0]` are

    φ_0 = −λ/2,   φ_1 = [1,1]_λ,   φ_2 = [1]_λ,   φ_3 = 0,

i.e. the **single** even-q CF family `φ_i = [1]^{h−i}` with `φ_0` overridden to
`−λ/2` (`f8_certify_tb_blocks.py:124-143`). Then

    c_i = (φ_{i−1}+φ_i)/2,   h_i = (φ_i−φ_{i−1})/2,   r_i = a_i h_i,
    (a_1,a_2,a_3) = (10, 4, 2).

The three strings `("10","4","2")` are **radius multipliers**, the exact
analogue of q=7's five strings `("3.522","2.622","2.372","1.79","1.6")`; they
multiply the half-widths at `f8_certify_tb_blocks.py:151`. "F1024" is the label
formed by concatenating them. All of this is verified in §5/V1–V2.

### 2.2 The eight occurrences

Assembly loop, `lane_f/f8_source_builder.py:108-114`, verbatim:

```python
    # ---- explicit 8-block eq.(32) assembly, h = kappa = 3 ----
    add_cols(1, h, inf_block(1, h, 2, False))
    add_cols(1, h, inf_block(1, h, 1, True), prefac=sgn)
    for i in range(2, h + 1):
        add_cols(i, i - 1, single_block(i, i - 1, 1, False))
        add_cols(i, h, inf_block(i, h, 2, False))
        add_cols(i, h, inf_block(i, h, 1, True), prefac=sgn)
```

Unrolled at `h = κ = 3`, with `sgn = acb(sign)` and the certified `sign = 1`:

| # | out `i` | in `j` | branch | head / tail (start `n₀`) | coeff |
|--:|--:|--:|---|---|--:|
| 1 | 1 | 3 | `+ℓ`, ℓ≥2 | tail, n₀=2 | +1 |
| 2 | 1 | 3 | `−ℓ`, ℓ≥1 | tail, n₀=1 | +1 |
| 3 | 2 | 1 | `+1` | head | +1 |
| 4 | 2 | 3 | `+ℓ`, ℓ≥2 | tail, n₀=2 | +1 |
| 5 | 2 | 3 | `−ℓ`, ℓ≥1 | tail, n₀=1 | +1 |
| 6 | 3 | 2 | `+1` | head | +1 |
| 7 | 3 | 3 | `+ℓ`, ℓ≥2 | tail, n₀=2 | +1 |
| 8 | 3 | 3 | `−ℓ`, ℓ≥1 | tail, n₀=1 | +1 |

Two heads, six tails. The independently hand-written constant list
`f8_certify_tb_blocks.py:105-115` (`BLOCKS`, guarded by
`assert len(BLOCKS) == 8`) agrees with this unroll **as an exact set**
(§5/V8). The branch maps and weights are

    θ_{+n}(z) = −1/(z+nλ),   w_{+n,s}(z) = ((z+nλ)²)^{−s},
    θ_{−n}(z) = +1/(z−nλ),   w_{−n,s}(z) = ((z−nλ)²)^{−s},

principal power of the squared denominator.

**Structural deltas from q=7 that matter to this note.** (1) q=7 is odd, MMS
eq.(34), κ=2h+1=5 discs, 19 occurrences, two interleaved CF families; q=8 is
even, eq.(32), κ=h=3 discs, 8 occurrences, one CF family. (2) At q=7 the
negative branch contributes a **head** at −1 plus a tail from −2; at q=8 the
negative branch is a **single tail from n₀=1**. (3) The eq.(32) operator is
arrow-shaped, `L = [[0,0,B₁],[A₂,0,B₂],[0,A₃,B₃]]`, which is what licenses the
Schur reduction `det(I−L_N) = det(I−C_N)`, `C_N = B₃ + A₃B₂ + A₃A₂B₁`
(`q8_schur_contour.py:4-12`); q=7 has no such reduction. The table above is
exactly that arrow pattern.

### 2.3 Why the binding is load-bearing, not bookkeeping

Every one of the six tail families has input disc **j = 3**. The R2 input-column
envelope uses `q = |c_j| / r_j` (`q8_r2_local.py:206`,
`q = (abs(centers[j-1]) / radii[j-1]).upper()`), and `tau_in(N)` sums
`A q^N/(1−q)`. The certified values are

    |c_1|/r_1 ≤ 1.065686,   |c_2|/r_2 ≤ 1.457107,   |c_3|/r_3 = 1/2 exactly.

`|c_3|/r_3 = 1/2` is exact, not numerical: `φ_3 = 0` forces `c_3 = −h_3`, and
`a_3 = 2` forces `r_3 = 2h_3`. For input discs 1 and 2 the ratio **exceeds 1**
and `A q^N/(1−q)` would be negative and divergent. It is never evaluated there
only because the two blocks with `j ∈ {1,2}` are heads, routed to
`single_block_tail(weight, rho, N)` with no `q` at all
(`q8_r2_local.py:216`). So the geometric convergence of the entire input-column
tail is contingent on the eq.(32) row structure sending **all** tails to disc 3.
A misidentification of the even-q row pattern would not produce a visibly wrong
answer; it would silently produce a divergent bound. This is the sharpest
argument that sub-lemma **B2** must be closed by source, not by inspection.

---

## 3. Sub-lemma decomposition

| id | statement | verdict |
|---|---|---|
| **B1** | The three discs `D(c_i,r_i)` used by the checker are exactly the even-q Markov-partition discs of `[−λ₈/2,0]` with multipliers (10,4,2), with `φ` identified in ℚ(λ₈) | **PROVED** |
| **B2** | The 8 occurrences, branches, weights and sector coefficients are a literal specialization of MMS eq.(32) at `h_8=κ_8=3` | **REDUCED** (2 residuals) |
| **B3** | `{e_{i,m}}` is an orthonormal basis of `H`; `P_N` is an orthogonal projection; `Σ_m|X[m,k]|² = ‖Xe_k‖₂²` — i.e. hypothesis **H0** | **PROVED** |
| **B4** | Point evaluation is bounded on `H²(D)`, with `|f(c+Rv)| ≤ (1−|v|²)^{−1/2}‖f‖`; the checker's Taylor-coefficient functionals are the basis coefficient functionals | **PROVED** |
| **B5** | Norm domination: the boundary sups `b_k` and enlarged sups `M_k(θ)` dominate `‖L_se_{j,k}‖_H`, and `θ^{−N}M_k(θ)` dominates the omitted-output rows | **PROVED** |
| **B6a** | Every branch weight is holomorphic and pole/cut-free on the **enlarged** discs `D(c_i, 1.15 r_i)` | **PROVED (new)** |
| **B6b** | Strict image contraction from the enlarged source disc into the **base** target disc, ratio `ρ̂_H < 1` | **PROVED**, on receipt-grade caveat |
| **B7** | `s ↦ L_s^H` is trace-class-valued holomorphic on `Ω*` (centered-tail column estimate, even-q form) | **PROVED**, conditional on B2 |
| **B8** | `det_H(1−L_s^H) = det_B(1−L_s^{MMS})` on `Ω*` | **REDUCED** (3 residuals) |

---

## 4. Proofs, reductions, obstructions

### B1 — Geometry. PROVED.

Recompute λ₈ two ways and the four `φ_j` from the λ-CF recursion in 384-bit Arb
ball arithmetic, and check containment in the pinned receipt balls; then
recompute `c_i`, `h_i`, `r_i = a_i h_i`. All 4 partition points and all 9
geometry quantities land inside the pinned balls (§5/V1–V2). The identification
`φ_1 = [1,1]_λ`, `φ_2 = [1]_λ` is exact in ℚ(λ₈), not a numerical coincidence:
it is the even-q rule `φ_i = [1]^{h−i}` at `h=3`.

### B2 — MMS eq.(32) identification. REDUCED.

**What is available.** The MMS source is Mayer–Mühlenbruch–Strömberg,
*The transfer operator for the Hecke triangle groups*, arXiv:0912.2236v2,
DCDS 32 (2012), 2453–2484; the version SHA-256 banked by
`lane_f/Q7_MMS_PRIMARY_SOURCE_RECEIPT.md:25-26` is
`a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072`. The even-q
reduced operator is **equation (32), p. 21** (MMS label `reduced1`), not the
odd-q equation (34) used at q=5 and q=7.

**Three independent in-repo attestations of eq.(32)'s content.**

1. A cold referee who fetched the PDF and reproduced the banked hash,
   `lane_f/Q_GENERIC_SCHUR_REDUCTION_REFEREE.md:264-267`:

   > Cold comparison with MMS equation (32), p. 21, confirms the even orientation:
   > row 1 has `L_inf,+2` and sector-signed `L_inf,-1` in terminal column `h`;
   > rows `2..h` additionally have `L_+1` in column `i-1`.  The tracked code places
   > exactly these calls at `zeta_cert_rosen_even.py:228-236`.

2. The abstract row form, `lane_f/Q_GENERIC_SCHUR_REDUCTION_SOL.md:176-188`:

   > (Lg)_1=B_1g_h, (Lg)_i=A_i g_{i-1}+B_i g_h, 2≤i≤h,
   > where (A_i=L_{+1}) is the single step-1 branch and (B_i) is the sum of
   > the positive (L^infty_{+2}) and signed negative (L^infty_{-1}) tails.

3. An **independent reimplementation written from the paper**, sharing no code
   (`mpmath` vs Arb, different interpreter, different head/tail split
   `n_head=6` vs 4), `lane_g/EVENQ_CROSSVAL_KIMI.md:42-47`:

   > ```
   > (L_{s,±} g)_1 = Linf_{2,s} g_h ± Linf_{-1,s} g_h
   > (L_{s,±} g)_i = L_{1,s} g_{i-1} + Linf_{2,s} g_h ± Linf_{-1,s} g_h ,  2≤i≤h
   > ```

   cross-validated at q=12 to relative error 2.07e−30 against the tracked
   builder. Because the Hurwitz tail closure is exact, the deliberately
   different split point also checks head+tail recombination.

**The specialization.** Setting `h = κ = 3` in the row form of (2)/(3) gives
exactly the eight occurrences of §2.2, with `B_i = L^∞_{+2}(·)_3 + L^∞_{−1}(·)_3`
and `A_i = L_{+1}` in column `i−1` for `i = 2,3`, and no `A` term in row 1.
This matches the `f8_source_builder.py:108-114` unroll and the independent
`BLOCKS` constant, occurrence for occurrence (§5/V8).

**Why this is REDUCED and not PROVED.**

* **R-B2-1 (verbatim source).** The MMS PDF is **not in the repo**. There is no
  `tmp/pdfs/mms-0912.2236v2.pdf` and no MMS PDF in any worktree; the q=7
  receipt banked only the odd-q `pdftotext` line numbers (its line 49,
  `For q = 2hq + 3 > 5 we get`, is the eq.(34) heading). No even-q line number
  or page-quoted text was ever recorded. **I did not download the PDF**, since
  downloading is owner-authorized, not agent-authorized. Consequently this note
  quotes attestations *about* eq.(32), not eq.(32) itself. Closing this is one
  `curl` plus one `pdftotext` and is by far the cheapest remaining action in
  the whole lane.
* **R-B2-2 (chain length).** The binding chain is
  MMS eq.(32) → `zeta_cert_rosen_even.py:228-246` → hand-derived `BLOCKS`
  (`f8_certify_tb_blocks.py:11-29` says "hand-derived") → `f8_source_builder.py:108-114`.
  Links 2→3→4 are machine-checkable and checked (§5/V8); link 1→2 rests on
  attestations (1)–(3). q=7 closed the analogous link by quoting eq.(34)
  directly; q=8 has not.

Note that the q=8 chain carries one safeguard q=7 lacks: `f8_source_builder.py:141-164`
`validate_against_generic_builder` rebuilds at uniform factor 2.5 and compares
entrywise against `zeta_cert_rosen_even.build_reduced_matrix_ball`.

### B3 — Orthonormal basis, hypothesis H0. PROVED.

`H²(D(c,r))` is the Hardy space of the disc with inner product
`⟨f,g⟩ = (1/2π)∫₀^{2π} f(c+re^{iφ}) conj(g(c+re^{iφ})) dφ` (boundary values in
the usual non-tangential sense). In the normalized variable `u = (z−c)/r` the
map `f ↦ f(c+ru)` is a unitary from `H²(D(c,r))` onto `H²(𝔻)`, and
`e_{m}(z) = ((z−c)/r)^m ↦ u^m`. Since

    ⟨u^m, u^k⟩ = (1/2π)∫₀^{2π} e^{i(m−k)φ} dφ = δ_{mk},

`{u^m}_{m≥0}` is orthonormal, and it is complete in `H²(𝔻)` because every
`f ∈ H²(𝔻)` is the `H²`-limit of the partial sums of its Taylor series. Hence
`{e_{i,m}}_{i≤3, m≥0}` is an orthonormal basis of the orthogonal direct sum
`H`. Therefore:

* `P_N`, truncation to `m<N` in each summand, is the orthogonal projection onto
  the closed span, so `‖P_N‖ = 1` and `‖I−P_N‖ = 1`;
* `Σ_m |X[m,k]|² = ‖X e_k‖₂²` is Parseval in this basis;
* the `T[m,k]` of `Q8_OUTPUT_TAIL_SOL.md:97` — the `m`-th Taylor coefficient in
  `u` of `(T e_{j,k})(c_i + r_i u)` — is precisely `⟨T e_{j,k}, e_{i,m}⟩`.

This is exactly hypothesis **H0** of `SCHUR_SUBSTITUTION_DERIVATION_SOL.md:315-326`,
and it is now **discharged**, not inherited. Lemma 2.2 and inequalities
(2.2)–(2.6) of that note no longer rest on an unproved orthonormality
assumption. Note this is a statement about the *Hilbert structure*; it does not
by itself say the matrix is the right operator (that is B2) nor that the sup
bounds dominate (that is B5).

### B4 — Bounded evaluation functionals. PROVED.

For `f ∈ H²(𝔻)` with `f = Σ a_m u^m`, Cauchy–Schwarz gives, for `|v| < 1`,

    |f(v)| ≤ Σ|a_m||v|^m ≤ (Σ|a_m|²)^{1/2} (Σ|v|^{2m})^{1/2}
           = ‖f‖_{H²} (1−|v|²)^{−1/2}.

So point evaluation at `v` is bounded with norm `≤ (1−|v|²)^{−1/2}`, uniformly
on `|v| ≤ ρ < 1`. This is the same estimate the certified q=5 note records at
`lane_g/TB_R5_DETERMINANT_IDENTIFICATION.md:70` and the q=7 note at
`lane_f/Q7_R5_OPERATOR_BINDING_SOL.md:392-395`; it is reused, not rebuilt. The
coefficient functionals `f ↦ T[m,k]` are the Fourier coefficients in the
orthonormal basis of B3, hence norm-one.

Together B3+B4 give the composition step: if a branch maps the (enlarged)
source disc into the closed subdisc of the target disc of ratio `ρ < 1`, then
for `f ∈ H²(D_j)` the composite `f∘θ` is bounded on the source disc by
`(1−ρ²)^{−1/2}‖f‖`, so `L_s` maps `H` into the space of functions holomorphic
on the enlarged discs and continuous on their closures, with the sup norm
controlled by `‖·‖_H`. This is the `H → B` mapping used in B8.

### B5 — Norm domination. PROVED.

Let `f_k(u) := (T^{(i,j)} e_{j,k})(c_i + r_i u)`, holomorphic on `|u| ≤ θ` for
the θ of B6a. Parseval on the circle `|u| = θ`:

    Σ_{m≥0} θ^{2m} |T[m,k]|²  =  ‖f_k‖²_{L²(|u|=θ)}  ≤  ( sup_{|u|=θ}|f_k| )²  =  M_k(θ)².

At `θ = 1` this gives `‖T e_{j,k}‖₂ ≤ b_k`, i.e. the R2 receipt's
**boundary sup-norm** bounds are legitimate `ℓ²` column bounds — which is what
`block_hilbert_tail_bound` (`q8_schur_contour.py:224-239`) uses them as, and
what `Q8_OUTPUT_TAIL_SOL.md:126-133` asserts. Dropping `m<N` and using
`θ^{2m} ≥ θ^{2N}` on the rest gives the omitted-output row tail

    Σ_{m≥N} |T[m,k]|²  ≤  θ^{−2N} M_k(θ)².

So the domination direction required by clause (iii) holds, in the strong form:
the certificates bound a **larger** quantity (a sup on a circle) than the
Hilbert norm they are consumed as. There is no gap in this direction and no
constant is lost. The trace-norm propagation `(2.5)` of `Q8_OUTPUT_TAIL_SOL.md`
follows from the same identity plus `‖(I−P_N)D_θ^{−1}‖_op = θ^{−N}`, which uses
B3's orthogonality of the `e_{i,m}`.

Two caveats, both direction-safe: this proves the *inequality*, not that any
particular recorded numeric `b_k`/`M_k(θ)` was computed correctly (that is the
R2/L-OUT receipts' business, and `recorded_tail_checks_pass` is independently
**false**); and it needs holomorphy on `|u| ≤ θ`, which is B6a.

### B6a — Enlarged-disc weight holomorphy. PROVED. *(new)*

This is the piece the E1 probe's own scope line flags as missing:
`Q8_E1_ENLARGED_PROBE_RECEIPT.json` carries
`"scope": "OPEN: full E1 weight holomorphy, contour, R2/R3, Ks and MMS linkage remain open"`.
The q=7 E1 certificate carries a per-block field
`remaining_pole_cut_clearance_lower_bound`; the q=8 probe has no such field.
It is supplied here.

**Argument.** The enlargement rule is, verbatim from `q8_e1_probe.py:38-44`:

```python
    source_clearances.append(min(margins, key=lambda value: value.lower()).lower())
    enlargements.append(min(source_clearances[index] / arb(4), arb("0.15") * radius.lower()))
```

so for source disc `i`, `e_i = min(clearance_i/4, 0.15 r_i)` where
`clearance_i` is the minimum over **all** branch rows out of disc `i` of the
pole margin and the branch-cut margin. The recorded margins are distances from
the **base disc boundary**: `pole_margin = |c_i − pole| − r_i` and
`branch_cut_margin = c_i + nλ − r_i` (resp. `nλ − c_i − r_i`), per
`q8_tb_support.py:99-107`. Enlarging the disc radius by `e_i` therefore reduces
each margin by exactly `e_i`. Since `e_i ≤ clearance_i/4 ≤ margin_B/4` for
every branch `B` out of disc `i`,

    margin_B − e_i  ≥  margin_B − margin_B/4  =  (3/4) margin_B  >  0.

Hence every pole and every branch cut stays strictly outside the closed
enlarged disc, and every branch weight `w_{εn,s}` is holomorphic and single-
valued there on the principal sheet. Certified per row in §5/V4: all 16 rows
(8 pole + 8 cut) are strictly positive, worst enlarged margin

    ≥ 0.678884   (block 2→1, +1, head; branch θ₁)

and the recorded ratio `(margin − e)/margin` is `≥ 0.909` on every row — well
above the 3/4 the argument needs. In fact the binding term in the `min` is
`0.15 r_i` on all three discs (§5/V4), so the enlargement is exactly `0.15 r_i`
and the enlarged radius is exactly `1.15 r_i`.

**Corollary (even-q specific).** The Hurwitz closures need `Re(a) > 0` for the
parameter `a_±(z) = n ∓/± z/λ` on the enlarged output disc. Since
`branch_cut_margin` is exactly `λ·min Re(a_±)` on the base disc, B6a's margins
divided by λ give it. Certified directly in §5/V7 for all six tail families at
both `n₀` and the actual closure start `n₀+n_head` (`n_head = 4`,
`f8_source_builder.py:99-106`): worst

    Re(a) ≥ 0.809619   (block 3→3, −1, tail, n = 1).

This check has **no q=7 counterpart** and is where the even-q structure could
have failed: q=8's negative tails start at `n₀ = 1`, where the Hurwitz
parameter is closest to the origin, whereas q=7's start at `n₀ = 2`.

### B6b — Contraction into the base target disc. PROVED, with a provenance caveat.

The probe computes `ratio = sup_{∂D_i^e}|θ(z) − c_j| / r_j^e`, i.e. relative to
the **enlarged** target radius (`q8_tb_support.py:117`, called with
`enlarged_radii`). What B4's composition step needs is the ratio relative to the
**base** target radius, since the Hilbert space is `H²(D(c_j,r_j))`. Since
`r_j^e / r_j = 1.15` exactly on all three discs,

    ρ̂_H := max_B  sup_{∂D_i^e}|θ_B(z) − c_j| / r_j
          = 1.15 · ρ̂_e  ≤  1.15 × 0.765069  ≤  **0.879829  <  1**,

worst block `3→2, +1, head`. Per-block base-relative ratios are in §5/V5; the
six tail families all sit at `≤ 0.577`. Maximum modulus applies on the closed
enlarged disc by B6a, so the boundary sup bounds the disc sup.

Equivalently, in q=7's `(η, ρ̂)` bookkeeping, `η = r_i/r_i^e = 1/1.15 = 20/23 =
0.869565217…`, exactly the value `eta_max_upper_bound` in the q=7 receipt. For
reference the q=7 gate value is `ρ̂ = 0.915242`; q=8's `0.879829` is *smaller*.
I have **not** verified that q=7's `ratio_upper_bound` uses the same denominator
convention, so treat the numerical comparison as indicative only; the q=8
derivation above is self-contained.

**Provenance caveat (residual R-B6b-1).** The underlying arc-cover computation
is the *same* routine `tb.certify_block` that produced the accepted TB
certificate, run at `M=512`, `K_start=12`, `K_max=64`, 384 bits, and I
reproduced it bit-identically (§5/V9). But the artifact is
`status: "DIAGNOSTIC_ONLY"`, carries no `verdict`, no `immutable_inputs` hash
binding, no `η` field, and is per-source-disc rather than per-block; and
`Q8_GENERIC_CERTIFICATION_SOL.md:188` states flatly "**E1 enlarged-disc
contraction — OPEN.** No q=8 E1 receipt has been made." The *mathematics* of
B6b is proved from certified interval data; the *receipt grade* is not that of
q=5/q=7. Promoting it needs a gated, hash-bound, η-bearing E1 receipt, i.e. the
q=8 analogue of `F7_E1_ENLARGED_CONTRACTION_V2_RECEIPT.json`. That is a
mechanical run, not new mathematics.

One unrelated defect noticed in passing, reported not charged: the F1024 TB
receipt's per-term `pass` / `ratio_less_than_0_70` flags were evaluated at the
`q8_tb_support.py:17-18` default threshold 0.70, while its
`certification_verdict` string reads `PASS_RHO_LT_0.99`
(`q8_candidate_tb_cert.py` never overrides `THRESHOLD`, unlike
`f8_certify_tb_blocks.run()`). Harmless here — it is the *conservative*
direction and `ρ_* ≤ 0.696591 < 0.70` — but the two numbers in that one receipt
are not gated at the same threshold.

### B7 — Trace-class holomorphy. PROVED, conditional on B2.

Transplant of the referee-CONFIRMED q=7 estimate R1–R9
(`Q7_R5_OPERATOR_BINDING_SOL.md:527-688`), with the even-q substitutions
`κ: 5→3`, tail input disc `5→3`, negative tail start `n₀: 2→1`.

Set `Ω₀ = {Re s > 1/2}` and `Ω* = {Re s > 1/2} ∪ {Re s > 0, Im s > 1}` (open,
connected, disjoint from the real pole lattice `s = (1−k)/2`).

*Heads.* For the two head occurrences, B4+B6b give
`‖L_s e_{j,k}‖_H ≤ H_K ρ̂_H^k` on compact `K ⋐ Ω*`, with `ρ̂_H ≤ 0.879829`.

*Tails.* Every tail occurrence has input disc 3, so put
`a = −c_3/r_3`, `|a| = 1/2` **exactly** (§2.3). With
`b_{ℓ,B}(z) = (θ_{εℓ}(z) − c_3)/r_3`, so `|b_{ℓ,B}| ≤ ρ̂_H`, the identity

    b^k − a^k = (b − a) Σ_{t=0}^{k−1} b^{k−1−t} a^t

and `Re p_{ℓ,B}(z) ≥ Δ_B + (ℓ−n₀)λ ≥ μ_B ℓ`, `μ_B = min(λ, Δ_B/n₀) > 0`, with
`Δ_B > 0` the B6a enlarged lower bound for `Re p_{n₀,B}`, give

    |b_{ℓ,B}(z) − a| ≤ 1/(r_3 μ_B ℓ),
    |b_{ℓ,B}(z)^k − a^k| ≤ k ρ̂_H^{k−1} / (r_3 μ_B ℓ).

Split the tail column exactly into the `m=0` Hurwitz closure plus the centered
remainder:

    F_{B,k}(s,z) = a^k Z_{B,0}(s,z) + Σ_{ℓ≥n₀} w_{εℓ,s}(z)(b_{ℓ,B}(z)^k − a^k),
    Z_{B,0}(s,z) = (λ²)^{−s} ζ(2s, n₀ ± z/λ).

`Z_{B,0}` is holomorphic on a neighbourhood of `K × closure(D_i^e)` by B6a's
corollary (`Re(a) ≥ 0.809619 > 0`) and because `K` avoids the pole lattice, so
`A_{B,K} := sup|Z_{B,0}| < ∞`. With `|w_{εℓ,s}(z)| ≤ W_{B,K} ℓ^{−2σ_K}`,
`σ_K = inf_K Re s > 0` (finitely many small indices absorbed into `W_{B,K}`,
the `|arg p| < π/2` right-half-plane branch from B6a):

    sup_z |F_{B,k}(s,z)| ≤ A_{B,K} ρ̂_H^k + C_{B,K} k ρ̂_H^{k−1},
    C_{B,K} = (W_{B,K}/(r_3 μ_B)) Σ_{ℓ≥n₀} ℓ^{−(2σ_K+1)} < ∞.

Summing the eight occurrence constants into `A_K, C_K`, and using B5 to pass
from sup norm to `H²` norm, `b_k(s) := Σ_{j=1}^{3} ‖L_s^H e_{j,k}‖_H` satisfies

    sup_{s∈K} Σ_{k≥0} b_k(s) ≤ A_K/(1−ρ̂_H) + C_K/(1−ρ̂_H)² < ∞,

finite because `ρ̂_H ≤ 0.879829 < 1`. Hence the rank-one expansion
`L_s^H = Σ_{j,k} (L_s^H e_{j,k}) ⊗ e_{j,k}^*` converges locally uniformly in
trace norm; each column is holomorphic, so by the Banach-valued Weierstrass
theorem `s ↦ L_s^H` is trace-class holomorphic on `Ω*`.

The identity `F_{B,k}` holds first as an absolutely convergent branch sum on
`Ω₀` (where `2Re s + m > 1` for all `m ≥ 0`) and then by the Hurwitz
continuation on `Ω*`.

*Even-q soundness of the transplant.* The three places the q=7 text is
q-specific are all discharged: `|a| = 1/2` replaces `1/1.6` (§2.3, exact);
`n₀ = 1` for the negative tails is admissible by B6a's corollary; and the
`1/(1−ρ̂)`-type constants use `ρ̂_H = 0.879829` in place of q=7's `0.915242`,
i.e. strictly better. Conditional on **B2**, since the occurrence list is the
input.

### B8 — Determinant equality. REDUCED.

Let `B = ⨁_{i=1}^3 B(D_i)` (holomorphic in `D_i`, continuous on the closure,
sup norm), `H` as above; `B ⊂ H` continuously. B4+B6a+B6b give
`L_s^H : H → B`. Hence any nonzero eigenvalue's eigenvector lies in `B`
(`v = λ^{-1}L_s^H v ∈ B`), and by induction along a Jordan chain
(`v_r = λ^{-1}(Lv_r − v_{r−1})`) the whole chain lies in `B`; conversely
`B ⊂ H`. So the two realizations share nonzero spectrum with algebraic
multiplicity on `Ω₀`.

Both determinants are then the genus-zero canonical product over that common
spectrum, normalized to 1 at `t=0` in `det(1−tL)`, so no exponential
normalization factor survives at `t=1`:

* **Hilbert side.** Barry Simon, *Notes on infinite determinants of Hilbert
  space operators*, Adv. Math. 24 (1977), Theorem 4.2 / eq. (4.2), p. 258
  (determinant = product over eigenvalues with algebraic multiplicity) and
  Theorem 3.3 (analyticity for a trace-class-holomorphic family). Applies by B7.
* **Banach side.** MMS Theorem 4.10 (the full operator is nuclear of order
  zero, with meromorphic continuation, pole lattice `s = (1−k)/2`); MMS
  Lemma 5.1 (`P` commutes, eigenspaces invariant and complemented by `(I±P)/2`,
  so bounded restriction preserves order-zero nuclearity); then Grothendieck,
  *Résumé…*, Ann. Inst. Fourier 4 (1952), Théorème 8, pp. 108–109, identifying
  the Fredholm determinant of a `p`-nuclear operator (`p = 2/3`) with the
  genus-zero spectral product.

Equality on `Ω₀` then extends to `Ω*` by the identity theorem, `Ω*` being open
and connected and both sides analytic there.

**Residuals.**

* **R-B8-1.** MMS Theorem 4.10 and Lemma 5.1 are banked in the q=7 receipt at
  odd-q page locations (`Q7_MMS_PRIMARY_SOURCE_RECEIPT.md:47-51`, p. 20–21).
  They are stated for the **full** operator `L_s : B → B` and the `P`-reduction,
  which are parity-independent as written — but this has been checked only
  against the q=7 receipt's quotations, not against the even-q text. Same root
  cause as R-B2-1.
* **R-B8-2.** The conjugacy from the `P`-eigenspace restriction to the
  **reduced three-disc** eq.(32) operator is asserted, not proved here. q=7's
  note has the same shape and its referee accepted it; q=8's even-q reduction
  is a different map and has had no referee.
* **R-B8-3.** `Ω*` must contain the flagship pin box
  (`s ≈ 0.4252310423737965 + 4.345760788321986i`, half-width 1e−6, from
  `F8_R3B_RECEIPT.json`). It does — `Re s > 0` and `Im s > 1` — but the
  containment is stated here, not certified in a receipt, and the winding
  contour as a whole must be checked to lie in `Ω*`, which is the separately
  open continuous-contour gate.

**This is a genuine reduction, not a proof.** B8 stands on four printed results
(Simon Thm 4.2, Thm 3.3; Grothendieck Thm 8; MMS Thm 4.10, Lemma 5.1), all of
which are the *same* results the referee-CONFIRMED q=7 note stands on, plus
three residuals above.

---

## 5. Certified receipts

Script (scratchpad, not added to the repo):
`/private/tmp/claude-501/-Users-za-Documents-farey-hecke/d132431f-d2c6-4401-96d1-90f58d3026fb/scratchpad/hh_binding_check.py`.
Interpreter `/Users/za/.venvs/farey-rh/bin/python`, python-flint Arb/Acb ball
arithmetic, `ctx.prec = 384`. Inputs, by SHA-256:

```text
5f9cd3f9179c5b15539b3666bd3a2a3144995408648369dc1db6eda36f51d35c  Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json
7b0f0df79dd7c98ac4ede0673ef9fb189c093d6cb5ea24da470df70131799c96  Q8_E1_ENLARGED_PROBE_RECEIPT.json
```

| id | check | result |
|---|---|---|
| **V1** | λ₈ = 2cos(π/8) and √(2+√2) overlap; receipt λ ball contains it; `φ_0=−λ/2, φ_1=[1,1]_λ, φ_2=[1]_λ, φ_3=0` all inside the pinned balls | **PASS** (4/4) |
| **V2** | `c_i, h_i, r_i = a_i h_i` with `a=(10,4,2)` inside the pinned balls | **PASS** (9/9) |
| **V3** | `\|c_1\|/r_1 ≤ 1.065686`, `\|c_2\|/r_2 ≤ 1.457107`, `\|c_3\|/r_3 = 1/2` exactly (`c_3+h_3 ∋ 0`, `r_3−2h_3 ∋ 0`) | **PASS** |
| **V4** | `e_i ≤ clearance_i/4` on all 3 discs; enlarged radius `= r+e = 1.15 r` exactly; all 16 pole/cut rows have `margin − e > 0`, worst `≥ 0.678884`, worst ratio `≥ 0.909` | **PASS** (16/16) |
| **V5** | `ρ_* ≤ 0.696591`; `ρ̂_e ≤ 0.765069`; inflation `= 1.15`; `ρ̂_H ≤ 0.879829 < 1`; per-block base-relative ratios, tails all `≤ 0.577` | **PASS** (8/8) |
| **V6** | TB receipt block list: 8 occurrences, `exact_count_check=true`, `κ=3`, `h_q=3`, `even_q=true`, `derivation="MMS eq.(32) explicit q=8 list"` | **PASS** |
| **V7** | Hurwitz `Re(a) > 0` on the enlarged output disc, all 6 tail families at both `n₀` and `n₀+4`; worst `≥ 0.809619` | **PASS** (12/12) |
| **V8** | Structural unroll of `f8_source_builder.py:108-114` at `h=3` equals the independent `f8_certify_tb_blocks.BLOCKS` **as a set**, count 8 = 8 | **PASS** |
| **V9** | `q8_e1_probe.py` rerun to a scratchpad path reproduces the pinned receipt: `rho_hat_upper_bound` string-identical, `rows` identical, `rho_hat_less_than_one=true` | **PASS** |

Selected raw output:

```text
== V4  enlarged-disc pole / branch-cut clearance
  i=1: clearance/4=0.4749547311844426496731  0.15r=0.1188845008358304095034  e_i=0.1188845008358304095034
  i=2: clearance/4=0.1865340133541050325534  0.15r=0.06725122937519476771716 e_i=0.06725122937519476771716
  i=3: clearance/4=0.2589912287008195089142  0.15r=0.08117941502192954765996 e_i=0.08117941502192954765996
  V4 enlarged weight-holomorphy PASS (all 16 rows strictly positive): True
  worst enlarged margin >= 0.67888482404122536250  at block [2, 1, 1, False, False] (theta_1)

== V5  contraction ratios
  TB base-disc   rho_*     <= 0.696590428020637535884545   verdict: PASS_RHO_LT_0.99
  E1 enlarged    rho_hat_e <= 0.765068270705029641495394  (relative to the ENLARGED target radius)
  max enlarged/base radius inflation <= 1.15000000000000000000000
  rho_hat_H := rho_hat_e * inflation <= 0.879828511310784087719704  < 1 : True

== V7  Hurwitz parameter Re(a) > 0 on the ENLARGED output disc
    3→3, −1, tail        n=1  Re(a) >= 0.80961940777125589086  positive=True
  V7 PASS (all tail families, both n0 and n0+4): True

== V8  block-list agreement
  SETS EQUAL : True     COUNT : 8 8

== V9  E1 rerun vs pinned
  identical: True   rows identical: True   lt_one: True
```

Working tree, at the end:

```text
$ git status --porcelain research_notes/rh_goals_2026-08-14/lane_f \
                         research_notes/rh_goals_2026-08-14/lane_g/l_out
(empty)
```

---

## 6. Verdict

**REDUCED.**

The gate (HH) decomposes into eight sub-lemmas. Clauses **(i)** and **(iii)**
of the gate — the orthonormal-basis / projection / Parseval content (B3, B4)
and the norm domination (B5) — are **fully PROVED**, together with the
geometry (B1) and both enlarged-disc analytic inputs (B6a, B6b). Clause **(iv)**
splits: the trace-class holomorphy B7 is **PROVED conditional on B2**, and the
determinant equality B8 is **REDUCED** to Simon (1977) Thm 4.2/3.3,
Grothendieck (1952) Thm 8, and MMS Thm 4.10 / Lemma 5.1, with three residuals.
Clause **(ii)** — B2, the eq.(32) identification — is **REDUCED** to MMS
equation (32), p. 21, supported by a cold source audit, the abstract row form,
and an independent from-the-paper reimplementation cross-validated at q=12 to
2.07e−30, with two residuals of which the binding one is that **no verbatim
even-q source text is banked in this repo**.

**Net movement.** Hypothesis **H0**, which
`SCHUR_SUBSTITUTION_DERIVATION_SOL.md` had to inherit as CONJECTURAL and on
which every norm in the L-OUT receipt chain rests, is **discharged** (B3).
The enlarged-disc **weight holomorphy** that the E1 probe's own scope line
lists as open is **proved** (B6a), and with it the even-q Hurwitz-parameter
admissibility at `n₀ = 1` (B6a corollary) that has no q=7 analogue. The
remaining distance to a q=8 analogue of the referee-CONFIRMED q=7 Link 4b is
two residuals, both mechanical rather than mathematical: bank the even-q source
text, and re-emit E1 as a gated hash-bound receipt.

**Explicitly NOT claimed.** No q=8 determinant, Fredholm, Selberg, zeta,
scattering, resonance, winding, parity, automorphic, or LAW statement.
`full_tail_certified` remains `False` and this note does not bear on it. The
omitted-output tail, `recorded_tail_checks_pass` (independently **false**),
`K_s` nonvanishing and word/lattice identification, the common meromorphic
continuation and Selberg factorization, the four-edge winding, and the `N=104`
vs `N≥262` pin decision are all untouched and remain **OPEN**.

---

## 7. What a referee should attack

Ordered by expected yield.

1. **R-B2-1, the missing source text.** Fetch `https://arxiv.org/pdf/0912.2236v2`
   (expect SHA-256 `a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072`),
   `pdftotext -layout`, locate the **even-q** heading (`q = 2h_q + 2`) and
   equation (32) on p. 21, and quote the displayed rows verbatim. Then check the
   §2.2 table against them occurrence by occurrence — especially the **sector
   sign on the negative tail** and the **tail start `n₀ = 1` vs `2`**. If the
   even-q negative family actually starts at `n₀ = 2`, block 2/5/8 are wrong and
   B7's constants change. This single action is the highest-value item in the
   lane and I deliberately did not take it (downloading is owner-authorized).
2. **B6a's margin semantics.** The whole of B6a rests on the claim that the
   recorded `margin` is a distance from the **base disc boundary**, so that
   enlarging by `e` reduces it by exactly `e`. Verify against
   `q8_tb_support.py:99-107`. If `margin` were a center distance, the argument
   collapses.
3. **B6b's denominator conversion.** Verify that `q8_tb_support.py:117`
   (`ratio = sup / radii[j-1]`) is called by `q8_e1_probe.py` with *enlarged*
   radii in **both** slots, so that multiplying by 1.15 is the correct and
   only conversion to the base target radius. An error here is the difference
   between `ρ̂_H = 0.880` and `ρ̂_H = 1.012 > 1`, which would break B7 entirely.
4. **B7's absorbed constants.** `W_{B,K}` absorbs the finitely many indices
   with `μ_B ℓ < 1`, and `μ_B = min(λ, Δ_B/n₀)` uses the B6a enlarged lower
   bound `Δ_B`. Neither is computed numerically here. Confirm finiteness is
   genuine and not merely asserted, and that the `m=0` Hurwitz term is kept as
   one closed tail rather than replaced by `Σ ℓ^{−(2σ+1)}` (the error the q=7
   first referee caught).
5. **R-B8-2, the even-q reduction conjugacy.** MMS Lemma 5.1 gives the
   `P`-eigenspace decomposition of the *full* operator. The passage to the
   reduced 3-disc eq.(32) operator is a different map at even q than at odd q.
   It is asserted in B8 and has never been refereed at q=8.
6. **The `|c_j|/r_j > 1` hazard (§2.3).** Confirm that no tail family has input
   disc 1 or 2, in the source *and* in the receipt, and consider whether
   `q8_r2_local.py` should assert `q < 1` rather than rely on the row structure.
   Currently a misidentified row would produce a silently divergent `tau_in`.
7. **The 0.70/0.99 threshold inconsistency** in
   `Q8_TB_BLOCK_CERTIFICATES_F1024_RECEIPT.json` (§B6b). Harmless at
   `ρ_* ≤ 0.696591`, but it means two numbers in one receipt were gated
   differently; decide whether to re-emit.
8. **Grade inflation.** Check that nothing above is written as though B6b were
   receipt-grade. It is not: the artifact says `DIAGNOSTIC_ONLY`, and
   `Q8_GENERIC_CERTIFICATION_SOL.md:188` says no q=8 E1 receipt exists. The
   claim made here is that the *mathematics* follows from certified interval
   data, not that a certificate exists.

---

**READY FOR JUDGING**

---

## Dated addendum (2026-08-20, orchestrator): B2 source text banked

The missing verbatim MMS eq. (32) is now banked in-repo.  The PDF
(arXiv 0912.2236) was fetched and stored as
`lane_g/MMS_arxiv_0912.2236.pdf`; its SHA-256

```text
a10020bd084534dc60fc3e887958f1583f2fc115d567961b461df1a59b32e072
```

is byte-identical to the receipt recorded at
LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:382 and independently
re-fetched and re-hashed by the second LAW audit
(LAW_SECOND_AUDIT_REFEREE.md, "Sources I obtained myself").
`pdftotext -layout` pages 20–22, transcription (layout-cleaned; the
PDF's own column breaks distort subscript placement):

> Let g = (g_i)_{1<=i<=kappa_q} in B_{kappa_q}.  For q = 2h_q + 2 we
> get
>
> (L_{s,±} g)_1(z) = L^inf_{2,s} g_{h_q}(z) ± L^inf_{−1,s} g_{h_q}(z),
>
> (32)  (L_{s,±} g)_i(z) = L_{1,s} g_{i−1}(z) + L^inf_{2,s} g_{h_q}(z)
>        ± L^inf_{−1,s} g_{h_q}(z),   2 <= i <= h_q.

Consistency with the claims of §B2 of this note, checked against the
transcription: (i) even-q form q = 2h_q + 2 (q = 8 gives h_q = 3, three
discs); (ii) operator-occurrence count = 2 + 3(h_q − 1) = 8 for q = 8;
(iii) the negative-index tail family L^inf_{−1,s} is present (source of
the "negative tails from n0 = 1" structural difference vs odd q); (iv)
one continued-fraction family L_{1,s}, not two.  The surrounding
symmetry lemma (Lemma 5.1, P-commutation, same pages) matches the
even-q restriction convention this note uses.  B2's reduction is
therefore discharged to a banked, hash-pinned printed source; the cold
referee should re-derive the checker's row consumption directly against
this transcription (attack item 1 of §"what a referee should attack").
