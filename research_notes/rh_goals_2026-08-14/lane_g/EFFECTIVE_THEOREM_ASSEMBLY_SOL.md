# Effective theorem assembly: the single citable conditional statement

**Date:** 2026-08-20
**Program:** `(RATE)` / R3 / R5 assembly, lane G
**Interpreter:** `/Users/za/.venvs/farey-rh/bin/python` (Python 3.13.13, `python-flint` 0.9.0, Arb)
**Scope:** assembly and audit only. This note proves nothing new, adds no
constant, and **upgrades no status**. Every claim carries the status of its
most-caveated source. No file outside this one was written; nothing was
committed or pushed.

---

## 0. What this note does

The lane holds a boundary rate theorem, an activation arithmetic, two
constant reductions, a monotonicity gate with ten correction blocks, a
holomorphy ledger, and a transport implication — in seven separate files with
seven separate scopes. Nobody can cite that. This note assembles the strongest
**single** statement those pieces jointly support, surfaces every hypothesis it
consumes, recomputes every integer in it from scratch in interval arithmetic,
and says plainly what the resulting statement is and is not worth.

---

## 1. Receipts before claims

### 1.1 Interpreter and source state

```bash
/Users/za/.venvs/farey-rh/bin/python -c "import sys,flint;print(sys.version.split()[0],'python-flint',flint.__version__)"
shasum -a 256 research_notes/rh_goals_2026-08-14/lane_g/{BOUNDARY_ALPHA_THEOREM_SOL,R5_ACTIVATION_CLOSURE_SOL,R5_ACTIVATION_CLOSURE_REFEREE,CR_REDUCTION_V2_SOL,CR_REDUCTION_V2_REFEREE,R5_MONOTONICITY_GATE_SOL,R5_MONOTONICITY_GATE_REFEREE,HOLOMORPHY_GATE_SOL,R3_TRANSPORT_EXECUTION_SOL,AM_REFEREE,RATE_A_REFEREE,FW_REFEREE,TWOMARK_REFEREE,KF_WALL_REFEREE,C0_TRANSPORT_CAMPAIGN_SOL}.md
```

```text
3.13.13 python-flint 0.9.0
5a8d0bccdedb7363eec73b6763436a8b7f95b78b366a52b365f3ebc51c152980  BOUNDARY_ALPHA_THEOREM_SOL.md
3b49d73d56cf963703137a6494f1f733fbb208d36c0afbe1affbd5d700ab2a53  R5_ACTIVATION_CLOSURE_SOL.md
1fe8fb625de90523bf234f6331a6d95eb79ee06e5e19175fbe96cc7777c07f52  R5_ACTIVATION_CLOSURE_REFEREE.md
e9e5b023ea911a5d196254a134393815a57b4f6cf00fec09150d83a0d7d4b7b6  CR_REDUCTION_V2_SOL.md
04f7f5ed2aa2065e9822be856e17e27f928c300ced81f418a3380772aff236b6  CR_REDUCTION_V2_REFEREE.md
162f1cdb564a986460a4c7a79da8101c68d89ceff867692f2a0750b2f4dbcf88  R5_MONOTONICITY_GATE_SOL.md
24844b19bf3c7bad096a57a5fa22190c445d75451b558836d986352cbc952348  R5_MONOTONICITY_GATE_REFEREE.md
54e5df9bdaaba537b3b051cbb4ee46b4d29750c480632824120824b45888cdea  HOLOMORPHY_GATE_SOL.md
a6b6a1297fc4401e47e194a809064baa5cade1f9effb29fe28e3bde47d3b6345  R3_TRANSPORT_EXECUTION_SOL.md
3d655f2c05395688be73e8786cd9a954182cc4842005ff9e7662d05cccf503b4  AM_REFEREE.md
b835804104f502f54cc757336ba8fe54a82a05eaa18261a4d78f697aba358590  RATE_A_REFEREE.md
39c2e0d10a2ef1bb880e34cd4ca53bc280b451305cac871eb2244bb52e490058  FW_REFEREE.md
07ae98864b6963b14a279cfc463c9d047d0c5e75bc4f8fac876781f34bd28263  TWOMARK_REFEREE.md
73c6eb59b25038f9e23ae38fa8c409af65d50fd0219b45417022663486361710  KF_WALL_REFEREE.md
91e26f6cd1928a35a6420e319fd2fc7a9ad3911bc6dd5be372ff7bd09a15fd21  C0_TRANSPORT_CAMPAIGN_SOL.md
```

**Hash-drift disclosure.** `BOUNDARY_ALPHA_THEOREM_SOL.md` hashes to
`5a8d0bcc…` here, not to the `58441b33…` recorded inside
`R5_ACTIVATION_CLOSURE_SOL.md:76`, and not to the value the CR-V2 promotion
block quotes. The difference is the append-only Sections 8 and 9 added after
that hash was taken; `CR_REDUCTION_V2_REFEREE.md` explicitly examined and
refuted the post-hash concern about this file. I did not re-verify the append
byte-by-byte against git history; a referee wanting that should run
`git log -p` on the file. **No claim in this note rests on the drift being
benign**: every constant below was recomputed from the assembly formula, not
copied.

### 1.2 Fixed geometry (all definitions verbatim from the sources)

`R3_TRANSPORT_EXECUTION_SOL.md:22-52`:

> \(\rho_1=\tfrac12+i\gamma_1\), \(t_0=\gamma_1/2\),
> \(z_0=\frac{1+\rho_1}{2}=\frac34+it_0\);
> \(\delta=\frac12\), \(r_z=\frac18\), \(D_z=D(z_0,r_z)\);
> \(\Omega=\{s:\frac12<\Re s<\frac{11}{10},\ |\Im s-t_0|<\frac12\}\);
> \(\Gamma_R=\{\frac{11}{10}+it:|t-t_0|\le\frac12\}\).

`BOUNDARY_ALPHA_THEOREM_SOL.md:19-21` names the same right edge as
\(\Gamma_R^A\) (closed, \(|t-t_0|\le\frac12\)) and its Route-B open subset
\(\Gamma_R^B\).

\(\phi_q\) is the scalar trivial-character scattering determinant of the
one-cusp Hecke triangle orbifold \(G_q\backslash\mathbb H\);
\(\phi_\infty(s)=\sqrt\pi\,\Gamma(s-\tfrac12)\zeta(2s-1)/
[\Gamma(s)\zeta(2s)(4^s-1)]\);
\(F_q=\phi_q-\phi_\infty\); \(E_R(q)=\sup_{\Gamma_R}|F_q|\).

---

## 2. THE THEOREM

> **THEOREM (conditional, effective).**
> Assume the six named gates
> **(H-RATE)**, **(H-HOL)**, **(H-GEOM)**, **(H-SIDE)**, **(H-C4)**,
> **(H-ROUTE)** of the hypothesis table in §3.
>
> Then, with
> \[
> \alpha=\tfrac65,\qquad
> C_R''=3018536183210772296097745,
> \]
> \[
> \boxed{Q_0=11761546420922598622910053339543258496}
> \qquad(\log_{10}Q_0=37.0704\ldots)
> \]
> the following holds for **every integer \(q\ge Q_0\)**.
>
> **(a) Boundary rate (transport input).**
> \[
> E_R(q)=\sup_{s\in\Gamma_R^A}\bigl|\phi_q(s)-\phi_\infty(s)\bigr|
> \;\le\;C_R''\,q^{-6/5},
> \]
> and in particular \(0\le E_R(q)\le 9.891\times10^{-21}<117=K_+\).
> *(Part (a) alone holds for every integer \(q\ge q_{\rm RATE}=12\); the
> threshold \(Q_0\) is not needed for it, only for (b)–(c).)*
>
> **(b) Two-constants transport to the disc.**
> \[
> \sup_{\partial D_z}\bigl|\phi_q-\phi_\infty\bigr|
> \;\le\;K_+^{1-\nu_z}\,E_R(q)^{\nu_z}
> \;<\;0.0439\;\le\;\min_{\partial D_z}|\phi_\infty|,
> \]
> with \(K_+=117\), \(\nu_z=0.1552\).
>
> **(c) Off-line resonance at explicit scale.**
> By Rouché, \(\phi_q\) and \(\phi_\infty\) have equal zero counts in
> \(D_z\) with multiplicity; since \(\phi_\infty(z_0)=0\) there is at least
> one \(s_q\in D_z=D(\tfrac34+i\gamma_1/2,\tfrac18)\) with
> \(\phi_q(s_q)=0\). Hence
> \[
> \tfrac58\le\Re s_q\le\tfrac78,
> \qquad
> \bigl|\Im s_q-\gamma_1/2\bigr|\le\tfrac18,
> \qquad \gamma_1/2=7.0673\ldots,
> \]
> so \(\Re s_q\ge\tfrac58>\tfrac12\) strictly, and by Hejhal's reflection
> identity (7.22) \(\phi_q\) has a pole of the same order at
> \(1-\overline{s_q}\), with \(\tfrac18\le\Re(1-\overline{s_q})\le\tfrac38<\tfrac12\).

**Scope of (c).** The resonance conclusion **is** licensed by a banked note —
`R3_TRANSPORT_EXECUTION_SOL.md:88-93,208-231` states exactly this Rouché +
reflection step, and its own §5 marks as `CONJECTURAL / MISSING` only the
inputs \((C_R,\alpha,q_{\rm RATE})\), \(K_+\) and \(q_{\rm divisor}\), all of
which are now supplied as the named gates of §3. Nothing beyond (c) is
claimed: no count of such zeros, no uniformity in \(q\), no statement about
any \(q<Q_0\), and no claim that the theorem is machine-verified.

**What the theorem is NOT.** It is not the R5 pincer. The finite block
\(3\le q<Q_0\) is uncovered and remains **OPEN / UNDEFINED**
(`R5_ACTIVATION_CLOSURE_SOL.md:490-493`). It is not unconditional. It is not
Lean-formalized. See §5.

---

## 3. HYPOTHESIS TABLE — every gate the theorem assumes

Nothing is omitted. "Status" is the **most caveated** grading found in any
banked source, not the most favourable.

### (H-RATE) — the boundary rate theorem

> **Exact source phrasing.** `BOUNDARY_ALPHA_THEOREM_SOL.md:728-734`:
> "Therefore `(RATE-A)` is now **CONFIRMED at paper level** on the stated
> balanced/matched boundary \(\Gamma_R^A\), with exponent \(6/5\), activation
> \(q_{\rm RATE}=12\), and the unchanged advertised upward ceiling."
> `AM_REFEREE.md:7`: "**Verdict:** **CONFIRMED — paper-level, conditional on
> the already accepted Route-B/Ford inputs; not machine-verified.**"

**Status: CONFIRMED-conditional (paper level), WITH A LIVE LEDGER CONFLICT.**

Two other banked notes still grade the same object OPEN:

- `HOLOMORPHY_GATE_SOL.md:579` — "| Positive full-boundary RATE and whole-tail
  monotonicity | **GENUINELY OPEN** | Current rigorous campaign proves only
  \(\alpha=0\); R5/DH2 cannot activate. |"
- `R5_MONOTONICITY_GATE_SOL.md` corrected bottom line (dated **2026-08-20**,
  i.e. *after* the RATE-A promotion): "`(RATE-A)` with `alpha>0`. Unchanged by
  this note; the rigorous campaign still proves only `alpha=0`. This remains
  the single standing blocker for every conditional statement above."

I do **not** adjudicate this conflict, and I do not treat the later date as
settling it. The theorem therefore states (H-RATE) as an **assumed** gate.
Reading (H-RATE) at its most-caveated banked grading, the theorem is
conditional-on-a-conjecture; reading it at the RATE-A/AM_REFEREE grading, the
theorem is conditional-on-paper-level-inputs. Both readings are recorded; the
theorem text is valid under either.

**What would discharge it:** an adjudication note that either (i) confirms the
two OPEN rows are stale wording superseded by the 2026-08-19 promotion, with a
line-level receipt, or (ii) exhibits the surviving gap. Machine formalization
of the §3–§4 argument of `BOUNDARY_ALPHA_THEOREM_SOL.md` would discharge it
outright.

**Sub-inputs consumed inside (H-RATE), each separately named:**

| sub-input | exact source phrasing | file:line | status | discharge |
|---|---|---|---|---|
| `(FW)` first-overflow renewal count | "**Verdict:** **CONFIRMED — paper-level, not machine-formalized.**" | `FW_REFEREE.md:5` | CONFIRMED-conditional (paper) | Lean/Arb formalization |
| `(DH_{2,4})` two-mark renewal | "**Verdict:** **CONFIRMED — paper-level, not machine-verified.**" | `TWOMARK_REFEREE.md:5` | CONFIRMED-conditional (paper) | Lean/Arb formalization |
| M1 localization triple / Route-B repair | "| `M1_ROUTE_B_REPAIR_SOL.md` | **CONFIRMED** | … The note correctly leaves \(O(q^{1-2\sigma})\) conjectural. |" | `M1_LOCALIZATION_TRIPLE_REFEREE.md:12` | CONFIRMED-conditional | as above |
| endpoint comparison \(x_X\le y_X\) | "In the balanced alphabet \(|a_i|\le h=\lfloor q/2\rfloor\), all entries are nonnegative and nondecreasing on \([\lambda_q,2]\), so \(x_W\le y_W\)." | `BOUNDARY_ALPHA_THEOREM_SOL.md:311-313` | PROVED (elementary, in-note) | — |
| Lemma 3.1 theta-endpoint derivative | "**Lemma 3.1 — PROVED.**" | `BOUNDARY_ALPHA_THEOREM_SOL.md:333` | PROVED (in-note, paper level) | formalization |
| Lemma 3.2 atom moment | "**Lemma 3.2 — PROVED from the confirmed two-mark coding.**" | `BOUNDARY_ALPHA_THEOREM_SOL.md:405` | PROVED (in-note); the bridge is separately CONFIRMED by `AM_REFEREE.md:405` | formalization |
| \(\sup_{K_{15}}|M(s)|=M(1.1)<2.775\) | "\sup_{s\in K_{15}}|M(s)|=M(1.1)<2.775." | `M3_UNIFORMITY_EXECUTION_SOL.md:275` | PROVED (beta-integral) | — |
| standalone N1-RATE, \(A=11/20\) | "| Canonical N1-RATE with \(A=11/20\) | **CONJECTURAL** |" | `BOUNDARY_ALPHA_THEOREM_SOL.md:681` | **OPEN-CONJECTURAL — but NOT consumed**: "it is no longer needed for the boundary sum" (`:282-283`) | not needed |

### (H-HOL) — finite-\(q\) holomorphy / no poles on \(\overline\Omega\)

> **Exact source phrasing.** `HOLOMORPHY_GATE_SOL.md:373-379`:
> "> **Finite-Hecke holomorphy theorem.** For every finite Hecke index `q>=3`,
> `phi_q` is holomorphic on an open neighborhood of the full `H_0`, of the
> A0 domain `overline{Omega}`, of `D_z`, and of the old Route-B right domains.
> … `q_pole=q_divisor=3`."
> `:256-257`: "The finite-Hecke **pole/holomorphy gate is provable from the
> printed theory and closes with `q_pole = q_divisor = 3`**".

**Status: PROVED from printed theory** (Hejhal Prop. 12.5 / Claim 9.6 + note
86; \(\phi_\infty\) pole-freeness by explicit formula).
Contributes the integer \(q_{\rm divisor}=3\) to the max.

**Attached negative, carried explicitly:** the *nonvanishing* companion is
false and is NOT assumed —
`HOLOMORPHY_GATE_SOL.md` §6: "| \(\phi_q\ne0\) on full \(H_0\) for every large
q | **FALSE** | Hejhal Theorem 7.11 proves eventual zeros. Correct use:
contradiction hypothesis / case split. |" The theorem above uses no
nonvanishing hypothesis; it *produces* a zero.

**What would discharge it:** already discharged for the domains used here.

### (H-GEOM) — the two A0 geometric floors

> **Exact source phrasing.** `R3_TRANSPORT_EXECUTION_SOL.md:60-65`:
> "\(m_z:=\min_{\partial D_z}|\phi_\infty(s)|\ge 0.0439\), \(\qquad
> \nu_z:=\inf_{\partial D_z}\omega(s,\Gamma_R;\Omega)\ge 0.1552\)."
> Ledger `:243-245` (as quoted in `R5_ACTIVATION_CLOSURE_REFEREE.md:244-245`):
> "| `m_z` | … | **PROVED**, Arb interval cover |",
> "| `nu_z` | … | **PROVED**, Arb/Fourier interval cover |".

**Status: PROVED (Arb interval cover).** Both are rounded in the safe
direction (minimum down, infimum down). Not \(q\)-dependent: an analytic PASS
gate contributing no integer (`R5_ACTIVATION_CLOSURE_SOL.md:360-368`).

**What would discharge it:** already discharged; only formalization remains.

### (H-SIDE) — the non-RATE side bound \(K_+=117\)

> **Exact source phrasing.** `R5_ACTIVATION_CLOSURE_SOL.md:116-118`:
> "The A0 side bound is the safe ledger value `K_+=117`, confirmed for the
> same quantity by `KF_WALL_REFEREE.md:27-31,211-240,409-414`".
> `R5_ACTIVATION_CLOSURE_REFEREE.md:58-62`: "the bound controls the same
> `K_+` quantity and gives the safe ledger choice `K_+=117`, conditional on the
> full-width `H_0` and the stated holomorphy/anchor gates … Thus the safe
> status is `K_+=117` as a **conditional source input**, not an unconditional
> theorem about every possible domain."
> Earlier, un-superseded historical row: "| `K_+` | non-RATE-boundary bound for
> `|F_q|` | **CONJECTURAL / MISSING family-uniformly** |"
> (`R3_TRANSPORT_EXECUTION_SOL.md:250`).

**Status: CONFIRMED-conditional source input.** The historical
`CONJECTURAL / MISSING family-uniformly` row is superseded *only* by the
side-wall report, which is itself conditional on full-width \(H_0\) and the
anchor gate — so the family-uniformity concern is answered conditionally, not
removed. It also carries the side hypothesis \(0<E_R(q)\le K_+\), discharged
inside the theorem by part (a) (\(E_R\le9.891\times10^{-21}<117\)); the
\(E_R(q)=0\) branch makes the A0 conclusion immediate
(`BOUNDARY_ALPHA_THEOREM_SOL.md:615-623`).

**What would discharge it:** an unconditional family-uniform bound on
\(\sup|F_q|\) over the three non-RATE sides of \(\partial\Omega\), or
discharge of the full-\(H_0\)/anchor gates it is conditional on.

### (H-C4) — the reduced tag coefficient \(C_4''\)

> **Exact source phrasing.** `BOUNDARY_ALPHA_THEOREM_SOL.md:812-830`:
> "Substituting the smaller explicit tag bound \(82944 = 2^{10}3^4\) from the
> atom bridge's (3.9) for its own \(2^{20}\) ceiling — proved
> non-double-counting: the ceiling enters the \(2^{62}\) subtotal exactly once,
> multiplicatively, at (3.25) — permits the paper-level coefficient
> \(C_4''=2^{52}\cdot81+1=364791569817010177\) … \(C_R''=3018536183210772296097745\)."
> `CR_REDUCTION_V2_REFEREE.md:44`: "**VERDICT: CONFIRMED**, subject to repair D1."

**Status: CONFIRMED-conditional** (three documentation repairs D1–D3 applied
in `CR_REDUCTION_V2_SOL.md`; narrow re-referee "RE-REFEREE: CONFIRMED —
promotion unblocked"). The source itself grades the constant
(`CR_REDUCTION_V2_SOL.md:341`) "**No theorem-ledger promotion.** `C_R''` is an
*unbanked candidate*" — so the theorem above should be read as **using an
unbanked-candidate constant**. The two safer alternatives remain valid and
give strictly larger \(Q_0\) (§4.4).

**What would discharge it:** a cold referee banking \(C_R''\) as a ledger
constant rather than a candidate.

### (H-ROUTE) — domain discipline: A0 is a first-zero ledger

> **Exact source phrasing.** `R5_ACTIVATION_CLOSURE_SOL.md:56-60`:
> "The requested single ledger pairing `K_F=109` with the old `d_*>0.6603` is
> **REFUTED as a domain combination**. It mixes the sixth-zero Route-B wall
> with the first-zero defect… selected A0 uses `K_+=117`, `m_z`, and `nu_z`".
> `R5_MONOTONICITY_GATE_SOL.md` D3 correction: "The parenthetical
> '(the banked constants)' is **false for route H**. `109` is the **Route-B
> sixth-zero direct wall** … The banked `K_F` for the two-stage route-H chain
> … is `K_F < e^57984`, not `109`."

**Status: PROVED (domain correction), and BINDING on this note.** The theorem
consumes \(K_+\), \(m_z\), \(\nu_z\) only. It consumes no \(K_F\) and no
\(d_*\) defect. §4.3 records what \(B\) becomes under each \(K_F\) reading and
uses the route-H-correct one.

**What would discharge it:** nothing — it is a constraint, honoured here.

### Gates that are NOT assumed, and are therefore NOT available

| item | exact source phrasing | file:line | status |
|---|---|---|---|
| finite scalar-\(\phi_q\) evaluator + winding block for \(q<Q_0\) | "| certified true-phi_q finite evaluator and winding block | **OPEN** |" | `KF_WALL_ATTACK_SOL.md:680` | **OPEN** |
| full all-\(q\) R5 closure | "| full all-q R5 closure | OPEN / UNDEFINED | finite block remains missing |" | `R5_ACTIVATION_CLOSURE_REFEREE.md:342` | **OPEN / UNDEFINED** |
| effective analytic \(q_0\) + finite-base coverage | "| Effective analytic \(q_0\) and finite-base coverage | **GENUINELY OPEN** |" | `HOLOMORPHY_GATE_SOL.md:580` | **OPEN** |
| remainder of \(q_{\rm monotone}\) (all envelopes other than the (1.11) pair) | "**The remainder of `q_monotone`** — all other envelopes, per `R3_R5_ASSEMBLY_PLAN_SOL.md:678` — is **untouched** by this note and stays `CONJECTURAL`." | `R5_MONOTONICITY_GATE_SOL.md` D-corrections §item 3 | **OPEN-CONJECTURAL** — see §4.5 |
| existing determinant/winding boxes as evidence | "This is **NOT EVIDENCE** for a zero or pole of phi_12" | `HOLOMORPHY_GATE_SOL.md:230` | NOT EVIDENCE |
| machine verification / Lean | "It is not a machine formalization or a certified full-operator enclosure." | `BOUNDARY_ALPHA_THEOREM_SOL.md:737-738` | **NOT CLAIMED** |

---

## 4. \(Q_0\): the computation, with receipts

### 4.1 The command

The complete program (written fresh for this note; not copied from any source
note) lives at
`/private/tmp/claude-501/-Users-za-Documents-farey-hecke/d132431f-d2c6-4401-96d1-90f58d3026fb/scratchpad/q0.py`
and is reproduced verbatim here.

```python
from flint import arb, acb, ctx
ctx.dps = 160
def Z(a):
    s = str(a); assert '+/-' not in s and 'e' not in s.lower()
    u, v = s.split('.', 1); assert set(v) <= set('0'); return int(u)

# ---- Stage 1: recompute C_R'' from the Section-4 assembly with C_4'' ----
p = arb(11)/5; alpha = arb(6)/5
C4pp = arb(2)**52*81 + 1
S = arb('7.648')
t0 = (acb.zeta_zero(1)/2).imag
Strue = (arb('1.1')**2 + (t0 + arb('.5'))**2).sqrt()
F = arb(1225)/4 + arb(91605)/12          # F(q) at q=12
pair = 2*arb.pi()**2*(S+1)*p*C4pp*F
wrap = p*128*(1+arb(2).log())*30
CRraw = arb('2.775')*(pair + wrap)
CRpp = Z(CRraw.upper().ceil())
print('C_4pp =', Z(C4pp))
print('sup|s| on Gamma_R^A =', Strue.upper(), ' < 7.648 :', bool(Strue < S))
print('F(12) =', F)
print('C_R_raw_upper =', CRraw.upper())
print('C_R_pp =', CRpp, ' strict_upper:', bool(arb(CRpp) > CRraw))
print('log C_R_pp =', arb(CRpp).log())
print('one_less_fails:', bool(arb(CRpp-1) < CRraw))

# ---- Stage 2: A0 activation arithmetic at C_R'' ----
nu = arb('0.1552'); m = arb('0.0439'); K = arb(117)
CR = arb(CRpp); beta = alpha*nu
T_side = (CR.log() - K.log())/alpha
e = T_side.exp()
lo, hi = Z(e.lower().floor()), Z(e.upper().floor())
q_side = hi + 1
print('T_side =', T_side)
print('floor lo/hi =', lo, hi)
print('q_side_pp =', q_side)
print('side_min_gt:', bool(arb(q_side).log() > T_side),
      ' side_min_le:', bool(arb(q_side-1).log() <= T_side))
ERs = CR*arb(q_side)**(-alpha)
print('E_R(q_side)_upper =', ERs.upper(), ' < K_+ :', bool(ERs < K))

T = ((1-nu)*K.log() - m.log())/beta + CR.log()/alpha
e = T.exp()
lo, hi = Z(e.lower().floor()), Z(e.upper().floor())
q_A0 = hi + 1
print('T =', T)
print('floor lo/hi =', lo, hi)
print('q_A0_pp =', q_A0)
print('min_gt:', bool(arb(q_A0).log() > T), ' min_le:', bool(arb(q_A0-1).log() <= T))
ERt = CR*arb(q_A0)**(-alpha)
U = K**(1-nu)*ERt**nu
print('E_R(q_A0)_upper =', ERt.upper(), ' < K_+ :', bool(ERt < K))
print('A0_lhs_upper =', U.upper(), ' < m :', bool(U < m))

# ---- Stage 3: N_monotone at C_R'' ----
# B = min(K_+, K_F^(1/nu) K_+^(1-1/nu))
for label, KF in (('routeB_diagnostic_KF=109', arb(109)),
                  ('routeH_banked_KF<e^57984', arb(57984).exp())):
    second = KF**(1/nu) * K**(1 - 1/nu)
    B = K if bool(K < second) else second
    print(f'  [{label}] second_term_log10 =', (second.log()/arb(10).log()).upper(),
          ' B =', B.lower())
    x = (CR/B)**(1/alpha)
    print(f'  [{label}] (C_R/B)^(1/alpha) =', x,
          ' N_monotone_bound =', Z(x.upper().floor())+1)

# ---- Stage 4: the max ----
terms = {'q_RATE': 12, 'q_divisor': 3, 'q_side_pp': q_side, 'q_A0_pp': q_A0}
B = K
x = (CR/B)**(1/alpha)
terms['N_monotone_(1.11)_bound'] = Z(x.upper().floor())+1
Q0 = max(terms.values())
for k, v in terms.items(): print(f'  {k:28s} = {v}')
print('Q_0 =', Q0, ' == q_A0_pp :', Q0 == q_A0)
print('Q_0 log10 =', (arb(Q0).log()/arb(10).log()))
print('N_monotone == q_side :', terms['N_monotone_(1.11)_bound'] == q_side)
```

Run:

```bash
/Users/za/.venvs/farey-rh/bin/python q0.py
```

### 4.2 Complete stdout

```text
C_4pp = 364791569817010177
sup|s| on Gamma_R^A = [7.646893243596647842577572508297090015450131975059035899179710862086914677608142758582637819718890540035761116143151805191554445929967598403684362033309710447524 +/- 3.00e-160]  < 7.648 : True
F(12) = 7940.000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
C_R_raw_upper = [3018536183210772296097744.833020924248614441468095501836354950933363614907380638983200411783345876090247222783751143169884641607154635985793356616167787102987431 +/- 4.24e-136]
C_R_pp = 3018536183210772296097745  strict_upper: True
log C_R_pp = [56.36681423818909707845172980616929009769148038573117144025789095688625577243434094995059413413525402635919207763665519846823066353522723162509234039357327068433 +/- 4.13e-159]
one_less_fails: True
T_side = [43.00386691949278413300645990896576673632602610443788785030788064912316876556059403066982330088941696667832818950998062112663541715948300414096789044588868175945 +/- 5.33e-159]
floor lo/hi = 4746157036282968394 4746157036282968394
q_side_pp = 4746157036282968395
side_min_gt: True  side_min_le: True
E_R(q_side)_upper = [116.9999999999999999816625966135411103646392794736648020757129424520000508137901754132727253683326929006656945238315529998512843729602837323559648005339725935176 +/- 2.22e-158]  < K_+ : True
T = [85.35789877998874367404346379859781755327461098881661120594595682483350056159554998647568206237340292239269595917507125359783971776924212368690978269271849078299 +/- 8.41e-159]
floor lo/hi = 11761546420922598622910053339543258495 11761546420922598622910053339543258495
q_A0_pp = 11761546420922598622910053339543258496
min_gt: True  min_le: True
E_R(q_A0)_upper = [9.890974306379110548771776148234686409412516353341223852976188448244817846815112761441381199076936566987587688266361778123361999741400936879232912856601569693988e-21 +/- 2.95e-181]  < K_+ : True
A0_lhs_upper = [0.04389999999999999999999999999999999999981027575908442172237117998433590868797851161921993146289719130753665995176549753764400186029396481057988178869506828877602 +/- 4.78e-162]  < m : True
  [routeB_diagnostic_KF=109] second_term_log10 = [1.869994084648622928615841526058978104721079739316937325233333851370282040994953052219258990157740214705544695596656817317399082467555603053925866480615364140104 +/- 4.40e-160]  B = [74.13001442794823893527626358385043008878450431910636443054911570887217296187594035530145665418535720491541381303224228989853283560885516552094659070574698342033 +/- 6.05e-160]
  [routeB_diagnostic_KF=109] (C_R/B)^(1/alpha) = [6942276674823096982.3939517273598876191982239362573871246745499452699325360952349285442922510222415922098347371143964530888957767937912200064218114117709344685 +/- 7.80e-140]  N_monotone_bound = 6942276674823096983
  [routeH_banked_KF<e^57984] second_term_log10 = [162244.7424952458171209173962613251260945459181158022949392477704637110706939356349224951788823232368787134734572605214449373851727456012208321575781460481835290 +/- 8.85e-156]  B = 117.0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
  [routeH_banked_KF<e^57984] (C_R/B)^(1/alpha) = [4746157036282968394.3801125633205057565991074967538848355997746837323680826673394163447869145367823141098259271281344436440360096529588420679969429628291771361 +/- 1.62e-140]  N_monotone_bound = 4746157036282968395
  q_RATE                       = 12
  q_divisor                    = 3
  q_side_pp                    = 4746157036282968395
  q_A0_pp                      = 11761546420922598622910053339543258496
  N_monotone_(1.11)_bound      = 4746157036282968395
Q_0 = 11761546420922598622910053339543258496  == q_A0_pp : True
Q_0 log10 = [37.07046442700542269724563939847585341190166110905856819967687736110724894120617443541901794988978879993049568045341799909046846675061749384953770284895706794550 +/- 3.09e-159]
N_monotone == q_side : True
```

### 4.3 Reading the receipt

**Rounding discipline.** \(C_R''\) is the **ceiling** of the upper endpoint of
the assembly interval (`strict_upper: True`, and `one_less_fails: True` shows
\(C_R''-1\) would not dominate) — bound UP. \(m_z=0.0439\) and
\(\nu_z=0.1552\) are the sources' floored values — margins DOWN.
\(K_+=117\) is the safe ledger value above the raw supremum — bound UP.
Every threshold is \(\lfloor e^T\rfloor+1\) with the Arb lower and upper
endpoints agreeing on the floor (`floor lo/hi` identical in both cases), which
is what makes the integer well defined; both minimality directions are checked
(`side_min_gt`/`side_min_le`, `min_gt`/`min_le`).

**Cross-check against the banked values.** All three reproduce digit-for-digit:

| quantity | banked | recomputed here | source |
|---|---|---|---|
| \(C_R''\) | `3018536183210772296097745` | `3018536183210772296097745` | `BOUNDARY_ALPHA_THEOREM_SOL.md:829`; `CR_REDUCTION_V2_SOL.md:208` |
| \(q_{\rm side}''\) | `4746157036282968395` | `4746157036282968395` | `CR_REDUCTION_V2_SOL.md:280,466` |
| \(q_{A0}''\) | `11761546420922598622910053339543258496` | `11761546420922598622910053339543258496` | `BOUNDARY_ALPHA_THEOREM_SOL.md:839`; `CR_REDUCTION_V2_SOL.md:287,302` |

The recomputation is independent in the sense that Stage 1 rebuilds \(C_R''\)
from the §4 assembly (\(2\pi^2(S+1)pC_4''F(12)\) plus wrap, times \(M_0\))
rather than reading the integer, and Stage 2 then consumes only that.

**\(N_{\rm monotone}\), per the monotonicity referee's formula.** With
\(B=\min\bigl(K_+,\;K_F^{1/\nu}K_+^{1-1/\nu}\bigr)\) and
\(N_{\rm monotone}\le\lfloor(C_R/B)^{1/\alpha}\rfloor+1\)
(`R5_MONOTONICITY_GATE_SOL.md:727-732`, D5: the relation is \(\le\), not \(=\);
it is an upper bound on the activation, which is exactly how a `max` of upper
bounds consumes it):

- **Route-H-correct pairing** (D3: banked \(K_F<e^{57984}\)): the second term
  has \(\log_{10}=162244.74\ldots\), astronomically above \(K_+\), so
  \(B=K_+=117\) and
  \(N_{\rm monotone}\le 4746157036282968395\) — **exactly \(q_{\rm side}''\)**,
  the same phenomenon the monotonicity note recorded at the Section-4 constant
  ("digit-for-digit the already-banked `q_side`"), now reproduced at \(C_R''\).
- **Route-B diagnostic** (\(K_F=109\), which D3/D10 forbid pairing with a
  route-H quantity — recorded for completeness only, **not used**):
  \(B=74.130\ldots\), \(N_{\rm monotone}\le 6942276674823096983\).

Either way \(N_{\rm monotone}\) is dominated by \(q_{A0}''\).

### 4.4 The max, and its sensitivity

\[
Q_0=\max\{\,q_{\rm RATE},\;q_{\rm divisor},\;q_{\rm side}'',\;
q_{A0}'',\;N_{\rm monotone}\,\}
=\max\{12,\;3,\;4.746\!\times\!10^{18},\;1.176\!\times\!10^{37},\;
4.746\!\times\!10^{18}\}
=q_{A0}''.
\]

At the two safer constants the same max gives strictly larger thresholds
(`BOUNDARY_ALPHA_THEOREM_SOL.md:48,798,839`):

| constant | \(C_R\) | \(Q_0\) | \(\log_{10}Q_0\) |
|---|---|---|---|
| §4 published | `10489412368759562746433608215977724802` | `332093267419812025416641789732742045430624465595` | 47.52 |
| §8 (\(C_4'=2^{62}+1\)) | `38160259896392973127946053` | `97418971860452658435229799565334786148` | 37.99 |
| **§9 (\(C_4''=2^{52}\!\cdot\!81+1\)) — used above** | `3018536183210772296097745` | `11761546420922598622910053339543258496` | **37.07** |

The theorem is valid at any of the three; the smallest is quoted. Note the
scale: reducing \(C_4\) by a factor \(3474\) moved \(\log_{10}Q_0\) by
\(10.4\) — because \(Q_0\sim C_R^{5/6}\times e^{T_0}\), where the
\(q\)-independent prefactor \(e^{T_0}\) alone is \(\approx 4.7\times10^{16}\).
Constant-shaving cannot rescue this; see §5(b).

### 4.5 The \(q_{\rm monotone}\) disclosure — read this before quoting \(Q_0\)

The instruction I followed is the **corrected** one, not the withdrawn one.
`R5_MONOTONICITY_GATE_SOL.md` §7.3 originally said \(q_{\rm monotone}\) is
removable; that claim is **WITHDRAWN and REFUTED on three grounds** (D6 wrong
\(C_R\), D7 wrong identification, D3 wrong \(\nu\)). The corrected instruction
is: "**Keep `q_monotone` in all four `max` expressions.**"

Accordingly:

- What I *computed* is the **(1.11) sub-gate** of \(q_{\rm monotone}\), whose
  closed form is Lemma G2a's \(N_{\rm monotone}\). It is dominated.
- What I *cannot* compute is **the rest of \(q_{\rm monotone}\)** —
  "the point from which **all** envelopes used above are proved monotone in
  the required direction" (`R3_R5_ASSEMBLY_PLAN_SOL.md:678`, quoted in D7).
  That remainder is **untouched and CONJECTURAL**.

**Therefore \(Q_0\) as displayed is a max over the *named and evaluable*
gates, and \(q_{\rm monotone}\) is retained symbolically in it.** Honest
form of the threshold:

\[
Q_0=\max\bigl\{12,\,3,\,q_{\rm side}'',\,q_{A0}'',\,q_{\rm monotone}\bigr\}
\;\ge\;11761546420922598622910053339543258496,
\]

with equality **iff** the un-evaluated remainder of \(q_{\rm monotone}\) does
not exceed \(q_{A0}''\). No banked source establishes that. A referee should
read the boxed \(Q_0\) as the value of the evaluable terms and the theorem as
carrying \(q_{\rm monotone}\) inside gate (H-RATE)/(H-ROUTE)'s conditional
scope. I do not claim the max is closed.

*(For the A0 route specifically, `R5_ACTIVATION_CLOSURE_SOL.md:377-382` argues
whole-tail monotonicity is an analytic PASS for every real \(q>0\) — the
envelope \(U(q)=K_+^{1-\nu}C_R^\nu q^{-\alpha\nu}\) has
\(U'<0\) since \(\alpha\nu=582/3125>0\) — and therefore that no integer
\(q_{\rm monotone}\) term arises for A0 at all. That reading, if accepted,
closes the max at \(q_{A0}''\). It was CONFIRMED-conditional by
`R5_ACTIVATION_CLOSURE_REFEREE.md`. But D7 was written afterwards and asserts
\(q_{\rm monotone}\) is broader than any one envelope. I record both and adopt
neither; the inequality form above is safe under either.)*

---

## 5. HONESTY SECTION

### (a) \(Q_0\) is astronomical, and "effective" here is a technical word

\(Q_0=1.176\times10^{37}\). Every constant in the theorem is explicit, every
threshold is a named integer with a checked minimality, and nothing is hidden
in an \(O(\cdot)\) — that is precisely what "effective" means, and the theorem
earns it. It does **not** mean the theorem is numerically bridgeable.

For scale: the theorem says nothing about \(q=3,4,5,\ldots,10^{37}\). The
certified Hecke computations this project actually owns run at \(q\le21\)
(onset theorem) and the current Kaggle campaign is grinding \(q=8\) contour
leaves at \(\sim2000\) seconds per leaf. The gap between "what is certified"
and "where the theorem starts" is thirty-six orders of magnitude. There is no
prospect — not with better hardware, not with better algorithms — of closing
it by computing the base cases one at a time. A finite-base *theorem* would be
needed, and none exists.

### (b) What the pincer would additionally need, and why it is out of reach

The R5 pincer is: analytic tail for \(q\ge Q_0\) **plus** certified coverage of
every \(3\le q<Q_0\). The banked statement of the missing half is verbatim
(`R5_ACTIVATION_CLOSURE_SOL.md:483-488`):

> For every finite integer index below the analytic onset (unless a separate
> covering theorem is supplied), build and independently certify a true scalar
> `phi_q` meromorphic-continuation evaluator, interval branch/derivative
> variation, denominator/pole clearance, and a Rouché or direct winding
> zero-minus-pole certificate.

Four reasons this is out of reach at current constants:

1. **No evaluator exists.** `git ls-tree -r HEAD -- engine/certify` returns
   empty; the existing `hecke_transfer_operator_zero` / R3B boxes are the
   wrong function and are graded **FALSE** as a gate-closer
   (`HOLOMORPHY_GATE_SOL.md` §6) and **NOT EVIDENCE** (`:230`). The build cost
   is recorded as unknown.
2. **The block is \(10^{37}\) wide.** Even a hypothetical evaluator at one
   microsecond per \(q\) needs \(\sim3\times10^{23}\) years.
3. **Shrinking \(Q_0\) does not help enough.** \(Q_0\sim C_R^{5/6}e^{T_0}\) and
   \(e^{T_0}\approx4.7\times10^{16}\) is \(C_R\)-independent: it is fixed by
   \(K_+=117\), \(m_z=0.0439\), \(\nu_z=0.1552\), \(\alpha=6/5\) alone.
   Driving \(C_R''\) to **1** would still leave \(Q_0\approx4.7\times10^{16}\).
   The binding parameter is \(\nu_z\) — the harmonic measure of the right edge
   seen from \(\partial D_z\) — which enters as \(1/(\alpha\nu_z)\approx4.47\)
   in the exponent. Only a geometry change (a fatter \(\Omega\), a closer
   disc, a larger \(\alpha\)) touches it.
4. **The route-H variant is far worse.** Where the two-stage transport is used
   instead of A0, the banked product is \(\pi_0=1.827324\times10^{-5}\) against
   an \(e^{56155}\) prefactor, giving
   `log q > 2.560914e9 + (5/6) log C_R` — graded
   **`CONJECTURAL` and effectively unreachable, not undefined**
   (`R5_MONOTONICITY_GATE_SOL.md`, corrected bottom line). That is
   \(\log_{10}q>10^9\).

So: the theorem in §2 is the tail half of a pincer whose other half has no
route. It should be published, if at all, as *an effective conditional tail
statement*, never as a step whose completion is imminent.

### (c) The unconditional qualitative LAW does not depend on any of this

Separately banked, and **logically disjoint from everything above**:

> For every finite integer \(q\ge3\) the scalar trivial-character scattering
> determinant of the one-cusp Hecke triangle orbifold has infinitely many
> nonreal zeros with \(\Re\rho>1/2\), hence infinitely many
> multiplicity-matched poles at \(1-\rho\) with \(\Re(1-\rho)<1/2\).

`LAW_SECOND_AUDIT_REFEREE.md` §Verdict: "**CONFIRMED**, with scope. Every
mathematical attack failed. … The chain is unconditional on printed
literature, at the generality needed". Its own source note still self-grades
"**Status: PROOF CANDIDATE -- CONJECTURAL until a separate cold referee accepts
the Jensen boundary bookkeeping**"
(`LAW_ORBIFOLD_SCATTERING_COUNT_SOURCE_SOL.md:5-6`) — that referee has since
reported CONFIRMED, but I do not adjudicate the note's own header and do not
promote it here. Two residuals are declared by the second audit: Selberg 1990
and Venkov Thm 3.5 were never read directly, and four bibliographic repairs
are mandatory before paper-level use.

The point for this note: the LAW consumes **no** RATE constant, **no**
\(K_+\), **no** \(C_R\), **no** \(Q_0\), and no gate in §3. It holds for every
\(q\ge3\) with no threshold at all. It gives infinitely many off-line zeros
but **no location and no effective height** (its error is \(O_q(\log T)\) with
group-dependent implied constant, and it claims "no \(q\)-uniform error or
effective height"). The §2 theorem gives **one** zero at an **explicit**
location and height but only for \(q\ge10^{37}\) and only conditionally.

They are complementary, not competing, and the weakness of one is not evidence
for the other. If the §2 theorem collapses — for instance if the (H-RATE)
conflict in §3 resolves against RATE-A — **the LAW is untouched.**

### (d) Residual honesty items

- The theorem is **paper-level throughout**. No part is machine-verified or
  Lean-formalized. `BOUNDARY_ALPHA_THEOREM_SOL.md:737-738` says so explicitly.
- \(C_R''\) is self-graded an **unbanked candidate**
  (`CR_REDUCTION_V2_SOL.md:341`). Using it is the sharpest legitimate reading;
  a conservative referee should substitute the §4 published constant, giving
  \(Q_0=3.32\times10^{47}\).
- \(\gamma_1\) enters the geometry only through \(t_0=\gamma_1/2\) and the fact
  \(\phi_\infty(z_0)=0\); the theorem uses **no simplicity assumption** on
  \(\rho_1\) (`R3_TRANSPORT_EXECUTION_SOL.md:110`).
- I did not re-derive Lemmas 3.1/3.2, the `(FW)`/`(DH_{2,4})` chains, the
  \(m_z,\nu_z\) interval covers, or the printed-theory holomorphy argument.
  Those are consumed at their banked referee statuses, which is what an
  assembly note is for — and is also exactly its weakness.
- The §3 (H-RATE) conflict is the single most important thing on this page. A
  referee who reads only one paragraph should read that one.

---

## 6. Claim ledger for this note

| claim | status | receipt |
|---|---|---|
| \(C_R''=3018536183210772296097745\) recomputed from the §4 assembly with \(C_4''\) | **REPRODUCED** (this note, Arb, 160 dps) | §4.2, `C_R_pp`, `strict_upper: True`, `one_less_fails: True` |
| \(q_{\rm side}''=4746157036282968395\) | **REPRODUCED**, both minimality directions | §4.2 |
| \(q_{A0}''=11761546420922598622910053339543258496\) | **REPRODUCED**, both minimality directions, `A0_strict_lt_m` | §4.2 |
| \(N_{\rm monotone}\le q_{\rm side}''\) at \(B=K_+=117\) (route-H-correct \(K_F\)) | **COMPUTED** as an upper bound (D5: \(\le\)) | §4.2, §4.3 |
| \(Q_0=q_{A0}''\) over the **evaluable** gates | **COMPUTED** | §4.2 |
| \(Q_0\) is the closed all-gates onset | **NOT CLAIMED** — remainder of \(q_{\rm monotone}\) un-evaluated | §4.5 |
| the §2 theorem, parts (a)(b)(c) | **assembled, conditional on (H-RATE)…(H-ROUTE)**; carries the most-caveated status of each | §2, §3 |
| any status upgrade of any source | **NONE** | this note edits no file and banks no promotion |
| finite block \(3\le q<Q_0\) | **OPEN / UNDEFINED** | §3 non-assumed table; §5(b) |
| machine verification | **NOT CLAIMED** | §5(d) |

---

**READY FOR JUDGING**

---

## Dated correction block (2026-08-20, referee defects 1–5, append-only)

Applied per EFFECTIVE_THEOREM_ASSEMBLY_REFEREE.md (verdict GAPS NOT
REFUTED; re-referee of attacks 1b/3/5 required before any promotion):

- **D1 (refuted number)**: §5(b) ":604" — "enters as 1/(alpha nu_z) ~
  4.47" is WRONG; the true value is 1/(alpha nu_z) = 5.36941580756...;
  the neighbouring K_+ coefficient is (1-nu_z)/(alpha nu_z) =
  4.5357...; no assembly quantity equals 4.47.
- **D2 (scope of "binding")**: nu_z is the most elastic parameter of
  the C_R-INDEPENDENT FLOOR e^{T_0} (elasticity -42.4 vs -38.4 for
  alpha).  For the FULL Q_0 at C_R'', alpha is the most elastic
  parameter (elasticity -85.4), because alpha also discounts
  C_R^{1/alpha}.  A geometry change raising alpha dominates one raising
  nu_z at current C_R; only nu_z (or m_z, K_+) moves the floor.  The
  research-steering sentence is corrected accordingly.
- **D3 (missing gate row)**: §3's "Nothing is omitted" was false — the
  two-constants/Rouché transport implication itself is consumed from
  R3_TRANSPORT_EXECUTION_SOL.md:60-93,190-231, which has NO dedicated
  referee and self-grades "CONDITIONAL TRANSPORT THEOREM PROVED;
  CURRENT UNCONDITIONAL R3 REMAINS A GAP".  New gate row adopted
  verbatim from the referee:

  ### (H-TRANS) — the two-constants/Rouché transport implication itself
  Source R3_TRANSPORT_EXECUTION_SOL.md:60-93,190-231 ((R3-Z), (3.4),
  §4).  Status: PAPER-LEVEL, UNREFEREED.  What would discharge it: a
  cold referee on the harmonic-measure/two-constants application
  (boundedness of F_q on the closed rectangle, the omega(s,Gamma_R;
  Omega) interval cover, and the Rouché strictness on the disc
  boundary).

- **D4**: the Hejhal (7.22) citation lacks a page; the assembly must
  not be cited until the page is printed and asserted to lie inside the
  in-repo excerpt pp. 568-600 (routed via LAW_HEJHAL_S7_EXTRACT.md:
  67-81).
- **D5**: §4.3's "same phenomenon reproduced" — the q_side'' agreement
  is an algebraic identity (route-H B = K_+ makes the two closed forms
  the same function), not an empirical corroboration.

STATUS: this note remains UNPROMOTED pending the re-referee (attacks
1b, 3, 5 — the (RATE-A) grade-conflict adjudication among them).

---

## Dated correction block 2 (2026-08-20, re-referee findings, append-only)

Applied per EFFECTIVE_THEOREM_ASSEMBLY_REREFEREE.md (combined verdict
GAPS NOT REFUTED; attacks 1b/3/5 completed):

- **Adjudication adopted (attack 5)**: the (RATE-A) ledger conflict is
  RESOLVED as different scopes, both grades correct — Scope 1 (single
  matched boundary Gamma_R^A, exponent 6/5, q_RATE = 12) is
  CONFIRMED-conditional at paper level and is what this note's (H-RATE)
  assumes; Scope 2 (positive full-boundary rate + family-uniform
  N-independent whole-tail monotonicity, the (G2)/R5-DH2 form) is
  GENUINELY OPEN.  §3's "LIVE LEDGER CONFLICT" phrasing is superseded:
  (H-RATE) status reads "CONFIRMED-conditional (paper level)"; the two
  banked OPEN rows grade Scope 2.  D12 appended to
  R5_MONOTONICITY_GATE_SOL.md same turn.
- **Hejhal pointer corrected (attack 1b)**: (7.22) is at printed p. 577
  of lane_p/literature/Hejhal_LNM1001_Vol2_s7_pp568-600.pdf (in-range),
  same phi_N family (LAW_HEJHAL_S7_EXTRACT.md:19-24), algebra exact —
  BUT as printed it sits inside the contradiction proof of Thm 7.11
  scoped to a no-zero subsequence; the correct citation for the
  reflection at a zero is the UNCONDITIONAL phi(s)phi(1-s) ≡ 1 /
  Hejhal Cor. 7.12 (p. 579, "Proof. Trivial.").  The delta choice
  delta = 3/8 (< 1 and < gamma_1/10) is hereby stated.  D4 is thus
  repaired: page printed, in-range asserted, pointer corrected to
  Cor. 7.12.
- **NEW gate row (H-REFL)** (attack 3): the reflection identity's own
  hypotheses — unitarity |phi_q(1/2+it)| ≡ 1, meromorphic continuation
  across the line, same-order transfer — are consumed in step (c).
  Source: Hejhal Cor. 7.12 p. 579 + FJS §2.4 (phi(s)phi(1-s) = 1,
  fn. 1 reality) as banked in the LAW notes.  Status:
  PRINTED-LITERATURE, same tier as (H-RATE)'s printed inputs.
- **Gate count**: the theorem assumes EIGHT named gates (the original
  six + (H-TRANS) + (H-REFL)); §2's "six" is superseded.
- **D1 completed and corrected**: §5(b):604's "~4.47" is refuted (body
  unedited per append-only); the true values are 1/(alpha nu_z) =
  5.36941580756... and (1-nu_z)/(alpha nu_z) = 4.53608247422680... —
  correction block 1's "4.5357" (inherited from referee 1) is itself
  WRONG and is superseded by 4.53608... .
- **Cite fixes**: BOUNDARY_ALPHA Lemma 3.1 is at :335 not :333;
  the R5_ACTIVATION_CLOSURE_REFEREE rows are at :41-43 (the :244-245
  pointer was a quoted-file line-number confusion);
  R3_TRANSPORT_EXECUTION_SOL simplicity sentence at :118 not :110;
  LAW_SECOND_AUDIT_REFEREE:50 reads "generality used" not "needed".
- **§1.1 hash staleness**: BOUNDARY_ALPHA_THEOREM_SOL.md is now
  58ac377f... (the §10 promotion, commit 848bf17), superseding the
  recorded 5a8d0bcc...; 14/15 other hashes unchanged.
- **Q₀ UPDATED BY §10**: with the referee-CONFIRMED C_R''' =
  541656022363559883954520, the propagated cutoff is q_A0''' =
  2810199067910634377586449487575862960 (log10 = 36.4487,
  re-referee-reproduced independently) — 4.19x smaller than the boxed
  Q₀.  The theorem's threshold therefore reads Q₀ =
  max{q_RATE, q_divisor, q_side''', q_A0''', q_monotone} ≥
  2810199067910634377586449487575862960, superseding §4.5's boxed
  value; all conditionality unchanged.
- **Flag recorded**: the "RE-REFEREE: CONFIRMED — promotion unblocked"
  quote backing (H-C4) is an orchestrating-session verdict recorded in
  BOUNDARY_ALPHA:853-854, not a repo referee file.

STATUS: still UNPROMOTED; combined verdict across both passes is GAPS
NOT REFUTED.  Remaining dischargers: a referee for
R3_TRANSPORT_EXECUTION ((H-TRANS)) and a final completeness pass over
the eight-gate table.
---

## Dated correction block 3 (2026-08-20, final completeness pass, append-only)

Applied per EFFECTIVE_THEOREM_FINAL_PASS_REFEREE.md (house verdict
CONFIRMED at conditional scope).

- **(H-TRANS) status superseded (F1).**  Block 1's "Status:
  PAPER-LEVEL, UNREFEREED" is stale.  The gate's own named discharger
  has since reported: R3_TRANSPORT_EXECUTION_REFEREE.md (2026-08-20)
  confirms all three asks block 1 wrote — the two-constants
  application (subharmonic maximum principle re-derived; harmonic-
  measure orientation cross-checked by a series-free Monte Carlo), the
  omega(s, Gamma_R; Omega) interval cover (reproduced at a different
  discretisation and phase offset), and the Rouché strictness on
  \partial D_z.  Its blocking defect D1 (Hejhal (7.22) mis-scoped) and
  D3 (unstated real reflection) are APPLIED AT SOURCE in
  R3_TRANSPORT_EXECUTION_SOL.md's dated correction block.  (H-TRANS)
  now reads:

  ### (H-TRANS) — the two-constants/Rouché transport implication itself
  Source R3_TRANSPORT_EXECUTION_SOL.md:60-93,190-231 ((R3-Z), (3.4),
  §4), as repaired by its dated correction block.  Status: ANALYTIC
  CORE REFEREED-CONFIRMED at the stated conditional scope
  (R3_TRANSPORT_EXECUTION_REFEREE.md, attacks 1/2/4/5 CONFIRMED, every
  numeral reproduced at dps = 60); reflection clause repaired at source
  via Hejhal Cor. 7.12 p. 579 + real (7.5) coefficients.  NOT
  discharged by that pass and still carried elsewhere in this table:
  C_R, alpha, q_RATE (= (H-RATE)), q_divisor (= (H-HOL)), and a
  family-uniform K_+ (= (H-SIDE)).  What would discharge the remainder:
  machine formalization.

- **Supersession pointer corrected (F2).**  Block 2's "superseding
  §4.5's boxed value" is a mis-pointer: the boxed Q_0 is at §2 (the
  THEOREM display).  Read: the §2 box Q_0 = 11761546420922598622910053
  339543258496 is superseded BOTH in value (by q_A0''' =
  2810199067910634377586449487575862960) AND in form (equality ->
  the >= form of §4.5, since q_monotone's remainder is unevaluated).
  Independently reproduced this pass: q_side''' = 1134004458443795841,
  q_A0''' = 2810199067910634377586449487575862960, log10 = 36.4487370
  8539722848..., ratio to the old box 4.18530721..., both minimality
  directions and floor-endpoint agreement checked, E_R(q_A0''') <=
  9.890974306e-21 < 117 and K_+^{1-nu} E_R^{nu} < 0.0439 <= m_z both
  re-displayed at the new constant.

- **§1.1 hash staleness, second instance (F3).**
  R3_TRANSPORT_EXECUTION_SOL.md is now d53b0ae62e54fa34d07397807c6173
  15a7bf4f2a964f71b2460e66bf5cb6239e, not the recorded a6b6a1297...;
  the drift is exactly its append-only D1-D6 correction block, which
  strengthens this assembly.  BOUNDARY_ALPHA_THEOREM_SOL.md remains
  58ac377fc29af3daa3d869ec2d3a1dd9db630fdd3b5fa6e4864678cbbc4777d9.

- **(7.22)-route vestiges removed (F4).**  Block 2's "delta = 3/8" is a
  hypothesis of the ABANDONED printed-(7.22) route and is not consumed
  by the Cor. 7.12 route; it is withdrawn (the source's own repair uses
  delta = 1/2 for the same, now-unused, purpose).  (H-REFL) consumes
  exactly: meromorphic continuation of phi_q to C, the unconditional
  functional equation phi_q(s)phi_q(1-s) = 1 (Hejhal Cor. 7.12, p. 579,
  "Proof. Trivial."), and reality phi_q(\bar s) = conj(phi_q(s)) from
  the (7.5) coefficients.  Unitarity |phi_q(1/2+it)| = 1 is a
  CONSEQUENCE of those two, not an additional hypothesis; its listing
  in block 2 is withdrawn as over-broad.

- **(H-C4) evidence base strengthened (recorded, no status change
  claimed here).**  The operative constant is now C_R''' =
  541656022363559883954520, which HAS a repo referee file —
  CR_REDUCTION_V3_REFEREE.md, final verdict "CONFIRMED ... Required
  repairs: none ... fit to be banked as candidates".  Block 2's flag
  that the C_4'' backing quote was a session utterance stands for C_4'';
  it no longer describes the constant actually used.

- **phi_infty holomorphy on \overline{Omega} (recorded).**  Consumed
  inside (H-HOL) and UNCONDITIONALLY PROVED in
  R3_TRANSPORT_EXECUTION_REFEREE.md §4.2 (Gamma factors pole-free since
  Im s in [6.56, 7.57]; zeta(2s-1)'s pole at s = 1 excluded; 4^s != 1
  for Re s > 0; zeta(2s) != 0 by Hadamard-de la Vallee Poussin on
  Re = 1 and the Euler product beyond).  The source bundles it into a
  CONJECTURAL hypothesis; that is conservative, and the only genuinely
  open holomorphy gate is the finite-q one (q_divisor = 3).

STATUS: PROMOTED.  The assembled statement of §2, read with all three
correction blocks, is **CONFIRMED-conditional at paper level on the
EIGHT named gates** (H-RATE Scope 1), (H-HOL), (H-C4), (H-ROUTE),
(H-GEOM), (H-SIDE), (H-TRANS), (H-REFL), at threshold
Q_0 = max{q_RATE, q_divisor, q_side''', q_A0''', q_monotone}
    >= 2810199067910634377586449487575862960.
NOT machine-verified, NOT Lean-formalized, NOT unconditional; the finite
block 3 <= q < Q_0 remains OPEN / UNDEFINED and the remainder of
q_monotone remains CONJECTURAL, so the max is not claimed closed.
