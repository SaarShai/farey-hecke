#!/usr/bin/env python3
"""Aux checks for U1: (C') restricted trace-monotonicity, (A1') identify the
O(1) constant in log E_q(s) = (2s-1) log q + C(s) + o(1)."""
import math, sys, cmath, json
sys.path.insert(0, "/Users/za/Documents/farey-hecke/research_notes/rh_goals_2026-08-14/lane_g/law_probes")
import mpmath as mp
import probe_t2_shape as T2

S_INF = complex(0.25, 7.0673625708673465)


def log_E(q, s, dps=60):
    with mp.workdps(dps):
        S = mp.mpc(s.real, s.imag)
        tot = mp.mpc(0)
        for k in range(q):
            tot += (mp.mpf(q - 2*k - 1)/q) * mp.log(mp.sin(mp.pi*(S+k)/q))
        return complex(tot)


print("=== A1'  log E_q(s) - (2s-1) log q  ->  C(s)? ===")
svals = [S_INF, complex(0.5, 7.0673625708673465), complex(0.0, 7.0673625708673465),
         complex(0.375, 7.2839), complex(0.125, 7.2839), complex(0.3, 3.0), complex(0.25, 1.0)]
res = {}
for s in svals:
    row = []
    for q in (300, 600, 1200, 2400, 4800):
        L = log_E(q, s)
        C = L - (2*complex(s) - 1) * math.log(q)
        row.append((q, C))
    print(f"  s={s}")
    for q, C in row:
        print(f"    q={q:5d}  C = {C.real:+.8f} {C.imag:+.8f}i")
    Cl = row[-1][1]
    # candidate closed forms
    S = mp.mpc(s.real, s.imag)
    cands = {
        "log(Gamma(1-s)/Gamma(s))": complex(mp.log(mp.gamma(1-S)/mp.gamma(S))),
        "2 log(Gamma(1-s)/Gamma(s))": complex(2*mp.log(mp.gamma(1-S)/mp.gamma(S))),
        "log(2 sin(pi s))": complex(mp.log(2*mp.sin(mp.pi*S))),
        "(1-2s) log(2pi)": complex((1-2*S)*mp.log(2*mp.pi)),
        "(2s-1) log(2pi)": complex((2*S-1)*mp.log(2*mp.pi)),
        "log(2pi)*(2s-1)+log(2sin(pi s))": complex((2*S-1)*mp.log(2*mp.pi)+mp.log(2*mp.sin(mp.pi*S))),
    }
    best = sorted(cands.items(), key=lambda kv: abs(kv[1]-Cl))[:3]
    for k, v in best:
        print(f"      cand {k:38s} = {v.real:+.6f}{v.imag:+.6f}i   |diff|={abs(v-Cl):.4g}")
    res[str(s)] = [(q, [C.real, C.imag]) for q, C in row]

print()
print("=== C'  |tr_w(lam_q)| <= |tr_w(2)| for FAITHFUL lifts? ===")


def word_matrix(w, lam):
    Rm = T2.R_of(lam); Rin = (Rm[3], -Rm[1], -Rm[2], Rm[0])
    M = (1.0, 0.0, 0.0, 1.0)
    for syl in w:
        if syl == 0:
            M = T2.mul(M, T2.S)
        else:
            g = Rm if syl > 0 else Rin
            for _ in range(abs(syl)):
                M = T2.mul(M, g)
    return M


theta = T2.enumerate_classes(2.0, 0, 10.0)
words = sorted(theta.keys(), key=lambda w: (len(w), w))
print(f"  theta words in ball r=10: {len(words)}")
qs = [5, 7, 8, 10, 12, 16, 22, 30, 50, 80, 150, 400]
violations = []
tested = 0
mono_fail = []
for w in words:
    amax = max((abs(x) for x in w if x != 0), default=0)
    valid_qs = [q for q in qs if q > 2 * amax]
    if not valid_qs:
        continue
    tr2 = abs(sum(word_matrix(w, 2.0)[i] for i in (0, 3)))
    prev = None
    for q in valid_qs:
        lam = 2.0 * math.cos(math.pi / q)
        trq = abs(sum(word_matrix(w, lam)[i] for i in (0, 3)))
        tested += 1
        if trq > tr2 + 1e-8:
            violations.append((tuple(w), q, trq, tr2))
        if prev is not None and trq < prev[1] - 1e-8:
            mono_fail.append((tuple(w), prev[0], q, prev[1], trq))
        prev = (q, trq)
print(f"  faithful (word,q) pairs tested: {tested}")
print(f"  |tr_w(lam_q)| > |tr_w(2)| violations: {len(violations)}")
for v in violations[:10]:
    print("    ", v)
print(f"  monotonicity-in-q failures: {len(mono_fail)}")
for v in mono_fail[:10]:
    print("    ", v)

print()
print("=== C''  faithful-lift COUNTING:  N_q^faithful(L) vs N_theta(L) ===")
for L in (4.0, 5.0, 6.0, 7.0, 8.0):
    nth = sum(1 for w in words if theta[w] <= L)
    line = f"  L={L}: N_theta={nth:5d}"
    for q in (10, 12, 16, 22, 30, 50):
        cl = T2.enumerate_classes(2.0*math.cos(math.pi/q), q, 10.0)
        nq = sum(1 for v in cl.values() if v <= L)
        line += f"   N_{q}={nq:5d}"
    print(line)
