prefactor(K)={my(cl,n,dvec,r2);cl=K.clgp;n=cl[1];dvec=cl[2];r2=0;for(i=1,#dvec,if(dvec[i]%2==0,r2=r2+1));[poldegree(K.pol),abs(K.disc),n,r2,(2^r2-1)/2.0,dvec]};
\\ Layer 3: tri-quadratic L, K = L(i)
print("Layer 3: K = L(i), L tri-quadratic, deg 16");
buildK(dlist)={my(pol);pol=x^2+1;for(i=1,#dlist,pol=polcompositum(pol,x^2-dlist[i])[1]);pol};
trip=[[5,13,17],[5,13,21],[5,13,33],[5,17,21],[5,17,33],[5,21,33],[13,17,21],[13,17,33],[13,21,33],[17,21,33]];
for(i=1,#trip,t=trip[i];pol=buildK(t);if(poldegree(pol)==16,print("L=Q(sqrt",t,",i)  ",prefactor(bnfinit(pol)))));
