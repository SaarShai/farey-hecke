# Draft v2: follow-up to Koyama (owner-gated; send only with owner approval)

Status: DRAFT, 2026-08-17. One ask (whole volume, with a two-range fallback),
plus a brief progress glimpse per owner instruction. Discloses direction and
the conditional payoff, but no unpublished results/constants.

---

Dear Professor Koyama,

Thank you — the §7 scan and the table of contents were exactly right, and
they have already been put to work. Your material let us isolate precisely
where the ineffectivity in Hejhal's Theorem 7.11 lives: it is confined to two
normal-families steps, and everything else in his argument carries explicit
constants. We are now building the missing quantitative ingredient (an
explicit rate for the convergence of the Hecke scattering coefficients to the
theta-group one), and the early pieces are going through formal verification.

If this succeeds, the payoff is an effective version of the Selberg–Hejhal
accumulation theorem: an explicit threshold q₀ such that every Hecke group
G_q with q ≥ q₀ provably has off-line scattering poles — which, combined with
computer-certified verification for the finitely many q below the threshold,
would upgrade the qualitative "poles appear for N sufficiently large" into a
proven law covering every non-arithmetic Hecke group. It would be, to our
knowledge, the first effective and fully certified statement of this kind,
and it grew directly out of the questions in our joint program.

One last bibliographic favor, to spare you repeated small requests: would it
be possible to send the whole of Volume 2 as a PDF, if you have it in that
form? If that is inconvenient, the only two parts we still need are:

- Chapter 6, §12 (a-priori bounds for φ(s), E(z;s;χ)), pp. 149–166 — the
  source of the constant used in §7's Lemma 7.7;
- Chapter 11, §3 (the theta group), pp. 524–532 — for equation (3.1), which
  we currently reproduce independently and would like to check against the
  printed form.

With many thanks again — the earlier scan unblocked several months' worth of
uncertainty in a single day.

Best regards,

Saar

---

## Notes for the owner (not part of the letter)

- The "formal verification" sentence refers to Aristotle v26 (P-chain
  machine-verified); deliberately vague — no constants, no ε(q) shape, no
  gap list disclosed.
- The payoff paragraph states the conditional result honestly ("if this
  succeeds") and credits the joint program — matches the two-stage
  publication strategy he referenced.
- Whole-volume ask first: ends the request cycle; fallback keeps his effort
  bounded if he only has physical copy access to scan.
- pp. 149–166 serves gap M2 (C₆ constant chain); pp. 524–532 serves the R4
  cross-check (printed eq. 3.1 vs our derived φ_∞). Both MEDIUM-HIGH value;
  neither is a hard blocker today (M2 may be provable from Appendix-E-free
  arguments; R4 is numerically self-consistent).
