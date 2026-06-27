/* OEIS A089676 — fixed-size simulated annealing.
 * State: a multiset-free array S[0..M-1] of M distinct vectors in {0,1}^N (M = TARGET).
 * Energy E(S) = number of (apex j, unordered leg pair {a,b}) with a right angle ((S[a]^S[j])&(S[b]^S[j])==0).
 * E==0  <=>  S is an acute set of size M  =>  record beaten if M > current record.
 * Move: pick slot s, propose new vector y (random or from neighborhood), accept by Metropolis on dE.
 * Delta is computed by counting only triples that involve slot s (apex=s, or s is a leg with apex!=s).
 * Build: cc -O3 -march=native -o acute_sa acute_sa.c -lpthread
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#include <pthread.h>

typedef uint32_t u32;
#define MAXM 512

static int N,M; static u32 UNIV; static double TLIMIT; static int NTHREADS;

typedef struct { uint64_t s0,s1; } rng_t;
static inline uint64_t rnext(rng_t* r){ uint64_t x=r->s0,y=r->s1; r->s0=y; x^=x<<23; r->s1=x^y^(x>>17)^(y>>26); return r->s1+y; }
static inline u32 rr(rng_t* r,u32 m){ return m? (u32)(rnext(r)%m):0; }
static inline double rdbl(rng_t* r){ return (rnext(r)>>11)*(1.0/9007199254740992.0); }

/* right angle between vectors at apex Q for P,R: ((P^Q)&(R^Q))==0 */
/* energy contribution of slot s in S (triples that involve s, each unordered triple counted once
   from its apex's perspective; but for the move-delta we need ALL triples touching s, counted such
   that summing the per-slot 'touch' is consistent). We define a symmetric per-PAIR-with-apex count:
   total E = sum over apex j, pairs a<b (a,b!=j) of [right]. A change at slot s affects terms where
   j==s (apex), or (a==s or b==s) with j!=s. We compute those exactly. */
static long energy_full(const u32* S){
    long e=0;
    for(int j=0;j<M;j++){ u32 Q=S[j];
        for(int a=0;a<M;a++){ if(a==j)continue; u32 xa=S[a]^Q;
            for(int b=a+1;b<M;b++){ if(b==j)continue; if((xa&(S[b]^Q))==0) e++; }}}
    return e;
}
/* energy of all triples involving slot s, given current S (S[s] is current value) */
static long energy_slot(const u32* S,int s){
    long e=0;
    /* apex = s */
    u32 Q=S[s];
    for(int a=0;a<M;a++){ if(a==s)continue; u32 xa=S[a]^Q;
        for(int b=a+1;b<M;b++){ if(b==s)continue; if((xa&(S[b]^Q))==0) e++; }}
    /* s is a leg, apex j!=s, other leg c!=s,!=j */
    for(int j=0;j<M;j++){ if(j==s)continue; u32 Qj=S[j]; u32 xs=S[s]^Qj;
        for(int c=0;c<M;c++){ if(c==s||c==j)continue; if((xs&(S[c]^Qj))==0) e++; }
    }
    /* the above double-counts nothing: apex=s set is disjoint from apex!=s set. Within apex!=s,
       each (j; s,c) with c iterating counts the pair {s,c} once. Good. */
    return e;
}

static volatile int g_found=0;
static u32 g_sol[MAXM]; static long g_bestE=1L<<60; static int g_solM=0;
static pthread_mutex_t mu=PTHREAD_MUTEX_INITIALIZER;
static double now(){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+ts.tv_nsec*1e-9; }

/* seeds (acute sets dim N), used to initialize */
#define MAXSEEDS 64
static u32 seeds[MAXSEEDS][MAXM]; static int seedlen[MAXSEEDS]; static int nseed=0;

static int contains(const u32* S,int m,u32 x){ for(int i=0;i<m;i++) if(S[i]==x)return 1; return 0; }

typedef struct{int tid; rng_t rng;} targ_t;

static void* worker(void* p){
    targ_t* t=(targ_t*)p; rng_t* rng=&t->rng;
    u32 S[MAXM];
    double t0=now();
    while(!g_found && now()-t0<TLIMIT){
        /* init: from a seed (pad with random distinct) or fully random distinct */
        int m=0;
        if(nseed>0 && rr(rng,2)==0){
            int si=rr(rng,nseed); int sl=seedlen[si];
            for(int i=0;i<sl && m<M;i++) S[m++]=seeds[si][i];
        }
        while(m<M){ u32 x=rr(rng,UNIV+1); if(!contains(S,m,x)) S[m++]=x; }
        long E=energy_full(S);
        double T=2.0;          /* initial temperature */
        double Tmin=0.02;
        long iters=0;
        long bestE=E;
        while(!g_found && E>0){
            iters++;
            if((iters&4095)==0){
                if(now()-t0>=TLIMIT) break;
                T*= 0.9999; if(T<Tmin) T=Tmin;
            }
            /* propose: replace slot s with new distinct vector y */
            int s=rr(rng,M);
            u32 old=S[s];
            u32 y;
            int tries=0;
            do{
                if(rr(rng,2)==0) y=rr(rng,UNIV+1);            /* random */
                else y= old ^ (1u<<rr(rng,N));                  /* flip one bit (neighbor) */
                tries++;
            } while(contains(S,M,y) && tries<8);
            if(contains(S,M,y)) continue;
            long e_old=energy_slot(S,s);
            S[s]=y;
            long e_new=energy_slot(S,s);
            long dE=e_new-e_old;
            if(dE<=0 || rdbl(rng)<exp(-(double)dE/T)){
                E+=dE;
                if(E<bestE){ bestE=E; }
                if(E<=0){ /* solution */
                    pthread_mutex_lock(&mu);
                    if(!g_found){ memcpy(g_sol,S,M*sizeof(u32)); g_solM=M; g_bestE=0; g_found=1; }
                    pthread_mutex_unlock(&mu);
                    break;
                }
            } else {
                S[s]=old; /* reject */
            }
            /* periodic reheat if stuck */
            if((iters&65535)==0 && E>bestE){ T=1.5; }
        }
        if(bestE<g_bestE){ pthread_mutex_lock(&mu); if(bestE<g_bestE){ g_bestE=bestE; } pthread_mutex_unlock(&mu); }
    }
    return NULL;
}

static int read_set(const char* path,u32* out){
    FILE* f=fopen(path,"r"); if(!f) return 0; char line[512]; int nv=0,Md=-1;
    while(fgets(line,sizeof line,f)){ int bit=0; u32 v=0; int any=0;
        for(char*c=line;*c;c++) if(*c=='0'||*c=='1'){ if(*c=='1'&&bit<N)v|=(1u<<bit); bit++; any=1; }
        if(any){ if(Md<0)Md=bit; out[nv++]=v; } }
    fclose(f); return nv;
}

int main(int argc,char**argv){
    if(argc<4){ fprintf(stderr,"usage: %s N M TLIMIT [NTHREADS] [--seed FILE]...\n",argv[0]); return 2; }
    N=atoi(argv[1]); M=atoi(argv[2]); TLIMIT=atof(argv[3]); NTHREADS=8;
    UNIV=(N>=32)?0xFFFFFFFFu:((1u<<N)-1);
    int ai=4; if(ai<argc && argv[ai][0]!='-'){ NTHREADS=atoi(argv[ai]); ai++; }
    while(ai<argc){ if(!strcmp(argv[ai],"--seed")&&ai+1<argc){ u32 s[MAXM]; int c=read_set(argv[ai+1],s);
            if(c>0 && nseed<MAXSEEDS){ int k=c<M?c:M; memcpy(seeds[nseed],s,k*sizeof(u32)); seedlen[nseed]=k; nseed++; fprintf(stderr,"seed %s -> %d vecs\n",argv[ai+1],k);} ai+=2; } else ai++; }
    fprintf(stderr,"SA N=%d M=%d threads=%d seeds=%d tlimit=%.0f\n",N,M,NTHREADS,nseed,TLIMIT);
    pthread_t th[64]; targ_t ta[64];
    for(int i=0;i<NTHREADS;i++){ ta[i].tid=i; ta[i].rng.s0=0x243F6A8885A308D3ull*(i*2+1)+7; ta[i].rng.s1=0x13198A2E03707344ull*(i*5+3)+11; for(int w=0;w<9;w++)rnext(&ta[i].rng); pthread_create(&th[i],NULL,worker,&ta[i]); }
    for(int i=0;i<NTHREADS;i++) pthread_join(th[i],NULL);
    if(g_found){ /* verify internally */
        long e=energy_full(g_sol);
        fprintf(stderr,"SA FOUND acute set size %d (energy %ld)\n",M,e);
        if(e!=0){ fprintf(stderr,"INTERNAL ERROR energy!=0\n"); return 1; }
        for(int i=0;i<M;i++){ for(int b=0;b<N;b++) printf("%d%s",(g_sol[i]>>b)&1,b+1<N?" ":""); printf("\n"); }
        return 0;
    }
    fprintf(stderr,"SA no full solution; best residual energy=%ld\n",g_bestE);
    return 3;
}
