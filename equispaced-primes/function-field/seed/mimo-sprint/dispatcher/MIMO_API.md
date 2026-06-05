# MiMo API access — fill in before Day 1

Status: **awaiting credentials from user**.

## Required

- `MIMO_API_KEY` env var
- Endpoint URL (OpenAI-compatible chat completions assumed; confirm if different)
- Model name string (e.g. `mimo-rl-30b`, `mimo-math-7b-v2`, …)
- Rate limits / concurrent request cap (informs whether to dispatch A/B/C/D truly parallel or staggered)

## Test prompt (Day 0 sanity)

```
Derive the leading asymptotic coefficient C in
  LHS_n(A) = π_{1/2,K}(q^n) − Φ(M) · π_{1/2}(q^n; M, A)
        = C · log n + c + o(1)
for the cyclotomic function field K = F_2(T)(ζ_M) with M = T^3, A = 1 (the trivial unit class), assuming m(σ_A) = 0. Show the derivation in 6 lines or fewer. State the value of C.

Expected: C = +1/2  (t = dim_F_2 G/G^2 = 1, so C = (2^t − 1)/2 = 1/2 for A ∈ G^2).
```

If MiMo returns C = +1/2 with correct reasoning, dispatch Day 1 agents. If it returns a different value or off-topic reasoning, escalate to user before parallel dispatch (sanity gate).

## Fallback

If MiMo access blocked, agents B/C downgrade to local `deepseek-r1:32b` per `../../../models.yaml` (symbolic work degrades gracefully). Agents A/E (heavy numerics) downgrade to local Python execution with no LLM in the loop. Day 1/2 plan unchanged in shape; only the executor changes.
