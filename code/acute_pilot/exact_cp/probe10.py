import time
from ortools.sat.python import cp_model
t0=time.time()
n=10; mask=(1<<n)-1
V=list(range(1<<n)); nz=[v for v in V if v]
m=cp_model.CpModel()
x={v:m.NewBoolVar(f"x{v}") for v in V}
m.Add(x[0]==1)
m.Add(sum(x.values())>=17)
cnt=0
L=len(nz)
for i in range(L):
    P=nz[i]; nP=~P&mask
    for j in range(i+1,L):
        R=nz[j]
        if (P&R)==0 or (P&nP... if False else (P & ~R & mask)==0) or (R&~P&mask)==0:
            pass
