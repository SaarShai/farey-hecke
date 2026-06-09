---
schema_version: 1
title: "Koyama correspondence raw record — complete Gmail thread through 2026-06-08"
date: 2026-06-08
type: correspondence-raw
tier: immutable
status: archived
participants:
  - saar.shai@gmail.com (outgoing)
  - koyama@tmtv.ne.jp (incoming; consumer ISP address, NOT @toyo.jp)
context:
  - Full Gmail thread pasted by user 2026-06-08. Spans 2026-04-27 → 2026-06-08.
    CONSOLIDATES and supersedes the partial raw records koyama-2026-05-12-exchange.md
    and koyama-2026-05-16-thread.md (those are kept, immutable). This is the most
    complete dump to date. Covers: CREST/Kiban-S/Tokusui grant arc + budget/salary
    discussion, Phase-1 replication of the Dominance-of-(-1) tables, the table
    discrepancies and their later "label-shift" reconciliation, the Lean-4
    inventory claims, and the new BCZ/Hecke ergodic-optimization + cluster-quartet
    thread.
tags: [koyama, correspondence, raw, 2026-06-08, journal, grant, budget, RISK-FLAG]
---

# Koyama thread — complete chronological record through 2026-06-08

Immutable raw record. Verbatim as pasted by the user (Gmail order: newest first).
Synthesis / action-signals / risk notes live in `../KOYAMA.md`.

> ⚠ RISK-FLAG (carried from prior raw record, see also memory `project_koyama_risk`):
> this thread mixes math collaboration with (a) large salary/budget figures that are
> entirely contingent on un-awarded grants and explicitly non-payable in advance,
> (b) a request to use Koyama's credentials/affiliation to apply for compute under
> the user's name, and (c) uniformly effusive praise with verification of the user's
> deliverables repeatedly deferred. Prior independent inspection also found at least
> one "machine-checked" Lean claim in this thread was a vacuous `True := by sorry`
> placeholder. Recorded here as raw fact for the user's own judgement; not acted on.

---

## Verbatim thread (Gmail dump, newest first)

```
Gmail  Saar shai <saar.shai@gmail.com>
Dominance of $-1$
Shin-ya Koyama <koyama@tmtv.ne.jp>  Mon, Jun 8, 2026 at 7:38 AM
To: Saar shai <saar.shai@gmail.com>
Dear Saar,

Thank you for this breathtaking update. I am completely fascinated by how rapidly and beautifully the landscape is unfolding. Calling it a "quartet" is highly appropriate — the collapse of the deep Stern–Brocot layers to the rational $2/45$ at $q^*$ is an incredibly elegant structural phenomenon.

It is also a tremendous relief and excitement to see that your family of extremal constants is definitively distinct from the Haas–Series Hurwitz constants. Knowing that the optimum drifts into the cusp via an escape-of-mass effect gives the Hecke triangle generalization a profound geometric depth. To have these trace identities already machine-checked in Lean 4 is spectacular and gives us absolute foundation.

Regarding the recent paper by Jenkinson et al., thank you for keeping a close eye on the literature. I agree that while the community is waking up to ergodic optimization, our specific corner—the BCZ/Hecke setting and our unique gap-product observables—remains entirely untouched and exclusively ours. We certainly have a clear, open path.

I would be absolutely delighted to receive the Lean proof files and your short write-up on the cluster-size computation. Please do send them over! I may not be able to dive into the code immediately as I step into the deeper parts of my $-1$-dominance repair, but having your text on hand will be immensely valuable as I envision the overall architecture of our joint paper.

It is beautiful to see that the thermodynamic formalism/transfer operators cleanly unify the cluster statistics, the extremal constants, and the fractal dimensions. Please feel free to continue developing and firming up these technical sections at your own comfortable pace over the summer. Your brilliant machine is running flawlessly.

I will be reading your write-up with great pleasure alongside my summer work. Let us keep our momentum steady and strong.

Warm regards,

Shin-ya Koyama


On Mon, Jun 8, 2026 at 4:11 PM Saar shai <saar.shai@gmail.com> wrote:

Dear Professor Koaya,

Thank you again for the last exchange — your size-2 maximality threshold (q*_BCZ ≈ 0.86181) and the universality diagnostic have been very much on my mind. I have a few developments that I think will interest you, all in the same Farey/BCZ orbit.

1. The cluster-size picture is now a "quartet." Your threshold sits at the center of what had been a "trilogy": the threshold value, the fact that at it every cluster has size at most 2, and the sharpness of that bound. We've now pinned down the missing fourth piece — the exact cluster-size distribution right at the threshold. At q*, clusters occur in only two sizes, with the split coming out to about 23% singletons and 77% pairs (Pr(L=1) = 0.22735…). The interesting part: the computation splits into Stern–Brocot "depth" layers, and the entire deep tail of those layers collapses to a perfectly clean rational, 2/45, while only a few shallow layers carry the stubborn non-elementary part — so most of the mass is rational and the "irrationality" lives in a small, finite, low-depth piece. A 5-billion-step Monte Carlo matches the analytic value to about six digits.

2. The extremal-constant family is now confirmed genuinely new. Alongside the threshold, we have a family of extremal constants for the BCZ map and its Hecke-triangle generalization: 2/9 at q=3, and more generally 1/λ³ = 1/(2cos(π/q))³ for the Hecke groups. My main worry was that 1/λ³ might secretly be the classical Hecke "Hurwitz constant" of Haas–Series — i.e. that we'd merely rediscovered something old. I ran this all the way down, and it is definitively not: the two never coincide (the Hurwitz constant sits in [0.447, 0.5] at every q, ours runs from 1 down to 1/8). So these really are new extremal constants for the Farey/BCZ class — a natural companion to your q*_BCZ phenomenon.

3. The Hecke generalization is locked across all q, and machine-checked. We now have the value pinned for the whole family, with a pleasing structural reason: the extremal configuration corresponds to the slowest elliptic element (the λ-rotation) of the Hecke triangle group. The key trace identities behind this are formally verified in Lean, and the value is confirmed "safe" out to q ≤ 200. One feature I find beautiful: the optimum is never actually attained — the best configurations drift off into the cusp (an escape-of-mass effect). The constant is the floor they approach but never reach.

4. A unifying picture. What's struck me most is that several things we'd been treating separately — the cluster-size statistics above, these extremal constants, and even the fractal dimension of the badly-approximable continued fractions — all turn out to be read off the same machine (transfer operators / thermodynamic formalism), just at different settings. As a sanity check I recomputed the classical bounded-type dimension this way and recovered the known value to ~16 digits. It's the same lens we've both been using; it just connects the whole landscape.

5. One field note. Jenkinson and coauthors posted a paper in December on ergodic optimization for the Gauss continued-fraction map. Reassuringly, it's the averaged problem on a different map — it doesn't touch the BCZ/Hecke setting, our gap-product observable, or any explicit constants, so our specific corner looks open. But the area is clearly waking up, so it may be worth our writing up the BCZ/Hecke constants before too long.

I'd love to know your thoughts about this, and suggestions for where to continue exploring.

No rush on any of this over the summer — I know you have the −1-dominance repair in view, and I'm in no hurry on my asymptotic gap either. Mostly I wanted to share that both the cluster-size and extremal-constant threads have firmed up into clean, self-contained results.

Warm regards,
Saar
P.S.
I'd be glad to send you the Lean proof files (the trace identities and the no-escape/value-safe checks) and the short write-up of the cluster-size computation with its Monte-Carlo cross-check.


On Wed, Jun 3, 2026 at 2:34 PM Shin-ya Koyama <koyama@tmtv.ne.jp> wrote:
Dear Saar,

Thank you for your wonderful and reassuring email. I am absolutely delighted that we are proceeding with Option A. It is a true honor to keep our forces combined for this joint paper.

Before we fully pause, I have one more fantastic piece of news regarding our Table 4 ($N=8, a=3$) verification. I just finished a re-run for the 13 trillion scale ($1.3 \times 10^{13}$), and it perfectly reproduced the original value of 102728!

Combined with my previous re-runs ($x = 1.3 \times 10^{11}$ giving 9199 and $x = 1.3 \times 10^{12}$ giving 42624), this completely solidifies the puzzle: our core computational logics are 100% identical. The data at the 13 trillion peak was perfectly exact, and the discrepancies at the lower checkpoints were purely due to a minor one-row label shift (1.0 data accidentally placed under 1.3 labels) during my manual compilation. It is incredibly satisfying to see our code bases align so flawlessly across all scales.

Your new scale extension up to $3 \times 10^{14}$ is spectacular. Seeing $-1$ emerge at the top for $N=7$ and $23$ exactly at this threshold is a beautiful, rigorous validation of the low-lying zero predictions discussed on page 19. Furthermore, your connection to the Fiorilli–Martin variance result is highly intuitive — it perfectly clarifies why $-1$ can be the "noisiest" in raw variance yet distinctively dominant under our $p^{-1/2}$ weighting framework. I would love to develop this together when we integrate the sections.

Regarding the single remaining cell ($N=11, a=10$ at $1.3 \times 10^{13}$), I agree that we should simply compare our raw, unadjusted $\pi(x; 11, 10)$ counts later this summer to pinpoint the structural convention difference.

Now that our roadmap is beautifully aligned and the rush is over, I will begin working on the asymptotic repair with peace of mind. Let us take a comfortable breath and enjoy the early summer. I will be in touch as soon as I have a fresh theoretical draft ready for your review.

Thank you again for your incredible collaboration and support!

Best regards,

Shin-ya Koyama


On Wed, Jun 3, 2026 at 11:23 PM Saar shai <saar.shai@gmail.com> wrote:

Dear Professor Koyama,

Indeed, I am also proud of the progress we are making and honored to collaborate with you!

An update on the onset-scale extension. The replication curve is now complete to x = 3×10¹⁴ (≈ the e^33.4 onset you identified for N=19), 438-point log grid, N ∈ {7, 8, 11, 19, 23}.

1. Integer validation: every count agrees exactly with our prior double-verified data at all nine shared checkpoints up to 1.3×10¹³ (567/567 cells, zero mismatches) — so the extension to 3×10¹⁴ carries no logic or overflow drift. A second independent-hardware run is finishing now as a further cross-check.
The −1 signal at the onset (raw π(x;N,a)−π(x;N,1)): −1 is strictly largest for N = 7 and N = 23 at 3×10¹⁴. For N = 8, 11, 19 it is mid-pack (for N = 19, −1 is actually slightly negative at this x).
The picture has also shifted relative to 1.3×10¹³ — i.e. it is still transient and modulus-dependent, exactly as your p.19 discussion of low-lying zeros predicts; 3×10¹⁴ appears to be only the threshold of the asymptotic regime, not yet inside it.

2. A complementary view (variance): if instead of the raw difference one looks at the variance of the normalized race over the grid, −1 is the maximum-variance non-residue cleanly for N = 7 and emerges as the maximum for N = 19 in the top decade. This connects to a result of Fiorilli–Martin (Crelle 2013, Thm 1.10) that −1 has the largest limiting variance among non-residues — which may be a useful bridge between the unweighted picture and your weighted dominance (it would explain why −1 can be "noisiest" in the raw race yet dominant under the p^{−1/2} weight). Happy to develop this if it's of interest.

3. One open cell: N = 11, a = 10 at 1.3×10¹³ — our value 11,503 still differs from the 71,711 in the draft; ours reconstructs exactly from identity (3.1) and agrees with the independent sieve at the lower checkpoints. Since it determines whether −1 is in the top group for N = 11, it would be good to reconcile against your raw π(x;11,10) when convenient.

On the manuscript: I'd be glad to go with Option A — let's keep everything together and integrate into the joint paper once you've completed the asymptotic repair over the summer (let me know where I can be of assistance); I'm in no hurry. For the computational side, please feel free to describe my contribution as the large-scale numerical verification and the Lean 4 formalization. I'll leave it to your judgement which of the auxiliary Farey/BCZ items best fit the paper's scope, and I'm happy to refine any technical section whenever you're ready to integrate.

Best regards,
Saar


On Mon, Jun 1, 2026 at 10:14 PM Shin-ya Koyama <koyama@tmtv.ne.jp> wrote:
Dear Saar,

I hope you are doing well. I have finally cleared my academic backlog, delivered the public lecture, and most importantly, successfully rebuilt my PARI/GP computing environment.

First, I have incredible news regarding our Phase-1 numerical discrepancies. You were absolutely right — it was a pure $x$-label error on my draft, and our underlying computational logics are in 100% perfect agreement.

For $N=8, a=3$ at true $x = 1.3 \cdot 10^{11}$ (130 billion), my re-run yields 9199. The old value 19369 in my table was actually the exact output for $x = 1.0 \cdot 10^{11}$ (100 billion), which matches your stack perfectly.

Similarly, for $x = 1.3 \cdot 10^{12}$ (1.3 trillion), my re-run confirms that the old value 42624 was actually the data for $x = 1.0 \cdot 10^{12}$ (1.0 trillion).

The labels had simply shifted by one row during my manual compilation. Our code bases are both flawlessly exact. (As for $N=11, a=10$, my system consistently reproduces 71711, so this remains a minor structural definition gap regarding bad primes, which we can easily reconcile later).

Second, I want to share a recent theoretical update with you regarding my section on the asymptotic formula for the "$-1$ dominance." During my recent review, I detected a subtle proof gap in that specific asymptotic derivation that requires a rigorous fix. Fortunately, the core conjecture of the $-1$ dominance itself relies strictly on the explicit formula analysis (which is untouched and secure), but I want to take my time—likely over the summer—to slowly and carefully repair this theoretical gap.

Regarding your email from five days ago, I am absolutely blown away by your latest results. Your discovery of the sharp size-2 maximality threshold ($q^*_{BCZ} \approx 0.86181$) and the 10-line universality diagnostic represents a profoundly new phenomenon that clearly separates the Farey/BCZ class from classical Wigner-Dyson statistics. Furthermore, your Tauberian reduction connecting the century-old Franel identity directly to Gonek’s weighted reciprocal-zeta moment framework—along with the new 13-digit stable constant—is a brilliant historical bridge that has completely evaded the literature until now.

Since these new theorems of yours are extraordinarily powerful and distinct, and because my gap repair will take until later this summer, I want to offer you full flexibility:

Option A (Joint Integration): We hold the manuscript and integrate everything into our joint paper once I completely finish repairing the asymptotic gap later this summer.

Option B (Your Sole-Author Publication + Guaranteed Co-authorship on the Dominance Paper): Since your Universality and Tauberian reduction results are so self-contained and groundbreaking, they easily constitute a spectacular, top-tier paper on their own. If you prefer to publish these discoveries immediately as a sole-author paper to secure your priority, I fully support you. Please rest assured that even if you choose this option, your status and rights as a principal co-author of our primary "$-1$ dominance" joint paper remain 100% secure and unchanged. Your extensive computational and technical contributions (the 18-page technical draft) are integral to it, and we will simply merge my revised section with your computational chapters later this summer.

Please let me know your thoughts on which direction you prefer. I am incredibly proud of how perfectly our computational frameworks matched up, and I look forward to your feedback.

Best regards,

Shin-ya Koyama


On Thu, May 28, 2026 at 12:37 AM Saar shai <saar.shai@gmail.com> wrote:
Dear Professor Koyama,

I hope you're making good progress with your back log, and that your system is back online (system crashing is all too familiar and frustrating).

I wanted to give you a short update on what's come out of the past couple of weeks. Three items are most likely to interest you:

A sharp upper bound on cluster size in the Farey/BCZ spacing dynamics, with closed-form threshold. Above q*_BCZ = (11 − 8·ln(3/2))/9 ≈ 0.86181, the maximum cluster of consecutive extreme-quantile gaps in the BCZ chain is exactly 2 — runs of length 3 or more vanish entirely. A 500-million-step Monte Carlo returned zero size-3+ clusters out of ~39 million tested at this exact constant, with the transition empirically sharp to 10⁻⁵ precision.
Significance: a sharp, closed-form cluster-size upper bound is qualitatively different from the geometric / power-law cluster-size tails of Poisson, Wigner-Dyson, and intermediate statistics — to my knowledge this is a new kind of universality phenomenon, with the BCZ density forcing exact size-2 maximality above the threshold.

A computable universality diagnostic that separates the Farey/BCZ class from Wigner-Dyson at roughly 100×. At extreme quantile q = 0.99 the size-2 cluster fraction is ~95% for Farey and the BCZ chain, ~0.5–0.75% for GOE/GUE/GSE/COE/CUE/CSE, and ~3% for Riemann ζ-zeros (consistent with GUE at low q). The diagnostic is a single sorted-spacing statistic, runs in ~10 lines.
Significance: combined with item 1, this gives a near-binary classifier — the BCZ class is the one where extreme-quantile clusters are bounded at size 2; everything else has a non-trivial size-3+ tail. Useful for placing L-function families that have so far resisted clean Katz-Sarnak placement.

A Tauberian reduction (under RH) of the Farey L²-discrepancy to a weighted reciprocal-zeta second-moment integral ∫_{(1/2)} dw / [w²(2−w)²·ζ(w)·ζ(2−w)] = 36·C·ζ(3)/π², where C is the totient summatory constant (OEIS A065483/2). The reduction passes through Σ_e (J_2(e)/e²)·T(⌊Q/e⌋)² + 2T(Q) + 1, a Jordan-totient convolution form of the Franel 1924 identity. A by-product constant Σ M(n)²/n³ = 1.1361623076908 (13 stable digits) doesn't appear in OEIS or in references I've checked.
Significance: this connects the century-old Farey L²-discrepancy problem (Franel 1924, Mikolás 1949/51, Kanemitsu-Yoshimoto 1996) to the weighted reciprocal-zeta moment framework on the critical line (Gonek 1989). I'm not aware of this bridge appearing in the literature.

All the best,
Saar


On Wed, May 20, 2026 at 6:28 PM Shin-ya Koyama <koyama@tmtv.ne.jp> wrote:
Dear Saar,

Thank you for your warm message and for understanding the intensity of the deadline leading up to the 20th. I am very pleased to let you know that we have successfully submitted the Tokusui (Specially Promoted Research) proposal for internal university review!

I have attached the finalized PDF proposal for your reference. Since it is currently under the university's internal check period, we can still make minor phrasing adjustments if needed. As you will see in the budget section, your 8.5M JPY salary and the annual 2.4(=0.6+1.5+0.3)M JPY flexible travel/equipment package are formally and beautifully secured.

Regarding our Phase-1 table reconciliation, I must kindly ask for your patience. I will need to push our discussion and my simulation re-runs back until the end of this month (around May 31st) due to two unexpected, urgent situations that have accumulated:

System Crash & Reinstallation: Right around the deadline, my primary computer suffered a major hardware failure. I have just finished re-installing Windows, which means I now have to rebuild my entire mathematical environment from scratch. It will take me some days to re-install and re-configure PARI/GP and my original simulation scripts to ensure our comparison is completely accurate.

Backlog of Academic Duties: Because I poured 100% of my energy into our grant proposals, my other duties have completely piled up. I am currently under tight deadlines for reviewing a book manuscript under my supervision, alongside preparing for a major public lecture at the end of the month on classical number theory (specifically on the Law of Quadratic Reciprocity and Fermat's Two-Square Theorem).

I am eager to dive into your 18-page draft and investigate the $N=11, a=10$ and other discrepancies as soon as my computing environment is back online and these immediate duties are discharged.

Thank you for your incredible support, and please enjoy reviewing the attached proposal. I will reach out to you as soon as I am ready around the end of the month.

Best regards,

Shin-ya


On Mon, May 18, 2026 at 11:47 PM Saar shai <saar.shai@gmail.com> wrote:

Thank you, Professor Koyama.

Wishing you and the rest of the team the best of luck with the upgraded application!

The budget for my lab is spot on.

I will await any further updates from you. I know how busy you are leading up to the 20th.

As always - if I can help with anything in the meantime - don't hesitate to let me know.

🤞🤞


On Sat, May 16, 2026 at 4:35 AM Shin-ya Koyama <koyama@tmtv.ne.jp> wrote:
Dear Saar,

I have a major update. After serious consultation with my co-investigators, we have officially upgraded our application from Kiban-S to "Specially Promoted Research" (Tokusui) — Japan's most prestigious funding tier for expanding the frontiers of pure mathematics.

https://www.jsps.go.jp/english/e-grants/grants01.html

I have just finalized the the English proposal. Because Tokusui has an absolute, rigid page-count limit and is reviewed by a panel of pure mathematicians, we kept the text focused entirely on the high-level analytic theory of the hierarchical bias. We unfortunately did not have even a single line of space to insert your beautiful $10^8$ plot or the Lean 4 verification details — those will remain the absolute core weapons for our CREST proposal, which is heavily focused on the computational/computational side.

However, I have protected your position to the maximum. As you can see in the finalized Tokusui budget, I have officially secured the 8,500,000 JPY per year budget line item for your Personnel/Honoraria.

If (and only if) either this Tokusui or the CREST is approved, this will still guarantee your position and provide you with roughly 600,000 yen/month net (take-home).

Furthermore, to fully support your environment and compute expenses, I have allocated an additional, dedicated research support package for you each year:

1,500,000 JPY/year for International Travel (to fund your visits to Japan or international conferences)

300,000 JPY/year for Domestic Travel

600,000 JPY/year for Equipment/Consumables (for PCs, hardware, and peripherals)

Under our budget management, these travel and equipment funds are flexible and reallocatary, meaning they can be strategically adjusted to directly offset your high-performance compute and infrastructure expenses.

However, as I emphasized before, the rule remains absolute:

Under Japanese audit laws, no advance or retroactive payments are permitted before the grant officially begins.

If we are rejected, the budget is zero.

To secure this 8.5M JPY/year position for you, we must win. And to win, I must focus 100% of my remaining energy on perfecting this Tokusui application until May 20th.

The administration is now locking down the system for the May 20th deadline. As we discussed, let us freeze all financial and administrative talk until May 21st. The mathematical framework is flawless, the budget is set, and your future role is beautifully secured in both proposals. Let us cross the finish line!

Best regards,

Shin-ya Koyama


On Sat, May 16, 2026 at 5:44 PM Saar shai <saar.shai@gmail.com> wrote:
Dear Professor Koyama.

The updated draft is attached. I was rigorous to meet the high standards of review.
It is the self-contained §X technical/computational section plus the two proof appendices.

Two phrasings, in case they help when quoting to reviewers:

Lean 4. "A 10-module Lean 4 / Mathlib (v4.28.0) formalisation; 8 of the 10 fully machine-checked with no sorry and no axiom (cumulative #print axioms audit); the 2 remaining sorrys are both the Dirichlet Polynomial Avoidance Conjecture at general K. Unconditional, fully proved DPAC for K ∈ {2,3,4}."
The 10⁸ verification. "The corrected B∞ identity is numerically verified across three K-scales to K = 10⁸, in two independent software stacks." The associated K^(−1/2) decay rate is RH-conditional (character analogue of Soundararajan, Crelle 2009); in our K-range it is the operative rate because the relevant zeros are numerically verified on the critical line. I've phrased it in §X.5.4 as exactly that — not as an unconditional theorem — so anything lifted verbatim stays referee-safe.

One note for the novelty wording in a panel context: the static Farey–Mertens "bridge" identity is classical (Mikolás 1949); what is genuinely ours is the differential, per-step refinement and the formalisation. §X.6 now states this provenance explicitly, so the draft is self-consistent on that point — worth preserving the same distinction in the Introduction when we get to it.

Your m-convention and the §2/§3 titles are noted for the post-20th integration. No rush.

Regarding the grant, that sounds like a good plan. I'm very much looking forward to it receiving approval.

On that matter, it has been my pleasure to collaborate and I'm very happy I'm able to contribute so much to this research. Considering the work I'm continuing to put in, it would be helpful at this point to receive a stipend until such time as the grand will (hopefully) come through. I was thinking 300,000 yen per month to cover my time and compute expenses. I hope this sounds fair.

Best,
Saar


On Fri, May 15, 2026 at 6:34 AM Shin-ya Koyama <koyama@tmtv.ne.jp> wrote:
Dear Saar,

Your progress is truly breathtaking. Thank you for the rigorous update and the numerical extension to $10^8$.

To answer your questions:

The m convention: Please proceed with your current definition $m = m(s, \chi) := \mathrm{ord}_{s'=s} L(s', \chi)$. This is the most consistent framing for our specific evaluations.

Introduction §1.1A: Your draft already captures my core message well. Please keep your current text as a placeholder; I will provide the definitive notation $(\chi_{a,1}, \text{etc.})$ and the formal statement of Conjecture 2 during my final review after May 20th.

Section Titles:

Section 2: The Dominance of $-1 \pmod N$ and Hierarchical Structure of Chebyshev's Bias

Section 3: Theoretical Consequences and Applications to Cryptographic Hardness

Updated Bundle: Yes, please send me the updated 18-page paper.pdf now. I would like to include some of your beautiful results (especially the Lean 4 status and the $10^8$ verification) in my current grant application to show the "state-of-the-art" progress of our collaboration.

I am very much looking forward to the updated PDF. It will be a powerful "visual proof" for my grant reviewers.

By the way, after consulting with Professor Aoki, I've decided to apply for the Special Research Promotion Program instead of Kiban S.
https://www.jsps.go.jp/english/e-grants/grants01.html

I'm currently writing the application. This grant is for 200 to 500 million yen, but the total expenses so far are about 280 million yen, so it's possible to include a little more. The 7.2 million yen you requested for the first year's computing equipment is included. In addition to that, if you need to replace the equipment within 5 years, please let me know so I can include that as well.

Best regards,

Shin-ya


On Fri, May 15, 2026 at 8:09 PM Saar shai <saar.shai@gmail.com> wrote:
Dear Shin-ya,

Thank you again for the green light. I'm thrilled we are on the right track!

A summary, then four small questions where I'd benefit from your judgement before LaTeX integration.

[1. Numerical extension to K = 10^8 — residual ratios 3.7 and 4.3 (clean χ5, χ11), slower 1.09–1.15 for χ_−4 (bad prime p=2); verified across three K-scales spanning two decades; §X.5.4 updated; BINFTY_K100M_run.log in bundle.]

[2. Lean inventory: 10 files, 8 fully proved, axiom audit clean. New RamanujanSum.lean discharges h_ramanujan_decomp (FareyBridgeIdentity now unconditional). MertensSpectroscopeUniversality.lean gained two unconditional lemmas (spectroscope_nonneg, reciprocal_sqrt_not_summable) + 5-step blueprint; headline still conditional on Soundararajan-style hypothesis. Remaining two sorrys = headline DPAC at general K (LI-class). New _AxiomCheck.lean: six headlines on standard trust base; dpac_le_4 also uses Lean.ofReduceBool + Lean.trustCompiler.]

[3. Adversarial review pass: T_K notation drift fixed (→ T(K) for Inoue truncation height); Soundararajan-2009 rate corrected from "unconditional" to RH-conditional in five places; two citation provenance fixes (Aoki–Koyama 2023 JNT 245; Inoue 2021 JTNB 33(1)). Bundle compiles to ≈18-page PDF (tectonic); all refs resolve.]

Four questions before integration: (1) the m convention in your (1.4); (2) the Dominance-of-−1 framing paragraph for §1.1 (placeholder KOYAMA-INSERT-1.1A); (3) section titles for §2 and §3 (placeholder KOYAMA-INSERT-1.5); (4) whether to send the updated bundle now or wait for your Phase-1 reconciliation.

Best, Saar


On Wed, May 13, 2026 at 5:23 AM Shin-ya Koyama <koyama@tmtv.ne.jp> wrote:
Dear Saar,

This is a monumental contribution!
I am amazed by your speed and the rigor of the Lean 4 formalization. I will list you as a key co-author.

Quick answers to your scope confirmations so you can proceed with LaTeX conversion:

1. Two scales: YES, please keep the $10^{13}$ (residue counts) and $10^7$ (analytic identities) rigorously separate as you suggested.

2. Double-verification: YES, your definition (two software stacks for each claim) is exactly what I had in mind.

Regarding the table discrepancies:

Thank you for the detailed audit. The $N=11, a=10$ cell is indeed critical. I will re-run my original scripts and check for label errors or transcription bugs after May 20th.

Please go ahead with the technical draft.

Best regards,

Shin-ya Koyama


[On Wed, May 13, 2026 at 4:10 PM Saar shai wrote: first-draft technical/computational section + Appendix A (corrected B∞ identity, Thm X.4.1) + Appendix B (c_K leading+subleading) + per-sorry Lean inventory. Two scope confirmations (two scales 10^13 vs 10^7; double-verification = two stacks per claim). Table-discrepancy audit vs nontriv.pdf Tables 3–7: load-bearing N=11,a=10 cell (11,503 vs 71,711); N=19,a=13 (24,559 vs 55,581); N=19,a=18 (54,192 vs 57,192); N=7,a=6 (26,129 vs 26,179); N=23,a=19 (79,327 vs 79,227); Table 4 small-x rows x-label error suspected. Lean: 6 files fully proved (LocalPerronResidue, CorrectedBInfty [cond. on one Tendsto], DPAC_closure_attempt [uncond K∈{2,3,4}], MertensSpectroscopeUniversality [cond], FareyBridgeIdentity [cond], SmoothedDwfFormula_full); 5 sorrys research-open (DPAC ×2 LI-class, FareySignPattern ×3). GL(1) halo route: negative finding (only K^{1/2+ε}).]

[On Mon, May 11, 2026 — Koyama: CREST proposal submitted; wants Saar as co-author; asks Saar to draft the Technical/Computational section. Saar earlier the same day: tightened EC/C_1 statements (rank trend now "conductor-confounded", not a clean law); NDC/DRH constant correction 1/ζ(2) → Mertens/Aoki–Koyama e^{−γ}; Δ anchor ~0.950232 as target not theorem; Sym²/Petersson proportionality falsified in raw form.]

[Apr 27 – May 4, 2026 — grant/role/budget arc: Koyama proposes CREST collaboration; team list (Aoki, Okumura, Sheth, Shoemann, Kimura; later Takagi senior advisor, Mitsunari); requests "Post-Bias Cryptographic Framework" + Lean-4 memo for lattice crypto; budget settled at 12M JPY/year (7.2M compute + 4.8M stipend) — "Strategic Research Architect"; Phase-1 replication of Dominance-of-(-1) Tables 3–7 at x≤1.3×10^13, two independent sieves, π(1.3×10^13)=445,831,610,611, identity (3.1) checked at 495 cells (worst 1.4×10^-4); full replication bundle delivered 2026-05-04. ADMIN NOTES (RISK-relevant): university cannot issue Saar an email until position activated post-award; Saar asked to "use my [Koyama's] credentials" / apply under "free usage category in your name, using my affiliation"; "no advance or retroactive payments before the grant officially begins"; "If we are rejected, the budget is zero."]
```

---

## Coverage check (what this record now contains)

- **Full grant arc** Apr 27 → Jun 8 (CREST → Kiban-S → Tokusui), team roster, and
  all budget/salary/stipend figures (12M JPY/yr; later 8.5M JPY/yr salary +
  2.4M package; Saar's declined 300k JPY/month stipend request).
- **Phase-1 replication** + the full table-discrepancy list and the eventual
  "label-shift" reconciliation (and the still-open N=11,a=10: Saar 11,503 vs
  Koyama 71,711).
- **Lean-4 inventory claims** as stated to Koyama (8/10 "fully proved") — see the
  RISK-FLAG re: a previously-found vacuous placeholder; Lean claims in this thread
  remain to be re-audited before any external reuse.
- **BCZ/Hecke** thread: cluster quartet, extremal constants 2/9·√2/8·1/λ³, the
  Jenkinson-et-al field note, ergodic-optimization framing.
- Synthesis + action signals: `../KOYAMA.md` (`Exchange (2026-06-08)` section).
