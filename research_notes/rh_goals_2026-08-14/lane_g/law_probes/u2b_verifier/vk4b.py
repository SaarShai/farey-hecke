import math
_z={}
def zeta(s,N=100000):
    if s in _z: return _z[s]
    tot=sum(k**-s for k in range(1,N))
    _z[s]=tot+N**(1-s)/(s-1)+0.5*N**-s+s*N**(-s-1)/12.0
    return _z[s]
def W(q,e_h,e_l):
    s=math.sin(math.pi/q); lam=2*math.cos(math.pi/q)
    h=0.0
    for a in range(2,q-1):
        h+=(math.sin(a*math.pi/q)/s)**-e_h
    return h+2*(lam**-e_l)*zeta(e_l)
def Winf(e_h,e_l):
    return 2*(zeta(e_h)-1)+2*(2**-e_l)*zeta(e_l)
for (eh,el) in [(2.5,3.6),(3.0,4.0)]:
    print(f"--- e_h={eh} e_l={el} sigma={(eh+el)/2}")
    vals=[(q,W(q,eh,el)) for q in range(5,2001)]
    mono=all(vals[i+1][1]<=vals[i][1]+1e-15 for i in range(len(vals)-1))
    mx=max(vals,key=lambda t:t[1])
    print(f"   max q=5..2000 at q={mx[0]} val={mx[1]:.6f}; strictly antitone={mono}")
    for q in (5,6,7,10,100,1000,2000,20000):
        print(f"     q={q:7d} W={W(q,eh,el):.6f}")
    print(f"   W_inf = {Winf(eh,el):.6f}")
