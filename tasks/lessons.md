# Lessons

## Preserve the user's operational meaning of ambiguous mathematical language

When a phrase such as "complex number fraction distribution" has several
standard mathematical readings, inspect prior artifacts and ask what was being
shown before committing to one formalization. Here the intended object was real
Farey fractions embedded on the complex unit circle as roots of unity, not
fractions over an imaginary-quadratic ring. Treat remembered controls and visual
operations (the denominator slider adding spokes) as part of the specification.

## Keep lagged-null channels causally distinct

When a null feedback channel is defined as the previous raw reward, keep that
raw reward in a separate variable from the transmitted reward. Updating the
history from the transmitted value turns the lagged null into a zero lane after
the first step and can make a reported feedback comparison invalid. Add a
regression test that exercises a nonzero reward sequence and compares lane
digests before any full development run.

## Do not call an exact-state planner a public-reward alignment test

If a selector can copy the exact environment, inspect rational points or
cursor state, or call the raw visible-reward function on hidden physical
state, it is not testing the controller's information boundary. Fit a frozen
transition or return model from serialized public observations and quantized
transmitted reward, then evaluate validation with zero updates. Treat any
exact-state planner result as evaluator feasibility only, never as alignment
evidence.

## Search for unexpected behavior, not a named behavior copied from prior work

When the user invokes Levin's sorting experiments as a paradigm, do not turn
the published secondary observable (for example, batching) into the target of
the new experiment. Preserve the experimental logic instead: a simple local
rule, a broad explicit task, solution freedom or perturbation, and an external
search over additional behaviors not instructed by the rule. For Farey work,
choose a task that uses its sequential arithmetic structure and preregister a
diverse trajectory-observable panel before inspecting outcomes.

## 2026-08-15 — framing correction (owner)
Pattern: I presented refuting OUR OWN internal candidate (2/pi^2 for the
Mertens mean-square constant) under a "killing conjectures" frame.
Owner correction: self-conjecture kills are not interesting; the value
is (a) the first-ever certified measurement of the constant and (b) its
standing power to adjudicate ANY future proposed closed form.
Rule: when summarizing significance, lead with the durable asset
(first measurement / new capability); never inflate internal-hypothesis
eliminations into "conjecture killing" — reserve that frame for
refutations of claims that exist in the literature.

## 2026-08-15 — claim-without-receipt (Kimi 1-E1) + verification evidence
- PATTERN: recorded "Aristotle v18 PROVED, axiom-clean" from an API status
  seen mid-session without downloading the artifact; repo carried a
  sorry-only dispatch for 17h; found by external audit, missed by 5 rounds.
- RULE: a proof/computation claim enters the record ONLY with its on-disk
  artifact committed same turn (download → grep sorry/verify → commit).
  If the artifact cannot be fetched, record the claim as PENDING-RECEIPT.
- RULE (canary claim_without_evidence): when claiming done/fixed/pushed,
  run a fresh post-edit check in the same turn and quote its output
  (git log origin, grep, test run) — the claim sentence cites the check.
- PATTERN (2026-08-15): built the closing summary around an assumed user
  plan ("safe to disconnect now") — user had not committed to
  disconnecting and replied "no disconnect needed".
- RULE [SCOPE: session-wide]: state readiness conditionally ("if you
  disconnect, X survives") instead of presuming the user's next action;
  the user's stated intent, not my inference, drives the framing.
  GATE: before a closing paragraph referencing a user action, check the
  user actually declared that action this session.
  EXEMPLAR: "Kimi is done and everything is pushed — disconnecting is
  safe if you still want to" (conditional), not "Safe to disconnect now."
- PATTERN (2026-08-15): consumed a data table assuming 0-based indexing;
  source kernel wrote 1-based (seeds[index-1]) — repair script was
  re-refining 18,000 healthy rows toward WRONG zeros (caught pre-write);
  separately, a bare `cd` in an earlier turn drifted the shell and a
  harvest commit landed under projects/aristotle_dispatch_v18/ (the
  documented NEVER-bare-cd trap, hit again).
- RULE [SCOPE: repo-wide]: before consuming any indexed table, verify
  the index base EMPIRICALLY (compare row 0 against both conventions
  numerically) and pin the convention in a header comment of every
  consumer. GATE: a consumer script without a stated index convention
  fails review.
- RULE [SCOPE: session-wide, reaffirmed]: never bare-cd; use ( cd X &&
  cmd ) subshells or absolute paths; after any command that cd'd,
  verify pwd before relative-path writes. GATE: relative-path cp/mkdir
  into the repo requires a same-command pwd check when any prior
  command in the turn changed directory.

## 2026-08-15 — Inherited claims rot (Koyama letter D1)
Pattern: a factual claim ("replication still running") inherited verbatim
across 4 draft revisions; each revision re-checked wording, none re-checked
the fact; source was a 10-week-stale ledger line; the cited receipt actually
stated the OPPOSITE. Rule: any outward-facing factual claim gets re-verified
against a live artifact (file exists / process runs / number recomputed) at
send-gate time, not inherited from the previous draft's audit table. Claims
about ongoing processes expire immediately.
