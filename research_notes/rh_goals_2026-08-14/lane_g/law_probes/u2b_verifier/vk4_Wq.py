import math
def zeta(s,N=400000):
    tot=sum(k**-s for k in range(1,N))
    return tot+N**(1-s)/(s-1)+0.5*N**-s+s*N**(-s-1)/12.0
def W(q,e_h,e_l):
    s=math.sin(math.pi/q); lam=2*math.cos(math.pi/q)
    h=sum((math.sin(a*math.pi/q)/s)**-e_h for a in range(2,q-1))
    return h+2*(lam**-e_l)*zeta(e_l)
def Winf(e_h,e_l):
    # u_a -> a for fixed a; both ends symmetric -> 2*sum_{a>=2} a^{-e_h}
    return 2*(zeta(e_h)-1) + 2*(2**-e_l)*zeta(e_l)
for (eh,el) in [(2.5,3.6),(3.0,4.0),(3.0,3.5),(4.0,4.0)]:
    print(f"--- e_h={eh} e_l={el} sigma={(eh+el)/2}")
    vals=[(q,W(q,eh,el)) for q in range(5,3001)]
    mono=all(vals[i+1][1]<=vals[i][1]+1e-15 for i in range(len(vals)-1))
    mx=max(vals,key=lambda t:t[1])
    print(f"   W_5={W(5,eh,el):.6f}  max over q=5..3000 at q={mx[0]} val={mx[1]:.6f}  strictly antitone(5..3000)={mono}")
    for q in (5,6,10,100,1000,3000,10000,100000,1000000):
        print(f"     q={q:8d} W={W(q,eh,el):.6f}")
    print(f"   W_infinity(analytic) = {Winf(eh,el):.6f}")
