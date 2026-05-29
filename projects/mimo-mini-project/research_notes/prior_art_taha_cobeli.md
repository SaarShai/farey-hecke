# Prior-art audit — Taha (1810.10668) & Cobeli–Zaharescu (1411.1321)

**Date**: 2026-05-27
**Trigger**: close the two remaining "abstract-only" gaps from `prior_art_addendum.md`
**Method**: full-text extraction (`pdftotext`) of arXiv PDFs; targeted keyword + section reads
**Cap**: ~45 min; both PDFs successfully parsed (no access blockers)

Subject under audit: our cluster=2 boundedness theorem for the BCZ chain at threshold `t = 2/9`, with closed-form `q*_BCZ = (11 − 8·ln(3/2))/9`.

---

## 1. Cobeli & Zaharescu (2014/2015), arXiv:1411.1321 — *"On the geometry behind a recurrent relation"*

### Summary (2 paragraphs)

The paper studies the integer "valence" chain `k = (k_1, …, k_r)` attached to `r+2` consecutive Farey denominators `q_0, …, q_{r+1}` via the recurrence `k_j q_j = q_{j-1} + q_{j+1}` — **exactly the continuant recurrence that underlies our cluster=2 proof**. The authors interpret each admissible chain `k ∈ A_r` as a convex polygon `T_r[k] ⊂ T` ("Farey triangle") and reduce questions about valence chains to a tessellation of `T`. Main quantitative result (§1, Remark 1.1; §5): for each `r`, `#{k ∈ A_r : ||k|| ≤ n} = r·n + C(r)` for all sufficiently large `n`, with tabulated constants `C(1)=0, C(2)=3, C(3)=15, …, C(20)=5761`. Whether `C(r)` has a closed form is left open.

The route to that asymptotic passes through **explicit bounds on small-`r` admissible chains** (§4, "Small Orders"). These bounds are run-length-style statements about consecutive valences. Crucially:

- **Lemma 3** (p. 5): "The smallest of any two consecutive neighbor valences cannot be larger than 3" — i.e. `min(k_j, k_{j+1}) ≤ 3`.
- **Lemma 4** (p. 5): "There are no two neighbor valences both equal to 1."
- **Lemma 5** (p. 5): if `(k, l)` are neighbor valences and `k ≥ 5`, then `l = 1`.
- **Lemma 6** (p. 6): for any three consecutive valences `(k, l, m)`, `min(k, m) < 8`.
- **§5 (Completion of proof, p. 6–7)**: "an admissible tuple has at most **one** very large component" — a structural cluster-style theorem on extremal valences in arbitrary-length chains.

### Verdict

**RELATED, but materially stronger than 'disjoint'** (upgrade from the abstract-only assessment in `prior_art_addendum.md`).

- **Not a PREDECESSOR of cluster=2 at threshold 2/9.** The CZ observable is the integer `k_j = ⌊(1+q_{j-1}/q_{j+1})·q_j/q_{j-1}⌋`-type valence, not the continuous BCZ-orbit product `X_j X_{j+1}` against the geometric threshold `2/9`. There is no mention of `2/9`, of `(11 − 8·ln(3/2))/9`, or of a quantile/density interpretation, and no statement that admissible chains of "large valences" have length ≤ 2.
- **Not IMPLICIT either.** The CZ extremality lemmas (3, 5, 6 and the §5 induction) bound `min(k, l)` or `min(k, m)`, not max-runs of `k_j ≥ K` for arbitrary K. In particular, **Lemma 5 + Lemma 6 together do NOT yield "at most 2 consecutive BCZ-extreme indices"** for our continuous threshold; they bound how *small* a neighbour of a large valence must be, which is a structurally different statement and uses a different (integer-floor) extremality notion.
- **Strong methodological overlap.** Their tessellation `{T_r[k]}` of `T` is the same convex-polygon partition that drives our `X_j X_{j+1} < 2/9` analysis. The continuant recurrence and the "sum of consecutive denominators > Q" trick (their Lemma 3 proof) are the two ingredients we also use. Anyone who has read CZ §4 will see our cluster=2 proof as "natural in that idiom."

**Recommended citation**: cite as the primary precedent for *integer-valence* cluster bounds on the same recurrence — explicitly noting that our threshold (geometric, `2/9`) and observable (continuous product) are different, and that CZ Lemma 5 / §5 are the closest extant statements but neither imply nor are implied by our cluster=2 at `t = 2/9`.

Suggested wording (for paper / Mathlib PR):
> "Cobeli–Zaharescu [CZ14, §4–§5] establish run-length-style bounds on the valence chain `k_j q_j = q_{j-1}+q_{j+1}` (the same continuant recurrence used here). Their Lemma 5 shows that a valence `k ≥ 5` forces its neighbour to equal 1, and their §5 induction shows admissible chains carry at most one very large valence. Our Theorem [cluster=2] is a parallel statement for the **continuous BCZ product** `X_j X_{j+1}` against the threshold `2/9`, and does not appear to follow from, or imply, the CZ valence bounds."

---

## 2. Diaaeldin E. Taha (2018), arXiv:1810.10668 — *"The BCZ Map Analogue for Hecke Triangle Groups G_q"*

### Summary (2 paragraphs)

The paper constructs the BCZ map analogue for the discrete orbit `Λ_q = G_q(1,0)^T`, where `G_q` is the Hecke triangle group with cusp parameter `λ_q = 2 cos(π/q)`. Section 2: defines a `G_q`-Farey triangle `T^q ⊂ T` and proves three structural theorems — (Thm 2.1) a `G_q`-Stern–Brocot tree, (Thm 2.2) the BCZ map `BCZ_q : T^q → T^q`, and (Thm 2.3) the next-term/horocycle algorithm. Section 3: identifies `(T^q, m_q, BCZ_q)` as a cross-section to the horocycle flow on `X_q = G_q\\SL(2,R)` (Thm 3.1) and gives an equidistribution corollary (Thm 3.2). Section 4: applications — discrete-orbit equidistribution (Cor 4.1), the slope-gap distribution for `Λ_q` (Cor 4.3, §4.2.1), and a weak Dirichlet approximation.

The closest content to a "cluster" statement is §4.2.1 (Slope Gap Distribution) and the proofs around the next-term algorithm. Throughout, "consecutive" appears only in the sense of *consecutive slopes / vectors `u_n, u_{n+1}` under the next-term map*, not in a run-length sense. The paper contains no maximum-run-length theorem, no threshold above which a cluster size becomes bounded, and no constant analogous to `(11 − 8·ln(3/2))/9` or `2/9`. The word "cluster" does not appear; "extremal" does not appear; "run length" does not appear.

### Verdict

**DISJOINT (with respect to cluster-bound content)**, but a candidate setting for a future generalisation.

- **Not a PREDECESSOR.** Taha proves no cluster/run-length bound and gives no `t = 2/9` analogue.
- **Not IMPLICIT.** The `G_q` BCZ map and `G_q`-Farey triangle are constructed, and the slope-gap distribution is derived (analogous to Boca–Cobeli–Zaharescu for `q = 3`), but no extreme-product threshold is identified. In particular, there is no statement of the form "for `G_q`, the max cluster of consecutive `X_j X_{j+1} < t(q)` is `k(q)`" for any `t(q), k(q)`.
- **Important open angle (flag, not a finding).** Taha's framework *would be the natural setting* for a `G_q`-generalisation of our cluster=2 theorem: one would expect a `q`-dependent threshold `t_q` and a cluster bound `k(q)` (with `k(3) = 2` recovering us). This is a research lead, not pre-existing prior art.

**Recommended citation**: cite as the canonical source for the `G_q`-BCZ map and as the natural setting for any future Hecke-group generalisation of cluster=2, explicitly noting that no cluster bound is given there.

Suggested wording:
> "Taha [Tah18] constructs the BCZ map analogue for the Hecke triangle groups `G_q` and derives the slope-gap distribution for the discrete orbits `Λ_q`. No cluster-size or run-length theorem appears in [Tah18]; a `G_q`-generalisation of our Theorem [cluster=2] (with a `q`-dependent threshold) is a natural open direction in that framework."

---

## Honest synthesis — is cluster=2 still novel?

**Yes, novel as a statement; not novel as a method.** Two qualified points:

1. **As a method**, Cobeli–Zaharescu §4–§5 (Lemmas 3, 5, 6 + §5 induction) already prove run-length-flavoured theorems on the exact same continuant recurrence, with the same Farey-triangle tessellation and the same "consecutive-denominators-sum-exceeds-Q" trick. Our cluster=2 proof lives in their idiom. Any honest write-up must lead with this and cite Lemma 5 / §5 alongside the cluster=2 theorem — otherwise readers familiar with [CZ14] will (correctly) view the framing as derivative.

2. **As a statement**, the specific bound — max run-length of `X_j X_{j+1} < 2/9` is 2, with the threshold `2/9` and the closed-form quantile `q*_BCZ = (11 − 8·ln(3/2))/9` — does not appear in either paper, nor is it an immediate corollary of any single result we found. CZ's Lemma 5 (`k ≥ 5 ⇒ l = 1`) and §5 (≤1 very large component) are siblings, not implicants.

**Net adjustment vs `prior_art_addendum.md`**:
- Cobeli–Zaharescu: from **"RELATED, not predecessor"** → **"RELATED-strong; cite Lemmas 3, 5, 6 + §5 explicitly; frame our theorem as a continuous-threshold analogue, not an independent discovery."**
- Taha: confirmed **"DISJOINT, contains no cluster bound"** → keep current framing; add as setting for `G_q`-generalisation.

**Risk if we don't update citations**: a referee or the CZ authors themselves could reasonably object that our cluster=2 framing implicitly recapitulates their §4 structural lemmas without attribution. The fix is cheap (one paragraph + 2 cite-keys) and protective.

---

## Files referenced

- `/tmp/taha.txt` — text extraction of `arxiv.org/pdf/1810.10668` (2169 lines)
- `/tmp/cobeli.txt` — text extraction of `arxiv.org/pdf/1411.1321` (644 lines)
- `/Users/za/Documents/Farey NOW/projects/mimo-mini-project/research_notes/prior_art_addendum.md` — prior abstract-only assessment (supersede entries 1 and 4)
