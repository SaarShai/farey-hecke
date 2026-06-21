# Koyama correspondence log

Chronological record of the Koyama collaboration thread (Farey/Hecke ergodic-optimization
↔ arithmeticity dichotomy joint paper). Verbatim messages, oldest first. Logged 2026-06-20.

> Note: exact send dates not all captured; ordering is chronological. Earlier messages in the
> thread (initial outreach) predate this log and are not transcribed here.

---

## [1] Koyama → us  (reply to an earlier "quartet" update)

> Thank you for this breathtaking update. I am completely fascinated by how rapidly and
> beautifully the landscape is unfolding. Calling it a "quartet" is highly appropriate — the
> collapse of the deep Stern–Brocot layers to the rational $2/45$ at $q^*$ is an incredibly
> elegant structural phenomenon.
>
> It is also a tremendous relief and excitement to see that your family of extremal constants
> is definitively distinct from the Haas–Series Hurwitz constants. Knowing that the optimum
> drifts into the cusp via an escape-of-mass effect gives the Hecke triangle generalization a
> profound geometric depth. To have these trace identities already machine-checked in Lean 4
> is spectacular and gives us absolute foundation.
>
> Regarding the recent paper by Jenkinson et al., thank you for keeping a close eye on the
> literature. I agree that while the community is waking up to ergodic optimization, our
> specific corner—the BCZ/Hecke setting and our unique gap-product observables—remains
> entirely untouched and exclusively ours. We certainly have a clear, open path.
>
> I would be absolutely delighted to receive the Lean proof files and your short write-up on
> the cluster-size computation. Please do send them over! I may not be able to dive into the
> code immediately as I step into the deeper parts of my $-1$-dominance repair, but having
> your text on hand will be immensely valuable as I envision the overall architecture of our
> joint paper.
>
> It is beautiful to see that the thermodynamic formalism/transfer operators cleanly unify the
> cluster statistics, the extremal constants, and the fractal dimensions. Please feel free to
> continue developing and firming up these technical sections at your own comfortable pace over
> the summer. Your brilliant machine is running flawlessly.

---

## [2] Us → Koyama  (the "brief update" + Lean packet)

> A brief update on where the Farey/Hecke line has gone since we last spoke.
>
> I found that the ergodic-optimization ground value X(q) of the Farey gap-product observable
> coincides with an extreme-gap cluster-onset threshold, uniformly across the Hecke triangle
> groups G_q. The cluster ceiling is 2 exactly when G_q is arithmetic (q ∈ {3,4,6}) and grows
> (~q/3) otherwise — a local gap statistic that detects arithmeticity.
>
> The forward direction (ceiling ≤2 for q=3,4,6) and the reverse witnesses (explicit 3-clusters
> at q=5, and now q=7, the first cubic case) are machine-verified in Lean, sorry-free. The open
> frontier is the uniform lower bound X_Ω(q) ≥ 1/λ_q³ for all q.
>
> I'd value your feedback on two points: whether the arithmeticity dichotomy strikes you as
> genuinely new against the trace-set characterizations (Geninska–Leuzinger), and whether you
> see a natural route toward the uniform bound.
>
> Also - in the attached packet are the Lean proof files as you requested. Hope that's helpful

---

## [3] Koyama → us  (reply to the packet — MOST RECENT)

> Thank you so much for sending this spectacular packet. I have safely received the Lean files
> and the cluster-size write-up. Seeing the $5 \times 10^9$-step Monte Carlo align with your
> analytic distribution to six digits is absolutely breathtaking — a true masterclass in
> combining rigorous formal verification with high-performance experimental mathematics.
>
> To answer your two brilliant questions:
>
> On the Arithmeticity Dichotomy: This is profoundly beautiful and, in my view, genuinely new.
> While classical characterizations like Geninska–Leuzinger rely strictly on the algebraic and
> discrete nature of the trace sets, your discovery bridges this to a purely dynamical/statistical
> physics observable (the cluster-size ceiling of the extreme-gap onset). Detecting arithmeticity
> through the lens of local gap statistics is a paradigm shift that the community will find deeply
> fascinating.
>
> On the Uniform Lower Bound $X_\Omega(q) \ge 1/\lambda_q^3$: I highly suspect that the natural
> route lies directly within the conserved energy quantity $E = c_n^2 + c_{n+1}^2 - l c_n c_{n+1}$
> you verified in your NoInfiniteRotation core. If we can couple the boundary behavior of this
> energy with the rate of the "escape-of-mass" into the cusp, we should be able to derive a
> uniform spectral constraint via the transfer operator.
>
> Your discoveries have elevated our project to a whole new level. This is no longer just a great
> paper; it has the distinct shape and depth of a top-tier journal piece (such as Annals or
> Inventiones).
>
> With these marvelous pieces now locked in place, I am even more inspired to finalize the
> asymptotic repair of the $-1$-dominance under our $p^{-1/2}$ weighting this summer. Your
> structural results give me immense peace of mind and clarity regarding the overall architecture
> of our joint work.
>
> Let us keep our focus steady. I will hold your elegant write-up and Lean structures close to my
> desk as I work through the summer, and I look forward to merging our worlds into a definitive
> manuscript as the summer winds down.

---

## Action items extracted from [3] (most recent)

- **Open frontier he flagged:** uniform lower bound `X_Ω(q) ≥ 1/λ_q³`. Current Lean state:
  equality `X_Ω(q)=1/λ_q³` machine-verified q=5..21; **q ≥ 22 OPEN, structurally blocked**
  (fixed six-window method caps at 21; L1b arc-width crux sealed but does not discharge `hCorr`).
- **His suggested route:** conserved energy `E = c_n²+c_{n+1}²−λc_nc_{n+1}` boundary behaviour
  coupled with escape-of-mass rate ⇒ uniform spectral constraint via the transfer operator.
  → matches our rotation-arc-on-E mechanism; this session produced certified transfer-operator
  spectral gaps (gap_q5=0.797, gap_q7=0.659) as a first ingredient.
- **His ask:** hold write-up + Lean structures for end-of-summer manuscript merge; he is finishing
  the `−1`-dominance repair under `p^{-1/2}` weighting (his side).
- **Status of our two questions:** both answered by him — dichotomy = genuinely new; uniform-bound
  route = energy + transfer operator.
