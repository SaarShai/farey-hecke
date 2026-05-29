# T8/T8b — Hecke-group G_q generalization of the cluster=2 (2/9) rigidity: verdict

**Status (2026-05-28, session-resume synthesis).** Numerics high-precision verified;
**full G_4 rigidity theorem PROVED by hand (§3) AND ✅ MACHINE-CHECKED IN LEAN 4
(`code/BCZHeckeG4_core.lean`: `g4_core` + orbit wrapper `g4_no_three_below`, axioms =
standard 3 only, no `sorry`)** — q=4 √2/8 now at the SAME gold standard as q=3 2/9 (v8).
A uniform engine (§3b) proves q=3 AND q=4 by one mechanism. PROVEN family = the PAIR
{q=3: 2/9, q=4: √2/8}. q=∞ honestly RETRACTED (parabolic cusp ⇒ degenerate cross-section;
§3b). Adversarial-honesty throughout. LOCAL only.

## 1. What is solid (high-precision, mpmath dps=50)

The 3-window min-max  f3(q) = min_{x in T^q} max(P(x), P(Tx), P(T^2 x))  for the
Taha (arXiv:1810.10668) G_q BCZ map, observable P = reciprocal roof (= a·b in the
"diagonal" region):

| q | lambda_q | f3(q) | f3·lambda | minimizer (a,b) | orbit | trust |
|---|----------|-------|-----------|------------------|-------|-------|
| 3 | 1        | 2/9   | 2/9       | (2/3, 1/3) vertex| word [2,2,2], NO interior periodic orbit (boundary limit) | proven (v8) |
| 4 | √2       | √2/8  | 1/4       | (1/2, √2/4)      | **genuine interior period-2 orbit, word [3,3]** | **PROVEN (§3, full theorem, by hand)** |
| 6 | √3       | √3/9  | 1/3       | (1/√3, ~0) **b→0 BOUNDARY** | word [4,4,4], period-1 | DEGENERATE-BY-THEOREM (§2b: no integer period-2, sec²(π/6)=4/3∉ℤ) |
| ∞ | 2        | —     | —         | —                | —     | DEGENERATE (parabolic cusp; coded cross-section empty: d_i>1 ∀i, no region, no fixed pt — §3b) |

**Honest reading.** q=4 is a *new* PROVEN constant: √2/8 with a verified interior
period-2 orbit (not a boundary artifact), full theorem by hand in §3. q=3 reproduces the
proven 2/9. q=6's minimizer sits on b≈0 (degenerate boundary) — explained by §2b (no integer
period-2 since sec²(π/6)=4/3∉ℤ). q=∞ now COMPUTED → degenerate: the parabolic cusp empties
the coded cross-section (§3b), so q=∞ is not a genuine family member (1/9 was an ungrounded
abstract-recurrence value, retracted).

**Numerology (NOT a law).** f3·lambda_q = 2/9, 1/4, 1/3 = **2/(12−q)** for q=3,4,6.
This is a 3-point fit (one point degenerate), has a pole at q=∞, and the arithmetic
Hecke groups are only {3,4,6,∞} — so it is *suggestive coincidence*, not an established
family law. Do NOT cite 2/(12−q) as a result.

## 2. q=4 analytical lead (upgrades #2 from numerics toward theorem)

For q=4, lambda=√2. Hecke vectors w_i = U^i(1,0), U=[[√2,−1],[1,0]]:
  w0=(1,0), w1=(√2,1), w2=(1,√2), w3=(0,1), w4=(−1,0).
Domain T^4 = {0<a≤1, 1−√2a<b≤1} (i.e. √2a+b>1). Regions i∈{2,3}:
  T_2: √2a+b>1 and a+√2b≤1;  P = a(a+√2b)/√2  (y_2=√2).
  T_3: a+√2b>1 and b≤1;       P = a·b           (y_3=1)  ← optimizing region.
In T_3 the map is T(a,b) = (b, k√2b − a),  k = ⌊(1+a)/(√2 b)⌋ ≥ 1.
**This is the classical (q=3) BCZ map with b ↦ √2 b in the floor and recurrence.**

**Step-1 analogue (the key new computation).** In T_3 the region constraint gives
a > 1 − √2 b, hence
        a·b  >  (1 − √2 b)·b.
The right side has  max_b (1 − √2 b) b = √2/8, attained ONLY at b = √2/4 = 1/(2√2)
(since (1−√2b)b = √2/8 − 8·(... )? explicitly 8b² − 4√2 b + 1 = 8(b − √2/4)², a perfect
square ⇒ double root). At b=√2/4 the boundary a = 1 − √2 b = 1/2, giving
        f3(4) = a·b = (1/2)(√2/4) = √2/8.
So the optimizer (1/2, √2/4) is FORCED analytically, matching the numerics exactly. The
mechanism is cleaner than q=3: a *double root* (single forced point) rather than q=3's two
branches {b<1/3, b>2/3} + a branch-elimination step.

### 2a. Single-sequence reduction + RIGOROUS period-2 classification (new, 2026-05-28)

Every region-3 step has a_{n+1}=b_n, so an orbit collapses to ONE scalar sequence (c_n)
with b_n=c_{n+1}, window products P(x_n)=c_n·c_{n+1}, and the three-term recurrence
        c_{n+2} = ⌊(1+c_n)/(√2 c_{n+1})⌋ · √2 c_{n+1} − c_n,
        region constraint  c_n + √2 c_{n+1} > 1,  c_n,c_{n+1} ∈ (0,1].
(This is the G_4 analogue of the classical Farey/BCZ consecutive-gap-product sequence.)

**Period-2 orbits fully classified.** A period-2 (alternating) orbit c: x,y,x,y has
c_{n+2}=c_n, forcing c_0 = k_0√2 c_1/2 with floor value k_0, and the RETURN step on (c_1,c_0)
forces k_1 = 2/k_0. Hence k_0·k_1 = 2, so {k_0,k_1}={1,2} are the ONLY consistent pairs;
k_0≥3 admits NO period-2 orbit. Both families (k_0=2: c_0=√2 c_1, product √2 c_1²;
k_0=1: the mirror) have product → √2/8 as c_1 ↓ √2/4 (resp. ↑ 1/2), the floor-discontinuity
boundary limit at the orbit (1/2,√2/4)↔(√2/4,1/2). VERIFIED numerically (mpmath dps=30,
2×10^5 grid per k_0): k_0∈{1,2} only, min product 0.17677849… → √2/8 at the boundary;
k_0∈{3,4,5,6} empty. **So √2/8 is rigorously the best PERIODIC (period-2) orbit.** The
remaining open piece is purely the no-better-APERIODIC-orbit lower bound (next section).

### 2b. Period-2 ground-state EXISTENCE criterion across Hecke groups (new, 2026-05-28)

**Result.** For the arithmetic-Hecke G_q region-(q−1) BCZ map, the recurrence is
c_{n+2}=k λ c_{n+1}−c_n with floor word (k_n), matrix M_k=[[0,1],[−1,kλ]]∈SL_2.
A period-2 orbit is a parabolic (eigenvalue-1, trace-2) fixed direction of M_{k_1}M_{k_0};
its trace is λ²k_0k_1 − 2, so trace=2 forces
        k_0 · k_1 = 4/λ² = sec²(π/q).
A genuine period-2 ground-state orbit (integer floor word) therefore EXISTS iff
sec²(π/q) ∈ ℤ_{>0}. Among the four arithmetic Hecke groups q∈{3,4,6,∞}:
  q=3: sec²60°=4 ⇒ {k_0,k_1}∈{(1,4),(2,2),(4,1)}, min product → 2/9      [VERIFIED]
  q=4: sec²45°=2 ⇒ {(1,2),(2,1)},                     min product → √2/8 [VERIFIED]
  q=6: sec²30°=4/3 ∉ ℤ ⇒ NO integer period-2 orbit                       [VERIFIED: empty]
  q=∞: sec²0°=1 ⇒ {(1,1)} abstractly, BUT theta-group cross-section is DEGENERATE — see §3b
       HONEST RETRACTION: U parabolic (trace 2), w_i=(i+1,i) never hits (0,1), d_i>1 always,
       no fixed point. So q=∞ is NOT a genuine member; 1/9 is an ungrounded formal value.

**Consequence (honest correction to the table).** G_6 is arithmetic yet has NO period-2
ground state, so its min-max optimizer cannot be an interior period-2 orbit — it degenerates
to the b→0 boundary (period-1 word [4]), exactly as the numerics showed. So the earlier
"SUSPECT (degenerate)" flag on √3/9 is now EXPLAINED, not a numerical artifact. The right
dividing line is NOT arithmeticity but the Niven-type condition sec²(π/q)∈ℤ, satisfied only
by q∈{3,4,∞} (cf. tan²(π/q)∈{0,1,3}). This refines §2a/§4 and kills the naive
"family law across {3,4,6,∞}" idea: q=6 is structurally different.

**Explicit ground-state family (verified at recurrence level, mpmath dps=30).** For the
FINITE Hecke lattices q=3,4 with sec²(π/q)∈ℤ, the min-max product (boundary limit of the
period-2 ground state) is:
  q=3  (λ=1):   orbit (1/3,2/3), k=(1,4) → **2/9**     [PROVEN, v8 + uniform §3b]
  q=4  (λ=√2):  orbit (1/2,√2/4), k=(2,1) → **√2/8**   [PROVEN, §3 full theorem + uniform §3b]
  q=∞  (λ=2):   abstract recurrence → 1/9   ⚠ NOT realized on the theta group — see §3b
               HONEST RETRACTION: G_∞'s coded cross-section is degenerate (parabolic cusp).
The PROVEN pair {2/9, √2/8} is a REAL mechanism-based family (period-2 ground state at the
region boundary), NOT the discredited 2/(12−q) numerology — the structure is in the k-word
(k_0k_1=sec²(π/q)), not in any closed form for the value. The earlier "{2/9,√2/8,1/9} triple"
overclaimed q=∞: the parabolic theta group breaks the finite-region construction, so 1/9 is an
ungrounded formal value, not a verified theta-group cluster constant (RESOLVED, not "cheap
remaining check" — the check was DONE and the q=∞ map is degenerate as coded).

## 3. FULL G_4 RIGIDITY THEOREM — PROVED (2026-05-28, by hand; brute-force-verified)

**Theorem (G_4 cluster rigidity).** For the Hecke group G_4 (λ=√2) BCZ map T on the domain
T^4={0<a≤1, 1−√2a<b≤1} with gap-product observable P (region-dependent: P=a(a+√2b)/√2 in
T_2, P=a·b in T_3),
        inf_{x∈T^4} max( P(x), P(Tx), P(T²x) ) = √2/8,
the infimum approached (not attained — a region-boundary/floor-discontinuity limit) by the
period-2 orbit family (1/2,√2/4)↔(√2/4,1/2). Equivalently max(P,P∘T,P∘T²) > √2/8 ∀x∈T^4,
sharp. This is the SECOND proven BCZ cluster-rigidity constant after q=3's 2/9.

Write t = √2/8 = 1/(4√2). Proof in five steps; all inequalities elementary (no nlinarith).

**Step 1 — region T_2 is automatically safe.** min over T_2 of P = 1 − 1/√2 ≈ 0.293 > t.
[Pf: set u=a+√2b. In T_2, P=au/√2, the region √2a+b>1 ⟺ a+u>√2 ⟺ a>√2−u, with u≤1 and
a≤1; so u>√2−1 (else a>√2−u>1). Min of au over the closed region is at the corner, value
√2−1, giving P=(√2−1)/√2=1−1/√2.]  Hence if ANY of x,Tx,T²x lies in T_2, that window's
P ≥ 1−1/√2 > t, so the max > t. ⇒ to have max < t, ALL THREE points lie in T_3.

**Step 2 — single-sequence form (all three in T_3).** Write the three points
x_0=(c_0,c_1), x_1=(c_1,c_2), x_2=(c_2,c_3) (since T sends (a,b)↦(b,·), a_{n+1}=b_n).
T_3 recurrence c_{n+2}=k_n√2 c_{n+1}−c_n with k_n=⌊(1+c_n)/(√2 c_{n+1})⌋≥1 (n=0,1) gives
c_0=k_0√2c_1−c_2, c_3=k_1√2c_2−c_1, hence the identities
        p_0 := c_0c_1 = k_0√2 c_1² − p_1,   p_2 := c_2c_3 = k_1√2 c_2² − p_1,   p_1 := c_1c_2.
T_3 membership of x_n is R_n: c_n+√2c_{n+1}>1, with c_n,c_{n+1}∈(0,1].

**Step 3 — only (k_0,k_1)∈{(1,1),(2,1)} can give all three < t.** Assume p_0,p_1,p_2<t.
From p_0+p_1=k_0√2c_1²<2t=√2/4 ⇒ c_1²<1/(4k_0) ⇒ c_1<1/(2√k_0). Likewise (p_1+p_2)
⇒ c_2<1/(2√k_1). Plug into R_1 (c_1+√2c_2>1):
        1 < c_1+√2c_2 < 1/(2√k_0)+√2/(2√k_1)  ⇒  1/√k_0 + √2/√k_1 > 2.
Enumerating integers k_0,k_1≥1, this holds ONLY for (1,1) [=2.414] and (2,1) [=2.121];
(1,2)=2.000 (not >2), (2,2),(3,1),… all <2. (For any other pair R_1 is already violated.)

**Step 4 — case (2,1) is impossible.** Here c_1<1/(2√2)=√2/4. The floor k_0=2 means
(1+c_0)/(√2c_1)<3, i.e. 1+c_0<3√2c_1; with c_0=2√2c_1−c_2 this gives 1−c_2<√2c_1, i.e.
c_1>(1−c_2)/√2. Combined with c_1<√2/4: (1−c_2)/√2<√2/4 ⇒ c_2>1/2. But c_2<1/(2√1)=1/2.
Contradiction. ∎(case)

**Step 5 — case (1,1) is impossible (middle product exceeds t unconditionally).**
The OUTER region constraints pin c_1,c_2 from below:
  R_0: c_0+√2c_1>1 with c_0=√2c_1−c_2>0 ⇒ 2√2c_1−c_2>1, and c_2>0 ⇒ c_1>1/(2√2)=√2/4;
  R_2: c_2+√2c_3>1 with c_3=√2c_2−c_1 ⇒ 3c_2−√2c_1>1 ⇒ c_2>(1+√2c_1)/3.
Therefore  p_1 = c_1c_2 > c_1·(1+√2c_1)/3 =: h(c_1).  h is increasing and
h(√2/4) = (√2/4)(1+1/2)/3 = (√2/4)(1/2) = √2/8 = t exactly. Since c_1>√2/4, p_1>h(c_1)>t,
contradicting p_1<t. ∎(case)

Steps 3–5 exhaust the cases ⇒ no T_3-triple has all products <t ⇒ (with Step 1) max≥t
on all of T^4. Upper bound: the period-2 family (§2a) gives max→t. Hence inf=t=√2/8. ∎

### 3b. UNIFORM region-(q−1) core lemma — proves q=3 and q=4 by one mechanism (new, 2026-05-28)

The five-step G_4 proof generalizes to one calculation valid for every λ=2cos(π/q). It
proves the **region-(q−1) core lemma** for the FINITE Hecke lattices with sec²(π/q)∈ℤ — i.e.
q=3 and q=4 (q=∞ is degenerate, see end of section): in the diagonal region (P=ab,
single-sequence form), the 3-window min-max equals the ground-state value t_q. Write the
diagonal recurrence
        c_{n+2} = k_n λ c_{n+1} − c_n,   k_n = ⌊(1+c_n)/(λ c_{n+1})⌋ ≥ 1,
region constraints R_n: c_n + λ c_{n+1} > 1, with products p_n = c_n c_{n+1}.

**The single identity.** From c_0+c_2 = k_0 λ c_1 (and c_1+c_3 = k_1 λ c_2):
        p_0 + p_1 = c_1(c_0+c_2) = k_0 λ c_1²,    p_1 + p_2 = k_1 λ c_2².
So "all three products < t" forces c_1 < √(2t/(k_0λ)) and c_2 < √(2t/(k_1λ)). Substituting
into the MIDDLE region constraint R_1 (c_1 + λ c_2 > 1) gives the **uniform k-reduction**:

        ┌─────────────────────────────────────────────────────────────┐
        │   a floor word (k_0,k_1) can give all 3 windows < t  ONLY if  │
        │            1/√k_0  +  λ/√k_1   >   √( λ / (2t) ).             │
        └─────────────────────────────────────────────────────────────┘

**Self-consistency (the reason t is forced).** Plug each family's ground-state value
t_q and its ground word (k_0,k_1) with k_0k_1 = sec²(π/q) (§2b). In EVERY case the ground
word lands *exactly on* the threshold √(λ/2t) — never strictly above:
  q=3 (λ=1,  t=2/9):   √(λ/2t)=3/2;  ground word (1,4)/(4,1):  1/√1+1/√4 = 3/2  (= thr)
  q=4 (λ=√2, t=√2/8):  √(λ/2t)=2;    ground word (1,2):        1/√1+√2/√2 = 2    (= thr)
  q=∞ (λ=2,  t=1/9):   √(λ/2t)=3;    ground word (1,1):        1/√1+2/√1 = 3     (= thr)
                       ⚠ q=∞ is the ABSTRACT λ=2 recurrence only — NOT a theta-group point
                         (degenerate; see HONEST RETRACTION at end of §3b).
Because the surviving condition is STRICT (products strictly < t), the ground word is
*excluded* — consistent with the infimum being approached, not attained (a boundary limit).
This pins t_q as the unique value at which the ground word sits on the reduction boundary.

**Surviving cases to kill, per family** (integers k_0,k_1≥1 strictly above threshold;
verified by enumeration):
  q=3:  {(1,1),(1,2),(2,1),(1,3),(3,1)}   — 5 cases   [core min-max 0.22241 ≈ 2/9]   GENUINE
  q=4:  {(1,1),(2,1)}                       — 2 cases   [core min-max 0.17737 ≈ √2/8] GENUINE
  q=∞:  {}                                   — 0 cases   [abstract recurrence → 1/9]  ⚠ NOT a
        theta-group cross-section (degenerate; see HONEST RETRACTION below)
This reproduces the v8 value 2/9 for q=3 far more cleanly (5 elementary case-kills, no SOS)
and is the same engine that gave √2/8 in §3.

**q=3 case-kills (λ=1, t=2/9; c_1,c_2 < (2/3)/√k via the identity).**
 • (1,1): R_0 (c_0=c_1−c_2, c_0+c_1>1) ⇒ 2c_1−c_2>1 ⇒ c_1>1/2; R_2 (c_3=c_2−c_1) ⇒
   2c_2−c_1>1 ⇒ c_2>(1+c_1)/2. Then p_1=c_1c_2 > c_1(1+c_1)/2 ≥ (1/2)(3/2)/2 = 3/8 > 2/9. ✗
 • (1,2): R_0 ⇒ c_1>1/2; R_2 (c_3=2c_2−c_1) ⇒ 3c_2−c_1>1 ⇒ c_2>(1+c_1)/3 > 1/2.
   Then p_1 = c_1c_2 > (1/2)(1/2) = 1/4 > 2/9. ✗   [(2,1) is the time-reverse ⇒ same kill]
 • (1,3): floor k_0=1 ⇒ 1+c_0<2c_1 ⇒ (c_0=c_1−c_2) ⇒ c_1>1−c_2; R_2 (c_3=3c_2−c_1) ⇒
   4c_2−c_1>1 ⇒ c_2>(1+c_1)/4. Combine: c_2>(2−c_2)/4 ⇒ c_2>2/5=0.40, but the identity
   gives c_2<(2/3)/√3 = 2/(3√3) = 0.3849. Contradiction. ✗   [(3,1) by time-reversal]
All 5 dead ⇒ core min-max = 2/9 for q=3, recovered uniformly.

**q=4 case-kills:** the (1,1) and (2,1) kills are Steps 5 and 4 of §3 verbatim. ✓

**q=∞ (theta group, λ=2): the abstract value t=1/9 is NOT grounded — HONEST RETRACTION.**
The boxed reduction applied to the abstract λ=2 single-sequence recurrence c_{n+2}=2c_{n+1}−c_n
has zero surviving cases and a constant ground sequence c≡1/3 with product 1/9. BUT — and this
is the correction — that recurrence is the region-(q−1) form, which exists only because finite
G_q has a region with w_{q−1}=(0,1) (forcing a_{n+1}=b_n). **The literal theta group has NO
such region.** For q=∞, U=[[2,−1],[1,0]] has trace 2 (parabolic, infinite order), so the Hecke
vectors w_i=(i+1,i) grow linearly and never return to (0,1). Worse, with the cross-section
domain 2a+b>1 used for finite q, one has d_i=a(i+1)+bi ≥ d_1=2a+b > 1 for EVERY i≥1 (verified:
min over domain = 1.0 on the boundary), so the region test "d_{i−1}>1 and d_i≤1" is NEVER
satisfied — the coded Taha cross-section is empty/degenerate at q=∞ (this, not a trivial
unpacking bug, is why the T8b q=∞ scan returns nothing). And the map has NO interior fixed
point: a_{n+1}=d_i=a forces i(a+b)=0, impossible for i≥1, a,b>0 — so the "(1/3,1/3) fixed
point" is an artifact of the abstract recurrence, not a point of the theta-group map.
**Claim status: q=∞ is NOT an established member of the family.** 1/9 is the ground value of a
formal λ=2 recurrence; whether it equals a cluster constant of some genuine theta-group
cross-section (Taha's finite-q one is degenerate here — the parabolic cusp makes q=∞
structurally different, just as §2b's Niven criterion and §4 already hinted) is UNVERIFIED.
The honest proven family is **{q=3: 2/9, q=4: √2/8}** — both finite Hecke lattices.

**Net.** A single general-λ reduction (the boxed inequality) drives the two finite arithmetic
Hecke groups with sec²(π/q)∈ℤ: q=3 and q=4. It (i) re-proves 2/9 and √2/8 with one mechanism,
and (ii) exhibits t_q as the value pinned by the ground word (k_0k_1=sec²(π/q)) sitting exactly
on the reduction boundary. The irrationality of λ never obstructs anything — every step is one
completed square. The q=∞ "third member" does NOT hold up: the theta group's parabolic cusp
breaks the finite-region cross-section, so the family is a PAIR {3,4}, not a triple.

**Status.** Proof is complete and elementary. Brute-force over T^4 (900×900 grid, both
regions, actual floors): min max = 0.17727 > t = 0.17677, zero violations — consistent with
the unattained infimum t. Mechanism cleaner than q=3/v8: the killer is the squeeze double
root (h(√2/4)=t exactly, Step 5) + a 2-case floor split (Steps 3–4), no heavy SOS needed.
Irrational √2 enters only through the constants 1/(2√2), √2/4, √2/8 = 1/(4√2) — all handled
by `nlinarith [sq_nonneg (b - s/4)]` type hints with `s` abstract, `s^2 = 2`, `s > 0`.

**✅ MACHINE-CHECKED IN LEAN 4 / Mathlib (2026-05-28).**
File `code/BCZHeckeG4_core.lean` — two theorems, compiles clean (no `sorry`, no `admit`,
no `native_decide`):
- `g4_core (s a b c d : ℝ) …` — the real-arithmetic core: with `s^2 = 2`, `s > 0`, the four
  positive coords `a,b,c,d`, region sums `a+s·b, b+s·c, c+s·d > 1`, recurrence
  `a+c = k₀·s·b`, `b+d = k₁·s·c` (`k₀,k₁ : ℤ`, `≥ 1`), and floor upper bound
  `1+a < (k₀+1)·s·b`, the three products `a·b, b·c, c·d` are NOT all `< s/8`. Proof = the
  §3 hand-proof verbatim: `e1,e2` recurrence sums → `b²<1/4` → `c²>1/8` → `k₁=1` →
  `c<1/2` → `b²>3/2−s` with `s<17/12` → `k₀≤2` → `interval_cases k₀` (k₀=1: `b·c ≥ s/8`
  contra; k₀=2: floor forces `c>1/2` contra `c<1/2`).
- `g4_no_three_below (s : ℝ) (hs : s^2=2) … (c : ℕ → ℝ) …` — orbit-form wrapper mirroring
  v8 `cluster_size_le_two_clean`: for any positive sequence above the line
  `c n + s·c(n+1) > 1` evolving by the floor recurrence
  `c(n+2) = ⌊(1+c n)/(s·c(n+1))⌋·s·c(n+1) − c n`, no three consecutive gap-products
  `c n · c(n+1)` are all `< s/8 = √2/8`. The floor word `k ≥ 1` is derived from orbit
  positivity (`k·s·c(n+1) = c n + c(n+2) > 0`); the floor upper bound from
  `Int.lt_floor_add_one` + `div_lt_iff₀`.

`#print axioms` ⇒ both depend on `[propext, Classical.choice, Quot.sound]` only (the three
standard Mathlib axioms; no `sorryAx`). So q=4 √2/8 cluster rigidity now sits at the SAME
gold standard as the q=3 2/9 result (v8 `BCZClusterCleanProof.lean`).

## 4. Non-arithmetic q (5,7,12): likely ill-posed

T8 saw non-monotone messy values there. The non-arithmetic Hecke groups are not lattices
with a clean discrete-Farey structure, so the "consecutive Farey fraction / cluster"
question is plausibly not well-defined for them. Treat q∈{5,7,12} numbers as artifacts
absent a well-posedness argument. (Literature check not completed — the background worker
was killed before recording it.)

## 5. Verdict

- **q=4 √2/8 is now a PROVEN, ✅ MACHINE-CHECKED THEOREM (§3), not just numerics** — the
  full G_4 cluster-rigidity lower bound min-max=√2/8 is established by hand (5 elementary
  steps: T_2-safe reduction + single-sequence form + 2-case floor split + double-root
  squeeze), brute-force-verified, AND formally verified in Lean 4 / Mathlib
  (`code/BCZHeckeG4_core.lean`: `g4_core` real-arithmetic core + `g4_no_three_below` orbit
  wrapper; `#print axioms` = `[propext, Classical.choice, Quot.sound]` only, no `sorry`).
  This is the SECOND proven BCZ cluster constant after q=3's 2/9, now at the SAME Lean
  gold standard as v8's `BCZClusterCleanProof.lean`. The period-2 part is rigorously
  classified (§2a, k_0k_1=2).
- **Cleanest new structural result (§2b): the period-2 ground state exists iff
  sec²(π/q)∈ℤ AND q<∞ (finite Hecke lattice).** sec²∈ℤ holds for q∈{3,4,∞} (=4,2,1), FALSE
  for the arithmetic group q=6 (=4/3); the lattice condition then excludes q=∞ (parabolic
  cusp, §3b). So among arithmetic q∈{3,4,6,∞} exactly {3,4} have an interior ground state.
  This explains G_6's degenerate boundary optimizer (fails sec²∈ℤ) and G_∞'s degeneracy
  (fails lattice), and replaces the bogus "2/(12−q) family law" with a real Niven-type
  criterion + a lattice condition. This is the most defensible single take-away of T8b.
- **Uniform engine (§3b): one general-λ reduction proves the region-(q−1) core for q=3 AND
  q=4 by the SAME mechanism.** A floor word (k_0,k_1) can dip below t only if
  1/√k_0+λ/√k_1 > √(λ/2t); the ground word (k_0k_1=sec²(π/q)) sits EXACTLY on this threshold,
  which is what pins t. Surviving cases: 5 (q=3, all killed → 2/9), 2 (q=4, all killed → √2/8).
  So the proven family is the PAIR {q=3: 2/9, q=4: √2/8}.
- **q=∞ does NOT hold up (honest retraction, §3b end).** The theta group's U=[[2,−1],[1,0]] is
  parabolic (trace 2), so its Hecke vectors w_i=(i+1,i) never return to (0,1) and the coded
  finite-q cross-section is degenerate at q=∞ (d_i>1 throughout ⇒ no valid region; no fixed
  point). The value 1/9 is the ground state of an ABSTRACT λ=2 recurrence with no realization
  on Taha's theta-group map. So the sec²(π/q)∈ℤ "family" of PROVEN cluster constants is a pair
  {3,4}, not a triple — the parabolic cusp breaks the construction at q=∞.
- With the §3 proof, this is no longer "modest numerics" — it is a complete second theorem
  in the BCZ cluster-rigidity / ergodic-optimization program (see T9/T12 breakthrough #1):
  the rigidity phenomenon provably transfers from SL_2(ℤ) to the Hecke group G_4 with a new
  constant √2/8 and a cleaner proof mechanism.

## 6. Ergodic-optimization transfer to G_4 + complete arithmetic-Hecke dichotomy (new, 2026-05-28)

Two consequences that lift the pointwise §3 theorem to the measure-theoretic level and close
the arithmetic family.

**6a. Measure-theoretic ergodic optimization for G_4 (corollary of §3 + the T12 argument).**
THEOREM. Let T be the G_4 BCZ return map on T^4 and P the gap-product observable (§3). For
EVERY T-invariant Borel probability measure μ on T^4,
        ess-sup_μ P ≥ √2/8,
and √2/8 is sharp (approached by the period-2 ground-state family of §2a). 
Proof. The T12 forward-good-set argument is abstract and needs only (a) T is a measurable
self-map of the domain and (b) the pointwise 3-window bound max(P,P∘T,P∘T²) ≥ t. (b) is §3
with t=√2/8; (a) is verified — T^4 is a return cross-section, and a direct check (8×10^6
iterated steps from 2×10^5 random domain points) found 100% of forward orbits remain in T^4,
0 exits. Given these: if ess-sup_μ P ≤ t'<√2/8 then A={P≤t'} is μ-full; each T^{-n}A is μ-full
by invariance; G=⋂_{n≥0}T^{-n}A is μ-full (countable intersection) hence nonempty; any x∈G has
P(T^n x)≤t' ∀n, so max(P(x),P(Tx),P(T²x))≤t'<√2/8, contradicting (b). ∎ (Poincaré not needed;
bound fully unconditional. Same closure caveat as q=3: over OPEN T^4 the infimum √2/8 is
unattained, so the equality-case "μ = the period-2 measure" needs the closed domain T̄^4.)
**Significance.** Ergodic optimization of the BCZ/horocycle-return map (breakthrough #1, T9/T12)
is NOT special to SL_2(ℤ): it transfers to the Hecke lattice G_4 with the new ground-state
value √2/8. The 2/9 result is one instance of a family of horocycle-return ground states.

**6b. Complete dichotomy across the arithmetic Hecke groups {3,4,6,∞}.** Combining §2b (period-2
existence ⇔ sec²(π/q)∈ℤ), §3 (q=4 proof), v8 (q=3), the q=6 numerics (§1), and the q=∞
retraction (§3b):

  | q | sec²(π/q) | lattice? | interior period-2 ground state? | cluster constant |
  |---|-----------|----------|--------------------------------|------------------|
  | 3 | 4   ∈ℤ    | yes      | YES (k₀k₁=4)                   | 2/9   (PROVEN)   |
  | 4 | 2   ∈ℤ    | yes      | YES (k₀k₁=2)                   | √2/8  (PROVEN)   |
  | 6 | 4/3 ∉ℤ    | yes      | NO (Niven fails)               | none interior; boundary √3/9 only |
  | ∞ | 1   ∈ℤ    | NO (parabolic) | NO (cross-section degenerate) | none (1/9 ungrounded) |

DICHOTOMY. Among the arithmetic Hecke groups, an interior period-2 ground state — equivalently
a BCZ cluster-rigidity constant of the §3b ground-word type — exists **iff sec²(π/q)∈ℤ AND q<∞**,
i.e. exactly for q∈{3,4}, with the two PROVEN constants 2/9 and √2/8. The two exclusions have
DISTINCT mechanisms: q=6 fails the Niven-type arithmetic condition sec²∈ℤ; q=∞ fails the
lattice condition (parabolic cusp empties the cross-section). This is the complete, honest
classification — no "family law in q", but a clean two-condition criterion and a proven pair.
