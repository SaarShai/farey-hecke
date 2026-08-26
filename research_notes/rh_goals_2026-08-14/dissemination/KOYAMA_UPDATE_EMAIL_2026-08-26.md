# DRAFT — reply to Koyama (2026-08-26). NOT SENT. Owner reviews, edits, sends.

Subject: Re: effective accumulation theorem — and a two-pin update

Dear Professor Koyama,

Thank you for the kind words — the §7 material really did unblock the
bottleneck, and your reading of it helped us see which part carries the
weight.

Since my last message the project has closed a milestone I want to share,
because it changes the shape of the no-go side of the program.

1. A second off-line zero of the Selberg zeta function of G_5 is now
   rigorously localized: Re(s2) in [0.41054273549473627, 0.41054473549473627],
   Im(s2) in [7.81976724701551188, 7.81976924701551188], by the same
   certified argument-principle contour method as the first pin (winding
   number 1, so the zero is simple). The assembly passed two independent
   adversarial referee passes this week.

2. The two certified real parts are provably distinct (interval gap
   >= 0.0433494...), which yields a statement one pin could never give:
   the nonreal strip zeros of Z_{G_5} lie on NO single vertical line
   Re(s) = c, for any c. The purely logical core of this step is
   machine-verified in Lean 4 (axiom-clean).

3. Via the completed-zeta divisor structure (Friedman–Jorgenson–Smajlović)
   and the one-cusp scalar specialization, the two pins transport to two
   zeros of the scattering determinant phi_5 with distinct real parts in
   (1/2, 1). This discharges what we had called the open problem of the
   no-go framework: the axiom list A (the analytic properties phi_q shares
   with completed zeta) does not entail P_line(c) for ANY c — one common
   countermodel defeats every candidate line simultaneously, uncondition-
   ally. Since RH is exactly P_line(3/4) for the arithmetic member, this
   is now the precise, referee-checked form of the slogan that a proof of
   RH cannot come from the shared analytic properties alone. The result is
   computer-assisted and citation-backed (FJS, Möller–Mayer–Strömberg);
   the dependency ledger is explicit.

On the effective accumulation theorem with explicit q_0: that lane is
unchanged and remains the conditional program you described — the eight
named gates are still open, and nothing above shortcuts them. The two-pin
result is complementary: it fixes the negative boundary of what the
generic machinery can prove, while the effective theorem is the positive
side for the actual family.

I would be glad to send the two assembly documents and the referee
reports if you would like to look at the details, and I would value your
judgment on where the two-pin statement best fits relative to our joint
draft.

With best regards,
Saar
