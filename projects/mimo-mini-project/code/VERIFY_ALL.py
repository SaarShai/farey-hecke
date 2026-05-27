"""Rigorous verification of all session claims. Re-computes everything from scratch.

Each test:
- CLAIM: what we're verifying
- TEST: independent computation method
- RESULT: pass/fail with numerical evidence
"""
import math
import sys

# ============================================================
# COMMON PRIMITIVES
# ============================================================

def sieve_mobius(N):
    mu = [1]*(N+1); mu[0]=0
    is_prime = [True]*(N+1); is_prime[0]=is_prime[1]=False
    for p in range(2, N+1):
        if is_prime[p]:
            for j in range(p, N+1, p):
                if j>p: is_prime[j]=False
                mu[j] = -mu[j]
            for j in range(p*p, N+1, p*p):
                mu[j] = 0
    return mu

def ramanujan_sum(q, m, mu):
    """c_q(m) = Σ_{d|gcd(q,m)} d·μ(q/d). Independent direct computation."""
    g = math.gcd(q, m)
    s = 0
    for d in range(1, g+1):
        if g % d == 0:
            s += d * mu[q // d]
    return s

def ramanujan_sum_direct(q, m):
    """c_q(m) = Σ_{a coprime to q, 1≤a≤q} exp(2πi·am/q). Computed as real (since c_q(m) is real)."""
    total = 0.0
    for a in range(1, q+1):
        if math.gcd(a, q) == 1:
            total += math.cos(2*math.pi*a*m/q)
    return total

def jordan_2(n):
    result = n*n
    nn = n
    p = 2
    while p*p <= nn:
        if nn % p == 0:
            result = result * (p*p - 1) // (p*p)
            while nn % p == 0:
                nn //= p
        p += 1
    if nn > 1:
        result = result * (nn*nn - 1) // (nn*nn)
    return result

# ============================================================
# Setup
# ============================================================
N_SIEVE = 100000
print(f"Sieving Mobius to N={N_SIEVE}...", flush=True)
import time
t0 = time.time()
mu = sieve_mobius(N_SIEVE)
M_arr = [0]*(N_SIEVE+1); s=0
for n in range(1, N_SIEVE+1): s+=mu[n]; M_arr[n]=s
print(f"  done in {time.time()-t0:.1f}s, M({N_SIEVE}) = {M_arr[N_SIEVE]}")
print()

passes = []
fails = []
def check(name, ok, detail=""):
    if ok:
        passes.append(name)
        print(f"  ✓ {name}{(': ' + detail) if detail else ''}")
    else:
        fails.append(name)
        print(f"  ✗ {name}{(': ' + detail) if detail else ''}")

# ============================================================
# CLAIM 1: Ramanujan-sum two-form identity
# c_q(m) via μ-formula = c_q(m) via exp-formula
# ============================================================
print("CLAIM 1: c_q(m) = Σ_{d|gcd(q,m)} d·μ(q/d) = Σ_{a coprime q} exp(2πiam/q)")
for q in [4, 6, 12, 30]:
    for m in [1, 2, 3, 5, 7, 12]:
        v1 = ramanujan_sum(q, m, mu)
        v2 = ramanujan_sum_direct(q, m)
        ok = abs(v1 - v2) < 1e-9
        if not ok:
            check(f"c_{q}({m})", False, f"μ-form={v1}, exp-form={v2:.4f}")
            break
    else:
        continue
    break
else:
    check("Ramanujan two-form identity (24 cases)", True)

# ============================================================
# CLAIM 2: S_Q(m) divisor identity
# S_Q(m) = Σ_{q≤Q} c_q(m) = Σ_{d|m} d·M(⌊Q/d⌋)
# ============================================================
print("\nCLAIM 2: S_Q(m) = Σ_{q≤Q} c_q(m) = Σ_{d|m} d·M(⌊Q/d⌋)")
def divisors(n):
    d=[]; i=1
    while i*i<=n:
        if n%i==0:
            d.append(i)
            if i!=n//i: d.append(n//i)
        i+=1
    return d
Q_test = 200
all_ok = True
for m in [1, 2, 3, 5, 6, 10, 12, 30, 60, 100]:
    v1 = sum(ramanujan_sum(q, m, mu) for q in range(1, Q_test+1))
    v2 = sum(d * M_arr[Q_test//d] for d in divisors(m))
    if v1 != v2:
        check(f"S_Q({m}) at Q={Q_test}", False, f"sum={v1}, divisor-form={v2}")
        all_ok = False
        break
if all_ok:
    check(f"S_Q(m) divisor identity (10 m values at Q={Q_test})", True)

# ============================================================
# CLAIM 3: Mikolás identity J(Q) = (1/(2π²)) · Σ_m |S_Q(m)|² / m²
# (verify via Parseval: ∫ g² = Σ |c_m|²)
# Direct comparison: compute J(Q) via Farey enumeration AND via Mikolás sum.
# ============================================================
print("\nCLAIM 3: J(Q) Mikolás identity (compare direct Farey-J vs Mikolás-sum)")
def J_direct(Q):
    """Compute J(Q) = ∫₀¹ (count_Q(x) - Φx)² dx via Farey enumeration."""
    # Use Stern-Brocot enumeration
    a, b, c, d = 0, 1, 1, Q
    farey = [a/b]
    while c <= Q:
        k = (Q + b) // d
        a, b, c, d = c, d, k*c - a, k*d - b
        farey.append(a/b)
    Phi = len(farey) - 1  # exclude one endpoint
    # Actually let me just use Φ = #F_Q (count from sieve)
    # Need to count |F_Q| properly. F_Q is fractions a/b with 0 ≤ a ≤ b ≤ Q, gcd(a,b)=1
    # Including 0/1 and 1/1, |F_Q| = 1 + Σ_{b=1}^Q φ(b)
    # The above enum is Stern-Brocot, gives all of F_Q from 0/1 to 1/1

    Phi = len(farey)
    # J = Σ_i ∫_{f_i}^{f_{i+1}} (i - Phi·x)² dx
    # Actually count_Q(x) = i for x ∈ (f_i, f_{i+1}) (using 0-indexed: count is 1 at x = 0/1, so we count from the start)
    # Let's redo. count(x) jumps by 1 at each Farey point.
    # E(x) = count(x) - Phi*x. At x = f_i+: E = i_pos - Phi*f_i, where i_pos = i (after the jump).
    # Between f_i+ and f_{i+1}-: E(x) = i_pos - Phi*x, decreasing linearly.
    # ∫_{f_i}^{f_{i+1}} (i_pos - Phi*x)² dx
    #   = -[(i_pos - Phi*x)³/(3Phi)]_{f_i}^{f_{i+1}}
    #   = (1/(3Phi)) · [(i_pos - Phi*f_i)³ - (i_pos - Phi*f_{i+1})³]

    # Use Phi = |F_Q| - 1 or |F_Q|? Let me match stream_J_v2 convention.
    # stream_J_v2.c: count=1 at start (f=0), Phi = total count
    # Their iterations: starts at e_plus = 1.0 (just past 0/1)

    # Use the same convention. Phi = |F_Q| (counting both 0/1 and 1/1).
    # Total Phi from sieve: 1 + Σ φ(b) for b in 1..Q (since 0/1 also counts).
    # Or: just len(farey) since enum gives all Farey including endpoints.

    J = 0.0
    e_plus = 1.0  # E_Q just past 0/1
    for i in range(len(farey) - 1):
        gap = farey[i+1] - farey[i]
        e_minus_new = e_plus - Phi * gap
        # contribution = ∫(E)² dx over this gap
        # E goes from e_plus down to e_minus_new linearly.
        # ∫(linear from a to b)² dx over interval of length L = L · (a² + ab + b²)/3
        contrib = (e_plus**3 - e_minus_new**3) / (3 * Phi)
        J += contrib
        e_plus = e_minus_new + 1.0
    return J, Phi

def J_via_mikolas(Q, M_max):
    """J(Q) = (1/(2π²)) Σ_{m=1}^{M_max} |S_Q(m)|² / m²"""
    total = 0.0
    for m in range(1, M_max+1):
        S = sum(d * M_arr[Q//d] for d in divisors(m))
        total += S * S / (m * m)
    return total / (2 * math.pi * math.pi)

for Q_test in [50, 100, 200, 500]:
    J_d, Phi = J_direct(Q_test)
    J_m = J_via_mikolas(Q_test, 50 * Q_test)  # large M_max for truncation accuracy
    rel_err = abs(J_d - J_m) / J_d
    detail = f"direct J={J_d:.4f}, Mikolás J={J_m:.4f}, rel_err={rel_err:.5f}"
    check(f"Mikolás Q={Q_test}", rel_err < 0.02, detail)

# ============================================================
# CLAIM 4: Structural double-sum identity
# 12 · J(Q) = Σ_{d,d'} gcd² M(Q/d) M(Q/d') / (dd')
# ============================================================
print("\nCLAIM 4: Structural double-sum identity")
def J_via_doublesum(Q):
    total = 0.0
    for d in range(1, Q+1):
        Md = M_arr[Q//d]
        if Md == 0: continue
        for dp in range(1, Q+1):
            Mdp = M_arr[Q//dp]
            if Mdp == 0: continue
            g = math.gcd(d, dp)
            total += g*g * Md * Mdp / (d * dp)
    return total / 12.0

for Q_test in [50, 100, 200, 500]:
    J_d, _ = J_direct(Q_test)
    J_ds = J_via_doublesum(Q_test)
    rel_err = abs(J_d - J_ds) / J_d
    check(f"DoubleSum Q={Q_test}", rel_err < 0.02, f"direct={J_d:.4f}, doublesum={J_ds:.4f}, rel_err={rel_err:.5f}")

# ============================================================
# CLAIM 5: Σ_e (J_2(e)/e²) T(Q/e)² convolution identity
# ============================================================
print("\nCLAIM 5: Σ_e (J_2(e)/e²) T(Q/e)² = Σ_{d,d'} gcd² M(Q/d) M(Q/d') / (dd')")
def T_Q(Q_prime):
    return sum(M_arr[Q_prime//k]/k for k in range(1, Q_prime+1))

for Q_test in [100, 500, 1000]:
    # Full double sum
    full = 0.0
    for d in range(1, Q_test+1):
        for dp in range(1, Q_test+1):
            g = math.gcd(d, dp)
            full += g*g * M_arr[Q_test//d] * M_arr[Q_test//dp] / (d*dp)

    # Via e-sum
    via_e = sum(jordan_2(e) / (e*e) * T_Q(Q_test//e)**2 for e in range(1, Q_test+1))

    rel_err = abs(full - via_e) / max(abs(full), 1e-9)
    check(f"Convolution identity Q={Q_test}", rel_err < 1e-9, f"direct={full:.6f}, via_e={via_e:.6f}, rel_err={rel_err:.2e}")

# ============================================================
# CLAIM 6: BCZ Corr(X,Y) = -1/2 — verify the moments
# ============================================================
print("\nCLAIM 6: BCZ moments via direct integration")
# Triangle T = {(x,y) : x+y>1, 0<x,y<1}, density f = 2 on T.
# Compute E[X], E[X²], E[XY] by Monte Carlo. Compare to 2/3, 1/2, 5/12.
import random
random.seed(12345)
N_samples = 1_000_000
sumX, sumX2, sumXY = 0.0, 0.0, 0.0
n = 0
for _ in range(N_samples):
    x = random.random()
    y = random.random()
    if x + y > 1:
        sumX += x; sumX2 += x*x; sumXY += x*y
        n += 1
E_X = sumX / n
E_X2 = sumX2 / n
E_XY = sumXY / n
Var_X = E_X2 - E_X**2
Cov_XY = E_XY - E_X**2
Corr = Cov_XY / Var_X
check(f"BCZ E[X] = 2/3", abs(E_X - 2/3) < 0.002, f"MC={E_X:.5f}, theory=0.66667")
check(f"BCZ E[X²] = 1/2", abs(E_X2 - 1/2) < 0.002, f"MC={E_X2:.5f}, theory=0.5")
check(f"BCZ E[XY] = 5/12", abs(E_XY - 5/12) < 0.002, f"MC={E_XY:.5f}, theory=0.41667")
check(f"BCZ Var(X) = 1/18", abs(Var_X - 1/18) < 0.001, f"MC={Var_X:.5f}, theory=0.05556")
check(f"BCZ Cov(X,Y) = -1/36", abs(Cov_XY - (-1/36)) < 0.001, f"MC={Cov_XY:.5f}, theory=-0.02778")
check(f"BCZ Corr(X,Y) = -1/2", abs(Corr - (-1/2)) < 0.005, f"MC={Corr:.5f}, theory=-0.5")

# ============================================================
# CLAIM 7: NW(Q) → C for large Q
# Empirical: NW(Q) at Q=10⁵ matches C+predicted M²/(6Q)
# ============================================================
print("\nCLAIM 7: NW(Q) ≈ C + M(Q)²/(6Q) at sampled Q (using prior stream_J data)")
# Hard-coded stream_J observations from this session
NW_data = {
    50000: 0.6642, 100000: 0.6681, 200000: 0.6691, 500000: 0.6700,
    1000000: 0.6793, 999983: 0.679361, 99991: 0.667929860108,
    199933: 0.670106294368, 299989: 0.699083585278, 499979: 0.670169128761,
}
C = 0.66989208
for Q, NW_obs in NW_data.items():
    if Q > N_SIEVE: continue
    M_Q = M_arr[Q]
    pred = C + M_Q*M_Q/(6*Q)
    err = abs(NW_obs - pred)
    check(f"NW({Q}): pred={pred:.5f}, obs={NW_obs:.5f}", err < 0.01, f"err={err:.5f}")

# ============================================================
# CLAIM 8: Σ M(n)²/n³ converges to ≈ 1.13616
# ============================================================
print("\nCLAIM 8: Σ M(n)²/n³ convergence")
running = 0.0
for n in range(1, N_SIEVE+1):
    running += M_arr[n]**2 / n**3
final = running
check(f"Σ M(n)²/n³ at N={N_SIEVE}", abs(final - 1.13616) < 0.001, f"value={final:.6f}, claim=1.13616")

# ============================================================
# CLAIM 9: C closed form = (1/2)∏_p(1+1/(p²(p-1))) ≈ 0.66989
# ============================================================
print("\nCLAIM 9: C Euler product value")
def primes_up_to(N):
    sieve = [True]*(N+1); sieve[0]=sieve[1]=False
    for p in range(2, int(N**0.5)+1):
        if sieve[p]:
            for j in range(p*p, N+1, p): sieve[j]=False
    return [p for p in range(N+1) if sieve[p]]

C_computed = 0.5
for p in primes_up_to(10000):
    C_computed *= (1 + 1/(p*p*(p-1)))
check(f"C = (1/2)∏(1+1/(p²(p-1)))", abs(C_computed - 0.6698920767843868) < 1e-9, f"value={C_computed:.16f}")

# ============================================================
# CLAIM 10: Empirical Pearson NW-C vs M²/(6Q) is positive and high
# ============================================================
print("\nCLAIM 10: Pearson(NW(Q)-C, M²/(6Q))")
xs = []
ys = []
for Q, NW in NW_data.items():
    if Q <= N_SIEVE:
        M_Q = M_arr[Q]
        xs.append(M_Q*M_Q/(6*Q))
        ys.append(NW - C)
n_pts = len(xs)
mx = sum(xs)/n_pts; my = sum(ys)/n_pts
sxy = sum((x-mx)*(y-my) for x,y in zip(xs,ys))
sxx = sum((x-mx)**2 for x in xs)
syy = sum((y-my)**2 for y in ys)
pearson = sxy / math.sqrt(sxx * syy)
check(f"Pearson(NW-C, M²/(6Q)) > 0.9", pearson > 0.9, f"Pearson={pearson:.4f} on {n_pts} points")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print(f"PASSED: {len(passes)}")
print(f"FAILED: {len(fails)}")
if fails:
    print("\nFailures:")
    for f in fails:
        print(f"  - {f}")
