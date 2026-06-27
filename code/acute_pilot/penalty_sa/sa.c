/* Fixed-cardinality penalty SA for OEIS A089676 acute sets in {0,1}^n.
 *
 * Energy = # unordered (apex j; leg pair {a,b}) with ((S[a]^S[j])&(S[b]^S[j]))==0.
 * Hold k fixed, drive energy->0 by single-vertex replacement (SA).
 * energy==0 => size-k acute set (verify externally with verify.py).
 *
 * Build:  cc -O3 -march=native -o sa sa.c
 * Run:    ./sa <n> <k> <seeds> <iters> <seed0/1> <rngbase> [out_prefix]
 *   seed0/1 = 1 to seed from record set hardcoded? No -> we read seeds from stdin
 *   We read optional seed masks (one decimal mask per line) from a file given as last arg.
 *
 * Actual CLI used by driver:
 *   ./sa n k seeds iters rngbase seedfile out_prefix
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

typedef uint32_t u32;
typedef uint64_t u64;

static u64 rs;
static inline u64 xrand(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static inline double urand(){ return (xrand()>>11)*(1.0/9007199254740992.0); }

int n,k;
u32 mask_full;
u32 *S;        /* current vertices, size k */

/* contribution of position idx if its value is val: number of violating
 * (apex, legpair) incidences touching idx. Matches Python vertex_contrib. */
static long contrib(int idx, u32 val){
    long e=0;
    /* idx as apex */
    for(int a=0;a<k;a++){ if(a==idx) continue;
        u32 xa=S[a]^val;
        for(int b=a+1;b<k;b++){ if(b==idx) continue;
            if((xa&(S[b]^val))==0) e++;
        }
    }
    /* idx as a leg, apex j!=idx, other leg b!=idx,j */
    for(int j=0;j<k;j++){ if(j==idx) continue;
        u32 q=S[j]; u32 xi=val^q;
        for(int b=0;b<k;b++){ if(b==idx||b==j) continue;
            if((xi&(S[b]^q))==0) e++;
        }
    }
    return e;
}

static long total_energy(){
    long e=0;
    for(int j=0;j<k;j++){ u32 q=S[j];
        for(int a=0;a<k;a++){ if(a==j) continue; u32 xa=S[a]^q;
            for(int b=a+1;b<k;b++){ if(b==j) continue;
                if((xa&(S[b]^q))==0) e++;
            }
        }
    }
    return e;
}

static int contains(u32 v){ for(int i=0;i<k;i++) if(S[i]==v) return 1; return 0; }

int main(int argc,char**argv){
    if(argc<6){ fprintf(stderr,"usage: sa n k seeds iters rngbase seedfile [prefix]\n"); return 2; }
    n=atoi(argv[1]); k=atoi(argv[2]);
    int seeds=atoi(argv[3]); long iters=atol(argv[4]);
    u64 rngbase=strtoull(argv[5],0,10);
    const char*seedfile=(argc>6)?argv[6]:0;
    const char*prefix=(argc>7)?argv[7]:"wit";
    mask_full=(n>=32)?0xffffffffu:((1u<<n)-1);

    /* read seed masks */
    u32 *seedm=0; int nseed=0,cap=0;
    if(seedfile){ FILE*f=fopen(seedfile,"r");
        if(f){ char line[256];
            while(fgets(line,sizeof line,f)){ char*p=line; while(*p==' '||*p=='\t')p++;
                if(*p<'0'||*p>'9') continue; u32 v=(u32)strtoul(p,0,10);
                if(nseed==cap){ cap=cap?cap*2:64; seedm=realloc(seedm,cap*sizeof(u32)); }
                seedm[nseed++]=v;
            } fclose(f);
        }
    }

    S=malloc(k*sizeof(u32));
    long best_e=1L<<60; u32 *best=malloc(k*sizeof(u32));

    for(int s=0;s<seeds;s++){
        rs = rngbase*2654435761u + (u64)s*40503u + 0x9e3779b97f4a7c15ULL;
        for(int w=0;w<7;w++) xrand();
        /* init: shuffle seed masks, take first up-to-k, fill random distinct */
        int used=0;
        if(nseed>0){
            /* Fisher-Yates a copy */
            u32 *tmp=malloc(nseed*sizeof(u32)); memcpy(tmp,seedm,nseed*sizeof(u32));
            for(int i=nseed-1;i>0;i--){ int j=xrand()%(i+1); u32 t=tmp[i];tmp[i]=tmp[j];tmp[j]=t; }
            int take = nseed<k?nseed:k;
            for(int i=0;i<take;i++) S[used++]=tmp[i];
            free(tmp);
        }
        while(used<k){ u32 v=xrand()&mask_full; if(!contains(v)){ S[used++]=v; } }

        long E=total_energy();
        /* per-vertex involvement (violations touching i), for biased selection */
        long *inv=malloc(k*sizeof(long));
        for(int i=0;i<k;i++) inv[i]=contrib(i,S[i]);
        long bestE=E; u32 *bestS=malloc(k*sizeof(u32)); memcpy(bestS,S,k*sizeof(u32));
        double Thi=2.5, Tlo=0.05;
        double T=Thi; long stagn=0;
        /* geometric cool over a "cycle"; on stagnation, reheat (reanneal) */
        long cyclen = iters/8; if(cyclen<20000) cyclen=20000;
        double cool=pow(Tlo/Thi, 1.0/(double)cyclen);
        for(long it=0; it<iters && E>0; it++){
            /* biased: with prob 0.8 pick a vertex weighted by involvement */
            int idx;
            if((xrand()&3)!=0){
                long tot=0; for(int i=0;i<k;i++) tot+=inv[i]+1;
                long r=(long)(xrand()% (u64)tot); idx=0;
                while(idx<k-1){ r-=inv[idx]+1; if(r<0) break; idx++; }
            } else idx=xrand()%k;
            u32 nv=xrand()&mask_full;
            if(contains(nv)) continue;
            long oldc=inv[idx];
            long newc=contrib(idx,nv);
            long d=newc-oldc;
            if(d<=0 || urand()<exp(-(double)d/(T>1e-9?T:1e-9))){
                S[idx]=nv; E+=d;
                /* update involvement vector incrementally is complex; recompute touched.
                   Cheap correct approach: recompute all inv (O(k^2)) only occasionally;
                   here just set idx and mark neighbors dirty by full recompute every accept
                   of changed vertex -> too slow. Instead recompute inv for all (O(k^2)). */
                for(int i=0;i<k;i++) inv[i]=contrib(i,S[i]);
                if(E<bestE){ bestE=E; memcpy(bestS,S,k*sizeof(u32)); stagn=0; } else stagn++;
            } else stagn++;
            T*=cool; if(T<Tlo) T=Tlo;
            if(stagn>cyclen){
                /* reheat + restart from best with a perturbation */
                memcpy(S,bestS,k*sizeof(u32));
                for(int r=0;r<2;r++){ int i2=xrand()%k; u32 vv=xrand()&mask_full; if(!contains(vv)) S[i2]=vv; }
                E=total_energy();
                for(int i=0;i<k;i++) inv[i]=contrib(i,S[i]);
                stagn=0; T=Thi;
            }
        }
        E=total_energy();
        if(bestE<E){ memcpy(S,bestS,k*sizeof(u32)); E=bestE; }
        free(inv); free(bestS);
        if(E<best_e){ best_e=E; memcpy(best,S,k*sizeof(u32)); }
        if(E==0){
            char fn[512]; snprintf(fn,sizeof fn,"%s_n%d_k%d_seed%d.txt",prefix,n,k,s);
            FILE*f=fopen(fn,"w");
            for(int i=0;i<k;i++){ for(int b=0;b<n;b++) fputc(((S[i]>>b)&1)?'1':'0',f); fputc('\n',f); }
            fclose(f);
            printf("ZERO ENERGY n=%d k=%d seed=%d -> %s\n",n,k,s,fn);
            fflush(stdout);
            return 0;
        }
        printf("  seed %d: best E=%ld\n",s,E); fflush(stdout);
    }
    char fn[512]; snprintf(fn,sizeof fn,"%s_n%d_k%d_BEST_e%ld.txt",prefix,n,k,best_e);
    FILE*f=fopen(fn,"w");
    for(int i=0;i<k;i++){ for(int b=0;b<n;b++) fputc(((best[i]>>b)&1)?'1':'0',f); fputc('\n',f); }
    fclose(f);
    printf("BEST n=%d k=%d energy=%ld -> %s\n",n,k,best_e,fn); fflush(stdout);
    return 0;
}
