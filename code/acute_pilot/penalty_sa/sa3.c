/* WalkSAT-style focused repair for A089676 acute sets.
 * Maintain size-k array. Find a violated (apex,legpair). Pick one of its 3 vertices.
 * Re-place it with the candidate value (full 2^n scan) that MINIMIZES total contrib of
 * that position (min-conflicts), with prob p take a random improving move (noise).
 * Periodic SA-style worsening acceptance + reheat. Seeded from record set.
 *
 * Build: cc -O3 -o sa3 sa3.c -lm
 * Run:   ./sa3 n k seeds iters rngbase seedfile [prefix]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
typedef uint32_t u32; typedef uint64_t u64;
static u64 rs;
static inline u64 xrand(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static inline double urand(){ return (xrand()>>11)*(1.0/9007199254740992.0); }
int n,k; u32 mask_full; u32 *S;

static long contrib(int idx,u32 val){ long e=0;
  for(int a=0;a<k;a++){ if(a==idx)continue; u32 xa=S[a]^val;
    for(int b=a+1;b<k;b++){ if(b==idx)continue; if((xa&(S[b]^val))==0)e++; } }
  for(int j=0;j<k;j++){ if(j==idx)continue; u32 q=S[j]; u32 xi=val^q;
    for(int b=0;b<k;b++){ if(b==idx||b==j)continue; if((xi&(S[b]^q))==0)e++; } }
  return e; }
static long total_energy(){ long e=0; for(int j=0;j<k;j++){u32 q=S[j];
  for(int a=0;a<k;a++){if(a==j)continue;u32 xa=S[a]^q;
   for(int b=a+1;b<k;b++){if(b==j)continue; if((xa&(S[b]^q))==0)e++;}}} return e; }
static int contains(u32 v){ for(int i=0;i<k;i++) if(S[i]==v) return 1; return 0; }

/* find a random violated incidence; return its 3 positions in t[]. returns 1 if found. */
static int find_violation(int t[3]){
  /* random scan order over apex */
  int j0=xrand()%k;
  for(int jj=0;jj<k;jj++){ int j=(j0+jj)%k; u32 q=S[j];
    int a0=xrand()%k;
    for(int aa=0;aa<k;aa++){ int a=(a0+aa)%k; if(a==j)continue; u32 xa=S[a]^q;
      for(int b=a+1;b<k;b++){ if(b==j)continue;
        if((xa&(S[b]^q))==0){ t[0]=j;t[1]=a;t[2]=b; return 1; } } } }
  return 0;
}

int main(int argc,char**argv){
  if(argc<6){ fprintf(stderr,"usage: sa3 n k seeds iters rngbase seedfile [prefix]\n"); return 2; }
  n=atoi(argv[1]); k=atoi(argv[2]); int seeds=atoi(argv[3]); long iters=atol(argv[4]);
  u64 rngbase=strtoull(argv[5],0,10);
  const char*seedfile=(argc>6)?argv[6]:0; const char*prefix=(argc>7)?argv[7]:"w3";
  mask_full=(n>=32)?0xffffffffu:((1u<<n)-1);
  u32 *seedm=0; int nseed=0,cap=0;
  if(seedfile){ FILE*f=fopen(seedfile,"r"); if(f){ char line[256];
    while(fgets(line,sizeof line,f)){ char*p=line; while(*p==' '||*p=='\t')p++;
      if(*p<'0'||*p>'9')continue; u32 v=(u32)strtoul(p,0,10);
      if(nseed==cap){cap=cap?cap*2:64; seedm=realloc(seedm,cap*sizeof(u32));} seedm[nseed++]=v; } fclose(f);} }
  S=malloc(k*sizeof(u32));
  long best_e=1L<<60; u32 *best=malloc(k*sizeof(u32));
  u32 ncand=mask_full+1; (void)ncand;
  double noise=0.20;
  #define POOL 400

  for(int s=0;s<seeds;s++){
    rs=rngbase*2654435761u+(u64)s*40503u+0x9e3779b97f4a7c15ULL; for(int w=0;w<7;w++)xrand();
    int used=0;
    if(nseed>0){ u32*tmp=malloc(nseed*sizeof(u32)); memcpy(tmp,seedm,nseed*sizeof(u32));
      for(int i=nseed-1;i>0;i--){int j=xrand()%(i+1);u32 t=tmp[i];tmp[i]=tmp[j];tmp[j]=t;}
      int take=nseed<k?nseed:k; for(int i=0;i<take;i++)S[used++]=tmp[i]; free(tmp); }
    while(used<k){ u32 v=xrand()&mask_full; if(!contains(v))S[used++]=v; }
    long E=total_energy(); long bestE=E; u32*bestS=malloc(k*sizeof(u32)); memcpy(bestS,S,k*sizeof(u32));
    long stagn=0; long sincebest=0;
    for(long it=0; it<iters && E>0; it++){
      int t[3]; if(!find_violation(t)){ E=0; break; }
      int idx = t[xrand()%3];
      u32 cur=S[idx];
      if(urand()<noise){
        /* random walk: random distinct value */
        u32 v; do{ v=xrand()&mask_full; }while(contains(v));
        long d=contrib(idx,v)-contrib(idx,cur);
        S[idx]=v; E+=d;
      } else {
        /* min-conflicts over a BOUNDED candidate pool (fast): single-bit neighbors of
           cur + a sample of random values. Pick the best (min contrib for idx). */
        long mn=1L<<60; u32 bv=cur; int ties=0;
        #define TRYCAND(v) do{ u32 _v=(v); int _dup=0; for(int _i=0;_i<k;_i++){ if(_i!=idx&&S[_i]==_v){_dup=1;break;} } if(!_dup){ S[idx]=cur; long _c=contrib(idx,_v); if(_c<mn){mn=_c;bv=_v;ties=1;} else if(_c==mn){ties++; if(xrand()%ties==0)bv=_v;} } }while(0)
        TRYCAND(cur);
        for(int b=0;b<n;b++) TRYCAND(cur ^ (1u<<b));          /* Hamming-1 neighbors */
        for(int r=0;r<POOL;r++) TRYCAND(xrand()&mask_full);    /* random sample */
        #undef TRYCAND
        S[idx]=cur;
        long d=contrib(idx,bv)-contrib(idx,cur);
        S[idx]=bv; E+=d;
      }
      if(E<bestE){ bestE=E; memcpy(bestS,S,k*sizeof(u32)); stagn=0; sincebest=0; }
      else { stagn++; sincebest++; }
      if(sincebest>40000){
        /* restart from best + perturb a few */
        memcpy(S,bestS,k*sizeof(u32));
        for(int r=0;r<4;r++){int i2=xrand()%k;u32 vv; do{vv=xrand()&mask_full;}while(contains(vv)); S[i2]=vv;}
        E=total_energy(); sincebest=0;
      }
    }
    E=total_energy(); if(bestE<E){ memcpy(S,bestS,k*sizeof(u32)); E=bestE; } free(bestS);
    if(E<best_e){ best_e=E; memcpy(best,S,k*sizeof(u32)); }
    if(E==0){ char fn[512]; snprintf(fn,sizeof fn,"%s_n%d_k%d_seed%d.txt",prefix,n,k,s);
      FILE*f=fopen(fn,"w"); for(int i=0;i<k;i++){for(int b=0;b<n;b++)fputc(((S[i]>>b)&1)?'1':'0',f);fputc('\n',f);} fclose(f);
      printf("ZERO ENERGY n=%d k=%d seed=%d -> %s\n",n,k,s,fn); fflush(stdout); return 0; }
    printf("  seed %d: best E=%ld\n",s,E); fflush(stdout);
  }
  char fn[512]; snprintf(fn,sizeof fn,"%s_n%d_k%d_BEST_e%ld.txt",prefix,n,k,best_e);
  FILE*f=fopen(fn,"w"); for(int i=0;i<k;i++){for(int b=0;b<n;b++)fputc(((best[i]>>b)&1)?'1':'0',f);fputc('\n',f);} fclose(f);
  printf("BEST n=%d k=%d energy=%ld -> %s\n",n,k,best_e,fn); fflush(stdout); return 0;
}
