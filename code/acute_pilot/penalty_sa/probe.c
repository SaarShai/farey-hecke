/* Exhaustive moves from a seed state (read from file of decimal masks).
 * 1) report base energy.
 * 2) best total energy after a single exhaustive single-vertex change.
 * 3) best after exhaustive PAIR of single-vertex changes restricted to the set
 *    of vertices currently involved in violations (small).
 * Build: cc -O3 -o probe probe.c
 * Run:   ./probe n seedfile
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32;
int n,k; u32 *S; u32 mask_full;
static long energy(){ long e=0; for(int j=0;j<k;j++){u32 q=S[j];
  for(int a=0;a<k;a++){if(a==j)continue;u32 xa=S[a]^q;
   for(int b=a+1;b<k;b++){if(b==j)continue; if((xa&(S[b]^q))==0)e++;}}} return e; }
static int contains(u32 v){ for(int i=0;i<k;i++) if(S[i]==v) return 1; return 0; }
int main(int ac,char**av){ n=atoi(av[1]); mask_full=(1u<<n)-1; u32 full=mask_full+1;
  FILE*f=fopen(av[2],"r"); char l[256]; S=malloc(300*sizeof(u32)); k=0;
  while(fgets(l,256,f)){char*p=l;while(*p==' ')p++; if(*p<'0'||*p>'9')continue; S[k++]=(u32)strtoul(p,0,10);} fclose(f);
  long E0=energy(); printf("base E=%ld (n=%d k=%d)\n",E0,n,k); fflush(stdout);
  /* single-vertex exhaustive */
  long best=E0; int bi=-1; u32 bv=0;
  for(int idx=0;idx<k;idx++){ u32 orig=S[idx];
    for(u32 v=0; v<full; v++){ if(v==orig)continue; if(contains(v))continue;
      S[idx]=v; long e=energy(); if(e<best){best=e;bi=idx;bv=v;} }
    S[idx]=orig; }
  printf("best 1-change: E=%ld (idx=%d val=%u)\n",best,bi,bv); fflush(stdout);
  if(getenv("PROBE_NOPAIR")) return 0;
  /* find vertices involved in violations */
  char inv[300]={0};
  for(int j=0;j<k;j++){u32 q=S[j]; for(int a=0;a<k;a++){if(a==j)continue;u32 xa=S[a]^q;
    for(int b=a+1;b<k;b++){if(b==j)continue; if((xa&(S[b]^q))==0){inv[j]=inv[a]=inv[b]=1;}}}}
  int inv_idx[300],ninv=0; for(int i=0;i<k;i++) if(inv[i]) inv_idx[ninv++]=i;
  printf("vertices in violations: %d\n",ninv);
  /* pair exhaustive over involved vertices: change two involved positions, each over all 2^n */
  long best2=best; int p1=-1,p2=-1; u32 w1=0,w2=0;
  for(int ii=0; ii<ninv; ii++){ int idx=inv_idx[ii]; u32 o1=S[idx];
    /* prune: for each candidate v1, then sweep a second involved position */
    for(u32 v1=0; v1<full; v1++){ if(contains(v1)&&v1!=o1)continue; if(v1==o1)continue;
      S[idx]=v1;
      for(int jj=0; jj<ninv; jj++){ int idx2=inv_idx[jj]; if(idx2==idx)continue; u32 o2=S[idx2];
        for(u32 v2=0; v2<full; v2++){ if(v2==o2)continue; if(contains(v2))continue;
          S[idx2]=v2; long e=energy(); if(e<best2){best2=e;p1=idx;w1=v1;p2=idx2;w2=v2; if(e==0){printf("ZERO via pair!\n");}} }
        S[idx2]=o2;
      }
    }
    S[idx]=o1;
  }
  printf("best 2-change (involved): E=%ld (idx=%d val=%u ; idx=%d val=%u)\n",best2,p1,w1,p2,w2);
  return 0; }
