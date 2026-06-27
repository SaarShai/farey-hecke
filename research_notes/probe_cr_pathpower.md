# Probe: crossing numbers of path powers cr(P_n^k) — Conjecture (Zheng 2009)

Date: 2026-06-27. Goal: attempt a genuine NEW math fact (settle/refute a small open
case of Zheng's conjecture, or improve a bound) via EXACT crossing-number computation,
with independently-checkable witnesses. READY FOR JUDGING.

Status legend: **KNOWN** (web-verified literature) / **COMPUTED** (this session, with witness)
/ **UNVERIFIED**.

---

## 1. Exact statements (web-verified)

Source: K. Clancy, M. Haythorpe, A. Newcombe, *A survey of graphs with known or bounded
crossing numbers*, arXiv:1901.05155v2 (Australas. J. Combin.), section on powers of paths.
Primary: W. Zheng, X. Lin, Y. Yang, G. Yang, *On the Crossing Numbers of the k-th Power of
P_n*, Ars Combinatoria 92:397–409, 2009 (DBLP ZhengLYY09).

**Definition.** The survey *text* says "P_n on n+1 vertices … P_n^k same vertex set, edge ab
iff dist_{P_n}(a,b) <= k." HOWEVER the stated exact values force the operational convention:

> **CONVENTION (pinned by anchors, COMPUTED):** P_n^k is the graph on **n vertices**
> {0,…,n−1} with edge {a,b} iff 0 < |a−b| <= k.
> Anchors: cr(P_6^5)=3 = cr(K_6); cr(P_7^6)=9 = cr(K_7); cr(P_8^7)=18 = cr(K_8).
> Each holds because when k >= n−1 the graph is complete K_n, and cr(K_6)=3, cr(K_7)=9,
> cr(K_8)=18 (Guy, proven). The survey's "n+1 vertices" phrasing is misleading; the
> subscript n equals the vertex count. (Verified by direct construction below.)

**Theorem 55 (Harary–Kainen 1993).** cr(P_n^4) = n−4 for n>=5. (k=4 fully solved.)

**Theorem 56 (Harary et al. 1999).** For n>=6: **2n−9 <= cr(P_n^5) <= 4n−21.** (lower bound)

**Theorem 57 (Zheng et al. 2009) — upper bounds.** For n>k>=5:
```
cr(P_6^5)=3, cr(P_7^5)=6, cr(P_8^5)=9,  cr(P_n^5) <= 4n−23  (n>=9);
cr(P_7^6)=9, cr(P_8^6)=15, cr(P_9^6) <= 22, cr(P_n^6) <= 8n−51 (n>=10);
cr(P_8^7)=18, cr(P_9^7) <= 30, cr(P_10^7) <= 42, cr(P_11^7) <= 57,
                               cr(P_n^7) <= 15n−109 (n>=12).
```
**Conjecture 58 (Zheng et al. 2009)** [= "Conjecture 2.48" in the prompt's survey numbering]:
**all upper bounds in Theorem 57 hold with equality.**

OPEN (UB only, equality conjectured): the P_n^5 family (n>=9), P_9^6 and the P_n^6 family
(n>=10), and P_9^7, P_10^7, P_11^7 and the P_n^7 family (n>=12).
Smallest fully-open exact value: **P_9^6 (conj 22)** and **P_9^7 (conj 30)**.

Graph sizes (COMPUTED, code/cr_probe/exact_cr.py::pnk_graph):
```
P_9^5: 9 v, 30 e (conj 13)   P_9^6: 9 v, 33 e (conj 22)    P_9^7:  9 v, 35 e (conj 30)
P_10^5:10 v,35 e (conj 17)   P_10^6:10 v,39 e (conj 29)    P_10^7:10 v,42 e (conj 42)
                             P_11^6:11 v,45 e (conj 37)    P_11^7:11 v,49 e (conj 57)
```

---

## 2. Exact computation

### 2a. Independent exact solver (validated)
`code/cr_probe/exact_cr.py` — planarization-search exact crossing number: enumerate sets of
crossing pairs, realize each as a planarized multigraph (dummy degree-4 vertices, per-edge
crossing order via backtracking), test planarity with networkx `check_planarity`. EXACT but
exponential; usable only for tiny cr.

**VALIDATION (COMPUTED):**
- K_5: cr = 1 ✓ (known 1).
- P_6^5 (= K_6): exhausts all C(45,2)=990 two-crossing sets (none realizable ⇒ cr>2), finds a
  realizable 3-crossing set ⇒ **cr(P_6^5)=3 ✓** (= known cr(K_6)=3). Witness crossing pairs:
  `{(0,1)×(2,3), (0,4)×(2,5), (1,5)×(3,4)}`.

Wall: cr=3 needs ~138k subset tests; cr=6 (P_7^5) needs C(150,6)≈1.4e10 — infeasible. The
brute-force exact route does NOT reach any open case (all have cr >= 13).

### 2b. Online exact ILP (crossings.uos.de, "Crossing Number Web Compute")
KNOWN-LIVE (2026, mid-migration). OGDF + Abacus branch-and-cut-and-price on a Kuratowski-
subgraph ILP; emits machine-verifiable formal proofs (Chimani–Wiedera). Backend = free CLP
(slower than CPLEX), **1 GB memory limit**. Submission = web form at /job/new requiring
username, affiliation, and **email confirmation** of each request; input formats GML/DOT/
GraphML/etc.
**Not used this session:** the email-confirmation handshake cannot be completed autonomously,
and submitting under a real identity without consent is inappropriate. The dense open targets
(33–49 edges, conj cr 22–42) are also near/beyond the practical reach of the free-CLP/1 GB
configuration. → This is a recommended NEXT STEP for a human operator (see §5).

### 2c. Straight-line (rectilinear) upper-bound search — VALIDATED tool
`code/cr_probe/ub_fast.py` — simulated annealing over vertex coordinates in R^2, incremental
crossing count, every reported count independently rechecked from scratch (and re-checkable by
anyone via `code/cr_probe/check_witness.py n k '<coords-json>'`). A straight-line drawing with
c crossings proves cr(G) <= c (since rectilinear cr >= topological cr). VALIDATED — hits the
true minima as straight-line drawings:
- P_6^5 (K_6): **3** ✓ (= cr 3), rechecked.
- P_7^6 (K_7): **9** ✓ (= cr 9), rechecked.
- P_7^5: **6** ✓ (= cr 6).  P_8^6: **15** ✓ (= cr 15).
- P_8^7 (K_8): **19** — correctly = rcr(K_8)=19 > cr(K_8)=18, demonstrating the rectilinear gap.

**P_9^6 (smallest fully-open exact value, COMPUTED):** straight-line search finds a drawing with
**exactly 22 crossings**, independently recomputed = 22 by the separate `check_witness.py`
(witness: `code/cr_probe/witness_P9_6_ub22.json`, also `witness_P9_6_drawing.svg`). So this
session gives a checkable, reproducible proof that **cr(P_9^6) <= 22 AND rcr(P_9^6) <= 22**,
realized by an explicit straight-line drawing. This independently corroborates Zheng's
(topological) UB of 22 and additionally shows it is achievable rectilinearly. The search did
NOT find any drawing below 22.

CAVEAT (decisive): straight-line gives the RECTILINEAR crossing number, which for these graphs
is **>= cr and often strictly >** (e.g. rcr(K_8)=19 > cr(K_8)=18). So this tool can only
(i) re-confirm a small value when rcr=cr, or (ii) **refute the conjecture only if it finds a
drawing strictly below the conjectured value** — it cannot prove the conjecture, and is not
expected to beat Zheng's topological construction.

---

## 3. Comparison vs Harary / Zheng / Conjecture

- **k=5** (Harary 1999 LB 2n−9; Zheng conj-UB 4n−23): gap grows linearly — n=9: [9,13], n=10:
  [11,17], n=11: [13,21], … (gap ≈ 2n−14). Wide and open from n>=9.
- **k=6, k=7**: there is **no published nontrivial lower bound** at all (Harary's 2n−9 is k=5
  only). The only LBs are weak global/clique-counting ones; gap is essentially [trivial, Zheng].
- Elementary **clique-counting / fractional-packing LP lower bound** (this session,
  `exact_cr.py` analysis + scipy LP over all induced K_{k+1}'s within windows): tops out FAR
  below both Harary and the conjecture (e.g. k=5: LB <= 6 for all n<=11, vs Harary 13;
  k=6: LB <= 18; k=7: LB <= 18). **Confirms the lower bound is genuinely hard** — elementary
  clique-counting cannot reach even Harary's hand-construction, let alone the conjectured value.
  No bound improvement obtainable this way.

## 4. New fact? — HONEST verdict: NO new fact produced this session.

- The exact brute-force solver is correct (validated K_5=1, P_6^5=3 with witness) but cannot
  reach any open case (smallest open cr is 13; brute force dies past cr=3).
- The straight-line UB tool is validated (4 known values reproduced) but (by the
  rectilinear-vs-topological gap) cannot prove the conjecture; it reproduced Zheng's UB of 22
  for P_9^6 (with a checkable witness) but did NOT beat it — no refutation.
- The clique-counting LP cannot improve the lower bound.
- The one solver that *could* settle a case (crossings.uos.de exact ILP with proof) requires an
  email-confirmation handshake not completable autonomously.

So: **convention pinned + exact value cr(P_6^5)=3 independently reconfirmed with a checkable
witness + lower-bound-hardness documented** — but **no settled open case, no refutation, no
improved bound.** Reported honestly, not dressed up.

## 5. Tractability wall & recommended next step

- Brute-force exact (self-contained): wall at **cr ~ 3** (subset explosion C(pairs, k)).
- Online exact ILP (crossings.uos.de): the right tool; needs a human to submit P_9^6 / P_9^7
  (GML/edge-list) and confirm by email; emits a machine-verifiable proof. Memory limit 1 GB /
  free CLP backend means even there, cr~22–42 dense instances may not finish — but P_9^6
  (9 v, 33 e) is the most likely to be within reach and is the highest-value single submission.
- Edge lists for direct submission are in `code/cr_probe/` (generated by `pnk_graph`).

## 6. Is cr(P_n^k) confirmed SOFT?

**Partially — softness is real but the soft spot is the LOWER bound, which is hard to attack
without heavy ILP.** The gap (Harary 2n−9 vs Zheng ≈4n−23 for k=5; nothing vs Zheng for k=6,7)
is genuinely wide, growing, and 25 years stale on the LB side — so the *target* is soft in the
sense of "much room, little recent work." BUT the two tractable attack surfaces here
(elementary counting LB; self-contained exact solver) are both blocked: counting can't reach
Harary, and exact computation explodes past cr=3. The realistic soft entry is **a single
crossings.uos.de submission of P_9^6 by a human operator** — if it returns 22 it CONFIRMS the
smallest open case (a genuine new fact); if <22 it REFUTES the conjecture. That is the
concrete, low-effort, high-value next action.

---

## Witnesses (files)
- `code/cr_probe/exact_cr.py` — exact planarization solver (validated K_5=1, P_6^5=3).
- `code/cr_probe/witness_P6_5_exact.json` — the 3-crossing realizable set + LB certificate.
- `code/cr_probe/ub_fast.py` — straight-line UB search (validated K_6=3, K_7=9).
- `code/cr_probe/check_witness.py` — independent recompute of any coordinate witness.
- `code/cr_probe/draw_ub.py` — earlier circular/plane variant (superseded by ub_fast).
