# Email reply draft to Shin-ya Koyama

**Subject:** Spectral section and corrections for the joint prime-bias manuscript

Dear Shin-ya,

Thank you for sending the update and the manuscript.  I am enthusiastic about developing
the joint prime-bias paper, and I have now prepared the main numerical contribution for
integration: a reproducible low-zero reconstruction of the ordinary prime-count races for
`N=7,8,11,19,23` through `3 x 10^14`, together with a five-panel figure, transition tables,
and a precise inventory of the Lean formalization.

The spectral results are strong.  Using the first 25 positive zeros of every nonprincipal
character gives top-decade correlations of approximately `0.965, 0.931, 0.939, 0.971,
0.826` for the five moduli.  At the same time, the rank of `-1` continues to change
frequently throughout that window.  I think this gives us a compelling finite-scale story:
the low zeros explain the observed trajectories quantitatively, but the races remain
dynamically unsettled at the 300-trillion scale.

The computation also revealed one material correction that we should resolve in the TeX.
For the primitive character of Conrey index 13 modulo 19, a positive ordinate occurs at
`0.0189563990802261...`, with `chi(-1)=-1`.  It passes both PARI mesh checks and a direct
`L`-value residual check.  I then reproduced it independently with Python FLINT/Arb: a
sign-definite Hardy-`Z` bracket of width below `6 x 10^-84` certifies existence of a
critical-line zero there.  Extending every nonprincipal character modulo 19 to 100 positive
zeros improves the top-decade correlation to `0.9925`, while rank and leader changes still
persist.  Thus the discussion treating `gamma approximately 1.74` as the lowest relevant
complex zero, and `3.18 x 10^14` as a settling scale, needs to be revised.  The stronger
supported statement is that a very slow low-zero transient remains active there.  The Arb
certificate establishes existence, not uniqueness, zero completeness, or GRH.

I also found a correctable character-convention issue in Definition 1.3.  As printed,
`(1-chi(a))chi(x)` selects the class `a^{-1}` rather than `a`; using
`(1-conj(chi(a)))chi(x)` gives the intended selector.  I have a clean Lean certificate for
this finite identity.  Separately, the current fixed-`T` theorem needs its `T`-dependence
and summed off-diagonal estimate made explicit before we present it as proved.  I have set
out the exact corrections and safe replacement wording in a short memo.

Could you please send me the complete current TeX source, bibliography, figures, and tables,
as well as the public arXiv identifier and version?  Once I have the source, I can integrate
the spectral section directly, reconcile notation and cross-references, and return a clean
joint draft.  I suggest that we then have the repaired analytic argument independently read
before setting a submission date.  This will let us make the strongest claims the evidence
supports without conflating the regularized statistic with the ordinary prime counts.

I have also drafted a detailed contribution statement so that the theoretical, numerical,
software, and formalization roles are recorded accurately.  Naturally, we should both
review and approve the complete manuscript, author order, contribution statement, cover
letter, and final submission version before anything is submitted.

I have included a proposed computational-assistance disclosure as well.  It records the
limited use of language-model and Aristotle assistance, makes clear that the Lean certificate
covers only selected finite algebraic statements, and leaves full responsibility with us as
the human authors.  We can reconcile that wording against the exact tools retained in the
final workflow.

For the separate boundary Euler--Perron project, I completed the central boundary identity
but also found close prior art that already supplies the substantive boundary-series
framework.  I therefore do not plan to present the present identity as a novel standalone
research theorem.  Its defensible role is a technical appendix or reproducibility note unless
a genuinely new theorem emerges.  Any future coauthorship would depend on a substantial,
documented joint contribution.

I would be happy to discuss the corrections by video call, but exchanging the complete TeX
first will make that conversation much more concrete.

Best regards,

[Your name]

## Proposed attachments

1. Compiled preview of “Transient spectral oscillations at the 300-trillion scale.”
2. Compact correction and redline memo.
3. Proposed author-contribution statement.
4. Proposed AI and computational-assistance disclosure.
5. Reproducibility manifest and code/data archive link (after an archival URL or agreed
   private transfer location is prepared).
