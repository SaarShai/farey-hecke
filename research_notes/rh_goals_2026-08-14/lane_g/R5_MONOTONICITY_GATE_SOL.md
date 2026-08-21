# The whole-tail monotonicity gate: split verdict

**Date:** 2026-08-20
**Program:** `(RATE)` / R5 activation closure, lane G, lane task G4
**Branch / commit:** `codex/prime-step-review-economic-validation` @ `b875327`
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` (`python-flint` 0.9.0 / Arb, 256 bits)
**Scope:** paper-level. No finite-base computation, no Lean promotion, no
machine verification is claimed here.

## 0. Verdict in one paragraph

The gate is **not one statement**. The sources carry three inequivalent
readings of it, and they have three different truth values.

| form | statement | verdict here |
|---|---|---|
| **(G1)** fixed one-stage A0 envelope | `U(q)=K_+^(1-nu)C_R^nu q^(-alpha nu)` decreasing | **ALREADY PROVED upstream** — `R5_ACTIVATION_CLOSURE_SOL.md` §3, referee-CONFIRMED. Not mine. |
| **(G2)** fixed two-stage route-H envelope | `E_3^up(N) <= C_3 N^(-p_3)`, single crossing promotes to whole integer tail | **PROVED** here, §3, conditional on `alpha>0` and N-independent `K_+,K_F,nu_seed,omega_*`. Elementary. |
| **(G3)** general N-dependent envelope, `R5_ASSEMBLY_EXECUTION_SOL.md` (2.5) | crossing promotes to tail sup, from RATE + family-uniform `K`'s + mixing gates (1.11) | **REFUTED as stated** — §4, certified admissible counter-instance. The implication is false; the exact missing hypothesis is named in §5. |

**Net effect on the R5 closure ledger:** whole-tail monotonicity is **not an
independent blocker outside `(RATE-A)`**. Its whole residue, once
`(RATE-A)` supplies `alpha>0`, is a *finite N-independent geometry* quantity
`pi_0 <= nu_seed*omega_*` with `pi_0>0` — which is already the separately
named `N_geometry` gate, not a new one. The two named gates blocking R5
activation closure reduce to **one**: `(RATE-A)`.

Everything below that is not explicitly labelled `PROVED` remains
**`CONJECTURAL`**. Margins are rounded DOWN, upper bounds UP.

## 1. Receipts before claims

### 1.1 Source identity

```text
$ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/{DH2_RENEWAL_PROOF_SOL.md,HOLOMORPHY_GATE_SOL.md,R5_ASSEMBLY_EXECUTION_SOL.md,R5_ACTIVATION_CLOSURE_SOL.md,KF_WALL_ATTACK_SOL.md}
096d389905ad21505e2c25c30aa37b5a2fa3d3f6d054bcb30229096fc5c8d885  DH2_RENEWAL_PROOF_SOL.md
54e5df9bdaaba537b3b051cbb4ee46b4d29750c480632824120824b45888cdea  HOLOMORPHY_GATE_SOL.md
842b4a923dc71943cd933507039c087071891f4ec0aa944407cbf7bbd6f5ec14  R5_ASSEMBLY_EXECUTION_SOL.md
3b49d73d56cf963703137a6494f1f733fbb208d36c0afbe1affbd5d700ab2a53  R5_ACTIVATION_CLOSURE_SOL.md
efa518c9908e3c68005c3b7349bdee6c4af63dc7146ef85b13882560c2644aad  KF_WALL_ATTACK_SOL.md
```

The `R5_ACTIVATION_CLOSURE_SOL.md` hash `3b49d73d...` is **byte-identical**
to the hash its cold referee quotes at `R5_ACTIVATION_CLOSURE_REFEREE.md:16`.
Its `CONFIRMED` verdict therefore applies to the file as read here.

### 1.2 Constants consumed, with provenance

| symbol | value used | source | status at source |
|---|---|---|---|
| `K_+` | `117` | `KF_WALL_ATTACK_SOL.md:161-168` (Theorem A0-117) | **PROVED** (ledger: "A0 non-RATE-side `K_+<117` — **PROVED** from `C_6(13/2)` plus certified theta boundary cover") |
| `K_F` | `109` | `KF_WALL_ATTACK_SOL.md` ledger | **PROVED conditional implication** under `H_0`, anchor activation, holomorphy/reflection |
| `nu` (A0) | `0.1552 = 97/625` | `R3_TRANSPORT_EXECUTION_SOL.md:64` | **ARB-CERTIFIED in source note** |
| `alpha` | `6/5 = 1.2` | `DH2_RENEWAL_PROOF_SOL.md` (8.6) | **`CONJECTURAL`** — "At `sigma=1.1`, `alpha=1.2`. This is conditional, not a RATE theorem." |
| `d_*` | `>0.6603` | `DH2_RENEWAL_PROOF_SOL.md` §9 | raw lower endpoint `0.660309770144522190093994140625...`; the strict R5 test is `E_3(q)<0.6603` |

`alpha=1.2` is used **only as a diagnostic instance** in §4 and §6. Nothing in
§3 depends on its value, only on `alpha>0`.

## 2. Exact gate statement, quoted

**LEDGER RULE compliance.** The most-caveated phrasing is the
`HOLOMORPHY_GATE_SOL.md` §2 inventory row, not the §6 one-liner. Both are
quoted; §3–§5 are worked against the §2 row and the (2.5) definition it cites.

`HOLOMORPHY_GATE_SOL.md:288` (§2, exact gate inventory):

> | tail-monotone | A single strict crossing must be promoted to the whole
> integer tail, with all activations and the tail supremum proved. |
> `R5_ASSEMBLY_EXECUTION_SOL.md:466-487`; `DH2_RENEWAL_PROOF_SOL.md:696-732` |
> **CONJECTURAL / OPEN.** DH2's strict test is \(E_3(q)<0.6603\), but DH2,
> RATE, and the remaining R5 gates are unproved. |

`HOLOMORPHY_GATE_SOL.md:579` (§6, gate-closure ledger):

> | Positive full-boundary RATE and whole-tail monotonicity | **GENUINELY
> OPEN** | Current rigorous campaign proves only \(\alpha=0\); R5/DH2 cannot
> activate. |

and the bottom line at `HOLOMORPHY_GATE_SOL.md:583-586`:

> The remaining pincer is still open because positive RATE, its activations,
> whole-tail monotonicity, and a true finite-\(q\) scattering evaluator are
> absent.

The first cited target, `R5_ASSEMBLY_EXECUTION_SOL.md:466-487`, is the
closure-distance ledger row:

> | **R5 monotonicity / integer tail** | **`CONJECTURAL`** until the preceding
> bounds exist. | Turns a point crossing into the for-all-`N>=N0` statement and
> validates floor-plus-one strictness. | Prove the tail supremum in (2.5), all
> activation thresholds, and the selected route's non-numeric analytic gates. |

and (2.5) itself, `R5_ASSEMBLY_EXECUTION_SOL.md` §2, is the operative
definition:

> For a general monotone envelope, the exact replacement is
>
> ```text
> E_3^up(N)
>  := K_F(N)^(1-omega_*(N))
>     K_+(N)^(omega_*(N)(1-nu_seed(N)))
>     E_R(N)^(omega_*(N)nu_seed(N)),
>
> N0^(H,env)
>  := min {Q in integers : Q >= N_pre,H and
>           sup_{integer N>=Q} E_3^up(N) < d_delta}.           (2.5)
> ```
>
> If the set in (2.5) is empty or its tail supremum is not proved, the
> threshold is `+infinity` by convention and remains **`UNVERIFIABLE`**.
> Finite sampling does not prove the tail supremum.

The mixing gates the promotion is allowed to assume are (1.11),
`R5_ASSEMBLY_EXECUTION_SOL.md` §1.4:

> ```text
> E_R(N) <= K_+,
> K_+^(1-nu_seed) E_R(N)^nu_seed <= K_F                       (1.11)
> ```
>
> [...] This is **`PROVED`** by differentiating the log of the geometric mix
> with respect to `nu_seed` and `omega_*`; without (1.11), replacing harmonic
> measures by lower bounds can reverse the intended inequality. In the
> threshold ledger below, `N_monotone` includes (1.11).

Note the exact scope of what (1.11) buys: it licenses replacing `nu_seed` and
`omega_*` by **lower** bounds. It says nothing about the behaviour of
`E_3^up` along the tail. §4 shows that this distinction is load-bearing.

### 2.1 A stale-ledger finding, recorded first

`HOLOMORPHY_GATE_SOL.md` is dated 2026-08-19 01:00; `R5_ACTIVATION_CLOSURE_SOL.md`
is dated 2026-08-19 04:01 and its referee `R5_ACTIVATION_CLOSURE_REFEREE.md`
returns `CONFIRMED`. The later note states at `R5_ACTIVATION_CLOSURE_SOL.md:20-25`:

> The upper envelope used to obtain it is strictly decreasing on real `q > 0`.
> Thus one strict check at `q_transport`, together with the paper-level RATE
> theorem for every integer `q >= 12`, closes the A0 whole-tail envelope gate.
> This does **not** assert that the unknown actual error function `E_R(q)` is
> itself monotone; only its proved upper envelope is used.

and at `:504`: "| whole-tail monotonicity of `U` | **PROVED** | derivative
(3.3); no claim about `E_R` monotonicity |".

**Therefore the §6 phrase "whole-tail monotonicity ... GENUINELY OPEN" is
already superseded for the selected A0 route.** That is form (G1). This note
claims no credit for it; it is recorded so that the residual gate is scoped
correctly. What (G1) does *not* cover is the two-stage route-H envelope of
(2.5), which carries `K_F`, `omega_*`, and `d_delta` and is the object the §2
`tail-monotone` row actually cites. That is what §3–§5 address.

## 3. (G2) PROVED: the fixed two-stage route-H envelope

### 3.1 Statement

> **Lemma G2 (whole-tail promotion, fixed geometry).**
> Suppose
>
> - **(H1) `(RATE-A)`:** there exist `C_R>0`, `alpha>0`, `N_RATE` with
>   `E_R(N) <= C_R N^(-alpha)` for every integer `N >= N_RATE`;
> - **(H2) frozen geometry:** the domains `Omega_+`, `Gamma_R`, `D_0`, `D_1`,
>   `D_+` of `R5_ASSEMBLY_EXECUTION_SOL.md` §1.2–§1.4 do not depend on `N`, so
>   `nu_seed, omega_* in (0,1]` are single N-independent constants, and there
>   are N-independent family-uniform `K_+ >= 1`, `K_F >= 1` valid for all
>   `N >= N_pre,H`;
> - **(H3)** the mixing gates (1.11) hold on that tail.
>
> Put `p_3 := alpha*nu_seed*omega_* > 0` and
> `C_3 := K_F^(1-omega_*) K_+^(omega_*(1-nu_seed)) C_R^(omega_* nu_seed)`,
> exactly as in (1.9)–(1.10). Then for every integer `Q >= max(N_pre,H, N_RATE)`
>
> ```text
> sup_{integer N >= Q} E_3^up(N)  <=  C_3 Q^(-p_3),
> ```
>
> so the single strict check `C_3 Q^(-p_3) < d_delta` promotes to the whole
> integer tail, and `N_C := floor((C_3/d_delta)^(1/p_3)) + 1` is the least such
> `Q` above the activation, with strictness preserved.

### 3.2 Proof

Write `nu := nu_seed`, `om := omega_*`, both in `(0,1]` and N-independent by
(H2). By (2.5) with the constants frozen,

```text
E_3^up(N) = K_F^(1-om) K_+^(om(1-nu)) E_R(N)^(om*nu).
```

Step 1. `x |-> x^(om*nu)` is strictly increasing on `x>0` because
`om*nu>0`. By (H1), `E_R(N) <= C_R N^(-alpha)` for `N>=N_RATE`, hence

```text
E_3^up(N) <= K_F^(1-om) K_+^(om(1-nu)) (C_R N^(-alpha))^(om*nu)
          =  C_3 N^(-p_3),        p_3 = alpha*om*nu > 0.       (3.1)
```

This is exactly (1.8)–(1.10); the substitution is licensed by (H3) per the
source's own `PROVED` note on (1.11).

Step 2. `U_H(x) := C_3 x^(-p_3)` satisfies `U_H'(x) = -p_3 C_3 x^(-p_3-1) < 0`
for all real `x>0`, since `C_3>0` and `p_3>0`. So `U_H` is strictly decreasing
on `(0,infinity)`.

Step 3. For every integer `N >= Q >= N_RATE`, combining Steps 1 and 2,
`E_3^up(N) <= U_H(N) <= U_H(Q) = C_3 Q^(-p_3)`. Taking the supremum over the
integer tail gives the claim. `[]`

### 3.3 Floor-plus-one strictness

`C_3 N^(-p_3) < d_delta` iff `N > (C_3/d_delta)^(1/p_3) =: A`. If `A` happens
to be an integer, `floor(A)+1 = A+1 > A` and strictness holds; a ceiling would
return `A` itself and give equality, not strict inequality. So the source's
`floor(...)+1` in (2.2) is correct and `ceil` is not. This confirms
`R5_ASSEMBLY_EXECUTION_SOL.md`'s own remark ("The floor-plus-one is
load-bearing: it preserves strictness if a real crossing is itself an
integer. A bare ceiling is then wrong.").

### 3.4 The gate is misnamed

Lemma G2 proves the *conclusion* the gate demands, and it does so **without
proving, using, or needing** monotonicity of `E_3^up` or of `E_R`. Both may
oscillate arbitrarily. All that is required is a **decreasing majorant with a
positive exponent**, and that majorant *is* the `(RATE-A)` statement (1.1)
itself. The name "whole-tail monotonicity" invites an attack on the wrong
object. The correct name is **whole-tail majorant**. This matches the
independent framing already adopted for (G1) at
`R5_ACTIVATION_CLOSURE_SOL.md:378-381` ("This is monotonicity of `U`, not of
`E_R`").

### 3.5 Closed-form activation of `N_monotone`, and it is non-binding

The gate row demands "all activations ... proved". `N_monotone` is defined by
the source to include (1.11). Under (H1)–(H2) it has a closed form.

> **Lemma G2a.** Put `B := min(K_+, K_F^(1/nu) K_+^(1-1/nu))`. If
> `E_R(N) <= B` then both inequalities of (1.11) hold. Consequently
> `N_monotone = floor((C_R/B)^(1/alpha)) + 1`.

*Proof.* `E_R <= B <= K_+` gives (1.11a). For (1.11b),
`B <= K_F^(1/nu)K_+^(1-1/nu)` implies `B^nu <= K_F K_+^(nu-1)`, hence
`K_+^(1-nu) B^nu <= K_F`; monotonicity of `x |-> x^nu` then gives
`K_+^(1-nu)E_R^nu <= K_F`. And `C_R N^(-alpha) <= B` iff
`N >= (C_R/B)^(1/alpha)`. `[]`

Certified instance at the banked constants (`K_+=117`, `K_F=109`) and the
A0 exponent `nu=97/625`:

```text
$ /Users/za/.venvs/farey-rh/bin/python .../g4_mono2.py
backend=python-flint Arb prec_bits= 256
B_exact = K_F^(1/nu)K_+^(1-1/nu) = [74.13001442794823893527626 +/- 3.59e-24]
B_safe = 74  <  B_exact ? True
gate(1.11a) B_safe <= K_+          : True
gate(1.11b) K_+^(1-nu)B_safe^nu    = [108.97030812331422161 +/- 3.59e-18]  < K_F=109 ? True

  C_R=1     (C_R/B_safe)^(1/alpha)=[0.0276889763416575 +/- 8.04e-18]  <=1 ? True
  C_R=1.64  (C_R/B_safe)^(1/alpha)=[0.0418160917763855 +/- 1.75e-17]  <=1 ? True
  C_R=2     (C_R/B_safe)^(1/alpha)=[0.0493361470588017 +/- 1.12e-17]  <=1 ? True
  C_R=74    (C_R/B_safe)^(1/alpha)=1.00000000000000  <=1 ? True
```

`B` is rounded DOWN to the safe integer `74` (the exact value `74.1300144...`
makes (1.11b) an equality at `109`, which an interval cannot decide; at
`B_safe=74` the gate is strict with margin `>0.029`). Reading:

**With `C_R < 74`, `N_monotone = 1`.** The mixing-gate activation is
**non-binding** — it imposes nothing beyond `N>=1`. The only `C_R` values ever
proposed in the sources are `1.64` (the measured R2 cell, rounded up) and the
already-forbidden `2`; both are two orders of magnitude below `74`. So
`q_monotone` contributes nothing to
`q_0=max(12,q_RATE,q_A,q_C,q_divisor,q_monotone)` at any plausible constant.

`CONJECTURAL` caveat: `nu=0.1552` is the *A0* transport exponent. Route H's
own `nu_seed` and `omega_*` are **not determined** in any source; they are the
separately named `N_geometry` gate. Lemma G2a is stated for general `nu`; the
numeric instance above is a diagnostic at the one certified `nu` on record,
not a route-H threshold.

### 3.6 What Lemma G2 must NOT be read as

`R5_ACTIVATION_CLOSURE_SOL.md` §6 records a domain incoherence:

> ## 6. Domain correction: why `K_F=109` plus `d_*>0.6603` fails
>
> The proposed pairing is not a valid single transport ledger. The source
> records the first-zero A0 contour as the segment consumed by A0, while the
> rebuilt direct `K_F` route uses sixth-zero geometry:
> `RATE_A_REFEREE.md:326-351`.

Lemma G2 is therefore kept **symbolic in `K_F`, `nu_seed`, `omega_*`,
`d_delta`**. No numeric route-H threshold is computed here, and in particular
`K_F=109` is **not** paired with `d_*>0.6603` anywhere in §3. Doing so would
reproduce the exact error that correction names.

## 4. (G3) REFUTED: the general N-dependent envelope form

### 4.1 What is being refuted

(2.5) writes the constants as `K_F(N)`, `K_+(N)`, `nu_seed(N)`, `omega_*(N)` —
i.e. it deliberately allows N-dependent transport geometry, as a hedge against
the then-open common-pole-free-domain gate. The question is whether the
promotion still follows from the hypotheses the R5 assembly actually supplies:

- (A) `(RATE-A)`: `E_R(N) <= C_R N^(-alpha)`, `C_R>0`, `alpha>0`;
- (B) family-uniform N-independent bounds `K_+(N) <= 117`, `K_F(N) <= 109`
  (the banked constants);
- (C) the mixing gates (1.11) hold at every `N` on the tail;
- (D) a single strict crossing: `E_3^up(N_1) < d_delta` at some `N_1`.

**Claim (REFUTED).** (A)+(B)+(C)+(D) do **not** imply
`sup_{integer N>=N_1} E_3^up(N) < d_delta`. The set in (2.5) can be empty
even though the crossing (D) occurs.

### 4.2 Counter-instance

Take, for all `N`:

```text
K_F(N) = 109,   K_+(N) = 117            (the banked constants, N-independent)
E_R(N) = N^(-1.2)                        (so (A) holds with C_R=1, alpha=1.2, N_RATE=1)
omega_*(N) = 1                           (admissible: omega_* in (0,1])
nu_seed(24) = 1;   nu_seed(N) = 1/log N  for N >= 25   (admissible: in (0,1] for N>=3)
d_delta = 0.6603                         (the DH2 strict test)
```

Every quantity lies in its declared range. Then, since `omega_*=1`, the
`K_F` factor has exponent `1-omega_*=0` and

```text
E_3^up(24) = E_R(24) = 24^(-1.2),
E_3^up(N)  = 117^(1-1/log N) * (N^(-1.2))^(1/log N)
           = 117^(1-1/log N) * e^(-1.2)       for N >= 25,
```

because `(N^(-alpha))^(1/log N) = exp(-alpha * log N / log N) = e^(-alpha)`
identically. So `E_3^up(N)` is *increasing* on the tail with limit
`117*e^(-1.2)`.

### 4.3 Certified receipt

```text
$ /Users/za/.venvs/farey-rh/bin/python .../g4_mono.py
backend=python-flint Arb prec_bits= 256
=== PART 2: refutation instance for the general N-dependent envelope (2.5) ===
crossing witness  E_3^up(24) = [0.022067163355183588610 +/- 3.06e-22]  < 0.6603 ? True
  N=25       nu_seed=1/log N=[0.310667467280 +/- 1.95e-13]  E_3^up(N)=[8.02628210187062 +/- 1.50e-15]  > 0.6603 ? True
  N=30       nu_seed=1/log N=[0.294014103795 +/- 2.07e-13]  E_3^up(N)=[8.68873738228240 +/- 3.15e-15]  > 0.6603 ? True
  N=100      nu_seed=1/log N=[0.217147240952 +/- 3.75e-13]  E_3^up(N)=[12.5294391073135 +/- 3.6e-17]  > 0.6603 ? True
  N=1000000  nu_seed=1/log N=[0.0723824136505 +/- 4.20e-14]  E_3^up(N)=[24.9650361298940 +/- 3.88e-15]  > 0.6603 ? True
tail limit  K_+ * e^(-alpha) = [35.239722793727645307 +/- 4.63e-19]  > 0.6603 ? True
mixing gate (1.11b) still holds:  sup = K_+*e^(-alpha) <= K_F ? True
```

Every bound is an Arb ball at 256 bits; each displayed comparison is a
certified interval decision, not a float comparison.

**Witness values, quoted.**
Crossing at `N_1 = 24`: `E_3^up(24)` is enclosed in
`[0.022067163355183588610 +/- 3.06e-22]`, strictly below `0.6603`, so (D)
holds.
Failure at `N = 25`: `E_3^up(25)` is enclosed in
`[8.02628210187062 +/- 1.50e-15]`, strictly above `0.6603` — by a factor
above `12`. The failure recurs at **every** `N >= 25`, and the tail supremum
is `117*e^(-1.2)` enclosed in `[35.239722793727645307 +/- 4.63e-19]`, some
`53` times `d_delta`.

**(C) is not violated by the counter-instance.** (1.11a) holds since
`E_R(N) <= 1 < 117`. (1.11b) requires `K_+^(1-nu)E_R^nu <= K_F`; its
supremum over the tail is exactly `117*e^(-1.2) = 35.2397...`, certified
`<= 109` in the last line above. So the counter-instance passes the mixing
gates at every `N` and is not excluded by `N_monotone`. `[]`

### 4.4 What the refutation does and does not say

It says: **the implication asserted by (2.5)-plus-a-crossing is false from
the listed hypotheses.** (A)–(D) are logically insufficient; some further
hypothesis is mandatory, and `N_monotone` / (1.11) is demonstrably not it.

It does **not** say that the actual route-H geometry degenerates. `nu_seed(N)
= 1/log N` is an admissible instance, not a measured one. This is a
sufficiency refutation, in the standard sense: it kills the proof route, not
the conclusion.

## 5. The corrected gate

> **(UP) uniform transport positivity.** There is an explicit `pi_0 > 0` and
> an `N_geometry` with
> `nu_seed(N) * omega_*(N) >= pi_0` for every integer `N >= N_geometry`.

> **Lemma G3 (sharp form).** Assume (A), (B) with `K_+(N), K_F(N) <= Kbar`
> for some `Kbar >= 1`, (C), and **(UP)**. Let
> `N_unit := floor(C_R^(1/alpha)) + 1`, so `E_R(N) <= 1` for `N >= N_unit`.
> Then for every integer `N >= max(N_RATE, N_geometry, N_unit)`
>
> ```text
> E_3^up(N) <= Kbar * C_R^(pi_0) * N^(-alpha*pi_0),
> ```
>
> whose right side is strictly decreasing with positive exponent
> `alpha*pi_0 > 0`. Hence the whole-tail promotion of §3 goes through verbatim
> with `(C_3,p_3)` replaced by `(Kbar C_R^(pi_0), alpha*pi_0)`.

*Proof.* Write `om := omega_*(N)`, `nu := nu_seed(N)`, `pi := om*nu >= pi_0`.
Prefactor: `K_F(N)^(1-om) K_+(N)^(om(1-nu)) <= Kbar^(1-om) Kbar^(om-om*nu)
= Kbar^(1-pi) <= Kbar`, using `Kbar>=1` and `pi in (0,1]`. Error factor: for
`N >= N_unit` we have `0 < E_R(N) <= 1`, so `x |-> E_R(N)^x` is
non-increasing in the exponent, giving `E_R(N)^pi <= E_R(N)^(pi_0) <=
(C_R N^(-alpha))^(pi_0)`. Multiply. `[]`

So (UP) is **sufficient**, and §4 shows that dropping it makes the gate
false. (UP) is exactly the hypothesis the counter-instance violates:
`nu_seed(N)omega_*(N) = 1/log N -> 0`.

**(UP) is free under frozen geometry.** If `Omega_+`, `Gamma_R`, `D_0`,
`D_1`, `D_+` are N-independent — which is what
`R5_ASSEMBLY_EXECUTION_SOL.md` §1.2–§1.4 actually specifies, `D_0 :=
D(1/2+i t0, delta/15)` and `D_1 := D(1/2+i t0, delta/20)` carrying no `N` —
then `nu_seed` and `omega_*` are single numbers and `pi_0 = nu_seed*omega_*`.
Their positivity is standard: `closure(D_+) subset D_0 intersect {Re s>1/2}`
is stated as a *closed* containment in the open right half-plane, so
`dist(closure(D_+), {Re s = 1/2}) > 0`, and `D_1 subset subset D_0` since
`delta/20 < delta/15`; Harnack on the compact segment
`D_1 intersect {Re s = 1/2}` inside `D_0 \ closure(D_+)` gives `omega_* > 0`,
and likewise `nu_seed > 0` for `D_+` compactly inside `Omega_+` against the
non-degenerate boundary arc `Gamma_R`.

**Why the frozen reading is now the right one.** The (2.5) hedge existed
because a *common* pole-free domain across the family was open. That is no
longer so. `HOLOMORPHY_GATE_SOL.md` §6 itself banks:

> | No finite-\(q\) poles on full \(H_0\) or the A0/Route-B right domains |
> **PROVED FROM PRINTED THEORY** | Proposition 12.5/Claim 9.6 + note 86 leave
> only \(s=1\) on the closed right half-plane at these heights. Take
> \(q_{\rm pole}=q_{\rm divisor}=3\). |

With `q_divisor = 3` and N-independent right domains, the family shares one
frozen transport geometry, so (H2) of Lemma G2 holds and (UP) is automatic.
The residual is only the *explicit value* of `pi_0`, needed to compute a
finite `N_C` — and that is the already-named `N_geometry` gate, a finite
N-independent harmonic-measure computation, **not** an N-asymptotic problem.

## 6. Verdict

| item | verdict | exact residue |
|---|---|---|
| (G1) fixed one-stage A0 envelope decreasing | **PROVED upstream**, not here | none; `R5_ACTIVATION_CLOSURE_SOL.md` §3, referee-CONFIRMED |
| (G2) fixed two-stage route-H envelope; crossing ⇒ whole integer tail | **PROVED** (§3), conditional on `(RATE-A)` `alpha>0` + frozen geometry + banked `K_+,K_F` | `alpha>0` — i.e. `(RATE-A)` |
| floor-plus-one strictness | **PROVED** (§3.3) | none |
| `N_monotone` closed form, and `=1` for `C_R<74` at `K_+=117,K_F=109,nu=0.1552` | **PROVED / Arb-certified** (§3.5) | route-H `nu_seed,omega_*` undetermined (`N_geometry`) |
| (G3) general N-dependent envelope (2.5) from (A)+(B)+(C)+(D) | **REFUTED** (§4), certified counter-instance | — |
| corrected gate = (2.5) + **(UP)** | **PROVED sufficient** (§5) | explicit `pi_0>0` |
| "whole-tail monotonicity" as an independent blocker | **DISSOLVED** | folds into `(RATE-A)` + `N_geometry` |
| an unconditional whole-tail statement | **OPEN** | `(RATE-A)`: the campaign still proves only `alpha=0` |

**The exact missing step**, named as the brief requires: *an explicit
positive constant `pi_0 <= nu_seed*omega_*` for the frozen route-H transport
geometry, together with `alpha>0` from `(RATE-A)`.* Neither is a
monotonicity question. `pi_0` is a finite, N-independent harmonic-measure
evaluation on fixed domains; `alpha>0` is the standing `(RATE-A)` blocker.
Nothing in this note reduces `(RATE-A)`, and nothing here contradicts
`HOLOMORPHY_GATE_SOL.md` §6's judgement that the *pincer* remains open.

## 7. Blast radius

**Downstream consumers of the gate, and what changes.**

1. `HOLOMORPHY_GATE_SOL.md:288` (`tail-monotone` row, **CONJECTURAL / OPEN**)
   — the promotion and tail-supremum halves are discharged by §3 under
   `alpha>0`; the row's residue is `(RATE-A)` alone. Row is **narrowed**, not
   cleared. *No edit made; this note does not modify existing files.*
2. `HOLOMORPHY_GATE_SOL.md:579` (`Positive full-boundary RATE and whole-tail
   monotonicity`, **GENUINELY OPEN**) — the conjunction should be split. The
   second conjunct is not independently open. Already superseded for A0 by
   `R5_ACTIVATION_CLOSURE_SOL.md` (§2.1 above).
3. `HOLOMORPHY_GATE_SOL.md:580` and the onset ledgers
   `q_0=max(12,q_RATE,q_A,q_C,q_divisor,q_monotone)`
   (`R3_ROUTE_B_TRANSPORT_SOL.md:583-592`) and
   `q_0=max(12,q_RATE,q_divisor,q_transport,q_monotone)`
   (`KF_WALL_ATTACK_SOL.md:652-661`), plus the same expression at
   `C0_TRANSPORT_CAMPAIGN_SOL.md:878` and `BOUNDARY_ALPHA_THEOREM_SOL.md:667`
   — **the `q_monotone` term is removable.** By §3.5 its integer value is `1`
   at the banked constants for every `C_R<74`, hence dominated by the `12`
   already in the max. This matches the A0 finding at
   `R5_ACTIVATION_CLOSURE_SOL.md:376-381` ("monotonicity is an analytic `PASS`
   gate, not an integer `q_monotone` term") and extends it to route H.
   Removing the term does **not** define `q_RATE` or make `q_0` finite.
4. `R5_ASSEMBLY_EXECUTION_SOL.md` (2.5) — the general-envelope definition is
   **unsound as a proof obligation** without (UP): §4 shows a crossing can
   exist while the set is empty. If (2.5) is retained, (UP) must be attached.
   If the frozen reading is adopted (justified in §5 by the now-banked
   `q_divisor=3`), (2.5) collapses to (2.4) and the gate disappears.
5. `R5_ASSEMBLY_EXECUTION_SOL.md:466-487` closure-distance row "R5
   monotonicity / integer tail" — its "Prove the tail supremum in (2.5)"
   requirement is met by §3 under `alpha>0`; its "all activation thresholds"
   requirement is met for `N_monotone` in closed form by §3.5. Remaining:
   the other activations, which belong to other gates.
6. `DH2_RENEWAL_PROOF_SOL.md` §9 — unaffected. Its strict test `E_3(q)<0.6603`
   and the `q_0` **UNDEFINED / NOT CERTIFIED** verdict stand: they are blocked
   by `(DH_2)`, `(RATE-A)`, and the full `C_R`, none of which this note
   touches.
7. **Anti-consumer warning.** Nothing here licenses pairing `K_F=109` with
   `d_*>0.6603` into one ledger; `R5_ACTIVATION_CLOSURE_SOL.md` §6 records
   that as a first-zero/sixth-zero domain mismatch. §3 is symbolic in
   `K_F, d_delta` for exactly this reason.

**Not affected:** `(RATE-A)` itself, `q_RATE`, `C_R`, the finite-base block,
the true finite-`q` scattering evaluator, `(DH_2)`, and the R4 continuous
defect `d_delta>0`. This note produces no new numeric onset and no finite
`N0`.

## 8. Reproduction

```text
$ /Users/za/.venvs/farey-rh/bin/python \
    <scratchpad>/g4_mono.py     # Part 1 (exact B) and Part 2 (counter-instance)
$ /Users/za/.venvs/farey-rh/bin/python \
    <scratchpad>/g4_mono2.py    # Part 1 re-run at the rounded-DOWN safe B=74
```

Both scripts are self-contained: `from flint import arb, ctx; ctx.prec = 256`,
no repository imports, no data files. Their full text is reproduced by the
formulas in §3.5 and §4.2; every constant is quoted with its source in §1.2.

## 9. Claim ledger

| claim | status | receipt |
|---|---|---|
| the §6 "whole-tail monotonicity GENUINELY OPEN" row is stale for the A0 route | **PROVED (documentary)** | §2.1; hash match to the CONFIRMED referee |
| fixed two-stage route-H envelope: crossing ⇒ whole integer tail | **PROVED conditional on `alpha>0` + frozen geometry** | §3.2 |
| `floor(...)+1`, not `ceil`, preserves strictness | **PROVED** | §3.3 |
| the gate needs a decreasing majorant, not monotonicity of `E_3^up` or `E_R` | **PROVED** | §3.2 Step 1–3 |
| `N_monotone = floor((C_R/B)^(1/alpha))+1`, `B=min(K_+,K_F^(1/nu)K_+^(1-1/nu))` | **PROVED** | §3.5 Lemma G2a |
| `B > 74` at `K_+=117,K_F=109,nu=97/625`; `N_monotone=1` for `C_R<74` | **ARB-CERTIFIED (256 bits)** | §3.5 receipt |
| (2.5) general-envelope promotion follows from RATE + uniform `K` + (1.11) + a crossing | **FALSE** | §4.3 certified counter-instance |
| the mixing gates (1.11) suffice for the tail promotion | **FALSE** | §4.3, last line: counter-instance passes (1.11) |
| (UP) `inf nu_seed*omega_* >= pi_0 > 0` restores the promotion | **PROVED** | §5 Lemma G3 |
| (UP) is automatic under frozen N-independent geometry | **PROVED** (Harnack) | §5 |
| `q_monotone` is removable from the onset ledgers | **PROVED at the banked constants, `C_R<74`** | §3.5, §7.3 |
| route-H `nu_seed`, `omega_*`, `pi_0` values | **OPEN / UNDEFINED** | separate `N_geometry` gate |
| `alpha>0` / `(RATE-A)` | **OPEN** — untouched here | `HOLOMORPHY_GATE_SOL.md:579` |
| any finite effective `N0` or `q_0` | **UNDEFINED** | unchanged by this note |
| machine verification / Lean promotion of anything above | **NOT CLAIMED** | paper-level only |

---

**READY FOR JUDGING**

---

# Corrections after cold referee (2026-08-20)

**Referee:** `R5_MONOTONICITY_GATE_REFEREE.md`, verdict **MAJOR REVISION
REQUIRED**. Confirmed: (a) Lemma G2, (a') floor-plus-one, (b) the (2.5)
refutation, (d1) Lemma G3 sufficiency, (e1) `B > 74`. Refuted: the two ledger
claims. This section is **append-only**: no sentence above was edited or
deleted. Each block quotes the defective sentence verbatim, then states the
correction. Margins DOWN, upper bounds UP. Anything not labelled `PROVED`
stays **`CONJECTURAL`**.

**Independent re-verification performed before writing these blocks** (Arb,
`/Users/za/.venvs/farey-rh/bin/python`, 500 bits; recoded from the banked
sources, not copied from the referee):

```text
C_R banked B= 74  x= [196305680128007199620898947325.88701 +/- 1.22e-6] -> N_monotone= 196305680128007199620898947326
C_R banked B= 117 x= [134010166814705707171424895245.34677 +/- 5.00e-6] -> N_monotone= 134010166814705707171424895246
C_R' banked B= 74  x= [57585923608207602637.995006254284883 +/- 2.08e-16] -> N_monotone= 57585923608207602638
C_R' banked B= 117 x= [39311645103099547635.023994997619048 +/- 8.62e-17] -> N_monotone= 39311645103099547636
C_R= 1     x= [0.027688976341657508031 +/- 4.19e-22] -> 1
C_R= 1.64  x= [0.041816091776385482599 +/- 2.19e-22] -> 1
C_R= 2     x= [0.049336147058801711177 +/- 4.47e-22] -> 1
C_R= 74    x= 1.0000000000000000000                  -> 2
log10 B(c_0=1.827324e-5) = [-1681.2328491784551708 +/- 9.67e-19]
log10 N_monotone at B(c_0), banked C_R = [1431.8780002812989922 +/- 4.50e-17]
Bx = [74.13001442794823893527626358385043008878 +/- 4.51e-39] > 74 ? True
gate (1.11b) at B_safe=74: [108.9703081233142216135839492959900214825 +/- 3.22e-38] <= 109 ? True
```

The `B = 117` row reproduces the already-banked
`q_side = 134010166814705707171424895246`
(`R5_ACTIVATION_CLOSURE_SOL.md:289,372,502`) **digit-for-digit**, which is the
independent proof that `(C_R, alpha) = (1.0489e37, 6/5)` is the live banked
pair. Source citations re-read at their stated lines and confirmed:
`BOUNDARY_ALPHA_THEOREM_SOL.md:31,191,733,758,786`;
`C0_TRANSPORT_CAMPAIGN_SOL.md:21,118-141,180`;
`R3_R5_ASSEMBLY_PLAN_SOL.md:678`.

### Correction (2026-08-20, referee D1): (1.11)/(H3) over-attributed in §3.2 Step 1

Defective sentence (§3.2, verbatim):

> This is exactly (1.8)–(1.10); the substitution is licensed by (H3) per the
> source's own `PROVED` note on (1.11).

**Corrected statement.** (H3) is **not consumed** by this step. Substituting
`E_R(N) <= C_R N^(-alpha)` into `x |-> x^(om*nu)` requires only that a power
with positive exponent is increasing on `x>0`; it requires nothing from
(1.11). (1.11) licenses replacing *harmonic measures* by lower bounds, and
under (H2) those lower bounds are the actual infima, so nothing is replaced.
Lemma G2 is therefore true **with (H3) deleted from its hypotheses**, and is
correspondingly stronger than stated. This is a presentation defect, not a
mathematical error: the lemma as printed remains valid, since deleting an
unused hypothesis cannot falsify it.

### Correction (2026-08-20, referee D2): `N_C` is not the least `Q` above the activation

Defective sentence (§3.1, Lemma G2 statement, verbatim):

> so the single strict check `C_3 Q^(-p_3) < d_delta` promotes to the whole
> integer tail, and `N_C := floor((C_3/d_delta)^(1/p_3)) + 1` is the least such
> `Q` above the activation, with strictness preserved.

**Corrected statement.** `N_C := floor((C_3/d_delta)^(1/p_3)) + 1` is the
least integer `Q >= 1` satisfying `C_3 Q^(-p_3) < d_delta`. The least such `Q`
**above the activation** is

```text
max(N_C, N_pre,H, N_RATE).
```

The source, `R5_ASSEMBLY_EXECUTION_SOL.md` (2.4), takes this maximum
correctly; the paraphrase in §3.1 dropped it. All numeric consequences drawn
in this note used the `max` form or were `N`-free, so no downstream number
changes.

### Correction (2026-08-20, referee D3, MAJOR): `K_F = 109` is not the banked route-H constant

Defective sentences (§4.1 (B) and §4.2, verbatim):

> - (B) family-uniform N-independent bounds `K_+(N) <= 117`, `K_F(N) <= 109`
>   (the banked constants);

> ```text
> K_F(N) = 109,   K_+(N) = 117            (the banked constants, N-independent)
> ```

**Corrected statement.** The parenthetical "(the banked constants)" is
**false for route H**. `109` is the **Route-B sixth-zero direct wall**
(`KF_WALL_ATTACK_SOL.md:600`; `R5_ACTIVATION_CLOSURE_SOL.md` §6 table). The
banked `K_F` for the **two-stage route-H chain that (2.5) actually
describes** is `C0_TRANSPORT_CAMPAIGN_SOL.md:21,180`:

> \(\log K_F<57984\), producing the base \(56155\)
> `K_H<e^{57983},\quad K_F<e^{57984}.`

i.e. `K_F < e^57984`, not `109`. This is precisely the route-H/Route-B
mis-pairing that this note's own §3.6 and §7.7 warn against; §7.7 scoped the
disclosure to §3 and thereby silently exempted §4.

**What survives under the correct pairing.**

1. The **logical refutation of (G3) is unaffected.** An implication is refuted
   by any admissible tuple; §4.2's tuple is admissible under the declared
   ranges. Only the *label* was wrong. In addition, in §4.2 `omega_* = 1`
   forces the exponent `1-omega_* = 0` on `K_F`, so `K_F` is arithmetically
   inert there: no printed number in §4.3 depends on `109`.
2. §4.1 (B) must be reread as: "**an** admissible family-uniform pair
   `K_+(N) <= 117`, `K_F(N) <= 109`", with no claim that this pair is the
   banked route-H pair.
3. Any statement in this note that pairs `K_F = 109` with a route-H quantity
   — including the §3.5 numeric instance and the §6/§9 ledger rows that cite
   it — is a **diagnostic at an admissible tuple only**, and is **not** a
   route-H result. With the true `K_F < e^57984`, Lemma G2a's bound gives
   `B = min(K_+, K_F^(1/nu)K_+^(1-1/nu)) = K_+ = 117`, since the second term
   is astronomically larger; see the D6 block for the resulting threshold.

### Correction (2026-08-20, referee D4, MAJOR): `pi_0` is already banked, so (UP) is dischargeable

Defective sentences (§3.5, §6 ledger, §6 headline, §9 ledger; verbatim):

> Route H's own `nu_seed` and `omega_*` are **not determined** in any source;
> they are the separately named `N_geometry` gate.

> | route-H `nu_seed`, `omega_*`, `pi_0` values | **OPEN / UNDEFINED** | separate `N_geometry` gate |

> **The exact missing step**, named as the brief requires: *an explicit
> positive constant `pi_0 <= nu_seed*omega_*` for the frozen route-H transport
> geometry, together with `alpha>0` from `(RATE-A)`.*

**Corrected statement.** All three quantities **are determined and banked**.
`C0_TRANSPORT_CAMPAIGN_SOL.md:118-141` Arb-computes and floors them downward:

```text
nu_lower=            0.00057973351410350818959475453918595651347099957474008429...
omega_lower=         0.031564460639675570232725004080329858158939930648996164...
product_lower=       1.8298975687420986327319170475889146590449519196238760e-5
floor_product=       1.8273240000000000000000000000000000000000000000000000e-5
relative_rounding_loss_upper= 0.0014064004379588010304597836459727460974382322218138008
```

(re-run and reproduced above). The floored product `c_0 = 1.827324e-5 > 0` is
propagated into the live two-stage inequality in three banked notes:
`DH2_RENEWAL_PROOF_SOL.md:716-719` (9.2), `TWOMARK_RENEWAL_SOL.md:900-914`
(7.1), `C0_TRANSPORT_CAMPAIGN_SOL.md:201`.

Consequently:

- The §3.5 sentence "**not determined** in any source" is **withdrawn**.
- The §6/§9 ledger row "route-H `nu_seed`, `omega_*`, `pi_0` values | **OPEN /
  UNDEFINED**" is **withdrawn** and replaced by: *banked* —
  `pi_0 = 1.827324e-5` at `C0_TRANSPORT_CAMPAIGN_SOL.md:118-141`, a
  rounded-DOWN certified lower bound on `nu_seed*omega_*`.
- The §6 headline "the exact missing step is an explicit `pi_0`" is
  **withdrawn**. **(UP) is dischargeable from banked material**: taking
  `pi_0 = 1.827324e-5` and `N_geometry` from the frozen-geometry reading of
  §5, Lemma G3 applies with an explicit constant. `(UP)` is therefore not
  merely satisfiable but **instantiated**.
- The genuine residue is **not the existence of `pi_0` but its smallness
  against the `e^56155` prefactor**. `DH2_RENEWAL_PROOF_SOL.md` (9.3) /
  `TWOMARK_RENEWAL_SOL.md` (7.2) express it as
  `log q > 2.560914e9 + (5/6) log C_R`, which remains `CONJECTURAL` /
  unreachable rather than undefined.
- §0's "the two named gates blocking R5 activation closure reduce to **one**:
  `(RATE-A)`" rested on a source (`C0_TRANSPORT_CAMPAIGN_SOL.md`) that this
  note did not consult. The *conclusion* — that `N_geometry` is not an
  independent blocker — in fact survives and is strengthened, because `pi_0`
  is banked rather than open; but the *stated reason* was wrong, and the
  smallness residue above is now the operative obstruction.

### Correction (2026-08-20, referee D5): Lemma G2a asserts `=` where only `<=` is proved

Defective sentence (§3.5, Lemma G2a, verbatim):

> Consequently
> `N_monotone = floor((C_R/B)^(1/alpha)) + 1`.

**Corrected statement.**

```text
N_monotone <= floor((C_R/B)^(1/alpha)) + 1.
```

The proof of Lemma G2a establishes only that `E_R(N) <= B` is **sufficient**
for (1.11); (1.11) may hold at smaller `N`, so the displayed expression is an
upper bound on the activation, not its definition. This is harmless wherever
the quantity is used as an upper bound (all uses in this note and in the
onset ledgers, where `q_0` is a `max` of upper bounds), but the equality as
printed is wrong. The §9 ledger row asserting the equality is downgraded
accordingly.

### Correction (2026-08-20, referee D6, MAJOR): the banked `C_R` is `1.0489e37`, not `< 74`

Defective sentences (§3.5, verbatim):

> **With `C_R < 74`, `N_monotone = 1`.** The mixing-gate activation is
> **non-binding** — it imposes nothing beyond `N>=1`. The only `C_R` values ever
> proposed in the sources are `1.64` (the measured R2 cell, rounded up) and the
> already-forbidden `2`; both are two orders of magnitude below `74`. So
> `q_monotone` contributes nothing to
> `q_0=max(12,q_RATE,q_A,q_C,q_divisor,q_monotone)` at any plausible constant.

**Corrected statement.** The claim "the only `C_R` values ever proposed in the
sources are `1.64` ... and ... `2`" is **FALSE**.
`BOUNDARY_ALPHA_THEOREM_SOL.md` — one of the four onset ledgers this note
itself cites in §7.3 — banks at `:31`, `:191`, `:733` and grades in its own
claim ledger at `:685` ("Boundary RATE with \(\alpha=6/5\), \(C_R\) above,
\(q_{\rm RATE}=12\) | **PROVED here, paper-level**"):

```text
C_R  = 10489412368759562746433608215977724802   (= 1.0489e37)
C_R' =             38160259896392973127946053   (= 3.8160e25)   [:758, :786]
```

At that banked `C_R`, with `alpha = 6/5` (which this note already takes from
the same family of notes) and `B_safe = 74`, my independent Arb run above
gives

```text
N_monotone = 196305680128007199620898947326    (~1.96e29),   not 1,
```

and at the banked `C_R'`, `N_monotone = 57585923608207602638` (~5.76e19).
With the **correct route-H pairing** of the D3 block (`K_F < e^57984`, hence
`B = K_+ = 117`) the same computation gives
`N_monotone = 134010166814705707171424895246` (~1.34e29), which is
**digit-for-digit the already-banked `q_side`** of the referee-CONFIRMED
`R5_ACTIVATION_CLOSURE_SOL.md:289,372,502`. So the sources had already
computed this activation, and it is `1.34e29`, not `1`.

Two further consequences, both against this note:

1. The `C_R < 74` regime is **disjoint** from the regime the four cited onset
   ledgers actually run in — off by 28 orders of magnitude in `N_monotone`.
   The error is a scope error of a specific kind: **this note used one half of
   a banked `(alpha, C_R)` pair and substituted a hypothetical for the other
   half.**
2. `B` is severely sensitive to `nu`. At the banked route-H
   `c_0 = 1.827324e-5` (D4 block) rather than the A0 `nu = 0.1552`,
   `log10 B(c_0) = -1681.23...`, and the corresponding
   `log10 N_monotone` at the banked `C_R` is `1431.878...`. So the
   "`N_monotone = 1`" reading fails by ~1400 orders of magnitude once the
   route-H exponent is used.

**Restated conclusion, now CONDITIONAL.** The `N_monotone = 1` /
"non-binding" reading holds **only for `C_R < 74`**, a hypothesis that **no
banked source provides**. Its use here is a hypothetical, and it is graded
**`CONJECTURAL`**, not `PROVED`. `q_monotone`-removability is therefore
conditional on a future `C_R < 74`; at every banked `C_R` on record the
(1.11) activation is a large binding integer.

### Correction (2026-08-20, referee D7, MAJOR): `q_monotone` is broader than `N_monotone`

Defective sentence (§7.3, verbatim):

> — **the `q_monotone` term is removable.** By §3.5 its integer value is `1`
> at the banked constants for every `C_R<74`, hence dominated by the `12`
> already in the max.

**Corrected statement.** Even if `N_monotone = 1` were granted, removability
does **not** follow. `R3_R5_ASSEMBLY_PLAN_SOL.md:678-679` defines:

> - `q_monotone` is the point from which all envelopes used above are proved
>   monotone in the required direction.

That is **all** envelopes, not only the (1.11) mixing pair.
`R5_ASSEMBLY_EXECUTION_SOL.md:262` says only that "`N_monotone` *also*
activates (1.11)" — i.e. (1.11) is a **subset** of what `q_monotone` carries.
This note silently identified the two. Discharging (1.11) leaves the remainder
of `q_monotone` intact.

**Net: the `q_monotone`-removable claim is REFUTED on three independent
grounds** — the wrong `C_R` (D6), the wrong `nu` (D3/D6), and the wrong
identification of the term (this block). The §9 ledger row
"`q_monotone` is removable from the onset ledgers | **PROVED at the banked
constants, `C_R<74`**" is **withdrawn** and replaced by: *the (1.11) sub-gate
has a closed form and is already banked as `q_side`
(`R5_ACTIVATION_CLOSURE_SOL.md:373`); the rest of `q_monotone`
(`R3_R5_ASSEMBLY_PLAN_SOL.md:678`) is untouched by this note.*

### Correction (2026-08-20, referee D8): the §2.1 dating is filesystem mtime

Defective sentence (§2.1, verbatim):

> `HOLOMORPHY_GATE_SOL.md` is dated 2026-08-19 01:00; `R5_ACTIVATION_CLOSURE_SOL.md`
> is dated 2026-08-19 04:01

**Corrected statement.** Both files carry only `**Date:** 2026-08-19` in
their headers; neither records a clock time. `01:00` and `04:01` are `ls -l`
**mtimes on this checkout**. Mtimes are not document content, are not
preserved across clone or checkout, and are not a citable provenance for a
row graded **PROVED (documentary)**. The ordering claim survives on
*content* grounds — the closure note cites the holomorphy note — but that,
not the mtime, is the receipt. The mtime sentence is withdrawn as evidence.

### Correction (2026-08-20, referee D9): "stale" overstates a correct conjunction

Defective sentence (§9 claim ledger, verbatim):

> | the §6 "whole-tail monotonicity GENUINELY OPEN" row is stale for the A0 route | **PROVED (documentary)** | §2.1; hash match to the CONFIRMED referee |

**Corrected statement.** The `HOLOMORPHY_GATE_SOL.md:579` row reads
*"Positive full-boundary RATE **and** whole-tail monotonicity | **GENUINELY
OPEN**"*. That is a **conjunction**, and its stated reason is the first
conjunct (`alpha=0`). A conjunction with an open conjunct is open, so the row
is **correct as written, not stale**. What is superseded is only the
*implicature* that the second conjunct is independently open — which §7.2 of
this note already words correctly ("the conjunction should be split"). The
ledger row hardened §7.2 into a stronger claim than §7.2 supports, and than
§6's own concession ("nothing here contradicts `HOLOMORPHY_GATE_SOL.md`
§6's judgement"). Row downgraded from **PROVED (documentary)** to: *the row's
conjunction should be split; the row itself is not stale.*

### Correction (2026-08-20, referee D10): §4.2 itself makes the pairing §3.6 forbids

Defective sentence (§7.7, verbatim):

> §3 is symbolic in `K_F, d_delta` for exactly this reason.

**Corrected statement.** The disclosure is scoped to §3 and thereby silently
excludes §4. §4.2 does set `K_F(N) = 109` and `d_delta = 0.6603` in the
**same instance**, and calls them "the banked constants" — exactly the
first-zero/sixth-zero domain mismatch that §3.6 and
`R5_ACTIVATION_CLOSURE_SOL.md` §6 record as
**"REFUTED as a single ledger combination"** (resting on
`RATE_A_REFEREE.md:326-351`, which assigns `d_*>0.3186` to the sixth-zero
`K_F=109` chain and `d_*>0.6603` to the first-zero window).

Mitigation, stated so it is not mistaken for an excuse: because §4.2 sets
`omega_* = 1`, `K_F` carries exponent `1-omega_* = 0` and is arithmetically
inert, so no printed number in §4.3 depends on the illegal pairing. **The
defect is disclosure, not arithmetic.** The correct disclosure is: *§3 **and**
§4 must be read as symbolic in `K_F, d_delta`; §4.2's tuple is admissible for
refuting an implication but is not a ledger.*

For completeness: a sweep of the banked lane-G files containing `0.6603`
finds **no banked ledger commits this error** — the live two-stage chains
(`DH2_RENEWAL_PROOF_SOL.md` (9.2)/(9.3), `TWOMARK_RENEWAL_SOL.md`
(7.1)/(7.2), `C0_TRANSPORT_CAMPAIGN_SOL.md:127,145,201,222`) pair
`d = 0.6603` with the prefactor `e^56155`, derived from `K_F < e^57984`
(`C0:21,180`), not from `109`. The anti-consumer warning is live and violated
only by this note's own §4.2.

### Correction (2026-08-20, referee D11): the fourth ledger expression is not the same expression

Defective sentence (§7.3, verbatim):

> plus the same expression at
> `C0_TRANSPORT_CAMPAIGN_SOL.md:878` and `BOUNDARY_ALPHA_THEOREM_SOL.md:667`

**Corrected statement.** All four ledger citations exist and are correctly
located — `R3_ROUTE_B_TRANSPORT_SOL.md:586` (8.5);
`KF_WALL_ATTACK_SOL.md:654-656`; `C0_TRANSPORT_CAMPAIGN_SOL.md:878`;
`BOUNDARY_ALPHA_THEOREM_SOL.md:667` — but the last is **not the same
expression**. It reads

```text
q_0 = max{12, q_RATE, q_transport, q_divisor, q_geometry, q_monotone, ...}
```

with an additional `q_transport`, an additional `q_geometry`, and a trailing
ellipsis. "The same expression" is withdrawn; the four ledgers carry
**different** `max` expressions sharing the `q_monotone` term.

### Correction (2026-08-20, referee (c)): the §4.2 witness is out of model at the crossing; in-model replacements

Defective sentence (§4.4, verbatim, insufficient as disclosure):

> It does **not** say that the actual route-H geometry degenerates. `nu_seed(N)
> = 1/log N` is an admissible instance, not a measured one.

**Corrected statement.** The disclosure is true but incomplete: it does not
say that a banked value exists, nor how far the witness sits from it. The
§4.2 witness needs `nu_seed(24) = omega_*(24) = 1`. Both are harmonic
measures of *proper* boundary subsets seen from interior points, hence
**strictly `< 1`**; the source's declared range `0 < nu_seed <= 1` is a
convenience box, not an attainability statement. Quantitatively, with
`omega_* = 1` and `E_R = N^(-1.2)`, a crossing at `N = 24` requires

```text
(1-nu) log 117 - 1.2 nu log 24 < log 0.6603
=> nu_seed * omega_* > 0.6037001417103053033534122194079850228505
```

against banked `nu_z >= 0.1552` (A0, one stage,
`R3_TRANSPORT_EXECUTION_SOL.md:60-66`) and the route-H two-stage product
`c_0 = 1.827324e-5` (`C0_TRANSPORT_CAMPAIGN_SOL.md:118-141`). The §4.2
witness therefore sits **~4.5 orders of magnitude above** the banked route-H
transport product at the very point its crossing lives. Graded **GAPS**, not
REFUTED.

**The refutation survives repair.** The referee supplies two in-model
replacement witnesses, both keeping `d_delta = 0.6603` and `omega_* < 1`, and
both passing (1.11a) and (1.11b) at every sampled `N` and in closed form on
the tail. They are adopted here by citation
(`R5_MONOTONICITY_GATE_REFEREE.md` §3.3), not re-derived:

- **Witness R1** — `omega_* = 0.9`, `nu_seed <= 0.1552` (the certified A0
  floor), so `pi <= 0.13968`; `pi(N) = pi_1` for `N <= N_1` and
  `pi(N) = pi_1 log(N_1)/log N` for `N > N_1`. Crossing at
  `N_1 = 471626194532` with `E_3^up(N_1) = [0.660000000000 +/- 1.78e-13]
  < 0.6603`, then failure at every larger sampled `N`, tail limit
  `[1.28359535466 +/- 3.78e-12] > 0.6603`.
- **Witness R2** — fully at the banked route-H scale: `omega_* = 0.9`,
  `nu_seed <= 2.03036e-5`, so `pi <= c_0 = 1.827324e-5`. Crossing at
  `log10 N_1 = [102396.428371 +/- 1.72e-7]` with
  `E_3^up(N_1) = [0.66029000000000 +/- 1e-19] < 0.6603`, tail limit
  `[0.66034746116518 +/- 3.04e-15] > 0.6603`.

Therefore the (G3) refutation is **not an endpoint artifact** of
`omega_* = nu_seed = 1`, and is not vulnerable to an
"`omega_* = 1` is unattainable" rebuttal. Caveat carried forward from the D10
block: Witness R2 consumes `K_F` at a nonzero exponent and so is subject to
the same `K_F`/`d_*` domain caveat; it is flagged, not hidden.

### Correction (2026-08-20): corrected honest bottom line

This block supersedes §0, §6 and §9 wherever they conflict with it.

**PROVED (as scoped by the referee, independently re-derived by it).**

1. **Lemma G2** (§3.1–§3.2): under (H1) `(RATE-A)` with `alpha>0` and (H2)
   frozen geometry, a single strict crossing promotes to the whole integer
   tail with `sup_{N>=Q} E_3^up(N) <= C_3 Q^(-p_3)`. True with (H3) deleted
   (D1). Every quantifier checks.
2. **Floor-plus-one strictness** (§3.3): `floor(A)+1`, not `ceil(A)`.
3. **The gate is misnamed**: it needs a *decreasing majorant with positive
   exponent*, not monotonicity of `E_3^up` or `E_R`. Correct name:
   **whole-tail majorant**.
4. **Lemma G3** (§5): `(UP)` is **sufficient** to restore the promotion; the
   algebra `pi = om*nu >= pi_0`, prefactor `<= Kbar^(1-pi) <= Kbar`, error
   factor `E_R^pi <= (C_R N^(-alpha))^(pi_0)` is correct.
5. **`B > 74`** at `K_+=117, K_F=109, nu=97/625`, margins DOWN: confirmed to
   73 digits, including the decision to round `B` **down** to `74` because the
   exact `B` makes (1.11b) an interval-undecidable equality at `109`.
   Re-reproduced above at 500 bits.
6. **(G3) is REFUTED** as an implication from (A)+(B)+(C)+(D): confirmed, and
   **strengthened** by the referee's in-model Witnesses R1/R2. `(1.11)` is
   genuinely not the missing hypothesis.

**REFUTED (this note's two ledger claims).**

1. **`q_monotone` is removable** — refuted on three grounds (D6, D7, D3):
   the banked `C_R = 1.0489e37` gives `N_monotone ~ 1.96e29` (`B=74`) or
   exactly the banked `q_side = 1.34e29` (`B=K_+=117`, the correct route-H
   pairing), not `1`; the route-H `nu = c_0` pushes it to `10^1431.878`; and
   `q_monotone` is by definition broader than the (1.11) sub-gate.
2. **"The exact missing step is an explicit `pi_0`"** — refuted (D4):
   `pi_0 = 1.827324e-5` is banked at `C0_TRANSPORT_CAMPAIGN_SOL.md:118-141`
   and propagated into three live notes. `(UP)` is instantiated, not open.

**GAPS (right finding, overclaimed label).** (c) the §4.2 witness is out of
model at its crossing; (D5) `N_monotone` is `<=`, not `=`; (D8) the dating
receipt is an mtime; (D9) the §6 row is a correct conjunction, not stale;
(D10) §4.2 itself makes the forbidden `109`/`0.6603` pairing; (D3) the
"banked constants" label; (D11) the four ledger expressions differ.
Additionally §4.2's "(UP) is free under frozen geometry | **PROVED**
(Harnack)" is **CONFIRMED but near-vacuous**: under (H2) it restates a
positivity the source already asserts by definition
(`R5_ASSEMBLY_EXECUTION_SOL.md:88-90`, `:161-163`), and the Harnack paragraph
is a two-sentence sketch with no named inequality and no regularity or
non-emptiness check on `Omega_+`, `D_0 \ closure(D_+)`. Label downgraded to
**SKETCH**.

**OPEN.**

- `(RATE-A)` with `alpha>0`. Unchanged by this note; the rigorous campaign
  still proves only `alpha=0`. This remains the single standing blocker for
  every conditional statement above.
- The **size** residue, which replaces the withdrawn `pi_0` residue: the
  banked `pi_0 = 1.827324e-5` against the `e^56155` prefactor yields
  `log q > 2.560914e9 + (5/6) log C_R` (`DH2` (9.3), `TWOMARK` (7.2)).
  **`CONJECTURAL`** and effectively unreachable, not undefined.
- Any finite effective `N0` or `q_0`: still **UNDEFINED**. This note produces
  no new numeric onset.
- Machine verification / Lean promotion: **NOT CLAIMED** anywhere.

**Corrected consequence for the four onset ledgers**
(`R3_ROUTE_B_TRANSPORT_SOL.md:586`; `KF_WALL_ATTACK_SOL.md:654-656`;
`C0_TRANSPORT_CAMPAIGN_SOL.md:878`; `BOUNDARY_ALPHA_THEOREM_SOL.md:667`, whose
expression additionally carries `q_transport`, `q_geometry` and an ellipsis
— D11). §7.3's instruction to remove `q_monotone` is **WITHDRAWN**. The
corrected instruction is:

1. **Keep `q_monotone` in all four `max` expressions.** It is not removable
   (D7), and at every banked `C_R` its (1.11) sub-gate is a large binding
   integer, not `1` (D6).
2. **The (1.11) sub-gate of `q_monotone` has a closed form and is already
   banked**: at `(C_R, alpha) = (1.0489e37, 6/5)` and `B = K_+ = 117` it is
   `q_side = 134010166814705707171424895246`
   (`R5_ACTIVATION_CLOSURE_SOL.md:289,372,502`, referee-CONFIRMED), which my
   independent Arb run reproduces digit-for-digit. At `B_safe = 74` the
   corresponding bound is `196305680128007199620898947326`. Both are upper
   bounds on the activation, per D5.
3. **The remainder of `q_monotone`** — all other envelopes, per
   `R3_R5_ASSEMBLY_PLAN_SOL.md:678` — is **untouched** by this note and stays
   `CONJECTURAL`.
4. **No ledger edit is licensed by this note.** No file other than this one
   was modified; no onset value anywhere is changed, cleared, or narrowed by
   these corrections.

Net: the **mathematics of this note stands** (whole-tail promotion, the
misnaming, the (G3) refutation, the `B>74` receipt, `(UP)` sufficiency); the
**ledger layer does not**. `q_monotone` is not removable, `pi_0` is not the
missing step, and this note's `C_R < 74` regime is disjoint from the regime
the four cited ledgers actually run in.

---

**READY FOR JUDGING**

### Correction (2026-08-20, re-referee D12): the bare label `(RATE-A)` in the OPEN list is under-scoped

Defective sentence (§ "OPEN", verbatim):

> - `(RATE-A)` with `alpha>0`. Unchanged by this note; the rigorous campaign
>   still proves only `alpha=0`. This remains the single standing blocker for
>   every conditional statement above.

**Corrected statement.**

```text
- Positive FULL-BOUNDARY RATE, and family-uniform N-independent whole-tail
  monotonicity -- i.e. `(RATE-A) with alpha>0` in the form consumed by (G2)
  and by the R5/DH2 activation, which additionally requires N-independent
  K_+, K_F, nu_seed, omega_*. Unchanged by this note; no RIGOROUS
  (machine-certified) campaign proves alpha>0. This remains the single
  standing blocker for the conditional statements above.

  NOT open, and not what this row grades: `(RATE-A)` restricted to the single
  matched boundary Gamma_R^A with exponent 6/5 and activation q_RATE=12. That
  statement is CONFIRMED AT PAPER LEVEL (BOUNDARY_ALPHA_THEOREM_SOL.md:728-734;
  AM_REFEREE.md:7, which closes reason 1 of RATE_A_REFEREE.md:14-17). The two
  gradings are different scopes, not a conflict; cf. this note's own D9, which
  rules HOLOMORPHY_GATE_SOL.md:579 "correct as written, not stale" because it
  is a conjunction whose first conjunct is the FULL-boundary rate.
```

No ledger promotion is licensed by this correction; it narrows a label, it
does not upgrade a status.
