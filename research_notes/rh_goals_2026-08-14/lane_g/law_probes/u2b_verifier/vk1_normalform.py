# INDEPENDENT check of Lemma U2b-1 by exact integer EVALUATION at many lambda values.
# A polynomial identity in Z[lam] of degree <= D is proved by agreement at D+1 distinct integers.
from fractions import Fraction

def mat_mul(A,B):
    return [[A[0][0]*B[0][0]+A[0][1]*B[1][0], A[0][0]*B[0][1]+A[0][1]*B[1][1]],
            [A[1][0]*B[0][0]+A[1][1]*B[1][0], A[1][0]*B[0][1]+A[1][1]*B[1][1]]]

def u_seq(n, lam):
    u=[0,1]
    for j in range(1,n+2): u.append(lam*u[-1]-u[-2])
    return u   # u[j]

AMAX=40
LAMS=list(range(-60,61))   # 121 distinct integer lambdas, > deg+1 for a<=40
bad=[]
for a in range(1,AMAX+1):
    for lam in LAMS:
        S=[[0,-1],[1,0]]
        R=[[0,-1],[1,lam]]
        # R^{-1}: det R = 0*lam-(-1*1)=1 -> inverse = [[lam,1],[-1,0]]
        Ri=[[lam,1],[-1,0]]
        assert mat_mul(R,Ri)==[[1,0],[0,1]]
        P=[[1,0],[0,1]]; Q=[[1,0],[0,1]]
        for _ in range(a): P=mat_mul(P,R); Q=mat_mul(Q,Ri)
        SRa=mat_mul(S,P); SRma=mat_mul(S,Q)
        u=u_seq(a+2,lam)
        M=[[u[a],u[a+1]],[u[a-1],u[a]]]
        negM=[[-M[0][0],-M[0][1]],[-M[1][0],-M[1][1]]]
        MT=[[M[0][0],M[1][0]],[M[0][1],M[1][1]]]
        det=M[0][0]*M[1][1]-M[0][1]*M[1][0]
        if SRa!=negM: bad.append(('SR^a',a,lam))
        if SRma!=MT: bad.append(('SR^-a',a,lam))
        if det!=1: bad.append(('det',a,lam,det))
print("a range 1..%d, %d integer lambdas, violations: %d"%(AMAX,len(LAMS),len(bad)))
print(bad[:5])

# also: negative-index convention u_{-j} = -u_j consistency for S R^{-a} = M_a^T
# and S*R = -T
for lam in (0,1,2,3,-5):
    S=[[0,-1],[1,0]]; R=[[0,-1],[1,lam]]
    print("lam=",lam," S*R =",mat_mul(S,R), " -T=",[[-1,-lam],[0,-1]])
    break
