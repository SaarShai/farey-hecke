/* Large-Neighborhood Search (destroy & repair) for A089676.
 * Start from seed (record set + filler to size k). Repeatedly:
 *   - DESTROY: remove D vertices (those most involved in violations, + random).
 *   - REPAIR: re-insert D vertices one at a time, each placed at the value minimizing
 *     added violations vs the current partial set (greedy min-conflicts insertion,
 *     full 2^n scan but only D insertions per round => cheap).
 * Accept if energy improved or by SA criterion; else revert. Reheat on stagnation.
 *
 * Build: cc -O3 -o lns lns.c -lm
 * Run:   ./lns n k rounds rngbase seedfile D [prefix]
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

static long contrib_set(u32 *T,int m,int idx,u32 val){ long e=0;
  for(int a=0;a<m;a++){ if(a==idx)continue; u32 xa=T[a]^val;
    for(int b=a+1;b<m;b++){ if(b==idx)continue; if((xa&(T[b]^val))==0)e++; } }
  for(int j=0;j<m;j++){ if(j==idx)continue; u32 q=T[j]; u32 xi=val^q;
    for(int b=0;b<m;b++){ if(b==idx||b==j)continue; if((xi&(T[b]^q))==0)e++; } }
  return e; }
static long total_energy_set(u32*T,int m){ long e=0; for(int j=0;j<m;j++){u32 q=T[j];
  for(int a=0;a<m;a++){if(a==j)continue;u32 xa=T[a]^q;
   for(int b=a+1;b<m;b++){if(b==j)continue; if((xa&(T[b]^q))==0)e++;}}} return e; }
static int contains_set(u32*T,int m,u32 v){ for(int i=0;i<m;i++) if(T[i]==v) return 1; return 0; }

/* added violations if we APPEND v to current partial set T[0..m-1] (T assumed; v not in T) */
static long added_to_partial(u32*T,int m,u32 v){ long e=0;
  /* v as apex over pairs in T */
  for(int a=0;a<m;a++){ u32 xa=T[a]^v;
    for(int b=a+1;b<m;b++){ if((xa&(T[b]^v))==0)e++; } }
  /* v as leg: apex j in T, other leg b in T */
  for(int j=0;j<m;j++){ u32 q=T[j]; u32 xv=v^q;
    for(int b=0;b<m;b++){ if(b==j)continue; if((xv&(T[b]^q))==0)e++; } }
  return e; }

int main(int argc,char**argv){
  if(argc<6){ fprintf(stderr,"usage: lns n k rounds rngbase seedfile D [prefix]\n"); return 2; }
  n=atoi(argv[1]); k=atoi(argv[2]); long rounds=atol(argv[3]);
  u64 rngbase=strtoull(argv[4],0,10); const char*seedfile=argv[5];
  int D=(argc>6)?atoi(argv[6]):5; const char*prefix=(argc>7)?argv[7]:"lns";
  mask_full=(n>=32)?0xffffffffu:((1u<<n)-1); u32 ncand=mask_full+1;
  u32 *seedm=0; int nseed=0,cap=0;
  { FILE*f=fopen(seedfile,"r"); if(f){ char line[256];
    while(fgets(line,sizeof line,f)){ char*p=line; while(*p==' '||*p=='\t')p++;
      if(*p<'0'||*p>'9')continue; u32 v=(u32)strtoul(p,0,10);
      if(nseed==cap){cap=cap?cap*2:64; seedm=realloc(seedm,cap*sizeof(u32));} seedm[nseed++]=v; } fclose(f);} }
  rs=rngbase*2654435761u+0x9e3779b97f4a7c15ULL; for(int w=0;w<9;w++)xrand();
  S=malloc(k*sizeof(u32));
  int used=0;
  if(nseed>0){ int take=nseed<k?nseed:k; for(int i=0;i<take;i++)S[used++]=seedm[i]; }
  while(used<k){ u32 v=xrand()&mask_full; if(!contains_set(S,used,v))S[used++]=v; }
  long E=total_energy_set(S,k);
  long bestE=E; u32 *bestS=malloc(k*sizeof(u32)); memcpy(bestS,S,k*sizeof(u32));
  u32 *cur=malloc(k*sizeof(u32));
  double T=2.0; long stagn=0;
  for(long r=0; r<rounds && bestE>0; r++){
    memcpy(cur,S,k*sizeof(u32));
    /* DESTROY: pick D indices to remove. Bias toward high-involvement vertices. */
    /* compute involvement */
    long *inv=malloc(k*sizeof(long)); for(int i=0;i<k;i++) inv[i]=contrib_set(S,k,i,S[i]);
    int rem[64]; int nrem=0;
    /* roulette without replacement */
    char taken[256]={0};
    for(int d=0; d<D; d++){
      long tot=0; for(int i=0;i<k;i++) if(!taken[i]) tot+=inv[i]+1;
      if(tot<=0) break; long rr=(long)(xrand()%(u64)tot); int pick=-1;
      for(int i=0;i<k;i++){ if(taken[i])continue; rr-=inv[i]+1; if(rr<0){pick=i;break;} }
      if(pick<0){ for(int i=0;i<k;i++) if(!taken[i]){pick=i;break;} }
      taken[pick]=1; rem[nrem++]=pick;
    }
    free(inv);
    /* build partial set = S minus removed */
    u32 part[256]; int m=0;
    for(int i=0;i<k;i++) if(!taken[i]) part[m++]=S[i];
    /* REPAIR: insert nrem vertices greedily (min added violations), randomized over best ties */
    for(int d=0; d<nrem; d++){
      long mn=1L<<60; u32 bv=0; int ties=0;
      for(u32 v=0; v<ncand; v++){
        if(contains_set(part,m,v)) continue;
        long c=added_to_partial(part,m,v);
        if(c<mn){mn=c;bv=v;ties=1;} else if(c==mn){ties++; if(xrand()%ties==0)bv=v;}
      }
      part[m++]=bv;
    }
    long newE=total_energy_set(part,m); /* m==k */
    long dlt=newE-E;
    if(dlt<=0 || urand()<exp(-(double)dlt/(T>1e-9?T:1e-9))){
      memcpy(S,part,k*sizeof(u32)); E=newE;
      if(E<bestE){ bestE=E; memcpy(bestS,S,k*sizeof(u32)); stagn=0; } else stagn++;
    } else { memcpy(S,cur,k*sizeof(u32)); stagn++; }
    T*=0.9995; if(T<0.05)T=0.05;
    if(stagn>300){ memcpy(S,bestS,k*sizeof(u32)); E=bestE;
      /* perturb: random replace a few */
      for(int q=0;q<6;q++){ int i2=xrand()%k; u32 vv; do{vv=xrand()&mask_full;}while(contains_set(S,k,vv)); S[i2]=vv; }
      E=total_energy_set(S,k); stagn=0; T=1.5; }
    if((r&1023)==0){ printf("  round %ld bestE=%ld E=%ld T=%.3f\n",r,bestE,E,T); fflush(stdout); }
  }
  if(bestE==0){ char fn[512]; snprintf(fn,sizeof fn,"%s_n%d_k%d_rb%llu.txt",prefix,n,k,(unsigned long long)rngbase);
    FILE*f=fopen(fn,"w"); for(int i=0;i<k;i++){for(int b=0;b<n;b++)fputc(((bestS[i]>>b)&1)?'1':'0',f);fputc('\n',f);} fclose(f);
    printf("ZERO ENERGY n=%d k=%d -> %s\n",n,k,fn); fflush(stdout); free(bestS); return 0; }
  char fn[512]; snprintf(fn,sizeof fn,"%s_n%d_k%d_rb%llu_BEST_e%ld.txt",prefix,n,k,(unsigned long long)rngbase,bestE);
  FILE*f=fopen(fn,"w"); for(int i=0;i<k;i++){for(int b=0;b<n;b++)fputc(((bestS[i]>>b)&1)?'1':'0',f);fputc('\n',f);} fclose(f);
  printf("BEST n=%d k=%d energy=%ld -> %s\n",n,k,bestE,fn); fflush(stdout); free(bestS); return 0;
}
