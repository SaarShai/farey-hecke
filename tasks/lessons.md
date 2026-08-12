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
