# Cramér–Rao lower bound T1 in the frozen model

- Type: research
- Mode: AFK
- Status: **A2 ENACTED** (A1 + A2 both enacted 2026-08-15; T1 draft v3; gaps
  ledger 17 entries, **4 closed / 13 open** — A2 closed GAP-3, GAP-14, GAP-15,
  reduced GAP-4, and opened GAP-16, GAP-17)
- Claimed by: lane T-opus
- Blocked by: none
- Source: user request 2026-08-14 "this should be your goal. continue down this path" + "also pursue this"

## Question
Does the CR lower bound of G1_MODEL_SPEC.md §4 T1 hold in noise model N2
with explicit constants — max_j RMSE ≥ c_d·S_ε(γ_j)^{1/2}/(a_{γ_j}(log X)^{3/2}),
yielding X(ε) exponential in ε^{-2/3}?

## Resolution
DRAFTED 2026-08-15 — research_notes/rh_goals_2026-08-14/lane_t/T1_CRAMER_RAO_DRAFT.md.
Bound holds in model N2 with c_d = sqrt(6) (independent of d); S_ε(ω) =
a_|ω|² log(|ω|/2π), so the ζ′ amplitudes CANCEL and the bound reduces to
max_j RMSE ≥ sqrt(6·log(γ_d/2π))/(log X)^{3/2}, giving
X(ε) ≥ exp((6 log(γ_d/2π))^{1/3} ε^{-2/3}) — c = 1.694 (d=1), 2.316 (d=10).
Gate G-a does not fire for the leading constant (amplitude-free). Gate G-b
passes: bound 0.0493 vs Gate-1 empirical 0.249 at X=3e7, d=10 → 5.05×.
Not closed: 13 gaps logged (§6), of which (R1) needed a band-limitation
repair NOT in the frozen spec (spec amendment owed), (R6) Gaussian-
approximability FAILS under the Gaussian smoothing W, and the γ_1 empirical
error sits 5.5× BELOW the bound (N2 is pessimistic at low height).

AMENDMENT APPROVAL 2026-08-15 (owner): M4-prime band-limitation
amendment APPROVED by owner ("i approve M4"). Logged per preregistration
discipline: the frozen model gains the band-limit clause Omega = 2*Gamma
repairing regularity (R1); see lane_t/T1_CRAMER_RAO_DRAFT.md GAP-2.
EXECUTION GATED: commence amendment write-up + T1 revision when the
owner reconnects (owner instruction).

EXECUTED 2026-08-15. (1) G1_MODEL_SPEC.md gains an additive, dated
"AMENDMENT A1 (2026-08-15, owner-approved)" section — clause M4′
(band limit |omega| <= Omega := 2*Gamma, estimator class restricted
accordingly), what it repairs ((R1) mutual absolute continuity, by
removing the vacuous infinite-information artifact of the
super-exponentially decaying noise floor / divergent Cameron-Martin
integral), and the honesty note that it is a post-freeze, post-hoc
amendment. The frozen v0 body is untouched. (2) Same section records
(R6)/GAP-3 as OPEN, KNOWN-FALSE AS WRITTEN, with the recommended
window replacement logged as "proposed amendment A2, AWAITING OWNER
RULING" — not enacted. (3) T1 draft revised to v2: M4′ cited in the
hypothesis set, GAP-2 CLOSED (REPAIRED-BY-A1); Fisher computation
re-derived under the band limit (new §4.0) — tones interior with
margin >= Gamma, S_ε(gamma_j) unchanged, factor 24 re-verified
(band-limited 3x3 FIM, white noise: 23.93 / 23.82 / 23.95 -> 24).
(4) Two findings the re-derivation forced, both logged rather than
smoothed over: v1's claim that a band-limited bound transfers to the
unrestricted record is BACKWARDS (band-limiting raises the CR bound),
so M4′ is an estimator-class restriction — corrected in v2 and in
spec §A1.3; and at the approved cut Omega = 2*Gamma the band-edge
leakage dominates the Fisher information (measured [I^-1]_ww is
7.7e-30 of the local 24-value at Gamma=50, T=17.2167), so T1 now
carries an explicit leakage hypothesis (B1) = new GAP-14, holding
only for Omega - gamma_d = O(1). GAP-15 (positivity of extended S_ε
below |omega| = 2*pi, benign but real) also opened. Ledger: 15
entries, 1 closed, 14 open.

AMENDMENT A2 APPROVED + ENACTED 2026-08-15 (owner: "i trust your
judgement. please do what you recommend", ruling on the A2 question
left open at G1_MODEL_SPEC §A1.5; the frontier recommendation on the
table was APPROVE). Window replaced: Gaussian W(x)=exp(-x^2),
M_W=0.5*Gamma(s/2) -> order-1 Riesz/Fejer W(x)=(1-x)_+,
M_W(s)=1/(s(s+1)), |M_W(1/2+i.omega)| ~ |omega|^-2. Chosen over Hann /
cos^2, higher Riesz orders, C-infinity bumps and the sharp cutoff
because it is the MILDEST smoothing that keeps the observable defined:
k=0 (sharp cut) makes sum_gamma a_gamma diverge, so the line-spectrum
representation is not absolutely convergent; k>=2 loses the closed
form (Hann needs a generalised cosine integral) and WORSENS the GAP-4
flatness defect, which scales like 2(k+1)/(omega*T). It also keeps
R_0 = -2 exactly, keeps M_W in closed form, and turns the arithmetic
side into the finite Cesaro mean (1/N)*sum_{k<N} M(k) - one Moebius
sieve pass, cheaper than the frozen observable.

ENACTED 2026-08-15. (1) G1_MODEL_SPEC.md gains an additive dated
"AMENDMENT A2" section: clause W' (window) + clause M4'' (spectral
floor theta_min = log(gamma_1/2pi), closing the low-omega positivity
convention), with the candidate-weighing table, the costs, and a
self-serving audit (§A2.6). A1 and the frozen v0 body untouched; A2
explicitly does NOT supersede A1 - under W' the full-line
Cameron-Martin integral still diverges, now because signal sidelobes
outrun the noise floor rather than the reverse. (2) T1 draft -> v3,
everything re-derived and MEASURED, not asserted; the verification
script reproduces every v2 Gaussian number to 5 digits before being
applied to the new window. RESULTS: Prop 4.4 is window-INDEPENDENT
(it never uses the form of M_W), so the amplitude cancellation
S_eps(gamma)^{1/2}/a_gamma = (log(gamma/2pi))^{1/2} survives untouched
and THE HEADLINE CONSTANTS ARE UNCHANGED - c_d = sqrt(6), c = 1.6944
(d=1) / 2.3157 (d=10), X(eps) >= exp(2.3157*eps^{-2/3}), bound 0.04933
at d=10. Factor 24 re-verified a THIRD time, now band-limited AND
coloured by the actual new S_eps at Omega=2*Gamma: [I^-1]_ww = 0.9943
x the local 24-value (was 7.7e-30 under the Gaussian). (3) GAP-3
CLOSED: Lindeberg ratio Lambda(Gamma) = 6pi/(Gamma*(log(Gamma/2pi)
+1/3)) -> 0, measured 0.157 / 0.0248 / 3.5e-3 / 2.4e-4 at Gamma =
50 / 200 / 1e3 / 1e4, against 4.76 (>1!) under the Gaussian. GAP-14
CLOSED: (B1) measured directly as lambda_max(I_N^-1 I_R) = 0.0858 <=
1/K = 0.25 at gamma_d, admissible band out to Omega ~ 400 = 8*Gamma
(was 1.73e+29). GAP-15 CLOSED by clause M4'' plus a floor-sensitivity
sweep (4e-4 relative over a factor 40 in theta_min). GAP-4 REDUCED but
NOT closed: S_eps flatness over the Lemma-1 band falls from a factor
98.2 to 1.23 (gamma_d) / 2.03 (gamma_1), now an explicit
O(K/(omega*T)) two-sided constant; tag drops FRONTIER ->
ARISTOTLE-ABLE. (4) Two findings logged rather than smoothed: (B1) as
an INEQUALITY still fails at the lowest tone gamma_1 (lambda_max
0.587) and is marginal at gamma_2 (0.220) - but the measured deficits
(max 0.257) all sit inside T1's own declared O(K^-1) = 0.25 with
implied constant ~1.03, and the max_j statement is attained at j=d
where the deficit is 0.6%; and A2 CREATES two gaps - GAP-16 (the
VERIFIED explicit-formula import is Gaussian-only and no longer
applies; the order-1 Riesz formula, incl. the NEW pole term
R_-1(N) = 12/N at s = -1 and absolute convergence resting on
J_{-1}(T) = O(T), is stated but NOT re-derived in this repo; largest
open item) and GAP-17 (Berry-Esseen rate behind the now-valid
Lindeberg condition; Lambda(50) = 0.157 is not negligible at the
operating point). (5) Honesty: the gamma_1 empirical tension of §5.2
is NUMERICALLY UNCHANGED and now HARDER to dismiss, since at
Omega=2*Gamma the bound is proved rather than a local surrogate; its
amplitude leg reverses (neighbouring interferers go from 250x weaker
to comparable, 0.454), so N2 is LESS pessimistic and the residual
pessimism is isolated to GAP-9. Falsification gate G-a no longer
fires. Practical payoff: |M_W| at gamma_10 rises 13.8 orders
(5.909e-18 -> 4.034e-4) and the dynamic range over gamma_1..gamma_10
falls from 13 orders to a factor 12.3. Ledger: 17 entries, 4 closed
(GAP-2, GAP-3, GAP-14, GAP-15), 13 open. Verification scripts
uncommitted (GAP-8, now four items).
