#!/usr/bin/env python3
"""Full Dirichlet character orthogonality sweep.

For every (N, checkpoint x, residue a coprime to N) loaded from out2.tsv,
verify Koyama identity (3.1):
  pi(x;N,a) - pi(x;N,1) = (1/phi(N)) * sum_{chi mod N} (chi(a)^{-1} - 1) * S(chi)
where S(chi) = sum_{r in (Z/N)^*} c[r] * chi(r).

Prints worst-case real residual and worst imaginary part across the entire
9-checkpoint x 5-modulus grid (all coprime a). PASS if worst real residual
< THRESH below (1e-2; conservative slack for cumulative cmath roundoff over
phi(N) * |coprimes| terms with summands on the order of 10^11).
"""
import cmath, math, re, pathlib, sys
from math import gcd

OUT = pathlib.Path(__file__).resolve().parent.parent / "out2.tsv"
text = OUT.read_text()

# parse: blocks per N
blocks = {}
cur_N = None
state = None  # 'counts' or 'diffs' or None
for line in text.splitlines():
    m = re.match(r"^## N = (\d+)", line)
    if m:
        cur_N = int(m.group(1))
        blocks[cur_N] = {"counts": {}, "diffs": {}}
        state = None
        continue
    if line.startswith("# diffs"):
        state = "diffs"; continue
    if line.startswith("x\tcount_a"):
        state = "counts"; continue
    if line.startswith("x\tdiff_a"):
        state = "diffs"; continue
    if state and line and line[0].isdigit():
        parts = line.split("\t")
        x = int(parts[0])
        vals = list(map(int, parts[1:]))
        if state == "counts":
            # cols: a=1..N-1
            blocks[cur_N]["counts"][x] = vals
        else:
            # cols: a=2..N-1
            blocks[cur_N]["diffs"][x] = vals

# Primitive roots for the moduli (precomputed)
prim = {7:3, 8:None, 11:2, 19:2, 23:5}  # (Z/8)^* not cyclic — handle separately

def chars_mod_N(N):
    """Return list of (chi: a -> complex) functions, length phi(N)."""
    coprimes = [a for a in range(1,N) if gcd(a,N)==1]
    if N == 8:
        # (Z/8Z)^* = {1,3,5,7} = Z/2 x Z/2.  Generators: 3 (order 2), 5 (order 2).
        # Map: 1=(0,0), 3=(1,0), 5=(0,1), 7=(1,1).
        idx = {1:(0,0), 3:(1,0), 5:(0,1), 7:(1,1)}
        chars = []
        for k1 in range(2):
            for k2 in range(2):
                def make(k1=k1, k2=k2):
                    def chi(a):
                        i,j = idx[a]
                        return ((-1)**(k1*i)) * ((-1)**(k2*j))
                    return chi
                chars.append(make())
        return chars
    g = prim[N]
    phi = len(coprimes)
    ind = {}
    v = 1
    for k in range(phi):
        ind[v] = k
        v = (v*g) % N
    chars = []
    for k in range(phi):
        def make(k=k):
            def chi(a):
                return cmath.exp(2j*math.pi*k*ind[a]/phi)
            return chi
        chars.append(make())
    return chars

def phi_func(N):
    return sum(1 for a in range(1,N) if gcd(a,N)==1)

worst_real = 0.0
worst_imag = 0.0
worst_cell = None
n_cells = 0

print(f"{'N':>3} {'x':>15} {'a':>3} {'direct':>14} {'char_sum_real':>20} {'imag':>12}")
for N in sorted(blocks):
    chars = chars_mod_N(N)
    phi = phi_func(N)
    coprimes = [a for a in range(1,N) if gcd(a,N)==1]
    counts_by_x = blocks[N]["counts"]
    for x in sorted(counts_by_x):
        # counts[a-1] for a in 1..N-1 (includes non-coprime as well; ignore those)
        cvec = counts_by_x[x]
        c = {a: cvec[a-1] for a in range(1, N)}
        S = []
        for chi in chars:
            s = 0+0j
            for r in coprimes:
                s += c[r] * chi(r)
            S.append(s)
        for a in coprimes:
            if a == 1: continue
            chsum = 0+0j
            for k, chi in enumerate(chars):
                # chi(a)^{-1} = conjugate(chi(a)) since |chi|=1
                chsum += (complex(chi(a)).conjugate() - 1) * S[k]
            chsum /= phi
            direct = c[a] - c[1]
            err_r = abs(chsum.real - direct)
            err_i = abs(chsum.imag)
            n_cells += 1
            if err_r > worst_real:
                worst_real = err_r; worst_cell = (N, x, a, direct, chsum)
            if err_i > worst_imag:
                worst_imag = err_i

print(f"\nTotal cells checked: {n_cells}")
print(f"Worst real residual:  {worst_real:.6e}")
print(f"Worst imaginary part: {worst_imag:.6e}")
if worst_cell:
    N,x,a,d,c = worst_cell
    print(f"Worst cell: N={N} x={x} a={a}  direct={d}  char={c.real:.4f} + {c.imag:.4e}j")
print()
THRESH = 1e-2
print("VERDICT:", "PASS" if worst_real < THRESH else "FAIL", f"(threshold {THRESH})")
sys.exit(0 if worst_real < THRESH else 1)
