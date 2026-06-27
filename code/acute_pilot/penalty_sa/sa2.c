/* Stronger penalty search: min-conflicts full-candidate scan + SA acceptance.
 * For a chosen position idx we can scan ALL 2^n candidate values (cheap for n<=15)
 * and compute contrib(idx, cand) for each, picking the best (min-conflicts) or a
 * Boltzmann-sampled improving candidate. This is a far stronger move than random.
 *
 * Build: cc -O3 -o sa2 sa2.c -lm
 * Run:   ./sa2 n k seeds iters rngbase seedfile [prefix]
 *   iters = number of (pick-position, scan-candidates, move) steps.
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

int main(int argc,char**argv){
  if(argc<6){ fprintf(stderr,"usage: sa2 n k seeds iters rngbase seedfile [prefix]\n"); return 2; }
  n=atoi(argv[1]); k=atoi(argv[2]); int seeds=atoi(argv[3]); long iters=atol(argv[4]);
  u64 rngbase=strtoull(argv[5],0,10);
  const char*seedfile=(argc>6)?argv[6]:0; const char*prefix=(argc>7)?argv[7]:"w2";
  mask_full=(n>=32)?0xffffffffu:((1u<<n)-1);
  u32 *seedm=0; int nseed=0,cap=0;
  if(seedfile){ FILE*f=fopen(seedfile,"r"); if(f){ char line[256];
    while(fgets(line,sizeof line,f)){ char*p=line; while(*p==' '||*p=='\t')p++;
      if(*p<'0'||*p>'9')continue; u32 v=(u32)strtoul(p,0,10);
      if(nseed==cap){cap=cap?cap*2:64; seedm=realloc(seedm,cap*sizeof(u32));} seedm[nseed++]=v; } fclose(f);} }
  S=malloc(k*sizeof(u32));
  long best_e=1L<<60; u32 *best=malloc(k*sizeof(u32));
  u32 ncand=mask_full+1;            /* number of candidate values 2^n */
  long *cc=malloc(ncand*sizeof(long)); /* contrib per candidate buffer */

  for(int s=0;s<seeds;s++){
    rs=rngbase*2654435761u+(u64)s*40503u+0x9e3779b97f4a7c15ULL; for(int w=0;w<7;w++)xrand();
    int used=0;
    if(nseed>0){ u32*tmp=malloc(nseed*sizeof(u32)); memcpy(tmp,seedm,nseed*sizeof(u32));
      for(int i=nseed-1;i>0;i--){int j=xrand()%(i+1);u32 t=tmp[i];tmp[i]=tmp[j];tmp[j]=t;}
      int take=nseed<k?nseed:k; for(int i=0;i<take;i++)S[used++]=tmp[i]; free(tmp); }
    while(used<k){ u32 v=xrand()&mask_full; if(!contains(v))S[used++]=v; }
    long E=total_energy();
    long bestE=E; u32*bestS=malloc(k*sizeof(u32)); memcpy(bestS,S,k*sizeof(u32));
    double Thi=2.5,Tlo=0.02; long cyclen=iters/6; if(cyclen<2000)cyclen=2000;
    double cool=pow(Tlo/Thi,1.0/(double)cyclen); double T=Thi; long stagn=0;
    for(long it=0; it<iters && E>0; it++){
      /* choose a position to re-place: prefer one with high current contrib */
      int idx;
      if((xrand()&3)!=0){
        /* sample by contrib weight */
        long tot=0; static long *iv=0; static int ivk=0;
        if(ivk!=k){ if(iv)free(iv); iv=malloc(k*sizeof(long)); ivk=k; }
        for(int i=0;i<k;i++){ iv[i]=contrib(i,S[i]); tot+=iv[i]+1; }
        long r=(long)(xrand()%(u64)tot); idx=0; while(idx<k-1){ r-=iv[idx]+1; if(r<0)break; idx++; }
      } else idx=xrand()%k;
      u32 cur=S[idx];
      /* scan all candidates: contrib if S[idx]=cand. exclude values already in S. */
      long mn=1L<<60;
      for(u32 v=0; v<ncand; v++){
        S[idx]=v; /* temporarily */
        /* skip duplicates (other positions) */
        int dup=0; for(int i=0;i<k;i++){ if(i!=idx && S[i]==v){dup=1;break;} }
        if(dup){ cc[v]=1L<<60; continue; }
        long c=contrib(idx,v); cc[v]=c; if(c<mn)mn=c;
      }
      S[idx]=cur;
      /* Boltzmann-sample a candidate: weight exp(-(c-mn)/T). Build cumulative over a
         shortlist of the best to bound work: collect all with c<=mn+ window. */
      long curc=contrib(idx,cur);
      /* gather candidates with c <= mn + 6 (window) */
      double Z=0; long pick=-1; double rsel=0;
      /* reservoir-style weighted pick in one pass */
      for(u32 v=0; v<ncand; v++){
        long c=cc[v]; if(c>=(1L<<60)) continue;
        if(c>mn+8) continue;
        double w=exp(-(double)(c-mn)/(T>1e-9?T:1e-9));
        Z+=w; if(urand()<w/Z){ pick=v; rsel=c; }
      }
      if(pick<0) continue;
      long d=(long)rsel-curc;
      /* SA acceptance vs current (min-conflicts already biased to improving) */
      if(d<=0 || urand()<exp(-(double)d/(T>1e-9?T:1e-9))){
        S[idx]=(u32)pick; E+=d;
        if(E<bestE){ bestE=E; memcpy(bestS,S,k*sizeof(u32)); stagn=0; } else stagn++;
      } else stagn++;
      T*=cool; if(T<Tlo)T=Tlo;
      if(stagn>cyclen){ memcpy(S,bestS,k*sizeof(u32));
        for(int r=0;r<3;r++){int i2=xrand()%k;u32 vv=xrand()&mask_full; if(!contains(vv))S[i2]=vv;}
        E=total_energy(); stagn=0; T=Thi; }
    }
    E=total_energy(); if(bestE<E){ memcpy(S,bestS,k*sizeof(u32)); E=bestE; }
    free(bestS);
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
