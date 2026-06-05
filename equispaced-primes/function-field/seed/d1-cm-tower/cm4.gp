prefactor(K)={my(cl,n,dvec,r2);cl=K.clgp;n=cl[1];dvec=cl[2];r2=0;for(i=1,#dvec,if(dvec[i]%2==0,r2=r2+1));[poldegree(K.pol),abs(K.disc),n,r2,(2^r2-1)/2.0,dvec]};
\\ Layer 2: K = Q(sqrt(a), sqrt(b), i), L = Q(sqrt(a),sqrt(b)) totally real biquadratic
print("Layer 2: K = Q(sqrt(a),sqrt(b),i), degree 8 CM");
print("[deg, |disc|, h_K, r2, prefactor, Cl]");
dlist=[2,3,5,6,7,10,11,13,14,15,17,21];
for(i=1,#dlist,for(j=i+1,#dlist,a=dlist[i];b=dlist[j];if(issquarefree(a*b),pol=polcompositum(polcompositum(x^2-a,x^2-b)[1],x^2+1)[1];if(poldegree(pol)==8,K=bnfinit(pol);print("a=",a,",b=",b,"  ",prefactor(K))))));
