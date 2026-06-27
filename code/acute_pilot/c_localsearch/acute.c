/* OEIS A089676 acute-set local search.
 * S subset of {0,1}^n. Right angle at apex Q between P,R iff ((P^Q)&(R^Q))==0.
 * S acute iff no ordered triple (apex,leg,leg) has a right angle.
 * Equivalent symmetric condition checked on add: for candidate x and current set,
 * for every PAIR of distinct points (including x) we must avoid right angle at every apex.
 *
 * can_add(x): adding x is safe iff:
 *   (A) no right angle with apex x:  for all a<b in S, ((S[a]^x)&(S[b]^x))!=0
 *   (B) no right angle with apex in S and one leg x: for all q in S, for all a in S (a!=q),
 *         ((x^S[q]) & (S[a]^S[q])) != 0
 * Build: cc -O3 -march=native -o acute acute.c -lpthread
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>
#include <pthread.h>

typedef uint32_t u32;

static int N;            /* dimension */
static int TARGET;       /* desired size */
static double TLIMIT;    /* seconds */
static int NTHREADS;

/* xorshift128+ per thread */
typedef struct { uint64_t s0,s1; } rng_t;
static inline uint64_t rnext(rng_t* r){
    uint64_t x=r->s0, y=r->s1; r->s0=y;
    x^=x<<23; r->s1=x^y^(x>>17)^(y>>26);
    return r->s1+y;
}
static inline u32 rint(rng_t* r,u32 m){ return (u32)(rnext(r)%m); }

/* check if x can be added to set arr[0..m-1] (all acute already) keeping acute */
static inline int can_add(const u32* arr,int m,u32 x){
    /* (A) apex x */
    for(int a=0;a<m;a++){
        u32 xa = arr[a]^x;
        for(int b=a+1;b<m;b++){
            if((xa & (arr[b]^x))==0) return 0;
        }
    }
    /* (B) apex q in S, legs x and arr[a] */
    for(int q=0;q<m;q++){
        u32 xq = x^arr[q];
        for(int a=0;a<m;a++){
            if(a==q) continue;
            if((xq & (arr[a]^arr[q]))==0) return 0;
        }
    }
    return 1;
}

/* full acute check of arr[0..m-1] */
static int is_acute(const u32* arr,int m){
    for(int j=0;j<m;j++){
        u32 Q=arr[j];
        for(int a=0;a<m;a++){ if(a==j)continue; u32 xa=arr[a]^Q;
            for(int b=a+1;b<m;b++){ if(b==j)continue;
                if((xa & (arr[b]^Q))==0) return 0; }}
    }
    return 1;
}

static volatile int g_found=0;
static u32 g_best_set[4096];
static int g_best_size=0;
static pthread_mutex_t g_mu=PTHREAD_MUTEX_INITIALIZER;

typedef struct { int tid; rng_t rng; u32* seeds; int nseeds; int seedlen; } targ_t;

/* greedy fill from a partial set, random candidate order */
static int greedy_fill(u32* arr,int m,rng_t* rng){
    u32 universe = (N>=32)?0xFFFFFFFFu:((1u<<N)-1);
    /* random scan order over all 2^N vertices via random start + odd stride */
    u32 size = universe+1; /* careful: if N==32 this overflows; N<=15 here so fine */
    u32 start = rint(rng,size);
    u32 stride = (rint(rng,size/2)*2+1)&universe; if(stride==0)stride=1;
    u32 v=start;
    for(u32 cnt=0;cnt<size;cnt++){
        u32 x=v;
        v=(v+stride)&universe;
        /* skip if already in set */
        int in=0; for(int i=0;i<m;i++) if(arr[i]==x){in=1;break;}
        if(in) continue;
        if(can_add(arr,m,x)){ arr[m++]=x; if(m>=TARGET) break; }
    }
    return m;
}

static void report(u32* arr,int m){
    pthread_mutex_lock(&g_mu);
    if(m>g_best_size){ g_best_size=m; memcpy(g_best_set,arr,m*sizeof(u32)); }
    pthread_mutex_unlock(&g_mu);
}

static double now(){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+ts.tv_nsec*1e-9; }

static void* worker(void* p){
    targ_t* t=(targ_t*)p;
    rng_t* rng=&t->rng;
    u32 cur[4096];
    double t0=now();
    long iter=0;
    while(!g_found && now()-t0<TLIMIT){
        iter++;
        int m=0;
        /* seed: half the time from a provided seed set (split-down), else fresh */
        if(t->nseeds>0 && (rint(rng,2)==0)){
            int si=rint(rng,t->nseeds);
            u32* sd=t->seeds+si*t->seedlen;
            /* take a random subset of the seed (truncated to N dims already) */
            int keep=t->seedlen;
            for(int i=0;i<keep;i++) cur[m++]=sd[i] & ((N>=32)?0xFFFFFFFFu:((1u<<N)-1));
            /* dedup */
            int w=0; for(int i=0;i<m;i++){int dup=0;for(int k=0;k<w;k++)if(cur[k]==cur[i]){dup=1;break;}if(!dup)cur[w++]=cur[i];}
            m=w;
            /* it may not be acute after projection; trim greedily to an acute core */
            int mm=0; u32 tmp[4096];
            for(int i=0;i<m;i++){ if(can_add(tmp,mm,cur[i])) tmp[mm++]=cur[i]; }
            memcpy(cur,tmp,mm*sizeof(u32)); m=mm;
        }
        m=greedy_fill(cur,m,rng);
        if(m>=TARGET){ report(cur,m); g_found=1; break; }

        /* plateau local search: (1,k) swaps. Remove some, refill, keep if >=. */
        int best_local=m;
        u32 bestcur[4096]; memcpy(bestcur,cur,m*sizeof(u32));
        int noimp=0;
        while(!g_found && noimp<2000 && now()-t0<TLIMIT){
            memcpy(cur,bestcur,best_local*sizeof(u32));
            m=best_local;
            /* remove 1-3 random points */
            int rem=1+rint(rng,3);
            if(rem>=m) rem=1;
            for(int r=0;r<rem && m>0;r++){
                int idx=rint(rng,m);
                cur[idx]=cur[--m];
            }
            m=greedy_fill(cur,m,rng);
            if(m>best_local){ best_local=m; memcpy(bestcur,cur,m*sizeof(u32)); noimp=0;
                if(m>=TARGET){ report(cur,m); g_found=1; break; }
            } else if(m==best_local){ /* accept lateral move sometimes */
                if(rint(rng,2)==0) memcpy(bestcur,cur,m*sizeof(u32));
                noimp++;
            } else noimp++;
        }
        report(bestcur,best_local);
    }
    return NULL;
}

int main(int argc,char**argv){
    if(argc<4){ fprintf(stderr,"usage: %s N TARGET TLIMIT [NTHREADS] [seedfile]\n",argv[0]); return 2; }
    N=atoi(argv[1]); TARGET=atoi(argv[2]); TLIMIT=atof(argv[3]);
    NTHREADS=(argc>4)?atoi(argv[4]):8;
    u32* seeds=NULL; int nseeds=0,seedlen=0;
    if(argc>5){
        /* seedfile: lines of 0/1 (one vector). We read all into one flat seed of length=#lines, dims truncated to N */
        FILE* f=fopen(argv[5],"r"); if(f){
            char line[256]; u32 vecs[8192]; int nv=0;
            while(fgets(line,sizeof line,f)){
                int bit=0; u32 v=0; int any=0;
                for(char*c=line;*c;c++){ if(*c=='0'||*c=='1'){ if(*c=='1'&&bit<N)v|=(1u<<bit); if(bit<N)bit++; any=1; } }
                if(any && bit>0) vecs[nv++]=v;
            }
            fclose(f);
            /* single seed = the whole projected set */
            seeds=malloc(sizeof(u32)*nv); memcpy(seeds,vecs,sizeof(u32)*nv);
            nseeds=1; seedlen=nv;
            fprintf(stderr,"loaded seed: %d vectors projected to %d dims\n",nv,N);
        }
    }
    pthread_t th[64]; targ_t ta[64];
    for(int i=0;i<NTHREADS;i++){
        ta[i].tid=i; ta[i].rng.s0=0x9E3779B97F4A7C15ull*(i+1)+0x12345; ta[i].rng.s1=0xD1B54A32D192ED03ull*(i+7)+99;
        for(int w=0;w<5;w++) rnext(&ta[i].rng);
        ta[i].seeds=seeds; ta[i].nseeds=nseeds; ta[i].seedlen=seedlen;
        pthread_create(&th[i],NULL,worker,&ta[i]);
    }
    for(int i=0;i<NTHREADS;i++) pthread_join(th[i],NULL);

    fprintf(stderr,"BEST size=%d (target %d) for N=%d\n",g_best_size,TARGET,N);
    if(!is_acute(g_best_set,g_best_size)){ fprintf(stderr,"INTERNAL ERROR not acute\n"); return 1; }
    /* print best set as 0/1 rows to stdout */
    for(int i=0;i<g_best_size;i++){
        for(int b=0;b<N;b++) printf("%d%s", (g_best_set[i]>>b)&1, b+1<N?" ":"");
        printf("\n");
    }
    return 0;
}
