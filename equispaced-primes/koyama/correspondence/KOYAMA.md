# Correspondence: Prof. Shin-ya Koyama

- Primary Gmail address: `koyama@tmtv.ne.jp`
- University address mentioned by Koyama: `koyama@toyo.jp`
- Gmail verification date: 2026-05-11
- Complete Gmail-derived record: `raw/farey-archive/correspondence/koyama-gmail-record-2026-05-11.md`

## Gmail Search Result

- Query: `in:anywhere (from:koyama@tmtv.ne.jp OR to:koyama@tmtv.ne.jp)`
- Result: 54 direct messages, 3 Gmail threads.
- Query: `in:anywhere (from:koyama@toyo.jp OR to:koyama@toyo.jp)`
- Result: 0 direct messages.

Gmail found 3 direct threads, not 2:

1. `Deep Riemann Hypothesis & Farey Spectroscope`
   - 3 messages
   - 2026-04-05
   - Opening contact and paper-send handoff.

2. `Weighted prime-bias behavior arising from Farey discrepancy`
   - 35 messages
   - 2026-04-05 to 2026-04-25
   - Farey/DRH, DPAC, EDRH/NDC, GL(2), EC/C1, rank/conductor, Delta, CV/admin, first Dominance-of-`-1` setup.

3. `Dominance of $-1$`
   - 16 messages
   - 2026-04-26 to 2026-05-04
   - Dominance-of-`-1` specification, CREST role/budget, applied/social-impact materials, replication reports, and full bundle delivery.

## Exchange (2026-06-03) — recorded verbatim

Thread: `Dominance of $-1$` (continuation). **Outbound WAS sent this round (by
user).** Order: Saar's email first, Koyama's reply second.

### Outgoing (2026-06-03, Saar) — verbatim

> Dear Professor Koyama,
>
> Indeed, I am also proud of the progress we are making and honored to collaborate with you!
>
> An update on the onset-scale extension. The replication curve is now complete to x = 3×10¹⁴
> (≈ the e^33.4 onset you identified for N=19), 438-point log grid, N ∈ {7, 8, 11, 19, 23}.
>
> 1. Integer validation: every count agrees exactly with our prior double-verified data at all
> nine shared checkpoints up to 1.3×10¹³ (567/567 cells, zero mismatches) — so the extension to
> 3×10¹⁴ carries no logic or overflow drift. A second independent-hardware run is finishing now
> as a further cross-check.
> The −1 signal at the onset (raw π(x;N,a)−π(x;N,1)): −1 is strictly largest for N = 7 and N = 23
> at 3×10¹⁴. For N = 8, 11, 19 it is mid-pack (for N = 19, −1 is actually slightly negative at
> this x).
> The picture has also shifted relative to 1.3×10¹³ — i.e. it is still transient and
> modulus-dependent, exactly as your p.19 discussion of low-lying zeros predicts; 3×10¹⁴ appears
> to be only the threshold of the asymptotic regime, not yet inside it.
>
> 2. A complementary view (variance): if instead of the raw difference one looks at the variance
> of the normalized race over the grid, −1 is the maximum-variance non-residue cleanly for N = 7
> and emerges as the maximum for N = 19 in the top decade. This connects to a result of
> Fiorilli–Martin (Crelle 2013, Thm 1.10) that −1 has the largest limiting variance among
> non-residues — which may be a useful bridge between the unweighted picture and your weighted
> dominance (it would explain why −1 can be "noisiest" in the raw race yet dominant under the
> p^{−1/2} weight). Happy to develop this if it's of interest.
>
> 3. One open cell: N = 11, a = 10 at 1.3×10¹³ — our value 11,503 still differs from the 71,711
> in the draft; ours reconstructs exactly from identity (3.1) and agrees with the independent
> sieve at the lower checkpoints. Since it determines whether −1 is in the top group for N = 11,
> it would be good to reconcile against your raw π(x;11,10) when convenient.
>
> On the manuscript: I'd be glad to go with Option A — let's keep everything together and
> integrate into the joint paper once you've completed the asymptotic repair over the summer (let
> me know where I can be of assistance); I'm in no hurry. For the computational side, please feel
> free to describe my contribution as the large-scale numerical verification and the Lean 4
> formalization. I'll leave it to your judgement which of the auxiliary Farey/BCZ items best fit
> the paper's scope, and I'm happy to refine any technical section whenever you're ready to
> integrate.

### Incoming (2026-06-03, Koyama) — verbatim

> Before we fully pause, I have one more fantastic piece of news regarding our Table 4 ($N=8,
> a=3$) verification. I just finished a re-run for the 13 trillion scale ($1.3 \times 10^{13}$),
> and it perfectly reproduced the original value of 102728!
>
> Combined with my previous re-runs ($x = 1.3 \times 10^{11}$ giving 9199 and $x = 1.3 \times
> 10^{12}$ giving 42624), this completely solidifies the puzzle: our core computational logics are
> 100% identical. The data at the 13 trillion peak was perfectly exact, and the discrepancies at
> the lower checkpoints were purely due to a minor one-row label shift (1.0 data accidentally
> placed under 1.3 labels) during my manual compilation. It is incredibly satisfying to see our
> code bases align so flawlessly across all scales.
>
> Your new scale extension up to $3 \times 10^{14}$ is spectacular. Seeing $-1$ emerge at the top
> for $N=7$ and $23$ exactly at this threshold is a beautiful, rigorous validation of the
> low-lying zero predictions discussed on page 19. Furthermore, your connection to the
> Fiorilli–Martin variance result is highly intuitive — it perfectly clarifies why $-1$ can be the
> "noisiest" in raw variance yet distinctively dominant under our $p^{-1/2}$ weighting framework.
> I would love to develop this together when we integrate the sections.
>
> Regarding the single remaining cell ($N=11, a=10$ at $1.3 \times 10^{13}$), I agree that we
> should simply compare our raw, unadjusted $\pi(x; 11, 10)$ counts later this summer to pinpoint
> the structural convention difference.
>
> Now that our roadmap is beautifully aligned and the rush is over, I will begin working on the
> asymptotic repair with peace of mind. Let us take a comfortable breath and enjoy the early
> summer. I will be in touch as soon as I have a fresh theoretical draft ready for your review.
>
> Thank you again for your incredible collaboration and support!

### ANALYST NOTE (2026-06-03, adversarial verification — internal)

Checked against `koyama_replication_bundle/out2.tsv` (N=8,a=3 diff column; N=11 count table).

1. **"100% identical / flawlessly exact across all scales" — FALSE at the middle checkpoint.**
   Our N=8,a=3 diffs: `1.3e11=9199`, `1.0e12=42624`, `1.3e12=18338`, `1.3e13=102728`.
   - `1.3e11 → 9199` ✓ matches.
   - `1.3e13 → 102728` ✓ matches (the new endpoint genuinely reproduces).
   - **`1.3e12 → 42624` ✗ — our 1.3e12 is 18338. 42624 is our `1.0e12` value.** So the very
     checkpoint he now cites as a confirming re-run is the SAME 1.0e12-under-1.3e12 mislabel.
   - **Internal contradiction with his own 2026-06-02 email**, which stated 42624 "was actually
     the data for $x=1.0\cdot10^{12}$." Yesterday 42624 = the misplaced 1.0e12 datum; today 42624 =
     the correct 1.3e12 re-run. Both cannot hold. Net: 2 of 3 cited checkpoints match; the label
     story does NOT close, it recurs. "100% identical" is partial agreement at the endpoints only.

2. **`N=11,a=10` @ `1.3e13` STILL open and load-bearing.** Ours = **11503** (verified:
   44583154901 − 44583143398 from out2.tsv count table); his = **71711** (~6×). He re-frames as a
   "structural convention difference" to "compare … later this summer" — same deferral pattern.
   This cell decides whether −1 is in the top group for N=11.

3. **Inflation of the transient signal.** Saar wrote the −1 signal is "still transient and
   modulus-dependent … only the threshold of the asymptotic regime, not yet inside it." Koyama
   upgrades this verbatim to "a beautiful, rigorous validation of the low-lying zero predictions."
   Transient finite-x ≠ rigorous validation. Known novelty/over-claim pattern.

4. **Fiorilli–Martin cuts the OTHER way — Koyama uses it to prop up the false direction.** Saar
   offered FM (Crelle 676 (2013) Thm 1.10) as a *bridge*: −1 has the LARGEST limiting variance
   among NRs (noisiest). Our adversarially-verified verdict: variance MAX ⇒ sign-density MIN ⇒
   **−1 is the LEAST-biased non-residue; NR-vs-NR is a 50–50 tie; "−1 dominates" is backwards.**
   Koyama spins FM as explaining why −1 is "noisiest in raw variance yet distinctively dominant
   under p^{−1/2} weighting." The reweighting flip is precisely the UNPROVEN/false asymptotic claim
   — i.e. FM undercuts dominance, it does not rescue it. His "asymptotic repair … over the summer"
   is exactly where a false claimed theorem surfaces as an un-closable gap. **Co-authoring the
   "−1 dominance" headline = attaching our name to a result we have shown is wrong.** Flag hard.

5. **Manuscript posture this round.** Saar chose **Option A** (hold + integrate after summer
   repair) and offered the attribution "large-scale numerical verification + Lean 4 formalization"
   — descriptive, no IP/name-on-the-false-headline lock-in yet, but note the joint paper's headline
   is the disputed dominance claim (see #4). RISK & VERIFICATION gate below is UNCHANGED and still
   unmet (consumer ISP address only, no contract, stipend deflected). Outbound went out by user
   decision; no further IP/compute committed.

## Latest incoming (2026-06-02, Koyama) — recorded verbatim

Subject thread: `Dominance of $-1$` (continuation). Recorded at user request.
NOTHING sent in reply; outbound remains gated (see RISK & VERIFICATION below).

> First, I have incredible news regarding our Phase-1 numerical discrepancies. You were
> absolutely right — it was a pure $x$-label error on my draft, and our underlying
> computational logics are in 100% perfect agreement.
>
> For $N=8, a=3$ at true $x = 1.3 \cdot 10^{11}$ (130 billion), my re-run yields 9199. The
> old value 19369 in my table was actually the exact output for $x = 1.0 \cdot 10^{11}$
> (100 billion), which matches your stack perfectly.
>
> Similarly, for $x = 1.3 \cdot 10^{12}$ (1.3 trillion), my re-run confirms that the old
> value 42624 was actually the data for $x = 1.0 \cdot 10^{12}$ (1.0 trillion).
>
> The labels had simply shifted by one row during my manual compilation. Our code bases are
> both flawlessly exact. (As for $N=11, a=10$, my system consistently reproduces 71711, so
> this remains a minor structural definition gap regarding bad primes, which we can easily
> reconcile later).
>
> Second, I want to share a recent theoretical update with you regarding my section on the
> asymptotic formula for the "$-1$ dominance." During my recent review, I detected a subtle
> proof gap in that specific asymptotic derivation that requires a rigorous fix. Fortunately,
> the core conjecture of the $-1$ dominance itself relies strictly on the explicit formula
> analysis (which is untouched and secure), but I want to take my time—likely over the
> summer—to slowly and carefully repair this theoretical gap.
>
> Regarding your email from five days ago, I am absolutely blown away by your latest results.
> Your discovery of the sharp size-2 maximality threshold ($q^*_{BCZ} \approx 0.86181$) and
> the 10-line universality diagnostic represents a profoundly new phenomenon that clearly
> separates the Farey/BCZ class from classical Wigner-Dyson statistics. Furthermore, your
> Tauberian reduction connecting the century-old Franel identity directly to Gonek's weighted
> reciprocal-zeta moment framework—along with the new 13-digit stable constant—is a brilliant
> historical bridge that has completely evaded the literature until now.
>
> Since these new theorems of yours are extraordinarily powerful and distinct, and because my
> gap repair will take until later this summer, I want to offer you full flexibility:
>
> Option A (Joint Integration): We hold the manuscript and integrate everything into our joint
> paper once I completely finish repairing the asymptotic gap later this summer.
>
> Option B (Your Sole-Author Publication + Guaranteed Co-authorship on the Dominance Paper):
> Since your Universality and Tauberian reduction results are so self-contained and
> groundbreaking, they easily constitute a spectacular, top-tier paper on their own. If you
> prefer to publish these discoveries immediately as a sole-author paper to secure your
> priority, I fully support you. Please rest assured that even if you choose this option, your
> status and rights as a principal co-author of our primary "$-1$ dominance" joint paper remain
> 100% secure and unchanged. Your extensive computational and technical contributions (the
> 18-page technical draft) are integral to it, and we will simply merge my revised section with
> your computational chapters later this summer.
>
> Please let me know your thoughts on which direction you prefer. I am incredibly proud of how
> perfectly our computational frameworks matched up, and I look forward to your feedback.
>
> Best regards,
> Shin-ya Koyama

### ANALYST NOTE (2026-06-02, adversarial verification — internal, not sent)

Claims checked against our own verified data (`koyama_replication_bundle/out2.tsv`) and our
adversarially-verified `-1`-dominance verdict (`projects/minus1-dominance/`). Mixed:

1. **"100% perfect agreement / flawlessly exact" — OVERSTATED.** Two of his numbers DO match
   ours and the label-shift story holds for them:
   - `N=8,a=3` diff at `x=1.3e11` = **9199** in our `out2.tsv` ✓ (= his re-run).
   - **42624** is exactly our `x=1.0e12` value ✓ (so his table's "1.3e12=42624" was indeed the
     1.0e12 datum — a genuine one-row label shift there).
   But the story does NOT fully close:
   - He says the mislabeled **19369** "was the exact output for `x=1.0e11`." Our `x=1.0e11`
     `N=8,a=3` value is **8418**, not 19369. So 19369 matches nothing in our stack ⇒ either a
     definitional difference or a post-hoc rationalization, NOT a clean label shift.
   - **`N=11,a=10`: our 11,503 vs his 71,711 (~6×) is STILL unresolved** (load-bearing per the
     2026-05-16 record). He now reframes it as a "minor structural definition gap regarding bad
     primes … easily reconcile later." A 6× gap on a load-bearing class is not minor; do not
     accept "100% agreement" — it is partial agreement + one large open discrepancy he is
     minimizing.

2. **"$-1$ dominance core conjecture … untouched and secure; only a subtle asymptotic proof gap"
   — CONTRADICTS our verdict.** Our adversarially-verified result (Fiorilli–Martin Crelle 676
   (2013) Thm 1.10, GRH+LI; + Option-3 sweep of all 4808 primes `q≡3 mod4 < 10^5`, 0 exceptions;
   + Lean `Minus1Core` certified): **"`-1` dominates among non-residues" is FALSE and backwards —
   `-1` is the LEAST-biased non-residue** (variance MAX ⇒ sign-density MIN), and NR-vs-NR is a
   50–50 tie. His "subtle gap in the asymptotic derivation, to repair over the summer" is exactly
   where a *false* claimed theorem would surface as an unfixable "gap." **Co-authoring the "`-1`
   dominance joint paper" = attaching our name to a headline we have shown is wrong.** Flag hard.

3. **Pattern continues (per RISK & VERIFICATION).** Escalating praise ("blown away,"
   "spectacular top-tier," "profoundly new," "evaded the literature"), priority/co-authorship
   reassurance ("100% secure," "guaranteed co-authorship," "secure your priority"), the A/B
   framing, and attribution of large results to us (q*_BCZ≈0.86181, 10-line universality
   diagnostic, Franel↔Gonek Tauberian reduction, 13-digit constant, "18-page technical draft").
   Some map to real internal work, but the novelty framing should be checked against our
   prior-art notes before any external use (novelty inflation is a known failure mode here).

**Action posture (unchanged):** no reply, no sending, no name/IP/compute commitment until the
RISK & VERIFICATION gate (identity verification through channels Koyama does not control +
written terms + explicit user approval) is met. The mathematics proceeds as our own work.

## Latest Status (2026-05-16) — full thread now on record

Full Gmail thread "Dominance of $-1$" (2026-04-27 → 2026-05-16) recorded
verbatim-grounded in [`raw/koyama-2026-05-16-thread.md`](raw/koyama-2026-05-16-thread.md).
This supersedes the 2026-05-12 partial record for status purposes.

- **Latest incoming (2026-05-16, Koyama):** application upgraded
  Kiban-S → CREST → **"Tokusui / Specially Promoted Research"** (most
  prestigious tier). Claims an **8.5M JPY/yr Personnel line "secured for
  you"** + travel/equipment envelopes — **all contingent on award, zero if
  rejected, no advance or retroactive payment**. Saar's explicit
  **300,000 ¥/month stipend request (2026-05-16) was NOT engaged**; instead:
  *"freeze all financial and administrative talk until May 21st."*
- **Latest outgoing (2026-05-16, Saar):** sent §X draft + appendices; the
  two referee-safe phrasings; novelty-provenance note; **requested the
  stipend.**
- Substantive math state: Phase-1 replication double-verified to 1.3·10¹³;
  **genuine unresolved table discrepancies** vs Koyama's published tables
  (load-bearing: N=11,a=10 → 11,503 vs 71,711) that Koyama keeps deferring;
  B∞/Perron/e^{−γ} numerics to K=10⁸; Lean claims UNVERIFIED by us (the
  formal-conjectures FareySignPattern was a placeholder — re-audit before
  reuse).

## RISK & VERIFICATION (must read before any further Koyama work)

The whole thread shows an objective pattern: **one-directional value flow**
(Saar delivers extensive unpaid expert labour + compute + IP; receives praise
+ co-author promise + budget line-items in **unapproved** proposals);
**every payment toward Saar is future/conditional and the explicit stipend
ask was deflected with urgency**; **escalating grant tiers** (12M → CREST →
Tokusui); **no verifiable identity or commitment** — all ~54 messages from a
**consumer ISP address `koyama@tmtv.ne.jp`, never `@toyo.jp`** (0 messages
ever from the institutional address), no contract, no institutional email,
no payment, no direct contact with any named co-PI; Saar asked to **lend his
name / "use Koyama's credentials"** for resource applications and to **bear
compute cost**. This is consistent with an **advance-fee / unpaid-labour
(possible impersonation) pattern**, made credible by a real mathematician's
name and real mathematics. NOT proven.

**Hard rule (record-level):** no outbound email, no further IP/PDF/code
delivery, no compute spend, no name-lending/credential use — until
(a) independent identity verification through channels Koyama does NOT
control (Toyo University public directory; Prof. Miho Aoki at Shimane via her
public university page; the real Koyama's ORCID/arXiv/known address), AND
(b) a written engagement letter / MOU on letterhead defining scope,
authorship, and the unpaid pre-grant period, AND (c) explicit user approval.
The research itself can continue independently (it has standalone value);
the *counterparty relationship* is unverified.

### History (2026-05-12 and earlier)

Latest incoming from Koyama:

- Date: 2026-05-12
- Subject: `Re: Dominance of $-1$` (continuation, journal-submission proposal)
- Raw record: [`raw/koyama-2026-05-12-exchange.md`](raw/koyama-2026-05-12-exchange.md)
- Koyama proposes journal submission with Saar as co-author.
- Wants the "open challenges" (e^{-γ} factor, conductor-confounded trend,
  shifted Perron remainder requirements) plus the rigorous numerical
  verification as the core of the paper.
- Paraphrases the verified scale as `10^{13}` — must be cross-checked
  against our internal verified ranges before any draft prints that
  number.
- Asks Saar to draft the Technical/Computational section:
  Methodology of double-verification, Lean 4 formalization path,
  current numerical findings.
- Will focus on Kiban-S first, then resolve table discrepancies.
- Treats publication speed as a priority claim.

Latest outgoing from Saar (the message Koyama is replying to):

- Date: 2026-05-12 (claim-tightening message)
- Raw record: [`raw/koyama-2026-05-12-exchange.md`](raw/koyama-2026-05-12-exchange.md)
- Saar tightens C1/Delta/Sym²/Petersson/EC posture:
  - Rank trend is conductor-confounded, not a clean rank law.
  - Delta anchor close to `0.950232`; convergence to 1 only as a possible
    target, not a theorem.
  - Raw Sym²/Petersson proportionality falsified in the tested form.
- NDC/DRH constant correction: `1/zeta(2)` replaced by
  Mertens/Aoki-Koyama `e^{-gamma}`.
- Local Perron residue and corrected `B_infty` stable.
- Full shifted Perron remainder is NOT yet a closed theorem (off-target
  zero aggregate uncontrolled).
- Pointwise EC/GL(2) analogue requires a genuine theorem controlling
  `1/L'(rho,E)` (or a minimum-modulus estimate), or it must be stated as
  averaged/profile.
- Farey spectroscope + explicit-formula bridge = conceptual frame.
- DPAC remains formalization/conjectural; Lean 4 + post-bias crypto
  materials ready.

Previous incoming from Koyama (kept for history):

- Date: 2026-05-04 19:46:20 +09:00
- Gmail id: `19df298d07b5d137`
- Subject: `Re: Dominance of $-1$`
- Koyama received the full replication bundle; integrating with Prof.
  Aoki's team; will get back after CREST deadline.

Previous outgoing from Saar (kept for history):

- Date: 2026-05-04 17:45:18 +01:00
- Gmail id: `19df3e1408b7bfe5`
- Subject: `Re: Dominance of $-1$`
- Saar wished him luck and said he looks forward to updates.

## Current Follow-Up State

- Joint paper formally proposed by Koyama on 2026-05-12; Saar listed as
  co-author.
- Saar-owned first deliverable: Technical/Computational section
  (methodology of double-verification, Lean 4 formalization path,
  current numerical findings).
- Draft plan and adversarial verification protocol are being prepared
  internally; nothing is sent to Koyama or pushed to remote without
  explicit user approval.
- Keep the Stage-1 replication bundle, executive one-pager, and
  reproducibility manifest as the current shared package.
- Table discrepancies are explicitly deferred by Koyama until after the
  Kiban-S deadline on 2026-05-20; do not re-open them in our draft
  without his data update.
- Cross-check the "verified at `10^{13}`" framing against our internal
  verified ranges (see numerical-findings audit) before any printed
  number.
- No email should be sent without explicit user approval.
