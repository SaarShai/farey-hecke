---
agent: E
day: 2
purpose: Extend S_3 sweep on x^3 − 2 from X = 10^8 to 10^9; repeat for d_4 field
---

# Agent E — Extended S_3 / d_4 numerical sweep for D3

## Context

D3 (paired Q_8 same-disc opposite-m_ρ companion note) is checked numerically by S_3 (over `x³−2`) and D_4 (over `Q(2^{1/4}, i)`) Chebyshev-bias sweeps. AK Theorem 2.2 predicts the residuals are bounded constants. Empirically (from existing X=10⁸ runs): "X=10⁷→10⁸ confirms AK Thm 2.2 residuals are bounded constants, signs match every test."

We push to X = 10⁹ for the D3 companion note.

## Existing scripts (inlined verbatim — these run; do not modify, only extend)

### `s3_bias_1e8.gp` — S_3 over splitting field of x³−2

```gp
default(parisize, "4000M");
default(realprecision, 40);

\\ S_3 example: L = splitting field of x^3-2
\\ Classify rational primes p (unramified, p ≠ 2,3) by Frobenius in S_3:
\\   p ≡ 2 mod 3                : Frob = transposition class (size 3)
\\   p ≡ 1 mod 3, 2^((p-1)/3) ≡ 1: Frob = identity (size 1)  [split completely]
\\   p ≡ 1 mod 3, 2^((p-1)/3) ≠ 1: Frob = 3-cycle (size 2)   [inert in Q(2^{1/3})]

X = 10^8;
print("Computing primes up to X = ", X);

s_id = 0.0; s_3c = 0.0; s_tr = 0.0;
n_id = 0; n_3c = 0; n_tr = 0;

forprime(p = 5, X, {
  if(p % 3 == 2,
    s_tr = s_tr + 1.0/sqrt(p);
    n_tr = n_tr + 1
  ,
    e = (p-1)/3;
    r = lift(Mod(2, p)^e);
    if(r == 1,
      s_id = s_id + 1.0/sqrt(p);
      n_id = n_id + 1
    ,
      s_3c = s_3c + 1.0/sqrt(p);
      n_3c = n_3c + 1
    )
  )
});

\\ AK Theorem 2.2 (iii) tests (assuming m_χ = m_ψ = 0):
\\   M(1) = 3/2,  M((12)) = -1/2,  M((123)) = 0
\\ Test A: S_tr/3 - S_id ~ (1/3) loglogX
\\ Test B: S_tr/3 - S_3c/2 ~ (1/12) loglogX
\\ Test C: S_id - S_3c/2 ~ (-1/4) loglogX
\\
\\ AK Theorem 2.2 (ii) tests:
\\ S_all - 6 S_id ~ (3/2) loglogX
\\ S_all - 2 S_tr ~ (-1/2) loglogX
\\ S_all - 3 S_3c ~ 0 (constant)
```

### `d4_bias.gp` — D_4 over `Q(2^{1/4}, i)`, current X = 10⁷

```gp
default(parisize, "4000M");
default(realprecision, 40);

\\ D_4 example: L = Q(2^{1/4}, i), Galois group D_4
\\ Conjugacy classes: {1}, {r²}, {r, r³}, {s, r²s}, {rs, r³s} → sizes 1,1,2,2,2
\\ Densities: 1/8, 1/8, 1/4, 1/4, 1/4
\\
\\ Frobenius classification (p ≠ 2):
\\   p ≡ 5 mod 8                                : Frob = r       (rotation order 4)
\\   p ≡ 7 mod 8, kronecker(-2, p) == -1        : Frob = s       (refl class A)
\\   p ≡ 7 mod 8, kronecker(-2, p) == +1        : Frob = rs      (refl class B)
\\   p ≡ 3 mod 8                                : Frob = rs
\\   p ≡ 1 mod 8, 2^((p-1)/4) == 1 mod p        : Frob = 1       (split completely)
\\   p ≡ 1 mod 8, 2^((p-1)/4) != 1 mod p        : Frob = r²      (central involution)
\\
\\ AK predictions (assuming m_ρ = m_χi = 0):
\\   M(1) = 5/2, M(r²) = 1/2, M(r) = M(s) = M(rs) = -1/2,  [L:K] = 8
\\ Test (ii):
\\   σ=1:   S_all - 8 S_1   ~ (5/2)  loglogX
\\   σ=r²:  S_all - 8 S_r²  ~ (1/2)  loglogX
\\   σ=r:   S_all - 4 S_r   ~ (-1/2) loglogX
\\   σ=s:   S_all - 4 S_s   ~ (-1/2) loglogX
\\   σ=rs:  S_all - 4 S_rs  ~ (-1/2) loglogX
```

## Your task

1. **Write `s3_bias_1e9.gp`** — same sweep, X = 10⁹. Track the same buckets. Output tab-separated table of `(test_name, measured, predicted, residual)` for AK Thm 2.2 (ii)-(iii). Include `forprime(p=5, X, ...)` block from above unchanged.

2. **Bound check.** Sample the residuals at X ∈ {10⁶, 10⁷, 10⁸, 10⁹} (instrument the inner loop with checkpoints — emit a table row whenever p crosses each decade boundary). For each test, fit residual to a constant c plus bounded noise. Report c and `max|r| over X ∈ [10⁶, 10⁹]`. If `max|r| / log log X` is growing, AK Thm 2.2's "bounded" interpretation is violated — flag.

3. **Write `d4_bias_1e9.gp`** — same upgrade: X = 10⁷ → 10⁹. Same bounded-residual analysis. For the (-1/2) tests on rs/s/r (which AK predicts equal), check whether the residuals are *also* asymptotically equal or differ by some non-AK structure (this is a sanity check on m_ρ = 0).

4. **Sign matches.** For each test in (ii) and (iii), at each decade boundary, report `sign(measured) == sign(predicted)`. Report match percentage.

5. **Wallclock estimate.** Single-core PARI/GP `forprime(p=5, 10⁹, ...)` is roughly 5–15 min depending on per-prime work. If realised wallclock exceeds 60 min, downscope to X = 3×10⁸ and clearly mark; do not extrapolate.

## Output format

```json
{
  "s3_x3_minus_2": {
    "script_path": "projects/ak-bias-followups/d3-central-zero-map/s3_bias_1e9.gp",
    "script_contents": "<full GP script as a string>",
    "X_max": 1000000000,
    "wallclock_s": ...,
    "decade_table": [
      {"X": 1e6, "test_A_measured": ..., "test_A_predicted": ..., "test_A_resid": ..., "...": "..."},
      {"X": 1e7, ...},
      {"X": 1e8, ...},
      {"X": 1e9, ...}
    ],
    "residual_constants": {
      "test_A": {"c": ..., "max_abs_r": ...},
      "test_B": {"c": ..., "max_abs_r": ...},
      "test_C": {"c": ..., "max_abs_r": ...},
      "test_iia": {"c": ..., "max_abs_r": ...},
      "test_iib": {"c": ..., "max_abs_r": ...},
      "test_iic": {"c": ..., "max_abs_r": ...}
    },
    "bounded_verdict": "BOUNDED" | "GROWING_LIKE_<form>",
    "sign_match_pct_overall": ...
  },
  "d4_field": { ...same shape... },
  "blocker": null | "<one-line if bounded_verdict not BOUNDED or sign_match_pct < 95%>"
}
```

## Norms

- The script content you produce in `script_contents` must be runnable as-is with PARI/GP (`gp -q script.gp`).
- Re-running existing 10⁸ output: include a slice at X=10⁸ in the decade_table; values should be within ~1e-6 of existing output (these are deterministic, not Monte-Carlo).
- If wallclock-prohibitive, mark X_max accordingly and do not fabricate decade rows.
- Do **not** invent numerical results. If you can't execute the script, output `"X_max": null, "needs_execution": true` and stop — the orchestrator will run it locally.
