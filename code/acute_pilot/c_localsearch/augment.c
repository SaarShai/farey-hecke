/* Deterministic small-k augmentation test for an acute set.
 * Given an acute set S of size m in {0,1}^N, search EXHAUSTIVELY for a way to reach size m+1:
 *   k=0: is there a single vertex addable to all of S?  (size m -> m+1 directly)
 *   k=1: for each s in S, remove it, then look for TWO vertices addable to S\{s} (size m-1 -> m+1)
 *        -> i.e. find 2 new vertices x,y with S\{s} ∪ {x,y} acute.
 *   k=2: remove each PAIR, find THREE addable vertices.  (m-2 -> m+1)
 * For the "find j addable vertices" subproblem we do a greedy+backtracking complete search over the
 * candidate set (all vertices addable to the reduced base), bounded. This is COMPLETE for k=0 (cheap),
 * and a strong (not fully exhaustive at large j) search for k>=1.
 * If it ever assembles size m+1, we print the witness (record BEATEN). Else: record is k-stable.
 * Build: cc -O3 -march=native -o augment augment.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef uint32_t u32;
#define MAXSET 512
static int N; static u32 UNIV;

static inline int can_add(const u32* arr,int m,u32 x){
    for(int a=0;a<m;a++){ u32 xa=arr[a]^x; for(int b=a+1;b<m;b++) if((xa&(arr[b]^x))==0) return 0; }
    for(int q=0;q<m;q++){ u32 xq=x^arr[q]; for(int a=0;a<m;a++){ if(a==q)continue; if((xq&(arr[a]^arr[q]))==0) return 0; } }
    return 1;
}
static int is_acute(const u32* arr,int m){
    for(int j=0;j<m;j++){ u32 Q=arr[j]; for(int a=0;a<m;a++){ if(a==j)continue; u32 xa=arr[a]^Q;
        for(int b=a+1;b<m;b++){ if(b==j)continue; if((xa&(arr[b]^Q))==0) return 0; }}}
    return 1;
}
/* candidate list = all vertices addable to base[0..m-1] */
static int build_cands(const u32* base,int m,u32* cand){
    int nc=0; for(u32 x=0;x<=UNIV;x++){ if(can_add(base,m,x)) cand[nc++]=x; if(x==UNIV)break; } return nc;
}
/* try to add `need` vertices from cand[ci..nc) onto base (size m). complete backtracking. */
static long nodes;
static int extend(u32* base,int m,const u32* cand,int nc,int ci,int need,u32* out){
    if(need==0) return 1;
    for(int i=ci;i<nc;i++){
        nodes++;
        if(!can_add(base,m,cand[i])) continue;   /* still addable given earlier picks */
        base[m]=cand[i]; out[0]=cand[i];
        if(extend(base,m+1,cand,nc,i+1,need-1,out+1)) return 1;
    }
    return 0;
}

static int read_set(const char* path,u32* out){
    FILE* f=fopen(path,"r"); if(!f)return 0; char line[512]; int nv=0,M=-1;
    while(fgets(line,sizeof line,f)){ int bit=0; u32 v=0,any=0;
        for(char*c=line;*c;c++) if(*c=='0'||*c=='1'){ if(*c=='1'&&bit<N)v|=(1u<<bit); bit++; any=1; }
        if(any){ if(M<0)M=bit; out[nv++]=v; } }
    fclose(f); return nv;
}

int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: %s SETFILE N [maxk]\n",argv[0]); return 2; }
    N=atoi(argv[2]); UNIV=(N>=32)?0xFFFFFFFFu:((1u<<N)-1);
    int maxk=(argc>3)?atoi(argv[3]):1;
    u32 S[MAXSET]; int m=read_set(argv[1],S);
    if(!is_acute(S,m)){ fprintf(stderr,"input not acute!\n"); return 1; }
    fprintf(stderr,"loaded acute set size %d, N=%d, trying to reach %d (maxk=%d)\n",m,N,m+1,maxk);
    u32 base[MAXSET], out[8];

    /* k=0: single addable vertex */
    { memcpy(base,S,m*sizeof(u32)); u32 cand[1<<16]; int nc=build_cands(base,m,cand);
      fprintf(stderr,"k=0: %d vertices addable to full set\n",nc);
      if(nc>0){ printf("# BEATEN k=0\n"); for(int i=0;i<m;i++){for(int b=0;b<N;b++)printf("%d%s",(S[i]>>b)&1,b+1<N?" ":"");printf("\n");}
                for(int b=0;b<N;b++)printf("%d%s",(cand[0]>>b)&1,b+1<N?" ":"");printf("\n"); return 0; } }

    for(int k=1;k<=maxk;k++){
        fprintf(stderr,"k=%d: remove %d, seek %d additions...\n",k,k,k+1);
        /* iterate over all combinations of k removals */
        int idx[8]; for(int i=0;i<k;i++)idx[i]=i;
        long combos=0;
        while(1){
            combos++;
            /* base = S minus the k chosen */
            int bm=0; u32 removed[8]; for(int i=0;i<k;i++)removed[i]=S[idx[i]];
            for(int i=0;i<m;i++){ int rm=0; for(int j=0;j<k;j++) if(i==idx[j]){rm=1;break;} if(!rm) base[bm++]=S[i]; }
            u32 cand[1<<16]; int nc=build_cands(base,bm,cand);
            if(nc>=k+1){ nodes=0;
                if(extend(base,bm,cand,nc,0,k+1,out)){
                    fprintf(stderr,"  BEATEN at k=%d (combo %ld)\n",k,combos);
                    printf("# BEATEN k=%d\n",k);
                    for(int i=0;i<bm;i++){for(int b=0;b<N;b++)printf("%d%s",(base[i]>>b)&1,b+1<N?" ":"");printf("\n");}
                    for(int i=0;i<k+1;i++){for(int b=0;b<N;b++)printf("%d%s",(out[i]>>b)&1,b+1<N?" ":"");printf("\n");}
                    return 0;
                }
            }
            /* next combination */
            int p=k-1; while(p>=0 && idx[p]==m-k+p) p--;
            if(p<0) break; idx[p]++; for(int q=p+1;q<k;q++) idx[q]=idx[q-1]+1;
        }
        fprintf(stderr,"k=%d: exhausted %ld combos, no augmentation -> record is %d-stable\n",k,combos,k);
    }
    fprintf(stderr,"NO augmentation up to k=%d. Record not locally beatable this way.\n",maxk);
    return 3;
}
