# Adversarial review V3: T-b determinant-truncation chain

Date: 2026-08-14
Disposition: **THEOREM NOT CERTIFIED. Do not state a proven winding box from this chain.**

## Executive verdict

The seeded row-truncation objection is real against the proof **as written**: the engine takes a square principal section, while L3 calls an input-column truncation “exactly” that matrix. There is, however, a cleaner repair than paying for two tails: on a properly chosen Hilbert trace-class space, the finite-rank identity

\[
\det_H(I-LP_N)=\det_{P_NH}(I-P_NLP_N)
\]

allows comparison of `L` with `LP_N`, so the determinant error needs only the input-column tail. The present chain does not state or justify this identity, does not put the operator on the Hilbert space needed by its Schatten-norm argument, and does not certify the full endpoint trace norm required in the exponential prefactor.

More seriously, the V2 weight envelope is not an upper bound for the implemented tail columns. It replaces

\[
\left|\frac{\theta_n-c_j}{R_j}\right|
\quad\text{by}\quad
\frac{|\theta_n|}{R_j},
\]

dropping the nonzero target-disc center. Every `k≥1` analytically summed tail column contains a nondecaying-in-`n`, `m=0` Hurwitz term. Thus the certified-looking values `W^(≥1)=18.6358...`, `F`, and “minimal N=567” are not valid bounds. The winding runner then compounds this by checking only 192 boundary samples, not the closed boundary.

| item | verdict | bottom line |
|---|---|---|
| A1 row truncation | **GAP** | L3 identifies `LP_N` with `P_NLP_N` without the determinant identity. Direct comparison needs the missing row tail; a Fredholm/Sylvester identity can avoid it. |
| A2 hybrid trace norm | **GAP** | The finite-matrix column inequality is sound. Its use as a bound for the infinite `H∞` operator and for both perturbation endpoints is not. |
| A3 winding with inflation | **BROKEN** | The mathematical Rouché argument is standard, but the implementation certifies a sampled polygon, not the determinant on the whole contour. |
| A4 arc cover and weight branch | **SOUND**, with a documentation gate | The `z`-arc cover is genuine. The two power expressions agree on the certified half-planes, but the chain mislabels the negative-branch squared weight as literal \((\theta')^s\). |
| A5 `k=0` indexing | **SOUND, narrowly** | Column zero is the constant input mode and is retained for `N≥1`. This does **not** validate the V2 split: the `m=0` Hurwitz contribution occurs in every `k`-column. |
| A6 bookkeeping and \(\rho_*\) transfer | **GAP** | Current-radius block orientation/normalization is consistent, but a mixed-radius repair needs a new operator-space argument and new receipts; current T-c geometry is not exactly bound to the certified radii. |

The proof chain as a whole is **BROKEN** because at least two quantities advertised as certificates—`W^(≥1)` and the boundary winding—do not enclose the objects claimed.

## A1 — finite section versus input-column truncation

### What the implementation computes

The engine uses normalized input columns (k) and normalized output rows (m) ([engine basis](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:184)). It fills only (m,k=0,\ldots,N-1) ([matrix assembly](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:382)) and takes the determinant of the leading rows **and** columns ([`_det_block`](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:394)). The T-c wrapper does the same ([`tc_rerun.py`](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/tc_rerun.py:147)). This is (\det(I-P_NLP_N)).

L3 instead defines (L_N) by deleting input modes (k\ge N), i.e. (L_N=LP_N), and immediately says this is “exactly” the square matrix ([L3](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_LEMMA_CHAIN.md:41)). That operator equality is false. Directly,

\[
L-P_NLP_N=(I-P_N)L+P_NL(I-P_N),
\]

whereas L2/L3 bound only (L(I-P_N)). L2 explicitly admits that same-contour Cauchy extraction supplies no output-index decay ([L2 note](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_LEMMA_CHAIN.md:30)). No inspected receipt bounds \((I-P_N)L\).

A concrete finite-dimensional witness to the invalid *direct* norm reduction is

\[
P=\begin{pmatrix}1&0\\0&0\end{pmatrix},\qquad
L=\begin{pmatrix}0&\varepsilon\\M&0\end{pmatrix}.
\]

Then (PLP=0), the discarded-column norm is (\|L(I-P)\|_1=|\varepsilon|), but (\|L-PLP\|_1) contains the arbitrarily large row-tail entry (M), and

\[
\det(I-L)-\det(I-PLP)=-\varepsilon M.
\]

This does not refute the one-sided Fredholm repair below—the large (M) reappears in the endpoint trace norm—but it does refute the chain's unstated identification of the two truncations.

### Minimal repair: use the finite-rank determinant identity

Let (H) be a Hilbert space on which (L) is trace class and (P_N) the orthogonal projection onto the first (N) modes in each component. Put (U=L|_{P_NH}:P_NH\to H) and (V=P_N:H\to P_NH). Then (UV=LP_N), (VU=P_NLP_N|_{P_NH}), and the finite-rank Fredholm/Sylvester identity gives

\[
\det_H(I-LP_N)=\det_{P_NH}(I-P_NLP_N).
\]

Consequently one may compare (L) with (LP_N), for which

\[
L-LP_N=L(I-P_N),
\]

and no row tail is needed in the determinant *difference*. This lemma is absent from the chain and must be stated with its space, projection, determinant definition, and hypotheses. It is the cheapest repair if valid analytic column bounds can be rebuilt.

### Alternative repair: genuine two-radius row and column bounds

If the proof insists on comparing (L) directly with (P_NLP_N), it must certify both tails. A determinant-preserving same-space construction keeps the basis radii (R_i) but proves analyticity on larger output contours (S_i>R_i). Cauchy then supplies row decay

\[
q_{\rm row,i}^m=(R_i/S_i)^m,
\]

while the image bound on the new contour is

\[
q_{\rm col,B}=\sup_{|z-c_i|=S_i}\frac{|\theta_B(z)-c_j|}{R_j}.
\]

Both must be below one, and the weights must be re-enclosed on the (S_i)-contours. The current (\rho_*=0.6978014199\ldots) is certified only on the current (R_i)-contours ([T-b V2 result](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md:1)); it does **not** transfer unchanged to enlarged contours.

The suggested “smaller extraction contour (r_i<R_i), larger target analyticity disc” is useful for coefficient estimates, but care is essential. Shrinking the source contour while retaining the target denominator (R_j) preserves or improves the current image bound by maximum modulus. Yet a matrix with output basis (r_i) and input basis (R_j) represents a map between different radius spaces; it is left-scaled, not generally similar to the engine matrix, so its determinant is not automatically the target determinant. If both basis radii are shrunk, the denominator also shrinks and nesting may worsen or fail. This route needs an explicit two-space Fredholm factorization, not just changed constants.

The current certifier hardcodes one radius vector through the imported V1 geometry ([V2 run](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_tb_blocks_v2.py:505)); no existing receipt certifies inner/outer radii.

### Corrected-N estimate

There is **no theorem-grade corrected (N)** available from the present receipts: the W-v2 constant is invalid, the full trace norm is absent, and the quoted contour lower bound belongs to a different finite determinant. As planning arithmetic only, a noninterval geometry reconnaissance of same-space enlarged contours suggests a balanced effective rate around (q\approx0.84). Reusing the old (3.939054\times10^{-6}) margin merely as a scale and writing a corrected tail schematically as (Cq^N), the condition

\[
e^{1+T}Cq^N<3.939054\times10^{-6}
\]

gives:

| assumed full trace bound (T) | (C=10) | (C=100) | (C=1000) |
|---:|---:|---:|---:|
| 10 | 148 | 161 | 175 |
| 15 | 177 | 190 | 203 |
| 20 | 206 | 219 | 232 |

Thus `N ~ 160–230` is a reasonable **engineering range**, not a certificate. Every entry must be replaced by interval-certified row/column rates, weight constants, a true infinite trace norm, and a fresh contour computation at that same `N`.

## A2 — the hybrid trace norm and determinant perturbation theorem

For a finite Euclidean matrix (M), the claimed inequality

\[
\|M\|_1\le\sum_k\|Me_k\|_2
\]

is sound: decompose (M=\sum_k(Me_k)\otimes e_k^*\) and use the triangle inequality for the nuclear norm. The runner's `certified_t1` does compute the sum of certified finite-column Euclidean norms ([implementation](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/run_tc3_flagship.py:212)).

The infinite-operator use is not sound as written:

1. The chain declares (B=\bigoplus H^\infty(D_j)) ([setup](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_LEMMA_CHAIN.md:8)), then invokes singular values, polar decomposition, orthonormal columns, and (\ell^2) norms ([L3 double-prime](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_LEMMA_CHAIN.md:88)). Those are Hilbert/Schatten notions. On (H^\infty), normalized monomials are not an orthonormal Hilbert basis and finite (\ell^2) column norms do not upper-bound a Banach-space nuclear norm.
2. `certified_t1` sees only the first (N) output rows of each low input column, hence bounds (\|P_NLP_N\|_1), not (\|LP_N\|_1) and not (\|L\|_1). The missing high-output parts of low columns are exactly the row-tail problem.
3. The correct perturbation inequality is

   \[
   |\det(I+A)-\det(I+B)|
   \le \|A-B\|_1
      \exp\!\left(1+\max(\|A\|_1,\|B\|_1)\right).
   \]

   This is the form recorded in Bornemann, Eq. (4.1), citing the Seiler–Simon perturbation bound ([Bornemann, arXiv:0804.2543](https://arxiv.org/abs/0804.2543)). The simplification to (e^{1+\|L\|_1}) is valid if (A=-L), (B=-LP_N), (P_N) is orthogonal, and a genuine infinite (\|L\|_1) bound is known; then (\|LP_N\|_1\le\|L\|_1). None of those analytic-space obligations is currently discharged.

Repair: formulate the operator on (\bigoplus H^2(D_i)) (or another explicitly selected Hilbert space), prove the normalized monomials form the intended orthonormal basis, prove trace class and equality with the target transfer determinant, certify full (H^2)-norms of the low columns including output tails, and certify the high-column sum. With the Fredholm identity from A1, a valid bound on (\|LP_N\|_1+\|L(I-P_N)\|_1) gives a full endpoint norm.

There is also an off-by-one in L3-prime's use of a `k=1` constant. If `W_1` bounds the `k=1` column and each image ratio is at most \(\rho_*\), then

\[
\|Le_k\|\le W_1\rho_*^{k-1},\qquad
\sum_{k\ge N}\|Le_k\|\le \frac{W_1\rho_*^{N-1}}{1-\rho_*},
\]

not (W_1\rho_*^N/(1-\rho_*)), unless (W_1) was defined with an extra (1/\rho_*). The V2 method says it is the (k=1) image-radius majorant ([W-v2 method](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/W_ENVELOPE_CERT_V2.md:20)), while the code uses (\rho_*^N) ([tail formula](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/run_tc3_flagship.py:232)). This underestimates the tail by about (1/0.697802\approx1.433).

## Fatal defect outside the seeded A1: W-v2 drops the disc center

V1 correctly found that the absolute weight sum diverges for every box because (2\Re(s)<1) ([V1 verdict](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/W_ENVELOPE_CERT.md:3)). L3-prime then asserts that for (k\ge1), the image ratio obeys (\rho_n\le c/n) ([L3-prime](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_LEMMA_CHAIN.md:68)). That assertion is false for the implemented normalized basis.

The engine uses

\[
e_k^{(j)}(\theta_n(z))
=\left(\frac{\theta_n(z)-c_j}{R_j}\right)^k
\]

([single-block implementation](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:199)). For all infinite-tail blocks (j=3), (\theta_n(z)\to0), so

\[
\left|\frac{\theta_n(z)-c_3}{R_3}\right|
\longrightarrow \frac{|c_3|}{R_3}=\frac1{1.70}=\frac{10}{17}\approx0.588235,
\]

not zero. For any fixed (k\ge1), the absolute branch magnitudes therefore still behave as a nonzero constant times (n^{-2\Re(s)}), and their absolute sum diverges when \(\Re(s)<1/2\).

The T-b block receipt itself handles the center correctly: its deep bound is `image_radius + |c_j|` ([block certifier](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_tb_blocks_v2.py:69)). In contrast, W-v2 explicitly documents and implements

\[
|\theta_n|/R_j\le 1/(R_jd_n)
\]

([report](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/W_ENVELOPE_CERT_V2.md:24), [code](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_tb_weights_v2.py:198)). This is not a bound on (|\theta_n-c_j|/R_j\).

The engine exposes the omitted term algebraically. Every tail column is

\[
R_j^{-k}\sum_{m=0}^k {k\choose m}(-c_j)^{k-m}Z[m],
\]

so the (m=0) term (({-c_j}/R_j)^kZ[0]) is present for every (k) ([tail all-columns builder](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:309)). Closing only the (k=0) column does not remove it.

Repair: analytically close the (m=0) Hurwitz contribution for **every** (k), exploit its geometric (k)-decay ((|c_3|/R_3)^k), and certify the (m\ge1) remainder with its extra powers of (1/n). A practical scheme is to certify finitely many complete tail columns from the exact Hurwitz formula, then prove a uniform generating-function/geometric majorant for the remaining (k). Merely restoring `+|c_j|` inside an absolute branch sum does not work; it restores the divergence.

Until that repair is complete, all W-v2 (W^{(\ge1)}), (F), and minimal-(N) fields—including pin 1's (18.635804\ldots) and 567 ([receipt summary](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/W_ENVELOPE_CERT_V2_RECEIPT.json:29034))—must be treated as invalid.

## A3 — what the winding/Rouché proof must say, and what the code does

Let

\[
f(s)=\det(I-L_s),\qquad f_N(s)=\det(I-P_NL_sP_N),
\]

and let \(\Omega\) be the rectangular winding box. A correct proof is:

1. Prove (s\mapsto L_s) is a holomorphic trace-class family on a neighborhood of \(\overline\Omega\); hence (f) is holomorphic there. The finite determinant (f_N) is holomorphic.
2. Prove a **uniform** boundary bound
   \[
   |f(s)-f_N(s)|\le F(s)\le F_*\quad(s\in\partial\Omega).
   \]
3. Prove on the **entire closed boundary**, not at selected points,
   \[
   |f_N(s)|>F_*.
   \]
   Then (f_N) and (f) are nonzero on the boundary and Rouché gives the same number of zeros in \(\Omega\), counted with multiplicity.
4. Certify the winding of the continuous curve (f_N(\partial\Omega)) about zero. By the argument principle this is the zero count of (f_N), because there are no poles. If that integer is at least one, (f) has at least one zero in \(\Omega\).

Inflating a certified enclosure of `f_N(s)` by `F_*` in both real and imaginary directions is conservative: the resulting square contains the Euclidean `F_*`-disk and hence contains `f(s)`. But those enclosures must cover every `s` on every boundary segment, and their union/homotopy must avoid zero.

The runner generates 48 exact points on each edge ([`contour_points`](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/run_tc3_flagship.py:184)), evaluates a separate exact-(s) matrix at each point ([evaluation loop](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/run_tc3_flagship.py:330)), and checks the products of adjacent **endpoint** balls ([`certified_winding`](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/run_tc3_flagship.py:248)). There is no interval (s)-segment evaluation, determinant derivative/Lipschitz bound, adaptive subdivision gate, or argument-principle integral. The code's `theorem_grade` flag is therefore false as a matter of logic even if every sampled ball excludes zero ([flag](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/run_tc3_flagship.py:405)).

A concrete adversary is obtained from the 192 sample locations (s_j):

\[
p(s)=1+C\prod_j(s-s_j).
\]

Every sample is exactly (p(s_j)=1), so all point balls can be tiny and exclude zero, while a suitable (C) produces zeros and arbitrary excursions between samples. Endpoint safety cannot certify the intervening analytic curve.

Repair with one of: (i) interval-evaluate (f_N) over closed (s)-segments and subdivide until each connected image enclosure avoids zero with controlled argument; (ii) certify a determinant derivative bound and tubes joining point enclosures; or (iii) certify the argument-principle integral directly. Then apply the uniform (F)-inflation to those segment enclosures.

## A4 — (z)-arc coverage and branch-power consistency

The L1/T-b (z)-arc cover is genuine. `arc_ball` encloses each closed angle interval by hulling the endpoint values of sine/cosine and inserting every possible interior extremum at multiples of (\pi/2) ([implementation](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_tb_blocks.py:133)). All (M=512) arcs are traversed ([`contour_sup`](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_tb_blocks.py:162)); neighboring rectangles share their true endpoint. This is not point sampling. The receipt's positive pole and branch-cut margins cover all 11 blocks ([T-b branch table](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2.md:154)).

For weights, W-v2 evaluates

\[
\left(1/(\mathrm{denom}^2)\right)^s
\]

([code](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_tb_weights_v2.py:163)); the engine evaluates

\[
(\mathrm{denom}^2)^{-s}
\]

([engine](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:199)). On the certified right half-plane for (z+n\lambda), and after writing (z-n\lambda=-(n\lambda-z)) with (n\lambda-z) in the right half-plane, \(\mathrm{denom}^2\) never lies on the negative real axis. Hence principal `Log(1/x)=-Log(x)` applies and the two expressions agree for the actual geometry. The receipt would be clearer and safer if it evaluated the engine expression literally and emitted an explicit denominator-square cut gate.

One documentation correction is mandatory: for a negative branch \(\theta(z)=1/(z-n\lambda)\), the literal derivative is `-1/(z-nλ)^2`. The engine intentionally uses the MMS squared weight `((z-nλ)^2)^(-s)`, not the principal power of that negative derivative. Calling the weight \((\theta')^s\) in the lemma chain ([setup](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_LEMMA_CHAIN.md:11)) invites a branch error even though the inspected W and engine expressions match each other.

## A5 — the (k=0/k\ge1) split

The actual indexing claim is correct. The engine starts `powk=1` and appends it as column (k=0) before multiplying by the normalized input variable ([single-block all-columns](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:270)). The matrix retains (k=0,\ldots,N-1), so the discarded input-column tail starts at (k=N); for (N\ge1), column zero is not in (L(I-P_N)).

This narrow fact does not justify L3-prime's analytic split. The word “(m=0)” in the exact Hurwitz/binomial expansion is a summation index inside **every** input column (k), not the input column (k=0). Confusing those indices is the mechanism behind the W-v2 failure above.

The exploratory helper `tc_rerun.tail_radius` also uses (\rho^{N+1}) even though the discarded column begins at (N) ([helper](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/tc_rerun.py:243)). The current flagship runner does not use that helper; it uses (\rho^N), so this is a stale exploratory bug rather than the current off-by-one identified in A2.

## A6 — composition bookkeeping, \(\rho_*\), and source binding

At the current certified radii, the core block bookkeeping is consistent:

- A tuple `(i,j,...)` produces output rows in disc (i) and consumes input columns in disc (j).
- L1 evaluates `z` on the output/source contour `D_i` and measures \(\theta_B(z)\) in the target/input disc `D_j` ([T-b certifier call](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tb_certify/certify_tb_blocks_v2.py:45)).
- The engine uses the same normalization \((\theta_B-c_j)/R_j\) for the input basis and expands the result in \((z-c_i)/R_i\) ([engine](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/zeta_cert_rosen_q5.py:184)).

W-v2 calls its aggregation rows “source” rows and takes (3\max_i\sum_{B:i(B)=i}W_B). A column-wise proof would naturally group by the input component (j), but (3\max_i\) dominates the sum of all three output-row groups and therefore is conservative if the individual (W_B) values are valid. The fatal issue is not this orientation; it is that the deep (W_B) values are not bounds on the normalized columns.

The certified \(\rho_*\) transfers only with the exact radius-space statement proved. For a concentric smaller (z)-contour and unchanged target radius (R_j), maximum modulus gives no worse image ratio. For enlarged output contours, shrunken target denominators, or a new endomorphism space, it must be re-certified. A mixed-radius matrix must also be related to the original determinant, as explained in A1.

There are theorem-grade source-binding gaps even before changing radii:

1. T-b/W receipts certify the decimal multiplier `3.14` ([receipt](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TB_BLOCK_CERTIFICATES_V2_RECEIPT.json:2105)); `tb_disc_opt.json` stores `3.1399999999999997` ([JSON](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/tb_disc_opt.json:1)), and T-c converts that float back through `Decimal(str(value))` ([loader](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/tc_rerun.py:51)). Thus T-c does **not** use exactly the certified radius, despite its comment. The numerical difference is tiny; the missing identity assertion is the defect.
2. The flagship loader searches W-box records by a `box` key, while the detailed receipt records use `name`; it silently falls back to the first record ([loader](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/run_tc3_flagship.py:113)). Current ordering happens to make that pin 1, but it is not a robust binding.
3. `TA_DERIVATION.md` is stale: it still states a uniform `2.5` radius ([geometry](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TA_DERIVATION.md:4)) and claims a (\rho_*^m) output-row bound ([its L2](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/TA_DERIVATION.md:24)), directly contradicting the optimized radii and corrected no-(m)-decay L2.
4. `tc_rerun.observed_coefficient_C` explicitly derives an empirical row envelope from the computed finite matrix ([helper](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/tc_rerun.py:215)). It is reconnaissance, not a proof constant.

Repair: make T-c consume exact decimal radii from the certificate receipt, assert receipt schema/hash/value equality, select the named box without fallback, assert sector/sign semantics, and delete or clearly supersede the stale T-a formulas.

## The N=567 “crude fallback”

It is not a fallback certificate.

1. It is computed from the invalid W-v2 envelope, so its arithmetic premise is false.
2. The receipt obtains 567 by comparing against the `TC_PREP` fallback lower bound (3.939054\times10^{-6}), because no per-pin T-c output existed ([receipt provenance](/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/W_ENVELOPE_CERT_V2_RECEIPT.json:29132)). That lower bound was for a different finite determinant. A lower bound for (f_{48}) cannot simply be reused for (f_{567}); the boundary determinant must be recomputed/certified at (N=567), or related by another rigorous perturbation bound.
3. The actual runner permits only (N=128) or (160) ([CLI gate](/Users/za/Documents/farey-hecke/.worktrees/aletheia-restore/code/tc_rerun/run_tc3_flagship.py:485)). There is no executable (N=567) certificate path.
4. It shares the (H^\infty/H^2) space mismatch, invalid W tail, off-by-one normalization, point-sampled boundary, and source-binding defects.
5. It need not *intrinsically* share the row-tail defect if the proof adds the Fredholm/Sylvester identity and a valid full trace-norm bound. As the chain stands, that lemma is absent, so the linkage is still a gap.

## Minimal theorem-grade repair set

In dependency order:

1. **Freeze the operator and space.** State the exact (G_5), sign/sector, block list, principal power convention, and exact radii. Put the transfer operator on a specified Hilbert space such as \(\bigoplus H^2(D_i)\), or replace every Schatten argument by a valid Banach-nuclear one. Prove its Fredholm determinant is the intended zeta/resonance determinant.
2. **Add the finite-section linkage.** Prefer the finite-rank identity (\det(I-LP_N)=\det(I-P_NLP_N)), allowing a one-sided input tail. If this cannot be justified on the chosen space, certify both row and column tails using new outer-contour receipts.
3. **Replace W-v2.** Close the `m=0` Hurwitz term for every `k`, certify the `m≥1` remainder, fix the `k=1` normalization/off-by-one, and assert that the receipt's rho bound is below the rho used inside the W certifier.
4. **Certify the full perturbation prefactor.** Bound (\|L\|_1) (or both exact endpoints) on the infinite Hilbert space. Finite (P_NLP_N) column norms alone are insufficient.
5. **Certify the closed (s)-boundary.** Replace point sampling by interval segment enclosures or derivative-controlled tubes; certify nonvanishing and winding for the entire boundary.
6. **Recompute at one chosen N.** Produce a T-c receipt whose matrix dimension, determinant lower bounds, trace norm, (F), radii, block source hashes, W source, sector, and boundary cover all bind to that same run. No reuse of the (N=48) lower bound at another (N).
7. **Reconcile documentation.** Supersede the false (\rho^m) T-a statement and the ambiguous \((\theta')^s\) notation.

## Final risk statement

The single most dangerous defect is **the W-v2 center omission**. The row-truncation problem is visible and has a standard finite-rank determinant repair. W-v2 is more treacherous: it produces finite Arb intervals and a plausible (N=567), but it bounds the wrong expression. That is exactly the failure mode most likely to survive superficial “all intervals passed” review and turn a heuristic resonance box into a false theorem.

No finite (N)—128, 160, 567, or otherwise—is certified by the inspected chain.

## Audit scope and validation

Read in full: the requested T-b lemma chain; T-b V2 report and JSON receipt; W v1/v2 reports and both receipts; T-a; `certify_tb_blocks_v2.py` and its imported contour implementation; `tc_rerun.py`; `run_tc3_flagship.py`; and the imported matrix/tail engine `zeta_cert_rosen_q5.py`. Receipt JSON parsed completely, and recorded source hashes were checked against the current files. No certifier or runner was executed because those programs write outputs; this review was static and read-only apart from this report.
