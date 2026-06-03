import math
import mpmath as mp
mp.mp.dps=25

def t_of_q(q):
    # number of distinct primes dividing q, with AK's correction
    f=set()
    qq=q
    d=2
    while d*d<=qq:
        while qq%d==0:
            f.add(d); qq//=d
        d+=1
    if qq>1: f.add(qq)
    tq=len(f)
    # AK: t = t(q)-1 if 2||q ; t(q) if 4||q or 2∤q ; t(q)+1 if 8|q
    if q%2==1:
        return tq
    v2=0; r=q
    while r%2==0: r//=2; v2+=1
    if v2==1: return tq-1
    if v2==2: return tq      # 4||q
    return tq+1              # 8|q (v2>=3)

for q in [4,7,8,11,19,23]:
    t=t_of_q(q)
    phi=sum(1 for a in range(1,q) if math.gcd(a,q)==1)
    lead=(2**t-1)/phi
    print(f"q={q}: t={t}, 2^t-1={2**t-1}, phi={phi}, leading NR coeff (vs residue) = (2^t-1)/phi = {lead:.6f}")
    print(f"   AK eq(3.4): pi_{{1/2}}(x;q,NR) - pi_{{1/2}}(x;q,QR) ~ {lead:.6f} * loglog x   (SAME for every NR b, incl b=-1)")
    print(f"   AK Cor 3.3: pi_{{1/2}}(x;q,b) - pi_{{1/2}}(x;q,b') = c + o(1) for ANY two NR b,b'  => NO leading difference, -1 does NOT lead at this order")
