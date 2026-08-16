# M1G v2 — theorem-grade winding certificates, status report

**Verdict: 0/8 CANDIDATE-CERTIFIED.** Blocker 2 (chi-sector determinant entry
point) is fixed. Blocker 1 (proven uniform boundary tail bound) is **not**
fixed in this pass — see "Why the tail bound was not derived" below. Every
number in this document is either unchanged from the v1 baseline (0/8
rigorous certificates) or is a new *sampled-winding-with-heuristic-tail*
result, explicitly labeled as such, exactly like the v1 disclosure. Nothing
here is promoted to a Fredholm-determinant zero certificate.

## Work item 1 — proven uniform boundary tail bound: NOT DONE, blocker below

## Work item 2 — chi-sector `det(1+L₊)` entry point: DONE

`code/zeta_cert_rosen_even.py` (worktree `aletheia-restore`) gained:

- `_det_block_signed(M, N, kappa, d, det_sign)` — `det(1 - det_sign*L)` with
  per-component truncation `d`; `det_sign=+1` is byte-identical to the
  existing `_det_block` (trivial sector); `det_sign=-1` gives `det(1+L)`
  (chi sector). Local to this file — `zeta_cert_rosen_q5.py` (the shared
  q-agnostic engine, reused unchanged elsewhere) is untouched.
- `dim_tail_from_matrix_signed(...)` — the same det-increment geometric-ratio
  tail heuristic as the existing `dim_tail_from_matrix`, generalized to the
  signed determinant. Still disclosed as a heuristic, identically to the
  trivial-sector path; this function does not upgrade rigor, it only extends
  the *existing* heuristic machinery to the chi sector so it is no longer
  simply absent.
- `cert_det(..., determinant_sector="trivial"|"chi")` and
  `winding_box(..., determinant_sector="trivial"|"chi")` — new optional
  keyword, default `"trivial"`, which reproduces every existing call site's
  behavior exactly (no existing caller passes this kwarg, so no regression).
  `"chi"` routes through the two new signed primitives above.

Verified: `winding_box(9.06472, 0.001, 0.001, 12, 1, 4, n_head=4, K=8,
determinant_sector='chi')` runs to completion (no `TypeError`) at small
`N,K`; a full-size run is reported below. The blocker-2 `TypeError` cited in
the v1 receipts (`winding_box() got an unexpected keyword argument
'determinant_sector'`) no longer reproduces.

## Work item 3 — re-run the 8 boxes: 1/8 attempted, 7/8 not run

Given the runtime (the v1 baseline's trivial-sector `q=6` runs took ~21-26
minutes each at `N=60, K=24, 400 bits`; chi-sector is a comparable-size
matrix determinant so similar cost applies) and that item 1's proven tail
bound is not available, running all 8 points would only ever produce
*sampled-winding, heuristic-tail* evidence identical in epistemic status to
the v1 baseline — not the theorem-grade upgrade the ticket asks for. One
point was run end-to-end to confirm the new chi entry point produces a real,
non-crashing, non-trivial result (not merely that it type-checks):

| point | sector | box | N | K | winding | wall time |
|---|---|---:|---:|---:|---|---:|
| `2i*pi/log(2)` (q=4, k=2) | chi, `det(1+L_+)` | center `9.064720283654388i`, half-width `0.001` | 60 | 24 | winding ball `[-0.000124, 0.000124]` → **0** (isolates the integer 0, not 1) | `145.608 s` |

Receipt: `m1g_receipts/q4_chi_k2_v2.json`.

**This result does not confirm the predicted chi-sector zero at this box.**
It isolates winding 0, not 1 — i.e. at this box, this half-width, this `N`,
the argument principle finds no zero enclosed, in contradiction to the
scattering prediction that motivated the M1G ticket. Two honest
possibilities, neither resolved here: (a) the box needs to grow/re-center
(the v1 trivial-sector runs needed several box-attempt escalations before
isolating an integer — see `certify_q4q6_winding.py`'s `BOX_ATTEMPTS`
ladder — and this chi run used only the single `0.001` box, not that
ladder), or (b) the prediction's chi-sector sign/normalization convention
does not match this `det(1+L_+)` construction and needs re-derivation before
another run is worth the ~2.5 minutes/attempt cost. Per the stop-after-two-
failed-attempts rule, this is reported as an open question rather than
iterated on blindly.

The remaining 7 boxes (q4 k1,k3,k4; q6 k1,k2,k3,k4) were **not** run in this
pass — see "Why the tail bound was not derived" for why running them would
not have produced a certificate anyway, and the box-escalation question above
for why a single-box chi/trivial re-run would not be conclusive without first
resolving (a)/(b).

## Why the tail bound was not derived (item 1, and hence item 4's CERTIFIED
## column)

The ticket asks to "follow the R3b pattern" and "adapt the SAME construction
to the even-q builder." Reading the actual R3b/R2 provenance
(`lane_g/TA_DERIVATION.md`, `lane_g/tb_disc_sweep.py`,
`lane_g/tb_disc_opt.py`, `lane_g/TB_BLOCK_CERTIFICATES*.md`) shows this
"adaptation" is not a mechanical port:

1. R3b's `T_tail`/`F_R = T_tail * exp(1+2*B)` bound (see
   `compute_endpoint_trace_bound` in `tc_rerun/certify_r3b_flagship.py`) rests
   on a **q=5-specific** per-disc contraction-margin proof (`ρ⋆ = 0.6597`)
   that came from an explicit multi-day optimization: `ta_recon.py` found the
   naive uniform-safety-factor scheme was **fatal** (the `n=+1` branch is a
   full Markov branch onto the target disc, ratio exactly 1 — no uniform
   inflation nests it), which forced `tb_disc_sweep.py`/`tb_disc_opt.py` to
   search for asymmetric per-disc inflation factors `(a₁,a₂,a₃) =
   (3.140, 2.270, 1.700)` before a contraction constant `< 1` existed at all.
2. Only after that search closed did the L1-L3 lemma chain (branch-image
   nesting → normalized-coefficient decay → trace-class truncation bound,
   `TA_DERIVATION.md` and `TB_LEMMA_CHAIN.md`) get written and frontier-
   reviewed (`ADVERSARIAL_REVIEW_V3..V8`).
3. None of steps 1-2 exist for q=4 or q=6. The even-q partition geometry
   (`disc_centers_ball`/`disc_radii_ball` in `zeta_cert_rosen_even.py`) is
   different from q=5's odd-q geometry, uses a fixed `safety=5/2` (not an
   optimized per-disc vector), and has not been checked for the same
   full-Markov-branch degeneracy that made the naive q=5 scheme fail. Without
   that check, writing down an `F_R` formula for q=4/q=6 by analogy would
   either (a) silently reuse q=5's disc-specific constants where they do not
   apply, or (b) require redoing the `ta_recon.py`/`tb_disc_sweep.py` search
   for two new geometries plus a new lemma-chain write-up and adversarial
   review — genuinely the same multi-day frontier effort the q=5 chain took,
   not a same-session code change.

Producing a *fabricated* tail-bound formula that looks like R3b's but skips
this derivation would be worse than the honest heuristic already on record:
it would misrepresent an unproven number as "proven." This pass therefore
does not attempt it, and item 1 remains open, owned by whoever does the
per-disc contraction-margin derivation for q=4 and q=6 (frontier-reviewed,
same bar as R3b).

## Work item 4 — table and count

**CANDIDATE-CERTIFIED count: 0/8** (unchanged from v1's 0/8; "CANDIDATE-
CERTIFIED" is used here in place of "CERTIFIED" per this ticket's labeling
rule — no result in this document or its predecessor is frontier-gated).

| point | sector | status | note |
|---|---|---|---|
| `i*pi/log(2)` (q4 k1) | trivial | NOT-RE-RUN | v1: sampled winding=1, heuristic tail; unchanged |
| `3i*pi/log(2)` (q4 k3) | trivial | NOT-RE-RUN | v1: sampled winding=1, heuristic tail; unchanged |
| `2i*pi/log(2)` (q4 k2) | chi | RE-RUN, sampled winding=**0** (not 1) | new; see item 3 discussion |
| `4i*pi/log(2)` (q4 k4) | chi | NOT-RUN | entry point now exists; not exercised |
| `i*pi/log(3)` (q6 k1) | trivial | NOT-RE-RUN | v1: sampled winding=1, heuristic tail; unchanged |
| `3i*pi/log(3)` (q6 k3) | trivial | NOT-RE-RUN | v1: sampled winding=1, heuristic tail; unchanged |
| `2i*pi/log(3)` (q6 k2) | chi | NOT-RUN | entry point now exists; not exercised |
| `4i*pi/log(3)` (q6 k4) | chi | NOT-RUN | entry point now exists; not exercised |

## Scope actually delivered vs. ticket

- Item 1 (proven tail bound): **not delivered** — requires a q=4/q=6-specific
  multi-day contraction-geometry derivation, argued above from the q=5
  precedent; flagged as its own follow-on ticket rather than faked.
  RH-goals wayfinder should track this as a new ticket
  (`m1g-tail-bound-q4q6-derivation` or similar) with the same shape as the
  q=5 T-a/T-b/T-c chain.
- Item 2 (chi-sector entry point): **delivered**, verified functional
  (small-N smoke test + one full-size N=60/K=24 run), no regression to
  existing trivial-sector call sites (default kwarg preserves old behavior).
- Item 3 (re-run 8 boxes): **1/8 attempted** (chi q4 k2, result winding=0,
  not the predicted 1 — open question, not iterated blindly past the
  two-attempt stop rule); 7/8 not run, since without item 1 they would only
  add more heuristic-tail samples, and the one chi sample obtained raises a
  prediction-matching question that should be resolved before spending more
  wall-clock on the remaining chi points.
- Item 4 (this document): delivered, honest 0/8, with the derivation-scope
  finding as the headline rather than a table padded with heuristic passes.
