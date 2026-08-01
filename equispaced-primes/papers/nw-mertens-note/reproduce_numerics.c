/*
 * Local, dependency-free reproducer for the numerical claims retained in
 * equispaced_honest_note.md.  It deliberately computes only three named
 * witnesses, not a range-wide statistic.
 *
 * Build:
 *   cc -O3 -std=c11 -o reproduce_numerics reproduce_numerics.c -lm
 * Run:
 *   ./reproduce_numerics delta 92173
 *   ./reproduce_numerics cross 237733 243799
 *
 * Definitions.
 * M(x) = sum_{n<=x} mu(n).
 * delta W(p) = W(p-1)-W(p), with
 * W(N)=sum_{j=0}^{|F_N|-1}(j/|F_N|-f_j)^2.
 * B_R1(p)=2 sum_{f in F_{p-1}} D_R1(f) delta_p(f),
 * D_R1(f)=rank_R1(f)-|F_{p-1}|f and
 * delta_p(a/b)=(a-(pa mod b))/b.  This is the R1/Lean convention for
 * the later cross-term counterexamples; it is not the broad M<0 statement.
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int *phi, *M;

static void kadd(long double *s, long double *c, long double x) {
  long double y=x-*c, t=*s+y; *c=(t-*s)-y; *s=t;
}

static void init(int n) {
  int *lp=calloc((size_t)n+1,sizeof *lp), *pr=malloc((size_t)n*sizeof *pr);
  phi=malloc(((size_t)n+1)*sizeof *phi); M=calloc((size_t)n+1,sizeof *M);
  if(!lp||!pr||!phi||!M) { fprintf(stderr,"allocation failure\n"); exit(2); }
  int pc=0; signed char *mu=calloc((size_t)n+1,sizeof *mu); mu[1]=1;
  for(int i=0;i<=n;i++) phi[i]=i;
  for(int i=2;i<=n;i++) if(phi[i]==i) for(int j=i;j<=n;j+=i) phi[j]-=phi[j]/i;
  for(int i=2;i<=n;i++) {
    if(!lp[i]) { lp[i]=i; pr[pc++]=i; mu[i]=-1; }
    for(int j=0;j<pc && pr[j]<=lp[i] && (long long)i*pr[j]<=n;j++) {
      int v=i*pr[j]; lp[v]=pr[j];
      if(i%pr[j]==0) { mu[v]=0; break; }
      mu[v]=-mu[i];
    }
  }
  for(int i=1;i<=n;i++) M[i]=M[i-1]+mu[i];
  free(lp); free(pr); free(mu);
}

static long long farey_size(int N) { long long n=1; for(int i=1;i<=N;i++) n+=phi[i]; return n; }

static void deltaW(int p) {
  int N=p-1, a=0,b=1,c=1,d=N; long long n=farey_size(N), np=n+p-1, oldrank=0;
  int k=1; long double so=0,co=0,sn=0,cn=0;
  for(;;) {
    /* Insert every new k/p strictly before the current old Farey fraction. */
    while(k<p && (long long)k*b < (long long)a*p) {
      long double x=(long double)k/p, D=(long double)(oldrank+k-1)-(long double)np*x;
      kadd(&sn,&cn,D*D); k++;
    }
    long double x=(long double)a/b, Do=(long double)oldrank-(long double)n*x;
    long double Dn=(long double)(oldrank+k-1)-(long double)np*x;
    kadd(&so,&co,Do*Do); kadd(&sn,&cn,Dn*Dn);
    if(a==1 && b==1) break;
    long long q=((long long)N+b)/d, na=c, nb=d;
    c=(int)(q*c-a); d=(int)(q*d-b); a=na; b=nb; oldrank++;
  }
  while(k<p) { long double x=(long double)k/p, D=(long double)(oldrank+k-1)-(long double)np*x; kadd(&sn,&cn,D*D); k++; }
  long double wold=so/((long double)n*n), wnew=sn/((long double)np*np), dw=wold-wnew;
  printf("definition=deltaW W(N)=sum_{j=0}^{|F_N|-1}(j/|F_N|-f_j)^2\n");
  printf("p=%d M(p)=%d |F_(p-1)|=%lld |F_p|=%lld\n",p,M[p],n,np);
  printf("W(p-1)=%.24Le\nW(p)=%.24Le\ndeltaW=%.24Le sign=%s\n",wold,wnew,dw,dw>0?"positive":dw<0?"negative":"zero");
}

static void cross(int p) {
  int N=p-1,a=0,b=1,c=1,d=N; long long n=farey_size(N), rank=1;
  long double s=0,cs=0;
  for(;;) {
    long double f=(long double)a/b, D=(long double)rank-(long double)n*f;
    long long r=b==1?0:((long long)p*a%b); long double del=(long double)(a-r)/b;
    kadd(&s,&cs,2*D*del);
    if(a==1&&b==1) break;
    long long q=((long long)N+b)/d,na=c,nb=d;
    c=(int)(q*c-a); d=(int)(q*d-b); a=na;b=nb;rank++;
  }
  printf("definition=B_R1=2sum D_R1(f)delta_p(f), rank_R1(0/1)=1\n");
  printf("p=%d M(p)=%d |F_(p-1)|=%lld\nB_R1=%.24Le sign=%s\n",p,M[p],n,s,s>0?"positive":s<0?"negative":"zero");
}

int main(int argc,char **argv) {
  if(argc<3 || (!strcmp(argv[1],"delta") && argc!=3)) { fprintf(stderr,"usage: %s delta p | %s cross p [p...]\n",argv[0],argv[0]); return 2; }
  int top=0; for(int i=2;i<argc;i++) { int p=atoi(argv[i]); if(p>top) top=p; }
  init(top); for(int i=2;i<argc;i++) { int p=atoi(argv[i]); if(!strcmp(argv[1],"delta")) deltaW(p); else if(!strcmp(argv[1],"cross")) cross(p); else return 2; }
  return 0;
}
