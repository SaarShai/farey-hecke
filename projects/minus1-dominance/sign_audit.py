"""
AUDIT the density-vs-variance direction. FM Thm 1.1: delta = 1/2 + rho/sqrt(2 pi V) + ...
=> delta DECREASES toward 1/2 as V INCREASES (rho>0 fixed). Larger V => SMALLER delta.
My density_implication.py claimed the OPPOSITE. Resolve by recomputing with the
CORRECT mean sign that gives delta>1/2 (NR leads).

The NR-vs-1 race has delta>1/2 (NR ahead). In the X-difference convention that
reproduces this, the MEAN of D=X_a - X_1 must be POSITIVE (so most mass is >0).
With mean m>0 fixed and variance V: delta=P(D>0)=P(D-m > -m)= P(standardized > -m/sqrt V).
As V grows, m/sqrt V shrinks => delta -> 1/2 from above => DECREASES. THIS matches FM.

My earlier density_implication.py used m=-2 (NEGATIVE) and got delta<1/2 increasing
toward 1/2 -- same phenomenon (|delta-1/2| shrinks as V grows) but I misread the
direction for the NR-leads case. CORRECT statement: |delta - 1/2| DECREASES as V
increases. Since NR leads (delta>1/2), larger V => delta SMALLER (closer to 1/2).
"""
import mpmath as mp
mp.mp.dps=25
def gp(m,amps,XI=100):
    def phi(xi):
        v=mp.e**(1j*xi*m)
        for A in amps: v*=mp.besselj(0,A*xi)
        return v
    return float(0.5+mp.quad(lambda xi: mp.im(phi(xi))/xi,[0,XI])/mp.pi)

print("CORRECT convention: NR leads => mean m=+2 (>0), delta>1/2. Vary V:")
print(f"{'V':>6} {'delta=P(D>0)':>14}  {'|delta-1/2|':>12}")
for V in [4,8,12,20,40,80]:
    K=120; A=mp.sqrt(2*V/K)
    d=gp(2.0,[A]*K)
    print(f"{V:6.1f} {d:14.5f}  {abs(d-0.5):12.5f}")
print("=> |delta-1/2| DECREASES as V grows. NR with LARGER V is LESS biased = LOSES.")
print("=> -1 has the LARGEST V (extra log2 term) => -1 is the LEAST-leading NR.")
print()
print("This REVERSES my earlier claim. FM Thm 1.10 is correct: -1 does NOT dominate;")
print("it is the unique LEAST-biased non-residue vs 1.")
