prefactor(K)={my(cl,n,dvec,r2);cl=K.clgp;n=cl[1];dvec=cl[2];r2=0;for(i=1,#dvec,if(dvec[i]%2==0,r2=r2+1));[poldegree(K.pol),abs(K.disc),n,r2,(2^r2-1)/2.0,dvec]};
print("Layer 0: K = Q(i)");
K=bnfinit(x^2+1);print(prefactor(K));
print("Layer 1: K = Q(sqrt(d),i)");
print("[deg, |disc|, h_K, r2, prefactor, Cl]");
for(d=2,30,if(issquarefree(d)&&d>1,pol=polcompositum(x^2-d,x^2+1)[1];K=bnfinit(pol);print("d=",d,"  ",prefactor(K))));
