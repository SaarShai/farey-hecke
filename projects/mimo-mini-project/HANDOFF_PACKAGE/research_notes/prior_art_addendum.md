# Prior-art investigation — cluster=2 + q*_BCZ closed form

**Date**: 2026-05-27
**Trigger**: independent reviewer flagged 4 likely-predecessor papers
**Method**: subagent literature scan via arXiv + abstract / metadata (PDFs not all accessible)
**Honest caveat**: verdicts are based on abstracts; full-text audits recommended for any "needs-check"

---

## Paper-by-paper verdicts

### 1. Cobeli & Zaharescu (2015) — arXiv:1411.1321
"On the geometry behind a recurrent relation"

**Main result**: studies a linear recursive relation defining continuant-like polynomials and their geometric interpretation, in the context of chains of *valences* in the Farey series.

**Re: cluster=2 / q*_BCZ**: same recurrence structure `k_j q_j = q_{j-1} + q_{j+1}` as ours, but the observable is **valence chains** (vertex degrees), not consecutive extreme product pairs `X_i X_{i+1} < 2/9`. The abstract does not mention cluster-size bounds or the (11 − 8 ln(3/2))/9 constant.

**Verdict**: **RELATED, not predecessor** — shared continuant recurrence, disjoint question domain.

### 2. Boca, Gologan, Zaharescu (2002) — arXiv:math/0201044
"On the index of Farey sequences" — Q. J. Math. 53(2), 377–391.

**Main result**: asymptotic formulae for the distribution of Farey-sequence indices as Q → ∞.

**Re: cluster=2 / q*_BCZ**: index distribution is a global average, not a local run-length statistic. Abstract makes no mention of consecutive-pair product constraints.

**Verdict**: **DISJOINT** — different observable, standard Farey index, not BCZ-chain extreme dynamics.

### 3. Augustin, Boca, Cobeli, Zaharescu (2001) — Math. Proc. Camb. Phil. Soc. 131
"The h-spacing distribution between Farey points"

**Main result**: limiting distribution for `h`-spacings (gaps between Farey points distance h apart in index) on [0, 1].

**Re: cluster=2 / q*_BCZ**: h-spacing is a different statistic from extreme-pair clustering. Abstract gives no evidence of cluster bounds.

**Verdict**: **DISJOINT** — h-spacing ≠ product constraints; different statistic.

### 4. Diaaeldin Taha (2018) — arXiv:1810.10668
"The Boca-Cobeli-Zaharescu Map Analogue for the Hecke Triangle Groups G_q"

**Main result**: derives BCZ-map analogue for discrete orbits of Hecke triangle groups; applications to slope-orbit statistics Λ_q.

**Re: cluster=2 / q*_BCZ**: this is the most closely related — a generalization of BCZ to Hecke groups. Abstract does NOT mention cluster-size bounds or the specific threshold, but full text was not accessed by the subagent.

**Verdict**: **NEEDS FULL-TEXT CHECK** — positive relation to BCZ; whether cluster bounds appear is unconfirmed from abstract.

---

## Honest synthesis

**Likely novel, pending Taha full-text check.** None of the four primary references in the reviewer's list explicitly states:
- A bound on max consecutive extreme product pairs ("cluster size ≤ 2")
- The product threshold `X_i · X_{i+1} < 2/9` as a structural constraint
- The closed-form quantile `q*_BCZ = (11 − 8 ln(3/2))/9 ≈ 0.86181`

Cobeli–Zaharescu (2015) shares the **continuant recurrence framework** that underlies our proof — they should be cited as the closest structural predecessor, even though their observable is different.

Taha (2018) extends BCZ to Hecke groups; if a parallel cluster bound appears in their §3–§5, we'd need to acknowledge / connect / cite. Otherwise this is independent extension.

The remaining two (Boca-Gologan-Zaharescu, Augustin et al.) are disjoint observables on the same Farey/BCZ system — should be cited only for context, not as predecessors.

---

## Recommended citation list

```bibtex
@article{Cobeli2015,
  title={On the geometry behind a recurrent relation},
  author={Cobeli, Cristian and Zaharescu, Alexandru},
  journal={Journal of Difference Equations and Applications},
  year={2015},
  note={arXiv:1411.1321}
}

@article{BocaGologanZaharescu2002,
  title={On the index of Farey sequences},
  author={Boca, F. P. and Gologan, R. N. and Zaharescu, A.},
  journal={Quarterly Journal of Mathematics},
  volume={53},
  number={2},
  pages={377--391},
  year={2002}
}

@article{AugustinBocaCobeli2001,
  title={The $h$-spacing distribution between Farey points},
  author={Augustin, P. and Boca, F. P. and Cobeli, C. and Zaharescu, A.},
  journal={Mathematical Proceedings of the Cambridge Philosophical Society},
  volume={131},
  pages={23--38},
  year={2001}
}

@article{Taha2018,
  title={The Boca-Cobeli-Zaharescu Map Analogue for the Hecke Triangle Groups $G_q$},
  author={Taha, Diaaeldin Eddine},
  journal={arXiv preprint arXiv:1810.10668},
  year={2018}
}

@article{BCZ2001,
  title={On the distribution of the Farey sequence with respect to spacings},
  author={Boca, F. P. and Cobeli, C. and Zaharescu, A.},
  journal={J. Reine Angew. Math.},
  volume={535},
  pages={207--236},
  year={2001}
}

@article{AthreyaCheung2014,
  title={A {P}oincar\'e section for the horocycle flow on the space of lattices},
  author={Athreya, J. and Cheung, Y.},
  journal={Int. Math. Res. Not.},
  volume={2014},
  number={10},
  pages={2643--2690},
  year={2014},
  note={arXiv:1206.6597}
}
```

---

## Limitations + follow-up

- Full-text PDF access was limited during the scan.
- **Highest-priority follow-up**: full-text read of Taha 2018 §3–§5 — if they prove or observe a parallel cluster bound on Hecke triangle groups, that's a direct related-work citation; if not, our result extends naturally to that setting.
- Cobeli–Zaharescu 2015 should be cited as the closest structural predecessor (continuant recurrence framework).
- We have NOT yet checked: Heersink (Farey gap moments), Marklof–Strömbergsson (Three-Gap revisited), Conrey–Snaith on L-function moment universality, other Boca/Zaharescu coauthored work.

**Bottom line**: our result is **likely novel** as a precise cluster-size-bound statement, but the **continuant recurrence framework** has clear prior art in Cobeli–Zaharescu. The paper writeup should acknowledge this lineage explicitly.
