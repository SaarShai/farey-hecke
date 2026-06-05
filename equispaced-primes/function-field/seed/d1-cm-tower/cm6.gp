prefactor(K)={my(cl,n,dvec,r2);cl=K.clgp;n=cl[1];dvec=cl[2];r2=0;for(i=1,#dvec,if(dvec[i]%2==0,r2=r2+1));[poldegree(K.pol),abs(K.disc),n,r2,(2^r2-1)/2.0,dvec]};
buildK(dlist)={my(pol);pol=x^2+1;for(i=1,#dlist,pol=polcompositum(pol,x^2-dlist[i])[1]);pol};
print("Layer 4: K = L(i), L quad-quadratic, deg 32");
quadr=[[5,13,17,21],[5,13,17,33],[5,13,21,33],[5,17,21,33],[13,17,21,33]];
for(i=1,#quadr,t=quadr[i];pol=buildK(t);if(poldegree(pol)==32,print("L=Q(sqrt",t,",i)  ",prefactor(bnfinit(pol,1)))));
