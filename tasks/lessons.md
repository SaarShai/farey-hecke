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
