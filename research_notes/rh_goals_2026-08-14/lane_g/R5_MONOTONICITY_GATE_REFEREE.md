# MAJOR REVISION REQUIRED

**Date:** 2026-08-20
**Scope:** cold adversarial referee of `R5_MONOTONICITY_GATE_SOL.md`.
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` (`python-flint` / Arb, 256-400 bits).
**Independence:** every number below was recoded from the target's stated
parameters. No script, receipt, or intermediate value was copied from the
target. All sources were re-read at the hashes recorded in §1.

**Verdict:** the target's two *mathematical* theorems (Lemma G2 and its
floor-plus-one corollary; the Lemma G3 sufficiency of `(UP)`) are
**CONFIRMED**. Its *refutation* of the general (2.5) implication is
**CONFIRMED and strengthened** — I supply a second witness that survives full
in-model restriction, which the target's witness does not. But the target's
two *ledger* claims are **REFUTED**: `q_monotone` is **not** removable (the
banked `C_R` is `1.0489e37`, not `<74`, and the correct `N_monotone` is
exactly the already-banked `q_side = 1.34e29`), and the "exact missing step
is an explicit `pi_0`" headline is **REFUTED** because `pi_0 = 1.827324e-5`
is already banked at `C0_TRANSPORT_CAMPAIGN_SOL.md:127-141`.

## 0. Target identity

```text
$ shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/R5_MONOTONICITY_GATE_SOL.md
```
Read at branch `codex/prime-step-review-economic-validation`, HEAD `8405112`
("Add monotonicity gate split-verdict note (unrefereed)"). The target's
header says `@ b875327`; `b875327` is the grandparent of the commit that
introduced the target. Not a defect, but the header commit is not the commit
the note lives in.

All five source hashes in the target's §1.1 **reproduce byte-for-byte**:

```text
096d389905ad21505e2c25c30aa37b5a2fa3d3f6d054bcb30229096fc5c8d885  DH2_RENEWAL_PROOF_SOL.md
54e5df9bdaaba537b3b051cbb4ee46b4d29750c480632824120824b45888cdea  HOLOMORPHY_GATE_SOL.md
842b4a923dc71943cd933507039c087071891f4ec0aa944407cbf7bbd6f5ec14  R5_ASSEMBLY_EXECUTION_SOL.md
3b49d73d56cf963703137a6494f1f733fbb208d36c0afbe1affbd5d700ab2a53  R5_ACTIVATION_CLOSURE_SOL.md
efa518c9908e3c68005c3b7349bdee6c4af63dc7146ef85b13882560c2644aad  KF_WALL_ATTACK_SOL.md
```

The `3b49d73d...` hash **does** match `R5_ACTIVATION_CLOSURE_REFEREE.md:16-18`,
whose banner is `# CONFIRMED`. Target §1.1 CONFIRMED.

Every block quotation in the target's §2, §2.1, §3.6 was checked against its
source line and is **verbatim**.

## 1. Per-claim verdict table

| # | claim | verdict |
|---|---|---|
| (a) | Lemma G2: crossing promotes to whole integer tail, fixed two-stage envelope | **CONFIRMED** (minor over-attribution, §2) |
| (a') | `floor(...)+1`, not `ceil`, preserves strictness | **CONFIRMED** (§2.2) |
| (b) | (2.5) + RATE + uniform `K` + (1.11) + a crossing does **not** imply the tail bound | **CONFIRMED**, and strengthened (§3) |
| (b') | the witness's constants are "the banked constants" | **REFUTED** (§3.3) — route-H's banked `K_F` is `e^57984`, not `109` |
| (c) | witness is in-model | **GAPS** (§3.2) — the target's witness needs `nu_seed*omega_* > 0.6037` at the crossing; the banked route-H value is `1.827324e-5`. Refutation survives; I supply an in-model witness. |
| (d1) | Lemma G3: `(UP)` is sufficient | **CONFIRMED** (§4) |
| (d2) | `(UP)` is free under frozen geometry | **CONFIRMED but near-vacuous** (§4.2) |
| (d3) | "the exact missing step is an explicit `pi_0`"; route-H `nu_seed,omega_*` "are **not determined** in any source" | **REFUTED** (§4.3) |
| (e1) | `B > 74` at `K_+=117,K_F=109,nu=97/625`, margins down | **CONFIRMED to 73 digits** (§5.1) |
| (e2) | `N_monotone = floor((C_R/B)^(1/alpha))+1` | **GAPS** — sufficiency only, not equality (§5.2) |
| (e3) | `N_monotone = 1` for `C_R < 74` | **CONFIRMED as arithmetic**, vacuous in scope (§5.3) |
| (e4) | `q_monotone` is removable from four onset ledgers | **REFUTED** (§5.3, §5.4) |
| (f) | HOLOMORPHY §6 row is "stale" for A0 | **GAPS** (§6) — quotes correct, "stale" overstated, dating is filesystem mtime |
| (g) | anti-consumer warning `K_F=109` + `d_*>0.6603` | **CONFIRMED as a rule**, **VIOLATED by the target's own §4.2** (§7) |

## 2. (a) Lemma G2 re-derived independently — CONFIRMED

I re-derived Lemma G2 from `R5_ASSEMBLY_EXECUTION_SOL.md` (1.1), (1.8)-(1.11),
(2.2), (2.5) without reading the target's §3.2.

Under (H2) the constants are N-free, so (2.5) collapses to
`E_3^up(N) = K_F^(1-om) K_+^(om(1-nu)) E_R(N)^(om*nu)`. With `om,nu in (0,1]`,
`om*nu > 0`, so `x -> x^(om*nu)` is strictly increasing on `x>0`; (H1) gives
`E_R(N) <= C_R N^(-alpha)` for `N >= N_RATE`; hence
`E_3^up(N) <= C_3 N^(-p_3)` with `C_3, p_3` exactly (1.9)-(1.10). `C_3 > 0`
because `K_F, K_+ >= 1` and `C_R > 0`. `U_H(x) = C_3 x^(-p_3)` has
`U_H' = -p_3 C_3 x^(-p_3-1) < 0`, so for integer `N >= Q >= max(N_pre,H,N_RATE)`,
`E_3^up(N) <= U_H(N) <= U_H(Q)`. Supremum over the integer tail gives the
claim. **Every quantifier checks. CONFIRMED.**

**Where "frozen geometry" is used, and whether it is available.** (H2) is used
in exactly one place — collapsing `K_F(N),K_+(N),nu_seed(N),omega_*(N)` to
constants. It is *assumed*, not derived, and Lemma G2 states it as a
hypothesis. That is honest. The target's separate argument (§5, "the frozen
reading is now the right one") that (H2) is *available* is a different claim
and is graded at §4.2 below.

**Defect D1 (minor, over-attribution).** Target §3.2 Step 1: "the substitution
is licensed by (H3) per the source's own `PROVED` note on (1.11)". False
attribution. Substituting `E_R(N) <= C_R N^(-alpha)` into `x^(om*nu)` needs
only monotonicity of a power, not (1.11). (1.11) licenses replacing *harmonic
measures* by lower bounds — which under (H2) are the actual infima, so (H3) is
not consumed by Lemma G2 at all. Lemma G2 is true with (H3) deleted. This
makes the lemma *stronger*, so it is a presentation defect, not an error.

**Defect D2 (minor, phrasing).** "`N_C := floor((C_3/d_delta)^(1/p_3)) + 1` is
the least such `Q` above the activation". `N_C` is the least integer `Q>=1`
with `C_3 Q^(-p_3) < d_delta`; the least such `Q` *above the activation* is
`max(N_C, N_pre,H, N_RATE)`. The target's own source (2.4) does the max
correctly; the target's sentence does not.

### 2.2 Floor-plus-one — CONFIRMED

`p_3 > 0`, so `C_3 N^(-p_3) < d_delta  <=>  N^(p_3) > C_3/d_delta  <=> N > A`
with `A := (C_3/d_delta)^(1/p_3)`. If `A in Z` then `floor(A)+1 = A+1 > A`
(strict) while `ceil(A) = A` gives equality. If `A notin Z` both agree.
**CONFIRMED**; matches `R5_ASSEMBLY_EXECUTION_SOL.md:290-292` verbatim.

## 3. (b) The (2.5) refutation — CONFIRMED, and strengthened

### 3.1 Independent replay of the target's witness

Recoded from the target's §4.2 parameters only (`K_F=109, K_+=117,
E_R(N)=N^(-1.2), omega_*=1, nu_seed(24)=1, nu_seed(N)=1/log N` for `N>=25`,
`d_delta=0.6603`), Arb 256 bits:

```text
E_3^up(24) = [0.02206716335518358861030572361373789460235554859337921933506 +/- 3.50e-78]  < 0.6603 ? True
  N=25             nu=[0.31066747 +/- 2.73e-9]  E3up=[8.02628210187 +/- 6.23e-13]  >0.6603? True  (1.11b) LHS <=109? True  (1.11a) ER<=K+? True
  N=26             nu=[0.30692768 +/- 3.58e-9]  E3up=[8.17050692634 +/- 4.64e-12] >0.6603? True  (1.11b) <=109? True  (1.11a) True
  N=30             nu=[0.29401410 +/- 3.80e-9]  E3up=[8.68873738228 +/- 2.40e-12] >0.6603? True  (1.11b) <=109? True  (1.11a) True
  N=100            nu=[0.21714724 +/- 9.52e-10] E3up=[12.5294391073 +/- 1.36e-11] >0.6603? True  (1.11b) <=109? True  (1.11a) True
  N=10^6           nu=[0.072382414 +/- 3.50e-10] E3up=[24.9650361299 +/- 6.01e-12] >0.6603? True  (1.11b) <=109? True  (1.11a) True
  N=10^12          nu=[0.036191207 +/- 1.75e-10] E3up=[29.6607645342 +/- 6.70e-12] >0.6603? True  (1.11b) <=109? True  (1.11a) True
tail limit K_+*e^-1.2 = [35.23972279372764530746238002873702781663324203614910234 +/- 5.17e-75]  >0.6603 ? True   <=109 ? True
nu_seed in (0,1] for N>=25 ? True True
```

The crossing at `N=24`, the failure at `N=25,26,30,100,10^6,10^12`, the tail
limit `117 e^(-1.2)`, and the closed-form identity
`(N^(-alpha))^(1/log N) = e^(-alpha)` all **reproduce exactly**. I added
`N=26` and `N=10^12`, which the target did not sample; the failure holds
there too, and the closed form makes it hold at every `N>=25`.

**Side conditions genuinely pass.** (1.11a): `E_R(N) <= 1 < 117` at every `N`,
checked. (1.11b): because `omega_*=1`, the (1.11b) left side coincides with
`E_3^up`, so its tail supremum is `117 e^(-1.2) = 35.2397... <= 109`, checked
in intervals at every sampled `N` and in closed form on the tail. **The
counter-instance does not quietly violate (1.11).** The logical refutation of
(A)+(B)+(C)+(D) => tail bound is **CONFIRMED**.

### 3.2 (c) IN-MODEL check — the target's witness is out of model at the crossing

The witness needs `nu_seed(24) = omega_*(24) = 1`. Both are harmonic measures
of *proper* boundary subsets viewed from interior points, so both are `< 1`
strictly; the source's own declared range `0 < nu_seed <= 1` is a convenience
box, not an attainability statement.

I quantified how much slack there is. With `omega_* = 1` and `E_R=N^(-1.2)`,
a crossing at `N=24` requires

```text
(1-nu) log 117 - 1.2 nu log 24 < log 0.6603
=> nu_seed * omega_* > 0.6037001417103053033534122194079850228505
```

Against this, the sources bank:

- `R3_TRANSPORT_EXECUTION_SOL.md:60-66` (A0, one stage): `nu_z >= 0.1552`;
- `C0_TRANSPORT_CAMPAIGN_SOL.md:118-141` (route H, two stages, **the object
  (2.5) describes**): `nu_lower = 0.000579733...`, `omega_lower = 0.0315644...`,
  `product_lower = 1.8298975687e-5`, floored to `c_0 = 1.827324e-5`.

So the target's witness sits **~4.5 orders of magnitude** above the banked
route-H transport product at the very point where its crossing lives. Graded
**GAPS**, not REFUTED, because the target says so itself at §4.4 ("an
admissible instance, not a measured one") — but the target does not disclose
that the banked value exists, nor how far away it is.

### 3.3 An in-model witness — the refutation survives repair

I built two replacements. Both keep `d_delta = 0.6603`.

**Witness R1** (`omega_* = 0.9 < 1`, `nu_seed <= 0.1552` = the certified A0
floor, so `pi <= 0.13968`). Set `pi(N) = pi_1` for `N <= N_1` and
`pi(N) = pi_1 log(N_1)/log N` for `N > N_1` (decreasing, in `(0,1]`):

```text
prefactor 109^0.1 * 117^(0.9*0.8448) = [59.73456758 +/- 3.44e-9]
N1 = 471626194532
crossing  E_3^up(N1) = [0.660000000000 +/- 1.78e-13]  < 0.6603 ? True
  N=10^12.67  E3up=[0.695565623401 +/- 2.82e-13] >0.6603? True  (1.11b) <=109? True
  N=10^23.35  E3up=[0.920419977007 +/- 3.74e-13] >0.6603? True  (1.11b) <=109? True
  N=10^58.37  E3up=[1.12370236907 +/- 2.68e-12] >0.6603? True  (1.11b) <=109? True
  N=10^300    E3up=[1.25079770778 +/- 4.28e-12] >0.6603? True  (1.11b) <=109? True
tail limit = [1.28359535466 +/- 3.78e-12]  > 0.6603 ? True
```

**Witness R2** (fully at the banked route-H scale: `omega_* = 0.9`,
`nu_seed <= 2.03036e-5`, so `pi <= c_0 = 1.827324e-5`):

```text
prefactor= [116.164153737 +/- 1.56e-10]   log10 N1 = [102396.428371 +/- 1.72e-7]
crossing  E_3^up(N1) = [0.66029000000000 +/- 1e-19]  < 0.6603 ? True
  log10 N = 2.048e5  E3up=[0.66031872995756 +/- 4.81e-15] >0.6603? True  (1.11b)=[0.374408 +/- 3.44e-7] <=109? True
  log10 N = 1.024e6  E3up=[0.66034171482365 +/- 9.59e-16] >0.6603? True  (1.11b) <=109? True
  log10 N = 1.024e8  E3up=[0.66034740370152 +/- 1.67e-16] >0.6603? True  (1.11b) <=109? True
tail limit = [0.66034746116518 +/- 3.04e-15]  > 0.6603 ? True
ratio limit/crossing = [1.00008702413 +/- 3.62e-12]
```

Both pass (1.11a) and (1.11b) at every sampled `N` and in closed form on the
tail; both keep `omega_* < 1` and `nu_seed` at or below a banked figure. The
**(G3) refutation is therefore CONFIRMED and is not an endpoint artifact.**

### 3.4 Defect D3 — the witness's constants are mislabelled

Target §4.2 line 321: `K_F(N) = 109, K_+(N) = 117  (the banked constants,
N-independent)`, and §4.1 (B): "family-uniform N-independent bounds
`K_+(N) <= 117`, `K_F(N) <= 109` (the banked constants)".

**REFUTED.** `109` is the *sixth-zero Route-B direct wall*
(`KF_WALL_ATTACK_SOL.md:600`, `R5_ACTIVATION_CLOSURE_SOL.md` §6 table). The
banked `K_F` for the **two-stage route-H chain that (2.5) actually describes**
is `C0_TRANSPORT_CAMPAIGN_SOL.md:21,180`:

> \(\log K_F<57984\), producing the base \(56155\)
> `K_H<e^{57983},\quad K_F<e^{57984}.`

`e^57984`, not `109`. The parenthetical "(the banked constants)" is false for
route H. The refutation logic is unaffected (any admissible tuple refutes an
implication) — but the label is wrong, and it is the same mis-pairing the
target itself flags as an anti-consumer error (see §7).

## 4. (d) The corrected gate `(UP)`

### 4.1 Lemma G3 sufficiency — CONFIRMED

Re-derived independently. `pi := om*nu >= pi_0`. Prefactor exponents sum:
`(1-om) + om(1-nu) = 1 - om*nu = 1 - pi`, so with `Kbar >= 1` and
`pi in (0,1]`, `K_F(N)^(1-om) K_+(N)^(om(1-nu)) <= Kbar^(1-pi) <= Kbar`.
Error factor: for `N >= N_unit = floor(C_R^(1/alpha))+1` we have
`E_R(N) <= C_R N^(-alpha) <= 1`, and `t -> E_R(N)^t` is non-increasing on a
base in `(0,1]`, so `E_R(N)^pi <= E_R(N)^(pi_0) <= (C_R N^(-alpha))^(pi_0)`.
Product gives `E_3^up(N) <= Kbar C_R^(pi_0) N^(-alpha pi_0)`, decreasing with
positive exponent `alpha pi_0`. Lemma G2 then applies verbatim.
**CONFIRMED.** (Degenerate `E_R(N)=0` is not covered by the stated "`0 <
E_R(N)`" but is trivially fine.)

`(UP)` is indeed exactly what Witnesses D/R1/R2 violate:
`nu_seed*omega_* -> 0`. **The diagnosis is right.**

### 4.2 "(UP) is free under frozen geometry" — CONFIRMED but near-vacuous

Under (H2) — frozen domains — `nu_seed` and `omega_*` are single numbers and
`pi_0 := nu_seed*omega_*`. This is a restatement, not a theorem: `(UP)`
reduces to positivity of two constants that the *source already asserts by
definition*, `0 < nu_seed <= 1` at `R5_ASSEMBLY_EXECUTION_SOL.md:88-90` and
`0 < omega_* <= 1` at `:161-163`. The target's Harnack paragraph re-derives an
assumption. It is also a sketch (no named Harnack inequality, no regularity /
non-emptiness check on `Omega_+`, `D_0 \ closure(D_+)`). Ledger row "(UP) is
automatic under frozen N-independent geometry | **PROVED** (Harnack)"
overstates a two-sentence sketch of a definitional fact. **GAPS on the label,
not on the content.**

### 4.3 Defect D4 (MAJOR) — the "exact missing step" already exists

Target §3.5:

> Route H's own `nu_seed` and `omega_*` are **not determined** in any source

Target §6 ledger:

> | route-H `nu_seed`, `omega_*`, `pi_0` values | **OPEN / UNDEFINED** |

Target §6 headline:

> **The exact missing step**, named as the brief requires: *an explicit
> positive constant `pi_0 <= nu_seed*omega_*` for the frozen route-H transport
> geometry* [...]

**REFUTED.** `C0_TRANSPORT_CAMPAIGN_SOL.md:118-141` computes all three in Arb
and floors them downward:

```text
nu_lower=            0.00057973351410350818959475453918595651347099957474008429...
omega_lower=         0.031564460639675570232725004080329858158939930648996164...
product_lower=       1.8298975687420986327319170475889146590449519196238760e-5
floor_product=       1.8273240000000000000000000000000000000000000000000000e-5
relative_rounding_loss_upper= 0.0014064004379588010304597836459727460974382322218138008
```

and that floored product is propagated as `c_0 = 1.827324e-5` into the live
two-stage inequality in **three** banked notes:
`DH2_RENEWAL_PROOF_SOL.md:716-719` (9.2), `TWOMARK_RENEWAL_SOL.md:900-914`
(7.1), `C0_TRANSPORT_CAMPAIGN_SOL.md:201`. So an explicit `pi_0 > 0` for
route H **is on the ledger**, and `(UP)` is not merely satisfiable but
instantiated. The target's headline residue is therefore mis-stated, and its
"blocking gates reduce to one" paragraph (§0) rests on a source it did not
consult. The genuine residue is not the *existence* of `pi_0` but its
*smallness against the `e^56155` prefactor*: `DH2` (9.3) /
`TWOMARK` (7.2) give `log q > 2.560914e9 + (5/6) log C_R`.

## 5. (e) The `B > 74` arithmetic and its scope

### 5.1 `B` — CONFIRMED to 73 digits

```text
prec 256
K_F^(1/nu)K_+^(1-1/nu) = [74.130014427948238935276263583850430088784504319106364430549115708872172962 +/- 3.50e-73]
Bx > 74 ?  True        Bx < 74.14 ?  True
gate 1.11a  B_safe=74 <= K_+ : True
gate 1.11b  K_+^(1-nu)*74^nu = [108.9703081233142216135839492959900214825321025609559420073917841157410838015 +/- 5.33e-74]  <= 109 ? True
            margin              [0.0296918766857783864160507040099785174678974390440579926082158842589161985 +/- 5.33e-74]
at exact Bx, K_+^(1-nu)Bx^nu = [109.000000000000000000000000000000000000000000000000000000000000000000000 +/- 8.17e-74]
```

The target's `74.13001442794823893527626 +/- 3.59e-24`, its `B_safe = 74`
rounding-DOWN discipline, its `108.97030812331422161` and its
"margin `>0.029`" all **reproduce exactly at higher precision**. The
observation that the exact `B` makes (1.11b) an equality (so an interval
cannot decide it) is **CONFIRMED** — my run shows the ball straddling `109`
with radius `8.17e-74`. Rounding down to `74` is the correct move. **§3.5's
Part 1 is fully CONFIRMED.**

Lemma G2a's algebra is also correct: `B <= K_F^(1/nu)K_+^(1-1/nu)` gives
`B^nu <= K_F K_+^(nu-1)` hence `K_+^(1-nu)B^nu <= K_F`; `x -> x^nu` increasing
transfers it to `E_R`.

### 5.2 Defect D5 — `N_monotone = ...` should be `N_monotone <= ...`

Lemma G2a states an **equality**. Its proof establishes only that `E_R(N)<=B`
is *sufficient* for (1.11). (1.11) can hold at smaller `N`. The correct
statement is `N_monotone <= floor((C_R/B)^(1/alpha))+1`. Harmless for an
upper bound; wrong as written.

### 5.3 Defect D6 (MAJOR) — the `C_R` scope error, nailed

Target §3.5:

> **With `C_R < 74`, `N_monotone = 1`.** The mixing-gate activation is
> **non-binding** [...] The only `C_R` values ever proposed in the sources are
> `1.64` (the measured R2 cell, rounded up) and the already-forbidden `2`;
> both are two orders of magnitude below `74`.

The italicised sentence is **FALSE**. `BOUNDARY_ALPHA_THEOREM_SOL.md` — a file
the target itself cites at its own line 482 as one of the four onset ledgers —
banks, at `:31`, `:191`, `:733` and in its claim ledger at `:685`
("Boundary RATE with \(\alpha=6/5\), \(C_R\) above, \(q_{\rm RATE}=12\) |
**PROVED here, paper-level**"):

```text
C_R = 10489412368759562746433608215977724802          (= 1.0489e37)
C_R'=              38160259896392973127946053          (= 3.8160e25)   [:758, :786]
```

Arb, 400 bits, `alpha = 6/5`, `B = 74`:

```text
  C_R=1                        (C_R/74)^(1/1.2) = [0.0276889763416575080305816116034181286955733747778 +/- 8.00e-78]  -> N_monotone=1
  C_R=1.64                     (C_R/74)^(1/1.2) = [0.0418160917763854825992180795443315765119411423237 +/- 9.08e-78]  -> N_monotone=1
  C_R=2                        (C_R/74)^(1/1.2) = [0.0493361470588017111765532986986319536056251534687 +/- 8.69e-78]  -> N_monotone=1
  C_R=74                       (C_R/74)^(1/1.2) = 1.0000000000000000000000000                                          -> N_monotone=2
  C_R=1.0489e37 (banked)       (C_R/74)^(1/1.2) = [196305680128007199620898947325.88700878226 +/- 5.27e-45]
                                                 -> N_monotone = 196305680128007199620898947326
  C_R'=3.8160e25 (banked)      (C_R/74)^(1/1.2) = [57585923608207602637.99500625428 +/- 5.62e-55]
                                                 -> N_monotone = 57585923608207602638
```

So at the banked `C_R`, `N_monotone ~ 1.96e29`, not `1` — **28 orders of
magnitude** off, and it *dominates* the `12` in the max rather than being
dominated by it. Note also that the target takes `alpha = 6/5` from this same
family of notes while declining to take its `C_R`. That is the scope error in
its sharpest form: **the target uses one half of a banked (alpha, C_R) pair
and substitutes a hypothetical for the other half.**

**Independent cross-check that this is the live pair.** The referee-CONFIRMED
`R5_ACTIVATION_CLOSURE_SOL.md:371-374` and its ledger `:502` already bank the
(1.11a) activation as an *actual integer term*:

> The fresh Arb receipt proves the minimal strict side threshold
> `q_side=134010166814705707171424895246` [...] Thus the side condition is
> included as an actual integer term in (0.2)

I reproduced it from scratch with `C_R = 1.0489e37`, `alpha = 6/5`, `K_+=117`:

```text
(C_R/117)^(1/1.2) = [134010166814705707171424895245.34677 +/- 5.00e-6]
floor+1            = 134010166814705707171424895246
banked q_side      = 134010166814705707171424895246
MATCH?             True
```

**Exact match.** This proves (i) the banked pair really is
`(C_R=1.0489e37, alpha=6/5)`, and (ii) the sources *already computed*
`N_monotone` in the `B = K_+` case and it is `1.34e29`, not `1`. The target's
§3.5 reading contradicts a referee-CONFIRMED source it cites elsewhere in the
same note.

**Additional sensitivity finding.** `B(nu) = K_+ (K_F/K_+)^(1/nu) -> 0` as
`nu -> 0`, fast:

```text
  nu=0.1552  B=[74.1300144279482389352762635838504300887845043191063644305 +/- 3.04e-73]
  nu=0.12    B=[64.8422132339313156932880026481157745705593467632359750514 +/- 2.79e-73]
  nu=0.10    B=[57.6225168651787265583340971078267775399092913376802080546 +/- 4.78e-73]
  nu=0.08    B=[48.2718356473171409985303723877259903667158776639263889747 +/- 1.77e-73]
  nu=0.05    B=[28.3790978622034767219546305725063792820547315542623077365 +/- 2.55e-73]
  nu=0.03    B=[11.0375767099415706173598941212593448876648339548364277576 +/- 2.56e-73]
```

and at the actual banked route-H `c_0 = 1.827324e-5`:

```text
  B(c_0)  = [5.84993204986e-1682 +/- 2.93e-1694]     (log10 B = -1681.23)
  log10 N_monotone at that B and the banked C_R = [1431.87800028 +/- 1.30e-9]
```

So the "`N_monotone = 1`" reading is not merely wrong at the banked `C_R`; it
is wrong by ~1400 orders of magnitude once the route-H exponent is used
instead of the A0 one. (In fairness: with the *true* route-H `K_F = e^57984`,
`B = min(K_+, huge) = K_+ = 117`, and `N_monotone = q_side = 1.34e29` — which
is the number already banked, and still not `1`.)

### 5.4 Defect D7 (MAJOR) — `q_monotone` is not `N_monotone`

Even granting `N_monotone = 1`, "the `q_monotone` term is removable" does not
follow. `R3_R5_ASSEMBLY_PLAN_SOL.md:678-679` defines:

> - `q_monotone` is the point from which all envelopes used above are proved
>   monotone in the required direction.

That is **all** envelopes, not just the (1.11) mixing pair.
`R5_ASSEMBLY_EXECUTION_SOL.md:262` says only that "`N_monotone` *also*
activates (1.11)" — *also*, i.e. (1.11) is a subset of what `N_monotone`
carries. The target silently identifies the two. Discharging (1.11) leaves the
rest of `q_monotone` intact.

I did verify all four ledger citations exist and are correctly located:
`R3_ROUTE_B_TRANSPORT_SOL.md:586` (8.5); `KF_WALL_ATTACK_SOL.md:654-656`;
`C0_TRANSPORT_CAMPAIGN_SOL.md:878`; `BOUNDARY_ALPHA_THEOREM_SOL.md:667`.
Minor: the target says "plus **the same expression** at [...]
`BOUNDARY_ALPHA_THEOREM_SOL.md:667`" — it is *not* the same expression, it is
`q_0=\max\{12,q_RATE,q_transport,q_divisor,q_geometry,q_monotone,\ldots\}`,
with `q_transport`, an extra `q_geometry`, and a trailing ellipsis.

**Net: the `q_monotone`-removable claim is REFUTED on three independent
grounds** — wrong `C_R`, wrong `nu`, and wrong identification of the term.

## 6. (f) The documentary claim — GAPS

The three HOLOMORPHY quotes (`:288`, `:579`, `:583-586`), the two
`R5_ACTIVATION_CLOSURE_SOL.md` quotes (`:20-25`, `:504`), the `:378-381`
quote, the `R5_ASSEMBLY_EXECUTION_SOL.md:466-487` row, and the (2.5)/(1.11)
blocks are all **verbatim**. The hash match to the CONFIRMED referee is
**CONFIRMED** (§0). So the evidentiary base is sound.

Two problems with the *conclusion*.

**D8 — the dating is filesystem mtime, not document date.** Target §2.1:
"`HOLOMORPHY_GATE_SOL.md` is dated 2026-08-19 01:00; `R5_ACTIVATION_CLOSURE_SOL.md`
is dated 2026-08-19 04:01". Both files carry only `**Date:** 2026-08-19` in
their headers — no clock time. `01:00` and `04:01` are the `ls -l` mtimes on
this checkout. Mtimes are not content, are not preserved across clone, and are
not a citable provenance for a claim graded **PROVED (documentary)**. The
ordering happens to be corroborated by content (the closure note cites the
holomorphy note), so the conclusion survives; the *receipt* does not.

**D9 — "stale" overstates.** The §6 row reads *"Positive full-boundary RATE
**and** whole-tail monotonicity | GENUINELY OPEN | Current rigorous campaign
proves only alpha=0"*. That is a **conjunction**, and its stated reason is the
first conjunct. A conjunction with an open conjunct is open. The row is
therefore **correct as written**, not stale. What is superseded is only the
*implicature* that the second conjunct is independently open — which is
exactly how the target words it at §7.2 ("the conjunction should be split").
The claim-ledger row "the §6 [...] row is **stale** for the A0 route |
**PROVED (documentary)**" is stronger than what §7.2 supports, and stronger
than the target's own §6 concession ("nothing here contradicts
`HOLOMORPHY_GATE_SOL.md` §6's judgement"). Grade: **GAPS** — right finding,
overclaimed label.

## 7. (g) The anti-consumer warning — correct rule, violated by the target

The rule is **CONFIRMED** and correctly sourced. `R5_ACTIVATION_CLOSURE_SOL.md`
§6 and its ledger `:505` record `K_F=109` + `d_*>0.6603` as
**"REFUTED as a single ledger combination"**, resting on `RATE_A_REFEREE.md:326-351`,
which I read in full:

> The direct rebuilt \(K_F\) route is **not** on that segment: it uses
> sixth-zero geometry [...] This would be a domain error if RATE-A were fed
> into that sixth-zero contour.

and the domain table assigns `d_*>0.3186` to the sixth-zero `K_F=109` chain
and `d_*>0.6603` to the first-zero window. **Correct.**

**Does any banked ledger make the illegal pairing?** I swept every lane-G file
containing `0.6603`. The live two-stage chains
(`DH2_RENEWAL_PROOF_SOL.md` (9.2)/(9.3), `TWOMARK_RENEWAL_SOL.md` (7.1)/(7.2),
`C0_TRANSPORT_CAMPAIGN_SOL.md:127,145,201,222`) pair `d=0.6603` with the
prefactor `e^56155`, which `C0:21,180` derives from `K_F < e^57984` — **not**
from `109`. So no banked ledger commits the `109`-with-`0.6603` error. The
warning is live and currently unviolated **in the sources**.

**D10 — but the target violates it.** Target §4.2 sets `K_F(N) = 109` and
`d_delta = 0.6603` in the *same* instance, and calls them "the banked
constants". Target §7.7 discloses only that "§3 is symbolic in `K_F, d_delta`
for exactly this reason" — carefully scoped to §3, silently excluding §4.
Mitigating: because `omega_* = 1` in that witness, `K_F` carries exponent
`1-omega_* = 0` and is arithmetically inert, so nothing numeric depends on it.
The defect is disclosure, not arithmetic. My in-model Witness R2 (§3.3) does
consume `K_F` at a nonzero exponent, and is therefore subject to the same
caveat; I flag it rather than hide it.

## 8. Defect list

| # | defect | where | severity | why it was likely missed |
|---|---|---|---|---|
| D1 | (1.11)/(H3) credited for a substitution that needs only `x^p` monotone | §3.2 Step 1 | minor | over-deference to the source's own `PROVED` label |
| D2 | "`N_C` is the least such `Q` above the activation" — omits the max | §3.1 | minor | source (2.4) does it correctly; paraphrase lost it |
| D3 | witness constants labelled "the banked constants"; route-H `K_F` is `e^57984` | §4.1(B), §4.2 | major (labelling) | `KF_WALL`'s `109` is the most visible `K_F`; `C0:180` was not read |
| D4 | "`pi_0` is not determined in any source" / "exact missing step" | §3.5, §5, §6, §9 | **major** | `C0_TRANSPORT_CAMPAIGN_SOL.md` was never opened; `nu_seed`, `omega_*`, `c_0` are banked there |
| D5 | Lemma G2a asserts `=` where only `<=` is proved | §3.5 | minor | sufficiency-vs-definition slip |
| D6 | `C_R < 74` premise; banked `C_R = 1.0489e37`; `N_monotone = 1.96e29` | §3.5, §7.3, §9 | **major** | `alpha=6/5` taken from `BOUNDARY_ALPHA`, `C_R` not; `q_side=1.34e29` in the CONFIRMED closure note contradicts it and was not cross-read |
| D7 | `q_monotone` silently identified with `N_monotone` | §7.3, §9 | **major** | `R3_R5_ASSEMBLY_PLAN_SOL.md:678` defines `q_monotone` more broadly |
| D8 | "dated 01:00 / 04:01" are `ls` mtimes, not document dates | §2.1 | minor | mtimes visible in the shell, look authoritative |
| D9 | "stale" for a conjunction whose first conjunct is open | §2.1, §9 | minor | §7.2 states it correctly; the ledger row hardened it |
| D10 | §4.2 itself pairs `K_F=109` with `d_delta=0.6603` | §4.2 vs §3.6/§7.7 | minor | the disclosure was scoped to §3 only |
| D11 | "the same expression at `BOUNDARY_ALPHA_THEOREM_SOL.md:667`" — it is not | §7.3 | minor | skimmed |

## 9. What survives

The target's mathematics is sound and its central diagnosis is right:

- **Lemma G2 and floor-plus-one: CONFIRMED.** Re-derived independently.
- **The gate is misnamed** ("whole-tail majorant", not "monotonicity"):
  **CONFIRMED**. Nothing in the proof touches monotonicity of `E_3^up` or `E_R`.
- **(G3) is REFUTED: CONFIRMED**, and I strengthened it with an in-model
  witness the target did not have. `(1.11)` is genuinely not the missing
  hypothesis.
- **`(UP)` is the right repair and is sufficient: CONFIRMED.**
- **`B > 74` and the whole §3.5 Part-1 receipt: CONFIRMED to 73 digits**,
  including the correct decision to round `B` down because the exact value
  makes (1.11b) an interval-undecidable equality.

What does not survive is the **ledger layer**: `q_monotone` is not removable,
`pi_0` is not the missing step, and the note's `C_R < 74` regime is disjoint
from the regime the four cited ledgers actually run in.

## 10. Required repairs before this note can be banked

1. Replace §3.5's `C_R` discussion with the banked `C_R = 1.0489e37`
   (`BOUNDARY_ALPHA_THEOREM_SOL.md:31`) and state
   `N_monotone = 134010166814705707171424895246`, noting it **equals** the
   already-banked `q_side` (`R5_ACTIVATION_CLOSURE_SOL.md:373`).
2. Withdraw §7.3 and claim-ledger row "`q_monotone` is removable". Replace
   with: the (1.11) sub-gate has a closed form and is already banked as
   `q_side`; the rest of `q_monotone`
   (`R3_R5_ASSEMBLY_PLAN_SOL.md:678`) is untouched.
3. Withdraw "route-H `nu_seed`, `omega_*`, `pi_0` **OPEN / UNDEFINED**" and
   the §6 "exact missing step" headline. Cite
   `C0_TRANSPORT_CAMPAIGN_SOL.md:118-141`: `pi_0 = 1.827324e-5`. Restate the
   residue as the size of `e^56155` against `d_*`, per `DH2` (9.3).
4. Relabel §4.2's constants: they are an admissible tuple, **not** the banked
   route-H constants (`K_F < e^57984`, `C0:180`). Add the in-model witness
   (§3.3 above) so the refutation is not vulnerable to an
   "`omega_*=nu_seed=1` is unattainable" rebuttal.
5. Fix D1, D2, D5, D8, D9, D10, D11.

---

**Final verdict: MAJOR REVISION REQUIRED.** Mathematics CONFIRMED
(Lemma G2, floor-plus-one, Lemma G3, the `B>74` receipt, the (G3) refutation —
the last strengthened by an in-model witness). Ledger claims REFUTED
(`q_monotone` removability at the banked `C_R = 1.0489e37`; the "explicit
`pi_0` is the missing step" headline, `pi_0 = 1.827324e-5` being banked).
Documentary claims GAPS. No file was edited; no commit; no push.

**READY FOR JUDGING**
