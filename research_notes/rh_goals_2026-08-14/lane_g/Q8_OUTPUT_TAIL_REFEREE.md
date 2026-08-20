# Cold referee — q=8 omitted-output (row / projection) coefficient tail

Date: 2026-08-20.
Target: `research_notes/rh_goals_2026-08-14/lane_g/Q8_OUTPUT_TAIL_SOL.md`
(tracked; added by commit `b701cee` "Add q8 omitted-output tail bound note
(unrefereed)").
Referee: independent cold review. Did not write the target. No file under
`lane_f/` or `lane_g/` was edited; this note is the only file written. Nothing
was committed or pushed by the referee.

## Method (independence)

I did **not** run the target's probe (`<scratchpad>/outtail_probe.py`). I built
an independent oracle in **mpmath** (no python-flint, no repo engine) from the
Hurwitz-closed branch formula re-derived from scratch, and cross-validated it
against the repo engine before using it:

```text
$ python -c "... taylor_cols(name,4,64) vs q8_r3b_engine.build_q8_block_matrices_and_s_derivative(s,12,1,4,('10','4','2')) ..."
A2 max rel diff engine vs my mpmath DFT = 1.377e-14
A3 max rel diff engine vs my mpmath DFT = 8.767e-17
B1 max rel diff engine vs my mpmath DFT = 6.447e-17
B2 max rel diff engine vs my mpmath DFT = 8.232e-17
B3 max rel diff engine vs my mpmath DFT = 7.198e-17
```

So my oracle reproduces the engine's block matrix entries. Everything below
uses the oracle, not the target's script.

---

## 1. Per-claim verdicts

### (a) `b_k` is an output-circle boundary sup, and Parseval justifies the HS use — **CONFIRMED**

Quoted:

> So `b_k` is a **sup-norm bound on the boundary circle of the output disc**, not
> an l2 column norm.

Source read: `lane_f/q8_r2_local.py:165` builds
`arcs = [[tb.arc_ball(centers[i], radii[i], index, M) ...] for i in range(KAPPA)]`
(0-based, so `arcs[i-1]` is the circle of **output** disc `i`), and line 189
calls `exact_tail_columns_on_arc(s, z, centers[j-1], radii[j-1], lam, n0, neg, K_head)`
— the **input** disc supplies `c_j, r_j` only as normalization. I re-derived
`exact_tail_columns_on_arc` symbolically for both `neg` branches and it is
exactly

```text
f_k(z) = r_j^{-k} sum_m C(k,m) (-c_j)^{k-m} (-1/lam)^m lam^{-2s} zeta(2s+m, a0),
a0 = n0 + z/lam  (neg=False)  /  n0 - z/lam  (neg=True),
```

which is the Hurwitz closure of `sum_{n>=n0} (D^2)^{-s} ((argument-c_j)/r_j)^k`
with `D = z ± n lam`. Correct, with correct radius conventions.

Independent numeric confirmation that the receipt values really dominate the
true circle sups — **all eight blocks, all `k <= 16`, not a sample**:

```text
CHECK: receipt selected_column_bounds b_k  >=  true sup on |u|=1 ?
(1, 3, 2, False, True) tail    min(b_k/sup_k)= 1.0418  violations: NONE
(1, 3, 1, True,  True) tail    min(b_k/sup_k)= 1.0377  violations: NONE
(2, 1, 1, False, False) single min(b_k/sup_k)= 1.0976  violations: NONE
(2, 3, 2, False, True) tail    min(b_k/sup_k)= 1.0262  violations: NONE
(2, 3, 1, True,  True) tail    min(b_k/sup_k)= 1.0275  violations: NONE
(3, 2, 1, False, False) single min(b_k/sup_k)= 1.0694  violations: NONE
(3, 3, 2, False, True) tail    min(b_k/sup_k)= 1.0371  violations: NONE
(3, 3, 1, True,  True) tail    min(b_k/sup_k)= 1.0331  violations: NONE
```

This is a stronger check than the target ran: `selected_column_bounds` is
`min(direct_sups[k], tail_envelope(...))` (`q8_r2_local.py:206`), so the
**envelope** branch could in principle undercut the true sup. It does not.
Parseval `sum_m |T[m,k]|^2 = ||f_k||^2_{L^2(|u|=1)} <= b_k^2` then holds, and
`tail_trace_tail`/`single_trace_tail` = `sum_{k>=N}(A q^k + C k rho^{k-1})`
does dominate `sum_{k>=N} ||T e_k||_2`. The retroactive justification is real.

Two small imprecisions, non-load-bearing: (i) `exact_tail_columns_on_arc` is
used for the **six tail families only**; for the two single-branch blocks
(`A2`, `A3`) `b_k = weight_sup * rho^k` from the W/TB receipts — still a
sup-norm bound (verified above), but not by the mechanism §1.3 names.
(ii) §1.3 writes `selected_column_bounds[k] = b_k <= min(...)`; the code has
`=`, not `<=`.

### (b) The bound and its trace counterpart — **CONFIRMED (algebra re-derived independently)**

Quoted:

> `|| (I - P_N) T P_N ||_HS  <=  theta^(-N) * sqrt( sum_{k < N} M_k(theta)^2 )`

Re-derivation, done from scratch:

* (2.1) `T(I-P_N) + (I-P_N)T P_N = T - TP_N + TP_N - P_N T P_N = T - P_N T P_N`. ✓
* (2.2) `T(I-P_N) = sum_{k>=N}(Te_k)e_k^*`; each summand is rank one with trace
  norm `||Te_k||_2`. ✓
* (2.3) `sum_{m>=N}|T[m,k]|^2 = sum_{m>=N} theta^{-2m}(theta^{2m}|T[m,k]|^2)
  <= theta^{-2N} sum_{m>=0} theta^{2m}|T[m,k]|^2 = theta^{-2N}||f_k||^2_{L^2(|u|=theta)}
  <= theta^{-2N} M_k(theta)^2`. ✓ No radius-convention drift: the Parseval
  circle and the `M_k` sup circle are the same `|u| = theta`, and `T[m,k]` are
  the Taylor coefficients of the *same* `f_k`, extended by analytic
  continuation (legitimate under G1).
* (2.4) sum over `k < N`. ✓
* (2.5) `D_theta` is diagonal, hence commutes with `I-P_N`, so
  `(I-P_N)D_theta^{-1} D_theta T P_N = (I-P_N)T P_N` exactly;
  `||AB||_1 <= ||A||_op ||B||_1`; `||(I-P_N)D_theta^{-1}||_op = theta^{-N}`;
  `||D_theta T P_N||_1 <= sum_{k<N}||D_theta T e_k||_2` by rank-one
  decomposition; `||D_theta T e_k||_2^2 = sum_m theta^{2m}|T[m,k]|^2 <= M_k^2`.
  **No factor is lost at the HS→trace step.** ✓

The claimed splitting property "the second term touches only `k < N`" is
literally true of `(I-P_N)T P_N`. ✓

### (c) Admissibility, `theta_max = 1.2369`, binding block, pole clearance — **CONFIRMED numerically, MISLABELLED**

Quoted:

> `theta_max (all 8 blocks, rho < 1)   = 1.2369074008682055`
> **The binding block is `(3,2,1,False,False)` = `A3`**

My independent Möbius sweep (mpmath, exact image disc
`centre = ∓a/(a^2-R^2)`, `radius = R/(a^2-R^2)`, `a = c_i ∓ n lam`,
`R = theta r_i`, `n` swept to 400):

```text
rho_1(1.845)= 1.002117473    note 1.002117
rho_2(1.300)= 0.9971980121   note 0.997198
rho_3(1.235)= 0.9972089985   note 0.997209
theta_max(all 8, rho<1.0)  = 1.23690740087   note 1.2369074008682055
theta_max(all 8, rho<0.99) = 1.23005315906   note 1.230053
theta_max(all 8, rho<0.95) = 1.20206669138   note 1.202067

disc 1 theta*(rho=1)= 1.842809042 rate= 0.5426498  binding ((1,3,1,True,True), n=1)
disc 2 theta*(rho=1)= 1.301850480 rate= 0.7681374  binding ((2,1,1,False,False), n=1)
disc 3 theta*(rho=1)= 1.236907401 rate= 0.8084680  binding ((3,2,1,False,False), n=1)
```

Every number reproduces. The binding block **is** `(3,2,1,False,False)`.
The claim "the optimum sits at `rho_i(theta) = 1` in every case" is also
confirmed — `rate(theta)` rises on **both** sides of `theta*`:

```text
disc 3: theta=1.2169 rho=0.9710 rate=0.82176
        theta=1.2369 rho=1.0000 rate=0.80847   <- minimum
        theta=1.2569 rho=1.0297 rate=0.81919
```

so pushing `theta` to `rho_theta = 1` is legitimate and **no constant blows up
there** (§2.4's `S_2(N,1)` is finite; the polynomial factor is the whole cost).

Pole/branch-cut table, recomputed from the pinned TB geometry as
`theta < |c_i ∓ n lam| / r_i`: `(2,1,·)` → `1.194477583/0.448341529 = 2.664213562`;
`(3,2,·)` → `1.577161015/0.541196100 = 2.914213562`; `(1,3,2,F)` → `3.597056275`;
`(1,3,1,T)` → `3.397056275`; `(2,3,2,F)` → `6.785533906`; `(2,3,1,T)` →
`5.578427125`; `(3,3,2,F)` → `6.328427125`; `(3,3,1,T)` → `3.914213562`.
All eight match the note. The identification "branch cut ≡ pole clearance
because the discs are real-centred" is correct: `denominator^2 ∈ (-inf,0]` iff
`Re(denominator) = 0` iff `theta r_i >= |c_i ∓ n lam|`.

**Mislabelling (GAP).** §3.2 presents `theta_max = 1.2369` as if it were an
admissibility ceiling ("An admissible `theta > 1` demonstrably exists:
`theta_max = 1.2369` uniform, binding block `(3,2,1,False,False)`", §6).
`rho_theta < 1` is **not** an admissibility condition — §3.3 of the same note
argues at length that `rho_theta >= 1` is fine. The actual G1 admissibility
ceiling is `2.664`. `1.2369` is the *rate-optimal* `theta`, not the maximal
admissible one. I verified admissibility beyond it directly (see (d)).

### (d) 45 adverse numerical comparisons — **CONFIRMED as bounds, GAPS on the count and on §4.2's "rate check"**

**The bound itself holds, in 60/60 of my own independent adverse checks**,
using the *true* `M_k(theta)` sups (a stronger, harder test than the note's
`G_k(theta) <= M_k(theta)`), and including regimes the note never tested
(`theta = 2.4` and `theta = 2.60`, i.e. near the `2.664` pole ceiling):

```text
blk  theta     N   brute            bound            ratio    holds
A2  1.2369074   6         4.101215         22.9074     5.5855  True
A2  1.2369074  10        0.6518769        9.842692    15.0990  True
A2  1.2369074  14        0.1094501        4.209034    38.4562  True
A3  1.2369074   6         2.413411        13.68607     5.6708  True
A3  1.2369074  10        0.4894527        6.015132    12.2895  True
A3  1.2369074  14        0.1203762        2.598791    21.5889  True
B1  1.2369074  14     0.0005962904       0.6528141  1094.79    True
B2  1.2369074  14      7.091129e-7       0.1816122  256111.8   True
B3  1.2369074  14     0.0006866609       0.5909594   860.63    True
A2        1.6  14        0.1094501        6.459949    59.02     True
A3        1.6  14        0.1203762        8.527221    70.84     True
B3        1.6  14     0.0006866609      0.04340682    63.21     True
A2        2.4  14        0.1094501     1.639023e+9   1.50e10    True
A3        2.4  14        0.1203762       4849452.0   4.03e7     True
B3        2.4  14     0.0006866609      0.04736098    68.97     True
A2       2.60  14        0.1094501    8.222894e+16   7.51e17    True
A3       2.60  14        0.1203762     5.038924e+9   4.19e10    True
B3       2.60  14     0.0006866609       0.1871046   272.48     True
   (full 60-row table: 5 blocks x 4 thetas x N in {6,10,14}; all True)
```

My `brute` values reproduce the note's §4.1 table to 7 significant figures
(`A2 0.6518769`, `A3 0.4894527`, `B1 0.02038971`, `B2 1.207337e-4`,
`B3 0.01021735` at `N = 10`) from a completely separate code path. The note's
brute-force numbers are **real**. Note also that the constants *do* blow up as
`theta` approaches the pole ceiling (A2 bound `4.2` → `8.2e16` from
`theta=1.237` → `2.60`), independently corroborating that `rho_theta = 1` is
the right operating point.

**GAP 1 — the count.** §6 says "The bound survives **45** adverse numerical
comparisons against brute-force tail sums". §4.1 contains 5 + 5 = 10 and §4.2
contains 15 x 2 = 30; total **40**. The remaining 5 are §4.3's naive-rebuild
prefactor comparisons, which are not bound-vs-brute comparisons at all (and
one of them *disagrees* by construction). The count is inflated by 5.

**GAP 2 — §4.2's "rate check" is a tautology, not a receipt.** Quoted:

> **Rate check.** A2 at `theta = 1.235`: 5.31153 (N=8) -> 0.982935 (N=16), a
> per-step factor `(0.982935/5.31153)^(1/8) = 0.809866`. The predicted rate from
> the independent Mobius computation of §3.2 is `0.809717`. Agreement to
> 2e-4 ... This is the strongest single receipt in this note.

`5.31153` and `0.982935` are values of the **bound**, not of the operator. The
bound is *defined* as `theta^{-N} * sqrt(sum_{k<N} G_k^2)` with an
`N`-independent-to-first-order prefactor, so its per-step factor is
`1/theta = 1/1.235 = 0.809717` **by construction**; the `2e-4` residual is
merely the prefactor's drift. Nothing about the Möbius geometry is tested.
The *measured* decay of the true omitted-output tail is materially different —
from my own table, A2 brute `4.101215 (N=6) -> 0.1094501 (N=14)` gives
`0.63573` per step, and the note's own §4.2 brute column gives `0.6427` (A2),
`0.7027` (A3), `0.4208` (B1), `0.2807` (B2), `0.5057` (B3). Calling this "the
strongest single receipt in this note" is an overstatement of a self-check.
(The bound remains valid; only the claimed corroboration is empty.)

§4.3's hazard reproduction, on the other hand, I confirmed exactly with my own
code driving the unmodified engine at `theta = 1.2`, `N = 10`, `MBIG = 90`:

```text
A2 i=2 j=1  direct=4.006989   naive-rebuild=4.006989   equal6sf=True
A3 i=3 j=2  direct=2.481296   naive-rebuild=2.481296   equal6sf=True
B1 i=1 j=3  direct=0.9038963  naive-rebuild=0.9038963  equal6sf=True
B2 i=2 j=3  direct=0.2810194  naive-rebuild=0.2810194  equal6sf=True
B3 i=3 j=3  direct=0.6959273  naive-rebuild=0.6637150  equal6sf=False
```

Identical to §4.1/§4.3 to 7 s.f. The `i == j == 3` hazard is real, the
rebuild **under**-estimates (`0.66372 < 0.69593`), and the note's stated
remedy (enlarge the evaluation contour only, leave `centers[j-1]`/`radii[j-1]`
untouched) is the correct one. For `i != j` the rebuild is exactly equivalent
because `T'[m,k] = theta^m T[m,k]`, which is why four of five agree.

Hazard 2 (sweep `rho_theta` over all `n >= n_0`) is also real: my sweep finds
the worst `n` for `(1,3,1,True,True)` is `n = 399` (i.e. deep in the tail) at
`theta = 1`, but `n = 1` at `theta = 1.8428`.

### (e) Diagnosis: output dominates, `DEFAULT_N = 104` too small, `N >~ 200` — **CONFIRMED in substance, GAPS in one figure**

`tau_in` values recomputed by me from the pinned receipts through the
checker's own `tail_trace_tail`/`single_trace_tail`:

```text
104 [5.56204863545e-15 +/- 4.56e-27]     (note: 5.56204863545e-15)     MATCH
256 [3.44999455033e-39 +/- 3.48e-51]     (receipt tail_bounds "256")   MATCH
320 [3.04813402759e-49 +/- 1.29e-61]     (receipt tail_bounds "320")   MATCH
```

`DEFAULT_N = 104` confirmed at `q8_schur_contour.py:50`.

The `N` targets check out. With `tau_out(N) ≈ 1.19138 * 0.809866^(N-16)`
(`1.19138` = quadrature total of the note's own `theta = 1.235`, `N = 16`
column, `sqrt(0.982935^2+0.616562^2+0.209592^2+0.062286^2+0.158959^2) = 1.19138` ✓):

```text
1e-12 -> N = 16 + 27.8085/0.2108864 = 148.1   note: N >= 148 (HS)   ✓
1e-15 -> N = 16 + 34.7173/0.2108864 = 180.6   note: N >= 181 (HS)   ✓
1e-18 -> N = 16 + 41.6259/0.2108864 = 213.4   note: N >= 214 (HS)   ✓
```

**GAP 3 — `tau_out(104) ≈ 1e-6` is not derivable from the note's own data.**
Quoted:

> so `tau_out(104)` is roughly `1e-6`, eight orders **worse** than
> `tau_in(104)`.

Same extrapolation at `theta = 1.235` gives
`1.19138 * 0.809866^88 = 1.04e-8` (HS), and `~1.6e-7` after the note's own
`sum_k M_k / sqrt(sum_k M_k^2)` trace inflation (`≈ 15`, implicit in the
13-step HS→trace offset of §3.2's table). At the suboptimal `theta = 1.2` the
note cites: prefactor `= 1.62826 * 1.2^16 = 30.10`, times
`1.2^{-104} = 5.823e-9` (I verify that value), gives `1.75e-7` HS. None of
these is `1e-6`; the unexplained factor is ~60x (HS at `theta = 1.2`) to ~100x
(HS at the optimal `theta`). Consequently "eight orders worse" should read
about **6.3 orders (HS) / 7.5 orders (trace)**. The error is in the
conservative direction and does not change the qualitative conclusion, but a
figure presented as derived must be derivable. The `N >~ 200` headline is
unaffected — it rests on `0.809866`, which is correct.

### (f) The only missing piece is receipt L-OUT — **GAPS**

Quoted:

> This is the *same* computation `q8_r2_local.py` already performs, with the arc
> cover built at radius `theta_i * r_i` instead of `r_i`. It requires no new
> analytic machinery.

Structurally right — and I verified the mechanism (arc radius and `c_j, r_j`
are independent arguments; `arcs[i-1]` at `theta_i * r_i` with
`centers[j-1]`/`radii[j-1]` untouched is exactly the enlarged-contour sup).
But the §5.1 spec as written is **not executable**:

**GAP 4 — the L-OUT receipt schema is written for the wrong family, and the
binding block is in that family.** §5.1's example record is

```json
{ "block": [3,2,1,false,false], "A_theta_upper_bound": "...",
  "C_theta_upper_bound": "...", "q_upper_bound": "...", "rho_theta_upper_bound": "..." }
```

`[3,2,1,false,false]` is a **single-branch head** block, not a Hurwitz-closed
tail family. The pipeline has two envelope shapes — `q8_r2_local.py:181-184`
emits `weight_sup_upper_bound` + `center_included_image_ratio_upper_bound`
for `tail == False`, and `A`/`C`/`q`/`rho` only for `tail == True`; the
checker mirrors this split (`single_trace_tail` vs `tail_trace_tail`, and
`SINGLE_NAME_TO_BLOCK` vs `TAIL_NAME_TO_BLOCKS`). `A_theta q^k + C_theta k
rho_theta^{k-1}` (2.7) and the §5.2 consumption formula
`theta^{-N}(A_theta G_1(N,q) + C_theta S_1(N,rho_theta))` therefore do not
apply to `A2` or `A3` at all; those need `theta^{-N} W_theta G_1(N, rho_theta)`.
Since `A3 = (3,2,1,False,False)` is precisely the **binding** block, the note's
headline closed form does not literally cover the case that drives the rate.
(This is a specification defect, not a mathematical one — the single-branch
form is easier, and I supply it in §3 below.)

**GAP 5 — "(2.6)" is applied at the wrong level in §5.2.** §5.2.2 says
`"full_tau": None` becomes `input_tail_only + output_projection_tail`, "i.e.
(2.6)". But `input_tail_only` (`q8_schur_contour.py:351-358`) is the
*telescoped* Schur combination
`trace[B3] + a3 trace[B2] + a3 a2 trace[B1] + trace[A3] b2 + trace[A3] a2 b1 +
a3 trace[A2] b1`, whereas (2.6) is a single-operator inequality. The
substitution *is* sound — telescoping `X - X~` factor by factor requires the
**full** per-block defect `tau_in + tau_out` in each `trace[.]` slot with the
`hs[.]` factors unchanged, which is what §5.2.1 prescribes — but the note
never states that step, and the bare "i.e. (2.6)" is a category slip that a
later reader could take as licence to add the two totals in the wrong order.

**GAP 6 — §3.1's third sub-condition margin is quoted for the wrong theta.**
Quoted: "With `n_0 + n_head >= 5` and `theta r_i/lambda <= 0.53` at the theta
of §3.2". `0.53` holds at the **uniform** `theta = 1.2369`
(`1.2369*0.792563/1.847759 = 0.5305`). At §3.2's own disc-1 per-disc optimum
`theta_1 = 1.845` the slope is `0.7905`. The conclusion ("wide margin") is
still correct — the Hurwitz Taylor radius is set by `a_0 >= 5`, not by `1` —
but the quoted number does not cover the per-disc option the same section
recommends.

### (g) Scope honesty / LEDGER — **CONFIRMED, one stale sentence**

All six quotations in §1.1 are verbatim-correct against
`Q8_SCHUR_CONTINUOUS_CONTOUR_REPAIR_SOL.md:102-104`,
`..._REPAIR_REFEREE.md:25-27` and `:200-202`, and
`q8_schur_contour.py:382` / `:398` (the note cites `:381` / `:397`, an
off-by-one on the multi-line string start — cosmetic). The status block,
§3.4, §3.5 and §6 all keep the Hardy/Hilbert binding, E1, `K_s`, the Selberg
factorization, the four-edge winding and `recorded_tail_checks_pass` OPEN, and
correctly state that L-OUT has **not** been run. `full_tail_certified = False`
is still `False` in the code (`q8_schur_contour.py:395`), and no `lane_f/` file
was modified. **No overstatement of closure was found.**

One stale sentence: the note's last line says "No file was committed, pushed,
or edited; one new file was written." The note is now tracked, added by commit
`b701cee`. Most likely an orchestration commit made after the note was
written rather than an author error — flagged, not charged.

**Reproducibility defect.** §4.4 cites the probe as
`` `<scratchpad>/outtail_probe.py` `` — a literal placeholder pointing into an
ephemeral, git-ignored session directory. §3.2's "Computed (Arb, 256 bits)"
geometry sweep emits no receipt file at all. Every §3.2/§4 number in the note
happens to be correct (I reproduced all of them), but none of them is
auditable from the repo. Any future L-OUT lane must ship the sweep as a
tracked script plus a JSON receipt, not a scratchpad path.

---

## 2. Verdict table

| # | Criterion | Independent evidence | Verdict |
|---|---|---|---|
| a | `b_k` = output-circle boundary sup; Parseval justifies HS use | source read of `q8_r2_local.py:165,189,206`; symbolic re-derivation of `exact_tail_columns_on_arc`; 8/8 blocks x 17 k values, `min(b_k/sup_k) ∈ [1.026, 1.098]`, zero violations | CONFIRMED |
| b | (2.1)–(2.5) HS + trace bound | full re-derivation; commutation of `D_theta` with `I-P_N`; `||AB||_1 <= ||A||_op||B||_1`; no lost factor | CONFIRMED |
| b' | Splitting touches only `k < N`; `rho_theta = 1` optimum legitimate | (2.1) verified by expansion; `rate(theta)` minimum at `rho = 1` verified on both sides for all 3 discs; no constant blows up there | CONFIRMED |
| c | `theta_max = 1.2369074008682055`, binding `(3,2,1,False,False)`, pole limits 2.66–6.79 | mpmath Möbius sweep, `n` to 400: `1.23690740087`; all 8 pole limits recomputed and matched; `rho` at 1.845/1.300/1.235 matched to 7 s.f. | CONFIRMED (numbers) / GAP (called "admissibility"; true G1 ceiling is 2.664) |
| d | 45/45 adverse comparisons; predicted 0.809717 vs measured 0.809866 | 60/60 of my own checks hold with the *true* `M_k`, incl. `theta = 2.4, 2.60`; brute values reproduced to 7 s.f.; §4.3 hazard reproduced exactly | Bound CONFIRMED / GAP: count is 40 not 45; the "rate check" is tautological, true tail decays ~0.64–0.70 per step |
| e | `tau_in(104) = 5.562e-15`; `N >= 148/181/214`; `N >~ 200` | recomputed 104/256/320 through the checker's own functions — exact match; all three `N` targets re-derived | CONFIRMED / GAP: `tau_out(104) ≈ 1e-6` and "eight orders" are ~1e-8 (HS) / ~1.6e-7 (trace) and ~6.3/7.5 orders |
| f | Only L-OUT is missing; a computation, not a lemma | mechanism verified (`c_j, r_j` independent of arc radius); B3 rebuild hazard reproduced | GAPS: §5.1 schema written for the wrong envelope family — and that family contains the binding block; §5.2 "i.e. (2.6)" is a level slip |
| g | Scope honesty / LEDGER | all 6 quotations verbatim; `full_tail_certified` still `False`; no `lane_f/` edit; git shows only the note added | CONFIRMED / stale "not committed" line; probes unreproducible |

**Nothing is REFUTED.** The central mathematics — (2.1)–(2.5), the Parseval
reinterpretation of `b_k`, the `theta` geometry, the admissible `theta > 1`,
the binding block, and the `N >~ 200` cost finding — survives independent
re-derivation and independent numerics.

## VERDICT: GAPS NOT REFUTED.

The derivation is correct and the headline numbers are all independently
reproduced. Six gaps, none fatal, all in the presentation/spec layer:
(1) `theta_max = 1.2369` mislabelled as an admissibility rather than a
rate-optimality bound; (2) "45" adverse comparisons is 40; (3) §4.2's rate
check is a tautology billed as the note's strongest receipt; (4)
`tau_out(104) ≈ 1e-6` / "eight orders" is off by ~1.5–2 orders in the
conservative direction; (5) the §5.1 L-OUT schema uses the tail-family key set
for a single-branch block and omits the single-branch closed form entirely,
which is the form the **binding** block needs; (6) §3.1's `0.53` slope margin
is quoted for the uniform `theta` only. Everything remains conditional on the
separately-OPEN "Exact q=8 MMS-to-Hardy/Hilbert operator, basis, and norm
binding", which this note does not and does not claim to close.

---

## 3. Executable spec for receipt L-OUT

Corrected for GAP 4 and GAP 5. This is what a compute lane should run.

### 3.1 What to run

New script `lane_f/q8_r2out_local.py`, a copy of `q8_r2_local.py` with **one**
structural change and one addition. Do **not** edit `q8_r2_local.py`.

* **Change.** Build the arc cover at the enlarged radius:
  `arcs[i] = [tb.arc_ball(centers[i], THETA[i] * radii[i], index, M) ...]`.
  `centers[j-1]` and `radii[j-1]` passed to
  `exact_tail_columns_on_arc(s, z, c_j, r_j, ...)` and to
  `direct_head_first_moment_sup(..., r_j, ...)` **must stay unscaled**. Any
  route that rebuilds geometry by scaling `factors[i-1]` is **rejected**: it
  silently rescales the input basis for `B3` (`i == j == 3`) and
  under-estimates by 4.6% at `theta = 1.2, N = 10` (`0.6637150` vs
  `0.6959273`, reproduced above).
* **Addition.** Emit per block a certified G1 record and a certified
  `rho_theta` from the exact Möbius image (below).

### 3.2 Parameters

```text
pin            s = 0.4252310423737965 + 4.345760788321986 i, half_width 1e-6
factors        ("10","4","2")   (pinned F1024; must reproduce the TB centers/radii)
sign           1
n_head         4
ctx.prec       384
M              512   (arc cover; same as the R2 receipt)
K_head         16    (same as the R2 receipt)
theta          UNIFORM theta = 1.2 is the recommended production value.
               1.2  gives rho_theta <= 0.87 on every block (comfortable margin,
                    rate 0.8333)
               1.2369074008682055 is the rate optimum (rate 0.80847) but sits
                    exactly at rho_theta = 1 -- do NOT pin the optimum; pin
                    1.230 (rho < 0.99, rate 0.8130) if the extra rate is wanted.
               Per-disc thetas (1.84, 1.30, 1.23) are permitted and better
               (rates 0.543/0.769/0.808) since D_theta is block-diagonal on the
               OUTPUT side only; if used, re-check the Hurwitz slope
               theta_1 r_1 / lambda = 0.79 < a_0 = 5. RECORD which was used.
N targets      104 (the current pin, expected to FAIL the 1e-15 target),
               181, 200, 214.
```

### 3.3 Required receipt content — `Q8_R2OUT_F1024_THETA_RECEIPT.json`,
schema `q8-r2out-local/v1`

Per block, **split by family exactly as `q8_r2_local.py` does**:

* `tail == True` (the six Hurwitz families, all with `j == 3`, `q = 0.5`):
  `A_theta_upper_bound`, `C_theta_upper_bound`, `q_upper_bound`,
  `rho_theta_upper_bound`, `selected_column_bounds_theta` (`K_head + 1`
  entries), each an Arb `.upper()` string.
* `tail == False` (`A2 = (2,1,1,F,F)`, `A3 = (3,2,1,F,F)` — **including the
  binding block**): `weight_theta_sup_upper_bound`,
  `rho_theta_upper_bound`, `selected_column_bounds_theta`. The consumption
  formula for these is `theta^{-N} * W_theta * G_1(N, rho_theta)` (trace) and
  `theta^{-N} * W_theta * sqrt(G_2(N, rho_theta))` (HS) — **not** the
  `A q^k + C k rho^{k-1}` form.
* `theta_exact_string`, and a `geometry` block carrying the **unscaled**
  `centers` / `source_radii` (so the checker's overlap test at
  `q8_schur_contour.py:295-318` applies unchanged).
* `holomorphy_gate`: `pole_clearance_pass`, `branch_cut_clearance_pass`
  (recomputed at `theta_i * r_i`, i.e. `theta_i < |c_i ∓ n_0 lam| / r_i`),
  `deep_tail_d_lower_bound` (`d = first_n*lam ∓ c_i - theta_i*r_i > 0`),
  `hurwitz_slope_upper_bound` (`theta_i * r_i / lam`, must be `< a_0`).
* `rho_theta` provenance: computed from the exact Möbius image
  `centre = ∓a/(a^2-R^2)`, `radius = R/(a^2-R^2)`, `a = c_i ∓ n lam`,
  `R = theta_i r_i`, **swept over all `n` from `n_0` up to at least 400** for
  the tail families. Sweeping only `n = n_0` is a known failure mode: the
  worst `n` for `(1,3,1,True,True)` is `n = 399` at `theta = 1` but `n = 1` at
  `theta = 1.84`.
* `TB_sha256`, `W_sha256`, engine source path — bound exactly as the R2
  receipt does.

### 3.4 Pass / fail

PASS requires **all** of:

1. `theta_i > 1` strictly, for every disc, recorded exactly.
2. Every `holomorphy_gate` field true, with `pole_clearance` margins strictly
   positive at the enlarged radius.
3. `rho_theta_upper_bound` in the receipt is **reproduced independently by the
   checker's own Möbius computation** (not trusted from the receipt).
4. Self-consistency: `selected_column_bounds_theta[k] >=`
   the direct enlarged-arc sup for every `k <= K_head` (the receipt's own
   envelope must not undercut its own direct sups), and
   `selected_column_bounds_theta[k] >= selected_column_bounds[k]` from the
   pinned R2 receipt (monotonicity in `theta`; a violation means the contour
   was not actually enlarged).
5. `output_projection_tail(N)` finite, and `full_tau = input_tail_only +
   output_projection_tail` computed with the output tail substituted into
   **each** `trace[.]` slot of the existing telescoping at
   `q8_schur_contour.py:351-358`, the `hs[.]` factors unchanged. State this
   substitution explicitly in the note that accompanies the receipt; it is the
   step (2.6) does not by itself license.
6. Regression: at `N = 104` the run is expected to report
   `full_tau ~ 1e-7` — i.e. **worse** than the `1e-15`-class `input_tail_only`.
   A run that reports `full_tau <= 1e-14` at `N = 104` is a **red flag**,
   not a success: it means the output term was dropped or mis-scaled.
7. `full_tail_certified` flips to `true` only if 1–6 all hold; otherwise the
   fail-closed path at `q8_schur_contour.py:717-721` / `746-790` stands.

Independent adverse regression the lane should also run, so the receipt is
checked against the operator and not only against itself: for each of the five
assembled blocks and `N in {6, 10, 14}`, verify
`theta^{-N} sqrt(sum_{k<N} M_k(theta)^2) >= sqrt(sum_{k<N} sum_{m>=N} |T[m,k]|^2)`
with `T` from the **unmodified** `q8_r3b_engine`. I ran exactly this at
`theta in {1.2369074, 1.6, 2.4, 2.60}`: 60/60 hold.

### 3.5 What L-OUT still does NOT close

The Hardy/Hilbert operator/basis/norm binding, E1 on the enlarged disc, `K_s`
nonvanishing and word/lattice identification, the Selberg
determinant/zeta/scattering factorization, the four-edge winding, and the
independently-false `recorded_tail_checks_pass` gate. L-OUT closes one gate of
six.

**READY FOR JUDGING.**
