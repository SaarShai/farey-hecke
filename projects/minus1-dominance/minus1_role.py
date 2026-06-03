import math, mpmath as mp
mp.mp.dps=20
# Role of a=-1 in the character sum m(a)=sum_{chi!=1} chi(-1) m_chi.
# Even/odd characters: chi(-1)=+1 (even) or -1 (odd). -1 is special as the unique order-2 element
# acting as complex conjugation; chi(-1) selects parity.
# Demonstrate: for the magnitude m(a), -1 weights characters by their parity sign.
# Also: the quadratic (Legendre) character chi_Leg has chi_Leg(-1)=(-1|q)=(-1)^((q-1)/2).
for q in [7,11,19,23]:
    leg_at_m1 = (-1)**((q-1)//2)
    print(f"q={q}: (-1|q) = chi_Legendre(-1) = {leg_at_m1}   [-1 is QR iff q=1 mod 4]  q mod 4={q%4}")
# All target q are 3 mod 4 (7,11,19,23) => -1 is a NON-residue, consistent with task premise.
print()
print("Check -1 is NR for each target q (q=3 mod4 => -1 is NR):")
for q in [7,11,19,23,8]:
    if q==8:
        # mod 8: -1=7, residues are {1}; 7 is NR
        print(f"q=8: -1=7, QRs mod8={{1}}, so -1=7 is NR: True")
    else:
        qr=set((a*a)%q for a in range(1,q))
        print(f"q={q}: -1={q-1}, is QR? {(q-1)%q in qr}  (False => NR, matches premise)")
